#!/usr/bin/env python3
"""The proposal as its own page on the delivery site, at /engagement-proposal.

Same source as catalogue document #2 (the v02 markdown), so the two cannot
drift. Different shell: no pack sidebar, no prev/next, a page that reads as a
single document with the Jewell mark at the top and the quote in it.
"""
import os, re, html
import markdown
from build_pack import ROOT, SITE, convert

SRC = os.path.join(ROOT, "00 Admin/04 Commercial + SOW",
                   "02__Proposal__Tap-That-Brewery__Client__Draft__v02.md")

raw = open(SRC, encoding="utf-8").read()
body = convert(SRC)
# convert() demotes h2 -> h3; give each section an id for the in-page nav.
secs = []
def tag(m):
    t = re.sub(r"<[^>]+>", "", m.group(1)); sid = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
    secs.append((sid, t)); return f'<h3 id="{sid}">{m.group(1)}</h3>'
body = re.sub(r"<h3>(.*?)</h3>", tag, body)
nav = "".join(f'<a href="#{i}">{html.escape(t)}</a>' for i, t in secs if not t.startswith("Appendix"))

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Proposal &middot; Tap That Brewery &middot; Jewell Projects</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--keg:#0E171F;--brass:#0066FF;--brass-lt:#5B8CFF;--cream:#FAF8F4;--paper:#FFFFFF;--ink:#111111;--steel:#666666;--rule:#D4D2D0;--shade:#EDEBEA}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--keg:#141C24;--brass:#5B8CFF;--brass-lt:#8FB4FF;--cream:#14181C;--paper:#1A1F25;--ink:#E9E7E3;--steel:#9AA0A6;--rule:rgba(233,231,227,.15);--shade:#191E23}}
:root[data-theme="dark"]{--keg:#141C24;--brass:#5B8CFF;--brass-lt:#8FB4FF;--cream:#14181C;--paper:#1A1F25;--ink:#E9E7E3;--steel:#9AA0A6;--rule:rgba(233,231,227,.15);--shade:#191E23}
html{scroll-behavior:smooth}
body{background:var(--cream);color:var(--ink);font-family:'Poppins',system-ui,sans-serif;font-size:15px;line-height:1.65;-webkit-font-smoothing:antialiased}
.top{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--cream) 90%,transparent);backdrop-filter:blur(12px);border-bottom:1px solid var(--rule)}
.top-in{max-width:960px;margin:0 auto;padding:12px 24px;display:flex;align-items:center;gap:18px;flex-wrap:wrap}
.wm{height:18px;width:auto;display:block}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .wm{filter:invert(1)}}
:root[data-theme="dark"] .wm{filter:invert(1)}
.top .k{font-size:11px;font-weight:600;letter-spacing:.13em;text-transform:uppercase;color:var(--steel)}
.top nav{margin-left:auto;display:flex;gap:2px;flex-wrap:wrap}
.top nav a{font-size:12px;color:var(--steel);text-decoration:none;padding:5px 9px;border-radius:6px}
.top nav a:hover{color:var(--ink);background:var(--shade)}
.wrap{max-width:960px;margin:0 auto;padding:44px 24px 80px}
.hero{padding-bottom:28px;margin-bottom:28px;border-bottom:2px solid var(--ink)}
.hero .eyebrow{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--brass);margin-bottom:12px}
.hero h1{font-size:clamp(30px,5vw,46px);font-weight:700;letter-spacing:-.03em;line-height:1.05;text-wrap:balance}
.hero h1 span{color:var(--brass)}
.hero .meta{margin-top:18px;display:grid;grid-template-columns:max-content 1fr;gap:6px 22px;font-size:13px}
.hero .meta b{font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--steel);padding-top:2px}
.prose h3{font-size:20px;font-weight:600;letter-spacing:-.015em;color:var(--brass);margin:44px 0 12px;padding-top:26px;border-top:1px solid var(--rule)}
.prose h3:first-of-type{border-top:0;padding-top:0;margin-top:0}
.prose h4{font-size:15px;font-weight:600;margin:26px 0 8px}
.prose p{margin:0 0 12px;max-width:72ch}
.prose em{color:var(--steel)}
.prose ul,.prose ol{margin:0 0 14px 22px;max-width:72ch}
.prose li{margin:0 0 6px}
.prose li::marker{color:var(--brass)}
.prose hr{display:none}
.tw{overflow-x:auto;margin:14px 0 20px;border:1px solid var(--rule);border-radius:8px;background:var(--paper)}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th,td{text-align:left;vertical-align:top;padding:10px 14px;border-bottom:1px solid var(--rule)}
th{font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--steel);background:var(--shade)}
tr:last-child td{border-bottom:0}
td strong{color:var(--ink)}
/* the metadata table at the top of the source has a blank header: render it as a key/value block */
.prose > .tw:first-of-type{display:none}
.foot{margin-top:60px;padding-top:16px;border-top:1px solid var(--rule);font-size:12px;color:var(--steel);display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
@media print{.top{display:none}body{background:#fff;color:#000;font-size:11pt}.wrap{padding:0;max-width:none}.tw{border-color:#ccc;break-inside:avoid}.prose h3{break-after:avoid}@page{size:A4;margin:18mm}}
</style>
</head>
<body>
<div class="top"><div class="top-in">
  <img class="wm" src="/brand/jewell-wordmark.png" alt="Jewell Projects">
  <span class="k">Tap That Brewery</span>
  <nav>@@NAV@@</nav>
</div></div>
<main class="wrap">
  <header class="hero">
    <div class="eyebrow">Proposal &middot; v02 &middot; 16 September 2026</div>
    <h1>Executing the plan on a page<span>.</span></h1>
    <div class="meta">
      <b>Engagement</b><span>Tap That Brewery – marketing strategy and execution</span>
      <b>Audience</b><span>Justin Mistry and Chris Smith, Tap That Brewery</span>
      <b>Status</b><span>Draft v02 – client-facing, with proposed investment</span>
      <b>Supersedes</b><span>Proposal v01, 28 August 2026</span>
      <b>Prepared by</b><span>Jewell Projects</span>
    </div>
  </header>
  <article class="prose">
@@BODY@@
  </article>
  <footer class="foot"><span>Jewell Projects</span><span>Proposal v02 – Tap That Brewery</span><span>clent@jewellprojects.com</span></footer>
</main>
</body>
</html>
"""
out = os.path.join(SITE, "engagement-proposal.html")
open(out, "w", encoding="utf-8").write(PAGE.replace("@@NAV@@", nav).replace("@@BODY@@", body))
print("wrote", out, f"({os.path.getsize(out):,} bytes; {len(secs)} sections)")
