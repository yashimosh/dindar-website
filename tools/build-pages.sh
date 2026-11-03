#!/usr/bin/env bash
# Build the public site into dist/ (used by the GitHub Action, also fine to run by hand).
#   1. regenerate the 12 pages + 404 from tools/site/content_*.json
#   2. build the CSS and stamp the cache hashes
#   3. copy only the public files into dist/ (same rules as tools/deploy.sh)
# Needs Python 3.12 (Pillow 10.4 and uharfbuzz 0.39 have no wheels for newer versions) and Node 20+.
# PYTHON=/path/to/python overrides the interpreter; SKIP_PIP=1 and SKIP_NPM_CI=1 skip the installs (local testing).
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${PYTHON:-python3}"
if [ -z "${SKIP_PIP:-}" ]; then
  "$PY" -m pip install --quiet -r tools/requirements-build.txt
fi
"$PY" tools/site/generate.py
if [ -z "${SKIP_NPM_CI:-}" ]; then
  npm ci --no-audit --no-fund
fi
npm run build
rm -rf dist
mkdir dist
tar -cf - \
  --exclude=./dist --exclude=./tools --exclude=./print --exclude=./docs --exclude=./node_modules \
  --exclude=./.git --exclude=./.github --exclude=./.wrangler --exclude=./.claude --exclude=./.pages.yml \
  --exclude='*.ttf' --exclude='*.otf' --exclude=./README.md --exclude=./package.json \
  --exclude=./package-lock.json --exclude=./build.js --exclude=./tailwind.config.js \
  --exclude=./css/tailwind.src.css --exclude=./.assetsignore --exclude=./.gitignore . | tar -xf - -C dist
if find dist \( -name '*.ttf' -o -name '*.otf' -o -name '*.py' \) | grep -q . || [ -e dist/tools ]; then
  echo "refusing: font or tool files ended up in dist/" >&2
  exit 1
fi
echo "dist/ ready: $(find dist -type f | wc -l) files"
