import json
import os

def find_responses():
    parent_log = "C:/Users/hungh/.gemini/antigravity/brain/44f19dea-857b-4620-9363-cef56bb6dbab/.system_generated/logs/transcript.jsonl"
    if not os.path.exists(parent_log):
        print("Parent log not found")
        return
        
    subagent_ids = ["3492bab1-7e9c-47a5-9af3-e44cc5e24615", "2402acad-2872-4426-84a2-136e31e689d1", "71fbee0a-b780-46c6-85f3-8c3507e17203"]
    
    print("Scanning log...")
    with open(parent_log, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                # Check for subagent responses or messages received
                content = data.get("content", "")
                if data.get("type") in ("SUBAGENT_RESPONSE", "MESSAGE_RECEIVE"):
                    print(f"[{data.get('type')} - Step {data.get('step_index')}]")
                    print(content[:500])
                    print("="*40)
                # Check tool calls
                if "tool_calls" in data:
                    for tc in data["tool_calls"]:
                        if tc.get("name") == "send_message":
                            print(f"[send_message in Step {data.get('step_index')}]")
                            print(str(tc.get("args"))[:500])
                            print("="*40)
            except Exception as e:
                pass

if __name__ == "__main__":
    find_responses()
