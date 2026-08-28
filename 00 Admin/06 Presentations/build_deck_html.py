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

slides = "\n".join(
    f'<section class="slide" id="s{i}" data-n="{i}">'
    f'<div class="frame">{slide_html(d,i)}</div></section>'
    for i, d in enumerate(SLIDES, 1))

CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--ink:#111111;--cream:#FAF8F4;--blue:#2D5BFF;--grey:#666666;--line:#EDEBEA;--pit:#0E0E0E}
html{scroll-snap-type:y mandatory;scroll-behavior:smooth;scroll-padding-top:0}
body{background:var(--pit);font-family:'Poppins',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
  color:var(--ink);-webkit-font-smoothing:antialiased}
.slide{height:100vh;height:100svh;scroll-snap-align:center;scroll-snap-stop:always;
  display:grid;place-items:center;padding:22px 22px 58px}
.frame{position:relative;overflow:hidden}
/* fail-safe reveal: visible by default, JS opts in to the animation */
.frame>.s{opacity:1;transform:scale(var(--k,1))}
html.js-rv .frame>.s{opacity:0;transition:opacity .5s ease,filter .5s ease;filter:blur(3px)}
html.js-rv .slide.in .frame>.s{opacity:1;filter:none}
.s{width:1280px;height:720px;transform-origin:top left;background:var(--cream);
  padding:76px 96px;display:flex;flex-direction:column;position:relative;
  box-shadow:0 18px 60px rgba(0,0,0,.45)}
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
  background:linear-gradient(to top,rgba(0,0,0,.68),transparent);pointer-events:none;z-index:5}
#hud .k{pointer-events:auto;display:flex;gap:10px;align-items:center}
#hud button{background:none;border:1px solid rgba(237,235,234,.3);color:#EDEBEA;border-radius:6px;
  padding:5px 11px;font:inherit;cursor:pointer}
#hud button:hover{border-color:var(--blue);color:#fff}
#hud button[disabled]{opacity:.32;cursor:default}
#hud button[disabled]:hover{border-color:rgba(237,235,234,.3);color:#EDEBEA}
#count{font-variant-numeric:tabular-nums;pointer-events:none}
#dots{position:fixed;top:0;left:0;height:2px;width:0;background:var(--blue);z-index:6}
/* scroll cue, on the first slide only, retires once you move */
#cue{position:fixed;left:50%;bottom:19px;transform:translateX(-50%);color:#EDEBEA;font-size:11px;
  letter-spacing:.16em;text-transform:uppercase;opacity:.7;z-index:5;pointer-events:none;
  transition:opacity .3s ease;animation:bob 2.4s ease-in-out infinite}
#cue.gone{opacity:0}
@keyframes bob{0%,100%{transform:translate(-50%,0)}50%{transform:translate(-50%,6px)}}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  #cue{animation:none}
  html.js-rv .frame>.s{transition:none;filter:none;opacity:1}
}
@media print{
  html{scroll-snap-type:none}
  body{background:#fff}
  #hud,#dots,#cue{display:none}
  .slide{height:auto;padding:0;display:block;page-break-after:always;break-after:page}
  .frame{width:100%!important;height:auto!important;overflow:visible}
  .s{opacity:1!important;filter:none!important;transform:none!important;
    width:100%;height:auto;aspect-ratio:16/9;box-shadow:none}
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

  // Scale each 1280x720 canvas to its section, sizing the frame to the scaled
  // box so nothing overflows the column and the page never scrolls sideways.
  function fit(){
    // Measure the section's CONTENT box. getBoundingClientRect() includes the
    // padding, and scaling against that pushes the canvas wider than the column.
    var el=slides[0], cs=getComputedStyle(el);
    var w=el.clientWidth -parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
    var h=el.clientHeight-parseFloat(cs.paddingTop) -parseFloat(cs.paddingBottom);
    var k=Math.min(w/1280,h/720);
    slides.forEach(function(el){
      var f=el.querySelector('.frame'), s=el.querySelector('.s');
      f.style.width=(1280*k)+'px'; f.style.height=(720*k)+'px';
      s.style.setProperty('--k',k); s.style.transform='scale('+k+')';
    });
  }

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
  addEventListener('resize',function(){fit();onScroll();});
  addEventListener('hashchange',function(){
    var k=parseInt(location.hash.slice(1),10); if(k&&k-1!==i) goto(k-1);
  });

  fit();
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
