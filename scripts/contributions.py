"""Shared helpers for the proceedings scripts (_contributions collection).

Used by check_contributions.py, import_contributions.py and
split_proceedings.py. Needs PyYAML (pip install pyyaml); the PDF scripts also
need pypdf and poppler's pdftotext.
"""
import os
import re
import subprocess
import unicodedata

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTRIBUTIONS = os.path.join(ROOT, "_contributions")
CONFERENCES = os.path.join(ROOT, "_conferences")

STOPWORDS = {"a", "an", "the", "of", "and", "for", "in", "on", "with", "to",
             "from", "by", "at", "as", "or", "into", "towards", "toward"}


def read_front_matter(path):
    """Return (front matter dict, body) of a Markdown file with YAML front matter."""
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        return None, text
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def load_data(name):
    with open(os.path.join(ROOT, "_data", name + ".yml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_conferences():
    """Conferences with a `year:` key, as {year: (path, front matter)}."""
    confs = {}
    for name in sorted(os.listdir(CONFERENCES)):
        if name.endswith(".md"):
            path = os.path.join(CONFERENCES, name)
            fm, _ = read_front_matter(path)
            if fm and fm.get("year"):
                confs[fm["year"]] = (path, fm)
    return confs


def load_contributions(year=None):
    """All entries (or one year's) as a list of (path, front matter, body)."""
    entries = []
    if not os.path.isdir(CONTRIBUTIONS):
        return entries
    for folder in sorted(os.listdir(CONTRIBUTIONS)):
        if year is not None and folder != year_folder(year):
            continue
        d = os.path.join(CONTRIBUTIONS, folder)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if name.endswith(".md"):
                path = os.path.join(d, name)
                fm, body = read_front_matter(path)
                entries.append((path, fm or {}, body))
    return entries


def ascii_fold(text):
    text = unicodedata.normalize("NFKD", text)
    return text.encode("ascii", "ignore").decode("ascii")


def make_slug(authors, title, words=3):
    """First author's surname plus the first few significant title words."""
    surname = ascii_fold(authors[0].split()[-1]).lower() if authors else "anon"
    surname = re.sub(r"[^a-z0-9]", "", surname)
    title_words = re.findall(r"[a-z0-9]+", ascii_fold(title).lower())
    picked = [w for w in title_words if w not in STOPWORDS][:words] or title_words[:words]
    return "-".join([surname] + picked)


def parse_pages(pages):
    """'7-13' -> (7, 13); 115 -> (115, 115); None -> None."""
    if pages in (None, ""):
        return None
    parts = [p.strip() for p in str(pages).replace("–", "-").split("-")]
    return int(parts[0]), int(parts[-1])


def year_folder(year):
    """A year's folder, both in _contributions/ (the entries) and in
    proceedings/ (their PDFs). Entry x.md is published as
    /proceedings/ACMCYYYY-proceedings/x.html, next to its PDF, because Google
    Scholar wants citation_pdf_url in the same directory as the page."""
    return f"ACMC{year}-proceedings"


def year_dir_url(year):
    return f"/proceedings/{year_folder(year)}"


def item_pdf_url(year, slug):
    """The default name for an item's own PDF (new splits and imports)."""
    return f"{year_dir_url(year)}/{slug}.pdf"


def write_pdf(reader_or_path, out, fm, proc, pages=None):
    """Write a PDF (all pages, or a range of a volume) with the item's own title
    and authors in its metadata, so Scholar doesn't credit e.g. the editor."""
    from pypdf import PdfReader, PdfWriter
    reader = reader_or_path if not isinstance(reader_or_path, str) else PdfReader(reader_or_path)
    writer = PdfWriter()
    for n in (range(pages[0] - 1, pages[1]) if pages else range(len(reader.pages))):
        writer.add_page(reader.pages[n])
    writer.add_metadata({
        "/Title": fm.get("title", ""),
        "/Author": "; ".join(fm.get("authors") or []),
        "/Subject": proc.get("title", ""),
    })
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as f:
        writer.write(f)


def site_path(url):
    """A site URL path like /proceedings/x.pdf -> the file in the repo."""
    return os.path.join(ROOT, url.lstrip("/"))


def page_text(pdf, page, column=None):
    """Text of one PDF page (1-based). column: None, 'left' or 'right'."""
    args = ["pdftotext", "-enc", "UTF-8", "-f", str(page), "-l", str(page)]
    if column:
        info = subprocess.run(["pdfinfo", "-f", str(page), "-l", str(page), pdf],
                              capture_output=True, text=True).stdout
        m = re.search(r"Page\s+\d+\s+size:\s+([\d.]+) x ([\d.]+)", info) or \
            re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", info)
        w, h = float(m.group(1)), float(m.group(2))
        x = 0 if column == "left" else w / 2
        args += ["-x", str(int(x)), "-y", "0", "-W", str(int(w / 2) + 1), "-H", str(int(h) + 1)]
    args += [pdf, "-"]
    return subprocess.run(args, capture_output=True, text=True).stdout


ABSTRACT_HEADING = r"abstract"
ABSTRACT_END = re.compile(
    r"^\s*((1|I)\.?\s*)?(introduction|background)\b|^\s*1\.?\s*$|^\s*(keywords|index terms)\b", re.I)
PAGE_NUMBER = re.compile(r"^\s*\d{1,4}\s*$")
CAPTION = re.compile(r"^\s*(figure|fig\.|table)\s*\d+", re.I)


def running_lines(pdf, page):
    """Running headers and footers: lines printed on both this page and the
    next (or previous) one, as keys from running_key(). pdftotext puts them in
    the middle of the text. The page number is ignored when comparing, so
    "ACMC2000 Page 1" matches "ACMC2000 Page 2"."""
    here = set(running_key(l) for l in page_text(pdf, page).splitlines() if l.strip())
    other = page_text(pdf, page + 1) or (page_text(pdf, page - 1) if page > 1 else "")
    return here & set(running_key(l) for l in other.splitlines() if l.strip())


def running_key(line):
    """Letters only, no digits: what's left of a running header once its page
    number is ignored."""
    return re.sub(r"[^a-z]", "", ascii_fold(line).lower())


def header_fragment(line, running=()):
    """Is this line a running header, or a piece of one left by column cropping
    ("ACMC200", "00 Page 18", "Pag", "ge 107")? `running` holds the keys of
    the page's running lines (see running_lines)."""
    key = running_key(line)
    if not key or len(line.strip()) > 40:
        return False
    if key in "acmcpage" and len(line.strip()) <= 16:
        return True
    return len(key) >= 12 and any(key in r for r in running)


# The same glued to the end of a text line by pdftotext ("colPage 107").
GLUED_HEADER = re.compile(r"(?<=[a-z])(?:ACMC\s?\d{0,4}\s*)?Page\s?\d{1,4}\s*$")


def _letters(text):
    return re.sub(r"[^a-z0-9]", "", ascii_fold(text).lower())


def extract_abstract(pdf, page=1, heading=ABSTRACT_HEADING, title=None):
    """Best-effort abstract from a two- or one-column first page. Check by eye.

    The text runs from a line that is just the heading (a regex; "abstract" by
    default, but e.g. "artist talk|poster|studio report" for items that print
    their text under the section's name) to the introduction, keywords, the
    page number or the item's `title` (printed after the text on some one-page
    items). Running headers and figure captions are dropped.

    The page is first cropped into two columns, then read whole as a fallback.
    scripts/test_extract_abstracts.py scores the strategies against the
    reviewed abstracts of 2000, 2007 and 2008: cropping matched on 51 of 67,
    reading order on 41, and reading order was better on only 5 (it often
    runs on past the abstract when a page has no "Introduction" heading)."""
    for columns in COLUMN_STRATEGIES:
        text = extract_abstract_from(pdf, page, heading, title, columns)
        if len(text) > 80:
            return text
    return ""


# Each strategy is the sequence of page_text() columns whose lines are joined.
COLUMN_STRATEGIES = ((None,), ("left", "right"))


def extract_abstract_from(pdf, page, heading, title, columns):
    """One strategy of extract_abstract(): "" if the heading isn't found."""
    start_re = re.compile(rf"^\s*({heading})\s*[.:—-]?\s*$", re.I)
    # Column cropping cuts running headers short, so drop parts of them too.
    running = running_lines(pdf, page)
    is_running = lambda l: header_fragment(l, running)
    title_key = _letters(title or "")
    is_title = lambda l: title_key and len(_letters(l)) >= 8 and title_key.startswith(_letters(l))
    lines = []
    for col in columns:
        lines += page_text(pdf, page, col).splitlines()
    # An "Abstract" heading wins over a section name printed above it.
    found = [i for i, l in enumerate(lines) if start_re.match(l)]
    start = next((i for i in found if re.match(r"\s*abstract", lines[i], re.I)), found[0] if found else None)
    if start is None:
        return ""
    out, caption = [], False
    for line in lines[start + 1:]:
        if ABSTRACT_END.match(line) or PAGE_NUMBER.match(line) or is_title(line):
            break
        if is_running(line):
            continue
        line = GLUED_HEADER.sub("", line)
        # A caption runs to the next blank line.
        caption = bool(CAPTION.match(line)) or (caption and line.strip() != "")
        if not caption:
            out.append(line.rstrip())
    return tidy_paragraphs(mark_paragraphs("\n".join(out)))


def mark_paragraphs(text):
    """pdftotext runs a column's paragraphs together. A line that ends a
    sentence well short of the column width ends its paragraph."""
    lines = text.splitlines()
    widths = sorted(len(l.strip()) for l in lines if l.strip())
    if len(widths) < 4:
        return text
    full = widths[len(widths) * 3 // 4]
    out = []
    for line in lines:
        out.append(line)
        if line.strip() and SENTENCE_END.search(line.strip()) and len(line.strip()) < 0.75 * full:
            out.append("")
    return "\n".join(out)


# A paragraph that stops without closing punctuation and is followed by one
# starting in lower case is one sentence broken by a page or column break.
SENTENCE_END = re.compile(r"[.!?:;)\]\"'’”…]$")


def broken_sentence(para, next_para):
    return not SENTENCE_END.search(para.rstrip()) and next_para[:1].islower()


def tidy_paragraphs(text):
    """Join wrapped lines into paragraphs; mend words split across lines and
    sentences split across pages."""
    paras = []
    for block in re.split(r"\n\s*\n", text):
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if not lines:
            continue
        if paras and broken_sentence(paras[-1], lines[0]):
            lines.insert(0, paras.pop())
        joined = lines[0]
        for line in lines[1:]:
            if joined.endswith("-") and line[:1].islower():
                joined = joined[:-1] + line
            else:
                joined += " " + line
        paras.append(joined)
    return "\n\n".join(paras)


class _EntryDumper(yaml.SafeDumper):
    """Writes multi-paragraph strings (e.g. `bio`) as readable literal blocks."""


_EntryDumper.add_representer(str, lambda dumper, s: dumper.represent_scalar(
    "tag:yaml.org,2002:str", s, style="|" if "\n" in s else None))


def dump_entry(path, fm, body):
    """Write an entry: YAML front matter in a fixed key order, then the body."""
    text = yaml.dump(fm, Dumper=_EntryDumper, sort_keys=False, allow_unicode=True, width=1000)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n" + text + "---\n")
        if body.strip():
            f.write(body.strip() + "\n")
