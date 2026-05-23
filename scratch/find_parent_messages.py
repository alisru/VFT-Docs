import json
import os

def find_parent_messages():
    parent_log = "C:/Users/hungh/.gemini/antigravity/brain/44f19dea-857b-4620-9363-cef56bb6dbab/.system_generated/logs/transcript.jsonl"
    if not os.path.exists(parent_log):
        print(f"Parent log does not exist at {parent_log}")
        return
        
    print(f"Scanning parent log: {parent_log}")
    with open(parent_log, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                # Look for messages received from subagents or user
                if data.get("type") in ("USER_INPUT", "SUBAGENT_RESPONSE", "MESSAGE_RECEIVE"):
                    content = data.get("content", "")
                    if "###" in content or "Plane:" in content:
                        print(f"[{data.get('type')} - Step {data.get('step_index')}]")
                        print(content[:500] + "...")
                        print("=" * 40)
                # Look for tool call results or execution results
                if "tool_calls" in data:
                    for tc in data["tool_calls"]:
                        # check if it's send_message or similar
                        pass
            except Exception as e:
                pass

if __name__ == "__main__":
    find_parent_messages()
