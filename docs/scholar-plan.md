# Plan: per-paper proceedings pages for Google Scholar

## Goal

Make every ACMC contribution show up as its own record in Google Scholar. The main focus is the pre-2019 volumes, which contain full papers. The post-2019 abstracts and program notes should get the same treatment, and the setup should be easy for the committee and future conference chairs to keep up.

Today most volumes are one big PDF with a plain title list (or no list) on the conference page. Scholar indexes **papers, not volumes**: it needs one HTML landing page per paper carrying `citation_*` meta tags. Nothing on the site sets those tags yet (see `docs/proceedings-status.md`).

## Decisions made

| Question | Decision |
|---|---|
| Storage | **One Markdown file per contribution** in a `_papers` collection. Front matter holds the metadata and the body holds the abstract. Native Jekyll, no generator plugin. |
| What gets Scholar tags | **Everything**: papers, abstracts, keynotes, posters, program notes, creative works. |
| Abstract whose full paper is in Chroma (2020+) | Own page, **no** Scholar tags, prominent link to the Chroma article, so citations collect on one record. |
| Full-volume PDFs | **Kept** and linked as "Complete proceedings", with no tags. Split PDFs are added alongside them. |
| DOIs | Not now. A `doi:` field is reserved so they can be added later (e.g. via Zenodo). |
| Data entry for old volumes | Claude drafts from each PDF's text layer, and the maintainer reviews it in a PR. |
| `_drafts/found/` (2002 per-paper files, 2003/2012 papers, 2020 CSV) | Left out for now. Those files are on another machine and come in a later phase. |

## What Google Scholar needs (checklist)

From Scholar's inclusion guidelines, which this design follows:

- [ ] One URL per paper, with the title and authors visible on the page and the full abstract (or full text) readable without login or JavaScript.
- [ ] Highwire Press tags in `<head>`: `citation_title`, `citation_author` (one per author), `citation_publication_date`, `citation_conference_title`, plus `citation_pdf_url`, `citation_firstpage`/`citation_lastpage`, `citation_publisher` and `citation_issn`/`citation_isbn` where known.
- [ ] Each PDF holds **one** paper and starts on that paper's first page, with title and authors at the top. A text layer is needed (it already exists for almost all volumes; 2002 and 2010 have some image-only pages to OCR). Keep PDFs under about 5 MB where possible.
- [ ] PDFs on the same site, ideally in the same directory as the landing page.
- [ ] A plain HTML browse path from the home page to every paper page: home → `/proceedings/` → year → paper. All paper pages in `sitemap.xml` (jekyll-sitemap does this automatically for collections).
- [ ] No citation tags on volume-level pages (conference pages, full-volume PDFs), so Scholar doesn't make one record for a whole book.

## Architecture

### 1. Conference = volume metadata

Each `_conferences/*.md` gets a `proceedings:` block. Volume metadata is stated once here, never repeated per paper:

```yaml
year: 2007
proceedings:
  title: "Proceedings of the Australasian Computer Music Conference 2007"
  editors: ["…"]
  publisher: "Australasian Computer Music Association"
  issn: "1448-7780"          # or isbn:
  published: 2007-06-19      # publication date (falls back to year)
  pdf: /proceedings/ACMC2007-proceedings.pdf   # full volume, kept
  page_offset: 6             # PDF page = printed page + offset (used by the splitter)
```

`year:` is the join key, which avoids the mixed `acmc-2007` / `acmc2018` filenames.

### 2. `_papers` collection: one file per contribution

Path: `_papers/acmc2007/harrald-collaborative-music-making.md`. URL: `/proceedings/acmc2007/harrald-collaborative-music-making/`. The slug is the first author's surname plus the first words of the title, lower-case ASCII, and never changes once published.

```yaml
---
title: "Collaborative Music Making with Live Algorithms"
authors:
  - Luke Harrald
year: 2007
type: paper          # paper | abstract | keynote | poster | studio-report | creative-work | program-note
section: Papers      # heading on the conference page (optional; defaults from type)
order: 12            # position in the volume/programme
pages: 45-52         # printed page range (optional)
pdf: /proceedings/acmc2007/harrald-collaborative-music-making.pdf
chroma:              # URL of the full paper in Chroma → page gets no citation tags
doi:                 # reserved
---
Abstract (Markdown). For program notes: the note itself.
```

New split PDFs go in `proceedings/acmc2007/<slug>.pdf`, next to their landing page. The files already split (2001, 2005, 2006, 2018) **stay where they are**. Their `pdf:` just points at the existing path, so no URLs break.

### 3. Templates

- `_layouts/paper.html`: writes the Highwire `citation_*` tags (pulling volume data from the matching conference), a schema.org `ScholarlyArticle` JSON-LD block, and a visible page. The page shows the title, the authors, "In: *Proceedings of ACMC 2007*, Canberra, pp. 45–52", the abstract, a PDF link, a copyable BibTeX entry, and a link back to the conference. If `chroma:` is set, the tags are skipped and the page says "Full paper in Chroma →".
- `_includes/paper-list.html`: conference pages replace their hand-typed lists with `{% include paper-list.html %}`. It lists `site.papers` for that year, grouped by `section` and sorted by `order`, with each entry linking to its landing page. The hand-written intro text on conference pages stays.
- `/proceedings/` index page: every year, with counts and links. This is the browse path for crawlers and people.

### 4. Scripts (`scripts/`, excluded from the site build)

| Script | Purpose |
|---|---|
| `check_papers.py` | Validates every `_papers` file: required fields, `type` enum, a conference exists for `year`, the `pdf` file exists, page ranges don't overlap, the slug is valid. **Runs in CI before `jekyll build`**, so a bad entry fails the build instead of shipping. |
| `split_proceedings.py <year>` | Reads `pages:` from that year's `_papers` files and `page_offset` from the conference, then writes the per-paper PDFs and sets the PDF Title/Author metadata. The front matter is the single source of truth, so re-running gives the same output. |
| `draft_papers.py <year>` | Pulls a TOC and abstracts from a volume's text layer and writes **draft** `_papers` stubs for human review. Used for the back catalogue. |
| `import_papers.py <year> <file.csv>` | For chairs. Takes a CSV (`title, authors, type, section, order, abstract, pdf, chroma`; authors separated by `;`), the kind of export conference systems produce, and writes the `_papers` files. |

### 5. Docs for future chairs

`docs/adding-proceedings.md` will cover the CSV template, how to run the import, where PDFs go, and how to check the result locally. Adding a year becomes: fill in the conference `proceedings:` block, import the CSV, drop in the PDFs, open a PR. CI catches mistakes.

## Phases (one PR each, or one per year where marked)

**Phase 1: infrastructure + pilot (ACMC 2006)**
- [ ] `_papers` collection config, `paper.html` layout, `paper-list.html` include, `/proceedings/` index
- [ ] `check_papers.py` wired into both workflows
- [ ] Migrate 2006 (55 PDFs, already split) as the pilot; check the built HTML tags against Scholar's guidelines
- [ ] Fix the stale 2011 row in `docs/proceedings-status.md` (the volume is committed and linked) and point the doc's plan at this issue

**Phase 2: migrate already-split years**
- [ ] 2001, 2005 (existing PDF paths kept)
- [ ] 2018 papers; split the combined abstracts and creative-works PDFs into per-item entries
- [ ] 2023 (abstracts now on the page → `_papers`, with `chroma:` for the 6 full papers)

**Phase 3: split volumes that already have title lists** (one PR per year; check each list against the PDF's TOC first, since the 2009/2010 lists look short)
- [ ] 2000 · [ ] 2004 · [ ] 2007 · [ ] 2008 · [ ] 2009 · [ ] 2010 (needs OCR on some pages) · [ ] 2011

**Phase 4: volumes with no list yet** (draft from TOC, then split)
- [ ] 2014 (papers volume + talks/posters volume) · [ ] 2015 · [ ] 2016 · [ ] 2017 · [ ] 2019

**Phase 5: abstract-era years (2020+)**
- [ ] 2021, 2022, 2024 from their volumes; 2020 from its CSV once `_drafts/found/` is back
- Proposal: **no per-abstract PDF splits** for these years. The abstract text is on the landing page, which is enough for Scholar, and the full volume stays linked. See open questions.

**Phase 6: going forward**
- [ ] `docs/adding-proceedings.md` + CSV template; 2026 is the first year done this way

**Later**
- [ ] 2002 per-paper originals, 2003, 2012 and the 1990s finds from `_drafts/found/`
- [ ] Optional: DOIs via a Zenodo community
- [ ] After launch: check Search Console for indexing; if paper pages still aren't in Scholar after a few months, use Scholar's publisher support form

## Notes and risks

- **Repo size:** keeping full volumes and adding split copies adds roughly 100 MB to `proceedings/` (currently 244 MB). This is acceptable for an archive repo, and FTP deploy only uploads changed files.
- **Scholar timing:** Scholar recrawls slowly. Expect weeks to months before entries appear. Tags must be right the first time, which is why there's a pilot year.
- **Tagging everything:** Scholar may quietly drop some program notes or creative works. That doesn't affect the papers.
- **Author names:** written as given in the volume ("Andrew R. Brown"). Keeping one spelling across years helps Scholar's author profiles, so the validator could warn on near-duplicates.
- **Page boundaries:** a few old volumes may start papers mid-page or share pages. These are flagged during review; the split rule is "starts on the paper's first page".

## Open questions

1. Abstract-era years: is the landing page enough, or do you also want one-page PDF splits per abstract? (Proposal: landing page only.)
2. URL shape `/proceedings/acmc2007/<slug>/`: OK?
3. Should `section` headings follow each volume's own TOC wording (e.g. "Refereed Papers", "Studio Reports") or a fixed vocabulary? (Proposal: the volume's own wording, with `type` as the fixed vocabulary.)
