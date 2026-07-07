#!/usr/bin/env bash
# Build the ACMC 2023 proceedings PDF.
#
#   ./build.sh          regenerate source from the webpage, render, and install
#                       the PDF into ../../proceedings/
#   ./build.sh --no-gen skip step 1 (use when you've only edited cover.tex)
#
# Requires: python3, pandoc, xelatex.
set -euo pipefail

cd "$(dirname "$0")"

SRC="ACMC2023-proceedings.md"
OUT="ACMC2023-proceedings.pdf"
DEST="../../proceedings/${OUT}"

if [[ "${1:-}" != "--no-gen" ]]; then
  echo "==> Regenerating ${SRC} from _conferences/acmc2023.md"
  python3 make_proceedings.py
fi

echo "==> Rendering ${OUT}"
pandoc "${SRC}" -o "${OUT}" \
  --pdf-engine=xelatex --toc \
  --include-before-body=cover.tex

echo "==> Installing to ${DEST}"
cp "${OUT}" "${DEST}"

echo "Done. Note: proceedings PDFs are covered by a global *.pdf gitignore —"
echo "commit with:  git add -f ${DEST}"
