# PDF Translation Viewer — Design Spec

## Overview

A static web app that displays pages of a Japanese PDF document alongside their Japanese transcription and English translation. Deployable to GitHub Pages with no build step.

## Source Material

- **PDF:** `F0200000.pdf` — 23 pages (document pages 67-89) from an NPA publication titled "50 Years of Japanese Police: Trajectory and New Developments" (日本警察50年の軌跡と新たなる展開)
- **Translation:** `F0200000_full_translation.md` — OCR'd Japanese text and English translation for all 23 pages

## Architecture

Single static HTML file (`index.html`) with inline CSS and JS. PDF pages pre-rendered as PNG images in an `images/` folder. All text content baked directly into the HTML. No frameworks, no build tools, no external dependencies.

### File Structure

```
npa-translation/
  index.html              # The app
  images/
    page-01.png           # Pre-rendered PDF pages
    page-02.png
    ...
    page-23.png
  F0200000.pdf            # Original PDF (kept for reference)
  F0200000_full_translation.md  # Source translation (kept for reference)
```

## Layout

Two-column layout, roughly 50/50 horizontal split.

### Left Column — PDF Pages

- PDF page images stacked vertically
- Each image gets a subtle box shadow and border to resemble a document page
- Images scale to fill the column width

### Right Column — Text Panels

One panel per page, each containing:

1. **English translation** (primary focus)
   - Larger font size (~16-18px)
   - Full opacity
   - Standard readable body text styling

2. **Japanese transcription** (secondary reference)
   - Smaller font size (~13-14px)
   - Muted opacity (~0.5-0.6)
   - Placed below the English text

3. **Page label** — small "Page X (p.YY)" indicator at the top of each panel to orient the reader

A subtle divider separates each page's content block.

## Scroll Sync

Both columns scroll independently but stay linked by page. As the user scrolls either column, the other column adjusts to keep the corresponding page roughly aligned. Implementation: use `IntersectionObserver` on page elements in the scrolled column to detect which page is in view, then `scrollIntoView` the matching element in the other column.

Sync should be smooth (not jarring snaps) and avoid infinite scroll-event loops (temporarily disable the listener on the synced column while programmatically scrolling it).

## Header

Fixed top bar containing:

- Document title: "50 Years of Japanese Police" / 日本警察50年の軌跡と新たなる展開
- Page indicator: "Page X of 23" updated based on scroll position

## Styling

- Clean, minimal design
- Light background (#f5f5f5 or similar), white content panels
- Good reading typography — system font stack or a clean sans-serif
- PDF images: subtle shadow, slight border-radius
- Responsive enough for laptop screens; mobile is not a priority

## Deployment

GitHub Pages from the repo root (or a `docs/` folder if preferred). No build step — push and it's live.

## Pre-rendering

PDF pages rendered to PNG using a script (e.g., `pdftoppm`, ImageMagick, or Python `pdf2image`). Target resolution: 150-200 DPI, sufficient for clear reading without excessive file size. Run once as a build/prep step, commit the images.

## Content Extraction

The markdown translation file is structured as `# Page X (p.YY)` with `## Japanese` and `## English Translation` subsections. A simple script will parse this and inject the content into the HTML template. Alternatively, done manually or by the implementation agent since it's only 23 pages.

## Out of Scope

- Mobile-optimized layout
- Search functionality
- Dark mode
- Live PDF rendering (pdf.js)
- Multi-document support
