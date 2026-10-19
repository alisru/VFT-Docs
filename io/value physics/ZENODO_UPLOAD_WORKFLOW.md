# Zenodo Deposition Workflow for Value Physics Research Packages

This guide details how to deposit and publish the Value Physics research packages and replication suites to [Zenodo](https://zenodo.org).

---

## Registered Packages in Portfolio

1. **Package 1 (VPE-55 / VPE-56):**
   - **Path:** `io/value physics/01_Empirical_Pricing_Audit_VPE55`
   - **Manifest:** `zenodo_vpe55_manifest.json`
   - **Target Journal:** *Ecological Economics*
   - **Target DOI:** `10.5281/zenodo.1755001`
   - **Primary Assets:** `manuscript_vpe55.pdf`, `vpe55_latex_package.zip`, `figure1_biophysical_breakdown.png`, `figure2_sclerosis_spectrum.png`, `rrp_fairness_audit.py`

2. **Package 2 (VPE-21):**
   - **Path:** `io/value physics/02_Physics_of_Economic_Value_VPE21`
   - **Manifest:** `zenodo_vpe21_manifest.json`
   - **Target Journal:** *Ecological Economics*
   - **Target DOI:** `10.5281/zenodo.1755021`
   - **Primary Assets:** `manuscript_vpe21.tex`, `vpe21_latex_package.zip`, `sfc_model.py`, `test_value_physics.py`

3. **Package 3 (VPE-49):**
   - **Path:** `io/value physics/03_Thermodynamic_State_Space_VPE49`
   - **Manifest:** `zenodo_v2.7.0_manifest.json`
   - **Target Journal:** *Journal of Economic Dynamics and Control*
   - **Target DOI:** `10.5281/zenodo.1755049`
   - **Primary Assets:** `work_antiwork_dynamics.py`, `test_value_physics.py`, `phase_portrait.png`, `bifurcation_diagram.png`, `vpe49_latex_package.zip`

---

## Upload Commands

### 1. Portfolio Dry-Run (Check All Packages)
Verify that all metadata files parse properly and check which files are on disk:
```bash
python tools/zenodo/zenodo_uploader.py "io/value physics" --batch --dry-run
```

### 2. Single Package Dry-Run
```bash
python tools/zenodo/zenodo_uploader.py "io/value physics/01_Empirical_Pricing_Audit_VPE55" --dry-run
```

### 3. Upload Draft to Zenodo Sandbox (Testing)
Uploads files and metadata as an unlisted draft on the Sandbox API:
```bash
python tools/zenodo/zenodo_uploader.py "io/value physics/01_Empirical_Pricing_Audit_VPE55" --sandbox
```

### 4. Upload Draft to Zenodo Production (Live)
Uploads files and metadata as a draft to production Zenodo for visual review:
```bash
python tools/zenodo/zenodo_uploader.py "io/value physics/01_Empirical_Pricing_Audit_VPE55" --production
```

### 5. Instant Publication
Uploads and mints the permanent citable DOI in one command:
```bash
python tools/zenodo/zenodo_uploader.py "io/value physics/01_Empirical_Pricing_Audit_VPE55" --production --publish
```

---

## Authentication Configuration
Set the personal access token in `.env` (or pass via `--token <TOKEN>`):
```bash
# Sandbox: https://sandbox.zenodo.org/account/settings/applications/tokens/new/
ZENODO_SANDBOX_TOKEN=your_token_here

# Production: https://zenodo.org/account/settings/applications/tokens/new/
ZENODO_PRODUCTION_TOKEN=your_token_here
```
*(Required scopes: `deposit:write`, `deposit:actions`)*
