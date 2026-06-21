"""One-time backfill: tag existing story JSONs with actors[], category, and event.

Runs a cheap batched LLM pass (Gemini with Agnes AI fallback) over every story
that isn't already tagged, then writes `actors`, `category`, and `event` back
into each JSON. Idempotent — re-running only processes untagged stories unless
--force is given. The live harvest pipeline uses the deterministic extractor in
actor_extract.py instead; this script exists purely to clean up the historical
corpus where Title-Case RSS headlines defeat regex extraction.

Usage:
    python enrich_stories.py                # tag all untagged stories
    python enrich_stories.py --force        # re-tag everything
    python enrich_stories.py --chunk-size 20
    python enrich_stories.py --dry-run      # show what would change, write nothing
"""
import os
import sys
import json
import glob
import time
import argparse
import urllib.request

from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, ".env"))

try:
    import google.generativeai as genai
except ImportError:
    genai = None

CATEGORIES = ["general", "tech", "business", "politics", "science", "world"]

SYSTEM_INSTRUCTION = (
    "You are a precise entity tagger. For each news item you are given an id and a subject line. "
    "Respond ONLY with a single valid JSON list (no markdown, no commentary). Each element must be "
    'an object: {"id": "<same id>", "actors": ["Person or Org", ...], "category": "<one of: '
    + ", ".join(CATEGORIES) + '>", "event": "<2-5 word event label>"}. '
    "actors = the specific named people, organisations, or governing bodies the story is ABOUT "
    "(max 5, empty list if none are named). Do not invent names. category = best single fit. "
    "event = a short canonical label for the underlying event so related stories can be grouped."
)


def get_gemini():
    key = os.environ.get("GEMINI_API_KEY")
    if not key or genai is None:
        return None
    genai.configure(api_key=key)
    return genai


def call_agnes(api_key, system_prompt, user_content, model="agnes-2.0-flash"):
    url = "https://apihub.agnes-ai.com/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0.0,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as response:
        res = json.loads(response.read().decode("utf-8"))
    return res["choices"][0]["message"]["content"]


def call_model(genai_client, agnes_key, user_payload, model_name):
    fallbacks = [model_name, "gemini-3.5-flash", "gemini-2.5-flash", "gemini-2.5-flash-lite"]
    seen = []
    for m in fallbacks:
        if m not in seen:
            seen.append(m)
    if agnes_key:
        seen.append("agnes-2.0-flash")

    last = None
    for model in seen:
        try:
            if model.startswith("agnes"):
                return call_agnes(agnes_key, SYSTEM_INSTRUCTION, user_payload, model=model)
            if not genai_client:
                raise ValueError("Gemini client unavailable.")
            cfg = genai_client.types.GenerationConfig(temperature=0.0, max_output_tokens=4096)
            inst = genai_client.GenerativeModel(
                model_name=model, system_instruction=SYSTEM_INSTRUCTION, generation_config=cfg
            )
            return inst.generate_content(user_payload).text.strip()
        except Exception as e:
            print(f"  Model {model} failed: {e}")
            last = e
            time.sleep(1.5)
    raise RuntimeError(f"All models failed: {last}")


def parse_json_list(text):
    t = text.strip()
    if t.startswith("```json"):
        t = t[7:]
    elif t.startswith("```"):
        t = t[3:]
    if t.endswith("```"):
        t = t[:-3]
    t = t.strip()
    s, e = t.find("["), t.rfind("]")
    if s == -1 or e == -1:
        return []
    try:
        return json.loads(t[s:e + 1])
    except Exception as ex:
        print(f"  Warning: could not parse model JSON ({ex}).")
        return []


def load_story(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    cfg = data[0] if isinstance(data, list) else data
    return data, cfg


def save_story(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser(description="Backfill actors/category/event on story JSONs.")
    ap.add_argument("--chunk-size", type=int, default=20)
    ap.add_argument("--model", type=str, default="gemini-3.5-flash")
    ap.add_argument("--force", action="store_true", help="Re-tag stories even if already tagged.")
    ap.add_argument("--dry-run", action="store_true", help="Show changes without writing.")
    args = ap.parse_args()

    stories_dir = os.path.join(script_dir, "stories")
    paths = (
        glob.glob(os.path.join(stories_dir, "factcheck_*.json"))
        + glob.glob(os.path.join(stories_dir, "live", "factcheck_*.json"))
        + glob.glob(os.path.join(stories_dir, "darkroom", "factcheck_*.json"))
    )
    print(f"Found {len(paths)} story files.")

    # Build worklist of untagged (or all, if --force) stories.
    work = []
    for p in paths:
        try:
            data, cfg = load_story(p)
        except Exception as e:
            print(f"  Skip unreadable {os.path.basename(p)}: {e}")
            continue
        if not args.force and "actors" in cfg and "category" in cfg and "event" in cfg:
            continue
        sid = cfg.get("id") or os.path.basename(p)
        work.append({"path": p, "data": data, "cfg": cfg, "id": sid,
                     "subject": (cfg.get("subject") or "")[:200]})

    if not work:
        print("Nothing to tag. (Use --force to re-tag everything.)")
        return

    print(f"{len(work)} stories need tagging. Processing in chunks of {args.chunk_size}...")

    genai_client = get_gemini()
    agnes_key = os.environ.get("AGNES_API_KEY")
    if not genai_client and not agnes_key:
        print("ERROR: No GEMINI_API_KEY or AGNES_API_KEY found in environment. Cannot run LLM backfill.")
        sys.exit(1)

    tagged = 0
    for i in range(0, len(work), args.chunk_size):
        chunk = work[i:i + args.chunk_size]
        total_chunks = (len(work) + args.chunk_size - 1) // args.chunk_size
        print(f"\nChunk {i // args.chunk_size + 1}/{total_chunks} ({len(chunk)} stories)...")

        items = [{"id": w["id"], "subject": w["subject"]} for w in chunk]
        payload = "Tag these news items:\n" + json.dumps(items, ensure_ascii=False)

        try:
            raw = call_model(genai_client, agnes_key, payload, args.model)
        except Exception as e:
            print(f"  Chunk failed entirely: {e}. Skipping.")
            continue

        results = {str(r.get("id")): r for r in parse_json_list(raw) if isinstance(r, dict)}

        for w in chunk:
            r = results.get(str(w["id"]))
            if not r:
                print(f"  No tag returned for: {w['id']}")
                continue
            actors = [str(a).strip() for a in (r.get("actors") or []) if str(a).strip()][:5]
            category = str(r.get("category", "general")).strip().lower()
            if category not in CATEGORIES:
                category = "general"
            event = str(r.get("event", "")).strip()[:60]

            w["cfg"]["actors"] = actors
            w["cfg"]["category"] = category
            w["cfg"]["event"] = event

            print(f"  {w['id']}: actors={actors} category={category} event='{event}'")
            if not args.dry_run:
                save_story(w["path"], w["data"])
            tagged += 1

    print(f"\n{'(dry-run) Would tag' if args.dry_run else 'Tagged'} {tagged} stories.")
    if not args.dry_run:
        print("Run rebuild_registries.py to propagate the new fields into stories_registry.js.")


if __name__ == "__main__":
    main()
