#!/usr/bin/env python3
"""
Chat Context — Cloud Sync Setup Wizard
Configures optional Google Drive sync (via rclone) and Git auto-backup for both Canvases and Chats.
Usage:
    python setup_sync.py
    python setup_sync.py --status
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

# Add project root to sys.path so we can import ctx modules directly
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ctx.config import CONFIG_PATH, load_config, save_config
from ctx.db import CANVASES_DIR

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def check_tool(name: str) -> bool:
    """Returns True if the CLI tool is available on PATH."""
    return shutil.which(name) is not None


def get_rclone_remotes():
    """Returns a list of configured rclone remotes, or empty list if none/error."""
    if not check_tool("rclone"):
        return []
    try:
        res = subprocess.run(["rclone", "listremotes"], capture_output=True, text=True, timeout=5)
        if res.returncode == 0:
            return [line.strip().rstrip(":") for line in res.stdout.splitlines() if line.strip()]
    except Exception:
        pass
    return []


def print_status():
    """Prints the current configuration status and CLI tool health."""
    cfg = load_config()
    print("\n" + "=" * 60)
    print("      Chat Context -- Current Sync & System Status")
    print("=" * 60)

    # Tool checks
    print("\n[System Tools]")
    tools = [
        ("git", "Git Version Control", check_tool("git")),
        ("rclone", "Rclone Cloud Sync", check_tool("rclone")),
        ("pandoc", "Pandoc Docx Converter (for Google Docs)", check_tool("pandoc")),
    ]
    for binary, desc, available in tools:
        status_icon = "[OK] Installed" if available else "[X] Missing"
        print(f"  - {binary:<8} ({desc}): {status_icon}")

    # Config status
    print(f"\n[Configuration File: {CONFIG_PATH}]")
    git_cfg = cfg.get("git_sync", {})
    gdrive_cfg = cfg.get("gdrive_sync", {})
    chat_git_cfg = cfg.get("chat_git_sync", {})
    chat_gdrive_cfg = cfg.get("chat_gdrive_sync", {})

    print("\n  1. Canvas Git Auto-Backup:")
    print(f"    - Enabled: {git_cfg.get('enabled', False)}")
    print(f"    - Remote:  {git_cfg.get('remote', 'origin')}")
    print(f"    - Branch:  {git_cfg.get('branch', 'main')}")
    print(f"    - Repo:    {git_cfg.get('repo_url') or '(Not configured)'}")
    is_git_repo = (CANVASES_DIR / ".git").exists()
    print(f"    - Canvases Local Repo: {'Initialized' if is_git_repo else 'Not initialized'}")

    print("\n  2. Canvas Google Drive Sync:")
    print(f"    - Enabled:        {gdrive_cfg.get('enabled', False)}")
    print(f"    - Rclone Remote:  {gdrive_cfg.get('rclone_remote', 'gdrive')}")
    print(f"    - Target Folder:  {gdrive_cfg.get('folder_name', 'Canvases')}")
    print(f"    - Root Folder ID: {gdrive_cfg.get('root_folder_id') or '(Default root)'}")

    print("\n  3. Chat Git Export & Backup:")
    print(f"    - Enabled:    {chat_git_cfg.get('enabled', False)}")
    print(f"    - Remote:     {chat_git_cfg.get('remote', 'origin')}")
    print(f"    - Branch:     {chat_git_cfg.get('branch', 'main')}")
    print(f"    - Repo:       {chat_git_cfg.get('repo_url') or '(Not configured)'}")
    print(f"    - Export Dir: {chat_git_cfg.get('export_dir', 'exports/chats')}")

    print("\n  4. Chat Google Drive Export:")
    print(f"    - Enabled:        {chat_gdrive_cfg.get('enabled', False)}")
    print(f"    - Rclone Remote:  {chat_gdrive_cfg.get('rclone_remote', 'gdrive')}")
    print(f"    - Target Folder:  {chat_gdrive_cfg.get('folder_name', 'AI_Chats')}")
    print(f"    - Root Folder ID: {chat_gdrive_cfg.get('root_folder_id') or '(Default root)'}")
    print("=" * 60 + "\n")


def run_interactive_wizard():
    print("\n" + "=" * 64)
    print("          Chat Context — Cloud Sync Setup Wizard")
    print("=" * 64)
    print("Configure automated backup of your canvases and chat history.")
    print("All sync operations run safely and non-destructively.\n")

    cfg = load_config()
    git_cfg = cfg.setdefault("git_sync", {})
    gdrive_cfg = cfg.setdefault("gdrive_sync", {})
    chat_git_cfg = cfg.setdefault("chat_git_sync", {})
    chat_gdrive_cfg = cfg.setdefault("chat_gdrive_sync", {})

    git_installed = check_tool("git")
    rclone_installed = check_tool("rclone")

    # --- 1. Canvas Git Auto-Backup ---
    print("\n--- 1. Canvas Git Auto-Backup ---")
    print("Automatically commits and pushes generated canvases to a GitHub/GitLab repo.")
    if not git_installed:
        print("[!] Note: 'git' was not found on your system PATH.")

    cur_git_en = git_cfg.get("enabled", False)
    enable_git_input = input(f"Enable Git auto-backup for canvases? [y/N] (currently: {'yes' if cur_git_en else 'no'}): ").strip().lower()
    enable_git = cur_git_en if enable_git_input == "" else enable_git_input in ("y", "yes")
    git_cfg["enabled"] = enable_git

    if enable_git:
        default_url = git_cfg.get("repo_url", "")
        repo_url = input(f"Git Remote Repository URL [{default_url}]: ").strip()
        if repo_url:
            git_cfg["repo_url"] = repo_url
        default_remote = git_cfg.get("remote", "origin")
        git_cfg["remote"] = input(f"Git remote name [{default_remote}]: ").strip() or default_remote
        default_branch = git_cfg.get("branch", "main")
        branch = input(f"Git branch name [{default_branch}]: ").strip() or default_branch
        git_cfg["branch"] = branch

        if git_installed:
            init_input = input(f"Initialize Git in '{CANVASES_DIR}' now? [Y/n]: ").strip().lower()
            if init_input in ("", "y", "yes"):
                CANVASES_DIR.mkdir(parents=True, exist_ok=True)
                if not (CANVASES_DIR / ".git").exists():
                    subprocess.run(["git", "init", "-b", branch], cwd=CANVASES_DIR, check=False)
                    print(f"  [OK] Initialized Git repo in {CANVASES_DIR}")
                if git_cfg.get("repo_url"):
                    remotes = subprocess.run(["git", "remote"], cwd=CANVASES_DIR, capture_output=True, text=True).stdout.splitlines()
                    if git_cfg["remote"] in remotes:
                        subprocess.run(["git", "remote", "set-url", git_cfg["remote"], git_cfg["repo_url"]], cwd=CANVASES_DIR, check=False)
                    else:
                        subprocess.run(["git", "remote", "add", git_cfg["remote"], git_cfg["repo_url"]], cwd=CANVASES_DIR, check=False)
                    print(f"  [OK] Remote '{git_cfg['remote']}' configured -> {git_cfg['repo_url']}")

    # --- 2. Canvas Google Drive Sync ---
    print("\n--- 2. Canvas Google Drive Sync (Native Google Docs) ---")
    print("Syncs canvases to Google Drive and converts them to native Google Docs via rclone.")
    if not rclone_installed:
        print("[!] Note: 'rclone' was not found on your system PATH.")

    cur_gdrive_en = gdrive_cfg.get("enabled", False)
    enable_gdrive_input = input(f"Enable Google Drive sync for canvases? [y/N] (currently: {'yes' if cur_gdrive_en else 'no'}): ").strip().lower()
    enable_gdrive = cur_gdrive_en if enable_gdrive_input == "" else enable_gdrive_input in ("y", "yes")
    gdrive_cfg["enabled"] = enable_gdrive

    if enable_gdrive:
        remotes = get_rclone_remotes()
        default_remote = gdrive_cfg.get("rclone_remote", remotes[0] if remotes else "gdrive")
        remote_name = input(f"Rclone remote name [{default_remote}]: ").strip() or default_remote
        gdrive_cfg["rclone_remote"] = remote_name.strip(":")
        default_folder = gdrive_cfg.get("folder_name", "Canvases")
        gdrive_cfg["folder_name"] = (input(f"Target folder name [{default_folder}]: ").strip() or default_folder).strip("/")
        default_id = gdrive_cfg.get("root_folder_id", "")
        root_id = input(f"Google Drive Root Folder ID (optional, press Enter to keep '{default_id or 'none'}'): ").strip()
        if root_id:
            gdrive_cfg["root_folder_id"] = root_id

    # --- 3. Chat Git Export & Backup ---
    print("\n--- 3. Chat History Git Backup ---")
    print("Pushes exported markdown conversations organized by topic to a private Git repository.")
    cur_cgit_en = chat_git_cfg.get("enabled", False)
    enable_cgit_input = input(f"Enable Git backup for chat history? [y/N] (currently: {'yes' if cur_cgit_en else 'no'}): ").strip().lower()
    enable_cgit = cur_cgit_en if enable_cgit_input == "" else enable_cgit_input in ("y", "yes")
    chat_git_cfg["enabled"] = enable_cgit

    if enable_cgit:
        default_url = chat_git_cfg.get("repo_url", "")
        repo_url = input(f"Chat Git Repository URL [{default_url}]: ").strip()
        if repo_url:
            chat_git_cfg["repo_url"] = repo_url
        default_remote = chat_git_cfg.get("remote", "origin")
        chat_git_cfg["remote"] = input(f"Git remote name [{default_remote}]: ").strip() or default_remote
        default_branch = chat_git_cfg.get("branch", "main")
        chat_git_cfg["branch"] = input(f"Git branch name [{default_branch}]: ").strip() or default_branch

    # --- 4. Chat Google Drive Export ---
    print("\n--- 4. Chat History Google Drive Backup ---")
    print("Syncs exported markdown conversations organized by topic to Google Drive via rclone.")
    cur_cgdrive_en = chat_gdrive_cfg.get("enabled", False)
    enable_cgdrive_input = input(f"Enable Google Drive sync for chats? [y/N] (currently: {'yes' if cur_cgdrive_en else 'no'}): ").strip().lower()
    enable_cgdrive = cur_cgdrive_en if enable_cgdrive_input == "" else enable_cgdrive_input in ("y", "yes")
    chat_gdrive_cfg["enabled"] = enable_cgdrive

    if enable_cgdrive:
        remotes = get_rclone_remotes()
        default_remote = chat_gdrive_cfg.get("rclone_remote", remotes[0] if remotes else "gdrive")
        remote_name = input(f"Rclone remote name [{default_remote}]: ").strip() or default_remote
        chat_gdrive_cfg["rclone_remote"] = remote_name.strip(":")
        default_folder = chat_gdrive_cfg.get("folder_name", "AI_Chats")
        chat_gdrive_cfg["folder_name"] = (input(f"Target folder name [{default_folder}]: ").strip() or default_folder).strip("/")
        default_id = chat_gdrive_cfg.get("root_folder_id", "")
        root_id = input(f"Google Drive Root Folder ID (optional, press Enter to keep '{default_id or 'none'}'): ").strip()
        if root_id:
            chat_gdrive_cfg["root_folder_id"] = root_id

    # Save to config.json
    save_config(cfg)
    print("\n" + "=" * 64)
    print(f"[OK] Configuration successfully saved to: {CONFIG_PATH}")
    print("=" * 64)
    print_status()


def main():
    parser = argparse.ArgumentParser(description="Chat Context Cloud Sync Setup Wizard")
    parser.add_argument("--status", action="store_true", help="Print current status and exit")
    args = parser.parse_args()

    if args.status:
        print_status()
    else:
        run_interactive_wizard()


if __name__ == "__main__":
    main()
