import json
import re

def extract_to_file():
    extracted = []
    
    # Let's inspect subagent_c1_transcript.txt
    c1_path = "e:/Vector Field Theory/VFT Docs/scratch/subagent_c1_transcript.txt"
    print(f"Reading {c1_path}...")
    with open(c1_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                # In subagent_c1, there is a step where it outputs the full response (step 9)
                if data.get("source") == "MODEL" and data.get("type") == "PLANNER_RESPONSE":
                    content = data.get("content", "")
                    if "###" in content:
                        extracted.append(("c1_planner_response", content))
                # Also check tool_calls
                if "tool_calls" in data:
                    for tc in data["tool_calls"]:
                        if tc.get("name") == "send_message":
                            msg = tc.get("args", {}).get("Message", "")
                            if "###" in msg:
                                extracted.append(("c1_send_message", msg))
            except Exception as e:
                pass

    # Let's inspect subagent_c3_transcript.txt
    c3_path = "e:/Vector Field Theory/VFT Docs/scratch/subagent_c3_transcript.txt"
    print(f"Reading {c3_path}...")
    with open(c3_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                # In subagent_c3, it generated the response but maybe it got truncated. Let's see what is in PLANNER_RESPONSE
                if data.get("source") == "MODEL" and data.get("type") == "PLANNER_RESPONSE":
                    content = data.get("content", "")
                    if "###" in content:
                        extracted.append(("c3_planner_response", content))
                if "tool_calls" in data:
                    for tc in data["tool_calls"]:
                        if tc.get("name") == "send_message":
                            msg = tc.get("args", {}).get("Message", "")
                            if "###" in msg:
                                extracted.append(("c3_send_message", msg))
            except Exception as e:
                pass
                
    # Write everything extracted to a file in scratch
    out_path = "e:/Vector Field Theory/VFT Docs/scratch/batch_c_extracted.txt"
    with open(out_path, 'w', encoding='utf-8') as out_f:
        for source, text in extracted:
            out_f.write(f"=== SOURCE: {source} ===\n")
            out_f.write(text)
            out_f.write("\n\n" + "="*80 + "\n\n")
            
    print(f"Extracted {len(extracted)} summary blocks to {out_path}")

if __name__ == "__main__":
    extract_to_file()
