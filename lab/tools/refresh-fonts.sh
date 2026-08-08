#!/usr/bin/env bash
# Re-measure every font in fonts/ and regenerate fonts.css + catalog.js.
# Run this after dropping a new .ttf/.otf into fonts/ -- wordmark.html picks it
# up automatically, no HTML editing required.
set -euo pipefail
cd "$(dirname "$0")/.."
echo "1/3  measuring cap height, stem width, O aspect ..."
uv run --with fonttools --with pillow python tools/analyse-fonts.py | tail -3
echo "2/3  classifying Q shape ..."
uv run --with pillow python tools/classify-q.py | head -3
echo "3/3  building fonts.css + catalog.js ..."
uv run --with fonttools python tools/build-catalog.py
echo "done - reload the page"
