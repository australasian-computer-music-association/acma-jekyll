#!/usr/bin/env python3
"""Check every link and image in the built site.

Usage (after `bundle exec jekyll build`):

    python3 scripts/check_links.py            # report failing links
    python3 scripts/check_links.py --json out.json

Internal links are checked against _site/. External links are fetched
(HEAD, falling back to GET). Links to web.archive.org are checked one at a
time because the Internet Archive refuses bursts of requests.

Some sites (Facebook, Twitter/X, monash.edu, msa.org.au, timeanddate.com)
block automated requests, so 400/403/520 from them usually means "alive".
Dead links are recorded in docs/missing-content.md.
"""
import argparse
import concurrent.futures as cf
import html
import json
import os
import re
import ssl
import time
import urllib.parse
import urllib.request

SITE_URL = "https://computermusic.org.au"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
BOT_BLOCKERS = re.compile(r"facebook\.com|twitter\.com|monash\.edu|msa\.org\.au|timeanddate\.com")


def collect(root):
    links = {}
    for dirpath, _, files in os.walk(root):
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(dirpath, name)
            text = open(path, encoding="utf-8", errors="replace").read()
            if "<title>Redirecting&hellip;</title>" in text:
                continue
            page = "/" + os.path.relpath(path, root).replace("index.html", "")
            text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
            text = re.sub(r"<script.*?</script>", "", text, flags=re.S)
            if "<main" in text:
                text = text.split("<main", 1)[1].split("</main>", 1)[0]
            for url in re.findall(r'(?:href|src)="([^"]+)"', text):
                url = html.unescape(url)
                if url.startswith(("mailto:", "#", "javascript:", "tel:")):
                    continue
                if not url.startswith(("http://", "https://")):
                    url = urllib.parse.urljoin(SITE_URL + page, url)
                links.setdefault(url.split("#")[0], set()).add(page)
    return links


def check(url, root):
    if url.startswith(SITE_URL + "/"):
        path = urllib.parse.unquote(urllib.parse.urlparse(url).path).lstrip("/")
        full = os.path.join(root, path)
        found = os.path.isfile(full) or os.path.isfile(os.path.join(full, "index.html"))
        return 200 if found else 404, ""
    status, detail = 0, ""
    for method in ("HEAD", "GET"):
        try:
            request = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
            response = urllib.request.urlopen(request, timeout=60, context=ssl.create_default_context())
            return response.status, ""
        except urllib.error.HTTPError as e:
            status, detail = e.code, ""
        except Exception as e:
            status, detail = 0, f"{type(e).__name__}: {e}"[:100]
    return status, detail


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", default="_site")
    parser.add_argument("--json")
    args = parser.parse_args()

    links = collect(args.site)
    archive = [u for u in links if "web.archive.org" in u]
    others = [u for u in links if "web.archive.org" not in u]
    results = {}
    with cf.ThreadPoolExecutor(12) as pool:
        for url, result in zip(others, pool.map(lambda u: check(u, args.site), others)):
            results[url] = result
    for url in archive:
        results[url] = check(url, args.site)
        time.sleep(5)

    failing = sorted(u for u, (status, _) in results.items() if not 200 <= status < 400)
    for url in failing:
        status, detail = results[url]
        note = " (site blocks bots; probably fine)" if BOT_BLOCKERS.search(url) else ""
        print(f"{status} {url}{note} {detail}".rstrip())
        for page in sorted(links[url]):
            print(f"      on {page}")
    print(f"\n{len(links)} links checked, {len(failing)} failing")

    if args.json:
        with open(args.json, "w") as f:
            json.dump([{"url": u, "status": s, "detail": d, "pages": sorted(links[u])}
                       for u, (s, d) in sorted(results.items())], f, indent=1)


if __name__ == "__main__":
    main()
