#!/usr/bin/env python3
"""Create _contributions entries for one year from a CSV file.

Usage:

    python3 scripts/import_contributions.py 2026 programme.csv
    python3 scripts/import_contributions.py 2007 toc.csv --extract-abstracts
    python3 scripts/import_contributions.py 2026 programme.csv --dry-run

One row per contribution, in programme or volume order (that order becomes
`order`). Columns, all optional except title, authors, type and section:

    title, authors          authors separated by ";"
    type                    see _data/contribution_types.yml
    section                 heading as printed, e.g. "Refereed Papers"
    pages                   printed page range, e.g. 7-13
    pdf                     this item's own PDF, e.g. /proceedings/acmc2007/x.pdf
    section_pdf             a PDF holding this item with others
    abstract                the abstract, or a creative work's program note
    keywords                separated by ";"
    reviewing               only to override the conference default; "unknown" = ""
    chroma                  link to the full paper in Chroma
    kind, format, duration, created, performers (";"), event, venue, date,
    research_statement      creative works only
    media                   "kind|url|label" items separated by ";"
    slug                    to override the generated file name

Existing entries are left alone unless --force is given. With
--extract-abstracts, an empty abstract is drafted from the item's PDF (its own
`pdf`, or the conference's `proceedings.source_pdf` at `pages` plus
`page_offset`). Drafted text must be checked by eye.

See docs/adding-proceedings.md for the whole process.
"""
import argparse
import csv
import os
import sys

from contributions import (CONTRIBUTIONS, dump_entry, extract_abstract, load_conferences,
                           make_slug, parse_pages, site_path)


def split_list(value):
    return [v.strip() for v in (value or "").split(";") if v.strip()]


def row_to_entry(row, year, order):
    g = lambda k: (row.get(k) or "").strip()
    fm = {
        "title": g("title"),
        "authors": split_list(g("authors")),
        "year": year,
        "type": g("type"),
        "section": g("section"),
        "order": order,
    }
    if g("pages"):
        fm["pages"] = g("pages")
    for key in ("pdf", "section_pdf", "chroma"):
        if g(key):
            fm[key] = g(key)
    if g("reviewing"):
        fm["reviewing"] = "" if g("reviewing").lower() == "unknown" else g("reviewing")
    if g("keywords"):
        fm["keywords"] = split_list(g("keywords"))
    if fm["type"] == "creative-work":
        work = {}
        for key in ("kind", "format", "duration", "created"):
            if g(key):
                work[key] = int(g(key)) if key == "created" and g(key).isdigit() else g(key)
        if g("performers"):
            work["performers"] = split_list(g("performers"))
        presented = {k: g(k) for k in ("event", "venue", "date") if g(k)}
        if presented:
            work["presented"] = presented
        if work:
            fm["work"] = work
    if g("media"):
        media = []
        for item in split_list(g("media")):
            kind, url, *label = [p.strip() for p in item.split("|")]
            media.append({"kind": kind, "url": url, **({"label": label[0]} if label else {})})
        fm["media"] = media
    if g("research_statement"):
        fm["research_statement"] = g("research_statement")
    return fm, g("abstract").replace("\\n", "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("year", type=int)
    ap.add_argument("csv")
    ap.add_argument("--extract-abstracts", action="store_true", help="draft empty abstracts from the PDFs")
    ap.add_argument("--force", action="store_true", help="overwrite existing entries")
    ap.add_argument("--dry-run", action="store_true", help="show what would be written")
    args = ap.parse_args()

    conf = load_conferences().get(args.year)
    if not conf:
        sys.exit(f"No conference has `year: {args.year}`. Add it to the _conferences file first.")
    proc = conf[1].get("proceedings") or {}

    with open(args.csv, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    folder = os.path.join(CONTRIBUTIONS, f"acmc{args.year}")
    used = set()
    written = skipped = 0
    for i, row in enumerate(rows, start=1):
        fm, body = row_to_entry(row, args.year, i)
        if not fm["title"] or not fm["authors"]:
            print(f"row {i}: no title or authors, skipped")
            continue
        slug = (row.get("slug") or "").strip() or make_slug(fm["authors"], fm["title"])
        base, n = slug, 2
        while slug in used:
            slug, n = f"{base}-{n}", n + 1
        used.add(slug)
        path = os.path.join(folder, slug + ".md")

        if args.extract_abstracts and not body:
            pdf, page = None, 1
            if fm.get("pdf") and os.path.isfile(site_path(fm["pdf"])):
                pdf = site_path(fm["pdf"])
            elif proc.get("source_pdf") and parse_pages(fm.get("pages")):
                pdf = site_path(proc["source_pdf"])
                page = parse_pages(fm["pages"])[0] + int(proc.get("page_offset") or 0)
            if pdf:
                body = extract_abstract(pdf, page)
                if not body:
                    print(f"row {i}: no abstract found in {os.path.basename(pdf)} p.{page}")

        if os.path.exists(path) and not args.force:
            skipped += 1
            continue
        if args.dry_run:
            print(f"would write {os.path.relpath(path)} ({len(body)} chars of abstract)")
        else:
            dump_entry(path, fm, body)
        written += 1
    print(f"{written} written, {skipped} already existed (use --force to overwrite)")


if __name__ == "__main__":
    main()
