"""Render the four event flyers as A4 promotional artwork.

The point of doing it this way: an image model cannot set type, so asking one
for a whole flyer gets you a picture of a flyer with mangled words on it. Here
the photograph is the only part that is generated, and everything with an edge
or a letterform is laid out in CSS at 200 dpi.

Structure follows Tap That's own in-venue flyer (site-visit photo 22,
"FUNCTIONS & KEG SYSTEM HIRE"): photo band up top with the headline over it,
a seam, the badge on the seam, dark green ground, gold sub-heads, contact and
QR at the foot.

Type follows 34 Brand Guidelines section 3, which asks for bold condensed
sans headlines over a plain workhorse sans for body, and rules out scripts and
serifs. Oswald over Barlow. No serif sub-heads, however well they photograph.

    python3 build_flyers.py            # commissioned hero plates
    python3 build_flyers.py --venue    # August site-visit photography
"""

import base64
import io
import json
import os
import pathlib
import subprocess
import sys

from PIL import Image, ImageEnhance
import qrcode

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PHOTOS = ROOT / "01 Discover" / "01 Inputs" / "site-visit-photos"
BRAND = ROOT / "00 Admin" / "11 Final Outputs" / "brand-source"
HEROES = ROOT / "02 Design" / "03 Assets" / "generated-heroes"
# --venue rebuilds the same four flyers on August site-visit photography, for
# anything that goes out as Tap That's own marketing rather than as concept
# artwork. Same copy, same layout, different plate.
VENUE = "--venue" in sys.argv
OUT = ROOT / "02 Design" / "03 Assets" / (
    "event-flyers-venue" if VENUE else "event-flyers")
NODE_MODULES = os.environ.get(
    "PIVOT_NODE_MODULES",
    "/tmp/claude-0/-home-user-tapthatbrewery/aff657a1-809f-5111-b96e-244c77408e59"
    "/scratchpad/pivot/node_modules",
)

sys.path.insert(0, str(HERE))
from flyer_content import FLYERS, CONTACT, SITE  # noqa: E402

# 34 Brand Guidelines section 2. Green leads, gold accents, never the reverse.
GREEN = "#14361D"
GREEN_DEEP = "#0C2113"
GOLD = "#CE9A49"
GOLD_SOFT = "rgba(206,154,73,.45)"
OFFWHITE = "#DFDFDF"

DPI = 200
W = round(210 / 25.4 * DPI)   # 1654
H = round(297 / 25.4 * DPI)   # 2339
BAND = 0.46                   # photo band as a fraction of the page


def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(pathlib.Path(path).read_bytes()).decode()


def font_face(family, weight, filename):
    uri = data_uri(pathlib.Path(NODE_MODULES) / filename, "font/woff2")
    return (f"@font-face{{font-family:'{family}';font-weight:{weight};"
            f"font-style:normal;src:url({uri}) format('woff2');}}")


def hero(f):
    """Crop to the photo band and grade it for type to sit over."""
    src = (PHOTOS / f["photo"]) if VENUE else (HEROES / f["hero"])
    bias = 0.28 if VENUE else f.get("hero_bias", 0.3)
    im = Image.open(src).convert("RGB")
    target = W / (H * BAND)
    w, h = im.size
    if w / h > target:                       # too wide, trim the sides
        new_w = int(h * target)
        im = im.crop(((w - new_w) // 2, 0, (w - new_w) // 2 + new_w, h))
    else:                                    # too tall, keep the band that
        new_h = int(w / target)              # carries the subject
        top = int((h - new_h) * bias)
        im = im.crop((0, top, w, top + new_h))
    im = im.resize((W, int(H * BAND)), Image.LANCZOS)
    # The site-visit frames are flat and have to be taken down hard before
    # white type holds. The commissioned plates are lit for it already, so the
    # scrim in .band::after does that work and the plate keeps its warmth.
    im = ImageEnhance.Color(im).enhance(0.82 if VENUE else 1.0)
    im = ImageEnhance.Brightness(im).enhance(0.72 if VENUE else 0.95)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def qr_uri(payload):
    q = qrcode.QRCode(box_size=10, border=1,
                      error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(payload)
    q.make(fit=True)
    img = q.make_image(fill_color=GREEN_DEEP, back_color="white").convert("RGB")
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def head_html(lines, gold_word):
    """Set the headline, with one phrase carried in gold as the flyers do."""
    out = []
    for line in lines:
        if gold_word and gold_word in line:
            before, after = line.split(gold_word, 1)
            line = f"{before}<span class='gold'>{gold_word}</span>{after}"
        out.append(f"<span class='hl'>{line}</span>")
    return "".join(out)


# --- drawn marks -----------------------------------------------------------
# Line art, stroked in gold, no fills. A hop cone and a stein: both read at
# 40px and neither depends on a typeface being present.

HOP = """<svg viewBox="0 0 48 60"><g fill="none" stroke="currentColor"
 stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
 <path d="M24 5c10 5 14 15 12 26-2 12-9 20-12 24-3-4-10-12-12-24C10 20 14 10 24 5z"/>
 <path d="M12 19c5 3 9 9 12 15 3-6 7-12 12-15"/>
 <path d="M13 32c5 3 9 8 11 13 2-5 6-10 11-13"/>
 <path d="M24 5v50"/></g></svg>"""

STEIN = """<svg viewBox="0 0 52 60"><g fill="none" stroke="currentColor"
 stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
 <path d="M12 16h22l-2 32a5 5 0 0 1-5 4h-8a5 5 0 0 1-5-4z"/>
 <path d="M34 23h6a6 6 0 0 1 0 13h-5"/>
 <path d="M12 25h21"/>
 <path d="M14 10c3-4 7-4 10 0 3-4 7-4 9 0"/></g></svg>"""

MAIL = """<svg viewBox="0 0 32 24"><g fill="none" stroke="currentColor"
 stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
 <rect x="2" y="3" width="28" height="18" rx="2"/>
 <path d="M3 5l13 10L29 5"/></g></svg>"""

# The seam. A shallow bowl: the green ground rides higher at the edges and
# dips under the badge, which is where the printed flyer's torn edge sits.
WAVE = """<svg class="wave" viewBox="0 0 1654 210" preserveAspectRatio="none">
 <path d="M0 14C286 14 452 168 827 168 1202 168 1368 14 1654 14L1654 210 0 210Z"
  fill="%(GREEN)s"/>
 <path d="M0 14C286 14 452 168 827 168 1202 168 1368 14 1654 14"
  fill="none" stroke="%(GOLD)s" stroke-width="5"/></svg>"""


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:%(W)spx;height:%(H)spx}
body{background:%(GREEN)s;color:%(OFFWHITE)s;
     font-family:'Barlow',sans-serif;overflow:hidden;position:relative}
svg{width:100%%;height:100%%;display:block}

/* --- photo band, headline over it --- */
.band{position:absolute;inset:0 0 auto 0;height:%(BANDPC)s%%;overflow:hidden}
.band img{width:100%%;height:100%%;object-fit:cover;display:block}
/* Dark at the top where the type sits, open through the middle so the plate
   keeps its depth, closing again into the seam. */
.band::after{content:'';position:absolute;inset:0;background:linear-gradient(
  180deg,rgba(8,22,13,.80) 0%%,rgba(8,22,13,.62) 26%%,rgba(8,22,13,.12) 52%%,
  rgba(8,22,13,.30) 100%%)}

.wave{position:absolute;left:0;right:0;top:calc(%(BANDPC)s%% - 150px);
  height:210px;z-index:2}

/* --- kicker, rules either side --- */
.kicker{position:absolute;top:96px;left:150px;right:150px;z-index:3;
  display:flex;align-items:center;gap:26px;
  font-family:'Oswald',sans-serif;font-weight:500;font-size:31px;
  letter-spacing:.36em;color:%(GOLD)s;text-transform:uppercase}
.kicker span{white-space:nowrap}
.kicker i{flex:1;height:1px;background:%(GOLD_SOFT)s}

.head{position:absolute;left:110px;right:110px;top:212px;z-index:3;
  text-align:center}
.hl{display:block;font-family:'Oswald',sans-serif;font-weight:700;
    font-size:%(HEAD)spx;line-height:1.0;letter-spacing:.004em;
    text-transform:uppercase;color:#F7F5F0;
    text-shadow:0 8px 30px rgba(0,0,0,.6)}
.gold{color:%(GOLD)s}

.badge{position:absolute;left:50%%;transform:translateX(-50%%);
  top:calc(%(BANDPC)s%% - 42px);width:336px;z-index:4}
.badge img{width:100%%;display:block}

/* --- green ground --- */
.frame{position:absolute;left:64px;right:64px;top:calc(%(BANDPC)s%% + 200px);
  bottom:64px;border:1px solid %(GOLD_SOFT)s;border-radius:6px;z-index:1}

.cols{position:absolute;left:132px;right:132px;top:calc(%(BANDPC)s%% + 268px);
  display:flex;align-items:flex-start}
.col{flex:1;padding:0 44px;text-align:center}
.divider{width:1px;align-self:stretch;background:%(GOLD_SOFT)s}
.ico{width:104px;height:104px;margin:0 auto 26px;border:2px solid %(GOLD)s;
  border-radius:50%%;display:flex;align-items:center;justify-content:center;
  color:%(GOLD)s}
.ico svg{width:62px;height:72px}
.col h2{font-family:'Oswald',sans-serif;font-weight:600;font-size:54px;
        letter-spacing:.01em;color:%(GOLD)s;margin-bottom:20px;line-height:1.08;
        min-height:118px;display:flex;align-items:center;
        justify-content:center;text-align:center}
.col p{font-size:38px;line-height:1.38;color:%(OFFWHITE)s}

/* --- strapline, rules either side --- */
.strap{position:absolute;left:150px;right:150px;bottom:%(STRAPB)spx;
  display:flex;align-items:center;gap:26px;
  font-family:'Oswald',sans-serif;font-weight:500;font-size:37px;
  letter-spacing:.14em;text-transform:uppercase;color:#F7F5F0}
.strap span{white-space:nowrap}
.strap i{flex:1;height:1px;background:%(GOLD_SOFT)s}

/* --- foot: QR, call to action, address, inside a gold-ruled box --- */
.foot{position:absolute;left:132px;right:132px;bottom:120px;height:206px;
  border:2px solid %(GOLD)s;border-radius:10px;
  display:flex;align-items:center;justify-content:center;gap:44px;
  padding:0 46px}
.foot>img{width:132px;height:132px;display:block;
  border:8px solid #fff;background:#fff;border-radius:5px}
.cta{font-family:'Oswald',sans-serif;font-weight:600;font-size:47px;
     letter-spacing:.02em;color:%(GOLD)s;line-height:1.1}
.mail{display:flex;align-items:center;gap:16px;margin-top:12px;
      font-size:37px;color:%(OFFWHITE)s}
.mail em{width:34px;height:26px;color:%(GOLD)s;font-style:normal;flex:none}
"""


def build_html(f, fonts):
    icons = [HOP, STEIN]
    cols = []
    for i, b in enumerate(f["blocks"]):
        cols.append(
            f"<div class='col'><div class='ico'>{icons[i % 2]}</div>"
            f"<h2>{b['title']}</h2><p>{b['body']}</p></div>")
    body = f"<div class='divider'></div>".join(cols)
    css = CSS % dict(W=W, H=H, GREEN=GREEN, GOLD=GOLD, GOLD_SOFT=GOLD_SOFT,
                     OFFWHITE=OFFWHITE, HEAD=130, BANDPC=BAND * 100,
                     STRAPB=396)
    return f"""<!doctype html><html><head><meta charset="utf-8">
<style>{fonts}
{css}
</style></head><body>
<div class="band"><img src="{hero(f)}"></div>
{WAVE % dict(GREEN=GREEN, GOLD=GOLD)}
<div class="kicker"><i></i><span>{f['kicker']}</span><i></i></div>
<div class="head">{head_html(f['head'], f.get('gold_word'))}</div>
<div class="badge"><img src="{data_uri(BRAND / 'tapthat-logo-hires.png', 'image/png')}"></div>
<div class="frame"></div>
<div class="cols">{body}</div>
<div class="strap"><i></i><span>{f['strap']}</span><i></i></div>
<div class="foot">
  <img src="{qr_uri(SITE)}">
  <div><div class="cta">{f['cta']}</div>
       <div class="mail"><em>{MAIL}</em>{CONTACT}</div></div>
</div>
</body></html>"""


RENDER_JS = r"""
const playwright = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await playwright.chromium.launch();
  const page = await browser.newPage({
    viewport: {width: jobs.w, height: jobs.h}, deviceScaleFactor: 1,
  });
  for (const j of jobs.items) {
    await page.goto('file://' + j.html);
    await page.evaluate(() => document.fonts.ready);
    // The collisions this layout can actually produce, tested rather than
    // eyeballed, so a copy edit cannot quietly push something off the page.
    const spill = await page.evaluate((H) => {
      const bad = [];
      const box = (s) => document.querySelector(s).getBoundingClientRect();
      for (const s of ['.kicker', '.head', '.cols', '.strap', '.foot']) {
        const r = box(s);
        if (r.top < 0 || r.bottom > H - 8) bad.push(s + ' off page ' + Math.round(r.top) + '-' + Math.round(r.bottom));
      }
      if (box('.head').bottom > box('.wave').top) bad.push('headline runs into the seam');
      if (box('.badge').bottom > box('.cols').top) bad.push('badge sits on the first sub-head');
      if (box('.cols').bottom > box('.strap').top) bad.push('copy runs into the strapline');
      if (box('.strap').bottom > box('.foot').top) bad.push('strapline runs into the foot');
      if (box('.foot').bottom > box('.frame').bottom) bad.push('foot breaks the frame');
      return bad;
    }, jobs.h);
    if (spill.length) console.log('SPILL ' + j.png + ': ' + spill.join(' | '));
    await page.screenshot({path: j.png});
    console.log('wrote ' + j.png);
  }
  await browser.close();
})();
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = pathlib.Path(os.environ.get("TMPDIR", "/tmp")) / "flyer-build"
    tmp.mkdir(parents=True, exist_ok=True)

    fonts = "".join([
        font_face("Oswald", 500, "@fontsource/oswald/files/oswald-latin-500-normal.woff2"),
        font_face("Oswald", 600, "@fontsource/oswald/files/oswald-latin-600-normal.woff2"),
        font_face("Oswald", 700, "@fontsource/oswald/files/oswald-latin-700-normal.woff2"),
        font_face("Barlow", 400, "@fontsource/barlow/files/barlow-latin-400-normal.woff2"),
        font_face("Barlow", 500, "@fontsource/barlow/files/barlow-latin-500-normal.woff2"),
    ])

    items = []
    for f in FLYERS:
        html_path = tmp / f"{f['slug']}.html"
        html_path.write_text(build_html(f, fonts), encoding="utf-8")
        items.append({"html": str(html_path), "png": str(OUT / f"{f['slug']}.png")})

    jobs = tmp / "jobs.json"
    jobs.write_text(json.dumps({"w": W, "h": H, "items": items}))
    js = tmp / "render.js"
    js.write_text(RENDER_JS)

    r = subprocess.run(["node", str(js), str(jobs)], capture_output=True, text=True)
    print(r.stdout, r.stderr, sep="")
    if r.returncode:
        sys.exit(r.returncode)
    if "SPILL" in r.stdout:
        sys.exit("flyer layout collides -- shorten the copy or drop a size")


if __name__ == "__main__":
    main()
