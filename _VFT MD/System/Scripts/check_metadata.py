import zipfile
import re
import os

docx_path = r"e:\Vector Field Theory\VFT Docs\Protocols\The Alethekanon Pulse Protocol.docx"

print(f"Inspecting {docx_path} for Image Alt Text...")

try:
    with zipfile.ZipFile(docx_path, 'r') as z:
        print("Files in ZIP:")
        for name in z.namelist():
            if 'embeddings' in name:
                print(f"Found Embedding: {name}")
            if 'math' in name.lower():
                print(f"Found Math-related file: {name}")
        
        # Also check one more document for OMML just to be 100% sure
        # (Already did this for Pulse Protocol and it was 0)

except Exception as e:
    print(f"Error: {e}")

except Exception as e:
    print(f"Error: {e}")
