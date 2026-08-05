# Walkthrough - Gemini LaTeX Exporter Extension (OAuth Version)

This document details the newly created Chrome Extension designed to export Gemini web responses to Google Docs with **clean, editable LaTeX syntax** rather than low-resolution, non-editable images.

This version uses **direct Google OAuth integration** to create and populate the document in your Google Drive automatically with **zero clicks/no pasting required**.

---

## What We Did

We created a custom Manifest V3 Chrome Extension containing the following files under [gemini-latex-exporter](file:///e:/Vector%20Field%20Theory/VFT%20Docs/gemini-latex-exporter/):

1.  **[manifest.json](file:///e:/Vector%20Field%20Theory/VFT%20Docs/gemini-latex-exporter/manifest.json)**: Configures the extension, permissions (`identity`), background service worker, and the `"oauth2"` client ID mapping for the app. Pinned with a stable public key to guarantee the extension ID is always `mldaenkgmbajbpepfiegdjgnbedkiilf`.
2.  **[content_gemini.js](file:///e:/Vector%20Field%20Theory/VFT%20Docs/gemini-latex-exporter/content_gemini.js)**: Runs on `gemini.google.com`.
    - Detects when the "Share & export" button is clicked.
    - Dynamically injects an **"Export to Docs (TeX)"** option.
    - When clicked, extracts the response HTML, replaces KaTeX math formatting with raw LaTeX tags (`$ ... $` and `$$\n ... \n$$`), and sends a message to the background script.
    - Shows an elegant, animated status toast ("Preparing...", "Exporting...", "Success!").
3.  **[background.js](file:///e:/Vector%20Field%20Theory/VFT%20Docs/gemini-latex-exporter/background.js)**: Service worker running in the background.
    - Listens for export requests.
    - Obtains an OAuth token via `chrome.identity.getAuthToken`.
    - Executes a multipart upload to the Google Drive API (`https://www.googleapis.com/upload/drive/v3/files`), passing the HTML and specifying `mimeType: "application/vnd.google-apps.document"` (telling Drive to automatically compile it into a Google Doc).
    - Opens the newly created Google Doc in a new browser tab.
4.  **[style.css](file:///e:/Vector%20Field%20Theory/VFT%20Docs/gemini-latex-exporter/style.css)**: Custom styles for the injected menu button and the slide-up toasts on the Gemini page.

---

## How to Reload and Test the Extension

1. Go to `brave://extensions/` (or `chrome://extensions/`).
2. Click the **Reload** (circular arrow) icon on the **Gemini LaTeX Docs Exporter** card to reload the updated code.
3. Refresh your **Gemini Web** page (`https://gemini.google.com/`).
4. Ask Gemini a question containing LaTeX, e.g.:
   > "Write down Euler's formula and explain it with inline math and display math."
5. Once generated, click the **Share & export** (share icon) at the bottom of the response, and select **"Export to Docs (TeX)"**.
6. The first time you run this, you will see a Google login popup:
   * Select your Google Account.
   * Because the app is local/in testing, you will see a screen saying: *"This app isn't verified by Google"*.
   * Click **Advanced** at the bottom, then click **"Go to Gemini LaTeX Exporter (unsafe)"** to authorize the extension to create files.
7. You will see a slide-up toast saying *"Exporting to Google Docs..."*, and in 1-2 seconds, a new tab will open with your Google Doc **completely created and formatted** with editable LaTeX text!
