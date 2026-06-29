import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from batch_upload_notebooks import NotebookLMClient

SOURCES_TO_DELETE = [
    "57d686e1-0883-417e-89fd-6eb1fa6d579c",
    "ab34a733-5234-4916-b68c-347cf0059b1d",
    "d8c38980-073d-47cc-93fe-21700ec9034e",
    "bd8c42c5-9c09-45cd-a937-c4bcb4c82a18",
    "1f4a0524-85e7-4205-9457-a91423838ae6",
    "ba0aba52-12e1-4ab1-89ac-99a0d5f68072",
    "77629359-94a2-49fb-a296-f3a3cd7d0e6c",
    "8467d965-e889-401f-8e90-a07d3fc9f6b3",
    "ba885d33-32f4-4449-95b4-cf23041fc8e3",
    "5ae084bd-1c7a-4ee5-b2bd-ede9e6e883a0",
    "c584a680-856c-4a2c-9dea-c752bec2e1b7",
    "a40115a6-7922-4be7-8055-9e9ced7f94b8",
    "3b3ac8c9-0ce2-4cd4-a8c6-47d8d13d5dfa",
    "1d8f17ff-1c50-4cf3-9f98-0b5c6a71ad32",
    "e2fc6535-32ad-4e78-ba87-d475ecd710ba",
    "bc113117-25bf-41ee-b414-556445e2edc6",
    "d7640426-9861-4da4-953c-f47a7979132e",
    "361e4ddf-5584-4ada-9b68-3906177c04f8",
    "0b087695-0cf9-4b12-9e00-40291f39fd34",
    "de634139-c1a6-4017-ac92-d1c6162f8832",
    "efcd7588-8d83-4e01-9a83-e9432b9f9af0",
    "c8ab4dc8-3e74-4c7f-bce7-8ec807c1cc5c",
    "dafca842-ab7a-4ee3-a0cc-07bb6720fc95",
    "570f4906-20a7-4e4e-86e5-e2fb1101f3c6",
    "47f94d64-08f3-4e54-90c3-06b716ab0cf1",
    "ec5a7886-f46e-465a-9243-1c48c5ade05f"
]

def main():
    executable = r"E:\Python\Scripts\notebooklm-mcp.exe"
    print("Spawning NotebookLM MCP server for cleanup...", flush=True)
    client = NotebookLMClient(executable)
    
    for i, source_id in enumerate(SOURCES_TO_DELETE):
        print(f"[{i+1}/{len(SOURCES_TO_DELETE)}] Deleting plans/tasks source UUID: {source_id}...", flush=True)
        try:
            client.call_tool("source_delete", {"source_id": source_id, "confirm": True})
            print("Successfully deleted.")
        except Exception as e:
            print(f"Error deleting: {e}")
            
    print("Cleanup completed.")
    client.close()

if __name__ == "__main__":
    main()
