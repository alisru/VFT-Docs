# Zenodo Upload Workflow & Automation Tool

Automates research deposition creation, metadata mapping, local file validation, and uploads to [Zenodo](https://zenodo.org) and [Zenodo Sandbox](https://sandbox.zenodo.org) via the Zenodo REST API.

---

## 1. Quick Start

### Step 1: Set Your API Token
Create a personal access token with `deposit:write` and `deposit:actions` scopes:
- **Sandbox Token (Testing):** [https://sandbox.zenodo.org/account/settings/applications/tokens/new/](https://sandbox.zenodo.org/account/settings/applications/tokens/new/)
- **Production Token (Live):** [https://zenodo.org/account/settings/applications/tokens/new/](https://zenodo.org/account/settings/applications/tokens/new/)

Save it in your environment or a `.env` file in the workspace root or `tools/zenodo/`:
```bash
ZENODO_SANDBOX_TOKEN=your_sandbox_token
ZENODO_PRODUCTION_TOKEN=your_production_token
```
*(Or pass directly via `--token <YOUR_TOKEN>`)*

---

### Step 2: Validate With a Dry Run
Always dry-run first to verify metadata parsing and asset file presence on disk without making network requests:
```bash
python tools/zenodo/zenodo_uploader.py "io/value physics/01_Empirical_Pricing_Audit_VPE55" --dry-run
```

---

### Step 3: Upload Deposition Draft to Sandbox
By default, the uploader targets **Zenodo Sandbox** and creates a **draft deposition** so you can inspect it in your browser before publishing:
```bash
python tools/zenodo/zenodo_uploader.py "io/value physics/01_Empirical_Pricing_Audit_VPE55" --sandbox
```
Output provides:
- Deposition ID
- Direct web link to the draft on Zenodo
- Pre-reserved DOI
- Upload progress for all attached files
- A `zenodo_upload_receipt.json` written to the package folder

---

### Step 4: Publish to Production
Once you've verified the deposit on Sandbox or want to deposit directly to Production:

**Upload as Draft to Production (Recommended for final review):**
```bash
python tools/zenodo/zenodo_uploader.py "io/value physics/01_Empirical_Pricing_Audit_VPE55" --production
```

**Upload and Immediately Publish (Mints DOI instantly):**
```bash
python tools/zenodo/zenodo_uploader.py "io/value physics/01_Empirical_Pricing_Audit_VPE55" --production --publish
```

---

## 2. CLI Options Reference

| Flag | Description | Default |
|---|---|---|
| `target` | Path to manifest JSON, package directory, or portfolio root | Required |
| `--dry-run` | Validates metadata and checks local files without making HTTP requests | `False` |
| `--sandbox` | Use Zenodo Sandbox API (`https://sandbox.zenodo.org/api`) | `True` |
| `--production` | Use Zenodo Production API (`https://zenodo.org/api`) | `False` |
| `--publish` | Publish deposition immediately to mint DOI (otherwise saves as draft) | `False` |
| `--batch` | Recursively discover and inspect/upload all manifests in directory | `False` |
| `--all-dir-files` | Upload all substantive files in package directory (skipping LaTeX temps) | `False` |
| `--files <f1> <f2>` | Explicit list of files to upload (overriding manifest discovery) | None |
| `--deposition-id <ID>` | Update and upload files to an existing draft deposition | None |
| `--token <TOKEN>` | Zenodo API personal access token | Reads from env |

---

## 3. Batch Portfolio Commands

Inspect all research packages in `io/value physics`:
```bash
python tools/zenodo/zenodo_uploader.py "io/value physics" --batch --dry-run
```

Batch upload all packages as drafts to Sandbox:
```bash
python tools/zenodo/zenodo_uploader.py "io/value physics" --batch --sandbox
```

---

## 4. Supported Manifest Schemas

The uploader automatically detects and translates two manifest formats:

1. **Replication Manifests (`zenodo_vpe55_manifest.json`, `zenodo_vpe21_manifest.json`)**:
   - Flat schema with `title`, `description`, `creators`, `keywords`, `license`, `repository_files`, and `jel_classifications`.
   - Automatically mapped to Zenodo's InvenioRDM deposit format.
   - Dual-licensing schemas (e.g. CC-BY-4.0 text / MIT code) are normalized into the primary license and annotated in deposition notes.

2. **Native Zenodo Schemas (`zenodo_v2.7.0_manifest.json`)**:
   - Pre-nested `{"metadata": { ... }}` schema.
   - Preserves custom fields, community links, and related identifiers.
