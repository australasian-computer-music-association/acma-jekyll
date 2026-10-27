---
name: proceedings-year
description: Add one ACMC year's proceedings to the site as per-item _contributions entries (papers, abstracts, creative works), splitting the volume PDF where needed, and open a PR. Use when asked to "do ACMC YYYY", migrate a year's proceedings, or resume such work on an acmcYYYY-contributions branch.
---

# Add one year's proceedings

You are doing one year of the plan in `docs/scholar-plan.md` (issue #9). The
field reference is `docs/adding-proceedings.md`. Read both before starting.
2018 (`_contributions/ACMC2018-proceedings/`, `_conferences/acmc2018.md`) is the worked
example; copy its patterns.

The work must be resumable. Push after every step, and keep the PR checklist
up to date, so a new session can carry on from the branch alone.

## 0. Start or resume

- Branch: `acmcYYYY-contributions` off `main`. If it already exists, check it
  out, read its PR (if any) and the commits, and continue from the first
  unticked step.
- Only touch `_contributions/ACMCYYYY-proceedings/`, `proceedings/ACMCYYYY-proceedings/`, that year's
  `_conferences/` file, and that year's row in `docs/proceedings-status.md`.
  Other years' PRs run in parallel. Template or script changes go in their
  own PR, unless they're tiny fixes the year needs; say so in the PR.
- Tools: `pip install pyyaml pypdf`; poppler (`pdftotext`, `pdfinfo`) is
  needed. Build with `bundle exec jekyll build`.

## 1. Survey the sources

- Find everything for the year: `proceedings/ACMCYYYY-*`, any per-item
  folders, programmes, the conference page's current lists, and the year's
  row in `docs/proceedings-status.md` and the review-terminology table in
  `docs/scholar-plan.md`.
- Extract the contents pages: `pdftotext -layout -f 1 -l 10 <volume>.pdf -`.
- Find the **page offset**: compare printed page numbers in footers with PDF
  page numbers (`pdftotext -f N -l N`). Note if it changes partway through.
- Read the front matter for: the volume title, editors, ISSN/ISBN, date,
  publisher, copyright or licence statement, review statements, and
  juries/committees. Quote review
  statements **verbatim**.
- Check the text layer (`pdftotext` gives words, not empty strings or
  gibberish). 2014's papers volume has every letter shifted by 3, so decode it
  or OCR it (`ocrmypdf`); 2002 and 2010 have some image-only pages.

## 2. Conference front matter

Add `year`, `start_date`/`end_date` (if known) and the `proceedings:` block.
Include `reviewing` defaults per section, set **only** from what the volume
states; use `""` for unknown (see the table in `docs/adding-proceedings.md`).
Add the volume's `review_statement` (verbatim), its `committees` (juries,
committees and organisers, as listed in the volume) and its `copyright`
statement (verbatim), where the volume has them.
For a volume to split, add `source_pdf` and `page_offset`. Commit and push.

## 3. Draft the entries

- Write a CSV (keep it out of the repo, e.g. in a scratch folder) with one row
  per item in volume order. Use **the title as printed on the item's own first
  page** (the contents page often differs), in title case, and authors as
  printed there. Sections use the volume's own heading wording.
- Entries go in `_contributions/ACMCYYYY-proceedings/` and are published as
  `/proceedings/ACMCYYYY-proceedings/<slug>.html`, in the **same folder as
  their PDFs**. Google Scholar wants `citation_pdf_url` in the same directory
  as the page, and the checker enforces this. In the CSV, put `split` in the
  `pdf` column for items to cut from the volume (they become `<slug>.pdf`).
  Items that share pages (abstracts, program notes) get `section_pdf`, not
  `pdf`.
- Items **already split** into their own files (2001, 2003, 2005, 2006) are
  already in `proceedings/ACMCYYYY-proceedings/`: point `pdf` at the existing
  file and **don't move or rename it**. Then run
  `python3 scripts/split_proceedings.py YYYY --fix-metadata` to put the right
  title and authors inside the PDFs. 2018 is the worked example.
- `python3 scripts/import_contributions.py YYYY file.csv --extract-abstracts`
- **Read every drafted abstract** against the PDF. Fix cropped author lines,
  words that lost their hyphens at line ends (`computeraided` →
  `computer-aided`), and en dashes lost from the text layer. Keep the authors'
  own typos as printed. Then run `python3 scripts/check_contributions.py`
  and clear its body warnings: a body that starts in lower case or with an
  institution is header text left over from the PDF, and a sentence split
  across two paragraphs is a page break.
- Creative works: program note in the body, `work.format` (required),
  `work.created`, `keywords` from "KW:" lines, and `work.kind` where it's
  clear. The note starts after the **whole** header block (title,
  instrumentation, affiliation). An instrumentation line can wrap onto a
  second line (ACMC 2018, *Noise in the Clouds*), so don't count lines.
- Commit and push.

## 4. Split the PDFs (volumes only)

The splitter writes each item's title and authors into its PDF's metadata.

- `python3 scripts/split_proceedings.py YYYY --dry-run`, then without
  `--dry-run`.
- Open the first page of at least three outputs (`pdftotext -l 1`): each must
  start with its own title and authors. Fix offsets with `pdf_pages` where
  needed.
- Commit and push.

## 5. Conference page

Replace the hand-typed lists with `{% include contribution-list.html %}` (or
`level=3` under a "Proceedings" heading), followed by
`{% include proceedings-review.html %}`, keeping the intro, links to the
complete volume and any call text. Remove links that the entries now cover.

## 6. Check

```sh
python3 scripts/check_contributions.py
bundle exec jekyll build
python3 scripts/check_contributions.py --site _site
```

Look at the conference page and two entry pages in a browser or a screenshot.
Update the year's row in `docs/proceedings-status.md`. Commit and push.

## 7. Pull request

Title "ACMC YYYY: per-item proceedings pages". The body lists what's in it
(counts by type), the review statuses and where they came from, every
judgement call (title differences, unclear review status, typos kept), and
this checklist for the reviewer:

- [ ] Item list matches the volume's contents
- [ ] Three PDFs spot-checked (start on the right page)
- [ ] Review statuses are as the volume states them
- [ ] Abstracts read cleanly

Keep at most two year-PRs open at a time.
