#!/usr/bin/env python3
"""Check every proceedings entry in _contributions/ before the site is built.

Usage:

    python3 scripts/check_contributions.py               # check the source files
    python3 scripts/check_contributions.py --site _site  # also check the built pages

Errors (exit status 1) are things that would publish wrong or broken pages:
missing fields, unknown types, a missing PDF, a review status that doesn't
resolve. Warnings are worth a look but don't fail the build.

The allowed `type` and `reviewing` values are in _data/contribution_types.yml
and _data/reviewing.yml. See docs/adding-proceedings.md for the fields.
"""
import argparse
import os
import re
import sys
from collections import defaultdict

from contributions import (ROOT, broken_sentence, load_conferences, load_contributions, load_data,
                           parse_pages, site_path, year_dir_url, year_folder)

REQUIRED = ["title", "authors", "year", "type", "section", "order"]
WORK_KINDS = {"composition", "performance", "installation", "audiovisual",
              "improvisation", "sound-art", "other"}
MEDIA_KINDS = {"audio", "video", "score", "documentation", "review", "website"}
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KNOWN_KEYS = set(REQUIRED) | {"pages", "pdf", "section_pdf", "reviewing", "chroma", "doi",
                              "keywords", "work", "media", "research_statement", "bio", "pdf_pages"}
RUNNING_HEADER = re.compile(r"Proceedings of the Australasian Computer Music Conference|^ACMC\s?\d{2,4}\b", re.I | re.M)
CAPTION = re.compile(r"^(Figure|Fig\.|Table)\s*\d+", re.I)
PLACEHOLDER = re.compile(r"^((format )?not (recorded|known|stated)|unknown|n/?a|tbc|tba|-+|\?+)$", re.I)
AFFILIATION = re.compile(r"\b(University|Universität|Université|Universidad|Conservatorium|"
                         r"Conservatory|Institute|College|Polytechnic)\b")


def body_problems(body):
    """Signs that an extracted abstract or program note picked up PDF layout:
    the end of the header block above it, or a sentence split at a page break."""
    text = re.sub(r"\{[%{].*?[%}]\}", "", body).strip()
    if not text:
        return []
    problems = []
    opening = " ".join(text.split()[:12])
    if text[:1].islower():
        problems.append(f"starts in lower case (“{opening} …”): header text left over from the PDF?")
    elif AFFILIATION.search(opening):
        problems.append(f"names an institution in its first words (“{opening} …”): "
                        "the author's affiliation left over from the PDF?")
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    for p in paras:
        if RUNNING_HEADER.search(p):
            problems.append(f"contains the volume's running header (“{' '.join(p.split()[:8])} …”)")
        elif re.fullmatch(r"\d{1,4}", p):
            problems.append(f"has a paragraph that is just “{p}”: a page number left over from the PDF?")
        elif CAPTION.match(p):
            problems.append(f"has a figure or table caption (“{' '.join(p.split()[:6])} …”)")
    for a, b in zip(paras, paras[1:]):
        if broken_sentence(a, b):
            problems.append(f"sentence split across paragraphs at “…{' '.join(a.split()[-3:])} / "
                            f"{' '.join(b.split()[:3])}…”: a page break in the PDF?")
    return problems


def check(site_dir=None):
    errors, warnings = [], []
    types = load_data("contribution_types")
    reviewing = load_data("reviewing")
    confs = load_conferences()
    own_pdf_pages = defaultdict(list)
    titles = defaultdict(list)

    for path, fm, body in load_contributions():
        rel = os.path.relpath(path, ROOT)
        err = lambda msg: errors.append(f"{rel}: {msg}")
        warn = lambda msg: warnings.append(f"{rel}: {msg}")

        for key in REQUIRED:
            if fm.get(key) in (None, "", []):
                err(f"missing `{key}`")
        for key in fm:
            if key not in KNOWN_KEYS:
                warn(f"unknown field `{key}` (typo?)")
        year = fm.get("year")
        folder = os.path.basename(os.path.dirname(path))
        slug = os.path.splitext(os.path.basename(path))[0]
        if folder != year_folder(year):
            err(f"is in {folder}/ but has year {year}")
        if not SLUG.match(slug):
            err(f"file name `{slug}` must be lower-case letters, digits and single hyphens")
        if not isinstance(fm.get("authors"), list):
            err("`authors` must be a list")
        if fm.get("type") and fm["type"] not in types:
            err(f"unknown type `{fm['type']}` (see _data/contribution_types.yml)")

        conf = confs.get(year, (None, {}))[1]
        proc = conf.get("proceedings") or {}
        if not conf:
            err(f"no conference in _conferences/ has `year: {year}`")
        elif not proc.get("title"):
            err(f"the {year} conference has no `proceedings.title`")
        elif not (proc.get("published") or conf.get("start_date")):
            err(f"the {year} conference needs `start_date` (or `proceedings.published`) to date its entries")

        # reviewing: a key on the entry wins ("" = explicitly unknown); a blank
        # `reviewing:` (None) falls back to the conference default for the section.
        value = fm.get("reviewing")
        if value is None:
            defaults = proc.get("reviewing") or {}
            if fm.get("section") not in defaults:
                err(f"section `{fm.get('section')}` has no default in the {year} conference's "
                    "`proceedings.reviewing`; add one there or set `reviewing` here (\"\" if unknown)")
            value = defaults.get(fm.get("section"))
        if value not in (None, "") and value not in reviewing:
            err(f"unknown reviewing value `{value}` (see _data/reviewing.yml)")

        try:
            pages = parse_pages(fm.get("pages"))
        except ValueError:
            pages = None
            err(f"can't read pages `{fm.get('pages')}`; use e.g. 7-13")
        if pages and pages[0] > pages[1]:
            err(f"pages {fm['pages']} run backwards")

        for key in ("pdf", "section_pdf"):
            url = fm.get(key)
            if url:
                if not str(url).startswith("/"):
                    err(f"`{key}` should be a site path starting with /")
                elif not os.path.isfile(site_path(url)):
                    err(f"`{key}` file not found: {url}")
        # Scholar wants citation_pdf_url in the same directory as the page.
        if fm.get("pdf") and os.path.dirname(str(fm["pdf"])) != year_dir_url(year):
            err(f"`pdf` must be in {year_dir_url(year)}/, the same folder as the entry's page")
        if fm.get("pdf") and pages:
            own_pdf_pages[year].append((pages, rel))

        if fm.get("type") == "creative-work":
            work = fm.get("work") or {}
            # Works known only from a programme often have no recorded format:
            # leave it out rather than writing a placeholder.
            if not work.get("format"):
                warn("no `work.format` (instrumentation or medium); fine if no source records it")
            elif PLACEHOLDER.match(str(work["format"]).strip()):
                err(f"`work.format` is a placeholder (“{work['format']}”); leave it out instead")
            if work.get("kind") and work["kind"] not in WORK_KINDS:
                err(f"unknown work.kind `{work['kind']}`; one of {', '.join(sorted(WORK_KINDS))}")
        elif fm.get("work"):
            warn("`work` details are only shown for type creative-work")
        for m in fm.get("media") or []:
            url = str(m.get("url", ""))
            if url.startswith("/"):
                if not os.path.isfile(site_path(url)):
                    err(f"media file not found: {url}")
            elif not url.startswith(("http://", "https://")):
                err(f"media url must be a site path starting with / or a full http(s) link: {url}")
            if m.get("kind") not in MEDIA_KINDS:
                warn(f"media kind `{m.get('kind')}` is not one of {', '.join(sorted(MEDIA_KINDS))}")
        if fm.get("chroma") and not str(fm["chroma"]).startswith("https://"):
            err("`chroma` should be the article's full https link")
        if fm.get("keywords") is not None and not isinstance(fm["keywords"], list):
            err("`keywords` must be a list")
        for problem in body_problems(body):
            warn(problem)
        if not body.strip():
            warn("no abstract or program note: the page gets no Scholar tags "
                 "(Scholar excludes bare bibliographic data)")

        titles[(year, str(fm.get("title", "")).lower())].append(rel)

    for year, items in own_pdf_pages.items():
        items.sort()
        for (a, rel_a), (b, rel_b) in zip(items, items[1:]):
            if b[0] <= a[1]:
                warnings.append(f"{rel_b}: pages {b[0]}-{b[1]} overlap {rel_a} ({a[0]}-{a[1]})")
    for (year, title), rels in titles.items():
        if len(rels) > 1:
            warnings.append(f"same title in {year}: {', '.join(rels)}")

    if site_dir:
        check_site(site_dir, errors)
    return errors, warnings


def check_site(site_dir, errors):
    """Each built entry page has its Scholar tags (or none, if its paper is in Chroma)."""
    for path, fm, body in load_contributions():
        slug = os.path.splitext(os.path.basename(path))[0]
        page = os.path.join(site_dir, "proceedings", year_folder(fm.get("year")), slug + ".html")
        rel = os.path.relpath(page, site_dir)
        if not os.path.isfile(page):
            errors.append(f"{rel}: not built")
            continue
        html = open(page, encoding="utf-8").read()
        tagged = 'name="citation_title"' in html
        if fm.get("chroma") and tagged:
            errors.append(f"{rel}: has citation tags but its paper is in Chroma")
        if not body.strip() and tagged:
            errors.append(f"{rel}: has citation tags but no abstract or program note")
        if not fm.get("chroma") and body.strip():
            for tag in ("citation_title", "citation_author", "citation_publication_date",
                        "citation_conference_title"):
                if f'name="{tag}"' not in html:
                    errors.append(f"{rel}: missing {tag}")
            if fm.get("pdf") and 'name="citation_pdf_url"' not in html:
                errors.append(f"{rel}: missing citation_pdf_url")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--site", help="also check the built site in this folder (e.g. _site)")
    args = ap.parse_args()
    errors, warnings = check(args.site)
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    n = len(load_contributions())
    print(f"{n} entries checked: {len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
