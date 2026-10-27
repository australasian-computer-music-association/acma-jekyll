# Missing and recovered content

Much of ACMA's older web content was lost along with the old WordPress site
and the shared hosting it ran on (the `acma.asn.au` and early
`computermusic.org.au` sites, including their `/media/` uploads). This file
records what is missing, what has been recovered, and where links now point.
Please keep it up to date.

Last full link check: October 2026 (`python3 scripts/check_links.py`).

## How dead links are marked in the source

Original URLs are never deleted. Files (PDFs, zips, images) should be brought into this repo; only web pages stay as archive links. Each dead link is rewritten in one of three ways,
and the original stays in an HTML comment so it can be searched for later:

| Situation | What the source looks like |
|---|---|
| An Internet Archive copy exists | `[label](https://web.archive.org/web/…) (archived copy)<!-- original link, dead by 2026: URL -->` |
| No useful archive | `label<!-- dead link removed 2026 (no useful archive): URL -->` |
| Image link to a lost full-size WordPress upload | `![alt](/assets/images/…)<!-- dead link to full-size original (WordPress-era upload, lost): URL -->` |
| Lost image | `<!-- image lost (not in the repo or the Internet Archive): path -->` |

To list them all: `grep -rn "dead link\|original link, dead\|image lost" --include=*.md .`

## Recovered from the Internet Archive into this repo

Downloaded in October 2026 (raw files via `https://web.archive.org/web/<timestamp>id_/<url>`),
checked to be complete, and linked from the conference pages.

| File in this repo | Original URL | Snapshot |
|---|---|---|
| `proceedings/ACMC2014-proceedings-papers.pdf`: **ACMC 2014 refereed papers** (110 pages) | `http://acma.asn.au/media/2014/01/ACMC-2014r1.pdf` | 20160227000627 |
| `proceedings/ACMC2014-concerts/ACMC2014-Concerts-*.pdf`: 7 concert programmes | `http://conference.acma.asn.au/ACMC2014-Concerts-*.pdf` | 2015-02-26 |
| `proceedings/ACMC2019-programme/TENOR-ACMC-2019-Conference-Booklet.pdf` (68 pages) | `http://computermusic.org.au/media/2019/07/…` | 20200229174804 (the 2019 capture is truncated) |
| `proceedings/ACMC2019-programme/TENOR-ACMC-2019-LABS.pdf` | `http://computermusic.org.au/media/2019/07/…` | 20191112054411 |
| `proceedings/ACMC2005-programme/ACMC05_Concert_Program.pdf`, `ACMC05workshops.pdf` | `http://www.acma.asn.au/acmc05/…` | 2006-08-19 |
| `assets/archives/ACMC2001-Waveform-call-for-submissions.pdf` | `http://www.acma.asn.au/2001Waveform.PDF` | 20010623065814 |
| `assets/archives/templates/ACMC-Templates-2011.zip` | `http://www.acma.asn.au/ACMC-Templates.zip` | 20110525225215 |
| `assets/archives/templates/ACMC2009_Paper_Templates.zip` (the 2010 zip is byte-identical) | `http://www.acma.asn.au/ACMC2009_Paper_Templates.zip` | 20090912041956 |
| `assets/images/Melbourne_Night_Panorama-1024x196.jpg` | `http://acma.asn.au/media/2014/03/…` | 20140904181137 |

Not copied, on purpose:

- `ACMC2005.zip` and `ACMC06.zip`: each holds exactly the PDFs already in
  `proceedings/ACMC2005-proceedings/` and `proceedings/ACMC2006-proceedings/`
  (checked file by file). The pages link every paper individually and still
  link the archived zips.
- ACMC 2019 full-resolution proceedings (63 MB,
  [20200229174641](https://web.archive.org/web/20200229174641/http://computermusic.org.au/media/2019/12/ACMC2019Proceedings.pdf)):
  the repo has the 11 MB reduced version.

Already safe in the repo: Chroma 1–37, AGM minutes, constitution,
mailing-list archive 1999–2019, ACMC 2000–2010 proceedings.

## Other fixes

- ACMC 2005 and 2006: every paper in `proceedings/ACMC2005-proceedings/` and `proceedings/ACMC2006-proceedings/` is linked individually, with author and title from the proceedings.
- `competitions.md`: competition contract now links to `/assets/minutes/ACMAcompetition.pdf`.
- Australian Music Centre: `amcoz.com.au` replaced with `australianmusiccentre.com.au`.
- ACMC 2014: the "Artist Talks, Posters, Performances" volume (`ACMC-2014r2.pdf`) is `proceedings/ACMC2014-proceedings.pdf`.

## Pointed at the Internet Archive

| Page(s) | Original URL |
|---|---|
| ACMC 2005 | `http://computermusic.org.au/acmc05/ACMC2005.zip` |
| ACMC 2006 | `/media/2006/ACMC06.zip` |
| ACMC 2011 | `http://conference.acma.asn.au/ACMC_11.html` |
| ACMC 2012 | `http://acmc2012.net/` |
| ACMC 2013 | `http://acma.asn.au/icmc-2013/scholarships/` |
| ACMC 2014, 2014 news posts | `http://conference.acma.asn.au` (and `conference.computermusic.org.au`, which was never archived; it points at the same archived site) |
| ACMC 2014 | call for papers on `conference.acma.asn.au/ocs/…` |
| ACMC 2015, 2015 news post | `http://acmc2015.net/` |
| ACMC 2016, 2016 news post | `http://www.sonicenvironments.org/` |
| ACMC 2017, 2017 news post | `https://acmc2017.com` |
| 2021 news post | `https://acmc21.art` |
| 2022 news post | `https://www.acmc2022.com` |
| ACMC 2023 | `https://uncleftwords.com/`, `https://www.foxcontrolmusic.com/bio` (presenter bios) |
| Community, Links | Clatterbox, NFRAM (ANU), Australian Sound Design Project (Melbourne), NoizeMaschin!! |

## Lost (no archive found)

| Page | What | Original URL |
|---|---|---|
| ACMC 2014 | Friday 5:15pm concert programme PDF (the concert is listed on page 40 of `proceedings/ACMC2014-proceedings.pdf`) | `conference.acma.asn.au/ACMC2014-Concerts-Friday1715.pdf` |
| ACMC 2013 | #ICMC2013 tweet archive page | `http://acma.asn.au/icmc-2013/icmc2013tweets/` |
| ACMC 2018 | 2018 submission templates | `http://www.computermusic.org.au/ACMC-Templates.zip` |
| 2013 news post | Perth banner image | `/assets/images/perth-city-sunset-870x230.jpg` |
| 2013–2018 news posts | 18 full-size originals of images whose thumbnails survive | `http://computermusic.org.au/media/…`, `http://acma.asn.au/media/…` |
| Community, Links | University programme pages that have moved (QUT, Waikato, Western Sydney); unlinked rather than archived | see comments in `community.md` and `links.md` |

## Links the checker can't verify

These sites block automated requests and report 400/403/520, but work in a browser:
Facebook, Twitter/X, monash.edu (TENOR 2019 pages), msa.org.au (2018 MSA registration), timeanddate.com.

## Old URLs that redirect

Conference pages answer at both slug styles (`/conferences/acmc-2019/` and
`/conferences/acmc2019/`) and at the WordPress-era `/wordpress/conferences/…`
paths. News posts answer at the WordPress-era `/news/<slug>/`. These are set
with `redirect_from` in each page's front matter.

The build turns them into real 301 redirects in `.htaccess` (generated from
`/.htaccess` in this repo), which the live LiteSpeed host reads. jekyll-redirect-from
also writes HTML redirect pages, which act as a fallback (e.g. on GitHub Pages).
The same `.htaccess` sends `http://` and `www.` to `https://computermusic.org.au`
and uses the site's own 404 page.

## Note on git and PDFs

If your global gitignore excludes `*.pdf`, this repo's `.gitignore` re-includes
them (`!*.pdf`), so new PDFs show up in `git status` as normal.
