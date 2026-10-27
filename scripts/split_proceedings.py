#!/usr/bin/env python3
"""Cut one year's proceedings volume into one PDF per contribution.

Usage:

    python3 scripts/split_proceedings.py 2007            # write missing PDFs
    python3 scripts/split_proceedings.py 2007 --dry-run  # show the page ranges
    python3 scripts/split_proceedings.py 2007 --force    # rewrite existing PDFs

The entries are the single source of truth. Each entry whose `pdf` is
/proceedings/acmcYYYY/<file>.pdf and which has `pages` is cut from the
conference's `proceedings.source_pdf`: PDF page = printed page +
`proceedings.page_offset`. If the offset changes partway through a volume
(unnumbered inserts), set `pdf_pages: 12-18` on the entry to give its PDF
pages directly. Each output PDF gets the item's title and authors as metadata.

Check the first page of a few outputs: each must start on the item's first
page, with its title and authors at the top.
"""
import argparse
import os
import sys

from pypdf import PdfReader, PdfWriter

from contributions import load_conferences, load_contributions, parse_pages, site_path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("year", type=int)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    conf = load_conferences().get(args.year)
    if not conf:
        sys.exit(f"No conference has `year: {args.year}`.")
    proc = conf[1].get("proceedings") or {}
    if not proc.get("source_pdf"):
        sys.exit(f"The {args.year} conference has no `proceedings.source_pdf` to split.")
    reader = PdfReader(site_path(proc["source_pdf"]))
    offset = int(proc.get("page_offset") or 0)
    prefix = f"/proceedings/acmc{args.year}/"

    made = 0
    for path, fm, _ in load_contributions(args.year):
        pdf = fm.get("pdf") or ""
        if not pdf.startswith(prefix):
            continue
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
        writer = PdfWriter()
        for n in range(span[0] - 1, span[1]):
            writer.add_page(reader.pages[n])
        writer.add_metadata({
            "/Title": fm.get("title", ""),
            "/Author": "; ".join(fm.get("authors") or []),
            "/Subject": proc.get("title", ""),
        })
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "wb") as f:
            writer.write(f)
        made += 1
    print(f"{made} PDFs written")


if __name__ == "__main__":
    main()
