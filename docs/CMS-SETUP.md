# Self-service editing for dindarahmed.com: setup

Goal: Dindar changes text, client logos and photos himself in a web form; saving publishes the site.
Nothing here replaces `tools/deploy.sh`, which still works for a manual deploy.

## How it fits together
1. **Pages CMS** (app.pagescms.org, open source, free to use as far as its docs say; check limits) edits files in this GitHub repo using the config in `.pages.yml`. It writes commits, no database of its own.
2. A commit on `main` starts **.github/workflows/deploy.yml**, which runs `tools/build-pages.sh` (regenerate pages from `tools/site/content_*.json`, build CSS, stage the public files into `dist/`) and publishes `dist/` to the existing Cloudflare Pages project `dindar-ahmed` with a pinned Wrangler (4.114.0).
3. The forms are generated from the content files: `python3 tools/cms/make_pages_yml.py` (run it again if a section is added to the content files).

## What stays developer-only
- `tools/site/generate.py`, `tools/site/nav_labels.json` (menu labels), CSS, JS, layout, fonts.
- `assets/data/clients.json` is now the single source for logos; `generate.py` only creates it if it is missing, so a rebuild never overwrites edits.

## Steps for Yash (each is an account action)
1. **Merge** branch `cms-editor` into `main` (open a PR from it, nothing is pushed yet).
2. **GitHub**: Settings, Collaborators, add Dindar with *Write* access (he needs a free GitHub account). The repo is public.
3. **Cloudflare**: My Profile, API Tokens, create a token with the Pages edit permission (not the account-wide token in Bitwarden). Note the Account ID.
4. **GitHub secrets** on the repo: `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`. Until both exist the workflow builds and skips publishing.
5. **Pages CMS**: sign in at app.pagescms.org with GitHub, add the repo (it asks to install its GitHub App), open it, check that the five entries load.
6. **Test with Dindar**: change one word in the English text, Save, watch the Actions run, reload the site; then change it back.

If you prefer Cloudflare's own Git build instead of GitHub Actions: an existing Direct Upload Pages project cannot be switched to Git, so it would need a new Pages project plus moving the domain. Not recommended.

## Known limits (honest list)
- **Not tested in the real Pages CMS yet**: the config parses as YAML and covers every key of the five JSON files, but the editor itself needs the repo on GitHub with the app installed. Syntax follows pagescms.org/docs; the docs did not confirm whether unlisted keys are kept on save, so every key is listed on purpose.
- Images in forms are file names: upload under *Photos* (or *Client logos*), then type the name.
- The same sentence exists in four language files; he must edit each one.
- Adding a list item (a case study, a reel) in one language needs the same item in the other three.
- Pages CMS rewrites the JSON files in its own formatting (diff noise, same content).
- Deleting a logo from `clients.json` leaves the image file in `assets/img/clients/`.
