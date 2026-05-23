import os

def list_brain():
    brain_dir = "C:/Users/hungh/.gemini/antigravity/brain"
    if os.path.exists(brain_dir):
        print(f"Contents of {brain_dir}:")
        for item in os.listdir(brain_dir):
            path = os.path.join(brain_dir, item)
            print(f"- {item} ({'DIR' if os.path.isdir(path) else 'FILE'})")
            # If it's a conversation ID, list its contents
            if os.path.isdir(path) and len(item) == 36:
                print(f"  Contents of {item}:")
                for sub in os.listdir(path):
                    subpath = os.path.join(path, sub)
                    print(f"  - {sub} ({'DIR' if os.path.isdir(subpath) else 'FILE'})")
                    if sub == ".system_generated":
                        logs_path = os.path.join(subpath, "logs")
                        if os.path.exists(logs_path):
                            print(f"    Logs inside .system_generated:")
                            for logfile in os.listdir(logs_path):
                                print(f"    - {logfile}")
    else:
        print(f"{brain_dir} does not exist!")

list_brain()
