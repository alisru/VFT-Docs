import os
import shutil

def execute_archiving():
    workspace_dir = r"e:\Vector Field Theory\VFT Docs"
    archive_dir = os.path.join(workspace_dir, "bluesky_bot", "_Archive")
    os.makedirs(archive_dir, exist_ok=True)
    print(f"Created archive directory at: {archive_dir}")
    
    # List of scratch files to archive
    scratch_files = [
        "worker1_batch1_eval.py",
        "worker3_eval.py",
        "worker4_eval.py",
        "worker4_eval_batch4.py",
        "process_batch.py",
        "process_batch_2.py",
        "process_batch3.py",
        "save_batch3_configs.py",
        "generate_jsons.py",
        "generate_batch2_files.py",
        "generate_batch2_graphs.py",
        "generate_batch4_graphs.py",
        "generate_graphs.py",
        "generate_graphs_for_batch.py",
        "repair_dry_run_links.py",
        "mark_live.py",
        "move_live.py",
        "filter_candidates.py",
        "sync_harvested_evaluations.py",
        "generate_evaluated_json_files.py",
        "detect_duplicates.py",
        "delete_root_factchecks.py",
        "clean_duplicate_files.py",
        "delete_corrupted_factchecks.py",
        "inspect_factchecks.py"
    ]
    
    # Move files from scratch/ to archive/
    for filename in scratch_files:
        src = os.path.join(workspace_dir, "scratch", filename)
        if os.path.exists(src):
            dst = os.path.join(archive_dir, filename)
            print(f"Moving scratch file: {filename} -> _Archive/")
            try:
                shutil.move(src, dst)
            except Exception as e:
                print(f"Error moving {filename}: {e}")
                
    # List of bluesky_bot/ files to archive
    bot_files = [
        "generate_dry_runs.py"
    ]
    
    # Move files from bluesky_bot/ to archive/
    for filename in bot_files:
        src = os.path.join(workspace_dir, "bluesky_bot", filename)
        if os.path.exists(src):
            dst = os.path.join(archive_dir, filename)
            print(f"Moving bot file: {filename} -> _Archive/")
            try:
                shutil.move(src, dst)
            except Exception as e:
                print(f"Error moving {filename}: {e}")
                
    print("\nArchiving completed successfully!")

if __name__ == "__main__":
    execute_archiving()
