"""
Configuration manager for Chat Context:
Handles optional cloud synchronization settings (Google Drive via rclone and Git auto-backup)
for both Canvases and Chat conversations.
"""
import json
from pathlib import Path
from typing import Any, Dict

from .db import ROOT

CONFIG_PATH = ROOT / "config.json"
EXAMPLE_CONFIG_PATH = ROOT / "config.example.json"

DEFAULT_CONFIG: Dict[str, Any] = {
    "git_sync": {
        "enabled": False,
        "remote": "origin",
        "branch": "main",
        "repo_url": ""
    },
    "gdrive_sync": {
        "enabled": False,
        "rclone_remote": "gdrive",
        "folder_name": "Canvases",
        "root_folder_id": ""
    },
    "chat_git_sync": {
        "enabled": False,
        "remote": "origin",
        "branch": "main",
        "repo_url": "",
        "export_dir": "exports/chats"
    },
    "chat_gdrive_sync": {
        "enabled": False,
        "rclone_remote": "gdrive",
        "folder_name": "AI_Chats",
        "root_folder_id": "",
        "export_dir": "exports/chats"
    }
}


def load_config() -> Dict[str, Any]:
    """Loads configuration from config.json, merging with safe defaults."""
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    if CONFIG_PATH.exists():
        try:
            user_cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            if isinstance(user_cfg, dict):
                for k, v in user_cfg.items():
                    if k in cfg and isinstance(v, dict):
                        cfg[k].update(v)
                    else:
                        cfg[k] = v
        except Exception as e:
            print(f"[config] Warning: Failed to parse {CONFIG_PATH}: {e}", flush=True)
    return cfg


def save_config(cfg: Dict[str, Any]) -> None:
    """Saves updated configuration to config.json."""
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


def get_git_config() -> Dict[str, Any]:
    return load_config().get("git_sync", DEFAULT_CONFIG["git_sync"])


def get_gdrive_config() -> Dict[str, Any]:
    return load_config().get("gdrive_sync", DEFAULT_CONFIG["gdrive_sync"])


def get_chat_git_config() -> Dict[str, Any]:
    return load_config().get("chat_git_sync", DEFAULT_CONFIG["chat_git_sync"])


def get_chat_gdrive_config() -> Dict[str, Any]:
    return load_config().get("chat_gdrive_sync", DEFAULT_CONFIG["chat_gdrive_sync"])
