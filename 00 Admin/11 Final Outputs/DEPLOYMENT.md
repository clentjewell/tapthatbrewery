# Delivery site — deployment notes

The client-facing 3D Process site, deployed to Cloudflare Pages.

| | |
|---|---|
| **Live** | https://tapthat-3d-process.pages.dev |
| **Password** | `tapthat2026` |
| **Pages project** | `tapthat-3d-process` (production branch `main`) |
| **Account** | Jewell Projects Cloudflare account |

## Routes

| Path | Page |
|---|---|
| `/` | **The complete pack** — all 65 documents rendered on one page, with a phase-grouped contents sidebar and a filter box |
| `/summary` | **The delivery summary** — the ten-section overview: what's in the set, what wasn't done, what's blocking sign-off |
| `/__signout` | Clears the session cookie |

The two pages cross-link, so the client can enter at either.

## Files

| File | Purpose |
|---|---|
| `site/index.html` | The complete pack. **Generated — do not hand-edit.** Built from the 65 markdown documents by `build/build_pack.py` |
| `site/summary.html` | The delivery summary. Generated from `delivery-summary.html` (same page, minus the doctype wrapper so it can also publish as an artifact) |
| `site/_worker.js` | Password gate + asset serving (Pages advanced mode: a root `_worker.js` takes over all routing) |
| `build/build_pack.py` | Converts every catalogue document to HTML and assembles the pack |
| `build/pack_template.html` | The pack's shell — design system, sidebar, scripts |

## Rebuild the pack after editing documents

```bash
python3 -m pip install --quiet markdown
python3 "00 Admin/11 Final Outputs/build/build_pack.py"
```

The script discovers documents by catalogue number from the filename prefix (`23__…`), maps the four legacy-named Discover anchors (`D02`→04, `D03`→09, `D05`→13, `D06`→20), strips each document's H1, demotes remaining headings one level, and wraps tables for horizontal scroll. It prints any catalogue number it could not find a file for.

## Rebuild the summary after editing it

Edit `delivery-summary.html`, then regenerate `site/summary.html` by wrapping it in a doctype/head/body shell (the artifact publish path strips these, the Pages path needs them).

## Redeploy

```bash
cd "00 Admin/11 Final Outputs/site"
npx wrangler pages deploy . --project-name tapthat-3d-process --branch main --commit-dirty=true
```

Requires `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` in the environment. Keep this file **outside** `site/` — anything inside that directory is uploaded as a public asset.

Cloudflare's edge caches aggressively. After a deploy that removes a file, the old copy can still answer for a few minutes; confirm with a cache-buster query (`?cb=123`) before concluding something is wrong, or purge the build cache via the API.

## The password gate

A **soft gate**, not security: the password is shared with the client, and the reference pack this mirrors prints its own password on screen. It keeps the pack out of search results and away from casual visitors. Nothing behind it is confidential beyond the engagement itself.

- Signed cookie (`tt_session`) — HMAC-SHA256 over the expiry, 7-day life, so it can't be forged by editing the cookie
- Wrong password re-renders the gate with an error
- `next` is restricted to same-origin paths, so the form can't be used as an open redirect
- Every response carries `noindex, nofollow, noarchive, nosnippet`

To change the password without editing code, set a `PACK_PASSWORD` environment variable on the Pages project (Settings → Environment variables); the worker prefers it over the built-in default.

## Custom domain

Not configured. To put this on a Jewell Projects domain, add it under the Pages project's Custom domains tab — DNS is already in Cloudflare.
