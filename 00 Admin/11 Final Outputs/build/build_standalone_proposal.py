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
nav = "".join(f'<a href="#{i}"><span class="n">{k:02d}</span>{html.escape(t)}</a>' for k, (i, t) in enumerate(secs, 1))

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
.top-in{position:relative}
.menu-b{margin-left:auto;display:inline-flex;align-items:center;gap:10px;font:inherit;font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--ink);background:none;border:1px solid var(--rule);border-radius:8px;padding:7px 12px;cursor:pointer}
.menu-b:hover{background:var(--shade)}
.menu-b:focus-visible{outline:2px solid var(--brass);outline-offset:2px}
.menu-b .bars{display:inline-block;width:16px;height:12px;position:relative}
.menu-b .bars i{position:absolute;left:0;right:0;height:2px;background:currentColor;border-radius:1px;transition:transform .18s,opacity .18s}
.menu-b .bars i:nth-child(1){top:0}.menu-b .bars i:nth-child(2){top:5px}.menu-b .bars i:nth-child(3){top:10px}
.menu-b[aria-expanded="true"] .bars i:nth-child(1){transform:translateY(5px) rotate(45deg)}
.menu-b[aria-expanded="true"] .bars i:nth-child(2){opacity:0}
.menu-b[aria-expanded="true"] .bars i:nth-child(3){transform:translateY(-5px) rotate(-45deg)}
.menu{position:absolute;right:24px;top:calc(100% + 6px);min-width:260px;max-width:min(360px,calc(100vw - 32px));background:var(--paper);border:1px solid var(--rule);border-radius:10px;box-shadow:0 12px 34px rgba(14,23,31,.14);padding:8px;display:none;z-index:30}
.menu[data-open="true"]{display:block}
.menu a{display:block;font-size:13.5px;color:var(--ink);text-decoration:none;padding:9px 12px;border-radius:7px}
.menu a:hover{background:var(--shade)}
.menu a:focus-visible{outline:2px solid var(--brass);outline-offset:-2px}
.menu .n{display:inline-block;width:22px;font-size:11px;font-weight:600;color:var(--brass);font-variant-numeric:tabular-nums}
@media (prefers-reduced-motion:reduce){.menu-b .bars i{transition:none}}
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
  <button class="menu-b" id="menu-b" type="button" aria-expanded="false" aria-controls="menu" aria-label="Contents"><span class="bars"><i></i><i></i><i></i></span>Contents</button>
  <nav class="menu" id="menu" data-open="false" aria-label="Sections">@@NAV@@</nav>
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
<script>
(function(){
  var b=document.getElementById('menu-b'), m=document.getElementById('menu');
  function set(open){ b.setAttribute('aria-expanded', String(open)); m.setAttribute('data-open', String(open)); }
  b.addEventListener('click', function(){ set(b.getAttribute('aria-expanded')!=='true'); });
  m.addEventListener('click', function(e){ if(e.target.closest('a')) set(false); });
  document.addEventListener('click', function(e){ if(!e.target.closest('.top-in')) set(false); });
  document.addEventListener('keydown', function(e){ if(e.key==='Escape'){ set(false); b.focus(); } });
})();
</script>
</body>
</html>
"""
out = os.path.join(SITE, "engagement-proposal.html")
open(out, "w", encoding="utf-8").write(PAGE.replace("@@NAV@@", nav).replace("@@BODY@@", body))
print("wrote", out, f"({os.path.getsize(out):,} bytes; {len(secs)} sections)")
