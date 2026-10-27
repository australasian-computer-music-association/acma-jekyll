# ACMA website: notes for Claude sessions

Jekyll site for the Australasian Computer Music Association, deployed by
GitHub Actions on pushes to `main` (GitHub Pages and FTP). Layouts, includes
and CSS live in this repo (Pico CSS plus `assets/css/main.css`).

## Proceedings

- Every ACMC paper, abstract and creative work is one file in
  `_contributions/acmcYYYY/<slug>.md`, published at
  `/proceedings/acmcYYYY/<slug>/` with Google Scholar tags
  (`_includes/citation-meta.html`). Conference pages list them with
  `{% include contribution-list.html %}`.
- Design and decisions: `docs/scholar-plan.md` (issue #9). Fields and the
  chairs' process: `docs/adding-proceedings.md`. What we hold for each year:
  `docs/proceedings-status.md`.
- To do a year, follow the `proceedings-year` skill
  (`.claude/skills/proceedings-year/SKILL.md`).
- Always run `python3 scripts/check_contributions.py` before committing
  entries. CI runs it on PRs and before deploys.

## Conventions

- Slugs (file names) are permanent URLs: never rename published entries.
- An item's own PDF lives in its page's folder,
  `proceedings/acmcYYYY/<slug>/<slug>.pdf` (Scholar's same-directory rule).
  Move an existing PDF only with `pdf_moved_from:` set on the entry, which
  generates a 301 in `.htaccess`.
- Whole volumes and multi-item PDFs live under `proceedings/ACMC*`, which is
  kept out of the sitemap. Only per-item PDFs carry `citation_pdf_url`.
- Record review status only from what a volume states; `""` means unknown.
- Creative works are first-class research outputs: give them the same care as
  papers.
- Australian English. Commit messages explain why, not just what.
