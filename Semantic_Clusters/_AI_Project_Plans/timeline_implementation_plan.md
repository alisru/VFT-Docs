# Implementation Plan: Document by Creation Date Timeline Explorer

This plan details the design and implementation of the VFT Timeline Explorer. It reads file creation dates from the filesystem to visualize the chronological order of your notes by their creation date, grouped by VFT topics and quadrants.

---

## 1. Proposed Changes

### 1.1 Python Backend (`start_viewer.py`)
Add a new API endpoint `/api/timeline`:
* **Filesystem Scan:** Reads all `.md` files in `_VFT MD` (using `corpus_manifest.json` as the index).
* **Creation Date Resolution:** For each file, reads the filesystem creation timestamp using `os.path.getctime(path)`.
* **VFT Topic Lookup:** For each file:
  * Looks up all paragraphs for that file in the paragraph-topic index (`cluster_mapping.json`).
  * Computes the file's primary VFT topic (the most frequent topic/quadrant).
  * Attaches VFT metadata: `topic_id`, `node_name`, `quadrant`, and top 3 `isms`.
  * If the file has no topic index (e.g. a system log or project plan), labels it as `System / Project Log`.
* **Chronological Sorting:** Returns the list of files sorted in reverse chronological order by their creation date.

---

### 1.2 HTML Frontend (`viewer.html`)

#### 1.2.1 Tab Navigation
* Add a new "Timeline" tab button in the header navbar:
  ```html
  <button class="tab-btn" onclick="switchTab('timeline-tab', this)">&#128337; Timeline</button>
  ```

#### 1.2.2 Timeline Panel Layout (`#timeline-tab`)
Add a view panel containing:
* **Timeline Sidebar (Filters):**
  * Search box to filter files by filename.
  * Dropdown selector for **Quadrants** (GG, LE, LG, GE).
  * Dropdown selector for **Node Names** (Language/Psychology, History/Reality, etc.).
* **Timeline Main Feed:**
  * Displays files grouped by their creation date (e.g., "August 5, 2026").
  * Each file is rendered as an interactive card showing the filename, path, primary VFT quadrant badge, node name, and top isms.

#### 1.2.3 Client-side Navigation Logic
* Implement `drOpenTimeline()`: Fetches `/api/timeline` and renders the chronological list.
* Clicking on any file card in the timeline switches the main tab to `docreader-tab` and loads that document.

---

## 2. Verification Plan

### 2.1 Backend Testing
* Run `start_viewer.py` and test `/api/timeline` using `curl` or browser query to confirm it outputs files sorted by creation date with their VFT metadata.

### 2.2 Manual UI Verification
* Open `viewer.html`, click the new "Timeline" tab, check filters, and confirm that clicking a file card opens it correctly in the Doc Reader.
