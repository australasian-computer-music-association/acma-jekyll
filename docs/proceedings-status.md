# Proceedings status and plan

What we hold for each year's ACMC proceedings, and what's left to do.
Please keep it up to date. Last audited: October 2026.

## Goal

Every ACMC year should list its contributions one by one, each with its own
PDF, instead of linking one big PDF. Google Scholar indexes papers, not
volumes. It also wants **one landing page per paper** with `citation_title`,
`citation_author`, `citation_publication_date`, `citation_conference_title`
and `citation_pdf_url` meta tags. Nothing on the site sets these yet. The
likely shape is a `_papers` collection (one front-matter file per paper), a
layout that writes the meta tags, and conference pages that list their papers
from the collection.

Since about 2020, peer-reviewed long papers are no longer published in the
conference proceedings. They go to the Chroma journal on its own OJS site
(<https://journal.computermusic.org.au/chroma>), which already gives each
article Scholar meta tags. For 2020 onwards the proceedings are abstracts
and program notes; the conference page should list each contribution with
its abstract and link the Chroma article where there is one (as ACMC 2023
does). ACMC 2019 already accepted reviewed abstracts only.

## Status by year

| Year | What we hold | Contributions listed on the page? | Status |
|---|---|---|---|
| 1993–1999 | Nothing; see "Before 2000" below | 1994 and 1999 paper lists from Chroma | **Missing** |
| 2000 | One PDF, 105 pp | Yes, plain titles | One big PDF |
| 2001 | One PDF per item, converted from the original Word files | Yes, linked | ✅ Per item (Bandt & Paine, Doornbusch were never in the zip) |
| 2002 | One PDF, 201 pp | Yes, plain titles | One big PDF |
| 2003 | 2 PDFs (Weinberg keynote, Fraietta) | Yes, about 30 titles, 2 linked | **Mostly missing** |
| 2004 | One PDF, 105 pp | Yes, plain titles | One big PDF |
| 2005 | 47 PDFs | Yes, linked | ✅ Per item |
| 2006 | 55 PDFs | Yes, linked | ✅ Per item |
| 2007 | One PDF, 134 pp | Yes, plain titles | One big PDF |
| 2008 | One PDF, 119 pp | Yes, plain titles | One big PDF |
| 2009 | One PDF, 138 pp | Yes, plain titles (list looks short) | One big PDF |
| 2010 | One PDF, 98 pp | Yes, plain titles (list looks short) | One big PDF |
| 2011 | Nothing; page says "COMING SOON" | Yes, plain titles | **Missing** |
| 2012 | Nothing | No | **Missing** |
| 2013 | Held with ICMC 2013 | No | Check the ICMC archive (already per paper) |
| 2014 | Papers PDF (110 pp), talks/posters PDF (68 pp), 7 concert programmes | No | One big PDF ×2 |
| 2015 | One PDF, 160 pp | No | One big PDF |
| 2016 | Nothing (held with NIME 2016) | No | **Missing** |
| 2017 | One PDF, 79 pp | No | One big PDF |
| 2018 | 15 paper PDFs, plus front matter, abstracts and creative works PDFs | Papers linked | ✅ Papers per item; abstracts still combined |
| 2019 | One PDF, 86 pp (reduced), programme booklet | No (page is still the call) | One big PDF; abstracts only |
| 2020 | Link to the conference's GitHub Pages site | No | **Unclear** |
| 2021 | One PDF, 30 pp | No | One big PDF; abstracts only |
| 2022 | No PDF; full papers in Chroma 39(1) | Concerts only | **Partial**: no abstracts |
| 2023 | One PDF, 46 pp (built in `_drafts/proceedings-build/`) | Yes, with abstracts | Abstracts on the page; 6 full papers link to Chroma 39(2) |
| 2024 | One PDF, 90 pp | No | One big PDF; abstracts only |

## Before 2000

The 1990s conferences had their own names. Chroma (newsletters 1–37 in
`chroma_pdf/`) has their calls and some programmes, but not the papers.
Chroma 1–23 are image-only scans; OCR them with PyMuPDF and tesseract to
search them.

| Year | Name | In Chroma | Proceedings |
|---|---|---|---|
| 1993 | CompMusic '93, Sydney | 13, 14 (review names presenters) | Meant for the ACMA journal *Mikropolyphonie*; not known to have appeared |
| 1994 | Synaesthetica '94, Canberra | 15–17 (full programme in 17) | Printed; no copy found |
| 1995 | ACMA Conference '95, Melbourne | 19, 20 | Unknown |
| 1996 | Brisbane (Andrew Brown) | Only a mention in 26–27 | Unknown |
| 1997 | Interface '97, Auckland | 22 | Unknown |
| 1998 | ACMA 98, Canberra | 23 | Unknown |
| 1999 | Imaginary Space, Wellington | 24, 25 (full schedule), 26–27 (reports) | Printed (17 papers, 2 studio reports); no copy found |

Leads: printed volumes from long-time members (Hirst, Riddell, Burt,
Schiemer, Young) or libraries (Trove/NLA, VUW, ANU); a possible online
*Mikropolyphonie* in the Internet Archive. ACMA papers before 1993 appeared
at the Australian New Music Conference (1990, 1992), and Chroma 9 reprints
some of the 1992 ones.

## Plan

1. Build the `_papers` collection and a layout with Scholar meta tags.
2. Move the years already split per item (2001, 2005, 2006, 2018) into it.
3. Split the single PDFs that already have title lists: 2000, 2002, 2004,
   2007–2010. Check each list against the PDF's table of contents first.
4. Write title lists from the PDFs for 2014, 2015 and 2017, then split them.
5. For 2019–2024, list each contribution with its abstract and link Chroma
   articles where they exist.
6. Keep hunting for 1993–1999, 2003, 2011, 2012 and 2016 (see
   `missing-content.md`).
