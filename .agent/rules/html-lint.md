
# HTML Lint Rule

After editing any `.html` file, run an HTML validator before reporting the work as done:

`npx --yes html-validate <file>`

- Fix every error that your edit caused. Do not silence rules to make it pass.
- Browsers accept broken HTML without any error, so `node -c` and the console will NOT catch it.
  An unclosed `<textarea>`, `<iframe>`, `<title>`, `<style>` or `<!--` can swallow the rest of the page, including the `<script>` tags.
- Raw tag names inside visible text (for example in a table cell) must be escaped: `&lt;textarea&gt;`.

## When a page loads blank with no console errors
1. Check whether the script is in the DOM first (`document.scripts`). If it is missing, the bug is in the HTML.
2. Compare the `.html` diff against git before reading the JavaScript.
