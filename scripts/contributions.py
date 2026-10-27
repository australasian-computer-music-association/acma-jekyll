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
    args = ["pdftotext", "-f", str(page), "-l", str(page)]
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


ABSTRACT_START = re.compile(r"^\s*abstract\s*[.:—-]?\s*$", re.I)
ABSTRACT_END = re.compile(
    r"^\s*((1|I)\.?\s*)?(introduction|background)\b|^\s*1\.?\s*$|^\s*(keywords|index terms)\b", re.I)


def extract_abstract(pdf, page=1):
    """Best-effort abstract from a two- or one-column first page. Check by eye."""
    for columns in (("left", "right"), (None,)):
        lines = []
        for col in columns:
            lines += page_text(pdf, page, col).splitlines()
        start = next((i for i, l in enumerate(lines) if ABSTRACT_START.match(l)), None)
        if start is None:
            continue
        out = []
        for line in lines[start + 1:]:
            if ABSTRACT_END.match(line):
                break
            out.append(line.rstrip())
        text = tidy_paragraphs("\n".join(out))
        if len(text) > 80:
            return text
    return ""


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


def dump_entry(path, fm, body):
    """Write an entry: YAML front matter in a fixed key order, then the body."""
    text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n" + text + "---\n")
        if body.strip():
            f.write(body.strip() + "\n")
