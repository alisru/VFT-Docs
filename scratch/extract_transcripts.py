import json

def extract_transcript(path):
    print(f"--- Extracting from {path} ---")
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                # Look for model responses that contain summaries
                if data.get("source") == "MODEL" and data.get("type") == "PLANNER_RESPONSE":
                    content = data.get("content", "")
                    if "###" in content:
                        print(f"Found summary in PLANNER_RESPONSE (step {data.get('step_index')}):")
                        print(content)
                        print("=" * 80)
                # Look for tool calls to send_message
                if "tool_calls" in data:
                    for tc in data["tool_calls"]:
                        if tc.get("name") == "send_message":
                            msg = tc.get("args", {}).get("Message", "")
                            if "###" in msg:
                                print(f"Found summary in send_message (step {data.get('step_index')}):")
                                print(msg)
                                print("=" * 80)
            except Exception as e:
                pass

extract_transcript("e:/Vector Field Theory/VFT Docs/scratch/subagent_c1_transcript.txt")
extract_transcript("e:/Vector Field Theory/VFT Docs/scratch/subagent_c3_transcript.txt")
