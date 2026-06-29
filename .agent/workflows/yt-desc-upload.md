---
description: How to generate YouTube descriptions for videos in a folder and upload them to the channel via the YouTube Data API
---

This workflow scans a folder for `.mp4` files, transcribes each with Whisper, generates a YouTube description from the transcript using AI, saves it as a `.desc.txt` sidecar file, then uploads the video to YouTube via the API. Descriptions on already-uploaded videos are never touched automatically — only new uploads.

---

## Prerequisites (One-Time Setup)

Config file lives at:
`e:\Vector Field Theory\VFT Docs\_AI files and chat logs\Videos\yt_config.json`

You need two credential files in that same folder:

1. **`client_secret*.json`** — OAuth2 client credentials
   - Google Cloud Console → APIs & Services → Credentials → Create OAuth 2.0 Client ID (Desktop App) → Download JSON and place it in the folder. The script automatically scans for `client_secret*.json` so you do not need to rename it.
2. **`yt_token.json`** — auto-generated on first auth run (see Step 4)

The API key (`AIzaSyCgHxeY04l6JQmSV5y9-x4UQoxRKO4-rR4`) is already saved in `yt_config.json`.

---

## Usage

Tell the agent:
> *"make yt descs for videos in [folder path] and upload them"*

Or target a specific video:
> *"make a yt desc for The_Geometry_of_Truth.mp4 and upload it"*

The agent will run through the steps below.

---

### Step 1: Identify Target Videos

The agent scans the specified folder for `.mp4` files without an existing `.desc.txt` sidecar. If all videos already have descriptions, ask the user whether to regenerate.

**Agent task** — no script needed. List files like:
```powershell
Get-ChildItem "e:\Vector Field Theory\VFT Docs\_AI files and chat logs\Videos" -Filter "*.mp4" | Where-Object { -not (Test-Path ($_.FullName -replace '\.mp4$', '.desc.txt')) }
```

---

### Step 2: Transcribe with Whisper + Generate Description

For each video without a `.desc.txt` sidecar:

**2a — Transcribe audio with Whisper:**
```powershell
python "e:\Vector Field Theory\VFT Docs\_AI files and chat logs\Videos\yt_transcribe.py" --file "path\to\video.mp4"
```
Outputs a `.transcript.txt` sidecar. Uses `openai-whisper` locally (no API call). Model defaults to `medium` — change with `--model large` for better accuracy.

**2b — Generate description and image prompts in Pack Format (Agent Task):**
The agent reads the `.transcript.txt` and writes a sidecar `.desc.txt` file next to the video. This file MUST strictly follow the parsed Pack Format defined in [yt_desc_styleguide.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_AI%20files%20and%20chat%20logs/Videos/yt_desc_styleguide.md). 

Do NOT invent arbitrary templates. Use the following exact layout:

```text
=== TITLE ===
[SEO-Optimized, High-CTR Title]

=== DESCRIPTION ===
[1-2 Sentence Hook - First 150 chars - Primary keyword + viewer benefit, drawn from video opening]

[3-5 Sentence Summary - 200-250 words total body - Natural secondary keyword integration. Only reference concepts spoken in the transcript]

0:00 [Keyword-rich chapter label]
X:XX [Keyword-rich chapter label]
X:XX [Keyword-rich chapter label]
(minimum 3 timestamps, must start at 0:00, each chapter min 10 seconds)

[CTA - One specific engaging question to drive comments]

---
📌 Topics: [Comma-separated search topics]

=== TAGS ===
[Comma-separated tags for YouTube backend metadata]

=== IMAGE PROMPTS ===
[Detailed Pop-Art Paper-Cut Collage prompt for cover generation in 16:9 format, ending with --ar 16:9]
```

Save as `.desc.txt` sidecar in the video's directory:
- `The_Geometry_of_Truth.desc.txt`

**2c — Generate cover image (Agent Task):**
1. Generate the widescreen cover image natively using the agent's `generate_image` tool using the prompt from the `=== IMAGE PROMPTS ===` section.
2. Ensure the prompt explicitly requests `16:9 widescreen format` and ends with `--ar 16:9`.
3. Save or copy the generated image as `<video_name>.cover.png` and `<video_name>.cover_v1.png` inside the video's subdirectory.

---

### Step 3: Review Checkpoint (No Duplicate Files)

**STOP HERE.** 
* **DO NOT** create review files or markdown artifacts (like `toBeUploaded_review.md`) containing duplicate copies of the descriptions. This wastes output tokens.
* Simply alert the user in the chat that the `.desc.txt` sidecars and `.cover.png` files have been written directly to their folders in the workspace.
* Ask the user to review the files directly in their workspace and provide approval to upload.
* Do not proceed to Step 4 without explicit user approval.


---

### Step 4: Authenticate with YouTube (First Run Only)

```powershell
python "e:\Vector Field Theory\VFT Docs\_AI files and chat logs\Videos\yt_auth.py"
```

`client_secret.json` identifies your app to Google, but YouTube OAuth2 still requires a **one-time user consent step** to authorise that app to act on your channel. This opens a browser window once — you click Allow, and `yt_token.json` is written. Every subsequent run uses the cached token silently with no browser involved.

This is a YouTube API requirement and cannot be skipped — service accounts don't have channel write access.

Skip this step if `yt_token.json` already exists and is valid.

---

### Step 5: Upload to YouTube

Uploads the `.mp4` with the generated description as a new video. Does **not** touch any existing videos on the channel.

```powershell
python "e:\Vector Field Theory\VFT Docs\_AI files and chat logs\Videos\yt_upload.py" --file "path\to\video.mp4" --visibility private
```

Visibility options: `private` (default) · `unlisted` · `public`

To override the default title parsed from the filename (e.g. replacing underscores and formatting colons), use the `--title` argument:
```powershell
python "e:\Vector Field Theory\VFT Docs\_AI files and chat logs\Videos\yt_upload.py" --file "path\to\video.mp4" --visibility private --title "Your Explicit Title Here"
```

To batch-upload all videos in a folder that have a `.desc.txt` sidecar:
```powershell
python "e:\Vector Field Theory\VFT Docs\_AI files and chat logs\Videos\yt_upload.py" --folder "e:\Vector Field Theory\VFT Docs\_AI files and chat logs\Videos" --visibility private
```

The script will:
1. Read the `.desc.txt` sidecar for the description
2. Derive the title from the filename (underscores → spaces, strip extension)
3. Upload via `videos.insert` and report the new YouTube video ID
4. Write the returned video ID to a `.ytid.txt` sidecar for reference

---

### Step 6: Verify

Check YouTube Studio, or confirm the upload IDs from the `.ytid.txt` sidecars written next to each video.

---

## Script Files Required

These scripts need to be created before first use (agent can generate them on demand):

| Script | Purpose |
|---|---|
| `yt_auth.py` | OAuth2 flow — generates `yt_token.json` |
| `yt_transcribe.py` | Runs Whisper on an `.mp4`, outputs `.transcript.txt` sidecar |
| `yt_upload.py` | Uploads `.mp4` + `.desc.txt` as a new YouTube video |

To generate the scripts, tell the agent:
> *"build the yt workflow scripts"*

---

## Notes

- `yt_config.json` and `client_secret.json` are excluded from git via `.gitignore`
- Default video visibility for new uploads: `private`
- Whisper runs locally — no OpenAI API key needed, but requires `pip install openai-whisper` and `ffmpeg` on PATH
- The YouTube quota limit is 10,000 units/day; each `videos.insert` costs 1,600 units (~6 uploads/day on free tier)
- Existing channel videos are never modified by this workflow — descriptions are only set at upload time
