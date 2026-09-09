# Implementation Plan v27: Spiritual Tradition Sub-Selectors & Operator Console Controls

## Overview
Enable granular, multi-tradition spiritual canon selection across both the AI batch generator (`google_ai_studio_one_shot.py`), registry compiler (`rebuild_registries_son.py`), and the operator console (`control_panel.html`). Instead of defaulting to single-tradition/Biblical quotes, the system supports dynamic multi-select sub-selectors (Christianity, Hinduism, Buddhism, Taoism, Islam & Sufism, Indigenous & Custodial, Stoicism & Classical, and Everything Else / Universal Lore), with preset combinations like "Core Four", "Eastern Metaphysics", and "All Traditions".

---

## Key Changes

### 1. `bluesky_bot/google_ai_studio_one_shot.py`
- Add `--spiritual-traditions` CLI argument (comma-separated string or list, default: `all`).
- Define canonical tradition mappings (Christianity, Hinduism, Buddhism, Taoism, Islam/Sufi, Indigenous, Stoic/Classical, Universal/Other).
- Upgrade `build_spiritual_prompt(selected_traditions)` to dynamically construct the `=== SPIRITUAL AUDIT DIRECTIVE ===` instructing the model to evaluate the story's core moral dilemma against the selected traditions without defaulting to single-religion biases.
- Remove hardcoded single-source anchors in prompt examples.

### 2. `bluesky_bot/rebuild_registries_son.py`
- Enhance `spiritual_audit` metadata extraction to auto-detect the tradition from the citation/quote and populate `"tradition"` (e.g. `Taoist`, `Buddhist`, `Hindu`, `Christian`, `Islamic`, `Indigenous`, `Stoic`, `Universal`).

### 3. `bluesky_bot/control_panel.html`
- **Tradition Badges**: Display an informative tradition tag on the `Spirithekanon` post in the Thread Emulator (e.g. `🕊️ Spirithekanon · [☯️ Taoist]`, `[🕉️ Hindu]`, `[☸️ Buddhist]`, `[✝️ Christian]`, etc.).
- **Sidebar Tradition Filter**: Add a tradition filter dropdown/pills to quickly filter existing stories by spiritual tradition cited.
- **Controller & Composer Sub-Selectors**: Add an interactive multi-select UI in the CLI Controller and AI Prompt Composer with checkboxes for each tradition and preset buttons (`Core Four`, `All Traditions`, `Eastern`, `Clear`).

---

## Verification Plan
1. Test CLI argument parsing in `google_ai_studio_one_shot.py` with `--help` and various `--spiritual-traditions` inputs.
2. Run `rebuild_registries_son.py` to verify that existing stories with Spirithekanon posts have their traditions classified and indexed in `stories_registry.js`.
3. Open/inspect `control_panel.html` in browser or verify DOM elements, tradition badges, filter handlers, and CLI composer synchronization.
