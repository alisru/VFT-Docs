AI Task: Convert Document to Styled HTML

Objective: Convert the provided text document into a single, fully-structured HTML file based on the rules below.

1.  Global Structure
    DOCTYPE: The file must start with \<!DOCTYPE html\>.
    Root Element: The root element is \<html lang="en-US"\>.
    Main Container: All primary content within the \<body\> must be wrapped in a single \<div class="container-lg px-3 my-5 markdown-body"\>.

\<head\> Section Requirements

The \<head\> section must be constructed as follows:

- Meta Tags: Include the following meta tags exactly as shown, replacing bracketed placeholders with content from the source document. \<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"\>\<meta http-equiv="X-UA-Compatible" content="IE=edge"\>\<meta name="viewport" content="width=device-width, initial-scale=1"\>\<title\>\[Document Title\] \| \[Site Name\]\</title\>\<meta property="og:title" content="\[Document Title\]"\>\<meta property="og:locale" content="en_US"\>\<meta name="description" content="\[Brief document description\]"\>\<meta property="og:description" content="\[Brief document description\]"\>\<meta property="og:site_name" content="\[Site Name\]"\>\<meta property="og:type" content="website"\>\<meta name="twitter:card" content="summary"\>\<meta property="twitter:title" content="\[Document Title\]"\>

- JSON-LD Schema Script: Include the following script, replacing placeholders. \<script type="application/ld+json"\>{"@context":"https://schema.org","@type":"WebPage","description":"\[Brief document description\]","headline":"\[Document Title\]"}\</script\>

- Stylesheet: Link to the shared stylesheet. The tag must be exactly: \<link rel="stylesheet" href="../style.css"\>

- Google Analytics: Insert the following script block exactly as written. \<!-- Google tag (gtag.js) --\>\<script async src="https://www.googletagmanager.com/gtag/js?id=G-4QHZV5Y81G"\>\</script\>\<script\> window.dataLayer = window.dataLayer \|\| \[\]; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-4QHZV5Y81G');\</script\>

3\.

\<body\> Section Requirements

- Navigation Link: The very first element inside the main \<div\> container must be the back navigation link: \<a href="./index.html"\>← Back To Navigation\</a\>

- Content Formatting: Convert the document's text using the following HTML tags:

  - Main Title: \<h1\>

  - Chapter/Section Titles: \<h2\>

  - Sub-Section Titles: \<h3\>

  - Minor Headings/Labels: \<h4\>

  - Paragraphs: \<p\> for all body text.

  - Bulleted Lists: \<ul\> containing \<li\> elements.

  - Numbered Lists: \<ol\> containing \<li\> elements.

  - Tables: Use a \<table\> with a \<thead\>.

  - Hyperlinks: \<a\> with an href attribute.

- **Citation Hyperlinking:** The conversion process must include hyperlinking for all citations, especially those from Google Docs.

  - **Step 1 (Tag Destinations):** Find the "Works Cited" section (which may be a heading with the text "Works Cited" or an element with id="works-cited") and its ordered list (\<ol\>). Assign a unique ID to each list item (\<li\>), formatted as id="citation-N", where N is the citation number (e.g., \<li id="citation-1"\>...\</li\>).

  - **Step 2 (Link Sources):** Scan the document's main text for in-text citations. This includes three primary formats:

    - Plain text citations like \[N\] or .N. This includes multi-number citations like \[4, 11\].

    - Avoid linking any hits within h level tags

    - **Google Docs Citations:** These appear as superscripted numbers in brackets, e.g., \<sup\>\[1\]\</sup\>.

  - **Step 3 (Create Links):** Convert each found number into an \<a\> tag linking to the corresponding destination ID.

    - For plain text citations, the link should replace the number (e.g., \[\<a href="#citation-4"\>4\</a\>, \<a href="#citation-11"\>11\</a\>\]).

    - For Google Docs citations, the new \<a\> tag must be placed back inside the \<sup\> tag to preserve the original styling (e.g., \<sup\>\[\<a href="#citation-1"\>1\</a\>\]\</sup\>).

    - Ensure this process does not incorrectly link currency values (e.g., \$10.50).

4.  Responsive Floating Table of Contents (TOC)
    Implement a TOC that appears as a fixed sidebar on desktop and becomes a toggleable "drawer" menu on mobile/tablet devices.

- HTML Structure: Place the following elements immediately inside the \<body\>, before the main content \<div\>.
  \<body\>
  \<!-- TOC Drawer for both desktop and mobile --\>
  \<nav id="toc-container"\>\</nav\>
  \<!-- Mobile-only header with toggle button --\>
  \<header id="mobile-header"\>
  \<button id="toc-toggle-btn"\>
  \<span\>\</span\>
  \<span\>\</span\>
  \<span\>\</span\>
  \</button\>
  \</header\>
  \<!-- Overlay for mobile drawer --\>
  \<div id="toc-overlay"\>\</div\>
  \<!-- Main Content --\>
  \<div class="container-lg px-3 my-5 markdown-body"\>
  \<!-- All page content goes here --\>
  \</div\>
  \<!-- Scripts go at the end of the body --\>
  \</body\>

- CSS Styling: Crucial: These styles must be added to the ../style.css file. The functionality will not work without them, and the mobile toggle button will appear to do nothing.
  /\* --- Generic TOC Styles --- \*/
  #toc-container h4 { margin-top: 0; font-size: 1em; color: #333; }
  #toc-container ul { list-style: none; padding: 0; margin: 0; }
  #toc-container li a {
  display: block; text-decoration: none; color: #555;
  padding: 6px 0 6px 10px; font-size: 0.9em; transition: all 0.2s ease;
  border-left: 2px solid transparent;
  }
  #toc-container li a.toc-h3 { padding-left: 25px; } /\* Indent sub-headings \*/
  #toc-container li a:hover { color: #000; }
  #toc-container li a.active { color: #007bff; font-weight: bold; border-left-color: #007bff; }
  /\* --- Desktop TOC (Sidebar) --- \*/
  \@media (min-width: 1400px) {
  #toc-container {
  position: fixed; top: 80px; left: 20px; width: 220px;
  max-height: calc(100vh - 100px); overflow-y: auto;
  border-left: 2px solid #e0e0e0; padding: 10px 15px;
  }
  #toc-container li a { margin-left: -17px; }
  .markdown-body { margin-left: 260px; } /\* Push content to the right \*/
  #mobile-header { display: none; }
  }
  /\* --- Mobile TOC (Off-canvas Drawer) --- \*/
  \@media (max-width: 1399.98px) {
  #mobile-header {
  display: block; position: fixed; top: 10px; left: 10px;
  z-index: 1001;
  }
  #toc-toggle-btn {
  background: #fff; border: 1px solid #ddd; border-radius: 5px;
  width: 44px; height: 44px; padding: 8px; cursor: pointer;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  #toc-toggle-btn span {
  display: block; width: 100%; height: 2px; background: #333;
  margin: 4px 0; transition: transform 0.3s ease;
  }
  #toc-container {
  position: fixed; top: 0; left: 0; height: 100%; width: 280px;
  background: #f9f9f9; z-index: 1002; padding: 20px;
  transform: translateX(-100%); transition: transform 0.3s ease-in-out;
  overflow-y: auto; box-shadow: 5px 0 15px rgba(0,0,0,0.1);
  }
  #toc-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.5); z-index: 1000;
  opacity: 0; visibility: hidden; transition: opacity 0.3s ease;
  }
  /\* Active states for mobile drawer \*/
  body.toc-open #toc-container { transform: translateX(0); }
  body.toc-open #toc-overlay { opacity: 1; visibility: visible; }
  body.toc-open #toc-toggle-btn span:nth-child(1) { transform: translateY(6px) rotate(45deg); }
  body.toc-open #toc-toggle-btn span:nth-child(2) { opacity: 0; }
  body.toc-open #toc-toggle-btn span:nth-child(3) { transform: translateY(-6px) rotate(-45deg); }
  }

- JavaScript Logic: Add the following script block at the very end of the \<body\>.
  \<script\>
  document.addEventListener('DOMContentLoaded', function () {
  // --- 1. Element Selection ---
  const tocContainer = document.getElementById('toc-container');
  const contentContainer = document.querySelector('.markdown-body');
  const tocToggleButton = document.getElementById('toc-toggle-btn');
  const tocOverlay = document.getElementById('toc-overlay');
  if (!tocContainer \|\| !contentContainer) return;
  // --- 2. Generate TOC Content ---
  const headings = contentContainer.querySelectorAll('h2, h3');
  if (headings.length === 0) {
  tocContainer.style.display = 'none';
  if (tocToggleButton) tocToggleButton.style.display = 'none';
  return;
  }
  const tocTitle = document.createElement('h4');
  tocTitle.textContent = 'On this page';
  tocContainer.appendChild(tocTitle);
  const tocList = document.createElement('ul');
  headings.forEach((heading, index) =\> {
  if (!heading.id) heading.id = \`heading-ref-\${index}\`;
  const listItem = document.createElement('li');
  const link = document.createElement('a');
  link.textContent = heading.textContent;
  link.href = \`#\${heading.id}\`;
  link.classList.add(heading.tagName.toLowerCase() === 'h3' ? 'toc-h3' : 'toc-h2');
  listItem.appendChild(link);
  tocList.appendChild(listItem);
  });
  tocContainer.appendChild(tocList);
  const tocLinks = tocContainer.querySelectorAll('a');
  // --- 3. Mobile Drawer Functionality ---
  const closeTocDrawer = () =\> document.body.classList.remove('toc-open');
  if (tocToggleButton && tocOverlay) {
  tocToggleButton.addEventListener('click', () =\> document.body.classList.toggle('toc-open'));
  tocOverlay.addEventListener('click', closeTocDrawer);
  }
  tocLinks.forEach(link =\> link.addEventListener('click', closeTocDrawer));
  // --- 4. Active Link Highlighting on Scroll ---
  const getAbsoluteTop = (element) =\> {
  let top = 0;
  while (element) {
  top += element.offsetTop;
  element = element.offsetParent;
  }
  return top;
  };
  const headingPositions = Array.from(headings).map(h =\> ({
  id: h.id,
  top: getAbsoluteTop(h)
  }));
  let scrollTimeout;
  const setActiveLink = () =\> {
  clearTimeout(scrollTimeout);
  scrollTimeout = setTimeout(() =\> {
  let currentId = '';
  const scrollPosition = window.scrollY + 120; // Offset for better UX
  for (let i = headingPositions.length - 1; i \>= 0; i--) {
  if (scrollPosition \>= headingPositions\[i\].top) {
  currentId = headingPositions\[i\].id;
  break;
  }
  }
  tocLinks.forEach(link =\> {
  link.classList.remove('active');
  if (link.getAttribute('href') === \`#\${currentId}\`) {
  link.classList.add('active');
  }
  });
  }, 50); // 50ms debounce delay
  };
  window.addEventListener('scroll', setActiveLink);
  setActiveLink(); // Set initial state
  });
  \</script\>

Ensure all citations and html urls are hyperlinked to the stated url
