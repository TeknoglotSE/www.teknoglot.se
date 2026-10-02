#!/usr/bin/env bash
# Full regeneration and verification chain.
#
# Order matters and is not obvious:
#
#   1. extract_* and capture_golden read master's committed docs/, which is the
#      ground truth for permalinks, descriptions, excerpts, counts and orderings
#   2. generate_content turns that into content/
#   3. hugo renders
#   4. the AppleDouble sweep, because this volume regenerates ._* sidecars as
#      files are written and Hugo's ignoreFiles does not apply to static/
#   5. verification
#
# Everything is idempotent. Re-run after changing content or templates.
#
#   ./migration/hugo/tools/build.sh              # build to a scratch dir
#   ./migration/hugo/tools/build.sh --publish    # build into docs/ (destructive)
#
# --publish replaces docs/ with the Hugo output. That is the switch-over step
# and is deliberately a separate, explicit invocation.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$REPO"

TOOLS=migration/hugo/tools
SCRATCH="${SCRATCH:-/private/var/folders/8d/fxh6n6b5075bqpkysnxhc8x00000gn/T/opencode/hugobuild}"
PUBLISH=0
[ "${1:-}" = "--publish" ] && PUBLISH=1

step() { printf '\n=== %s ===\n' "$1"; }

if [ "$PUBLISH" -eq 0 ]; then
  if [ ! -d docs/css ]; then
    echo "FAIL: docs/css is gone, so master's assets are no longer available." >&2
    echo "     The extraction tools read docs/ and cannot run without it." >&2
    exit 1
  fi
fi

step "1/6 golden fixtures and extractions (read master's docs/)"
python3 "$TOOLS/extract_permalinks.py"
node "$TOOLS/extract_descriptions.js"
node "$TOOLS/extract_excerpts.js"
python3 "$TOOLS/capture_golden.py"

step "2/6 generate content/"
python3 "$TOOLS/generate_content.py"

step "3/6 render"
rm -rf "$SCRATCH"
hugo --destination "$SCRATCH" --minify --logLevel warn

step "4/6 sweep AppleDouble sidecars"
# Not cosmetic: without this the output carries 227 junk files, and Hugo's
# ignoreFiles does not cover static/.
find "$SCRATCH" -name '._*' -delete 2>/dev/null || true
echo "remaining: $(find "$SCRATCH" -name '._*' | wc -l | tr -d ' ')"

step "5/6 verify"
python3 "$TOOLS/compare.py" "$SCRATCH" | sed -n '1,20p'
python3 "$TOOLS/check_heading_ids.py" "$SCRATCH" | tail -3

if [ "$PUBLISH" -eq 1 ]; then
  step "6/6 publish into docs/"
  echo "WARNING: this replaces master's committed Hexo output."
  find docs -name '._*' -delete 2>/dev/null || true
  rm -rf docs
  cp -R "$SCRATCH" docs
  # The copy itself can regenerate AppleDouble sidecars on macOS, so sweep
  # after copying as well as during the scratch-build stage above.
  find docs -name '._*' -delete 2>/dev/null || true
  find docs -type d -name '.AppleDouble' -prune -exec rm -rf {} + 2>/dev/null || true
  echo "remaining docs Apple metadata: $(find docs \( -name '._*' -o -name '.DS_Store' -o -name '.AppleDouble' -o -name '__MACOSX' \) | wc -l | tr -d ' ')"
  echo "docs/ now holds $(find docs -name '*.html' | wc -l | tr -d ' ') html files"
else
  step "6/6 skipped (scratch build only; pass --publish to replace docs/)"
  echo "scratch: $SCRATCH"
fi
