# ACMA website: notes for Claude sessions

Jekyll site for the Australasian Computer Music Association, deployed by
GitHub Actions on pushes to `main` (GitHub Pages and FTP). Layouts, includes
and CSS live in this repo (Pico CSS plus `assets/css/main.css`).

## Proceedings

- Every ACMC paper, abstract and creative work is one file in
  `_contributions/ACMCYYYY-proceedings/<slug>.md`, published at
  `/proceedings/ACMCYYYY-proceedings/<slug>.html` with Google Scholar tags
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

- Record what you find in an issue: a lost programme or schedule, a name or
  detail someone supplies, a review, and anything left unknown, skipped or not
  entered. Do this even when you're about to act on it, so the gaps stay
  visible and anyone can fill them in later (see #29–#35 for examples).
- Anything you bring into the repo goes through a pull request, never
  straight to `main`.
- Slugs (file names) are permanent URLs: never rename published entries.
- An item's own PDF lives in the same folder as its page,
  `proceedings/ACMCYYYY-proceedings/` (Scholar's same-directory rule; the
  checker enforces it). Existing PDFs there keep their names and addresses;
  new ones are `<slug>.pdf`. Don't move published PDFs.
- PDFs and zips under `proceedings/` that aren't an entry's own `pdf` (whole
  volumes, front matter, section PDFs) are kept out of the sitemap by
  `_plugins/contributions.rb`.
- Record review status only from what a volume states; `""` means unknown.
- Creative works are first-class research outputs: give them the same care as
  papers.
- Australian English. Commit messages explain why, not just what.
