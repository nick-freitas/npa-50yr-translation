#!/usr/bin/env python3
"""
Build script for the PDF translation viewer.

Reads F0200000_full_translation.md, parses per-page Japanese and English content,
converts to HTML, and injects into template.html to produce index.html.
"""

import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(SCRIPT_DIR, "F0200000_full_translation.md")
TEMPLATE_FILE = os.path.join(SCRIPT_DIR, "template.html")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "index.html")
TOTAL_PAGES = 23
PAGE_OFFSET = 66  # Page 1 = p.67, so document_page = page_num + 66


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------------------
# Markdown-to-HTML converter (basic, no external deps)
# ---------------------------------------------------------------------------

def md_to_html(text):
    """Convert basic markdown to HTML: paragraphs, bold, headers, lists, tables, italic."""
    if not text or not text.strip():
        return ""

    lines = text.strip().split("\n")
    html_parts = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Blank line — skip
        if not line.strip():
            i += 1
            continue

        # Horizontal rule
        if re.match(r"^---+\s*$", line.strip()):
            i += 1
            continue

        # Headers
        hm = re.match(r"^(#{1,6})\s+(.+)$", line)
        if hm:
            level = len(hm.group(1))
            content = inline_format(hm.group(2))
            html_parts.append(f"<h{level}>{content}</h{level}>")
            i += 1
            continue

        # Table — detect lines starting with |
        if line.strip().startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            html_parts.append(parse_table(table_lines))
            continue

        # Unordered list (- or * or bullet)
        if re.match(r"^\s*[-*]\s+", line) or re.match(r"^\s*・", line):
            list_lines = []
            while i < len(lines) and (
                re.match(r"^\s*[-*]\s+", lines[i])
                or re.match(r"^\s*・", lines[i])
            ):
                text_content = re.sub(r"^\s*[-*・]\s*", "", lines[i])
                list_lines.append(text_content)
                i += 1
            items = "".join(f"<li>{inline_format(li)}</li>" for li in list_lines)
            html_parts.append(f"<ul>{items}</ul>")
            continue

        # Ordered list
        if re.match(r"^\s*\d+[.)]\s+", line):
            list_lines = []
            while i < len(lines) and re.match(r"^\s*\d+[.)]\s+", lines[i]):
                text_content = re.sub(r"^\s*\d+[.)]\s+", "", lines[i])
                list_lines.append(text_content)
                i += 1
            items = "".join(f"<li>{inline_format(li)}</li>" for li in list_lines)
            html_parts.append(f"<ol>{items}</ol>")
            continue

        # Paragraph: collect consecutive non-blank, non-special lines
        para_lines = []
        while i < len(lines):
            ln = lines[i]
            if not ln.strip():
                break
            if re.match(r"^#{1,6}\s+", ln):
                break
            if ln.strip().startswith("|"):
                break
            if re.match(r"^---+\s*$", ln.strip()):
                break
            if re.match(r"^\s*[-*]\s+", ln) and not para_lines:
                break
            if re.match(r"^\s*・", ln) and not para_lines:
                break
            if re.match(r"^\s*\d+[.)]\s+", ln) and not para_lines:
                break
            para_lines.append(ln)
            i += 1

        if para_lines:
            text_content = " ".join(para_lines)
            html_parts.append(f"<p>{inline_format(text_content)}</p>")

    return "\n".join(html_parts)


def inline_format(text):
    """Handle bold, italic, and inline code."""
    # Bold: **text** or __text__
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
    # Italic: *text* or _text_ (but not inside ** or __)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    # Inline code
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def parse_table(lines):
    """Parse markdown table lines into an HTML table."""
    if not lines:
        return ""

    rows = []
    for line in lines:
        # Skip separator lines like |---|---|
        if re.match(r"^\|[\s\-:]+\|$", line):
            continue
        cells = [c.strip() for c in line.split("|")]
        # Remove empty first/last from leading/trailing |
        if cells and cells[0] == "":
            cells = cells[1:]
        if cells and cells[-1] == "":
            cells = cells[:-1]
        if cells:
            rows.append(cells)

    if not rows:
        return ""

    html = "<table>"
    for idx, row in enumerate(rows):
        html += "<tr>"
        tag = "th" if idx == 0 else "td"
        for cell in row:
            html += f"<{tag}>{inline_format(cell)}</{tag}>"
        html += "</tr>"
    html += "</table>"
    return html


# ---------------------------------------------------------------------------
# Markdown parser — extract per-page Japanese and English content
# ---------------------------------------------------------------------------

def parse_markdown(md_text):
    """
    Parse the translation markdown and return a dict:
      { page_num: { 'japanese': str, 'english': str } }
    for pages 1-23.
    """
    pages = {}

    # Split into lines for processing
    lines = md_text.split("\n")

    # We'll identify page boundaries and extract content per page
    # Strategy: find all page header lines, then extract between them

    page_starts = []  # list of (line_index, page_num)

    for i, line in enumerate(lines):
        # Match patterns like:
        #   # Page 1 (p.67)
        #   ## Page 11 (p. 77)
        #   # Page 16 (p. 82)
        m = re.match(r"^#{1,3}\s+Page\s+(\d+)\s+\(p\.?\s*(\d+)\)", line)
        if m:
            page_num = int(m.group(1))
            page_starts.append((i, page_num))

    # Extract content blocks between page boundaries
    for idx, (start_line, page_num) in enumerate(page_starts):
        if idx + 1 < len(page_starts):
            end_line = page_starts[idx + 1][0]
        else:
            end_line = len(lines)

        page_lines = lines[start_line:end_line]
        page_text = "\n".join(page_lines)

        japanese, english = extract_japanese_english(page_text, page_num)
        pages[page_num] = {"japanese": japanese, "english": english}

    return pages


def extract_japanese_english(page_text, page_num):
    """
    Given the text block for a single page, extract Japanese and English sections.
    Handles the four different formatting variants.
    """
    lines = page_text.split("\n")

    # Strategy: find section markers and split content accordingly

    japanese_parts = []
    english_parts = []

    # --- Format for pages 20-23: interleaved **Japanese Transcription:** / **English Translation:** ---
    # Also handles variant with (Chart): **Japanese Transcription (Chart):** etc.
    if re.search(r"\*\*Japanese Transcription(?:\s*\(Chart\))?:\*\*", page_text) or \
       re.search(r"\*\*English Translation(?:\s*\(Chart\))?:\*\*", page_text):
        return extract_interleaved(page_text, page_num)

    # --- Format for pages 1-10: ## Japanese / ## English Translation ---
    # --- Format for pages 11-15: ### Japanese Transcription / ### English Translation ---
    # --- Format for pages 16-19: ## Japanese Transcription / ## English Translation ---

    # Find section headers
    jp_start = None
    en_start = None
    jp_ends = []
    en_ends = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        # Japanese section headers
        if re.match(r"^#{2,3}\s+Japanese(\s+Transcription)?$", stripped):
            jp_start = i + 1
        # English section headers
        elif re.match(r"^#{2,3}\s+English\s+Translation$", stripped):
            en_start = i + 1
            # The Japanese section ends here if it was started
            if jp_start is not None and not jp_ends:
                jp_ends.append(i)

    # Determine boundaries
    if jp_start is not None:
        jp_end = jp_ends[0] if jp_ends else (en_start - 1 if en_start else len(lines))
        jp_text = "\n".join(lines[jp_start:jp_end]).strip()
        # Remove trailing --- separators
        jp_text = re.sub(r"\n---+\s*$", "", jp_text).strip()
    else:
        jp_text = ""

    if en_start is not None:
        en_text = "\n".join(lines[en_start:]).strip()
        # Remove trailing --- separators
        en_text = re.sub(r"\n---+\s*$", "", en_text).strip()
    else:
        en_text = ""

    return jp_text, en_text


def extract_interleaved(page_text, page_num):
    """
    For pages 20-23: content is interleaved with **Japanese Transcription:** and
    **English Translation:** markers within subsections.
    """
    lines = page_text.split("\n")

    japanese_parts = []
    english_parts = []

    current_lang = None
    current_buffer = []
    # Track headers seen so we can put them in both sections
    pending_headers = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Skip the page header line itself
        if re.match(r"^#{1,3}\s+Page\s+\d+", stripped):
            continue

        # Skip "### Section Header" lines
        if stripped == "### Section Header":
            continue

        # Check for language markers (including "(Chart)" variant)
        if re.match(r"^\*\*Japanese Transcription(?:\s*\(Chart\))?:\*\*$", stripped):
            # Flush any pending buffer
            if current_lang == "english" and current_buffer:
                english_parts.extend(current_buffer)
                current_buffer = []
            elif current_lang == "japanese" and current_buffer:
                japanese_parts.extend(current_buffer)
                current_buffer = []

            # Add pending headers to japanese
            if pending_headers:
                japanese_parts.extend(pending_headers)
                pending_headers = []

            current_lang = "japanese"
            continue

        if re.match(r"^\*\*English Translation(?:\s*\(Chart\))?:\*\*$", stripped):
            # Flush japanese buffer
            if current_lang == "japanese" and current_buffer:
                japanese_parts.extend(current_buffer)
                current_buffer = []
            elif current_lang == "english" and current_buffer:
                english_parts.extend(current_buffer)
                current_buffer = []

            # Add pending headers to english
            if pending_headers:
                english_parts.extend(pending_headers)
                pending_headers = []

            current_lang = "english"
            continue

        # Horizontal rules act as subsection separators
        if re.match(r"^---+\s*$", stripped):
            if current_lang == "japanese" and current_buffer:
                japanese_parts.extend(current_buffer)
                current_buffer = []
            elif current_lang == "english" and current_buffer:
                english_parts.extend(current_buffer)
                current_buffer = []
            current_lang = None
            continue

        # Headers that appear between sections (subsection titles)
        # These should go in both Japanese and English, or be assigned to the next lang block
        if current_lang is None and re.match(r"^#{1,6}\s+", stripped):
            pending_headers.append(line)
            continue

        # Regular content
        if current_lang:
            current_buffer.append(line)
        elif stripped:
            # Content before any language marker — could be a section header line
            # for pages 20-23 these are things like the section header text
            # Add to both
            pending_headers.append(line)

    # Flush final buffer
    if current_lang == "japanese" and current_buffer:
        japanese_parts.extend(current_buffer)
    elif current_lang == "english" and current_buffer:
        english_parts.extend(current_buffer)

    jp_text = "\n".join(japanese_parts).strip()
    en_text = "\n".join(english_parts).strip()

    # Clean up trailing separators
    jp_text = re.sub(r"\n---+\s*$", "", jp_text).strip()
    en_text = re.sub(r"\n---+\s*$", "", en_text).strip()

    return jp_text, en_text


# ---------------------------------------------------------------------------
# HTML generation
# ---------------------------------------------------------------------------

def generate_pdf_html(pages_dict):
    """Generate HTML for the PDF image column."""
    parts = []
    for page_num in range(1, TOTAL_PAGES + 1):
        doc_page = page_num + PAGE_OFFSET
        img_name = f"page-{page_num:02d}.jpg"
        parts.append(
            f'      <div class="pdf-page" data-page="{page_num}">\n'
            f'        <img src="images/{img_name}" alt="Page {page_num} (p.{doc_page})" loading="lazy">\n'
            f'      </div>'
        )
    return "\n".join(parts)


def generate_text_html(pages_dict):
    """Generate HTML for the text column."""
    parts = []
    for page_num in range(1, TOTAL_PAGES + 1):
        doc_page = page_num + PAGE_OFFSET
        data = pages_dict.get(page_num, {"japanese": "", "english": ""})

        english_html = md_to_html(data["english"])
        japanese_html = md_to_html(data["japanese"])

        parts.append(
            f'      <div class="text-page" data-page="{page_num}">\n'
            f'        <div class="page-label">Page {page_num} (p.{doc_page})</div>\n'
            f'        <div class="english">{english_html}</div>\n'
            f'        <div class="japanese">{japanese_html}</div>\n'
            f'      </div>'
        )
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Read inputs
    md_text = read_file(MD_FILE)
    template = read_file(TEMPLATE_FILE)

    # Parse markdown
    pages = parse_markdown(md_text)

    # Verify we got all 23 pages
    missing = [p for p in range(1, TOTAL_PAGES + 1) if p not in pages]
    if missing:
        print(f"WARNING: Missing pages: {missing}")

    for pn in sorted(pages.keys()):
        jp_len = len(pages[pn]["japanese"])
        en_len = len(pages[pn]["english"])
        if jp_len == 0:
            print(f"WARNING: Page {pn} has no Japanese content")
        if en_len == 0:
            print(f"WARNING: Page {pn} has no English content")

    # Generate HTML fragments
    pdf_html = generate_pdf_html(pages)
    text_html = generate_text_html(pages)

    # Inject into template
    output = template.replace("<!-- PDF_PAGES -->", pdf_html)
    output = output.replace("<!-- TEXT_PAGES -->", text_html)

    # Write output
    write_file(OUTPUT_FILE, output)

    # Verify
    pdf_count = output.count('class="pdf-page"')
    text_count = output.count('class="text-page"')
    print(f"Generated index.html with {pdf_count} pages")
    if pdf_count != TOTAL_PAGES:
        print(f"ERROR: Expected {TOTAL_PAGES} pdf-page divs, got {pdf_count}")
    if text_count != TOTAL_PAGES:
        print(f"ERROR: Expected {TOTAL_PAGES} text-page divs, got {text_count}")


if __name__ == "__main__":
    main()
