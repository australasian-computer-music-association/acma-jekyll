# Proceedings status and plan

What we hold for each year's ACMC proceedings, and what's left to do.
Please keep it up to date. Last audited: October 2026 (web and library search, 27 October 2026).

## Goal

Every ACMC year should list its contributions one by one (papers, abstracts
and creative works), each with its own page and, where printed, its own PDF,
instead of linking one big PDF. Google Scholar indexes papers, not volumes.
This is now built: see `docs/scholar-plan.md` (issue #9) for the design and
`docs/adding-proceedings.md` for how to add a year. A year is done when its
entries are in `_contributions/ACMCYYYY-proceedings/`. 2018 was the first.

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
| 1993–1999 | A few papers (Mikropolyphonie, author copies); see "Before 2000" below | 1994 and 1999 paper lists from Chroma | **Mostly missing**; printed volumes in libraries |
| 2000 | One PDF, 105 pp | Yes, plain titles | One big PDF |
| 2001 | One PDF per item, converted from the original Word files | Yes, linked | ✅ Per item. Bandt & Paine survives as HTML on the archived Sound Design Project site; Doornbusch still missing |
| 2002 | One PDF, 201 pp; also the original per-paper print-run files (`_drafts/found/ACMC2002-per-paper/`) | Yes, plain titles | Per-paper originals found; not yet linked |
| 2003 | 2 PDFs (Weinberg keynote, Fraietta); 5 more found (`_drafts/found/acmc2001-2003/`) | Yes, about 30 titles, 2 linked | **Mostly missing**; NLA holds the printed volume |
| 2004 | One PDF, 105 pp | Yes, plain titles | One big PDF |
| 2005 | 47 PDFs (44 items + front matter), concert programme, workshops | ✅ Entries: 2 keynotes, 1 invited speaker, 24 papers, 4 artist talks, 6 studio reports, 4 posters, 5 workshops, 36 creative works (32 concert works, 4 installations) | ✅ Done. Review status per paper from the contents page: 15 full paper, 9 abstract |
| 2006 | 55 PDFs (52 items; 3 duplicates) | ✅ Entries: 2 keynotes, 1 invited speaker, 29 papers, 5 posters, 4 studio reports, 7 artist talks, 4 workshops | ✅ Done. No front matter survives, so review status is unknown except for keynotes |
| 2007 | One PDF, 134 pp | Yes, plain titles | One big PDF |
| 2008 | One PDF, 119 pp | Yes, plain titles | One big PDF |
| 2009 | One PDF, 138 pp | Yes, plain titles (list looks short) | One big PDF |
| 2010 | One PDF, 98 pp | Yes, plain titles (list looks short) | One big PDF |
| 2011 | One PDF, 143 pp (`proceedings/ACMC2011-proceedings.pdf`) | Yes, plain titles | One big PDF |
| 2012 | 4 papers found (`_drafts/found/acmc2011-2012/`) | No | **Missing**: paperback on Lulu; ask the editors for the PDF |
| 2013 | Held with ICMC 2013 | No | ICMC 2013 is in the ICMC archive, 82 papers: <https://quod.lib.umich.edu/i/icmc/bbp2372.2013>. No separate ACMC track |
| 2014 | Papers PDF (110 pp), talks/posters PDF (68 pp), 7 concert programmes | No | One big PDF ×2 |
| 2015 | One PDF, 160 pp | No | One big PDF |
| 2016 | One PDF, 121 pp, recovered from the Wayback Machine (`proceedings/ACMC2016-proceedings.pdf`) | No | One big PDF |
| 2017 | One PDF, 79 pp | No | One big PDF |
| 2018 | 15 paper PDFs, plus front matter, abstracts and creative works PDFs | ✅ Entries: 15 papers, 4 abstracts, 24 creative works | ✅ Done (pilot year) |
| 2019 | One PDF, 86 pp (reduced), programme booklet | No (page is still the call) | One big PDF; abstracts only |
| 2020 | Link to the conference's GitHub Pages site; its repo has all 74 abstracts in `sitedata/papers.csv` (copy in `_drafts/found/acmc2020-data/`) | No | Abstracts only; list them from the CSV |
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
| 1993 | CompMusic '93, Sydney | 13, 14 (review names presenters) | Published as print *Mikropolyphonie* 1(1) (La Trobe/ACMA). No library copy found. Online *MikroPolyphonie* vol. 1 (1996) reprints 4 papers: Henderson-Sellers & White, Hirst, Pressing, Monro |
| 1994 | Synaesthetica '94, Canberra | 15–17 (full programme in 17) | *Synaesthetica '94: proceedings*, ACAT 1994. **ANU Art & Music Library, 789.99 SYM** (the only copy found). The catalogue says it was held at the Lakeside Hotel, not at ACAT |
| 1995 | ACMA Conference '95, Melbourne | 19, 20 | *Proceedings of the ACMA 1995 Conference*, 167 pp. **ANU Art & Music 789.99 AUS**; Monash 786.74 A938P; Sydney Q 786.76 12 (offers "Request to Borrow or Digitise") |
| 1996 | Brisbane, QUT (Andrew Brown) | Only a mention in 26–27 | *Engaging with Art and Industry* (or "artistry"), QUT 1996. No library copy found. Brown's paper (pp. 27–35) is on QUT ePrints 13016 |
| 1997 | Interface '97, Auckland | 22 | Spiral-bound papers sold by the Auckland School of Music. No library copy found. The full paper list with abstracts is archived: <https://web.archive.org/web/19971009192050/http://www.mus.auckland.ac.nz:80/acma97/program.html> |
| 1998 | ACMA 98, Canberra | 23 | Nothing found: no paper list, volume or library record |
| 1999 | Imaginary Space, Wellington | 24, 25 (full schedule), 26–27 (reports) | *Imaginary space: proceedings of the 1999 ACMC*, VUW, 98 pp., ISBN 0475110641, OCLC 42215674. **VUW ML1380 A938 1999**; Auckland 789.9 A93; Waikato ML1380.A98 1999. *MikroPolyphonie* vol. 5 ("ACMC 99") reprints 9 papers |

*Mikropolyphonie* did appear. It was an online journal from La Trobe (ISSN 1327-256X, edited
by David Hirst, 1996–2003), and the NLA's PANDORA archive holds it in full:
<http://nla.gov.au/nla.arc-10054>. Volume 1 has CompMusic '93 papers, volume 5 has ACMC 1999
papers and volume 6 has ACMC 2000 papers.

ACMA papers before 1993 appeared at the Australian New Music Conference (1990, 1992), and
Chroma 9 reprints some of the 1992 ones.

## Leads from the October 2026 search

The files found are in `_drafts/found/`, one folder per period. Nothing there is linked
from the site yet.

**Quick to get (a browser login or an order):**

- **2012:** *Interactive*, edited by Matt Hitchcock and Jodie Taylor, 180 pp., is a paperback
  on Lulu (no ebook):
  <https://www.lulu.com/shop/matt-hitchcock/acmc-2012-conference-proceedings/paperback/product-20230652.html>.
  Ask the editors for the PDF they uploaded. Charles Martin's 2012 poster PDF was cut from
  the full volume ("ACMC 2012 Proceedings.pdf", July 2012), so an old copy may still be in
  mail or Dropbox.
- **2003:** NLA holds *Converging Technologies*, edited by Lindsay Vickery (Bib ID 3257664,
  Nq 786.76 AUS), and its record offers "Order a scan". McIlwain & Doornbusch is on
  Academia.edu (academia.edu/168451) and Stuart James is on ResearchGate (297732157);
  both need a login.
- **ECU Research Online** blocks scripts but works in a browser. It has 2011 papers by
  Herrington & Vickery, Hope, James & Hope, Vickery and Riddoch, and 2012 papers by Hope,
  James & Vickery and by Vickery (`ro.ecu.edu.au/ecuworks2011`, `ecuworks2012`).
- **1994, 1995, 1999:** ask the ANU Art & Music Library to scan 1994 and 1995, and VUW to
  scan 1999.

**Ask people:**

- 1993 print *Mikropolyphonie* 1(1): David Hirst, Gordon Monro.
- 1996: Andrew Brown. 1997: Ian Whalley, John Elmsly, Greg Schiemer, or the Auckland School
  of Music. 1998: David Worrall, Tim Kreger, Stuart Ramsden.
- 2001 Doornbusch, "The music of CSIRAC": Paul Doornbusch. Only the later CMJ article and
  book versions are online.
- 2003: Hirst, Hope, Wooller, Alsop, Clemen, Mustard, HEDKIKR, Burtt & Lavers have no
  copies online.

**Not worth repeating:**

- The Wayback Machine has every PDF, zip and .doc file from `acma.asn.au` and
  `computermusic.org.au`. Apart from the 2002 zip, all of them are already in the repo.
  The archived `Proceedings01.zip` is identical to `proceedings/ACMC2001-proceedings.zip`.
- `acmc2012.net` was only ever a redirect to a Griffith submission-system (OCS) install,
  of which only the home page was archived. The "archived copy" link on the 2012 page shows
  a parked domain.
- The 2009 OCS on `conference.acma.asn.au` has abstract pages (titles, authors) for 48
  papers, which are useful for checking the 2009 list, but no paper PDFs. 2010 and 2011
  have nothing.
- The *Contemporary Music Review* 36(1–2) (2017) percussion issue came out of the 2016
  Australian Percussion Gathering, not ACMC 2016.
- ACMC 2015: 19 of its 27 per-item PDFs are archived on `acmc2015.net`. That only saves
  splitting the volume.

## Plan

The year-by-year plan and its order are in `docs/scholar-plan.md` (issue #9).
Each year is done in its own PR, following the `proceedings-year` skill.
Separately, follow up the leads above for 1993–1999, 2001, 2003 and 2012.
