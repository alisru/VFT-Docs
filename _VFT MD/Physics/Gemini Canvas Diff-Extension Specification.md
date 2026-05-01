# Gemini Canvas Diff-Extension Architecture Specification

## 1. Overview

I require a Chrome browser extension (Manifest V3) designed to bypass the output generation limits of Large Language Models (LLMs) when working with massive code files (e.g., 3000+ lines).

Currently, the LLM can ingest the code but fails to output a full rewrite due to token limits. This extension shifts the rewriting workload to the local browser. The LLM will be instructed to output only a precise JSON payload of diff operations. The extension will read this JSON, apply it to a local master string, and inject the completed code into the web application\'s virtualized code editor (Canvas).

## 2. Core Architecture

The extension must consist of three main components:

- manifest.json (Manifest V3, requiring storage and activeTab/content_script permissions).

- styles.css (For a floating side-panel UI).

- content.js (The core logic engine).

### 2.1. Master State Management

The target web editor uses DOM virtualization (windowing). HTML nodes for specific lines do not exist unless currently scrolled into view. Therefore, the extension cannot target DOM nodes by line number.

- The extension must maintain a masterCodeState string variable in memory.

- The user will paste the initial 3000-line code into a custom \<textarea\> within the extension\'s floating UI to initialize this master state.

### 2.2. The JSON Diff Payload

The LLM will output code blocks fenced with json:diff-payload. The extension must look for this exact structure:

{\
\"operations\": \[\
{\
\"action\": \"replace\",\
\"start_line\": 2850,\
\"end_line\": 2865,\
\"content\": \"def new_function():\\n return True\"\
},\
{\
\"action\": \"insert\",\
\"line\": 1500,\
\"content\": \" \# Added new logic block\\n process_data(input)\"\
},\
{\
\"action\": \"delete\",\
\"start_line\": 42,\
\"end_line\": 45\
}\
\]\
}

### 2.3. The Mutation Observer

The content.js script must deploy a MutationObserver on the chat container (e.g., document.querySelector(\'chat-app\') or document.body as a fallback) to watch the chat DOM for new nodes.

- It must extract text from \<code\> blocks generated within the chat response elements.

- **CRITICAL PARSER WARNING:** When writing the JavaScript for this observer, the LLM generating the code MUST NOT use three consecutive backticks in any string literals or regex (e.g., do not write /\`\`\`/). This will break the LLM\'s own file generation parser. Use String.fromCharCode(96) or regex quantifiers like /\`{3}/ instead.

### 2.4. Reverse-Sequential Patching (The Line Shift Fix)

When the JSON is parsed, the operations array must be sorted in descending order based on the start_line or line property.

- Applying edits to the highest line numbers first ensures that the array indices of the code above remain static.

- The logic must split the masterCodeState string by \\n into an array, use Array.prototype.splice() to execute the deletes, inserts, and replaces, and then join the array back into a string.

### 2.5. Synthetic Paste Injection (Bypassing Framework State)

Because the target canvas is managed by strict state frameworks like Google Wiz and utilizes advanced editor components (often Monaco or CodeMirror instances), altering the .innerText of the DOM will fail. The extension must trick the application into accepting the update as a user action.

- **Precise DOM Selectors:** Due to Wiz class name obfuscation and Shadow DOM nesting, the extension must cascade through known editor selectors to find the active canvas. Locate the active canvas editor using this exact Javascript logic:

const editorTarget =\
// 1. Target Monaco Editor textarea (common in web canvases)\
document.querySelector(\'.monaco-editor textarea\') \|\|\
// 2. Target CodeMirror 6 content area\
document.querySelector(\'.cm-content\[contenteditable=\"true\"\]\') \|\|\
// 3. Target standard Wiz framework areas within Shadow DOMs specifically in the canvas side-panel\
document.querySelector(\'model-viewer, custom-canvas-element\')?.shadowRoot?.querySelector(\'\[contenteditable=\"true\"\]\') \|\|\
// 4. Fallback to any active generic contenteditable inside the right-hand panel\
document.querySelector(\'right-panel \[contenteditable=\"true\"\], .canvas-container \[contenteditable=\"true\"\]\') \|\|\
// 5. Ultimate fallback\
document.querySelector(\'\[contenteditable=\"true\"\]\');

- Execute editorTarget.focus().

- Execute document.execCommand(\'selectAll\', false, null) to highlight all existing virtualized text.

- Create a new DataTransfer() object and set its text data to the newly patched masterCodeState.

- Dispatch a new ClipboardEvent(\'paste\', { clipboardData: \... }) to the editorTarget.

## 3. UI Requirements

The extension needs a floating UI panel injected into the page with a high z-index (e.g., 999999).

- A toggle button to show/hide the panel.

- A \<textarea\> to hold the master code.

- A \"Save to Memory\" button to initialize the masterCodeState.

- A \"Force Inject\" button to manually trigger the synthetic paste event.

- A status text field to log observer detections and patching success/failures.
