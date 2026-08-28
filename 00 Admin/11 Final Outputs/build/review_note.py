"""
Generate the review note for Christy Kilmartin: every finding from the
27 August review, and the document it landed in.

Reads the same REVIEW_BEARS_ON map the audit checks against, so the note cannot
claim something landed that the audit does not verify. If a finding has not
landed, it says so rather than quietly omitting the row.

    python3 review_note.py     # writes site/review-note.html
"""
import os, re, sys, html, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT  = os.path.join(HERE, "..", "site", "review-note.html")
sys.path.insert(0, HERE)
from audit_pack import REVIEW_BEARS_ON, REVIEW_MARKERS   # noqa: E402

def catalogue():
    src = open(os.path.join(HERE, "build_pack.py"), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"CAT = \{.*?\n\}", src, re.S).group(0), ns)
    out = {}
    for n, v in ns["CAT"].items():
        out[{205: "20A", 206: "20B"}.get(n) or f"{n:02d}"] = (v[0], v[1], v[2])
    return out

CAT = catalogue()

def landed(num, marker):
    f = [x for x in glob.glob(os.path.join(ROOT, "0[123] */02 Working Drafts/*.md"))
         if os.path.basename(x).startswith(num + "__")]
    if not f:
        return False
    return bool(re.search(REVIEW_MARKERS[marker], open(f[0], encoding="utf-8").read(), re.I))

# The findings grouped as Christy raised them, each pointing at its documents.
GROUPS = [
 ("What Discover did not say", [
   ("The business is losing money, and it is nowhere in the set", ["23", "21", "24"]),
   ("The taproom and the refill model are zero-sum", ["17", "23", "21", "50"]),
   ("Nobody has priced the cost drivers, 27 taps included", ["21", "23", "14"]),
   ("The commercial opportunity is buried: one account is worth ten households", ["12", "50", "24"]),
 ]),
 ("Claims we can no longer lean on", [
   ("The 20&ndash;30% taproom conversion has never been measured", ["30", "17"]),
   ("The census is fifty self-selected people, not the anchor", ["31", "27", "06"]),
   ("A thousand giveaway entries is not a thousand buyers", ["30"]),
 ]),
 ("The three moves, ranked", [
   ("Buy the system-owner databases", ["24", "16", "77"]),
   ("A direct Harvey Norman arrangement", ["24", "16"]),
   ("Tour operators, commercial and wholesale, properly resourced", ["24", "12", "50", "71"]),
   ("Taproom traffic via social, ranked below all three", ["43", "46", "64", "77"]),
 ]),
 ("Product and pricing", [
   ("Cut to about six core beers plus seasonals", ["14"]),
   ("Reverse razor-and-blades: lease-to-buy priced like a gym membership", ["15", "07"]),
   ("A low-alcohol line as a reactivation product, not a trend note", ["14", "08", "28"]),
   ("The RTD range is an afterthought; women are covered, not catered for", ["07", "14"]),
   ("Second Earth: premium beats the middle ground", ["32", "10"]),
   ("Delivery priced as a member benefit", ["15"]),
 ]),
 ("CRM and loyalty", [
   ("The blanket 90-day SMS is tone-deaf; model each customer's own rhythm", ["48", "47", "28"]),
   ("10/60/40 &mdash; and the 40% is where the growth is", ["28", "17", "47"]),
   ("Simplify loyalty: every tenth keg free", ["48", "15"]),
 ]),
 ("The taproom", [
   ("Destination, not journey: restrict hours, run it as an event venue", ["21", "50"]),
   ("The puppy-dog close &mdash; a system in a booth", ["16"]),
 ]),
 ("Website and brand", [
   ("The full above-the-fold teardown; Drink Hopper as the reference", ["37", "39"]),
   ("The Crafted award and &ldquo;fits any system&rdquo; belong on the landing page", ["37", "39", "40", "71"]),
   ("Wholesale is missing its WIIFM entirely", ["12", "37"]),
   ("One membership across taproom and refills", ["37"]),
 ]),
 ("Closed by the review", [
   ("The competitor is Aardvark and Arrow &mdash; domain suspended, merged with Burleigh Homebrew", ["10", "40", "12"]),
 ]),
]

def rows():
    out = []
    for group, items in GROUPS:
        body = []
        for finding, docs in items:
            links, all_ok = [], True
            for d in docs:
                title, _stage, slug = CAT.get(d, ("?", "?", "#"))
                ok = d in REVIEW_BEARS_ON and landed(d, REVIEW_BEARS_ON[d][1])
                all_ok &= ok
                links.append(f'<a href="/{slug}">#{d} {html.escape(title)}</a>')
            body.append((finding, " &middot; ".join(links), all_ok))
        out.append((group, body))
    return out

CSS = """
:root{--ink:#111;--cream:#FAF8F4;--steel:#666;--rule:#D4D2D0;--blue:#0066FF;--ok:#1F8A5B}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{background:var(--cream);color:var(--ink);font-family:'Poppins',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
 line-height:1.6;padding:clamp(28px,5vw,70px);max-width:940px;margin:0 auto}
.eyebrow{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--steel)}
h1{font-size:clamp(30px,4.4vw,46px);font-weight:600;letter-spacing:-.025em;line-height:1.1;margin:14px 0 20px;max-width:22ch}
.lede{font-size:17px;max-width:64ch;color:#333}
.lede b{color:var(--ink)}
h2{font-size:15px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--steel);
 margin:44px 0 4px;padding-top:18px;border-top:1px solid var(--rule)}
.f{padding:16px 0;border-bottom:1px solid var(--rule)}
.f-t{font-size:16.5px;font-weight:500;display:flex;gap:10px;align-items:baseline}
.tick{color:var(--ok);font-size:13px;flex:0 0 auto}
.f-d{font-size:13.5px;color:var(--steel);margin-top:6px;line-height:1.75}
.f-d a{color:var(--blue);text-decoration:none;border-bottom:1px solid rgba(0,102,255,.28)}
.f-d a:hover{border-bottom-color:var(--blue)}
.note{background:#fff;border:1px solid var(--rule);border-radius:12px;padding:22px 24px;margin:34px 0;font-size:15px;max-width:70ch}
.note b{display:block;margin-bottom:6px}
footer{margin-top:54px;padding-top:20px;border-top:1px solid var(--rule);font-size:12.5px;color:var(--steel)}
@media print{body{background:#fff}a{color:var(--ink)}}
"""

def build():
    data = rows()
    total = sum(len(b) for _, b in data)
    done  = sum(1 for _, b in data for _, _, ok in b if ok)
    parts = [f"""<meta charset="utf-8">
<title>What we did with your review &middot; Tap That Brewery</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
<div class="eyebrow">Jewell Projects &middot; Tap That Brewery &middot; for Christy Kilmartin</div>
<h1>What we did with your review.</h1>
<p class="lede">Every finding from 27 August, and the document it landed in. <b>{done} of {total}</b>
worked through the set rather than noted and left. The intent is that you can check the changes
without re-reading seventy-nine documents &ndash; each row links straight to the page that carries it.</p>

<div class="note"><b>Two things we deliberately did not do.</b>
#29 Messaging by Stage and #33 Messaging &amp; Offer Architecture rest on the driver order, and whether
cost belongs in open channels is a founders' decision rather than ours. Both are marked provisional
pending CP1 instead of being rewritten in a direction the client has not chosen.</div>
"""]
    for group, body in data:
        parts.append(f"<h2>{group}</h2>")
        for finding, links, ok in body:
            tick = '<span class="tick">&#10003;</span>' if ok else '<span class="tick" style="color:#B4442E">&#9679;</span>'
            parts.append(f'<div class="f"><div class="f-t">{tick}<span>{finding}</span></div>'
                         f'<div class="f-d">{links}</div></div>')
    parts.append("""
<div class="note"><b>What we would most like your eye on.</b>
Whether the taproom framing is now hard enough, whether the commercial and wholesale reversal in
#24 goes far enough, and whether the CRM rebuild in #48 is the right answer to the blanket-clock
problem. Also: the schooner figure is still unsettled &ndash; $2.70, $2.98/$2.34 and $2.55/$3.19 all
follow from different keg prices and schooner counts, and there is a live ad running on one of them.</div>

<footer>Generated from the same record the pack is audited against, so this page cannot claim a
finding landed that the audit does not verify. Jewell Projects, 28 August 2026.</footer>""")
    open(OUT, "w", encoding="utf-8").write("\n".join(parts))
    print(f"wrote {OUT} ({done}/{total} findings verified landed)")

if __name__ == "__main__":
    build()
