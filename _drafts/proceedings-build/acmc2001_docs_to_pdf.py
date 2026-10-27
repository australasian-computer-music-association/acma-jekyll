#!/usr/bin/env python3
"""Convert the ACMC 2001 (WAVEFORM) Word 2000 .doc files to PDF.

The 2001 proceedings only survive as the Word files Gordon Monro used to
assemble the printed book (proceedings/ACMC2001-proceedings.zip). Modern Word
often refuses to open them, but LibreOffice reads them fine. This script:

  1. unzips the archive (ignoring the __MACOSX resource-fork junk),
  2. converts every .doc to PDF with headless LibreOffice,
  3. strips the blank verso/recto filler pages the book layout inserted,
  4. writes one PDF per item to proceedings/ACMC2001-proceedings/, named by
     its start page in the printed contents, and
  5. merges everything in book order into proceedings/ACMC2001-proceedings.pdf.

Requires: LibreOffice (`brew install --cask libreoffice`) and pypdf.
Usage:    python3 -I _drafts/proceedings-build/acmc2001_docs_to_pdf.py
"""

import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from pypdf import PdfReader, PdfWriter

REPO = Path(__file__).resolve().parents[2]
ZIP = REPO / "proceedings" / "ACMC2001-proceedings.zip"
OUT_DIR = REPO / "proceedings" / "ACMC2001-proceedings"
FULL_PDF = REPO / "proceedings" / "ACMC2001-proceedings.pdf"

# (source .doc stem, start page in the printed contents) in book order.
# Section dividers and front matter have no page number of their own.
# Bandt & Paine (p. 1) and Doornbusch (p. 25) are not in the archive.
FRONT = ["ZTitlePage", "ZContents", "ZPaperHead"]
PAPERS = [
    ("BrownARef", 9),
    ("CabreraD", 17),
    ("FraiettaA", 43),
    ("FumarolaA", 49),
    ("Gebhardt.N", 51),
    ("HelyerN", 53),
    ("KCaleb", 55),
    ("Mcilwain.P", 57),
    ("PaineG", 67),
    ("RichardsD", 75),
    ("SchiemerG", 81),
    ("WhitelawM", 91),
    ("WoollerN", 93),
]
ART_TALKS = [
    ("Art_BerryR", 99),
    ("Art_BrownCC", 100),
    ("Art_GoodwinR", 101),
    ("Art_Narushima", 102),
    ("Art_NezvanovaN", 103),
    ("Art_StevensonI", 105),
    ("Art_YuilleJ", 106),
]
STUDIO_REPORTS = [
    ("Stud_BrownA", 109),
    ("Stud_ElmslyJ", 110),
    ("Stud_KnowlesJ", 111),
    ("Stud_McilwaineP", 112),
]

# A filler page carries only the running header/footer: a page number, the
# "ACMA Proceedings 2001" footer, and possibly a short running title.
FOOTERS = re.compile(
    r"^(\d+|ACMA Proceedings 2001( \d+)?|"
    r"Proceedings of the 2001 ACMA Conference, University of Western Sydney)$"
)


def is_filler(page):
    contents = page.get_contents()
    if contents is not None and re.search(rb"\bDo\b", contents.get_data()):
        return False  # draws an image or other XObject
    lines = [l.strip() for l in (page.extract_text() or "").splitlines()]
    body = [l for l in lines if l and not FOOTERS.match(l)]
    return len(body) <= 1 and sum(map(len, body)) < 100


def clean(pdf_path):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    dropped = []
    for i, page in enumerate(reader.pages, 1):
        if is_filler(page):
            dropped.append(i)
        else:
            writer.add_page(page)
    return writer, dropped


def out_name(stem, start):
    return f"{start:03d}-{stem.replace('.', '')}.pdf"


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        src = tmp / "doc"
        pdf = tmp / "pdf"
        src.mkdir()
        with zipfile.ZipFile(ZIP) as z:
            for name in z.namelist():
                if name.endswith(".doc") and not name.startswith("__MACOSX"):
                    (src / Path(name).name).write_bytes(z.read(name))

        subprocess.run(
            ["soffice", "--headless",
             f"-env:UserInstallation=file://{tmp}/lo-profile",
             "--convert-to", "pdf", "--outdir", str(pdf),
             *sorted(map(str, src.glob("*.doc")))],
            check=True, stdout=subprocess.DEVNULL,
        )

        OUT_DIR.mkdir(exist_ok=True)
        full = PdfWriter()

        def add(stem, start=None):
            writer, dropped = clean(pdf / f"{stem}.pdf")
            for page in writer.pages:
                full.add_page(page)
            if start is None:
                print(f"  {stem}: {len(writer.pages)} pp (front matter)")
                return
            dest = OUT_DIR / out_name(stem, start)
            writer.write(dest)
            note = f", dropped filler {dropped}" if dropped else ""
            print(f"  {dest.name}: {len(writer.pages)} pp{note}")

        for stem in FRONT:
            add(stem)
        for stem, start in PAPERS:
            add(stem, start)
        add("ZArtTalks")
        for stem, start in ART_TALKS:
            add(stem, start)
        add("ZStudioReps")
        for stem, start in STUDIO_REPORTS:
            add(stem, start)

        full.add_metadata({
            "/Title": "WAVEFORM 2001: Proceedings of the Australasian "
                      "Computer Music Conference 2001",
            "/Author": "Australasian Computer Music Association",
        })
        full.write(FULL_PDF)
        print(f"  {FULL_PDF.name}: {len(full.pages)} pp")


if __name__ == "__main__":
    sys.exit(main())
