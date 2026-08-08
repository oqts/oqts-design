#!/usr/bin/env bash
# Download candidate mono fonts as TTF for the OQTS wordmark exploration.
# Google Fonts' CSS2 API serves TTF (not woff2) to legacy user agents, so we
# ask as Mozilla/4.0 and pull the raw font files it points at. TTF suits both
# the browser preview and fontconfig, so server-side rendering can verify it.
set -uo pipefail
DEST="$(cd "$(dirname "$0")/.." && pwd)/fonts"
mkdir -p "$DEST"
UA="Mozilla/4.0"

fetch_gf() {
  local family_url="$1" slug="$2"
  local css
  css=$(curl -sS --max-time 30 -A "$UA" "https://fonts.googleapis.com/css2?family=${family_url}") || {
    echo "FAIL(css) $slug"; return 1; }
  local urls
  urls=$(grep -oE 'https://[^)]*\.ttf' <<<"$css" | sort -u)
  if [[ -z "$urls" ]]; then echo "FAIL(nourl) $slug"; return 1; fi
  local i=0
  while read -r u; do
    [[ -z "$u" ]] && continue
    curl -sS --max-time 30 -o "${DEST}/${slug}-${i}.ttf" "$u" || echo "FAIL(dl) $slug-$i"
    i=$((i+1))
  done <<<"$urls"
  echo "OK $slug ($i files)"
}

# family URL spec                         slug
fetch_gf "IBM+Plex+Mono:wght@400;500;600" ibmplexmono
fetch_gf "Space+Mono:wght@400;700"        spacemono
fetch_gf "JetBrains+Mono:wght@400;500;700" jetbrainsmono
fetch_gf "Courier+Prime:wght@400;700"     courierprime
fetch_gf "Anonymous+Pro:wght@400;700"     anonymouspro
fetch_gf "Inconsolata:wght@400;600"       inconsolata
fetch_gf "Source+Code+Pro:wght@400;600"   sourcecodepro
fetch_gf "DM+Mono:wght@400;500"           dmmono
fetch_gf "Share+Tech+Mono"                sharetechmono
fetch_gf "VT323"                          vt323
fetch_gf "Major+Mono+Display"             majormono
fetch_gf "Martian+Mono:wght@400;600"      martianmono
fetch_gf "Cutive+Mono"                    cutivemono
fetch_gf "Nova+Mono"                      novamono
fetch_gf "Azeret+Mono:wght@400;500"       azeretmono
fetch_gf "Red+Hat+Mono:wght@400;600"      redhatmono
fetch_gf "Fira+Mono:wght@400;500;700"     firamono
fetch_gf "Geist+Mono:wght@400;500"        geistmono
fetch_gf "Spline+Sans+Mono:wght@400;600"  splinesansmono
fetch_gf "Overpass+Mono:wght@400;600"     overpassmono
fetch_gf "B612+Mono:wght@400;700"         b612mono
# serif companions for the lockups
fetch_gf "EB+Garamond:wght@400;500;600"   ebgaramond
fetch_gf "Spectral:wght@300;400;600"      spectral
fetch_gf "Inter:wght@400;500"             inter

# Latin Modern Mono — the LaTeX / Computer Modern typewriter face (CTAN, not Google).
# This is the literal typeface of academic mathematics papers.
for f in lmmono10-regular lmmonolt10-bold; do
  curl -sS --max-time 40 -o "${DEST}/latinmodernmono-${f}.otf" \
    "https://mirrors.ctan.org/fonts/lm/fonts/opentype/public/lm/${f}.otf" \
    && echo "OK latinmodernmono ${f}" || echo "FAIL latinmodernmono ${f}"
done

echo "--- downloaded ---"
ls -S "$DEST" | head -60
echo "--- count/size ---"
ls "$DEST" | wc -l
du -sh "$DEST"
