# PDF Translation Viewer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a static web app displaying PDF pages alongside Japanese transcription and English translation, deployable to GitHub Pages.

**Architecture:** Single `index.html` with inline CSS/JS. Pre-rendered PNG images of PDF pages in `images/`. A Python build script parses the translation markdown and generates the final HTML. No runtime dependencies.

**Tech Stack:** HTML/CSS/JS (vanilla), Python 3 (build script), pdftoppm (PDF rendering)

---

### File Structure

```
npa-translation/
  index.html                    # Generated — the app
  build.py                      # Generates index.html from template + markdown
  template.html                 # HTML template with placeholder for page content
  images/
    page-01.png ... page-23.png # Pre-rendered PDF pages
  F0200000.pdf                  # Source PDF
  F0200000_full_translation.md  # Source translations
  docs/                         # Specs and plans (not deployed)
```

---

### Task 1: Pre-render PDF pages to PNG

**Files:**
- Create: `images/page-01.png` through `images/page-23.png`

- [ ] **Step 1: Create images directory**

```bash
mkdir -p images
```

- [ ] **Step 2: Render PDF pages to PNG at 200 DPI**

```bash
pdftoppm -png -r 200 F0200000.pdf images/page
```

This will create `images/page-01.png` through `images/page-23.png`.

- [ ] **Step 3: Verify output**

```bash
ls -la images/*.png | wc -l
```

Expected: 23 files.

```bash
ls -lh images/page-01.png
```

Verify reasonable file size (should be ~100-300KB per page at 200 DPI).

- [ ] **Step 4: Commit**

```bash
git add images/
git commit -m "feat: pre-render PDF pages as PNG images"
```

---

### Task 2: Write the HTML template

**Files:**
- Create: `template.html`

This is the shell of the app — header, two-column layout, scroll sync JS. Page content will be injected by the build script at the `<!-- PAGES -->` placeholder.

- [ ] **Step 1: Create `template.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>50 Years of Japanese Police — Translation Viewer</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background: #f0f0f0;
      color: #1a1a1a;
    }

    header {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: 52px;
      background: #fff;
      border-bottom: 1px solid #ddd;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      z-index: 100;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }

    header h1 {
      font-size: 15px;
      font-weight: 600;
      color: #333;
    }

    header h1 span.jp {
      font-weight: 400;
      color: #888;
      margin-left: 8px;
    }

    #page-indicator {
      font-size: 13px;
      color: #888;
      font-variant-numeric: tabular-nums;
    }

    .container {
      display: flex;
      margin-top: 52px;
      height: calc(100vh - 52px);
    }

    .col {
      flex: 1;
      overflow-y: auto;
      padding: 24px;
    }

    .col-pdf {
      background: #e8e8e8;
      border-right: 1px solid #ddd;
    }

    .col-text {
      background: #fafafa;
    }

    .pdf-page {
      margin-bottom: 24px;
    }

    .pdf-page img {
      width: 100%;
      display: block;
      border-radius: 2px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
      background: #fff;
    }

    .text-page {
      margin-bottom: 48px;
      padding-bottom: 32px;
      border-bottom: 1px solid #e0e0e0;
    }

    .text-page:last-child {
      border-bottom: none;
    }

    .page-label {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #999;
      margin-bottom: 16px;
      font-weight: 600;
    }

    .english {
      font-size: 17px;
      line-height: 1.7;
      color: #1a1a1a;
      margin-bottom: 24px;
    }

    .english h2, .english h3, .english h4 {
      margin-top: 20px;
      margin-bottom: 8px;
      color: #111;
    }

    .english h2 { font-size: 20px; }
    .english h3 { font-size: 18px; }
    .english h4 { font-size: 17px; }

    .english p {
      margin-bottom: 12px;
    }

    .english table {
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0;
      font-size: 14px;
    }

    .english th, .english td {
      border: 1px solid #ddd;
      padding: 6px 10px;
      text-align: left;
    }

    .english th {
      background: #f5f5f5;
      font-weight: 600;
    }

    .english ul, .english ol {
      margin: 8px 0 8px 24px;
    }

    .english li {
      margin-bottom: 4px;
    }

    .japanese {
      font-size: 14px;
      line-height: 1.8;
      color: rgba(26, 26, 26, 0.5);
      border-top: 1px solid #eee;
      padding-top: 16px;
    }

    .japanese p {
      margin-bottom: 10px;
    }

    .japanese table {
      width: 100%;
      border-collapse: collapse;
      margin: 12px 0;
      font-size: 12px;
    }

    .japanese th, .japanese td {
      border: 1px solid #e0e0e0;
      padding: 4px 8px;
      text-align: left;
    }

    .japanese th {
      background: #f8f8f8;
    }
  </style>
</head>
<body>
  <header>
    <h1>50 Years of Japanese Police<span class="jp">日本警察50年の軌跡と新たなる展開</span></h1>
    <div id="page-indicator">Page 1 of 23</div>
  </header>

  <div class="container">
    <div class="col col-pdf" id="col-pdf">
<!-- PDF_PAGES -->
    </div>
    <div class="col col-text" id="col-text">
<!-- TEXT_PAGES -->
    </div>
  </div>

  <script>
    const colPdf = document.getElementById('col-pdf');
    const colText = document.getElementById('col-text');
    const indicator = document.getElementById('page-indicator');
    const totalPages = 23;
    let syncing = false;

    function getVisiblePageIndex(container, prefix) {
      const pages = container.querySelectorAll('[data-page]');
      const containerTop = container.scrollTop;
      const containerMid = containerTop + container.clientHeight / 3;

      let closest = 0;
      let closestDist = Infinity;

      pages.forEach((page, i) => {
        const dist = Math.abs(page.offsetTop - containerMid);
        if (dist < closestDist) {
          closestDist = dist;
          closest = i;
        }
      });

      return closest;
    }

    function syncScroll(source, target) {
      if (syncing) return;
      syncing = true;

      const pageIndex = getVisiblePageIndex(source, '');
      const targetPage = target.querySelector(`[data-page="${pageIndex + 1}"]`);

      if (targetPage) {
        const targetScrollTop = targetPage.offsetTop - 24;
        target.scrollTo({ top: targetScrollTop, behavior: 'smooth' });
      }

      const pageNum = pageIndex + 1;
      indicator.textContent = `Page ${pageNum} of ${totalPages}`;

      setTimeout(() => { syncing = false; }, 150);
    }

    let pdfTimer, textTimer;

    colPdf.addEventListener('scroll', () => {
      clearTimeout(pdfTimer);
      pdfTimer = setTimeout(() => syncScroll(colPdf, colText), 80);
    });

    colText.addEventListener('scroll', () => {
      clearTimeout(textTimer);
      textTimer = setTimeout(() => syncScroll(colText, colPdf), 80);
    });
  </script>
</body>
</html>
```

- [ ] **Step 2: Verify template loads in browser**

Open `template.html` in a browser. Should show the header with title and "Page 1 of 23", two empty columns. No console errors.

- [ ] **Step 3: Commit**

```bash
git add template.html
git commit -m "feat: add HTML template with layout and scroll sync"
```

---

### Task 3: Write the build script

**Files:**
- Create: `build.py`

This script:
1. Parses `F0200000_full_translation.md` to extract per-page Japanese and English content
2. Generates the PDF image HTML and text panel HTML for each page
3. Injects them into `template.html` at the placeholder comments
4. Writes `index.html`

The markdown has inconsistent formatting across page groups (produced by different agents). The parser must handle all variants:
- Pages 1-10: `## Japanese` / `## English Translation` headers
- Pages 11-15: `### Japanese Transcription` / `### English Translation` headers
- Pages 16-19: `## Japanese Transcription` / `## English Translation` headers
- Pages 20-23: Interleaved `**Japanese Transcription:**` / `**English Translation:**` per subsection

- [ ] **Step 1: Create `build.py`**

```python
#!/usr/bin/env python3
"""Build index.html from template.html and translation markdown."""

import re
import html as html_module
import markdown  # pip install markdown, or inline conversion below

# We'll do a simple markdown-to-HTML conversion without external deps.

def md_to_html(text):
    """Minimal markdown to HTML: paragraphs, bold, tables, headers, lists."""
    lines = text.strip().split('\n')
    out = []
    in_table = False
    in_list = False
    paragraph = []

    def flush_paragraph():
        if paragraph:
            content = ' '.join(paragraph)
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
            out.append(f'<p>{content}</p>')
            paragraph.clear()

    def flush_list():
        nonlocal in_list
        if in_list:
            out.append('</ul>')
            in_list = False

    for line in lines:
        stripped = line.strip()

        # Skip markdown horizontal rules
        if stripped == '---':
            flush_paragraph()
            flush_list()
            continue

        # Headers
        header_match = re.match(r'^(#{1,4})\s+(.+)', stripped)
        if header_match:
            flush_paragraph()
            flush_list()
            level = len(header_match.group(1))
            text = header_match.group(2)
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            out.append(f'<h{level}>{text}</h{level}>')
            continue

        # Table rows
        if stripped.startswith('|'):
            flush_paragraph()
            flush_list()
            if not in_table:
                in_table = True
                out.append('<table>')
            # Skip separator rows like |---|---|
            if re.match(r'^\|[\s\-:|]+\|$', stripped):
                continue
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            tag = 'th' if not any(c and not c.startswith('---') for prev in out[-5:] if '<tr>' in prev for c in []) else 'td'
            # Simple heuristic: first data row after table start is header
            existing_rows = sum(1 for x in out if '<tr>' in x and out.index(x) > len(out) - 30)
            row_html = '<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>'
            out.append(row_html)
            continue
        else:
            if in_table:
                out.append('</table>')
                in_table = False

        # List items
        if re.match(r'^[-*]\s+', stripped):
            flush_paragraph()
            if not in_list:
                in_list = True
                out.append('<ul>')
            item_text = re.sub(r'^[-*]\s+', '', stripped)
            item_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item_text)
            out.append(f'<li>{item_text}</li>')
            continue
        else:
            flush_list()

        # Blank line = flush paragraph
        if not stripped:
            flush_paragraph()
            continue

        # Bold-only lines (treat as pseudo-headers)
        if re.match(r'^\*\*.+\*\*$', stripped):
            flush_paragraph()
            text = stripped.strip('*')
            out.append(f'<p><strong>{text}</strong></p>')
            continue

        # Regular text
        paragraph.append(stripped)

    flush_paragraph()
    flush_list()
    if in_table:
        out.append('</table>')

    return '\n'.join(out)


def parse_pages_1_to_10(text):
    """Parse pages with ## Japanese / ## English Translation headers."""
    pages = {}
    page_blocks = re.split(r'^# Page (\d+) \(p\.(\d+)\)', text, flags=re.MULTILINE)
    # page_blocks: ['', '1', '67', content, '2', '68', content, ...]
    i = 1
    while i < len(page_blocks) - 2:
        page_num = int(page_blocks[i])
        doc_page = page_blocks[i + 1]
        content = page_blocks[i + 2]

        jp = ''
        en = ''

        # Split on ## Japanese and ## English Translation
        jp_match = re.split(r'^## (?:Japanese|Japanese Transcription)\s*$', content, flags=re.MULTILINE)
        if len(jp_match) > 1:
            after_jp = jp_match[1]
            en_split = re.split(r'^## English Translation\s*$', after_jp, flags=re.MULTILINE)
            jp = en_split[0].strip()
            if len(en_split) > 1:
                en = en_split[1].strip()

        pages[page_num] = {'jp': jp, 'en': en, 'doc_page': doc_page}
        i += 3

    return pages


def parse_pages_11_to_15(text):
    """Parse pages with ## Page X (p. Y) and ### Japanese Transcription / ### English Translation."""
    pages = {}
    page_blocks = re.split(r'^## Page (\d+) \(p\.\s*(\d+)\)', text, flags=re.MULTILINE)
    i = 1
    while i < len(page_blocks) - 2:
        page_num = int(page_blocks[i])
        doc_page = page_blocks[i + 1]
        content = page_blocks[i + 2]

        jp = ''
        en = ''

        jp_match = re.split(r'^### (?:Japanese Transcription|Japanese)\s*$', content, flags=re.MULTILINE)
        if len(jp_match) > 1:
            after_jp = jp_match[1]
            en_split = re.split(r'^### English Translation\s*$', after_jp, flags=re.MULTILINE)
            jp = en_split[0].strip()
            if len(en_split) > 1:
                en = en_split[1].strip()

        pages[page_num] = {'jp': jp, 'en': en, 'doc_page': doc_page}
        i += 3

    return pages


def parse_pages_16_to_19(text):
    """Parse pages with # Page X (p. Y) and ## Japanese Transcription / ## English Translation."""
    pages = {}
    page_blocks = re.split(r'^# Page (\d+) \(p\.\s*(\d+)\)', text, flags=re.MULTILINE)
    i = 1
    while i < len(page_blocks) - 2:
        page_num = int(page_blocks[i])
        doc_page = page_blocks[i + 1]
        content = page_blocks[i + 2]

        jp = ''
        en = ''

        jp_match = re.split(r'^## (?:Japanese Transcription|Japanese)\s*$', content, flags=re.MULTILINE)
        if len(jp_match) > 1:
            after_jp = jp_match[1]
            en_split = re.split(r'^## English Translation\s*$', after_jp, flags=re.MULTILINE)
            jp = en_split[0].strip()
            if len(en_split) > 1:
                en = en_split[1].strip()

        pages[page_num] = {'jp': jp, 'en': en, 'doc_page': doc_page}
        i += 3

    return pages


def parse_pages_20_to_23(text):
    """Parse pages with interleaved **Japanese Transcription:** / **English Translation:** blocks."""
    pages = {}
    page_blocks = re.split(r'^## Page (\d+) \(p\.\s*(\d+)\)', text, flags=re.MULTILINE)
    i = 1
    while i < len(page_blocks) - 2:
        page_num = int(page_blocks[i])
        doc_page = page_blocks[i + 1]
        content = page_blocks[i + 2]

        # Collect all Japanese and English chunks
        jp_chunks = []
        en_chunks = []

        # Split by the bold labels and collect
        parts = re.split(r'\*\*(?:Japanese Transcription|English Translation):\*\*', content)
        labels = re.findall(r'\*\*(Japanese Transcription|English Translation):\*\*', content)

        for idx, label in enumerate(labels):
            chunk = parts[idx + 1].strip() if idx + 1 < len(parts) else ''
            if 'Japanese' in label:
                jp_chunks.append(chunk)
            else:
                en_chunks.append(chunk)

        # Also grab any non-labeled content (section headers, chart descriptions)
        # that appears before the first label — add to both
        preamble = parts[0].strip() if parts else ''
        # Filter out horizontal rules and section header noise
        preamble_lines = [l for l in preamble.split('\n')
                         if l.strip() and l.strip() != '---'
                         and not l.strip().startswith('### Section Header')]

        preamble_text = '\n'.join(preamble_lines)

        jp = '\n\n'.join(jp_chunks)
        en = '\n\n'.join(en_chunks)

        if preamble_text:
            en = preamble_text + '\n\n' + en
            jp = preamble_text + '\n\n' + jp

        pages[page_num] = {'jp': jp, 'en': en, 'doc_page': doc_page}
        i += 3

    return pages


def main():
    with open('F0200000_full_translation.md', 'r', encoding='utf-8') as f:
        full_text = f.read()

    # Split the file into the chunks produced by different agents
    # Pages 1-10: start of file up to the "日本警察50年の軌跡と新たなる展開" title before page 11
    # Pages 11-15: from that title to "Pages 16-19"
    # Pages 16-19: from "Pages 16-19" header to "日本警察50年の軌跡と新たなる展開" before page 20
    # Pages 20-23: remainder

    # Find boundaries
    chunks = re.split(r'^# 日本警察50年の軌跡と新たなる展開\s*$', full_text, flags=re.MULTILINE)
    # chunks[0] = pages 1-10
    # chunks[1] = pages 11-15 content
    # chunks[2] might start with pages 16-19 header or be pages 20-23

    chunk_1_10 = chunks[0]

    # chunks[1] contains pages 11-15 then pages 16-19
    rest_1 = chunks[1] if len(chunks) > 1 else ''
    parts_16 = re.split(r'^# Pages 16-19.*$', rest_1, flags=re.MULTILINE)
    chunk_11_15 = parts_16[0]
    chunk_16_19 = parts_16[1] if len(parts_16) > 1 else ''

    # chunks[2] contains pages 20-23
    chunk_20_23 = chunks[2] if len(chunks) > 2 else ''

    all_pages = {}
    all_pages.update(parse_pages_1_to_10(chunk_1_10))
    all_pages.update(parse_pages_11_to_15(chunk_11_15))
    all_pages.update(parse_pages_16_to_19(chunk_16_19))
    all_pages.update(parse_pages_20_to_23(chunk_20_23))

    # Generate HTML for PDF column and text column
    pdf_html_parts = []
    text_html_parts = []

    for page_num in range(1, 24):
        page = all_pages.get(page_num)
        if not page:
            print(f"WARNING: Page {page_num} not found in parsed content")
            continue

        doc_page = page['doc_page']

        # PDF column
        pdf_html_parts.append(
            f'      <div class="pdf-page" data-page="{page_num}">\n'
            f'        <img src="images/page-{page_num:02d}.png" alt="Page {page_num} (p.{doc_page})" loading="lazy">\n'
            f'      </div>'
        )

        # Text column
        en_html = md_to_html(page['en'])
        jp_html = md_to_html(page['jp'])

        text_html_parts.append(
            f'      <div class="text-page" data-page="{page_num}">\n'
            f'        <div class="page-label">Page {page_num} (p.{doc_page})</div>\n'
            f'        <div class="english">\n{en_html}\n        </div>\n'
            f'        <div class="japanese">\n{jp_html}\n        </div>\n'
            f'      </div>'
        )

    pdf_html = '\n'.join(pdf_html_parts)
    text_html = '\n'.join(text_html_parts)

    # Read template and inject
    with open('template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    output = template.replace('<!-- PDF_PAGES -->', pdf_html)
    output = output.replace('<!-- TEXT_PAGES -->', text_html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"Generated index.html with {len(all_pages)} pages")


if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Run the build script**

```bash
python3 build.py
```

Expected output: `Generated index.html with 23 pages`

If any pages are missing, check the warning output and debug the parser for that page range.

- [ ] **Step 3: Verify the generated HTML**

```bash
grep -c 'data-page=' index.html
```

Expected: 46 (23 PDF page divs + 23 text page divs).

```bash
grep 'class="pdf-page"' index.html | wc -l
```

Expected: 23.

- [ ] **Step 4: Open in browser and spot-check**

Open `index.html` in a browser. Verify:
- All 23 page images load
- English text appears above Japanese text for each page
- Japanese text is visually smaller and more muted
- Scroll sync works (scrolling one column moves the other)
- Page indicator in header updates on scroll

- [ ] **Step 5: Commit**

```bash
git add build.py
git commit -m "feat: add build script to generate index.html from markdown"
```

---

### Task 4: Generate and commit final index.html

**Files:**
- Create: `index.html` (generated)

- [ ] **Step 1: Run build and verify**

```bash
python3 build.py
```

- [ ] **Step 2: Final browser check**

Open `index.html`. Scroll through all 23 pages. Check:
- No missing pages or empty text panels
- Tables render correctly
- Bold text and headings render correctly
- Scroll sync is smooth, not jittery

- [ ] **Step 3: Commit everything**

```bash
git add index.html
git commit -m "feat: generate index.html — PDF translation viewer"
```

---

### Task 5: Set up GitHub Pages deployment

**Files:**
- None to create — just repo configuration

- [ ] **Step 1: Initialize git repo if not already**

```bash
git init  # skip if already a repo
```

- [ ] **Step 2: Create .gitignore**

```
.DS_Store
*.swp
__pycache__/
```

- [ ] **Step 3: Ensure all files are committed**

```bash
git status
git add .gitignore
git commit -m "chore: add .gitignore"
```

- [ ] **Step 4: Create GitHub repo and push**

```bash
gh repo create npa-translation --public --source=. --push
```

Or if repo already exists:

```bash
git remote add origin <url>
git push -u origin main
```

- [ ] **Step 5: Enable GitHub Pages**

```bash
gh api repos/{owner}/npa-translation/pages -X POST -f source.branch=main -f source.path=/
```

Or via GitHub Settings > Pages > Source: main branch, root directory.

- [ ] **Step 6: Verify deployment**

Wait 1-2 minutes, then visit `https://<username>.github.io/npa-translation/`. Verify the app loads and all images display correctly.
