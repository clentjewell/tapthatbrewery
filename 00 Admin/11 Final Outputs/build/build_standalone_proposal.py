#!/usr/bin/env python3
"""The proposal as a designed page at /engagement-proposal.

Same markdown as catalogue document #2, so the two cannot drift. The
difference is that this does not pour the document through a generic prose
renderer: it parses the markdown into its real parts and gives each one a
treatment. Seven workstreams read as seven workstreams. The ladder reads as a
ladder. The money gets the weight the money deserves.

House identity is fixed by 11 Final Outputs/DEPLOYMENT.md, so the palette and
the single Poppins family are inherited, not invented. The expression is in
scale, rhythm and composition.
"""
import os, re, html
import markdown
from build_pack import ROOT, SITE

SRC = os.path.join(ROOT, "00 Admin/04 Commercial + SOW",
                   "02__Proposal__Tap-That-Brewery__Client__Draft__v03.md")
OUT = os.path.join(SITE, "engagement-proposal.html")

# ---------------------------------------------------------------- parsing

def inline(md):
    """Inline markdown to HTML, without the wrapping paragraph."""
    h = markdown.markdown(md.strip())
    return re.sub(r"^<p>|</p>$", "", h.strip())


def prose(md):
    h = markdown.markdown(md.strip(), extensions=["tables", "sane_lists"])
    h = h.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    return h


def split_table(chunk):
    """Rows of a pipe table as lists of raw cell markdown. Header dropped."""
    rows = []
    for ln in chunk.splitlines():
        ln = ln.strip()
        if not ln.startswith("|"):
            continue
        # A separator row must actually contain a dash. Without that test an
        # empty header row, "| | |", reads as a separator and the first real
        # row is then dropped in its place: that is how the Tap That signature
        # line disappeared from the sign-off block.
        if "-" in ln and set(ln) <= set("|:- "):
            continue
        rows.append([c.strip() for c in ln.strip("|").split("|")])
    return rows[1:] if rows else []


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", t).lower()).strip("-")


# The package this proposal belongs to. Copied into the site at build time
# rather than uploaded by hand, so the link and the file cannot drift apart.
COMMERCIAL = os.path.join(ROOT, "00 Admin/04 Commercial + SOW")
PLAN = os.path.join(ROOT, "00 Admin/11 Final Outputs/plan-on-a-page")
DOWNLOADS = [
    ("The proposal", "PDF", os.path.join(COMMERCIAL, "JP_TapThat_Proposal_v03.pdf")),
    ("The proposal", "Word", os.path.join(COMMERCIAL, "JP_TapThat_Proposal_v03.docx")),
    ("The proposal, as a deck", "PDF", os.path.join(COMMERCIAL, "JP_TapThat_ProposalDeck_v03.pdf")),
    ("The proposal, as a deck", "PowerPoint", os.path.join(COMMERCIAL, "JP_TapThat_ProposalDeck_v03.pptx")),
    ("The plan on a page", "PDF, five A3 sheets", os.path.join(PLAN, "TapThat_Plan-on-a-Page_A3.pdf")),
    ("The plan on a page", "PowerPoint, editable A3", os.path.join(PLAN, "TapThat_Plan-on-a-Page_A3.pptx")),
]


def r_downloads():
    import shutil
    out_dir = os.path.join(SITE, "downloads")
    os.makedirs(out_dir, exist_ok=True)
    cards = ['<p class="lede">Everything in this proposal, as files you can keep. '
             'The deck is the same content as the document, laid out to be walked through.</p>',
             '<div class="dl">']
    src_mtime = os.path.getmtime(SRC)
    for title, fmt, src in DOWNLOADS:
        if not os.path.exists(src):
            raise SystemExit("download missing, build it first: " + src)
        # A file older than the proposal it is generated from is a stale
        # download waiting to be served. Copying it silently is how the page
        # ends up contradicting its own attachments.
        if src.startswith(COMMERCIAL) and os.path.getmtime(src) < src_mtime - 1:
            raise SystemExit(
                "stale download: %s predates the proposal markdown.\n"
                "Rebuild the docx and the deck first, then run this again."
                % os.path.basename(src))
        name = os.path.basename(src)
        shutil.copyfile(src, os.path.join(out_dir, name))
        kb = os.path.getsize(src) / 1024.0
        size = "%.1f MB" % (kb / 1024) if kb > 1024 else "%d KB" % round(kb)
        ext = name.rsplit(".", 1)[1].upper()
        cards.append(
            f'<a class="dl-c rv" href="/downloads/{name}" download>'
            f'<span class="dl-x">{ext}</span>'
            f'<span class="dl-t">{html.escape(title)}</span>'
            # The badge already carries the extension, so only repeat the
            # format when it says something the badge does not.
            f'<span class="dl-m">{size if fmt.upper() == ext else html.escape(fmt) + " · " + size}</span></a>')
    cards.append("</div>")
    return "\n".join(cards)


raw = open(SRC, encoding="utf-8").read()

meta = {}
for m in re.finditer(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|$", raw, re.M):
    meta[m.group(1).strip()] = m.group(2).strip()
    if m.group(1).strip() == "Prepared by":
        break

body = raw[raw.index("\n## Purpose"):]
body = re.sub(r"\n---\n.*$", "", body, flags=re.S)

sections = []
for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", body, re.M | re.S):
    sections.append((m.group(1).strip(), m.group(2).strip()))

# ------------------------------------------------------------- renderers

HORIZON = [("30 days", "a"), ("3 months", "b"), ("6 months", "c"),
           ("1 year", "d"), ("Ongoing", "e"), ("As dated", "e")]

def horizon_class(t):
    for k, c in HORIZON:
        if t.lower().startswith(k.lower()):
            return c
    return "e"


def r_workstreams(content):
    intro, rest = content.split("\n### ", 1)
    out = [f'<p class="lede">{inline(intro)}</p>', '<div class="streams">']
    for blk in ("### " + rest).split("\n### "):
        blk = blk.lstrip("# ").strip()
        head, tail = blk.split("\n", 1)
        num, title = head.split(". ", 1)
        lede = tail.split("|", 1)[0].strip()
        rows = split_table(tail[tail.index("|"):])
        out.append(f'''<section class="stream rv">
  <div class="stream-h"><span class="stream-n">{int(num):02d}</span>
    <div><h4>{inline(title)}</h4>{f'<p>{inline(lede)}</p>' if lede else ''}</div></div>
  <ul class="acts">''')
        for a, d, w in rows:
            how, _, gets = d.partition("**You get:**")
            got = ""
            if gets.strip():
                items = [g.strip().rstrip(".") for g in gets.strip().split(";") if g.strip()]
                # The source reads as a sentence, so the final clause carries an
                # "and" that a bullet does not want.
                items = [re.sub(r"^and ", "", g) for g in items]
                lis = "".join(f"<li>{inline(g)}</li>" for g in items)
                got = f'<div class="gets"><span class="gets-k">You get</span><ul>{lis}</ul></div>'
            out.append(f'''<li><div class="act-n">{inline(a)}</div>'''
                       f'''<div class="act-d">{inline(how.strip())}{got}</div>'''
                       f'''<div class="act-w"><span class="when w-{horizon_class(w)}">{html.escape(w)}</span></div></li>''')
        out.append("</ul></section>")
    out.append("</div>")
    return "\n".join(out)


def r_thirty(content):
    intro = content.split("\n1.", 1)[0].strip()
    items = re.findall(r"^\d+\.\s+(.*)$", content, re.M)
    out = [f'<p class="lede">{inline(intro)}</p>', '<ol class="steps">']
    for i, it in enumerate(items, 1):
        out.append(f'<li class="rv"><span class="step-n">{i:02d}</span><p>{inline(it)}</p></li>')
    out.append("</ol>")
    return "\n".join(out)


def r_ladder(content):
    rows = split_table(content[content.index("|"):])
    note = re.search(r"^\*(.+)\*$", content, re.M)
    out = ['<ol class="ladder">']
    for h, what in rows:
        h = re.sub(r"\*\*", "", h)
        when, _, dated = h.partition(" – ")
        out.append(f'''<li class="rv"><div class="rung-h"><span class="rung-k">{html.escape(when)}</span>'''
                   f'''<span class="rung-d">{html.escape(dated)}</span></div>'''
                   f'''<p>{inline(what)}</p></li>''')
    out.append("</ol>")
    if note:
        out.append(f'<p class="note">{inline(note.group(1).lstrip("– "))}</p>')
    return "\n".join(out)


def r_investment(content):
    intro = content.split("\n|", 1)[0].strip()
    basis = split_table(content[content.index("|"):content.index("### Option A")])
    out = [f'<p class="lede">{inline(intro)}</p>', '<dl class="basis">']
    for k, v in basis:
        out.append(f'<div><dt>{inline(k)}</dt><dd>{inline(v)}</dd></div>')
    out.append("</dl>")

    blocks = dict(re.findall(r"^### (.+?)\n(.*?)(?=^### |\Z)", content, re.M | re.S))
    out.append('<div class="options">')
    for key, tag in [("Option A – the ninety-day sprint", "A"),
                     ("Option B – twelve months", "B")]:
        chunk = blocks[key]
        rows = split_table(chunk[chunk.index("|"):])
        pay = re.search(r"^Payment: (.+)$", chunk, re.M)
        lines = [r for r in rows if not r[0].lower().startswith("**option")]
        # The price is read off the table's own total row, so the figure on
        # the page and the figure in the document are one number, not two.
        total = [r for r in rows if r[0].lower().startswith("**option")][0][1]
        m = re.match(r"\*\*(.+?)\*\*(.*)", total)
        headline, rest = m.group(1).strip(), m.group(2)
        big = re.match(r"\$[\d,]+", headline).group(0)
        sub = headline[len(big):].strip(" ·,")
        was = re.search(r"normally (\$[\d,]+)", rest)
        extra = [x.strip() for x in rest.split("·") if x.strip() and "normally" not in x]
        sub = " · ".join([x for x in [sub] + extra if x])
        wasline = (f'<span class="was">Normally <s>{was.group(1)}</s></span>'
                   if was else "")
        offtag = '<span class="opt-off">Discounted</span>' if was else ""
        out.append(f'''<section class="opt rv">
  <div class="opt-top"><span class="opt-tag">Option {tag}</span>{offtag}
    <h4>{inline(key.split("– ",1)[1].strip().capitalize())}</h4></div>
  <div class="opt-price">{wasline}<strong>{big}</strong><span>{sub}</span></div>
  <ul class="opt-lines">''')
        for line, fee in lines:
            out.append(f'<li><span class="ol-t">{inline(line)}</span>'
                       f'<span class="ol-f">{inline(fee)}</span></li>')
        out.append(f'</ul><p class="opt-pay"><strong>Payment:</strong> '
                   f'{inline(pay.group(1)) if pay else ""}</p></section>')
    out.append("</div>")

    earn = blocks["What it has to earn"]
    earn_p = earn.split("\n|", 1)[0].strip()
    out.append(f'<div class="earn rv"><h4>What it has to earn</h4><p>{inline(earn_p)}</p></div>')
    notin = split_table(earn[earn.index("|"):])
    out.append('<h4 class="sub">Not included</h4><dl class="basis tight">')
    for k, v in notin:
        out.append(f'<div><dt>{inline(k)}</dt><dd>{inline(v)}</dd></div>')
    out.append("</dl>")
    tail = re.search(r"^\*–\s*(.+)\*$", earn, re.M)
    if tail:
        out.append(f'<p class="note">{inline(tail.group(1))}</p>')
    return "\n".join(out)


def r_signoff(content):
    """A sign-off block that can actually be signed.

    Each party types a name and either draws a signature or types one, and the
    state is kept in that browser so a half-finished signature survives a
    reload. It is deliberately not a filing system: there is no store behind
    this page, so the block says what it is and offers a signed copy to send
    back.
    """
    rows = split_table(content[content.index("|"):])
    out = ['<div class="signs">']
    for i, (who, _) in enumerate(rows):
        pid = "p%d" % i
        out.append(f'''<form class="sign rv" data-party="{pid}" novalidate>
  <div class="sign-top"><span class="sign-k">{inline(who)}</span>
    <span class="sign-state" data-state="unsigned">Unsigned</span></div>

  <label class="sign-l" for="{pid}-name">Full name</label>
  <input class="sign-in" id="{pid}-name" name="name" type="text" autocomplete="name"
         placeholder="Type your full name" spellcheck="false">

  <div class="sign-l sign-l-row"><span>Signature</span>
    <span class="sig-modes" role="group" aria-label="Signature method">
      <button type="button" class="sig-m" data-mode="draw" aria-pressed="true">Draw</button>
      <button type="button" class="sig-m" data-mode="type" aria-pressed="false">Type</button>
    </span></div>
  <div class="sig-wrap">
    <canvas class="sig-pad" aria-label="Signature pad. Draw your signature, or switch to Type."></canvas>
    <img class="sig-img" alt="" hidden>
    <span class="sig-hint">Draw here</span>
  </div>

  <div class="sign-foot">
    <span class="sign-date">Date <b>&mdash;</b></span>
    <span class="sign-acts">
      <button type="button" class="btn-t sig-clear">Clear</button>
      <button type="submit" class="btn-p sig-go">Sign</button>
    </span>
  </div>
</form>''')
    out.append("</div>")
    out.append('<p class="sign-note">Signing here records your acceptance and keeps it '
               'in this browser so nothing is lost on a reload. It does not send anything: '
               'use <button type="button" class="btn-t" id="sign-print">download a signed copy</button> '
               'and return it, and we will issue the executed original for countersignature.</p>')
    return "\n".join(out)


RENDER = {
    "the-work-by-workstream": r_workstreams,
    "the-first-30-days": r_thirty,
    "timeline-on-your-ladder": r_ladder,
    "investment-and-terms": r_investment,
    "sign-off": r_signoff,
}

# --------------------------------------------------------------- assembly

nav, blocks = [], []
for i, (title, content) in enumerate(sections, 1):
    sid = slug(title)
    nav.append(f'<a href="#{sid}"><span class="n">{i:02d}</span>{html.escape(title)}</a>')
    inner = RENDER.get(sid, prose)(content)
    dark = ' data-dark="1"' if sid == "investment-and-terms" else ""
    blocks.append(f'''<section class="sec" id="{sid}"{dark}>
  <div class="sec-in">
    <header class="sec-h rv"><span class="sec-n">{i:02d}</span><h3>{html.escape(title)}</h3></header>
    <div class="sec-b">{inner}</div>
  </div>
</section>''')

i = len(sections) + 1
nav.append(f'<a href="#take-it-away"><span class="n">{i:02d}</span>Take it away</a>')
blocks.append(f'''<section class="sec" id="take-it-away">
  <div class="sec-in">
    <header class="sec-h rv"><span class="sec-n">{i:02d}</span><h3>Take it away</h3></header>
    <div class="sec-b">{r_downloads()}</div>
  </div>
</section>''')

THESIS = ("One marketer cannot run a switcher campaign, a referral programme, an events "
          "calendar, a wholesale pipeline and a CRM build at once. This is the hands.")

FIGURES = [("1,000", "active keg refillers by year three"),
           ("250", "by March 2027, your first milestone"),
           ("$2.55", "a schooner at home, against $12 at the pub"),
           ("56%", "of refill customers bought their system elsewhere")]

figs = "".join(f'<div class="fig rv"><strong>{n}</strong><span>{t}</span></div>' for n, t in FIGURES)
metarows = "".join(f'<div><dt>{html.escape(k)}</dt><dd>{inline(v)}</dd></div>'
                   for k, v in meta.items() if k in
                   ("Engagement", "Audience", "Status", "Supersedes", "Prepared by"))

PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Proposal &middot; Tap That Brewery &middot; Jewell Projects</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --keg:#0E171F;--keg-2:#16222D;--brass:#0066FF;--brass-lt:#5B8CFF;
  --cream:#FAF8F4;--paper:#FFFFFF;--ink:#111111;--steel:#666666;
  --rule:#D4D2D0;--shade:#EFEDEA;--tint:#F2F5FB;
  --meas:68ch;--pad:clamp(20px,5vw,64px);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --keg:#0B1218;--keg-2:#131C25;--brass:#5B8CFF;--brass-lt:#8FB4FF;
  --cream:#12161A;--paper:#181E24;--ink:#E9E7E3;--steel:#9AA0A6;
  --rule:rgba(233,231,227,.16);--shade:#1B2128;--tint:#16202C;}}
:root[data-theme="dark"]{
  --keg:#0B1218;--keg-2:#131C25;--brass:#5B8CFF;--brass-lt:#8FB4FF;
  --cream:#12161A;--paper:#181E24;--ink:#E9E7E3;--steel:#9AA0A6;
  --rule:rgba(233,231,227,.16);--shade:#1B2128;--tint:#16202C}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{background:var(--cream);color:var(--ink);font-family:'Poppins',system-ui,sans-serif;
  font-size:15.5px;line-height:1.66;-webkit-font-smoothing:antialiased;overflow-x:hidden}
h1,h2,h3,h4{letter-spacing:-.025em;line-height:1.1;text-wrap:balance}
strong{font-weight:600}
em{font-style:italic;color:var(--steel)}

/* ---- progress + bar ---- */
.prog{position:fixed;top:0;left:0;height:2px;background:var(--brass);width:0;z-index:60}
.top{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--cream) 88%,transparent);
  backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-bottom:1px solid var(--rule)}
.top-in{max-width:1280px;margin:0 auto;padding:11px var(--pad);display:flex;align-items:center;gap:16px;position:relative}
.wm{height:17px;width:auto;display:block;flex:none}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .wm{filter:invert(1)}}
:root[data-theme="dark"] .wm{filter:invert(1)}
.top .k{font-size:10.5px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--steel);white-space:nowrap}
@media(max-width:620px){.top .k{display:none}}
.menu-b{margin-left:auto;display:inline-flex;align-items:center;gap:10px;font:inherit;font-size:11px;
  font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);background:none;
  border:1px solid var(--rule);border-radius:999px;padding:8px 15px;cursor:pointer;transition:background .15s}
.menu-b:hover{background:var(--shade)}
.menu-b:focus-visible{outline:2px solid var(--brass);outline-offset:2px}
.menu-b .bars{display:inline-block;width:15px;height:11px;position:relative}
.menu-b .bars i{position:absolute;left:0;right:0;height:1.5px;background:currentColor;border-radius:1px;transition:transform .2s,opacity .2s}
.menu-b .bars i:nth-child(1){top:0}.menu-b .bars i:nth-child(2){top:4.75px}.menu-b .bars i:nth-child(3){top:9.5px}
.menu-b[aria-expanded="true"] .bars i:nth-child(1){transform:translateY(4.75px) rotate(45deg)}
.menu-b[aria-expanded="true"] .bars i:nth-child(2){opacity:0}
.menu-b[aria-expanded="true"] .bars i:nth-child(3){transform:translateY(-4.75px) rotate(-45deg)}
.menu{position:absolute;right:var(--pad);top:calc(100% + 8px);min-width:280px;max-width:min(380px,calc(100vw - 32px));
  background:var(--paper);border:1px solid var(--rule);border-radius:12px;
  box-shadow:0 18px 50px rgba(14,23,31,.18);padding:8px;display:none;z-index:55}
.menu[data-open="true"]{display:block}
.menu a{display:flex;gap:12px;align-items:baseline;font-size:13.5px;color:var(--ink);
  text-decoration:none;padding:9px 13px;border-radius:8px}
.menu a:hover{background:var(--shade)}
.menu a:focus-visible{outline:2px solid var(--brass);outline-offset:-2px}
.menu .n{font-size:10.5px;font-weight:700;color:var(--brass);font-variant-numeric:tabular-nums;flex:none}

/* ---- cover ---- */
.cover{background:var(--keg);color:#F4F2EE;padding:clamp(56px,11vw,132px) var(--pad) clamp(44px,7vw,84px);
  position:relative;overflow:hidden}
.cover::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(120% 90% at 88% -10%,rgba(0,102,255,.20),transparent 62%)}
.cover-in{max-width:1280px;margin:0 auto;position:relative;z-index:1}
.eyebrow{font-size:11px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--brass-lt)}
.cover h1{font-size:clamp(38px,7.4vw,92px);font-weight:700;letter-spacing:-.04em;margin:20px 0 0;max-width:15ch}
.cover h1 .dot{color:var(--brass-lt)}
.cover .thesis{margin-top:26px;max-width:52ch;font-size:clamp(15.5px,1.7vw,20px);line-height:1.5;color:rgba(244,242,238,.72)}
.cover dl{margin-top:clamp(34px,5vw,56px);display:grid;gap:1px;background:rgba(244,242,238,.16);
  border:1px solid rgba(244,242,238,.16);border-radius:12px;overflow:hidden;
  grid-template-columns:repeat(auto-fit,minmax(215px,1fr))}
.cover dl>div{background:var(--keg);padding:15px 18px}
.cover dt{font-size:9.5px;font-weight:600;letter-spacing:.15em;text-transform:uppercase;color:rgba(244,242,238,.5)}
.cover dd{font-size:13.5px;margin-top:5px;line-height:1.45;color:rgba(244,242,238,.94)}

/* ---- figures ---- */
.figs{max-width:1280px;margin:0 auto;padding:0 var(--pad);display:grid;gap:1px;background:var(--rule);
  border:1px solid var(--rule);border-radius:14px;overflow:hidden;
  grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
  margin-top:clamp(-46px,-4vw,-30px);position:relative;z-index:2;
  max-width:min(1280px,calc(100% - 2*var(--pad)));padding:0;box-shadow:0 14px 40px rgba(14,23,31,.10)}
.fig{background:var(--paper);padding:22px 24px}
.fig strong{display:block;font-size:clamp(28px,3.6vw,40px);font-weight:700;letter-spacing:-.04em;
  color:var(--brass);line-height:1;font-variant-numeric:tabular-nums}
.fig span{display:block;margin-top:9px;font-size:12.5px;line-height:1.45;color:var(--steel)}

/* ---- sections ---- */
.sec{padding:clamp(54px,7vw,92px) var(--pad)}
.sec-in{max-width:1280px;margin:0 auto;display:grid;grid-template-columns:150px minmax(0,1fr);gap:clamp(20px,4vw,56px)}
@media(max-width:900px){.sec-in{grid-template-columns:1fr;gap:18px}}
.sec-h{grid-column:1;display:flex;align-items:baseline;gap:14px}
@media(min-width:901px){.sec-h{flex-direction:column;gap:6px;position:sticky;top:96px;align-self:start}}
.sec-n{font-size:12px;font-weight:700;letter-spacing:.14em;color:var(--brass);font-variant-numeric:tabular-nums}
.sec-h h3{font-size:clamp(20px,2.3vw,25px);font-weight:600;color:var(--ink)}
@media(min-width:901px){.sec-h h3{font-size:19px;color:var(--steel);font-weight:500;letter-spacing:-.01em}}
.sec-b{grid-column:2;min-width:0}
@media(max-width:900px){.sec-b{grid-column:1}}
.sec-b>p{margin:0 0 14px;max-width:var(--meas)}
.sec-b>ul{margin:0 0 16px;padding-left:0;list-style:none;max-width:var(--meas)}
.sec-b>ul>li{position:relative;padding-left:22px;margin-bottom:11px}
.sec-b>ul>li::before{content:"";position:absolute;left:2px;top:.68em;width:6px;height:6px;
  border-radius:1px;background:var(--brass)}
.lede{font-size:clamp(17px,2vw,21px);line-height:1.5;font-weight:500;letter-spacing:-.015em;
  color:var(--ink);max-width:46ch;margin:0 0 26px!important}
.note{margin-top:20px!important;padding-top:14px;border-top:1px solid var(--rule);
  font-size:13px;line-height:1.55;color:var(--steel);max-width:var(--meas)}
h4.sub{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;
  color:var(--steel);margin:34px 0 12px}

/* ---- generic tables (kept for the plain sections) ---- */
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:0 0 20px;border:1px solid var(--rule);border-radius:12px;background:var(--paper)}
/* Subheads written in a prose section, such as the positioning options. */
.sec-b h3{font-size:clamp(17px,2.2vw,20px);font-weight:600;letter-spacing:-.01em;
  line-height:1.25;margin:34px 0 10px}
.sec-b h3:first-child{margin-top:0}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th,td{text-align:left;vertical-align:top;padding:13px 16px;border-bottom:1px solid var(--rule)}
th{font-size:10.5px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--steel);background:var(--shade)}
tr:last-child td{border-bottom:0}
td:first-child{width:32%;color:var(--ink)}

/* ---- workstreams ---- */
.streams{display:flex;flex-direction:column;gap:14px}
.stream{background:var(--paper);border:1px solid var(--rule);border-radius:14px;padding:24px clamp(18px,2.4vw,28px)}
.stream-h{display:flex;gap:16px;align-items:flex-start;padding-bottom:16px;margin-bottom:4px;border-bottom:1px solid var(--rule)}
.stream-n{font-size:clamp(26px,3vw,34px);font-weight:700;color:var(--brass);line-height:.9;
  font-variant-numeric:tabular-nums;letter-spacing:-.05em;flex:none;opacity:.9}
.stream-h h4{font-size:clamp(17px,2vw,20px);font-weight:600}
.stream-h p{margin-top:7px;font-size:14px;line-height:1.55;color:var(--steel);max-width:58ch}
.acts{list-style:none}
.gets{margin-top:11px;padding:11px 14px;background:var(--tint);border:1px solid var(--rule);border-radius:10px}
.gets-k{display:block;font-size:9.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
  color:var(--brass);margin-bottom:6px}
.gets ul{list-style:none;display:grid;gap:5px}
.gets li{font-size:13.2px;line-height:1.5;color:var(--ink);padding-left:14px;position:relative}
.gets li::before{content:"";position:absolute;left:0;top:8px;width:5px;height:5px;border-radius:50%;
  background:var(--brass);opacity:.55}
.acts > li{display:grid;grid-template-columns:200px minmax(0,1fr) 128px;gap:18px;align-items:start;
  padding:15px 0;border-bottom:1px solid var(--rule)}
.acts > li:last-child{border-bottom:0;padding-bottom:0}
@media(max-width:760px){.acts > li{grid-template-columns:1fr;gap:6px}}
.act-n{font-size:14px;font-weight:600;line-height:1.45}
.act-d{font-size:13.8px;line-height:1.6;color:var(--steel)}
.act-w{text-align:right}
@media(max-width:760px){.act-w{text-align:left;margin-top:3px}}
.when{display:inline-block;max-width:100%;font-size:10.5px;font-weight:600;letter-spacing:.09em;
  text-transform:uppercase;padding:5px 11px;border-radius:999px;line-height:1.34;
  white-space:normal;text-wrap:balance;border:1px solid transparent}
.w-a{background:var(--brass);color:#fff}
.w-b{background:var(--tint);color:var(--brass);border-color:color-mix(in srgb,var(--brass) 28%,transparent)}
.w-c{background:transparent;color:var(--steel);border-color:var(--rule)}
.w-d,.w-e{background:transparent;color:var(--steel);border-color:var(--rule);opacity:.78}

/* ---- steps ---- */
.steps{list-style:none;display:grid;gap:1px;background:var(--rule);border:1px solid var(--rule);
  border-radius:14px;overflow:hidden;grid-template-columns:repeat(auto-fit,minmax(310px,1fr))}
.steps li{background:var(--paper);padding:20px 22px;display:flex;gap:14px;align-items:flex-start}
.step-n{font-size:12px;font-weight:700;color:var(--brass);font-variant-numeric:tabular-nums;
  padding-top:3px;flex:none}
.steps p{font-size:14px;line-height:1.6;color:var(--steel)}
.steps strong{color:var(--ink)}

/* ---- ladder ---- */
.dl{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:26px}
.dl-c{display:flex;flex-direction:column;gap:5px;padding:20px 22px;text-decoration:none;
  background:var(--paper);border:1px solid var(--rule);border-radius:14px;color:var(--ink);
  transition:border-color .15s,transform .15s}
.dl-c:hover{border-color:var(--brass);transform:translateY(-2px)}
.dl-x{font-size:10px;font-weight:700;letter-spacing:.14em;color:var(--brass)}
.dl-t{font-size:16px;font-weight:600;line-height:1.3}
.dl-m{font-size:12.5px;color:var(--steel)}
@media print{.dl-c{break-inside:avoid}}
.ladder{list-style:none;position:relative;padding-left:30px}
.ladder::before{content:"";position:absolute;left:5px;top:8px;bottom:8px;width:1px;background:var(--rule)}
.ladder li{position:relative;padding:0 0 30px}
.ladder li:last-child{padding-bottom:0}
.ladder li::before{content:"";position:absolute;left:-29px;top:7px;width:11px;height:11px;border-radius:50%;
  background:var(--cream);border:2px solid var(--brass)}
.ladder li:first-child::before{background:var(--brass)}
.rung-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px}
.rung-k{font-size:15.5px;font-weight:600;letter-spacing:-.01em}
.rung-d{font-size:11px;font-weight:600;letter-spacing:.11em;text-transform:uppercase;color:var(--brass)}
.ladder p{margin-top:7px;font-size:14px;line-height:1.6;color:var(--steel);max-width:62ch}

/* ---- investment ---- */
.sec[data-dark]{background:var(--keg);color:#F4F2EE}
.sec[data-dark] .sec-h h3{color:rgba(244,242,238,.62)}
.sec[data-dark] .sec-n{color:var(--brass-lt)}
.sec[data-dark] .lede{color:rgba(244,242,238,.9)}
.sec[data-dark] .note{color:rgba(244,242,238,.6);border-top-color:rgba(244,242,238,.18)}
.sec[data-dark] h4.sub{color:rgba(244,242,238,.6)}
.basis{display:grid;gap:1px;background:rgba(244,242,238,.16);border:1px solid rgba(244,242,238,.16);
  border-radius:12px;overflow:hidden;margin-bottom:26px}
.basis>div{background:var(--keg-2);padding:16px 19px;display:grid;grid-template-columns:230px minmax(0,1fr);gap:18px}
@media(max-width:760px){.basis>div{grid-template-columns:1fr;gap:5px}}
.basis dt{font-size:13.5px;font-weight:600;color:#F4F2EE}
.basis dd{font-size:13.5px;line-height:1.6;color:rgba(244,242,238,.74)}
.basis.tight>div{padding:13px 19px}
.options{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));margin-bottom:26px}
.opt{background:var(--keg-2);border:1px solid rgba(244,242,238,.16);border-radius:16px;padding:26px clamp(20px,2.4vw,28px);display:flex;flex-direction:column}
.opt:first-child{border-color:color-mix(in srgb,var(--brass-lt) 42%,transparent)}
.opt-top{display:flex;flex-wrap:wrap;align-items:center;gap:10px}
.opt-tag{font-size:10px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--brass-lt)}
.opt-off{font-size:9.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
  background:var(--brass);color:#fff;padding:4px 9px;border-radius:999px}
.opt-top h4{flex-basis:100%;font-size:19px;font-weight:600;margin-top:2px;color:#F4F2EE}
.opt-price{margin:20px 0 18px;padding-bottom:18px;border-bottom:1px solid rgba(244,242,238,.16)}
.opt-price .was{display:block;font-size:13px;color:rgba(244,242,238,.52);margin-bottom:6px}
.opt-price .was s{text-decoration-thickness:1.5px;text-decoration-color:var(--brass-lt)}
.opt-price strong{display:block;font-size:clamp(36px,4.6vw,52px);font-weight:700;letter-spacing:-.045em;
  line-height:1;color:#fff;font-variant-numeric:tabular-nums}
.opt-price span{display:block;margin-top:9px;font-size:12.5px;color:rgba(244,242,238,.62)}
.opt-lines{list-style:none;flex:1}
.opt-lines li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;padding:11px 0;
  border-bottom:1px solid rgba(244,242,238,.1);font-size:13.3px;line-height:1.55}
.opt-lines li:last-child{border-bottom:0}
.ol-t{color:rgba(244,242,238,.74)}
.ol-t strong{color:#F4F2EE}
.ol-f{color:#F4F2EE;font-weight:600;white-space:nowrap;text-align:right;font-variant-numeric:tabular-nums}
.opt-pay strong{color:rgba(244,242,238,.82)}
.opt-pay{margin-top:16px;padding-top:14px;border-top:1px solid rgba(244,242,238,.16);
  font-size:12.5px;line-height:1.55;color:rgba(244,242,238,.62)}
.earn{border-left:2px solid var(--brass-lt);padding:4px 0 4px 20px;margin-bottom:28px}
.earn h4{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--brass-lt)}
.earn p{margin-top:10px;font-size:15px;line-height:1.62;color:rgba(244,242,238,.88);max-width:62ch}

/* ---- sign-off ---- */
.signs{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}
.sign{background:var(--paper);border:1px solid var(--rule);border-radius:14px;padding:24px}
.sign-k{display:block;font-size:11px;font-weight:600;letter-spacing:.13em;text-transform:uppercase;
  color:var(--brass);margin-bottom:20px}
.sign-f{display:flex;align-items:baseline;gap:12px;margin-bottom:17px}
.sign-f:last-child{margin-bottom:0}
.sign-f span{font-size:11px;color:var(--steel);width:64px;flex:none}
.sign-f i{flex:1;border-bottom:1px solid var(--rule);height:15px}

/* ---- sign-off ---- */
.sign-top{display:flex;align-items:center;gap:12px;margin-bottom:20px}
.sign-state{margin-left:auto;font-size:9.5px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;
  padding:4px 10px;border-radius:999px;border:1px solid var(--rule);color:var(--steel)}
.sign-state[data-state="signed"]{background:var(--brass);border-color:var(--brass);color:#fff}
.sign-l{display:block;font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;
  color:var(--steel);margin-bottom:7px}
.sign-l-row{display:flex;align-items:center;gap:12px;margin-top:18px}
.sign-in{width:100%;font:inherit;font-size:15px;color:var(--ink);background:var(--cream);
  border:1px solid var(--rule);border-radius:9px;padding:11px 13px}
.sign-in::placeholder{color:var(--steel);opacity:.75}
.sign-in:focus-visible{outline:2px solid var(--brass);outline-offset:1px;border-color:var(--brass)}
.sign-in[readonly]{background:transparent;border-style:dashed;color:var(--ink)}
.sig-modes{margin-left:auto;display:inline-flex;border:1px solid var(--rule);border-radius:7px;overflow:hidden}
.sig-m{font:inherit;font-size:10.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;
  background:none;border:0;color:var(--steel);padding:5px 10px;cursor:pointer}
.sig-m+.sig-m{border-left:1px solid var(--rule)}
.sig-m[aria-pressed="true"]{background:var(--brass);color:#fff}
.sig-m:focus-visible{outline:2px solid var(--brass);outline-offset:-2px}
/* the pad stays white paper in both themes, the way a signature strip is */
.sig-wrap{position:relative;margin-top:8px;background:#fff;border:1px solid var(--rule);
  border-radius:9px;height:110px;overflow:hidden}
.sig-pad{display:block;width:100%;height:100%;touch-action:none;cursor:crosshair}
.sig-img{display:block;width:100%;height:100%;object-fit:contain;object-position:left center}
.sig-hint{position:absolute;left:14px;top:50%;transform:translateY(-50%);font-size:12.5px;
  color:#B9B6B1;pointer-events:none}
.sig-wrap[data-dirty="1"] .sig-hint{display:none}
.sign-foot{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-top:16px;
  padding-top:15px;border-top:1px solid var(--rule)}
.sign-date{font-size:12.5px;color:var(--steel)}
.sign-date b{color:var(--ink);font-weight:600}
.sign-acts{margin-left:auto;display:flex;gap:8px}
.btn-t{font:inherit;font-size:12px;font-weight:600;background:none;border:1px solid var(--rule);
  border-radius:8px;padding:8px 14px;color:var(--steel);cursor:pointer}
.btn-t:hover{color:var(--ink);border-color:var(--steel)}
.btn-p{font:inherit;font-size:12px;font-weight:600;background:var(--brass);border:1px solid var(--brass);
  border-radius:8px;padding:8px 18px;color:#fff;cursor:pointer}
.btn-p:hover{filter:brightness(1.08)}
.btn-t:focus-visible,.btn-p:focus-visible{outline:2px solid var(--brass);outline-offset:2px}
.sign-note{margin-top:18px;font-size:12.5px;line-height:1.6;color:var(--steel);max-width:var(--meas)}
.sign-note .btn-t{padding:3px 9px;font-size:11.5px}

/* ---- foot ---- */
.foot{border-top:1px solid var(--rule);padding:26px var(--pad) 60px}
.foot-in{max-width:1280px;margin:0 auto;display:flex;justify-content:space-between;gap:16px;
  flex-wrap:wrap;font-size:12px;color:var(--steel)}

/* ---- motion ---- */
html.js .rv{opacity:0;transform:translateY(14px)}
html.js .rv.in{opacity:1;transform:none;transition:opacity .6s cubic-bezier(.16,1,.3,1),transform .6s cubic-bezier(.16,1,.3,1)}
html.js .cover .eyebrow,html.js .cover h1,html.js .cover .thesis,html.js .cover dl{
  opacity:0;animation:rise .82s cubic-bezier(.16,1,.3,1) forwards}
html.js .cover h1{animation-delay:.07s}
html.js .cover .thesis{animation-delay:.15s}
html.js .cover dl{animation-delay:.22s}
@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  html.js .rv,html.js .cover *{opacity:1!important;transform:none!important;animation:none!important}
  .menu-b .bars i{transition:none}}

/* ---- print ---- */
@media print{
  .top,.prog,.menu{display:none}
  .sig-modes,.sign-acts,.sig-hint,.sign-note .btn-t{display:none!important}
  .sign-in{border:0;border-bottom:1px solid #999;border-radius:0;padding-left:0;background:#fff!important}
  .sig-wrap{border:0;border-bottom:1px solid #999;border-radius:0;height:76px}
  .sign-state{border-color:#999;background:#fff!important;color:#000!important}
  body{background:#fff;color:#000;font-size:10.5pt}
  .cover,.sec[data-dark]{background:#fff!important;color:#000!important}
  .cover::after{display:none}
  .cover h1{font-size:30pt}
  .was,.was s,.cover dt,.cover dd,.cover .thesis,.sec[data-dark] .lede,.sec[data-dark] .note,
  .basis dt,.basis dd,.ol-t,.ol-f,.earn p,.opt-price strong,.opt-top h4,.opt-pay{color:#000!important}
  .cover dl>div,.opt,.basis>div{background:#fff!important}
  /* the 1px-gap trick paints a grey block wherever the grid has no cell */
  .figs,.basis,.cover dl,.steps{background:#fff!important;box-shadow:none!important;gap:0}
  .figs{grid-template-columns:repeat(4,1fr)}
  .fig,.steps li{border:1px solid #ccc;margin:-0.5px}
  .eyebrow,.sec-n,.opt-tag,.rung-d,.earn h4{color:#333!important}
  .sec-in{grid-template-columns:1fr}
  .sec-h{position:static}
  .sec{padding:18pt 0;break-inside:auto}
  .stream,.opt,.sign,.steps li{break-inside:avoid}
  .sec-h h3{color:#000!important;font-size:15pt}
  html.js .rv{opacity:1!important;transform:none!important}
  @page{size:A4;margin:16mm}
}
</style>
</head>
<body>
<div class="prog" id="prog"></div>
<div class="top"><div class="top-in">
  <img class="wm" src="/brand/jewell-wordmark.png" alt="Jewell Projects">
  <span class="k">Tap That Brewery</span>
  <button class="menu-b" id="menu-b" type="button" aria-expanded="false" aria-controls="menu" aria-label="Contents"><span class="bars"><i></i><i></i><i></i></span>Contents</button>
  <nav class="menu" id="menu" data-open="false" aria-label="Sections">@@NAV@@</nav>
</div></div>

<header class="cover">
  <div class="cover-in">
    <div class="eyebrow">Proposal &middot; v02 &middot; 16 September 2026</div>
    <h1>Executing the plan on a page<span class="dot">.</span></h1>
    <p class="thesis">@@THESIS@@</p>
    <dl>@@META@@</dl>
  </div>
</header>
<div class="figs">@@FIGS@@</div>

<main>
@@BLOCKS@@
</main>

<footer class="foot"><div class="foot-in">
  <span>Jewell Projects</span><span>Proposal v02 &middot; Tap That Brewery</span>
  <span>clent@jewellprojects.com</span>
</div></footer>

<script>
document.documentElement.className += ' js';
(function(){
  var b=document.getElementById('menu-b'), m=document.getElementById('menu');
  function set(o){ b.setAttribute('aria-expanded',String(o)); m.setAttribute('data-open',String(o)); }
  b.addEventListener('click',function(){ set(b.getAttribute('aria-expanded')!=='true'); });
  m.addEventListener('click',function(e){ if(e.target.closest('a')) set(false); });
  document.addEventListener('click',function(e){ if(!e.target.closest('.top-in')) set(false); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape'){ set(false); b.focus(); } });

  var p=document.getElementById('prog');
  function prog(){ var h=document.documentElement;
    var d=h.scrollHeight-h.clientHeight;
    p.style.width=(d>0?(h.scrollTop/d)*100:0)+'%'; }
  addEventListener('scroll',prog,{passive:true}); prog();

  var rv=[].slice.call(document.querySelectorAll('.rv'));
  if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches){
    rv.forEach(function(el){ el.classList.add('in'); }); return; }
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
  },{rootMargin:'0px 0px -8% 0px',threshold:.06});
  rv.forEach(function(el){ io.observe(el); });
})();
</script>

<script>
/* Sign-off. Draw or type a signature, stamp the date, keep it in this
   browser. There is no store behind this page, so nothing leaves the
   machine; the printed copy is what gets returned. */
(function(){
  var KEY = 'tt-proposal-signoff-v1';
  var forms = [].slice.call(document.querySelectorAll('.sign[data-party]'));
  if (!forms.length) return;

  function load(){ try { return JSON.parse(localStorage.getItem(KEY)) || {}; }
                   catch(e){ return {}; } }
  function save(st){ try { localStorage.setItem(KEY, JSON.stringify(st)); } catch(e){} }
  var state = load();

  function today(){
    try { return new Date().toLocaleDateString('en-AU',
            { day:'numeric', month:'long', year:'numeric' }); }
    catch(e){ return new Date().toDateString(); }
  }

  forms.forEach(function(f){
    var id    = f.getAttribute('data-party'),
        name  = f.querySelector('.sign-in'),
        wrap  = f.querySelector('.sig-wrap'),
        cv    = f.querySelector('.sig-pad'),
        img   = f.querySelector('.sig-img'),
        dateB = f.querySelector('.sign-date b'),
        pill  = f.querySelector('.sign-state'),
        go    = f.querySelector('.sig-go'),
        clr   = f.querySelector('.sig-clear'),
        modes = [].slice.call(f.querySelectorAll('.sig-m')),
        ctx   = cv.getContext('2d'),
        mode = 'draw', drawing = false, dirty = false, signed = false;

    function fit(){
      var r = cv.getBoundingClientRect(), d = window.devicePixelRatio || 1;
      if (!r.width) return;
      var keep = dirty ? cv.toDataURL() : null;
      cv.width = Math.round(r.width * d); cv.height = Math.round(r.height * d);
      ctx.setTransform(d, 0, 0, d, 0, 0);
      ctx.lineWidth = 2.1; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      ctx.strokeStyle = '#141414'; ctx.fillStyle = '#141414';
      if (keep) { var im = new Image();
        im.onload = function(){ ctx.drawImage(im, 0, 0, r.width, r.height); };
        im.src = keep; }
    }

    function mark(on){ dirty = on; wrap.setAttribute('data-dirty', on ? '1' : '0'); }

    function pt(e){ var r = cv.getBoundingClientRect();
                    return { x: e.clientX - r.left, y: e.clientY - r.top }; }

    cv.addEventListener('pointerdown', function(e){
      if (signed || mode !== 'draw') return;
      drawing = true; cv.setPointerCapture(e.pointerId);
      var q = pt(e); ctx.beginPath(); ctx.moveTo(q.x, q.y);
      ctx.lineTo(q.x + 0.1, q.y + 0.1); ctx.stroke(); mark(true);
    });
    cv.addEventListener('pointermove', function(e){
      if (!drawing) return; var q = pt(e); ctx.lineTo(q.x, q.y); ctx.stroke();
    });
    ['pointerup','pointercancel','pointerleave'].forEach(function(ev){
      cv.addEventListener(ev, function(){ drawing = false; });
    });

    function typeSig(){
      var r = cv.getBoundingClientRect(), t = (name.value || '').trim();
      ctx.clearRect(0, 0, r.width, r.height); mark(false);
      if (!t) return;
      var size = 40;
      ctx.textBaseline = 'middle';
      do { ctx.font = 'italic 500 ' + size + "px 'Poppins', serif"; size -= 1; }
      while (ctx.measureText(t).width > r.width - 28 && size > 12);
      ctx.fillText(t, 14, r.height / 2); mark(true);
    }

    modes.forEach(function(m){
      m.addEventListener('click', function(){
        if (signed) return;
        mode = m.getAttribute('data-mode');
        modes.forEach(function(x){
          x.setAttribute('aria-pressed', String(x === m)); });
        cv.style.cursor = mode === 'draw' ? 'crosshair' : 'default';
        var r = cv.getBoundingClientRect();
        ctx.clearRect(0, 0, r.width, r.height); mark(false);
        if (mode === 'type') typeSig();
      });
    });
    name.addEventListener('input', function(){ if (mode === 'type' && !signed) typeSig(); });

    function lock(on){
      signed = on;
      name.readOnly = on;
      pill.textContent = on ? 'Signed' : 'Unsigned';
      pill.setAttribute('data-state', on ? 'signed' : 'unsigned');
      go.textContent = on ? 'Edit' : 'Sign';
      cv.hidden = on; img.hidden = !on;
      cv.style.cursor = on ? 'default' : (mode === 'draw' ? 'crosshair' : 'default');
    }

    function store(){
      state[id] = signed
        ? { name: name.value, date: dateB.textContent, sig: img.src }
        : null;
      save(state);
    }

    f.addEventListener('submit', function(e){
      e.preventDefault();
      if (signed) { lock(false); store(); return; }
      if (!name.value.trim()) { name.focus(); name.reportValidity
        ? name.setCustomValidity('') : 0; name.placeholder = 'Your full name is needed';
        return; }
      if (!dirty) { wrap.animate
        ? wrap.animate([{transform:'translateX(-4px)'},{transform:'translateX(4px)'},
                        {transform:'none'}], {duration:220}) : 0;
        return; }
      img.src = cv.toDataURL('image/png');
      img.alt = 'Signature of ' + name.value.trim();
      dateB.textContent = today();
      lock(true); store();
    });

    clr.addEventListener('click', function(){
      if (signed) lock(false);
      var r = cv.getBoundingClientRect();
      ctx.clearRect(0, 0, r.width, r.height); mark(false);
      dateB.innerHTML = '&mdash;'; store();
    });

    // restore
    fit();
    var was = state[id];
    if (was && was.sig) {
      name.value = was.name || '';
      dateB.textContent = was.date || today();
      img.src = was.sig; img.alt = 'Signature of ' + (was.name || '');
      mark(true); lock(true);
    }
    addEventListener('resize', function(){ if (!signed) fit(); });
  });

  var pr = document.getElementById('sign-print');
  if (pr) pr.addEventListener('click', function(){ window.print(); });
})();
</script>
</body>
</html>
"""

out = (PAGE.replace("@@NAV@@", "".join(nav))
           .replace("@@THESIS@@", THESIS)
           .replace("@@META@@", metarows)
           .replace("@@FIGS@@", figs)
           .replace("@@BLOCKS@@", "\n".join(blocks)))
open(OUT, "w", encoding="utf-8").write(out)
print(f"wrote {OUT} ({os.path.getsize(OUT):,} bytes; {len(sections)} sections)")
