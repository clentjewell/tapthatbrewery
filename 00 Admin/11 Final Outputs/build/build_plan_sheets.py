"""Build the five plan-on-a-page sheets from the 15 September catch-up.

Standalone of the pack build: wraps each A3 fragment in oap-plan/ with the
existing sheet CSS, renders it at true A3 landscape, and checks every element
for clipped content before writing the PDF.

The per-element check is the point. Sheet-level scrollHeight is not enough,
because a box with its own overflow clips its text while the sheet still
measures clean. That is how three persona cards on the Design sheet lost 15px
of copy without anything flagging it.

    python3 build_plan_sheets.py
"""

import json
import os
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SITE = ROOT / "00 Admin" / "11 Final Outputs" / "site"
OUT = ROOT / "00 Admin" / "11 Final Outputs" / "plan-on-a-page"
WORK = HERE / "build-plan"

SHEETS = [
    ("01-summary", "summary.html", "The plan on a page"),
    ("02-business", "business.html", "Business plan"),
    ("03-brand", "brand.html", "Brand plan"),
    ("04-sales-and-marketing", "sales.html", "Sales and marketing plan"),
    ("05-activation", "activation.html", "Activation plan"),
]

# A3 landscape at 96dpi. The sheet itself is laid out in mm, so this only has
# to be big enough that nothing wraps differently than it will on paper.
VIEWPORT = {"width": 1587, "height": 1123}

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<title>%(title)s</title>
<style>
@font-face{font-family:'Poppins';font-weight:400;src:local('Poppins')}
:root{--brass:#0066FF;--steel:#4A5565;--rule:#E3E7EC;--paper:#fff;--ink:#0E171F;--shade:#F5F7FA}
*{margin:0;padding:0}
html,body{background:#fff}
.oap-stage{transform-origin:top left}
%(css)s
</style></head><body>
%(frag)s
</body></html>"""

RENDER_JS = r"""
const playwright = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await playwright.chromium.launch({
    executablePath: '/opt/pw-browsers/chromium',
  });
  let bad = 0;
  for (const j of jobs.items) {
    const page = await browser.newPage({ viewport: jobs.viewport });
    await page.goto('file://' + j.html, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(200);

    const clipped = await page.evaluate(() => {
      const sheet = document.querySelector('.oap');
      if (!sheet) return [{ cls: 'no .oap element', px: 0 }];
      return [...sheet.querySelectorAll('*')]
        .filter(el => el.scrollHeight - el.clientHeight > 2
                   && getComputedStyle(el).overflow !== 'visible')
        .map(el => ({ cls: String(el.className).slice(0, 60),
                      px: el.scrollHeight - el.clientHeight }));
    });
    if (clipped.length) {
      bad += clipped.length;
      console.log('CLIPPED ' + j.name + ': '
        + clipped.map(c => `${c.cls} by ${c.px}px`).join(' | '));
    } else {
      console.log('clean   ' + j.name);
    }
    await page.pdf({ path: j.pdf, width: '420mm', height: '297mm',
                     printBackground: true, pageRanges: '1' });
    await page.close();
  }
  await browser.close();
  process.exit(bad ? 1 : 0);
})();
"""


def main():
    WORK.mkdir(exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    css = ((HERE / "oap.css").read_text(encoding="utf-8")
           + "\n" + (HERE / "oap-plan.css").read_text(encoding="utf-8"))

    items = []
    for slug, fname, title in SHEETS:
        frag = (HERE / "oap-plan" / fname).read_text(encoding="utf-8")
        # The fragments carry a relative logo path so they also work when the
        # pack build drops them into site/.
        frag = frag.replace('src="brand/tapthat-icon.png"',
                            f'src="file://{SITE}/brand/tapthat-icon.png"')
        page = WORK / f"{slug}.html"
        page.write_text(PAGE % dict(title=title, css=css, frag=frag),
                        encoding="utf-8")
        items.append({"name": slug, "html": str(page),
                      "pdf": str(WORK / f"{slug}.pdf")})

    jobs = WORK / "jobs.json"
    jobs.write_text(json.dumps({"viewport": VIEWPORT, "items": items}))
    js = WORK / "render.js"
    js.write_text(RENDER_JS)

    r = subprocess.run(["node", str(js), str(jobs)], capture_output=True,
                       text=True)
    print(r.stdout, r.stderr, sep="")
    if r.returncode:
        sys.exit("a sheet is clipping its own content -- cut copy or retune "
                 "that row in oap-plan.css")

    from pypdf import PdfWriter
    merged = OUT / "TapThat_Plan-on-a-Page_A3.pdf"
    w = PdfWriter()
    for i in items:
        w.append(i["pdf"])
        (OUT / pathlib.Path(i["pdf"]).name).write_bytes(
            pathlib.Path(i["pdf"]).read_bytes())
    w.write(str(merged))
    print("wrote", merged, "and", len(items), "single sheets")


if __name__ == "__main__":
    main()
