"""vft_mcp_server.py — Dedicated FastMCP Server for the VFT Corpus, Qdrant Vector Store & Discussion Archive.

## Usage
To connect to Claude Desktop or AGY, add to claude_desktop_config.json:
{
  "mcpServers": {
    "vft-vdb": {
      "command": "python",
      "args": ["e:/Vector Field Theory/VFT Docs/Semantic_Clusters/vft_mcp_server.py"]
    }
  }
}
"""
import os
import sys
import json
import glob
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(script_dir)
load_dotenv(os.path.join(workspace_dir, "bluesky_bot", ".env"))

# Import local SQLite memory engine
sys.path.insert(0, os.path.join(workspace_dir, "bluesky_bot"))
try:
    import memory_store
except ImportError:
    memory_store = None

# Qdrant Credentials from test_qdrant_search.py
QDRANT_URL = "https://182bf3c8-faf1-428e-a670-9fb5e705769f.australia-southeast1-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6YjAwZDY4MjctNjZhZS00ZjQ2LWEwMDItMmNjODQzZTNhZTkyIn0.ZAQZ69ZNkSnX1pp_SAmU5_XSHEGqQsCmxEmjCALdJXs"
COLLECTION_NAME = "vft_paragraphs"

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    try:
        from mcp.server import MCPServer as FastMCP
    except ImportError:
        FastMCP = None

if FastMCP is None:
    print("Warning: 'mcp' python package is not installed. Install via: pip install mcp", file=sys.stderr)

mcp = FastMCP("VFT Corpus & Vector DB") if FastMCP else None

_qdrant_client = None
_embedding_model = None

def _get_qdrant_and_model():
    global _qdrant_client, _embedding_model
    if _qdrant_client is None:
        try:
            from qdrant_client import QdrantClient
            _qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=10.0)
        except Exception as e:
            print(f"[VFT MCP] Qdrant connection warning: {e}", file=sys.stderr)
    if _embedding_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"[VFT MCP] SentenceTransformer load warning: {e}", file=sys.stderr)
    return _qdrant_client, _embedding_model


if mcp:
    @mcp.tool()
    def search_semantic_clusters(query: str, limit: int = 5) -> str:
        """Search the Qdrant Vector Database collection 'vft_paragraphs' for canonical VFT formulas, mathematical worldview proofs, and definitions."""
        client, model = _get_qdrant_and_model()
        if not client or not model:
            return json.dumps({"error": "Qdrant client or SentenceTransformer model unavailable."})

        try:
            query_vector = model.encode(query).tolist()
            search_result = client.query_points(
                collection_name=COLLECTION_NAME,
                query=query_vector,
                limit=limit,
                with_payload=True
            )
            results = []
            for p in search_result.points:
                results.append({
                    "score": round(float(p.score), 4),
                    "file": p.payload.get("file", "Unknown"),
                    "paragraph_index": p.payload.get("paragraph_index", 0),
                    "text": p.payload.get("text", "")
                })
            return json.dumps(results, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Vector search failed: {str(e)}"})

    @mcp.tool()
    def get_topic_clusters(topic: str = "") -> str:
        """Search and retrieve philosophical clusters, ism tags, and document mappings from Semantic_Clusters."""
        mapping_path = os.path.join(script_dir, "topic_ism_mapping.json")
        if not os.path.exists(mapping_path):
            return json.dumps({"error": "topic_ism_mapping.json not found."})

        try:
            with open(mapping_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not topic:
                # Return summary overview of top clusters
                keys = list(data.keys())[:30]
                return json.dumps({"total_clusters": len(data), "sample_topics": keys}, indent=2)

            q = topic.lower().strip()
            matched = {}
            for k, v in data.items():
                if q in k.lower():
                    matched[k] = v
                    if len(matched) >= 10:
                        break
            return json.dumps(matched if matched else {"message": f"No topic cluster matching '{topic}' found."}, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    def search_archive_logs(query: str, limit: int = 5) -> str:
        """Search 170+ Gemini and Claude discussion transcripts in '_AI files and chat logs/' using full-text FTS5 search."""
        if not memory_store:
            return json.dumps({"error": "memory_store module unavailable."})
        results = memory_store.search_archive_logs(query, limit=limit)
        return json.dumps(results, indent=2)

    @mcp.tool()
    def get_archive_file(filename: str) -> str:
        """Get the full raw content of a specific discussion log from '_AI files and chat logs/'."""
        ai_dir = os.path.join(workspace_dir, "_AI files and chat logs")
        target_path = os.path.join(ai_dir, os.path.basename(filename))
        if not os.path.exists(target_path):
            return json.dumps({"error": f"File '{filename}' not found in archive directory."})
        try:
            try:
                with open(target_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(target_path, "r", encoding="latin-1") as f:
                    content = f.read()
            return content
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.resource("vft://archive-stats")
    def get_archive_stats_resource() -> str:
        """Get statistics on indexed VFT discussion files and chunks."""
        if memory_store:
            return json.dumps(memory_store.get_memory_stats(), indent=2)
        return "{}"


if __name__ == "__main__":
    if mcp:
        mcp.run()
    else:
        print("MCP SDK not available. Run: pip install mcp")
