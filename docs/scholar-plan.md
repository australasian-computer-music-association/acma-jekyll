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
| Review status | A `reviewing` key records how an item was reviewed **only when the volume says so** (e.g. "fully refereed" → `full-paper`). Unknown is an empty string, and nothing is shown. Defaults are set per conference and per section, can be overridden per item, and are shown on the page with the volume's own review statement quoted. This is the evidence NTRO reporting asks for. See "Review terminology" below. |
| Types and sections | `type` is a small fixed list, worked out from the volumes' own headings (consistent up to 2020). `section` keeps each volume's exact heading wording. |
| Abstract whose full paper is in Chroma (2020+) | Own page, **no** Scholar tags, prominent link to the Chroma article, so citations collect on one record. |
| Per-item PDFs | Only where an item was printed in a volume (papers, pre-2020). **2020+ items and creative works without a printed note get a landing page only.** |
| Full-volume PDFs | **Kept** and linked as "Complete proceedings", with no tags. Split PDFs are added alongside them. |
| Media (audio, video, scores) | Not stored in git. Linked from the entry to wherever it lives (archive.org, Vimeo/YouTube, Zenodo, an artist's site). |
| DOIs | **Deferred; see how things go first.** The landing page on this site is the version of record. Zenodo DOIs resolve to Zenodo's copy rather than to that page, which has confused matters for NIME, so Zenodo is not the plan. If DOIs are wanted later, the likely route is minting ACMA's own (e.g. Crossref or DataCite membership, with the cost budgeted) so that each DOI resolves to the landing page. A `doi:` field is reserved so nothing has to change structurally. |
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

## As built (step 1)

Step 1 changed a few details from the design below. `docs/adding-proceedings.md` is the authoritative field reference.

- Conference `proceedings:` block: `full_volume` (the complete volume, kept) and, for volumes to be split, `source_pdf` and `page_offset`. Review statements are per section (`review_statements:`), because 2018 had separate paper and music juries. Entries take their date from `proceedings.published`, or else the conference's `start_date`, which is now required.
- Entries: `section_pdf` for items printed on shared pages (abstracts, program notes), linked but not tagged as the item's PDF; `keywords` (from "KW:" lines); `research_statement` as a front-matter field rather than a body section; `pdf_pages` to override the page offset for one item.
- Three scripts, not four: abstract drafting is `import_contributions.py --extract-abstracts`, rather than a separate `draft_contributions.py`.
- One small plugin, `_plugins/contribution_dates.rb`. Without it, jekyll-seo-tag would give every entry the build time as its publication date.
- Allowed `type` and `reviewing` values live in `_data/contribution_types.yml` and `_data/reviewing.yml`, which the templates and the checker both read.
- 2018's ISSN is 2206-5296, not 1448-7780: check each volume's own ISSN or ISBN.

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
  review_statement: >-      # quoted verbatim from the volume, shown on item pages
    The paper refereeing process is conducted according to the specifications of the
    Australian Government for the collection of Higher Education research data, and fully
    refereed papers therefore meet Australian Government requirements for fully-refereed
    research papers.
  reviewing:                 # default per section heading; only what the volume states
    "Refereed Papers": full-paper
    "Non-refereed Abstracts": non-refereed
    "Refereed Creative Works": refereed
```

`year:` is the join key, which avoids the mixed `acmc-2007` / `acmc2018` filenames.

### 2. `_contributions` collection: one file per contribution

Path: `_contributions/acmc2018/<slug>.md`. URL: `/proceedings/acmc2018/<slug>/`. The slug is the first creator's surname plus the first words of the title, lower-case ASCII, and never changes once published.

Fields shared by every entry:

```yaml
---
title: "…"
authors:             # creators: authors, composers, artists
  - Jesse Austin-Stewart
year: 2018
type: creative-work  # paper | abstract | keynote | artist-talk | studio-report | poster | creative-work
section: Refereed Creative Works   # heading on the conference page (the volume's own wording)
order: 1             # position in the volume/programme
pages: 3             # printed page range, if printed in a volume
pdf:                 # per-item PDF, if any
reviewing:           # optional override of the section default: full-paper | abstract | refereed | invited | non-refereed | "" (unknown)
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
  - Visible page: title, creators, **review status** (e.g. "Refereed creative work", with the volume's review statement on hover or underneath; nothing shown when unknown), the "In: *Proceedings of ACMC 2018*, Perth" line, the abstract or program note and research statement, the work's details (format, duration, performers, where and when presented), documentation links, a PDF link, a **"How to cite"** line and a copyable BibTeX entry, and a link back to the conference.
  - BibTeX: `@inproceedings` when the item is printed in the proceedings (works included, as NIME does), otherwise `@misc` with the event in `howpublished`.
  - If `chroma:` is set, the tags are skipped and the page says "Full paper in Chroma →".
- `_includes/contribution-list.html`: conference pages replace their hand-typed lists with `{% include contribution-list.html %}`. It lists the year's entries grouped by `section` and sorted by `order`, with papers and works given the same treatment. The hand-written intro text on conference pages stays.
- `/proceedings/` index page: every year, with counts of papers and of creative works, and links. A second index, `/proceedings/creative-works/`, lists every work across all years, so the creative archive is visible in its own right.

### 4. Scripts (`scripts/`, excluded from the site build)

| Script | Purpose |
|---|---|
| `check_contributions.py` | Validates every entry: required fields, `type`/`reviewing`/`work.kind` enums, a conference exists for `year`, every item's `section` is either known to the conference's `reviewing` map or has its own `reviewing` (an empty string counts, so "unknown" is always a deliberate choice), creative works have `work.format`, the `pdf` file exists, page ranges don't overlap, the slug is valid, and media URLs are well-formed. **Runs in CI before `jekyll build`**, so a bad entry fails the build instead of shipping. |
| `split_proceedings.py <year>` | Reads `pages:` from that year's entries and `page_offset` from the conference, then writes the per-item PDFs and sets the PDF Title/Author metadata. The front matter is the single source of truth, so re-running gives the same output. |
| `draft_contributions.py <year>` | Pulls a TOC, abstracts and program notes from a volume's or programme's text layer and writes **draft** entries for human review. Used for the back catalogue. |
| `import_contributions.py <year> <file.csv>` | For chairs. Takes a CSV with columns `title, authors, type, section, order, abstract, pdf, chroma`, plus the work columns `kind, format, duration, performers, event, venue, date, media_url, research_statement`. Authors are separated by `;`. Writes the entries. This is the kind of export conference systems produce. |

### 5. Docs for future chairs

`docs/adding-proceedings.md` will cover:
- the CSV template, how to run the import, where PDFs go, and how to check the result locally;
- what to collect from artists at submission time: program note, research statement, format, duration, performers, documentation link (and ideally a licence for the documentation);
- how to fill in the year's review statement and `reviewing` map (state the process in the call and in the proceedings, so it can be recorded).

Adding a year becomes: fill in the conference `proceedings:` block, import the CSV, drop in the PDFs, open a PR. CI catches mistakes.

## Execution order

Each year is a small, self-contained job that any fresh session can pick up from the repo alone, so the work can be paused, resumed or run in parallel to suit token quotas.

**Step 1: architecture + 2018 pilot (one session, one PR)**
- Build the collection, layout, list include, the two index pages and the four scripts.
- Add a **PR build check**: a workflow that runs `check_contributions.py` and `jekyll build` on every PR, without deploying. The current workflows only run on pushes to `main`, so PRs get no CI today.
- Write the **per-year runbook** as a repo skill (`.claude/skills/proceedings-year/SKILL.md`), plus a short `CLAUDE.md` with the conventions, so later sessions read the runbook instead of rediscovering the design.
- Do 2018 by following the runbook, which tests the runbook as well as the templates.

**Step 2: merge and check the live site** (tags, `sitemap.xml`, Zotero) before scaling up. The data model is what gets copied into hundreds of files, so it has to be right. Template fixes later are cheap.

**Step 3: one session per year (or small batch), each its own branch and PR off `main`**
- Prompt: "Do ACMC YYYY following the proceedings-year skill". The session drafts entries, then commits and pushes, then splits the PDFs, runs the check and build, and opens a PR.
- It pushes after each step, so a session that runs out of quota can be resumed by a new one from the branch and the PR checklist.
- Each PR touches only `_contributions/acmcYYYY/`, `proceedings/acmcYYYY/`, that year's conference file, and that year's row in `docs/proceedings-status.md`, so years don't conflict.
- PR review checklist: the list matches the TOC, three PDFs spot-checked, and review statuses as the volume states them.
- Keep **at most two year-PRs open at a time**, since review is the bottleneck.

**Year order** (easiest first, so the runbook gets refined before the hard years):
1. 2006, 2005, 2001, 2023 (already split / on the page)
2. 2007, 2008, 2000, 2004, 2009, 2011, 2010 (title lists exist; 2010 needs OCR)
3. 2015, 2016, 2017, 2019, 2014 (no lists; 2014 needs its text layer decoded)
4. 2021, 2022, 2024, 2020 (2020 once its CSV is back)
5. Creative works back catalogue

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
- [ ] 2014 (papers volume + talks/posters volume + 7 concert programmes). **The papers PDF's text layer is garbled** (a font-encoding fault that shifts every letter by 3, e.g. "ZRUWK RI" = "worth of"). Decode it or OCR it before drafting. · [ ] 2015 · [ ] 2016 · [ ] 2017 · [ ] 2019 (+ programme booklet)

**Phase 5: abstract-era years (2020+)**
- [ ] 2021, 2022, 2024 from their volumes; 2020 from its CSV once `_drafts/found/` is back
- **No per-abstract PDF splits** for these years. The text is on the landing page, which is enough for Scholar, and the full volume stays linked.

**Phase 6: creative works back catalogue**
- [ ] Years whose works survive only outside the proceedings: concert lists in Chroma reports, archived conference sites and programmes. Each work gets an entry with at least title, creators, format and the concert it was in, even where no program note survives.

**Phase 7: going forward**
- [ ] `docs/adding-proceedings.md` + CSV template; 2026 is the first year done this way, with research statements requested from artists

**Later**
- [ ] 2002 per-paper originals, 2003, 2012 and the 1990s finds from `_drafts/found/`
- [ ] Revisit DOIs once the pages have been live for a while. If they're wanted, mint ACMA's own DOIs pointing at the landing pages (costs to be budgeted), not Zenodo
- [ ] Long-term preservation, in case the association or GitHub goes away. Current hosting is fine for now. Options for later include a periodic Internet Archive capture or a deposit with a library (e.g. the NLA's web archive, which already holds *Mikropolyphonie*)
- [ ] After launch: check Search Console for indexing; if pages still aren't in Scholar after a few months, use Scholar's publisher support form

## Notes and risks

- **Repo size:** keeping full volumes and adding split copies adds roughly 100 MB to `proceedings/` (currently 244 MB). This is acceptable for an archive repo, and FTP deploy only uploads changed files. Media stays out of git.
- **Scholar timing:** Scholar recrawls slowly. Expect weeks to months before entries appear. Tags must be right the first time, which is why there are pilot years.
- **Scholar and creative works:** Scholar decides for itself what it lists, and it favours entries with substantial text and a PDF. Creative works with a full program note, a research statement and (where printed) a PDF stand the best chance. Whatever Scholar does, each work still has a stable URL, a review statement, a "How to cite" line and tags Zotero can read, so it is citable either way.
- **Review history:** recorded only where the volume (or the call for works) states it. Gaps stay as empty strings and can be filled later from Chroma reports and calls, without guessing.
- **Creator names:** written as given in the volume ("Andrew R. Brown"). Keeping one spelling across years helps Scholar's author profiles, so the validator could warn on near-duplicates.
- **Page boundaries:** a few old volumes may start items mid-page or share pages (common for program notes). These are flagged during review; the split rule is "starts on the item's first page", and items that share a page get no per-item PDF.

## Review terminology found in the volumes

From a text search of every volume (October 2026). These are **provisional** and are checked again per year when the year's entries are drafted.

| `reviewing` | Shown as | Volume wording it maps from |
|---|---|---|
| `full-paper` | Peer reviewed (full paper) | "fully refereed", "peer review of full paper", "(REF)", "Refereed Papers" in years with a full-paper review statement |
| `abstract` | Peer reviewed (abstract) | "peer review by abstract", "selected by abstract", "Refereed Abstracts" |
| `refereed` | Refereed | "Refereed Creative Works", "Refereed Performance Works", "Refereed Artist Talks": refereed, with the basis not stated |
| `invited` | Invited | keynotes, "Invited Speaker" |
| `non-refereed` | Not refereed | "Non-refereed Papers", "Non-refereed Abstracts" |
| `""` | (nothing) | no statement found |

| Year | What the volume says |
|---|---|
| 2000 | Per-paper markers: "* peer review of full paper", "† peer review by abstract" |
| 2001 | "Papers marked (REF) have been fully refereed. The others were selected by abstract." Also Artist Talks, Studio Reports |
| 2002, 2004 | "Refereed Papers" and "Non-refereed Papers" sections |
| 2005 | "Refereed Papers" |
| 2007, 2014, 2017, 2018 | Government statement: "fully refereed papers therefore meet Australian Government requirements for fully-refereed research papers" (HERDC wording) |
| 2008–2010 | "Refereed Papers"; 2010 also "Artist Talk" |
| 2011 | No statement found yet; check the front matter by eye |
| 2015, 2016 | "The peer review process applied to full papers … impartial and independent assessment … by independent, qualified experts". 2015: Refereed Full Papers, Studio Reports, Artist Talks. 2016: Refereed Papers, Creative Works, Artist Talks |
| 2017 | Refereed Papers, Refereed Abstracts, Refereed Artist Talks, Refereed Performance Works |
| 2018 | Refereed Papers, Refereed Creative Works. Non-refereed Abstracts: the contents page says "Non-refereed", but the abstracts section's first page says "Refereed". **Judgement: the contents page is right**, and the section heading is the error |
| 2019 | Refereed Papers, Refereed Creative Works (program notes) |
| 2021, 2024 | No statement found → `""` unless the call for papers says otherwise |
| 2023 | Full papers peer reviewed (published in Chroma) |

## Open questions

None at present.

## Resolved

- 2020+ items: landing page only, no per-abstract PDFs.
- Creative works with no printed note: landing page only, no generated PDF.
- URL shape `/proceedings/acmc2018/<slug>/`: confirmed.
- Types: worked out from the volumes' headings (consistent up to 2020). `section` keeps each volume's wording.
- Review vocabulary: taken from the volumes (above). A `reviewing` key is set only from clear statements, and is an empty string when unknown.
- 2018 abstracts: `non-refereed`, following the contents page. The entries' YAML carries a comment noting that the section heading says "Refereed".
