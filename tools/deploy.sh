#!/usr/bin/env bash
# Deploy only the public site. Cloudflare Pages ignores .assetsignore, so a plain
# `wrangler pages deploy .` would publish tools/ (including licensed font files kept locally).
# This copies just the site into a temp folder and deploys that.
set -euo pipefail
cd "$(dirname "$0")/.."
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
rsync -a \
  --exclude tools --exclude print --exclude node_modules --exclude .git --exclude .wrangler \
  --exclude .claude --exclude '*.ttf' --exclude '*.otf' --exclude README.md \
  --exclude package.json --exclude package-lock.json --exclude build.js \
  --exclude tailwind.config.js --exclude css/tailwind.src.css --exclude .assetsignore \
  ./ "$STAGE/"
if find "$STAGE" \( -name '*.ttf' -o -name '*.otf' -o -name '*.py' \) | grep -q .; then
  echo "refusing to deploy: font or tool files in the staging folder" >&2; exit 1
fi
npx wrangler pages deploy "$STAGE" --project-name dindar-ahmed --branch main
