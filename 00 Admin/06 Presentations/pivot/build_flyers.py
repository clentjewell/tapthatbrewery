"""Render the four event flyers as A4 promotional artwork.

The point of doing it this way: an image model cannot set type, so asking one
for a whole flyer gets you a picture of a flyer with mangled words on it. Here
the photograph is the only generated-looking part and it is not generated at
all -- it is Tap That's own venue, shot on the August site visit. Everything
with an edge or a letterform is laid out in CSS at 200 dpi.

The layout copies Tap That's existing in-venue flyer (site-visit photo 22,
"FUNCTIONS & KEG SYSTEM HIRE"): photo band up top with the headline over it,
torn edge, badge on the seam, dark green ground, gold sub-heads, contact and
QR at the foot.

    python3 build_flyers.py            # writes ../../..//02 Design/03 Assets/event-flyers
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
OUT = ROOT / "02 Design" / "03 Assets" / "event-flyers"
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
OFFWHITE = "#DFDFDF"

DPI = 200
W = round(210 / 25.4 * DPI)   # 1654
H = round(297 / 25.4 * DPI)   # 2339


def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(pathlib.Path(path).read_bytes()).decode()


def font_face(family, weight, filename):
    uri = data_uri(pathlib.Path(NODE_MODULES) / filename, "font/woff2")
    return (f"@font-face{{font-family:'{family}';font-weight:{weight};"
            f"font-style:normal;src:url({uri}) format('woff2');}}")


def hero(photo_name):
    """Crop to the photo band and grade it down so white type holds."""
    im = Image.open(PHOTOS / photo_name).convert("RGB")
    target = W / (H * 0.46)
    w, h = im.size
    if w / h > target:                       # too wide, trim the sides
        new_w = int(h * target)
        im = im.crop(((w - new_w) // 2, 0, (w - new_w) // 2 + new_w, h))
    else:                                    # too tall, keep the middle band
        new_h = int(w / target)
        top = int((h - new_h) * 0.28)
        im = im.crop((0, top, w, top + new_h))
    im = im.resize((W, int(H * 0.46)), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(0.82)
    im = ImageEnhance.Brightness(im).enhance(0.72)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=88)
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
            line = (f"{before}<span class='gold'>{gold_word}</span>{after}")
        out.append(f"<span class='hl'>{line}</span>")
    return "".join(out)


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:%(W)spx;height:%(H)spx}
body{background:%(GREEN)s;color:%(OFFWHITE)s;
     font-family:'Barlow Condensed',sans-serif;overflow:hidden;position:relative}

/* --- photo band, headline sits over it --- */
.band{position:absolute;inset:0 0 auto 0;height:46%%;overflow:hidden}
.band img{width:100%%;height:100%%;object-fit:cover;display:block}
.band::after{content:'';position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(12,33,19,.62) 0%%,rgba(12,33,19,.30) 38%%,
                             rgba(12,33,19,.78) 100%%)}

/* The torn seam. A single clipped block, not a stripe: it is the top edge of
   the green ground eating into the photograph, the way the printed one does. */
.tear{position:absolute;left:0;right:0;top:calc(46%% - 46px);height:120px;
  background:%(GREEN)s;z-index:2;
  clip-path:polygon(0 54px,38px 31px,88px 49px,132px 22px,186px 46px,236px 18px,
    292px 44px,348px 15px,402px 41px,458px 12px,516px 43px,572px 17px,628px 40px,
    686px 13px,742px 45px,798px 19px,856px 38px,912px 14px,970px 42px,1026px 16px,
    1084px 47px,1140px 20px,1198px 39px,1254px 13px,1312px 44px,1368px 18px,
    1426px 41px,1482px 15px,1540px 46px,1596px 24px,1654px 50px,
    1654px 120px,0 120px)}

.kicker{position:absolute;top:74px;left:0;right:0;text-align:center;z-index:3;
  font-family:'Oswald',sans-serif;font-weight:500;font-size:34px;
  letter-spacing:.42em;color:%(GOLD)s;text-transform:uppercase}

.head{position:absolute;left:96px;right:96px;top:250px;z-index:3;text-align:center}
.hl{display:block;font-family:'Oswald',sans-serif;font-weight:700;
    font-size:%(HEAD)spx;line-height:.98;letter-spacing:.005em;
    text-transform:uppercase;color:#F4F2ED;
    text-shadow:0 6px 26px rgba(0,0,0,.55)}
.gold{color:%(GOLD)s}

/* --- badge on the seam --- */
.badge{position:absolute;left:50%%;transform:translateX(-50%%);
  top:calc(46%% - 22px);width:360px;z-index:4}
.badge img{width:100%%;display:block}

/* --- green ground --- */
.body{position:absolute;left:150px;right:150px;top:calc(46%% + 258px);
      bottom:392px;text-align:center;
      display:flex;flex-direction:column;justify-content:center;gap:70px}
.blk h2{font-family:'Oswald',sans-serif;font-weight:600;font-size:56px;
        letter-spacing:.02em;color:%(GOLD)s;margin-bottom:16px}
.blk p{font-size:44px;line-height:1.28;color:%(OFFWHITE)s}

.strap{position:absolute;left:150px;right:150px;bottom:250px;text-align:center;
  font-family:'Oswald',sans-serif;font-weight:500;font-size:38px;
  letter-spacing:.13em;text-transform:uppercase;color:#F4F2ED;
  padding-top:34px;border-top:2px solid rgba(206,154,73,.42)}

/* --- foot: QR left, contact right, as on the house flyer --- */
.foot{position:absolute;left:150px;right:150px;bottom:92px;
  display:flex;align-items:center;gap:38px;text-align:left}
.foot img{width:150px;height:150px;display:block;
  border:9px solid #fff;background:#fff;border-radius:6px}
.cta{font-family:'Oswald',sans-serif;font-weight:600;font-size:44px;
     letter-spacing:.03em;color:%(GOLD)s;line-height:1.1}
.mail{font-size:40px;color:%(OFFWHITE)s;margin-top:8px;word-break:break-all}
"""


def build_html(f, fonts):
    return f"""<!doctype html><html><head><meta charset="utf-8">
<style>{fonts}
{CSS % dict(W=W, H=H, GREEN=GREEN, GOLD=GOLD, OFFWHITE=OFFWHITE, HEAD=124)}
</style></head><body>
<div class="band"><img src="{hero(f['photo'])}"></div>
<div class="tear"></div>
<div class="kicker">{f['kicker']}</div>
<div class="head">{head_html(f['head'], f.get('gold_word'))}</div>
<div class="badge"><img src="{data_uri(BRAND / 'tapthat-logo-hires.png', 'image/png')}"></div>
<div class="body">
  {''.join(f"<div class='blk'><h2>{b['title']}</h2><p>{b['body']}</p></div>" for b in f['blocks'])}
</div>
<div class="strap">{f['strap']}</div>
<div class="foot">
  <img src="{qr_uri(SITE)}">
  <div><div class="cta">{f['cta']}</div><div class="mail">{CONTACT}</div></div>
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
    // Report anything that spills, so a copy edit cannot silently overflow.
    const spill = await page.evaluate((H) => {
      const bad = [];
      const box = (s) => document.querySelector(s).getBoundingClientRect();
      for (const s of ['.kicker', '.head', '.body', '.strap', '.foot']) {
        const r = box(s);
        if (r.top < 0 || r.bottom > H - 8) bad.push(s + ' off page ' + Math.round(r.top) + '-' + Math.round(r.bottom));
      }
      // The two overlaps this layout can actually produce.
      if (box('.head').bottom > box('.tear').top) bad.push('headline runs into the tear');
      if (box('.badge').bottom > box('.body').top) bad.push('badge sits on the first sub-head');
      if (box('.body').bottom > box('.strap').top) bad.push('copy runs into the strapline');
      // Copy clipped inside its own flex box.
      const b = document.querySelector('.body');
      if (b.scrollHeight > b.clientHeight + 2) bad.push('copy clipped by ' + (b.scrollHeight - b.clientHeight) + 'px');
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
        font_face("Barlow Condensed", 400,
                  "@fontsource/barlow-condensed/files/barlow-condensed-latin-400-normal.woff2"),
        font_face("Barlow Condensed", 600,
                  "@fontsource/barlow-condensed/files/barlow-condensed-latin-600-normal.woff2"),
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
        sys.exit("flyer text overflows its page -- shorten the copy or drop a size")


if __name__ == "__main__":
    main()
