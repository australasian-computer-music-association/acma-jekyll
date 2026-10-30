#!/usr/bin/env python3
"""Score extract_abstract() against abstracts that have already been reviewed.

Usage:

    python3 scripts/test_extract_abstracts.py            # 2000, 2007 and 2008
    python3 scripts/test_extract_abstracts.py 2008 2010  # these years

For every entry with its own `pdf` and a body, each column strategy in
contributions.COLUMN_STRATEGIES is run on the PDF's first page and compared
with the committed text (difflib ratio, 1.00 = identical). Entries whose body
is the paper's introduction (no printed abstract) are skipped. Run this before
changing the extractor and again after: the mean and the per-entry list show
what got better and what got worse. It needs pdftotext and takes a minute.
"""
import os
import re
import sys
from difflib import SequenceMatcher
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contributions as c  # noqa: E402

HEADING = "abstract|artist talk|poster|studio report|workshop"
norm = lambda t: re.sub(r"\s+", " ", re.sub(r"\{[%{].*?[%}]\}", "", c.ascii_fold(t))).strip().lower()
rows = []
YEARS = [int(a) for a in sys.argv[1:]] or [2000, 2007, 2008]
for year in YEARS:
    for path, fm, body in c.load_contributions(year):
        if not fm.get("pdf") or not body.strip() or not os.path.isfile(c.site_path(fm["pdf"])):
            continue
        # A body taken from the introduction (no printed abstract) can't match.
        front = open(path, encoding="utf-8").read().split("\n---")[0]
        if "introduction" in front.lower():
            continue
        pdf = c.site_path(fm["pdf"]); page = 1
        scores = []
        for cols in c.COLUMN_STRATEGIES:
            t = c.extract_abstract_from(pdf, page, HEADING, fm["title"], cols)
            scores.append(SequenceMatcher(None, norm(t), norm(body)).ratio() if len(t) > 80 else None)
        rows.append((year, os.path.basename(path), scores))
def fmt(x): return "  --" if x is None else f"{x:.2f}"
import statistics
for i, cols in enumerate(c.COLUMN_STRATEGIES):
    vals = [r[2][i] for r in rows if r[2][i] is not None]
    print(f"strategy {cols}: found {len(vals)}/{len(rows)}, mean {statistics.mean(vals):.3f}, "
          f">=0.9: {sum(v>=0.9 for v in vals)}, <0.7: {sum(v<0.7 for v in vals)}")
better_plain = sum(1 for r in rows if (r[2][0] or 0) > (r[2][1] or 0) + 0.02)
better_cols = sum(1 for r in rows if (r[2][1] or 0) > (r[2][0] or 0) + 0.02)
print(f"plain better: {better_plain}, columns better: {better_cols}, tie: {len(rows)-better_plain-better_cols}")
print("\nentries where plain < 0.9 or columns beats plain:")
for y, n, s in rows:
    if (s[0] or 0) < 0.9 or (s[1] or 0) > (s[0] or 0) + 0.02:
        print(f"  {y} {n:50s} plain {fmt(s[0])}  cols {fmt(s[1])}")
