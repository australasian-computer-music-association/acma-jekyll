# Plan: citable proceedings: per-item pages for papers and creative works

## Goal

Give every ACMC contribution its own citable, indexable record: papers, abstracts, keynotes and **creative works**. Each one gets its own page and appears in Google Scholar. The main focus is the pre-2019 volumes, which contain full papers. The post-2019 abstracts and program notes get the same treatment, and the setup should be easy for the committee and future conference chairs to keep up.

**Creative works are first-class outputs, not an add-on.** Every ACMC creative work was selected by peer review or by a jury or committee, so each is a reviewed non-traditional research output (NTRO) and deserves the same citable record as a paper. The models are the NIME music proceedings (each work is a citable entry with a program note) and the *Journal for Artistic Research* (a work is presented with a statement of its research). ACMC takes a simpler version of that idea: a **program note**, an optional **research statement**, a clear **review statement**, and links to **documentation** (audio, video, score).

Today most volumes are one big PDF with a plain title list (or no list) on the conference page, and creative works are mostly absent or only in concert programmes. Scholar indexes **items, not volumes**: it needs one HTML landing page per item carrying `citation_*` meta tags. Nothing on the site sets those tags yet (see `docs/proceedings-status.md`).

## Decisions made

| Question | Decision |
|---|---|
| Storage | **One Markdown file per contribution** in a `_contributions` collection. Front matter holds the metadata. The body holds the abstract, or for a creative work its program note and optional research statement. Native Jekyll, no generator plugin. The collection is deliberately not called `_papers`, because papers and works sit side by side in it. |
| What gets Scholar tags | **Everything**: papers, abstracts, keynotes, posters and creative works. Creative works get the same citation tags as papers. |
| Review status | Every entry states how it was reviewed (peer-reviewed / juried / curated / invited). The default is set per conference and per type, can be overridden per entry, and is shown on the page. This is the evidence NTRO reporting asks for. |
| Abstract whose full paper is in Chroma (2020+) | Own page, **no** Scholar tags, prominent link to the Chroma article, so citations collect on one record. |
| Full-volume PDFs | **Kept** and linked as "Complete proceedings", with no tags. Split PDFs are added alongside them. |
| Media (audio, video, scores) | Not stored in git. Linked from the entry to wherever it lives (archive.org, Vimeo/YouTube, Zenodo, an artist's site). |
| DOIs | Not now. A `doi:` field is reserved. Note: DOIs matter more for NTROs than for papers, because university research offices often ask for one, so Zenodo should be revisited soon (see Later). |
| Data entry for old volumes | Claude drafts from each PDF's text layer and concert programmes, and the maintainer reviews it in a PR. |
| `_drafts/found/` (2002 per-paper files, 2003/2012 papers, 2020 CSV) | Left out for now. Those files are on another machine and come in a later phase. |

## What Google Scholar needs (checklist)

From Scholar's inclusion guidelines, which this design follows:

- [ ] One URL per item, with the title and creators visible on the page and the full abstract or program note (or full text) readable without login or JavaScript.
- [ ] Highwire Press tags in `<head>`: `citation_title`, `citation_author` (one per creator), `citation_publication_date`, `citation_conference_title`, plus `citation_pdf_url`, `citation_firstpage`/`citation_lastpage`, `citation_publisher` and `citation_issn`/`citation_isbn` where known. Zotero and Mendeley read the same tags, so a creative work becomes one-click citable even if Scholar is slow to list it.
- [ ] Each PDF holds **one** item and starts on that item's first page, with title and creators at the top. A text layer is needed (it already exists for almost all volumes; 2002 and 2010 have some image-only pages to OCR). Keep PDFs under about 5 MB where possible.
- [ ] PDFs on the same site, ideally in the same directory as the landing page.
- [ ] A plain HTML browse path from the home page to every item page: home → `/proceedings/` → year → item. All item pages in `sitemap.xml` (jekyll-sitemap does this automatically for collections).
- [ ] No citation tags on volume-level pages (conference pages, full-volume PDFs), so Scholar doesn't make one record for a whole book.

## Architecture

### 1. Conference = volume metadata

Each `_conferences/*.md` gets a `proceedings:` block. Volume metadata, including how each kind of contribution was reviewed that year, is stated once here and never repeated per item:

```yaml
year: 2018
proceedings:
  title: "Proceedings of the Australasian Computer Music Conference 2018"
  editors: ["…"]
  publisher: "Australasian Computer Music Association"
  issn: "1448-7780"          # or isbn:
  published: 2018-12-06      # publication date (falls back to year)
  pdf: /proceedings/ACMC2018-proceedings.zip   # full volume, kept
  page_offset: 0             # PDF page = printed page + offset (used by the splitter)
  review:                    # default review statement per type; shown on each item page
    paper: { status: peer-reviewed, note: "Double-blind peer review" }
    abstract: { status: not-reviewed }
    creative-work: { status: peer-reviewed, note: "Selected by peer review of submitted works" }
```

`year:` is the join key, which avoids the mixed `acmc-2007` / `acmc2018` filenames. Where a year's process is unknown, the default for creative works is `juried` ("Selected by the conference committee"). Years with known detail say so.

### 2. `_contributions` collection: one file per contribution

Path: `_contributions/acmc2018/<slug>.md`. URL: `/proceedings/acmc2018/<slug>/`. The slug is the first creator's surname plus the first words of the title, lower-case ASCII, and never changes once published.

Fields shared by every entry:

```yaml
---
title: "…"
authors:             # creators: authors, composers, artists
  - Jesse Austin-Stewart
year: 2018
type: creative-work  # paper | abstract | keynote | poster | studio-report | creative-work
section: Refereed Creative Works   # heading on the conference page (the volume's own wording)
order: 1             # position in the volume/programme
pages: 3             # printed page range, if printed in a volume
pdf:                 # per-item PDF, if any
review:              # optional override of the conference default
  status: peer-reviewed
chroma:              # full paper in Chroma → no citation tags on this page
doi:                 # reserved
---
```

Extra fields for creative works (all optional except `format`):

```yaml
work:
  kind: composition        # composition | performance | installation | audiovisual | improvisation | sound-art | other
  format: "8-channel fixed media for 40-speaker wall"   # instrumentation / medium, as in the programme
  duration: "8:00"
  created: 2018            # year of the work, if different from the conference
  performers: ["…"]        # if not the creators
  presented:               # where ACMC presented it
    event: "Concert 2"
    venue: "WAAPA Music Auditorium, Perth"
    date: 2018-12-07
media:                     # documentation, hosted elsewhere
  - { kind: video, url: "https://…", label: "Performance video" }
  - { kind: score, url: "https://…" }
```

Body: an **abstract** for papers. For creative works, a **Program note** section and an optional **Research statement** section (background, contribution, significance: the three headings NTRO reporting uses). Old years will mostly have the program note only, and new years can ask artists for both.

New split PDFs go in `proceedings/acmc2018/<slug>.pdf`, next to their landing page. The files already split (2001, 2005, 2006, 2018 papers) **stay where they are**. Their `pdf:` just points at the existing path, so no URLs break.

### 3. Templates

- `_layouts/contribution.html`: one layout for every type, with a creative-work block switched on by `type`.
  - `<head>`: Highwire `citation_*` tags (volume data pulled from the matching conference), plus schema.org JSON-LD: `ScholarlyArticle` for papers, and `MusicComposition` / `CreativeWork` for works, with the creators, date and the ACMC event where it was presented.
  - Visible page: title, creators, **review statement** (e.g. "Peer-reviewed creative work"), the "In: *Proceedings of ACMC 2018*, Perth" line, the abstract or program note and research statement, the work's details (format, duration, performers, where and when presented), documentation links, a PDF link, a **"How to cite"** line and a copyable BibTeX entry, and a link back to the conference.
  - BibTeX: `@inproceedings` when the item is printed in the proceedings (works included, as NIME does), otherwise `@misc` with the event in `howpublished`.
  - If `chroma:` is set, the tags are skipped and the page says "Full paper in Chroma →".
- `_includes/contribution-list.html`: conference pages replace their hand-typed lists with `{% include contribution-list.html %}`. It lists the year's entries grouped by `section` and sorted by `order`, with papers and works given the same treatment. The hand-written intro text on conference pages stays.
- `/proceedings/` index page: every year, with counts of papers and of creative works, and links. A second index, `/proceedings/creative-works/`, lists every work across all years, so the creative archive is visible in its own right.

### 4. Scripts (`scripts/`, excluded from the site build)

| Script | Purpose |
|---|---|
| `check_contributions.py` | Validates every entry: required fields, `type`/`review.status`/`work.kind` enums, a conference exists for `year`, a review status resolves (either a conference default or an override), creative works have `work.format`, the `pdf` file exists, page ranges don't overlap, the slug is valid, and media URLs are well-formed. **Runs in CI before `jekyll build`**, so a bad entry fails the build instead of shipping. |
| `split_proceedings.py <year>` | Reads `pages:` from that year's entries and `page_offset` from the conference, then writes the per-item PDFs and sets the PDF Title/Author metadata. The front matter is the single source of truth, so re-running gives the same output. |
| `draft_contributions.py <year>` | Pulls a TOC, abstracts and program notes from a volume's or programme's text layer and writes **draft** entries for human review. Used for the back catalogue. |
| `import_contributions.py <year> <file.csv>` | For chairs. Takes a CSV with columns `title, authors, type, section, order, abstract, pdf, chroma`, plus the work columns `kind, format, duration, performers, event, venue, date, media_url, research_statement`. Authors are separated by `;`. Writes the entries. This is the kind of export conference systems produce. |

### 5. Docs for future chairs

`docs/adding-proceedings.md` will cover:
- the CSV template, how to run the import, where PDFs go, and how to check the result locally;
- what to collect from artists at submission time: program note, research statement, format, duration, performers, documentation link (and ideally a licence for the documentation);
- how to fill in the year's review statement.

Adding a year becomes: fill in the conference `proceedings:` block, import the CSV, drop in the PDFs, open a PR. CI catches mistakes.

## Phases (one PR each, or one per year where marked)

**Phase 1: infrastructure + pilots**
- [ ] `_contributions` collection config, `contribution.html` layout, `contribution-list.html` include, `/proceedings/` and `/proceedings/creative-works/` indexes
- [ ] `check_contributions.py` wired into both workflows
- [ ] Pilot with **2018**, which has refereed papers (already split), non-refereed abstracts and **refereed creative works** in one year, so both the paper and the work page shapes are tested on real data. Check the built tags against Scholar's guidelines and test with Zotero
- [ ] Fix the stale 2011 row in `docs/proceedings-status.md` (the volume is committed and linked) and point the doc's plan at this plan/issue

**Phase 2: migrate the other already-split years**
- [ ] 2001, 2005 (with the 2005 concert programme's works), 2006 (existing PDF paths kept)
- [ ] 2023 (abstracts and concert works now on the page → entries, with `chroma:` for the 6 full papers)

**Phase 3: split volumes that already have title lists** (one PR per year; check each list against the PDF's TOC first, since the 2009/2010 lists look short). Add each year's creative works in the same PR where the volume or a programme has them.
- [ ] 2000 · [ ] 2004 · [ ] 2007 · [ ] 2008 · [ ] 2009 · [ ] 2010 (needs OCR on some pages) · [ ] 2011

**Phase 4: volumes with no list yet** (draft from TOC, then split)
- [ ] 2014 (papers volume + talks/posters volume + 7 concert programmes) · [ ] 2015 · [ ] 2016 · [ ] 2017 · [ ] 2019 (+ programme booklet)

**Phase 5: abstract-era years (2020+)**
- [ ] 2021, 2022, 2024 from their volumes; 2020 from its CSV once `_drafts/found/` is back
- Proposal: **no per-abstract PDF splits** for these years. The text is on the landing page, which is enough for Scholar, and the full volume stays linked. See open questions.

**Phase 6: creative works back catalogue**
- [ ] Years whose works survive only outside the proceedings: concert lists in Chroma reports, archived conference sites and programmes. Each work gets an entry with at least title, creators, format and the concert it was in, even where no program note survives.

**Phase 7: going forward**
- [ ] `docs/adding-proceedings.md` + CSV template; 2026 is the first year done this way, with research statements requested from artists

**Later**
- [ ] 2002 per-paper originals, 2003, 2012 and the 1990s finds from `_drafts/found/`
- [ ] DOIs via a Zenodo community. This is a high priority for creative works, because Zenodo supports audio, video and other resource types and gives NTROs the persistent identifier research offices ask for. It also gives documentation a durable home
- [ ] After launch: check Search Console for indexing; if pages still aren't in Scholar after a few months, use Scholar's publisher support form

## Notes and risks

- **Repo size:** keeping full volumes and adding split copies adds roughly 100 MB to `proceedings/` (currently 244 MB). This is acceptable for an archive repo, and FTP deploy only uploads changed files. Media stays out of git.
- **Scholar timing:** Scholar recrawls slowly. Expect weeks to months before entries appear. Tags must be right the first time, which is why there are pilot years.
- **Scholar and creative works:** Scholar decides for itself what it lists, and it favours entries with substantial text and a PDF. Creative works with a full program note, a research statement and (where printed) a PDF stand the best chance. Whatever Scholar does, each work still has a stable URL, a review statement, a "How to cite" line and tags Zotero can read, so it is citable either way. This is another reason for DOIs later.
- **Review history:** the review process for creative works in old years (peer review vs. jury vs. committee) has to be confirmed year by year from calls for works and Chroma reports. Until a year is confirmed, the default is "selected by the conference committee".
- **Creator names:** written as given in the volume ("Andrew R. Brown"). Keeping one spelling across years helps Scholar's author profiles, so the validator could warn on near-duplicates.
- **Page boundaries:** a few old volumes may start items mid-page or share pages (common for program notes). These are flagged during review; the split rule is "starts on the item's first page", and items that share a page get no per-item PDF.

## Open questions

1. Abstract-era years: is the landing page enough, or do you also want one-page PDF splits per abstract? (Proposal: landing page only.)
2. Creative works with no printed note: should a small per-work PDF be generated from the entry (note + details + review statement) to help Scholar? (Proposal: not at first; revisit with DOIs, since Zenodo needs a file anyway.)
3. URL shape `/proceedings/acmc2018/<slug>/`: OK?
4. Should `section` headings follow each volume's own TOC wording (e.g. "Refereed Papers", "Studio Reports") or a fixed vocabulary? (Proposal: the volume's own wording, with `type` as the fixed vocabulary.)
5. Review vocabulary: are `peer-reviewed | juried | curated | invited | not-reviewed` the right terms for ACMC, and do you know which years used which process for creative works?
