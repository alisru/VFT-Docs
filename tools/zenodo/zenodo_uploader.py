#!/usr/bin/env python3
"""
Zenodo Upload Workflow CLI & Automation Engine
----------------------------------------------
Automates research deposition creation, metadata mapping, local asset verification,
and file uploading to Zenodo via the Zenodo REST API.

Supports:
- Zenodo Sandbox (https://sandbox.zenodo.org) [Default for safety]
- Zenodo Production (https://zenodo.org) via --production
- Both flat manifest formats (vpe55, vpe21) and native Zenodo manifest formats (v2.7.0)
- Single package deposition or multi-package portfolio batch inspection (--batch)
- Auto-discovery of publication assets (--all-dir-files) ignoring LaTeX artifacts (.aux, .log, .out, .spl)
- Safe dry-run mode (--dry-run)
- Draft-by-default workflow with optional instant publishing (--publish)
- Upload receipts logging (zenodo_upload_receipt.json)
"""

import os
import sys
import json
import zipfile
import argparse
import hashlib
import mimetypes
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Set

try:
    import requests
except ImportError:
    print("Error: 'requests' package is required. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

# Ensure proper encoding on Windows console
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Attempt to load .env if python-dotenv is available
try:
    from dotenv import load_dotenv
    current = Path(__file__).resolve().parent
    for p in [current, current.parent, current.parent.parent]:
        env_file = p / ".env"
        if env_file.is_file():
            load_dotenv(dotenv_path=env_file)
            break
except ImportError:
    pass

ZENODO_PROD_URL = "https://zenodo.org/api"
ZENODO_SANDBOX_URL = "https://sandbox.zenodo.org/api"

# File patterns to exclude from automated directory uploads
EXCLUDED_EXTENSIONS: Set[str] = {
    ".aux", ".log", ".out", ".spl", ".toc", ".synctex.gz", ".bbl", ".blg",
    ".tmp", ".temp", ".pyc"
}
EXCLUDED_FILENAMES: Set[str] = {
    "zenodo_upload_receipt.json"
}


def get_token(is_sandbox: bool, cli_token: Optional[str] = None) -> Optional[str]:
    """Retrieve Zenodo access token from CLI args or environment."""
    if cli_token:
        return cli_token.strip()
    if is_sandbox:
        return os.environ.get("ZENODO_SANDBOX_TOKEN") or os.environ.get("ZENODO_TOKEN")
    return os.environ.get("ZENODO_PRODUCTION_TOKEN") or os.environ.get("ZENODO_TOKEN")


def compute_file_hash(filepath: Path) -> Tuple[int, str]:
    """Return file size in bytes and MD5 hexadecimal hash."""
    hasher = hashlib.md5()
    size = 0
    with open(filepath, "rb") as f:
        while chunk := f.read(1024 * 1024):
            size += len(chunk)
            hasher.update(chunk)
    return size, hasher.hexdigest()


def format_size(bytes_num: int) -> str:
    """Format bytes into human-readable string."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_num < 1024.0:
            return f"{bytes_num:.1f} {unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.1f} TB"


def normalize_license(lic: Any) -> str:
    """Normalize license to a Zenodo-compliant identifier."""
    if isinstance(lic, dict):
        lic_val = lic.get("manuscript_and_data") or lic.get("primary") or next(iter(lic.values()), "cc-by-4.0")
    elif isinstance(lic, str):
        lic_val = lic
    else:
        lic_val = "cc-by-4.0"

    lic_val = str(lic_val).strip()
    lic_lower = lic_val.lower().replace(" ", "-")
    if "cc-by-4.0" in lic_lower or "cc-by-4" in lic_lower:
        return "cc-by-4.0"
    if "cc0" in lic_lower:
        return "cc0-1.0"
    if "mit" in lic_lower:
        return "mit"
    if "gpl-3" in lic_lower:
        return "gpl-3.0"
    if "apache-2" in lic_lower:
        return "apache-2.0"
    return lic_val.lower()


def map_manifest_to_zenodo_metadata(manifest_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Translates manifest dictionary to Zenodo Deposit Metadata schema.
    Supports both native Zenodo metadata structure and flat replication manifests.
    """
    if "metadata" in manifest_data and isinstance(manifest_data["metadata"], dict):
        meta = dict(manifest_data["metadata"])
        if "license" in meta:
            meta["license"] = normalize_license(meta["license"])
        if "access_right" not in meta:
            meta["access_right"] = "open"
        return meta

    title = manifest_data.get("title", "Untitled Research Deposit")
    raw_desc = manifest_data.get("description", "")
    
    if raw_desc and not ("<p>" in raw_desc or "<div>" in raw_desc):
        paras = [f"<p>{p.strip()}</p>" for p in raw_desc.split("\n\n") if p.strip()]
        description = "".join(paras) if paras else f"<p>{raw_desc}</p>"
    else:
        description = raw_desc or "<p>No description provided.</p>"

    upload_type = manifest_data.get("upload_type")
    pub_type = manifest_data.get("publication_type")

    if not upload_type:
        if "target_manuscript" in manifest_data or "manuscript" in title.lower():
            upload_type = "publication"
            pub_type = pub_type or "preprint"
        elif "replication" in title.lower() or "dataset" in title.lower():
            upload_type = "dataset"
        elif "software" in title.lower():
            upload_type = "software"
        else:
            upload_type = "publication"
            pub_type = pub_type or "preprint"

    raw_creators = manifest_data.get("creators", [])
    creators = []
    for c in raw_creators:
        creator_obj = {
            "name": c.get("name", "Unknown Author")
        }
        if c.get("affiliation"):
            creator_obj["affiliation"] = c["affiliation"]
        if c.get("orcid"):
            creator_obj["orcid"] = c["orcid"]
        creators.append(creator_obj)

    if not creators:
        creators = [{"name": "Hamilton, Jarrod Lyndsay", "affiliation": "Alethekanon Research Institute"}]

    notes_parts = []
    if manifest_data.get("deliverable_id"):
        notes_parts.append(f"Deliverable ID: {manifest_data['deliverable_id']}")
    if manifest_data.get("target_manuscript"):
        notes_parts.append(f"Target Manuscript: {manifest_data['target_manuscript']}")
    if manifest_data.get("jel_classifications"):
        notes_parts.append(f"JEL Classifications: {', '.join(manifest_data['jel_classifications'])}")
    if isinstance(manifest_data.get("license"), dict):
        sub_lic = ", ".join([f"{k}: {v}" for k, v in manifest_data["license"].items()])
        notes_parts.append(f"Licensing Breakdown: {sub_lic}")
    if manifest_data.get("replication_instructions"):
        notes_parts.append(f"Replication Instructions: {manifest_data['replication_instructions']}")

    notes = " | ".join(notes_parts) if notes_parts else None

    zenodo_meta: Dict[str, Any] = {
        "title": title,
        "upload_type": upload_type,
        "description": description,
        "creators": creators,
        "access_right": "open",
        "license": normalize_license(manifest_data.get("license", "CC-BY-4.0")),
    }

    if upload_type == "publication" and pub_type:
        zenodo_meta["publication_type"] = pub_type

    if manifest_data.get("publication_date"):
        zenodo_meta["publication_date"] = manifest_data["publication_date"]

    if manifest_data.get("version"):
        zenodo_meta["version"] = manifest_data["version"]

    if manifest_data.get("keywords"):
        zenodo_meta["keywords"] = manifest_data["keywords"]

    if notes:
        zenodo_meta["notes"] = notes

    if manifest_data.get("communities"):
        zenodo_meta["communities"] = manifest_data["communities"]

    if manifest_data.get("related_identifiers"):
        zenodo_meta["related_identifiers"] = manifest_data["related_identifiers"]

    return zenodo_meta


def discover_files_from_manifest(
    manifest_path: Path,
    manifest_data: Dict[str, Any],
    all_dir_files: bool = False
) -> Tuple[List[Path], List[str], List[str]]:
    """
    Discover files for deposition.
    Returns: (files_to_upload, missing_files, zipped_files)
    """
    package_dir = manifest_path.parent
    files_to_upload: List[Path] = []
    missing_files: List[str] = []
    zipped_files: List[str] = []
    candidates: List[str] = []

    # Check zip packages in directory to see what they contain
    contained_in_zips: Dict[str, str] = {}
    for zpath in package_dir.glob("*.zip"):
        try:
            with zipfile.ZipFile(zpath, "r") as zf:
                for zname in zf.namelist():
                    contained_in_zips[zname] = zpath.name
        except Exception:
            pass

    if all_dir_files:
        # Collect all substantive non-hidden, non-intermediate files in directory
        for p in package_dir.iterdir():
            if not p.is_file():
                continue
            if p.name.startswith("."):
                continue
            if p.suffix.lower() in EXCLUDED_EXTENSIONS:
                continue
            if p.name in EXCLUDED_FILENAMES:
                continue
            if p.name == manifest_path.name:
                continue
            files_to_upload.append(p)
        return sorted(files_to_upload, key=lambda x: x.name), [], []

    # Parse candidate files from manifest
    if "repository_files" in manifest_data:
        for item in manifest_data["repository_files"]:
            fname = item.get("filename") if isinstance(item, dict) else str(item)
            if fname:
                candidates.append(fname)

    elif "replication_assets" in manifest_data:
        assets = manifest_data["replication_assets"]
        for group in ["python_modules", "visual_assets", "submission_packages"]:
            for item in assets.get(group, []):
                fname = item.get("filename") if isinstance(item, dict) else str(item)
                if fname:
                    candidates.append(fname)

    for cand in candidates:
        p = (package_dir / cand).resolve()
        if p.is_file():
            files_to_upload.append(p)
        elif cand in contained_in_zips:
            zipped_files.append(f"{cand} (inside {contained_in_zips[cand]})")
        else:
            missing_files.append(cand)

    # If no files matched from manifest, fall back to substantive directory files
    if not files_to_upload:
        for p in package_dir.iterdir():
            if p.is_file() and not p.name.startswith(".") and p.suffix.lower() not in EXCLUDED_EXTENSIONS:
                if p.name != manifest_path.name and p.name not in EXCLUDED_FILENAMES:
                    files_to_upload.append(p)

    return sorted(files_to_upload, key=lambda x: x.name), missing_files, zipped_files


class ZenodoClient:
    """Zenodo REST API Client."""

    def __init__(self, token: str, is_sandbox: bool = True):
        self.token = token
        self.is_sandbox = is_sandbox
        self.base_url = ZENODO_SANDBOX_URL if is_sandbox else ZENODO_PROD_URL
        self.headers = {
            "Authorization": f"Bearer {self.token}",
        }

    def verify_auth(self) -> Dict[str, Any]:
        """Verify API token with Zenodo."""
        url = f"{self.base_url}/deposit/depositions"
        res = requests.get(url, headers=self.headers, params={"size": 1}, timeout=15)
        if res.status_code == 200:
            return {"status": "authenticated", "env": "sandbox" if self.is_sandbox else "production"}
        raise PermissionError(f"Zenodo Authentication failed (HTTP {res.status_code}): {res.text}")

    def create_deposition(self, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create new deposition draft."""
        url = f"{self.base_url}/deposit/depositions"
        payload = {"metadata": metadata} if metadata else {}
        headers = {**self.headers, "Content-Type": "application/json"}
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        if res.status_code in (200, 201):
            return res.json()
        raise RuntimeError(f"Failed to create deposition (HTTP {res.status_code}): {res.text}")

    def get_deposition(self, deposition_id: str) -> Dict[str, Any]:
        """Retrieve deposition details."""
        url = f"{self.base_url}/deposit/depositions/{deposition_id}"
        res = requests.get(url, headers=self.headers, timeout=20)
        if res.status_code == 200:
            return res.json()
        raise RuntimeError(f"Failed to get deposition {deposition_id} (HTTP {res.status_code}): {res.text}")

    def update_metadata(self, deposition_id: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Update deposition draft metadata."""
        url = f"{self.base_url}/deposit/depositions/{deposition_id}"
        headers = {**self.headers, "Content-Type": "application/json"}
        res = requests.put(url, headers=headers, json={"metadata": metadata}, timeout=30)
        if res.status_code == 200:
            return res.json()
        raise RuntimeError(f"Failed to update metadata for deposition {deposition_id} (HTTP {res.status_code}): {res.text}")

    def upload_file_bucket(self, bucket_url: str, filepath: Path) -> Dict[str, Any]:
        """Upload a file using Zenodo's Bucket API."""
        filename = filepath.name
        url = f"{bucket_url}/{filename}"
        mime, _ = mimetypes.guess_type(str(filepath))
        mime = mime or "application/octet-stream"

        file_size = filepath.stat().st_size
        headers = {
            **self.headers,
            "Content-Type": mime,
            "Content-Length": str(file_size)
        }

        with open(filepath, "rb") as f:
            res = requests.put(url, headers=headers, data=f, timeout=300)

        if res.status_code in (200, 201):
            return res.json()
        raise RuntimeError(f"Failed to upload {filename} via bucket (HTTP {res.status_code}): {res.text}")

    def upload_file_legacy(self, deposition_id: str, filepath: Path) -> Dict[str, Any]:
        """Fallback multipart upload for legacy deposits."""
        url = f"{self.base_url}/deposit/depositions/{deposition_id}/files"
        with open(filepath, "rb") as f:
            files = {"file": (filepath.name, f)}
            data = {"name": filepath.name}
            res = requests.post(url, headers=self.headers, files=files, data=data, timeout=300)

        if res.status_code in (200, 201):
            return res.json()
        raise RuntimeError(f"Failed to upload {filepath.name} via legacy API (HTTP {res.status_code}): {res.text}")

    def publish_deposition(self, deposition_id: str) -> Dict[str, Any]:
        """Publish deposition to mint DOI."""
        url = f"{self.base_url}/deposit/depositions/{deposition_id}/actions/publish"
        res = requests.post(url, headers=self.headers, timeout=30)
        if res.status_code == 202:
            return res.json()
        raise RuntimeError(f"Failed to publish deposition {deposition_id} (HTTP {res.status_code}): {res.text}")


def execute_workflow(
    manifest_path: Path,
    file_overrides: Optional[List[Path]] = None,
    all_dir_files: bool = False,
    is_sandbox: bool = True,
    dry_run: bool = False,
    publish: bool = False,
    cli_token: Optional[str] = None,
    existing_dep_id: Optional[str] = None
) -> Dict[str, Any]:
    """Execute complete validation and upload workflow."""

    if not manifest_path.is_file():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)

    # 1. Map metadata
    zenodo_meta = map_manifest_to_zenodo_metadata(manifest_data)
    env_name = "Sandbox" if is_sandbox else "Production"
    base_endpoint = ZENODO_SANDBOX_URL if is_sandbox else ZENODO_PROD_URL

    # 2. File discovery & verification
    if file_overrides:
        files = [p.resolve() for p in file_overrides if p.resolve().is_file()]
        missing_files = []
        zipped_files = []
    else:
        files, missing_files, zipped_files = discover_files_from_manifest(
            manifest_path, manifest_data, all_dir_files=all_dir_files
        )

    file_details = []
    total_bytes = 0
    for p in files:
        sz, md5 = compute_file_hash(p)
        total_bytes += sz
        file_details.append({
            "path": str(p),
            "filename": p.name,
            "size_bytes": sz,
            "size_formatted": format_size(sz),
            "md5": md5
        })

    report = {
        "manifest_path": str(manifest_path.resolve()),
        "target_environment": env_name,
        "endpoint": base_endpoint,
        "title": zenodo_meta.get("title"),
        "upload_type": zenodo_meta.get("upload_type"),
        "total_files": len(files),
        "total_size": format_size(total_bytes),
        "files_to_upload": file_details,
        "missing_manifest_files": missing_files,
        "zipped_files": zipped_files,
        "metadata_payload": zenodo_meta,
    }

    print("=" * 76)
    print(f"ZENODO DEPOSITION: {zenodo_meta.get('title')[:60]}...")
    print("=" * 76)
    print(f"Target Env:     {env_name.upper()} ({base_endpoint})")
    print(f"Manifest:       {manifest_path.name}")
    print(f"Upload Type:    {zenodo_meta.get('upload_type')} ({zenodo_meta.get('publication_type', 'standard')})")
    print(f"Files Ready:    {len(files)} file(s) ({format_size(total_bytes)})")
    for f_info in file_details:
        print(f"  + {f_info['filename']} ({f_info['size_formatted']}, md5: {f_info['md5'][:8]}...)")

    if zipped_files:
        print(f"\nFiles contained in release ZIPs ({len(zipped_files)}):")
        for zf in zipped_files:
            print(f"  * {zf}")

    if missing_files:
        print(f"\nWarning: {len(missing_files)} file(s) listed in manifest not found on disk:")
        for mf in missing_files:
            print(f"  ! {mf}")

    if dry_run:
        print(f"\n[DRY-RUN COMPLETE]: Metadata validated. Ready for {env_name} upload.")
        report["status"] = "dry_run_success"
        return report

    # 3. Network Execution
    token = get_token(is_sandbox, cli_token)
    if not token:
        env_var_name = "ZENODO_SANDBOX_TOKEN" if is_sandbox else "ZENODO_PRODUCTION_TOKEN"
        raise ValueError(
            f"No Zenodo API token found for {env_name}!\n"
            f"Please set '{env_var_name}' or 'ZENODO_TOKEN' in your environment or .env file,\n"
            f"or pass it via --token <YOUR_TOKEN>."
        )

    client = ZenodoClient(token=token, is_sandbox=is_sandbox)

    print(f"\n[1/4] Verifying Zenodo API Authentication ({env_name})...")
    client.verify_auth()
    print("      Authentication verified.")

    # Deposition creation or retrieval
    if existing_dep_id:
        print(f"\n[2/4] Fetching existing deposition draft #{existing_dep_id}...")
        dep = client.get_deposition(existing_dep_id)
    else:
        print("\n[2/4] Creating new deposition draft...")
        dep = client.create_deposition(metadata=zenodo_meta)

    dep_id = str(dep["id"])
    bucket_url = dep.get("links", {}).get("bucket")
    html_url = dep.get("links", {}).get("html", f"{base_endpoint.replace('/api', '')}/deposit/{dep_id}")
    prereserved_doi = dep.get("metadata", {}).get("prereserved_doi", {}).get("doi", "Pending")

    print(f"      Deposition ID:  {dep_id}")
    print(f"      Browser URL:    {html_url}")
    print(f"      Reserved DOI:   {prereserved_doi}")

    # 4. Upload Files
    print(f"\n[3/4] Uploading {len(files)} file(s)...")
    for f_info in file_details:
        fpath = Path(f_info["path"])
        print(f"      Uploading: {fpath.name} ({f_info['size_formatted']})...", end="", flush=True)
        if bucket_url:
            client.upload_file_bucket(bucket_url, fpath)
        else:
            client.upload_file_legacy(dep_id, fpath)
        print(" DONE")

    # 5. Metadata Sync
    print("\n[4/4] Updating metadata...")
    client.update_metadata(dep_id, zenodo_meta)

    if publish:
        print("\n[PUBLISH ACTION] Minting permanent DOI on Zenodo...")
        pub_res = client.publish_deposition(dep_id)
        final_doi = pub_res.get("doi", prereserved_doi)
        print(f"SUCCESS: Deposition published permanently! DOI: {final_doi}")
        status = "published"
    else:
        print("\nSUCCESS: Deposition saved as DRAFT.")
        print(f"Inspect and review draft in browser before publishing: {html_url}")
        status = "draft_created"

    receipt = {
        "status": status,
        "environment": env_name,
        "deposition_id": dep_id,
        "html_url": html_url,
        "reserved_doi": prereserved_doi,
        "files_uploaded": [f["filename"] for f in file_details],
        "total_size": format_size(total_bytes),
        "manifest_used": str(manifest_path.resolve())
    }

    receipt_path = manifest_path.parent / "zenodo_upload_receipt.json"
    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)
    print(f"Receipt written to: {receipt_path}")

    return receipt


def run_batch_portfolio(
    directory: Path,
    all_dir_files: bool = False,
    is_sandbox: bool = True,
    dry_run: bool = True,
    publish: bool = False,
    cli_token: Optional[str] = None
):
    """Scan and process all Zenodo manifests in a portfolio directory."""
    manifests = sorted(list(directory.rglob("*zenodo*manifest*.json")))
    if not manifests:
        manifests = sorted(list(directory.rglob("*manifest*.json")))

    if not manifests:
        print(f"No Zenodo manifest files found under: {directory}")
        return

    print("=" * 76)
    print(f"ZENODO PORTFOLIO SCAN: Found {len(manifests)} packages under {directory.name}")
    print("=" * 76)

    results = []
    for idx, m in enumerate(manifests, 1):
        print(f"\n>>> [{idx}/{len(manifests)}] Processing Package: {m.parent.name}")
        try:
            res = execute_workflow(
                manifest_path=m,
                all_dir_files=all_dir_files,
                is_sandbox=is_sandbox,
                dry_run=dry_run,
                publish=publish,
                cli_token=cli_token
            )
            results.append((m, True, res))
        except Exception as e:
            print(f"[ERROR]: {e}")
            results.append((m, False, str(e)))

    print("\n" + "=" * 76)
    print("PORTFOLIO SUMMARY:")
    for m, ok, details in results:
        status_str = "OK" if ok else "FAILED"
        print(f"  [{status_str}] {m.parent.name} -> {m.name}")
    print("=" * 76)


def main():
    parser = argparse.ArgumentParser(
        description="Automated Zenodo Upload & Deposition CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate metadata and check files for a single package (Dry-Run):
  python tools/zenodo/zenodo_uploader.py "io/value physics/01_Empirical_Pricing_Audit_VPE55" --dry-run

  # Batch inspect all research packages in value physics:
  python tools/zenodo/zenodo_uploader.py "io/value physics" --batch --dry-run

  # Include all substantive files in the directory (not just manifest list):
  python tools/zenodo/zenodo_uploader.py "io/value physics/01_Empirical_Pricing_Audit_VPE55" --all-dir-files --dry-run

  # Upload draft to Zenodo Sandbox (requires ZENODO_SANDBOX_TOKEN):
  python tools/zenodo/zenodo_uploader.py "io/value physics/01_Empirical_Pricing_Audit_VPE55" --sandbox

  # Upload draft to Zenodo Production (requires ZENODO_PRODUCTION_TOKEN):
  python tools/zenodo/zenodo_uploader.py "io/value physics/01_Empirical_Pricing_Audit_VPE55" --production
        """
    )

    parser.add_argument(
        "target",
        help="Path to manifest JSON, package directory, or portfolio directory"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Scan and execute all manifest packages found recursively under target directory"
    )
    parser.add_argument(
        "--all-dir-files",
        action="store_true",
        help="Upload all substantive files in directory, ignoring LaTeX temp files (.aux, .log, .out, .spl)"
    )
    parser.add_argument(
        "--sandbox",
        action="store_true",
        default=True,
        help="Use Zenodo Sandbox API (https://sandbox.zenodo.org) [Default: True]"
    )
    parser.add_argument(
        "--production",
        dest="sandbox",
        action="store_false",
        help="Use Zenodo Production API (https://zenodo.org)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate metadata and local files without making network requests"
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Publish immediately after upload (mints real DOI; default leaves as draft)"
    )
    parser.add_argument(
        "--token",
        help="Zenodo API personal access token (overrides environment variables)"
    )
    parser.add_argument(
        "--deposition-id",
        help="Update and upload to an existing draft deposition ID instead of creating new"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        help="Explicit list of files to upload (overrides manifest discovery)"
    )

    args = parser.parse_args()
    target_path = Path(args.target).resolve()

    if args.batch:
        if not target_path.is_dir():
            print(f"Error: Target for --batch must be a directory: {target_path}", file=sys.stderr)
            sys.exit(1)
        run_batch_portfolio(
            directory=target_path,
            all_dir_files=args.all_dir_files,
            is_sandbox=args.sandbox,
            dry_run=args.dry_run,
            publish=args.publish,
            cli_token=args.token
        )
        return

    manifest_file = None
    if target_path.is_file() and target_path.suffix == ".json":
        manifest_file = target_path
    elif target_path.is_dir():
        manifests = list(target_path.glob("*zenodo*manifest*.json")) or list(target_path.glob("*manifest*.json"))
        if manifests:
            manifest_file = manifests[0]
        else:
            print(f"Error: No zenodo manifest JSON found in directory: {target_path}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Error: Target path does not exist: {target_path}", file=sys.stderr)
        sys.exit(1)

    override_files = [Path(f) for f in args.files] if args.files else None

    try:
        execute_workflow(
            manifest_path=manifest_file,
            file_overrides=override_files,
            all_dir_files=args.all_dir_files,
            is_sandbox=args.sandbox,
            dry_run=args.dry_run,
            publish=args.publish,
            cli_token=args.token,
            existing_dep_id=args.deposition_id
        )
    except Exception as e:
        print(f"\n[ERROR]: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
