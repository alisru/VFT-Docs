import os
import sys
import time
from notebooklm_mcp.api_client import NotebookLMClient
from notebooklm_mcp.auth import load_cached_tokens

sys.stdout.reconfigure(encoding='utf-8')

NOTEBOOK_ID = 'e2bd8f97-3dbe-484d-a30a-33fc087e5b01'
SHRUNK_DIR = r'e:\Vector Field Theory\VFT Docs\_VFT MD\bible\source_texts\shrunk'

FILES_TO_UPLOAD = [
    ('Greek_Grammar_Morphology_Codes.txt', 'Greek Grammar & Morphology Parsing Codes'),
    ('Hebrew_Grammar_Morphology_Codes.txt', 'Hebrew Grammar & Morphology Parsing Codes'),
    ('Biblical_Proper_Names_Index.txt', 'Biblical Proper Names & Historical Figures Index'),
    ('ESV_Tagged_Translation.txt', 'Tagged English Standard Version (ESV to Strongs)'),
    ('Greek_Lexicon_Extended_Strongs.txt', 'Greek Biblical Lexicon (Extended Strongs Dictionary)'),
    ('Hebrew_Lexicon_Extended_Strongs.txt', 'Hebrew Biblical Lexicon (Extended Strongs Dictionary)'),
    ('Greek_NT_Gospels_Mat-Jhn.txt', 'Greek New Testament: Gospels (Matthew - John)'),
    ('Greek_NT_Epistles_Act-Rev.txt', 'Greek New Testament: Acts, Epistles & Revelation'),
    ('Hebrew_OT_History_Jos-Est.txt', 'Hebrew Old Testament: Historical Books (Joshua - Esther)'),
    ('Hebrew_OT_Wisdom_Job-Sng.txt', 'Hebrew Old Testament: Wisdom & Poetry (Job - Song of Songs)'),
    ('Hebrew_OT_Torah_Gen-Deu.txt', 'Hebrew Old Testament: Torah (Genesis - Deuteronomy)'),
    ('Hebrew_OT_Prophets_Isa-Mal.txt', 'Hebrew Old Testament: Prophets (Isaiah - Malachi)'),
]

def main():
    print("Loading NotebookLM authentication...")
    auth = load_cached_tokens()
    if not auth:
        print("ERROR: Failed to load cached auth tokens.")
        return

    client = NotebookLMClient(
        cookies=auth.cookies,
        csrf_token=auth.csrf_token,
        session_id=auth.session_id
    )

    print(f"Connecting to notebook: {NOTEBOOK_ID}")
    
    success_count = 0
    fail_count = 0

    for idx, (filename, title) in enumerate(FILES_TO_UPLOAD, 1):
        fp = os.path.join(SHRUNK_DIR, filename)
        if not os.path.exists(fp):
            print(f"[{idx}/{len(FILES_TO_UPLOAD)}] SKIP: File not found: {fp}")
            continue

        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()

        chars = len(text)
        words = len(text.split())
        print(f"\n[{idx}/{len(FILES_TO_UPLOAD)}] Uploading: '{title}' ({words:,} words, {chars:,} chars)...")

        retries = 3
        uploaded = False
        for attempt in range(1, retries + 1):
            try:
                res = client.add_text_source(
                    notebook_id=NOTEBOOK_ID,
                    text=text,
                    title=title
                )
                if res is not None:
                    print(f"  -> SUCCESS! Source added. Response: {res}")
                    uploaded = True
                    success_count += 1
                    break
                else:
                    print(f"  -> Attempt {attempt}: Received None response. Retrying...")
            except Exception as e:
                print(f"  -> Attempt {attempt} error: {e}")
            time.sleep(3)

        if not uploaded:
            print(f"  -> FAILED to upload '{title}' after {retries} attempts.")
            fail_count += 1

        # Generous cooldown between large uploads
        time.sleep(2)

    print("\n" + "=" * 50)
    print(f"Upload Complete! Successfully uploaded: {success_count}/{len(FILES_TO_UPLOAD)} (Failed: {fail_count})")
    print("=" * 50)

if __name__ == '__main__':
    main()
