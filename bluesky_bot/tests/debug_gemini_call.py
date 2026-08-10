import os
import sys
import json
from dotenv import load_dotenv

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google import genai
from google.genai import types

load_dotenv(".env")
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in env.")
    sys.exit(1)

# Import helper to get system instruction and user prompt format
from google_ai_studio_one_shot import _load_rules, transpose_flat_to_json

def run_debug():
    candidates_path = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\harvested_candidates.json"
    if not os.path.exists(candidates_path):
        print(f"Error: Candidates file {candidates_path} not found.")
        sys.exit(1)
        
    with open(candidates_path, "r", encoding="utf-8") as f:
        all_candidates = json.load(f)
        
    # Take the first 2 candidates (representing batch size = 2)
    candidates = all_candidates[:2]
    print(f"Loaded {len(candidates)} candidates for debugging.")
    
    use_son = True
    use_search = True
    thinking_level = "HIGH"
    
    # 1. Load rules
    convergence_rules, formatting_rules = _load_rules(use_son=use_son)
    
    # 2. Build system instruction
    system_instruction = (
        "You are the Master Aletheia Auditor. Respond ONLY with the exact delimited data rows requested. No commentary, no markdown, no preamble, no explanation. "
        "Use Google Search ONLY to fact-check names, dates, and medical/legal claims from the article. Do NOT use search results to alter your structural analysis or your Alethekanon persona. "
        "You are strictly forbidden from inventing, guessing, or inferring specific details not explicitly written in the text or verified by search. "
        "Adhere to a strict budget of AT MOST 1 search query per story to stay within API quota limits. "
        "If you used Google Search to verify any information in your response for a candidate, you MUST append the emoji 🌐 at the end of the first post (post 1) of that candidate's thread, and you should mention/cite the verified facts or source details in the Alethekanon post (post 11) if relevant. "
        "CRITICAL: EVERY SINGLE POST IN THE THREAD MUST BE UNDER 270 CHARACTERS. THIS IS A HARD LIMIT. BE CONCISE."
    )
    
    # 3. Build output format demand
    n = len(candidates)
    expected_len = 25 if use_son else 17
    
    output_format = (
        f"OUTPUT FORMAT — YOUR ENTIRE RESPONSE MUST BE A SINGLE VALID JSON LIST OF LISTS. NO commentary, NO markdown formatting (other than JSON code fences if desired), NO explanation.\n"
        f"The JSON array must contain exactly {n} elements (one per candidate, in the same order). Each element must be a list of exactly {expected_len} items representing the evaluation of that candidate in this specific structure:\n"
        "[\n"
        "  [\n"
        '    "thinking",                                // item[0]: detailed thinking/scratchpad calculations (Phase 1 to 5 calculations)\n'
        '    "id",                                      // item[1]: clean story id slug\n'
        '    "subject",                                 // item[2]: story subject\n'
        '    "link",                                    // item[3]: story link\n'
        '    "target_url",                              // item[4]: reply target post url\n'
        "    claim_u (float),                           // item[5]: stated morality\n"
        "    claim_psi (float),                         // item[6]: stated will\n"
        "    real_u (float),                            // item[7]: actual morality\n"
        "    real_psi (float),                          // item[8]: actual will\n"
        '    "mode",                                    // item[9]: root or reply\n'
        "    [\n"
        '      "post 1 (under 260 chars, ending with 1-2 hashtags)",\n'
        '      "post 2 (under 260 chars)",\n'
        "      ...\n"
        "      (exactly 13 posts)                       // item[10]: posts array\n"
        "    ],\n"
        '    ["Actor / Org / Geopolitical tag", ...],  // item[11]: actors array\n'
        '    "macro_event",                             // item[12]: overarching context name or "" if none\n'
        "    macro_claim_u (float or null),             // item[13]: macro stated morality, null if none\n"
        "    macro_claim_psi (float or null),           // item[14]: macro stated will, null if none\n"
        "    macro_real_u (float or null),              // item[15]: macro actual morality, null if none\n"
        "    macro_real_psi (float or null)"            # item[16]
    )
    if use_son:
        output_format += (
            ",\n"
            "    claim_rnet (float),                        // item[17]: stated R_net integrity score\n"
            "    real_rnet (float),                         // item[18]: actual R_net integrity score\n"
            "    claim_z (int),                             // item[19]: stated uncertainty score (blank count, sum of blank counts across planes)\n"
            "    real_z (int),                              // item[20]: actual uncertainty score\n"
            "    claim_z_profile (7-number array of ints),  // item[21]: stated blank profile [B_Q1, B_Q2, B_Q3, B_Q4, B_Q5, B_Q6, B_Q7]\n"
            "    real_z_profile (7-number array of ints),   // item[22]: actual blank profile\n"
            '    "claim_integrity",                         // item[23]: stated integrity label mapped from claim_rnet\n'
            '    "real_integrity"                           // item[24]: actual integrity label mapped from real_rnet\n'
        )
    output_format += (
        "\n"
        "  ]\n"
        "]\n\n"
        "CRITICAL FOR MACRO CONTEXT:\n"
        "Identify if the candidate news story exists within a distinct overarching macro-event context. If so, provide the macro-event name in item[12] and evaluate its stated and actual u/psi coordinates in items[13] to [16]. If no distinct macro-context exists, use empty string for item[12] and null for items[13] to [16].\n\n"
        "item[11] = actors array: principal named individuals, orgs, nation-states, or blocs (CRINK/BRICS/NATO/AUKUS/G7/SCO/Five Eyes) the story is ABOUT. Canonical full names. Max 6. [] if none.\n\n"
    )
    
    user_payload = [
        f"=== CONVERGENCE TEST RULES ===\n{convergence_rules}\n\n",
        f"=== THREAD FORMATTING & SCHEMAS ===\n{formatting_rules}\n\n",
        f"=== CANDIDATES TO EVALUATE ({n} total) ===\n{json.dumps(candidates, separators=(',', ':'), ensure_ascii=False)}\n\n",
        f"{output_format}"
    ]
    user_payload_str = "".join(user_payload)
    
    # 4. Initialize client
    print("Initializing Client...")
    client = genai.Client(api_key=api_key)
    
    # 5. Build GenerateContentConfig
    safety_settings = [
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=types.HarmBlockThreshold.BLOCK_NONE
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=types.HarmBlockThreshold.BLOCK_NONE
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=types.HarmBlockThreshold.BLOCK_NONE
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=types.HarmBlockThreshold.BLOCK_NONE
        ),
    ]
    
    tools_list = [types.Tool(google_search=types.GoogleSearch())] if use_search else None
    
    thinking_config = types.ThinkingConfig(thinking_level="HIGH")
    
    config = types.GenerateContentConfig(
        temperature=0.15,
        max_output_tokens=8192,
        system_instruction=system_instruction,
        safety_settings=safety_settings,
        tools=tools_list,
        thinking_config=thinking_config
    )
    
    print("Calling Gemini model gemini-3.5-flash...")
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=user_payload_str,
            config=config
        )
        print("Call completed successfully!")
        
        # Save output to debug_output.txt
        out_path = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\tests\debug_output.txt"
        with open(out_path, "w", encoding="utf-8") as out_f:
            out_f.write("=== RESPONSE TEXT ===\n")
            out_f.write(response.text or "EMPTY")
            out_f.write("\n\n=== RESPONSE OBJECT STR ===\n")
            out_f.write(str(response))
        print(f"Raw response output successfully saved to {out_path}.")
        
    except Exception as e:
        print(f"API call failed with exception: {e}")

if __name__ == "__main__":
    run_debug()
