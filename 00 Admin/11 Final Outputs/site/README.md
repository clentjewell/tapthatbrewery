# Delivery pack site — deployment notes

The client-facing 3D Process delivery summary, deployed to Cloudflare Pages.

| | |
|---|---|
| **Live** | https://tapthat-3d-process.pages.dev |
| **Password** | `tapthat2026` |
| **Pages project** | `tapthat-3d-process` (production branch `main`) |
| **Account** | Jewell Projects Cloudflare account |

## Files

| File | Purpose |
|---|---|
| `index.html` | The delivery pack — single page, ten sections, self-contained (Google Fonts is the only external request) |
| `_worker.js` | Password gate + asset serving. Pages advanced mode: a root `_worker.js` takes over all routing |

`index.html` is generated from `../delivery-summary.html` (the same page, without the doctype/head wrapper so it can also publish as an artifact). Edit whichever you prefer, but keep the two in step.

## Redeploy

```bash
cd "00 Admin/11 Final Outputs/site"
npx wrangler pages deploy . --project-name tapthat-3d-process --branch main --commit-dirty=true
```

Requires `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` in the environment.

## The password gate

A **soft gate**, not security: the password is shared with the client and is printed on the page in the reference pack it mirrors. It keeps the pack out of search results and away from casual visitors. Nothing behind it is confidential beyond the engagement itself.

- Signed cookie (`tt_session`), HMAC-SHA256 over the expiry, 7-day life
- Wrong password re-renders the gate with an error; `next` is restricted to same-origin paths so it can't be used as an open redirect
- `/__signout` clears the cookie
- All responses carry `noindex, nofollow, noarchive, nosnippet`

To change the password without editing code, set a `PACK_PASSWORD` environment variable on the Pages project (Settings → Environment variables) — the code prefers it over the built-in default.

## Custom domain

Not configured. To put this on a Jewell Projects domain, add it under the Pages project's Custom domains tab; DNS is already in Cloudflare.
