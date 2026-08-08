# Walkthrough: VFT Horizontal Matrix & 32-Category Timeline

This document summarizes the changes made to implement the 32-category split and the Horizontal Grid Matrix view mode in the Timeline Explorer.

## Changes Made

### 1. 32-Category Split Logic (`viewer.html`)
* Added `VFT_32_CATEGORIES` which lists all 16 Optimisms and 16 Pessimisms (Isms) as distinct categories, completely un-baking merged pairs like `"Physics / Meta-Physics"` and `"Internal Judgment / Conscience"`.
* Implemented `getFileCategories(file)` to parse a document's VFT indicators (node name, quadrant, and specific isms) and map it to one or more of the 32 distinct categories:
  * For example, files mapping to `Physics / Meta-Physics` are now correctly routed to either `Physics (Objectivity)` or `Meta-Physics (Imagination)` based on their isms (`Objectivity` or `Imagination`), or both if both apply.

### 2. Horizontal Grid Timeline Mode (`viewer.html`)
* **Header Toggles:** Added view mode toggle buttons (`☰ List View` and `box⊞ Grid View`) to switch between the original vertical list layout and the new horizontal grid matrix.
* **Sticky 2D Matrix Table:** Implemented `drRenderHorizontalGrid(items)` which builds a sticky 2D table matrix:
  * **Y-Axis (Left Column, Sticky):** The VFT Categories. To keep the grid dense, only rows containing active matching notes are rendered.
  * **X-Axis (Top Row, Sticky):** Sorted dates in reverse chronological order.
  * **Grid Cells:** clickable mini-cards displaying notes created on that date mapping to that category. Clicking a card navigates directly to the document reader.

---

## Verification Results

* **Visual Check:** Switched to "Grid View" locally, verifying that dates scroll horizontally while categories stay frozen on the left.
* **Separation Verified:** Notes previously grouped under combined categories are now cleanly separated across distinct rows (e.g. *Physics* on the Physics row, *Meta-Physics* on the Meta-Physics row).
