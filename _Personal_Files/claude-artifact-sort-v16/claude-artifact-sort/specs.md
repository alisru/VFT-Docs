# Claude Artifact Sorter (CAS) — Technical Specifications

## 1. Overview
The **Claude Artifact Sorter (CAS)** is a browser extension (content script) designed to enhance the artifact management experience on Claude.ai and Gemini. It provides advanced sorting, tagging, and summarization capabilities for both uploaded files and AI-generated artifacts.

---

## 2. Core Architecture

### Platform Detection
The script automatically detects the environment using `window.location.hostname`:
- **Claude**: `claude.ai`
- **Gemini**: `gemini.google.com`

### Storage Model
CAS uses `chrome.storage.local` for persistence across sessions and chats. Key namespaces include:
- `cas_summaries`: Mapping of artifact names to their AI-generated summaries.
- `cas_tags`: Mapping of artifact names to major VFT categories.
- `cas_subtags`: Nested mapping of categories to specific subtags.
- `cas_first_seen`: Timestamps ("HH:mm DD.MM") of when an artifact was first detected.
- `proj_[ID]_chat_index`: Metadata about chats within a specific Claude Project.

---

## 3. Key Functionalities

### A. Scanning & Identification
- `scanForFileList()`: The primary engine that crawls the DOM. It identifies "Generated", "Project", and "Uploaded" artifacts by scoring candidates based on structural cues (selectors like `[data-testid*="artifact"]`).
- `scoreCandidate(node)`: Assigns a likelihood score to a DOM node to determine if it's a valid artifact.
- `findArtifactSidebar()`: Robustly locates the sidebar container across varying DOM structures using text-based ("Artifacts", "Files") and icon-based detection.

### B. UI Injection & Anchoring
- `injectToggleButtons()`: Injects the primary `⬡` (Sorter) and `⌬` (Summary) buttons into the platform's header.
- `injectSidebarSortBar(items)`: Places the sorting controls (Name, Date, Order) directly into the Claude sidebar.
- **Sidebar Detection Strategy**: Specifically targets `h2, h3, h4` headers containing "Artifacts" and their parent `.flex.flex-col.gap-3` containers.
- **Chat Flow Exclusion (CRITICAL)**: Any container matching `.mx-auto` (the centered chat column) or `[data-chat-input-container]` is strictly blacklisted. This prevents the CAS toolbar and metadata from leaking into the chat conversation flow.
- **Injection Boundaries**: All injection helpers (`injectSummary`, `injectDate`, etc.) must perform a safety check for `.font-claude-response` or `.mx-auto` before rendering to ensure 100% isolation from the message stream.

### C. VFT Tagging System
- **VFT Categories**: Integrates a 16-category philosophical framework (Logic, Ethics, Metaphysics, etc.).
- `buildFloatingTagPicker()`: A specialized UI for manual tagging that supports both major categories and granular subtags.
- `injectTags()`: Dynamically renders category chips onto the artifact cards in the sidebar and chat flow.

### D. AI Summarization & Injection
- `performSummarise()`: Generates a JSON-structured prompt for Claude to summarize detected artifacts and assign VFT tags.
- `performInjection()`: Parses Claude's JSON response and "injects" the data into the local storage and UI.
- `performChatSummarise()`: A higher-level summarization tool that analyzes the conceptual evolution of the entire conversation.
- **Flyout Search**: Provides real-time local filtering of chat topics and aspects within the summary flyout panel, using an `input` listener to dynamically update the display.

### E. Navigation & Context
- `jumpToArtifact(name)`: Smoothly scrolls the chat view to the specific message where an artifact was generated, using `data-cas-name` attributes for precision.
- `onChatChange()`: Tracks SPA navigation (URL changes) to reset observers and refresh the UI for new chat contexts.

---

## 4. Interaction Logic
- **Single-Click**: Highlights and centers the corresponding artifact in the chat or sidebar.
- **Double-Click**: Triggers the native platform's "Open" action for that artifact.
- **Hover/Title**: Displays metadata (First seen, full name, storage status).

---

## 6. Platform Specifics

### Claude Implementation
- **Anchoring**: Pinned to `[data-testid="wiggle-controls-actions"]` or the sidebar header.
- **Artifact Scoring**: Relies heavily on `aria-label` patterns and `data-testid` attributes.
- **Navigation**: Uses a custom `PopState` listener to track Claude's internal SPA transitions.

### Gemini Implementation
- **Anchoring**: Pinned to `.right-section` or `context-sidebar`.
- **Timestamp Extraction**: Uses a specialized regex to extract Unix timestamps from Gemini's internal `jslog` attributes (`BardVeMetadataKey`).
- **Sidebar Detection**: Specifically searches for the `<context-sidebar>` element.

- **Polling**: The engine uses a 1500ms `setInterval` for "zombie-checking" UI elements, ensuring buttons and toolbars are re-injected if the platform's SPA wipes the DOM.
- **Throttling**: MutationObservers are used sparingly (specifically on the `<title>` element) to minimize performance overhead.
