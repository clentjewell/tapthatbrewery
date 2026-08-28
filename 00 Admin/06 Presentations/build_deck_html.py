"""Render the same deck content as a Cloudflare page. Reads deck_content.py."""
import html, os
from deck_content import SLIDES, TITLE

OUT = "/home/user/tapthatbrewery/00 Admin/11 Final Outputs/site/deck.html"
def esc(t):  return html.escape(t).replace("\n","<br>")
def flow(t): return html.escape(t).replace("\n"," ")   # pptx line breaks are not the page's

def slide_html(d, n):
    t = d["type"]
    if t == "title":
        return f'''<div class="s s-title">
  <div class="bar">{esc(d["bar"])}</div>
  <div class="t-block">
    <h1>{flow(d["title"])}</h1>
    <p class="sub">{esc(d.get("subtitle",""))}</p>
  </div>
  <div class="date">{esc(d.get("date",""))}</div>
</div>'''
    if t == "divider":
        strap = f'<p class="strap">{esc(d["strapline"])}</p>' if d.get("strapline") else ""
        return f'''<div class="s s-div">
  <div class="bar">{esc(d["num"])}</div>
  <div class="d-mid"><h2>{esc(d["title"])}</h2></div>
  {strap}
</div>'''
    if t == "closer":
        return f'''<div class="s s-close">
  <div class="c-mid"><h2>Next.</h2>
    <p class="c-line">{esc(d["action"])}</p>
    <p class="c-line">{esc(d["owner"])}</p>
  </div>
</div>'''
    parts = [f'<div class="bar">{esc(d["eyebrow"])}</div>',
             f'<h2 class="head">{flow(d["headline"])}</h2>']
    if d.get("body"):  parts.append(f'<p class="body">{esc(d["body"])}</p>')
    if d.get("stats"):
        cells = "".join(f'<div class="stat"><span class="n">{esc(a)}</span>'
                        f'<span class="l">{esc(b)}</span></div>' for a, b in d["stats"])
        parts.append(f'<div class="stats">{cells}</div>')
    if d.get("rows"):
        rows = "".join(f'<div class="r"><div class="rk">{esc(a)}</div>'
                       f'<div class="rv">{esc(b)}</div></div>' for a, b in d["rows"])
        parts.append(f'<div class="rows">{rows}</div>')
    return '<div class="s s-content">' + "".join(parts) + "</div>"

slides = "\n".join(f'<section class="slide" id="s{i}" data-n="{i}">{slide_html(d,i)}</section>'
                   for i, d in enumerate(SLIDES, 1))

CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--ink:#111111;--cream:#FAF8F4;--blue:#2D5BFF;--grey:#666666;--line:#EDEBEA}
html,body{height:100%}
body{background:#0E0E0E;font-family:'Poppins',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
  color:var(--ink);overflow:hidden}
#stage{position:fixed;inset:0;display:grid;place-items:center}
.slide{width:1280px;height:720px;position:absolute;opacity:0;pointer-events:none;
  transform-origin:center center;transition:opacity .28s ease}
.slide.on{opacity:1;pointer-events:auto}
.s{width:100%;height:100%;background:var(--cream);padding:76px 96px;display:flex;flex-direction:column;position:relative}
.bar{font-size:11px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:var(--ink)}
/* title */
.s-title .t-block{margin-top:auto}
.s-title h1{font-size:64px;font-weight:600;line-height:1.07;letter-spacing:-.03em;max-width:20ch;text-wrap:balance}
.s-title .sub{font-size:19px;font-weight:300;margin-top:22px;max-width:60ch}
.s-title .date{position:absolute;right:96px;bottom:60px;font-size:12px;color:var(--grey)}
/* divider */
.s-div{background:var(--ink);color:var(--cream)}
.s-div .bar{color:var(--cream)}
.s-div .d-mid{flex:1;display:grid;place-items:start center;align-content:center}
.s-div h2{font-size:104px;font-weight:300;line-height:1;letter-spacing:-.03em;color:var(--cream)}
.s-div .strap{font-size:17px;font-weight:300;color:var(--cream)}
/* content */
.head{font-size:40px;font-weight:500;line-height:1.18;letter-spacing:-.022em;margin-top:52px;max-width:26ch;text-wrap:balance}
.body{font-size:16px;line-height:1.62;margin-top:auto;max-width:74ch;padding-bottom:8px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:28px;margin-top:auto;padding-bottom:6px}
.stat{border-top:1px solid var(--line);padding-top:14px;display:flex;flex-direction:column;gap:9px}
.stat .n{font-size:34px;font-weight:600;letter-spacing:-.03em;line-height:1}
.stat .l{font-size:12px;line-height:1.42;color:var(--grey)}
.rows{margin-top:34px;display:flex;flex-direction:column}
.r{display:grid;grid-template-columns:280px 1fr;gap:34px;border-top:1px solid var(--line);padding:15px 0}
.r:last-child{border-bottom:1px solid var(--line)}
.rk{font-size:15px;font-weight:600;line-height:1.35}
.rv{font-size:15px;line-height:1.45;color:var(--grey)}
/* closer */
.s-close .c-mid{margin:auto 0}
.s-close h2{font-size:104px;font-weight:600;line-height:1;letter-spacing:-.035em}
.s-close .c-line{font-size:16px;margin-top:14px}
.s-close .c-line:first-of-type{margin-top:38px}
/* chrome */
#hud{position:fixed;left:0;right:0;bottom:0;height:52px;display:flex;align-items:center;
  justify-content:space-between;padding:0 20px;color:#EDEBEA;font-size:12px;letter-spacing:.06em;
  background:linear-gradient(to top,rgba(0,0,0,.55),transparent);pointer-events:none}
#hud .k{pointer-events:auto;display:flex;gap:14px;align-items:center}
#hud button{background:none;border:1px solid rgba(237,235,234,.3);color:#EDEBEA;border-radius:6px;
  padding:5px 11px;font:inherit;cursor:pointer}
#hud button:hover{border-color:var(--blue);color:#fff}
#count{font-variant-numeric:tabular-nums}
#dots{position:fixed;top:0;left:0;height:2px;background:var(--blue);transition:width .28s ease}
@media print{
  body{background:#fff;overflow:visible}
  #hud,#dots{display:none}
  #stage{position:static;display:block}
  .slide{position:static;opacity:1!important;transform:none!important;page-break-after:always;
    width:100%;height:auto;aspect-ratio:16/9}
  @page{size:A4 landscape;margin:0}
}
"""

JS = """
(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide'));
  var n=slides.length, i=0, stage=document.getElementById('stage');
  function fit(){
    var s=Math.min(window.innerWidth/1280,(window.innerHeight-52)/720);
    slides.forEach(function(el){el.style.transform='scale('+s+')';});
  }
  function show(k){
    i=Math.max(0,Math.min(n-1,k));
    slides.forEach(function(el,j){el.classList.toggle('on',j===i);});
    document.getElementById('count').textContent=(i+1)+' / '+n;
    document.getElementById('dots').style.width=((i+1)/n*100)+'%';
    if(history.replaceState) history.replaceState(null,'','#'+(i+1));
  }
  addEventListener('keydown',function(e){
    if(['ArrowRight','PageDown',' '].indexOf(e.key)>-1){e.preventDefault();show(i+1);}
    if(['ArrowLeft','PageUp'].indexOf(e.key)>-1){e.preventDefault();show(i-1);}
    if(e.key==='Home')show(0); if(e.key==='End')show(n-1);
  });
  stage.addEventListener('click',function(e){show(e.clientX<window.innerWidth*0.3?i-1:i+1);});
  document.getElementById('prev').addEventListener('click',function(e){e.stopPropagation();show(i-1);});
  document.getElementById('next').addEventListener('click',function(e){e.stopPropagation();show(i+1);});
  document.getElementById('print').addEventListener('click',function(e){e.stopPropagation();window.print();});
  addEventListener('resize',fit);
  addEventListener('hashchange',function(){
    var k=parseInt(location.hash.slice(1),10); if(k&&k-1!==i) show(k-1);
  });
  fit(); show(Math.max(0,(parseInt(location.hash.slice(1),10)||1)-1));
})();
"""

page = f"""<meta charset="utf-8">
<title>{html.escape(TITLE)} · Tap That Brewery</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
<div id="dots"></div>
<div id="stage">
{slides}
</div>
<div id="hud">
  <div class="k">
    <button id="prev">Prev</button><button id="next">Next</button><button id="print">Print</button>
  </div>
  <span id="count"></span>
</div>
<script>{JS}</script>
"""
open(OUT,"w",encoding="utf-8").write(page)
print(f"wrote {OUT} ({len(page):,} chars, {len(SLIDES)} slides)")
