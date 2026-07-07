#!/usr/bin/env python3
"""Build the ACMC 2023 proceedings markdown source from the conference webpage.
Strips Jekyll front matter and Liquid, prepends pandoc metadata + front matter."""
import re, pathlib

root = pathlib.Path(__file__).resolve().parents[2]
src = (root / "_conferences/acmc2023.md").read_text()

# strip YAML front matter
src = re.sub(r"^---\n.*?\n---\n", "", src, count=1, flags=re.S)

lines = src.splitlines()
out = []
for ln in lines:
    if "Conference Proceedings:" in ln:      # drop self-reference
        continue
    if "{%" in ln or "%}" in ln:             # drop any liquid
        continue
    out.append(ln)
body = "\n".join(out)

# Replace the webpage's opening heading with a top-level "About" section, and
# start the content on a fresh page after the ToC.
body = body.replace(
    "## Australasian Computer Music Conference 2023 & ElectroMUSE Concert Series",
    "# About ACMC 2023")
body = "\\clearpage\n\n" + body

preface = r"""---
lang: en
toc: true
toc-depth: 2
numbersections: false
mainfont: "Charter"
sansfont: "Helvetica Neue"
monofont: "Menlo"
fontsize: 11pt
geometry: "a4paper, margin=2.5cm"
linkcolor: "RoyalBlue"
urlcolor: "RoyalBlue"
toccolor: "black"
header-includes:
  - \usepackage{tikz}
  - \usepackage{graphicx}
  - \definecolor{covertitle}{HTML}{141019}
  - \definecolor{covermuted}{HTML}{555159}
  - \definecolor{coverrule}{HTML}{141019}
  - \AtBeginDocument{\hypersetup{pdftitle={Proceedings of the Australasian Computer Music Conference 2023}, pdfauthor={Australasian Computer Music Association}, pdfsubject={ACMC 2023 ElectroMUSE}}}
  - \usepackage{newunicodechar}
  - \newfontfamily\fallbackfont{Arial Unicode MS}
  - \newunicodechar{破}{{\fallbackfont 破}}
  - \newunicodechar{境}{{\fallbackfont 境}}
  - \newunicodechar{逸}{{\fallbackfont 逸}}
  - \newunicodechar{宸}{{\fallbackfont 宸}}
  - \newunicodechar{ˈ}{{\fallbackfont ˈ}}
  - \newunicodechar{ʊ}{{\fallbackfont ʊ}}
  - \newunicodechar{ɔ}{{\fallbackfont ɔ}}
  - \newunicodechar{Ṉ}{{\fallbackfont Ṉ}}
  - \newunicodechar{ì}{{\fallbackfont ì}}
  - \newunicodechar{á}{{\fallbackfont á}}
---

"""

dest = root / "_drafts/proceedings-build/ACMC2023-proceedings.md"
dest.write_text(preface + body + "\n")
print("wrote", dest, len(body), "chars body")
