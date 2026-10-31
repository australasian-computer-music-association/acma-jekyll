#!/usr/bin/env python3
"""Cut one year's proceedings volume into one PDF per contribution.

Usage:

    python3 scripts/split_proceedings.py 2007            # write missing PDFs
    python3 scripts/split_proceedings.py 2007 --dry-run  # show the page ranges
    python3 scripts/split_proceedings.py 2007 --force    # rewrite existing PDFs
    python3 scripts/split_proceedings.py 2018 --fix-metadata  # only set titles/authors

The entries are the single source of truth. Each entry with `pages` whose
`pdf` (normally /proceedings/ACMCYYYY-proceedings/<slug>.pdf) doesn't exist
yet is cut from the conference's `proceedings.source_pdf`: PDF page = printed page +
`proceedings.page_offset`. If the offset changes partway through a volume
(unnumbered inserts), set `pdf_pages: 12-18` on the entry to give its PDF
pages directly. A year issued as more than one PDF (2014) keeps one volume in
`proceedings.source_pdf`; an entry in another volume names it in its own
`source_pdf`, with `pdf_pages` giving the pages in that file. Each output PDF
gets the item's title and authors as metadata.

--fix-metadata doesn't split anything: it rewrites the title, author and
subject inside every existing per-item PDF of the year (e.g. PDFs supplied
already split, whose metadata often says "Microsoft Word - draft3.docx" or
names the editor as author).

Check the first page of a few outputs: each must start on the item's first
page, with its title and authors at the top.
"""
import argparse
import os
import sys

from pypdf import PdfReader

from contributions import (load_conferences, load_contributions, parse_pages, site_path,
                           write_pdf, year_dir_url)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("year", type=int)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--fix-metadata", action="store_true", help="only rewrite existing PDFs' metadata")
    args = ap.parse_args()

    conf = load_conferences().get(args.year)
    if not conf:
        sys.exit(f"No conference has `year: {args.year}`.")
    proc = conf[1].get("proceedings") or {}
    if args.fix_metadata:
        fixed = 0
        for path, fm, _ in load_contributions(args.year):
            if fm.get("pdf") and os.path.isfile(site_path(fm["pdf"])):
                print(os.path.basename(fm["pdf"]))
                if not args.dry_run:
                    tmp = site_path(fm["pdf"]) + ".tmp"
                    write_pdf(site_path(fm["pdf"]), tmp, fm, proc)
                    os.replace(tmp, site_path(fm["pdf"]))
                fixed += 1
        print(f"{fixed} PDFs' metadata set")
        return
    if not proc.get("source_pdf"):
        sys.exit(f"The {args.year} conference has no `proceedings.source_pdf` to split.")
    readers = {proc["source_pdf"]: PdfReader(site_path(proc["source_pdf"]))}
    offset = int(proc.get("page_offset") or 0)

    made = 0
    for path, fm, _ in load_contributions(args.year):
        pdf = fm.get("pdf") or ""
        if os.path.dirname(pdf) != year_dir_url(args.year):
            continue
        source = fm.get("source_pdf") or proc["source_pdf"]
        if source not in readers:
            readers[source] = PdfReader(site_path(source))
        reader = readers[source]
        span = parse_pages(fm.get("pdf_pages"))
        if not span:
            printed = parse_pages(fm.get("pages"))
            if not printed:
                print(f"{os.path.basename(path)}: has a pdf but no pages; skipped")
                continue
            span = (printed[0] + offset, printed[1] + offset)
        if span[0] < 1 or span[1] > len(reader.pages):
            print(f"{os.path.basename(path)}: PDF pages {span[0]}-{span[1]} are outside the volume "
                  f"({len(reader.pages)} pages)")
            continue
        out = site_path(pdf)
        label = f"{os.path.basename(out)}: PDF pages {span[0]}-{span[1]}"
        if os.path.exists(out) and not args.force:
            print(f"{label} (exists, kept)")
            continue
        print(label)
        if args.dry_run:
            continue
        write_pdf(reader, out, fm, proc, span)
        made += 1
    print(f"{made} PDFs written")


if __name__ == "__main__":
    main()
