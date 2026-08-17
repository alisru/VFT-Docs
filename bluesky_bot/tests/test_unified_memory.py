"""test_unified_memory.py — Automated verification test for Aletheia Topic Threading & Memory Engine.
"""
import os
import sys
import json
import unittest

script_dir = os.path.dirname(os.path.abspath(__file__))
bot_dir = os.path.dirname(script_dir)
workspace_dir = os.path.dirname(bot_dir)
sys.path.insert(0, bot_dir)
sys.path.insert(0, os.path.join(workspace_dir, "Semantic_Clusters"))

import memory_store
import chat_server

class TestUnifiedMemoryEngine(unittest.TestCase):

    def test_01_sqlite_memory_and_archive_search(self):
        """Test SQLite FTS5 database creation and search."""
        stats = memory_store.get_memory_stats()
        self.assertGreater(stats["archive_documents"], 0)
        self.assertGreater(stats["archive_chunks"], 0)

        # Search for known concept in archive
        res = memory_store.search_archive_logs("gender roles", limit=2)
        self.assertTrue(len(res) > 0)
        self.assertIn("filename", res[0])

        # Test creating structured memory
        mem = memory_store.create_memory("Test actualism observation", category="test", tags=["#vft", "#actualism"], coords_u=1.2, coords_psi=0.8)
        self.assertIn("id", mem)

        # Search memories
        mem_search = memory_store.search_memories("actualism", category="test")
        self.assertTrue(len(mem_search) > 0)

    def test_02_session_migration_and_thread_branching(self):
        """Test hierarchical multi-thread branching and migration."""
        test_session_id = "test_s_001"
        session = chat_server.load_session(test_session_id)
        
        # Verify structure
        self.assertIn("threads", session)
        self.assertIn("main", session["threads"])
        self.assertEqual(session["active_thread_id"], "main")

        # Append messages to main trunk
        session["threads"]["main"]["messages"].append({
            "role": "user",
            "content": "Message 1: Baseline economics"
        })
        session["threads"]["main"]["messages"].append({
            "role": "model",
            "content": "Message 2: Baseline response"
        })
        chat_server.save_session(session)

        # Create sub-thread
        new_tid = "thread_deepdive"
        session["threads"][new_tid] = {
            "id": new_tid,
            "name": "Economics Deep Dive",
            "parent_thread_id": "main",
            "fork_message_index": 1,
            "created_at": "2026-08-15T00:00:00Z",
            "messages": [
                {"role": "user", "content": "Deep dive question on interest rates"},
                {"role": "model", "content": "Detailed calculation (-0.5, 0.2)"}
            ]
        }
        session["active_thread_id"] = new_tid
        chat_server.save_session(session)

        # Verify reload
        reloaded = chat_server.load_session(test_session_id)
        self.assertIn("thread_deepdive", reloaded["threads"])
        self.assertEqual(reloaded["active_thread_id"], "thread_deepdive")

        # Cleanup test session
        path = os.path.join(chat_server.SESSIONS_DIR, f"session_{test_session_id}.json")
        if os.path.exists(path):
            os.remove(path)

    def test_03_mcp_servers_import(self):
        """Verify both MCP servers import cleanly with their respective tools."""
        import aletheia_mcp_server
        self.assertIsNotNone(aletheia_mcp_server.mcp)

        import vft_mcp_server
        self.assertIsNotNone(vft_mcp_server.mcp)


if __name__ == "__main__":
    unittest.main()
