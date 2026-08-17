# Gemini LaTeX Docs & Markdown Exporter

A Manifest V3 browser extension that exports Google Gemini responses to Google Docs and local Markdown files with **clean, editable LaTeX mathematical equations** instead of fuzzy, non-editable images.

---

## Key Features

*   **Clean LaTeX Recovery:** Replaces transient KaTeX DOM rendering with original `$ ... $` (inline) and `$$\n ... \n$$` (display) LaTeX notation.
*   **Zero-Click Google Docs Export:** Utilizes Google OAuth2 flow to directly create, style, and open a Google Doc in your Drive with one click.
*   **Instant Markdown Download:** Converts responses locally into clean, github-flavored Markdown (`.md`), automatically formatting headers, lists, code blocks (with language tags), math equations, and tables.
*   **Brave Browser Integration:** Uses `chrome.identity.launchWebAuthFlow` to bypass browser-specific identity sync blocks, making it fully compatible with Brave, Chrome, and other Chromium browsers.
*   **Glassmorphic UI Toasts:** Visual feedback (loading, success, error) styled to blend seamlessly with the native Gemini interface.

---

## Local Developer Installation

1.  Clone or download this repository.
2.  Open Brave or Chrome and navigate to `chrome://extensions/` (or `brave://extensions/`).
3.  Enable **Developer mode** (toggle in the top-right corner).
4.  *(Brave users only)* Go to `brave://settings/extensions` and toggle **"Allow Google login for extensions"** to **ON**.
5.  Click **Load unpacked** in the top-left and select the [gemini-latex-exporter](file:///e:/Vector%20Field%20Theory/VFT%20Docs/gemini-latex-exporter/) folder.
6.  Note the **Extension ID** generated on the extension's card (e.g. `mldaenkgmbajbpepfiegdjgnbedkiilf`).

---

## Project Structure

*   **`manifest.json`**: Extension configuration, permissions (`identity`), and stable key setup.
*   **`background.js`**: Background service worker handling Google Drive API multipart uploads and OAuth web flow.
*   **`content_gemini.js`**: Content script injected into Gemini Web, handling LaTeX parsing, DOM cleanup, button injection, Markdown compilation, and toasts.
*   **`style.css`**: Styling for the menu buttons and slide-up toasts.
*   **`key.pem`**: The private key used to maintain a stable, permanent Extension ID.

---

## Troubleshooting OAuth Setup

To enable the direct-to-Docs export feature, you must configure a Google Cloud project to whitelist your Extension ID:
1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a project and go to **OAuth Consent Screen** (Branding/Audience). Set type to **External** and add your Gmail to **Test Users**.
3.  Select the scope: `https://www.googleapis.com/auth/drive.file`.
4.  Go to **Credentials** (Clients), click **+ Create Credentials > OAuth client ID**, and select **Chrome extension**.
5.  Enter your Extension ID and click **Create**.
6.  Copy the Client ID and insert it into `background.js`.
