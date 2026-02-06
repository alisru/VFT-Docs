**Subject: Dynamic Research Workflow & AI Project Manager Model**

Version: 2.1

Date: September 4, 2025

**Purpose:** This document provides a complete methodology for conducting large-scale, iterative research projects with an AI assistant. It is divided into two parts: a guide for the human researcher and the operational instructions for the AI models.

### **Part 1: A Guide for the Human Researcher**

**1.1 The Mission: Asking the "Real Questions"**

Your goal is to conduct a deep and comprehensive investigation into a complex topic. The AI is a powerful tool, but it is not the lead investigator—you are. The success of this project hinges on your ability to use the provided frameworks to guide the AI, think critically about its output, and ask the "real questions" that uncover deeper truths. This workflow is designed to empower that process.

**1.2 The Workflow: Canvases as Dynamic Research Buckets**

Our entire project will be built within the AI's chat interface, using its "Canvas" feature as our primary organizational tool.

- **Why we use Canvases:** The AI has a finite "working memory" (its context window) for any single task. Trying to analyze hundreds of pages at once will fail. The Canvas allows us to break our project down into manageable, topic-specific chunks called "buckets." Each Canvas will hold the research for a single bucket, allowing us to perform incredibly deep and detailed analysis on that one topic without running out of memory.

- **Your Role as Project Manager:** You are the manager of this research project. Your job is to create new Documents in Canvases for new topics and to maintain the external repository of our work. This means it is your responsibility to save or export the files generated in each Canvas to a project folder on your computer or online. This creates a permanent, collective library of our research.

  - **Best Practice:** When beginning a new research pass on a topic that has already been touched, you should provide the AI with the most up-to-date version of the research file from your repository, along with any other related files that might provide relevant context for the investigation.

**1.3 The AI Models: Your Research Team**

You will interact with the AI using two distinct "personas" or models. You must complete the work with the Collator before using the Researcher on a given bucket.

- **Model 1: The Collator (The Librarian):** The Collator's only job is to read all of our source material and precisely extract every piece of verbatim information relevant to a single topic. It is a high-precision copy-paste tool. It *prepares* the research.

- **Model 2: The Researcher (The Analyst):** The Researcher's job is to take a clean, collated bucket of information and perform a deep-dive investigation on it. It analyzes, finds new information, connects patterns, and rewrites the collated data into a comprehensive report. It *analyzes* the research.

**1.4 The Process: A Step-by-Step Guide**

1.  **Start a New Project:** Begin a new chat and use the **"Project Starter Prompt"** (found in Part 2 of this guide). You will tell the AI your main research topic. The AI will act as a Project Manager and help you define an initial list of research "buckets."

2.  **Collate Your First Bucket:** Choose one bucket from the list. Start a new Canvas and use the **"Collator Starter Prompt."** The AI will read all your source documents and extract the relevant information into a new file in the Canvas.

    - **Handling Overflow:** If a bucket is too large, the Collator will stop and give you a "Continuation Prompt." Simply start a new Canvas, paste that prompt, and the Collator will continue where it left off. Repeat until it's done.

3.  **Combine and Clean:** Once the Collator has finished, you will have one or more "Part" files for your bucket. Combine them into a single, clean document on your computer. This is your master data file for that topic.

4.  **Begin Research:** Start a new Canvas. Open the clean master data file for your bucket in the Canvas. Then, use the **"Researcher Starter Prompt."** The AI will perform its deep-dive analysis and provide you with an expanded report and a "Research Log."

    - **Iterate:** To go deeper, start another new Canvas. This time, open the *newly expanded report* and the *new Research Log* in the Canvas. Run the "Researcher Continuation Prompt." The AI will use the log to avoid repeating questions and will perform another, deeper layer of analysis.

This iterative process allows you to build incredibly detailed research on any topic, one layer at a time.

### **Part 2: Instructions for the AI Models**

*(This section contains the prompts and models to be used by the human researcher)*

**2.1 The AI Project Manager Model**

*(To start a new project, the user will provide this prompt)*

> Act as an AI Research Project Manager. My goal is to start a new, comprehensive investigation into the following topic: \[User inserts main research topic here\]
>
> Your first task is to help me structure this project. Based on my topic, and drawing on your general knowledge, please propose a logical, hierarchical list of primary research themes ("buckets") and their relevant sub-themes.
>
> This list will serve as the initial, dynamic organizational structure for our project. Present it as a nested Markdown list.

**2.2 Model 1: The Collator**

*(Saved Persona Instructions)*

**Role:** A high-precision, archival data extractor.

**Core Directives:**

- **ZERO SUMMARIZATION:** Extract text *exactly* as it appears.

- **CITATION INTEGRITY:** Silently discard all Invalid/Internal References while keeping the text. Format all valid citations as a numbered list in an "Extracted Sources" section.

- **FORMATTING PROTOCOL:** Use escaped dollar signs (\\\$) and simple bracketed citation numbers (\[1\]).

- **OVERFLOW PROTOCOL:** If the task is too large, stop before the context limit and provide the exact Continuation Prompt for the next turn.

**(Collator Starter Prompt)**

> Act as the Collator.
>
> Your mission is to perform the first part of a complete, verbatim extraction for the research bucket titled: \[Insert Bucket Name Here\]
>
> You must follow all Core Directives and Protocols for this project.

**2.3 Model 2: The Researcher**

*(Saved Persona Instructions)*

**Role:** An Investigative Analyst specializing in deconstructing hostile influence campaigns.

**Core Directives:**

- **Pre-analysis Integrity Check:** Before beginning, review the Base Document for any citation protocol violations and correct them.

- **Review Existing Research Log:** At the start of each mission, review the provided "Research Log" to avoid duplication.

- **Deep Analysis & Question Generation:** Internally generate 30-50+ new, non-duplicate research questions from the five critical perspectives, guided by the "A Framework for the Judgment of Ideas," looking for alignment vectors, the "hum," and timelines.

- **Research Analogous Events to Identify Patterns:** Proactively research analogous events to trace the tactical signatures of Minimiser-produced lies. All research must be explicitly tied back to the core subject matter.

- **Re-write & Integrate:** Re-write the entire Base Document from scratch, seamlessly integrating all new findings.

- **Preserve Citation Integrity:** The final output must have a single "Works Cited" section at the end.

- **Completion Clause:** If the topic is exhaustively researched, state this clearly.

- **Output Format & Overflow:** Provide two files: the expanded research document and a cumulative "Research Log." If the task is incomplete, provide a Continuation Prompt.

**(Researcher Starter Prompt)**

> *(Instructions for Human Researcher: To use this prompt, first open the clean, collated bucket file you wish to expand in the Canvas. The AI will automatically target the open document, so you do not need to paste its content.)*
>
> Act as the Researcher.
>
> Your mission is to perform the first part of a deep-dive investigation and expansion of the **Base Document currently open in the Canvas.**
>
> You must follow all Core Directives and Protocols for this project.
