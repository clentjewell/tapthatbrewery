"""Assemble the five plan sheets into one self-contained web page.

The sheets are print artefacts at a fixed 420 x 297mm, so the page does not
reflow them. It scales each one to the reader's width and keeps the design
exactly as it prints, which is the point: what you read on the link and what
comes out of the printer are the same sheet.

The shell around them is the only thing designed here. It goes dark when the
reader's theme is dark; the sheets stay white, because paper does.

    python3 build_plan_web.py <out.html>
"""

import base64
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent / "site"

SHEETS = [
    ("summary",    "summary.html",    "The plan",
     "The north star, the four plans in one line each, and what Justin decides first."),
    ("business",   "business.html",   "Business",
     "Where the money actually is, the four units, and the canning question."),
    ("brand",      "brand.html",      "Brand",
     "The position, the enemy, designing for her, and the proof already owned."),
    ("sales",      "sales.html",      "Sales and marketing",
     "Connect the system first. Then convert the owners who are already sold."),
    ("activation", "activation.html", "Activation",
     "Ninety days, the destination programme, partnerships, and who does what."),
]


def data_uri(rel):
    b = (SITE / rel).read_bytes()
    return "data:image/png;base64," + base64.b64encode(b).decode("ascii")


def main():
    out = pathlib.Path(sys.argv[1])
    css = ((HERE / "oap.css").read_text(encoding="utf-8")
           + "\n" + (HERE / "oap-plan.css").read_text(encoding="utf-8"))

    marks = {m: data_uri(f"brand/{m}") for m in
             ("tapthat-icon.png", "jewell-wordmark.png")}

    blocks, nav = [], []
    for i, (slug, fname, label, blurb) in enumerate(SHEETS, 1):
        frag = (HERE / "oap-plan" / fname).read_text(encoding="utf-8")
        for mark, uri in marks.items():
            frag = frag.replace(f'src="brand/{mark}"', f'src="{uri}"')
        nav.append(f'<button class="nav-b" data-go="s-{slug}">'
                   f'<span class="n">{i:02d}</span>{label}</button>')
        blocks.append(
            f'<section class="plate" id="s-{slug}">\n'
            f'  <header class="plate-head">\n'
            f'    <span class="plate-n">Sheet {i:02d} of 5</span>\n'
            f'    <h2>{label}</h2>\n'
            f'    <p>{blurb}</p>\n'
            f'  </header>\n'
            f'  <div class="scroller"><div class="stage">{frag}</div></div>\n'
            f'</section>')

    page = (PAGE
            .replace("@@CSS@@", css)
            .replace("@@NAV@@", "\n      ".join(nav))
            .replace("@@BLOCKS@@", "\n".join(blocks))
            .replace("@@JP@@", marks["jewell-wordmark.png"]))
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size:,} bytes)")


PAGE = r"""<title>Tap That Plan on a Page</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

/* ---- shell tokens. Light is the bare :root so the un-stamped
   system-default state resolves; dark redefines the same names. ---- */
:root{
  --ground:#EEEDEA;        /* a grey pulled a touch warm, off the paper */
  --ground-2:#E4E3DF;
  --shell-ink:#15181C;
  --shell-dim:#5A6069;
  --shell-line:#D3D2CD;
  --shell-bar:rgba(238,237,234,.88);
  --accent:#0066FF;
  --shadow:0 1px 2px rgba(14,23,31,.08),0 12px 34px rgba(14,23,31,.14);
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ground:#16181B;
    --ground-2:#101214;
    --shell-ink:#ECEBE8;
    --shell-dim:#9AA0A8;
    --shell-line:#2C3035;
    --shell-bar:rgba(22,24,27,.88);
    --accent:#5B9BFF;
    --shadow:0 1px 2px rgba(0,0,0,.5),0 16px 44px rgba(0,0,0,.55);
  }
}
:root[data-theme="dark"]{
  --ground:#16181B; --ground-2:#101214; --shell-ink:#ECEBE8;
  --shell-dim:#9AA0A8; --shell-line:#2C3035; --shell-bar:rgba(22,24,27,.88);
  --accent:#5B9BFF;
  --shadow:0 1px 2px rgba(0,0,0,.5),0 16px 44px rgba(0,0,0,.55);
}

body{
  background:var(--ground);
  color:var(--shell-ink);
  font-family:'Poppins',system-ui,-apple-system,sans-serif;
  -webkit-font-smoothing:antialiased;
}
*{box-sizing:border-box;}

/* ---- top bar ---- */
.bar{
  position:sticky; top:env(safe-area-inset-top,0px); z-index:40;
  background:var(--shell-bar);
  backdrop-filter:blur(14px); -webkit-backdrop-filter:blur(14px);
  border-bottom:1px solid var(--shell-line);
}
.bar-in{
  max-width:1560px; margin:0 auto;
  padding-block:10px; padding-left:max(16px,env(safe-area-inset-left));
  padding-right:max(16px,env(safe-area-inset-right));
  display:flex; align-items:center; gap:14px; flex-wrap:wrap;
}
.wm{height:17px;width:auto;display:block;flex:none;}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .wm{filter:invert(1);}}
:root[data-theme="dark"] .wm{filter:invert(1);}
.bar-t{
  font-size:11px; font-weight:600; letter-spacing:.13em;
  text-transform:uppercase; color:var(--shell-dim); white-space:nowrap;
}
.nav{display:flex; gap:4px; flex-wrap:wrap; margin-left:auto;}
.nav-b{
  font:inherit; font-size:12px; font-weight:500; color:var(--shell-dim);
  background:none; border:1px solid transparent; border-radius:7px;
  padding:5px 10px; cursor:pointer; display:flex; align-items:baseline; gap:6px;
  transition:color .13s, border-color .13s, background .13s;
}
.nav-b .n{
  font-size:9.5px; font-weight:700; letter-spacing:.06em;
  color:var(--accent); font-variant-numeric:tabular-nums;
}
.nav-b:hover{color:var(--shell-ink); border-color:var(--shell-line);}
.nav-b[aria-current="true"]{
  color:var(--shell-ink); border-color:var(--shell-line);
  background:var(--ground-2);
}
.nav-b:focus-visible{outline:2px solid var(--accent); outline-offset:2px;}

.zoom{display:flex; border:1px solid var(--shell-line); border-radius:8px;
  overflow:hidden; flex:none;}
.zoom button{
  font:inherit; font-size:11px; font-weight:600; letter-spacing:.04em;
  color:var(--shell-dim); background:none; border:0; padding:5px 11px;
  cursor:pointer; transition:color .13s, background .13s;
}
.zoom button+button{border-left:1px solid var(--shell-line);}
.zoom button[aria-pressed="true"]{background:var(--accent); color:#fff;}
.zoom button:focus-visible{outline:2px solid var(--accent); outline-offset:-2px;}

/* ---- page ---- */
.wrap{
  max-width:1560px; margin:0 auto;
  padding-block:30px 60px;
  padding-left:max(16px,env(safe-area-inset-left));
  padding-right:max(16px,env(safe-area-inset-right));
  display:flex; flex-direction:column; gap:44px;
}
.intro{display:flex; flex-direction:column; gap:12px; max-width:62ch;}
.intro h1{
  font-size:clamp(25px,4.2vw,40px); font-weight:700; letter-spacing:-.028em;
  line-height:1.08; text-wrap:balance; margin:0;
}
.intro .lede{font-size:15px; line-height:1.6; color:var(--shell-dim); margin:0;}
.meta{
  display:flex; gap:7px; flex-wrap:wrap; margin-top:2px;
  font-size:10.5px; font-weight:600; letter-spacing:.1em; text-transform:uppercase;
}
.meta span{
  border:1px solid var(--shell-line); border-radius:999px; padding:4px 11px;
  color:var(--shell-dim);
}
.meta span.hot{border-color:var(--accent); color:var(--accent);}

.plate{display:flex; flex-direction:column; gap:14px;}
.plate-head{display:flex; flex-direction:column; gap:5px; max-width:66ch;}
.plate-n{
  font-size:10px; font-weight:700; letter-spacing:.15em; text-transform:uppercase;
  color:var(--accent); font-variant-numeric:tabular-nums;
}
.plate-head h2{
  font-size:clamp(19px,2.6vw,25px); font-weight:600; letter-spacing:-.02em;
  line-height:1.15; margin:0; text-wrap:balance;
}
.plate-head p{font-size:13.5px; line-height:1.55; color:var(--shell-dim); margin:0;}

/* The sheet is a fixed-size artefact: scaled to fit, or scrolled at full size. */
.scroller{overflow-x:auto; overflow-y:hidden; border-radius:3px;}
.stage{transform-origin:top left;}
.stage .oap .sheet{box-shadow:var(--shadow); border-color:rgba(0,0,0,.10);}

.foot{
  border-top:1px solid var(--shell-line); padding-top:18px;
  font-size:12.5px; line-height:1.65; color:var(--shell-dim); max-width:70ch;
}
.foot strong{color:var(--shell-ink); font-weight:600;}

@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto !important;}}

/* the pack stylesheet, scoped to .oap */
@@CSS@@
</style>

<div class="bar">
  <div class="bar-in">
    <img class="wm" src="@@JP@@" alt="Jewell Projects">
    <span class="bar-t">Tap That Brewery</span>
    <nav class="nav" aria-label="Sheets">
      @@NAV@@
    </nav>
    <div class="zoom" role="group" aria-label="Sheet size">
      <button type="button" id="z-fit" aria-pressed="true">Fit</button>
      <button type="button" id="z-full" aria-pressed="false">Full size</button>
    </div>
  </div>
</div>

<main class="wrap">
  <div class="intro">
    <h1>The plan on a page</h1>
    <p class="lede">Five A3 sheets: a summary, then one page each for the
      business, the brand, sales and marketing, and activation. Built from the
      catch-up on 15 September, then reworked around Justin's own plan on a
      page and one-page business plan, received the next day. Where the two
      differ, Justin's framing, numbers and names lead, and the Jewell
      Projects recommendation stands beside them as a recommendation. Where a
      number is not settled, the sheet says so.</p>
    <div class="meta">
      <span class="hot">Draft for review</span>
      <span>v02 &middot; 16 Sept 2026</span>
      <span>A3 landscape &middot; 420 &times; 297mm</span>
    </div>
  </div>

@@BLOCKS@@

  <p class="foot"><strong>These print at true size.</strong> A3 landscape, one
    sheet per page, and the editable PowerPoint carries the same words at the
    same size, so a slide and a printed sheet are the same artefact rather than
    two versions of it. The north star is Justin's: 1,000 active keg refillers
    by year three, 250 by March 2027. The at-home cost per schooner is his
    figure too, $2.55, and the open item is making sure the live ad and every
    piece of collateral carry that one number. One figure stays deliberately
    unsettled: the split between lapsed customers who are cutting back and
    those who simply did not get around to it, which has to be read off the
    CRM before either message is written.</p>
</main>

<script>
(function(){
  var SHEET_W = 420 / 25.4 * 96;      // 420mm at 96dpi
  var SHEET_H = 297 / 25.4 * 96;
  var mode = 'fit';
  try { mode = localStorage.getItem('tt-plan-zoom') || 'fit'; } catch (e) {}

  var stages = [].slice.call(document.querySelectorAll('.stage'));
  var fitB = document.getElementById('z-fit');
  var fullB = document.getElementById('z-full');

  function layout(){
    stages.forEach(function(st){
      var box = st.parentNode;                       // .scroller
      var k = mode === 'full' ? 1
            : Math.min(1, box.clientWidth / SHEET_W);
      st.style.transform = 'scale(' + k + ')';
      st.style.width = SHEET_W + 'px';
      box.style.height = Math.ceil(SHEET_H * k) + 'px';
    });
  }

  function setMode(m){
    mode = m;
    fitB.setAttribute('aria-pressed', String(m === 'fit'));
    fullB.setAttribute('aria-pressed', String(m === 'full'));
    try { localStorage.setItem('tt-plan-zoom', m); } catch (e) {}
    layout();
  }

  fitB.addEventListener('click', function(){ setMode('fit'); });
  fullB.addEventListener('click', function(){ setMode('full'); });

  // Nav scrolls to a sheet and marks itself current.
  var btns = [].slice.call(document.querySelectorAll('.nav-b'));
  btns.forEach(function(b){
    b.addEventListener('click', function(){
      var t = document.getElementById(b.dataset.go);
      if (!t) return;
      var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    });
  });

  if ('IntersectionObserver' in window) {
    var seen = new IntersectionObserver(function(es){
      es.forEach(function(e){
        if (!e.isIntersecting) return;
        btns.forEach(function(b){
          b.setAttribute('aria-current',
            String(b.dataset.go === e.target.id));
        });
      });
    }, { rootMargin: '-15% 0px -70% 0px' });
    document.querySelectorAll('.plate').forEach(function(p){ seen.observe(p); });
  }

  setMode(mode);
  window.addEventListener('resize', layout);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(layout);
})();
</script>
"""

if __name__ == "__main__":
    main()
