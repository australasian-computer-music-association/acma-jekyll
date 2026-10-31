# Adding a year's proceedings

Every paper, abstract and creative work at ACMC gets its own page on the site,
with a citation and the tags Google Scholar reads. This guide is for conference
chairs and the committee. The design behind it is in `docs/scholar-plan.md`
(issue #9).

Each contribution is one Markdown file in `_contributions/ACMCYYYY-proceedings/`. You
don't usually write these by hand. Fill in a spreadsheet, export it as CSV, and
a script writes the files.

## Quick version

1. Add the year's details to its conference page (`_conferences/acmcYYYY.md`);
   see [The conference page](#the-conference-page).
2. Fill in the CSV template (`docs/contributions-template.csv`), one row per
   paper, abstract or creative work, in programme order.
3. In the CSV's `pdf` column, give the path to each item's PDF on your
   computer. The import copies it into the item's own folder.
4. Run:

   ```sh
   pip install pyyaml pypdf
   python3 scripts/import_contributions.py YYYY your-file.csv
   python3 scripts/check_contributions.py
   ```

5. On the conference page, put `{% include contribution-list.html %}` where
   the list should appear, and `{% include proceedings-review.html %}` for the
   review statement and committees.
6. Preview with `bundle exec jekyll serve`, then open a pull request. CI checks
   every entry again.

## What to collect at submission time

Ask for these in the call and the submission form, so nothing needs chasing
later.

**Everyone:** title, all authors' names as they want them cited (keep the
spelling the same as in earlier years), and a 150–300 word abstract.

**Creative works:**
- a program note;
- the format: instrumentation or medium, e.g. "8-channel fixed media" or
  "clarinet and live electronics";
- the duration and the year the work was made;
- performers, if they aren't the creators;
- a link to documentation (video, audio or score) the artist is happy to have
  public;
- optionally, a short **research statement** under three headings:
  background, contribution and significance. This is what university research
  offices ask for when reporting a creative work as research.

**Review process:** say in the call how each kind of submission is reviewed
(e.g. "full papers are double-blind peer reviewed; creative works are selected
by a jury"). State the same in the proceedings, so it can be recorded.

## The conference page

Add `year`, the dates, and a `proceedings:` block to the front matter:

```yaml
year: 2026
start_date: 2026-12-01
end_date: 2026-12-04
proceedings:
  title: "Proceedings of the Australasian Computer Music Conference 2026"
  editors: ["Editor Name"]
  publisher: "Australasian Computer Music Association"
  issn: "2206-5296"           # or isbn:
  published: 2026-11-28       # optional; the conference start date is used otherwise
  full_volume: /proceedings/ACMC2026-proceedings.pdf   # optional complete volume
  copyright: "Copyright remains with the authors."     # optional; the volume's own statement, or a licence
  reviewing:                  # how each section was reviewed (see below)
    "Refereed Papers": full-paper
    "Abstracts": abstract
    "Creative Works": refereed
  review_statement: >-        # optional: how review worked, as stated in the volume
    Full papers were double-blind peer reviewed by at least two reviewers.
  committees:                 # optional: juries and committees, as listed in the volume
    - name: Paper Committee
      members: [Name One, Name Two]
    - name: Music Jury
      members: [Name Three, Name Four]
```

`reviewing` values are in `_data/reviewing.yml`:

| Value | Shown as | Use when the volume or call says |
|---|---|---|
| `full-paper` | Peer reviewed (full paper) | full papers were refereed or peer reviewed |
| `abstract` | Peer reviewed (abstract) | items were selected by peer review of an abstract |
| `refereed` | Refereed | refereed or juried, basis not stated (often creative works) |
| `invited` | Invited | keynotes and invited speakers |
| `non-refereed` | Not refereed | the volume says non-refereed |
| `""` | (nothing shown) | unknown |

Only record what was actually stated. Leaving a status unknown is fine.
When the volume's own marks and the call for papers disagree, the volume
wins: ACMC 2000's call promised full-paper review, but the contents page
marks ten of the thirteen full papers "†" (peer review by abstract), so they
are `abstract`. A `review_statement` may start with the volume's own "*"
mark; the template stops Markdown turning it into a list bullet, so quote it
as printed.

Each entry's page shows only a short marker, such as "Peer reviewed (full
paper)". Put `{% include proceedings-review.html %}` on the conference page
to show the review statement and committees there, once for the whole
volume, as a journal lists its editorial board. The markers link to it.

## The CSV

Columns (only `title`, `authors`, `type` and `section` are required):

| Column | What goes in it |
|---|---|
| `title` | as printed, in title case |
| `authors` | separated by `;`, e.g. `Cat Hope;Stuart James` |
| `type` | `paper`, `abstract`, `keynote`, `artist-talk`, `studio-report`, `poster`, `workshop` or `creative-work` |
| `section` | the heading it appears under, e.g. `Refereed Papers` |
| `pages` | printed page range, e.g. `7-13` |
| `pdf` | this item's own PDF: a file on your computer (copied in), or `split` to cut it from the volume |
| `section_pdf` | a PDF that holds this item with others (e.g. all program notes) |
| `abstract` | the abstract, or a creative work's program note |
| `keywords` | separated by `;` |
| `reviewing` | only to override the section default; `unknown` for "" |
| `chroma` | link to the full paper in Chroma, if published there |
| `kind` | creative works: `composition`, `performance`, `installation`, `audiovisual`, `improvisation`, `sound-art` or `other` |
| `format` | creative works: instrumentation or medium. Ask every artist for it; for old years, leave it empty if no source records it (never a placeholder like "not recorded") |
| `duration`, `created` | creative works: e.g. `8:30`, `2026` |
| `performers` | creative works, separated by `;` |
| `event`, `venue`, `date` | creative works: where ACMC presented it, e.g. `Concert 2`, `Riverside Theatres`, `2026-12-02` |
| `media` | documentation links: `kind\|url\|label` items separated by `;`, e.g. `video\|https://vimeo.com/123\|Performance video`. Kinds: `audio`, `video`, `score`, `documentation`, `review`, `website`. A file in this repo is linked by its site path, e.g. `/proceedings/ACMC2007-proceedings/ACMC07_Schedule.pdf` |
| `research_statement` | creative works: the research statement |
| `bio` | the authors' or artists' biographies, where the volume prints them |
| `slug` | only to override the generated file name |

The row order becomes the order on the conference page.

## The fields in an entry

The import script writes these, but you can edit an entry by hand. Example:

```yaml
---
title: Their Lives are Stripped of Meaning
authors:
- Cat Hope
- Stuart James
year: 2018
type: creative-work
section: Refereed Creative Works
order: 27
pages: 120-121
section_pdf: /proceedings/ACMC2018-proceedings/17acmc2018proceedingsrefCreativeWorks.pdf
keywords:
- Animated Notation
work:
  kind: composition
  format: trumpet, voice and electronics
  created: 2018
media:
- kind: video
  url: https://example.org/video
  label: Performance video
---
The program note (or, for papers, the abstract) goes here, in Markdown.
```

Rules worth knowing:

- **File names are permanent.** The file name becomes the page's URL
  (`/proceedings/ACMC2018-proceedings/hope-their-lives-are.html`), so don't
  rename a published entry.
- **`reviewing`**: a blank `reviewing:` (or no key) uses the conference default
  for the section; `reviewing: ""` means "explicitly unknown".
- **`chroma`**: if the full paper is in Chroma, set this. The page then links
  there and carries no Scholar tags, so citations collect on the journal
  version.
- **PDFs**: an item's own `pdf` must hold only that item and start on its
  first page. It lives in the year's folder, `/proceedings/ACMCYYYY-proceedings/`,
  next to the item's page, because Google Scholar only accepts a PDF in the
  same directory as its page. The checker enforces this. PDFs that were
  already there keep their names (e.g. `01Connell.pdf`); new ones are named
  `<slug>.pdf`. Items that share pages with others use `section_pdf` instead,
  and their page is enough for Scholar. Whole volumes and multi-item PDFs are
  kept out of the sitemap automatically.
- **PDF metadata**: for PDFs supplied already split, run
  `python3 scripts/split_proceedings.py YYYY --fix-metadata`, so each PDF's
  built-in title and author are the item's own, not "Microsoft Word -
  draft.docx" or the editor's name.
- **Abstracts matter**: Google Scholar excludes pages that show "bare
  bibliographic data without abstracts". An entry with no abstract or
  program note still gets its page, but no Scholar tags. Chase missing notes.
- **Media**: recordings and videos stay outside this repository; link to
  them. Documents already in the repo (a concert programme, a schedule) can be
  linked by site path, which the checker checks exists. A published review of
  the concert is `kind: review`.

## Splitting an old volume

For a year with one big PDF, set `proceedings.source_pdf` and
`proceedings.page_offset` (PDF page number minus printed page number) on the
conference page. Give each entry `pages`, and `split` in the CSV's `pdf`
column (which sets `pdf` to the entry's own folder), then run:

```sh
python3 scripts/split_proceedings.py YYYY --dry-run   # check the ranges
python3 scripts/split_proceedings.py YYYY
```

If the offset changes partway through (unnumbered inserts), set
`pdf_pages: 40-47` on the affected entries. If the year was issued as more
than one PDF (2014), keep one in `proceedings.source_pdf` and give each entry
in another volume its own `source_pdf` and `pdf_pages`. Look at the first
page of a few outputs.

`import_contributions.py --extract-abstracts` drafts empty abstracts from the
PDFs. It starts after an "Abstract" heading; items that print their text under
the section's name instead (artist talks, posters, studio reports) need
`--abstract-heading "abstract|artist talk|poster|studio report"`. It stops at
the introduction, keywords, the page number or the item's title, drops
running headers and figure captions, and guesses paragraph breaks from short
lines. Always read the drafts: two-column layouts, cropped author blocks,
paragraph breaks and words split across lines need fixing by hand.

Two cases the extractor can't handle:

- **No abstract printed** (common before about 2005). Use the opening of the
  paper's introduction, the sentences that say what the paper does, and add
  a YAML comment above the body saying so, e.g. `# No abstract is printed:
  the body is the statement of purpose from the paper's introduction.`
  Scholar still gets a description, and the comment keeps the record honest.
- **An abstract with no heading** (the text just starts under the authors).
  The extractor looks for a heading line, so it finds nothing. Type the text
  from the page into the CSV's `abstract` column.

If you change the extractor, run `python3 scripts/test_extract_abstracts.py`
before and after: it scores every strategy against the abstracts already
reviewed in 2000, 2007 and 2008.

## OCR

Install with `brew install ocrmypdf` (it brings tesseract). Check each
volume's text layer first: `pdftotext -f N -l N volume.pdf -` should give
readable words. There are three cases:

- **Image-only pages** (2002, 2010): nothing comes out. Add a text layer
  without touching the pages that have one, and commit the result in place of
  the volume before splitting, so the split PDFs are searchable too:

  ```sh
  ocrmypdf --skip-text -O 1 volume.pdf volume-ocr.pdf
  ```

- **Garbled text** (2014's papers volume shifts every letter by 3): OCR a
  copy into a scratch folder and draft from that. Don't commit it: forced OCR
  turns every page into an image, so a born-digital PDF grows 10–40 times
  (2007's 7-page Burt keynote: 390 KB to 3.9 MB with `-O 3`).

  ```sh
  ocrmypdf --force-ocr -O 3 volume.pdf /tmp/scratch/volume-ocr.pdf
  pdftotext -f N -l N /tmp/scratch/volume-ocr.pdf -
  ```

  To draft abstracts from it, point `proceedings.source_pdf` at the OCR copy
  only while running the import, or paste the text into the CSV's `abstract`
  column.

- **Messy but readable text** (2007's Burt keynote: "th a t", "graph ics"):
  leave the published PDF alone and fix the abstract by hand. Scholar copes
  with this, and the page's abstract is what it indexes first.

Scanned pages often need `--rotate-pages` or `--deskew`. Check the OCR text
of names, titles and numbers against the page image.

## Checks

`scripts/check_contributions.py` runs in CI on every pull request and before
every deploy. It fails on missing fields, unknown types or review values,
missing PDFs, a section with no review default, or a conference without a
date. Run it with `--site _site` after a build to check the Scholar tags on
the built pages.
