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
        dense = " dense" if len(d["rows"]) >= 5 else ""
        parts.append(f'<div class="rows{dense}">{rows}</div>')
    return '<div class="s s-content">' + "".join(parts) + "</div>"

slides = "\n".join(f'<section class="slide" id="s{i}" data-n="{i}">{slide_html(d,i)}</section>'
                   for i, d in enumerate(SLIDES, 1))

CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
/* Brand Book Ed. 02, locked May 2026 */
:root{--ink:#111111;--charcoal:#1A1A1A;--cream:#FAF8F4;--grey:#EDEBEA;--blue:#2D5BFF;--muted:#666666;
  /* one scale unit = 1/1280 of the reference canvas, tracking whichever edge binds,
     so every brand size below is its exact px value at 1280x720 and grows with the page */
  --k:min(0.078125vw, 0.13888vh)}
html{scroll-snap-type:y mandatory;scroll-behavior:smooth}
body{background:var(--cream);color:var(--ink);
  font-family:'Poppins',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased}
.slide{height:100vh;height:100svh;scroll-snap-align:start;scroll-snap-stop:always;position:relative}
/* fail-safe reveal: visible by default, JS opts in */
.slide .s{opacity:1}
html.js-rv .slide .s{opacity:0;transition:opacity .45s ease}
html.js-rv .slide.in .s{opacity:1}

/* the slide fills the page. 96px of 1280 = the brand's 1in margin */
.s{position:absolute;inset:0;background:var(--cream);
  padding:calc(var(--k)*96) calc(var(--k)*96) calc(var(--k)*104);
  display:flex;flex-direction:column}
.bar{font-size:max(10px,calc(var(--k)*12));font-weight:500;letter-spacing:.18em;
  text-transform:uppercase;color:var(--ink)}

/* 01 title */
.s-title .t-block{margin-top:auto}
.s-title h1{font-size:calc(var(--k)*96);font-weight:600;line-height:1.04;letter-spacing:-.03em;
  max-width:19ch;text-wrap:balance}
.s-title .sub{font-size:calc(var(--k)*28);font-weight:300;margin-top:calc(var(--k)*32);max-width:52ch;line-height:1.4}
.s-title .date{position:absolute;right:calc(var(--k)*96);bottom:calc(var(--k)*96);
  font-size:max(10px,calc(var(--k)*14));color:var(--muted)}

/* 03 divider */
.s-div{background:var(--ink);color:var(--cream)}
.s-div .bar{color:var(--cream);font-weight:300}
.s-div .d-mid{flex:1;display:flex;flex-direction:column;justify-content:center}
.s-div h2{font-size:calc(var(--k)*160);font-weight:300;line-height:.98;letter-spacing:-.035em;color:var(--cream)}
.s-div .strap{font-size:calc(var(--k)*20);font-weight:300;color:var(--cream);margin-top:calc(var(--k)*24);max-width:46ch}

/* 02 content */
.head{font-size:calc(var(--k)*56);font-weight:500;line-height:1.14;letter-spacing:-.025em;
  margin-top:calc(var(--k)*56);max-width:22ch;text-wrap:balance}
.body{font-size:calc(var(--k)*18);line-height:1.62;margin-top:auto;max-width:70ch}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:calc(var(--k)*32);margin-top:auto}
.stats + .body{margin-top:calc(var(--k)*40)}
.stat{border-top:1px solid var(--grey);padding-top:calc(var(--k)*18);
  display:flex;flex-direction:column;gap:calc(var(--k)*12)}
.stat .n{font-size:calc(var(--k)*46);font-weight:600;letter-spacing:-.035em;line-height:1}
.stat .l{font-size:max(10px,calc(var(--k)*14));line-height:1.45;color:var(--muted)}
.rows{margin-top:calc(var(--k)*48);display:flex;flex-direction:column}
.r{display:grid;grid-template-columns:minmax(0,0.34fr) minmax(0,1fr);gap:calc(var(--k)*40);
  border-top:1px solid var(--grey);padding:calc(var(--k)*18) 0}
.r:last-child{border-bottom:1px solid var(--grey)}
.rows.dense{margin-top:calc(var(--k)*30)}
.rows.dense .r{padding:calc(var(--k)*12) 0}
.rows.dense .rk{font-size:calc(var(--k)*17)}
.rows.dense .rv{font-size:calc(var(--k)*16);line-height:1.42}
.rows.dense ~ *,.head:has(+ .rows.dense){margin-top:calc(var(--k)*40)}
.rk{font-size:calc(var(--k)*19);font-weight:600;line-height:1.3}
.rv{font-size:calc(var(--k)*18);line-height:1.5;color:var(--muted)}

/* 05 closer */
.s-close .c-mid{margin:auto 0}
.s-close h2{font-size:calc(var(--k)*160);font-weight:600;line-height:1;letter-spacing:-.04em}
.s-close .c-line{font-size:calc(var(--k)*18);margin-top:calc(var(--k)*16);max-width:64ch}
.s-close .c-line:first-of-type{margin-top:calc(var(--k)*56)}

/* chrome */
#hud{position:fixed;left:0;right:0;bottom:0;height:46px;display:flex;align-items:center;
  justify-content:space-between;padding:0 20px;font-size:11px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--muted);pointer-events:none;z-index:5;
  mix-blend-mode:difference;filter:invert(1) grayscale(1) contrast(2)}
#hud .k{pointer-events:auto;display:flex;gap:8px;align-items:center}
#hud button{background:none;border:0;color:inherit;font:inherit;letter-spacing:inherit;
  text-transform:inherit;padding:6px 4px;cursor:pointer;opacity:.75}
#hud button:hover{opacity:1}
#hud button[disabled]{opacity:.25;cursor:default}
#count{font-variant-numeric:tabular-nums}
#dots{position:fixed;top:0;left:0;height:2px;width:0;background:var(--blue);z-index:6}
#cue{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);font-size:10px;
  letter-spacing:.18em;text-transform:uppercase;color:var(--muted);z-index:5;pointer-events:none;
  transition:opacity .3s ease;animation:bob 2.4s ease-in-out infinite}
#cue.gone{opacity:0}
@keyframes bob{0%,100%{transform:translate(-50%,0)}50%{transform:translate(-50%,5px)}}

@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}#cue{animation:none}
  html.js-rv .slide .s{transition:none;opacity:1}}
/* below the 16:9 reference the fixed canvas would crowd, so let type breathe on its own scale */
@media (max-width:820px){
  :root{--k:min(0.115vw, 0.1vh)}
  .s{padding:26px 22px 56px}
  .stats{grid-template-columns:repeat(2,1fr)}
  .r{grid-template-columns:1fr;gap:6px}
}
@media print{
  html{scroll-snap-type:none}
  #hud,#dots,#cue{display:none}
  .slide{height:auto;page-break-after:always;break-after:page}
  .s{position:relative;inset:auto;aspect-ratio:16/9;opacity:1!important;
    --k:min(0.078125vw, 0.13888vh)}
  @page{size:A4 landscape;margin:0}
}
"""

JS = """
(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide'));
  var n=slides.length;
  var count=document.getElementById('count'), bar=document.getElementById('dots');
  var cue=document.getElementById('cue');
  var prev=document.getElementById('prev'), next=document.getElementById('next');
  var i=0;

  // Sizing is CSS: --k scales every brand dimension off the viewport, so the
  // slide fills the page rather than sitting letterboxed inside it.


  function goto(k){
    k=Math.max(0,Math.min(n-1,k));
    slides[k].scrollIntoView({block:'center'});
  }

  var ticking=false;
  function onScroll(){
    if(ticking) return; ticking=true;
    requestAnimationFrame(function(){
      ticking=false;
      var mid=innerHeight/2, best=0, bestd=Infinity;
      slides.forEach(function(el,j){
        var r=el.getBoundingClientRect(), d=Math.abs(r.top+r.height/2-mid);
        if(d<bestd){bestd=d; best=j;}
      });
      if(best!==i){
        i=best;
        count.textContent=(i+1)+' / '+n;
        prev.disabled=(i===0); next.disabled=(i===n-1);
        if(history.replaceState) history.replaceState(null,'','#'+(i+1));
      }
      var max=document.documentElement.scrollHeight-innerHeight;
      bar.style.width=(max>0?(scrollY/max*100):100)+'%';
      if(cue&&scrollY>40) cue.classList.add('gone');
    });
  }

  // Reveal as each slide arrives. Set up inside try/catch and only hide the
  // slides once the observer is actually running, so a failure here leaves a
  // readable page rather than a blank one.
  try{
    if('IntersectionObserver' in window){
      var io=new IntersectionObserver(function(es){
        es.forEach(function(e){ if(e.isIntersecting) e.target.classList.add('in'); });
      },{threshold:0.35});
      document.documentElement.classList.add('js-rv');
      slides.forEach(function(el){io.observe(el);});
    }
  }catch(err){ document.documentElement.classList.remove('js-rv'); }

  addEventListener('keydown',function(e){
    if(e.metaKey||e.ctrlKey||e.altKey) return;
    if(['ArrowRight','ArrowDown','PageDown',' '].indexOf(e.key)>-1){e.preventDefault();goto(i+1);}
    else if(['ArrowLeft','ArrowUp','PageUp'].indexOf(e.key)>-1){e.preventDefault();goto(i-1);}
    else if(e.key==='Home'){e.preventDefault();goto(0);}
    else if(e.key==='End'){e.preventDefault();goto(n-1);}
  });
  prev.addEventListener('click',function(){goto(i-1);});
  next.addEventListener('click',function(){goto(i+1);});
  document.getElementById('print').addEventListener('click',function(){window.print();});
  addEventListener('scroll',onScroll,{passive:true});
  addEventListener('resize',onScroll);
  addEventListener('hashchange',function(){
    var k=parseInt(location.hash.slice(1),10); if(k&&k-1!==i) goto(k-1);
  });

  count.textContent='1 / '+n;
  prev.disabled=true;
  var start=parseInt(location.hash.slice(1),10);
  if(start&&start>1){ slides[Math.min(n,start)-1].scrollIntoView({block:'center',behavior:'auto'}); }
  onScroll();
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
<main id="deck">
{slides}
</main>
<div id="cue">Scroll</div>
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
