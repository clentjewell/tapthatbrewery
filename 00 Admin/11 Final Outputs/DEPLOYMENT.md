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
| `/` | **The pack landing page** — hero, the numbers, and a phase-grouped card index of all 78 documents |
| `/<slug>` | **One page per document** — e.g. `/paid-media-launch`, `/discover-summary`. Same sidebar, prev/next at the foot |
| `/deck` | **The client deck** — 13 slides, keyboard or click navigation, deep-linkable by `#n`, prints to PDF. Generated from `06 Presentations/deck_content.py`, the same source as the .pptx |
| `/on-a-page-overall`<br>`/on-a-page-discover`<br>`/on-a-page-design`<br>`/on-a-page-deploy` | **The four sheets** — one for the whole engagement plus one per phase — each phase distilled to one A3 landscape sheet. Fit / full-size / print controls |
| `/summary` | **The delivery summary** — the ten-section overview: what's in the set, what wasn't done, what's blocking sign-off |
| `/__signout` | Clears the session cookie |

The two pages cross-link, so the client can enter at either.

## Files

| File | Purpose |
|---|---|
| `site/index.html` | The landing page. **Generated — do not hand-edit.** |
| `site/<slug>.html` | One per document, 78 of them. **Generated — do not hand-edit.** Built from the markdown document set by `build/build_pack.py` |
| `site/summary.html` | The delivery summary. Generated from `delivery-summary.html` (same page, minus the doctype wrapper so it can also publish as an artifact) |
| `site/_worker.js` | Password gate + asset serving (Pages advanced mode: a root `_worker.js` takes over all routing) |
| `build/build_pack.py` | Converts every catalogue document to HTML and assembles the pack |
| `build/pack_template.html` | The shared page shell — design system, sidebar, scripts. Placeholders: `{{TITLE}}`, `{{NAV}}`, `{{MAIN}}`, `{{TOTAL}}` |
| `build/oap.css` | The A3 sheet framework, scoped to `.oap`. Appended into the shell's `<style>` at build time |
| `build/oap/{discover,design,deploy}.html` | The three sheets, **hand-authored** — not generated from markdown. Edit these directly |

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

## Branding

The site is a **Jewell Projects deliverable**, so it carries the JP house identity, not the client's:

| | |
|---|---|
| Typeface | Poppins (single family, per `jp-brand-document`) |
| Ground | Cream `#FAF8F4`, ink `#111111`, secondary `#666666`, rule `#D4D2D0` |
| Accent | JP blue `#0066FF` — 4.56:1 on cream, passes AA. On dark grounds it drops to 3.74:1, so dark bands use a lightened `#5B8CFF` (5.72:1) |
| Dark bands | Maxxim dark `#0E171F` |
| Marks | Jewell wordmark leads the sidebar lockup; the Tap That badge is the client mark (sidebar roundel + gate) |

Per the JP spec there are **no icons, emoji or decorative unicode glyphs** anywhere — sign-off is marked with the word "Sign-off", not a symbol.

Note the separation: this is the *delivery vehicle's* branding. The client's own palette (green `#14361D`, gold `#CE9A49`) is documented inside Brand Guidelines (#34) as content, and must not be swapped to JP colours.

## The password gate

A **soft gate**, not security: the password is shared with the client, and the reference pack this mirrors prints its own password on screen. It keeps the pack out of search results and away from casual visitors. Nothing behind it is confidential beyond the engagement itself.

- Signed cookie (`tt_session`) — HMAC-SHA256 over the expiry, 7-day life, so it can't be forged by editing the cookie
- Wrong password re-renders the gate with an error
- `next` is restricted to same-origin paths, so the form can't be used as an open redirect
- Every response carries `noindex, nofollow, noarchive, nosnippet`

To change the password without editing code, set a `PACK_PASSWORD` environment variable on the Pages project (Settings → Environment variables); the worker prefers it over the built-in default.

## Custom domain

Not configured. To put this on a Jewell Projects domain, add it under the Pages project's Custom domains tab — DNS is already in Cloudflare.

## Routing note

Cloudflare Pages resolves an extensionless path to its `.html` file, so `/paid-media-launch`
serves `site/paid-media-launch.html`. The sidebar links use the extensionless form. Slugs are
the Maxxim taxonomy slugs, so a document's URL matches its filename in `tap-that-brewery/memory/generated/`. Three had drifted (`okrs`, `brand-copy-workbook`, `activation-plan`) and were realigned on 20 Aug — the taxonomy slug is canonical.

An unknown path falls through to the landing page rather than a 404. Harmless for a gated client pack, but it means a typo'd URL looks like it worked.

The pack was a single continuously-scrolling page until 20 August 2026. It is now one page per
document: the largest page is ~45 KB against the old 712 KB, and a document's URL can be sent
to someone on its own.

## The on-a-page sheets

Four A3-landscape sheets — the whole engagement, plus one per phase, at `/on-a-page-<phase>`. Unlike every other page
these are hand-written HTML fragments in `build/oap/`, because a sheet is a layout, not a
document — the grid placement carries as much meaning as the words.

- Sheet size is a true **420mm × 297mm**, so `@page { size: A3 landscape }` prints at 1:1.
- On screen the sheet is scaled to the content column by a small script; **Full size** switches
  to a scrolling 100% view, **Print A3** calls `window.print()`.
- Layout is a 12-column grid on `.canvas`, with per-sheet row heights and box placement at the
  foot of `oap.css`. If a box clips, adjust that sheet's `grid-template-rows` — don't shrink
  the type past ~6pt or it won't survive print.
- Every figure on the sheets is traceable to the client's own census, business records or
  planning documents. Open items are marked open rather than resolved with an estimate.

## Getting back to the summary

Every pack page carries a **Delivery summary** button at the top of the sidebar, above the
filter and outside `.nav` so it stays visible when the contents collapse on mobile. The brand
mark beside it links to `/` (it used to be a `#top` anchor, which did nothing on 81 of the 82
pages). The summary links the other way from its Access section.
