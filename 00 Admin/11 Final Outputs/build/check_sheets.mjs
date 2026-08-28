/**
 * Overflow check for the four A3 on-a-page sheets.
 *
 * Sheet-level scrollHeight is not enough: a box with its own overflow can clip
 * its text while the sheet itself measures clean. That is how three persona
 * cards on the Design sheet lost 15px of copy without anything flagging it.
 * This walks every descendant and reports any element hiding its own content.
 *
 *   cd site && python3 -m http.server 8899 &
 *   PW_DIR=<dir with playwright installed> node build/check_sheets.mjs
 *
 * ESM ignores NODE_PATH, so playwright is resolved through createRequire from
 * PW_DIR when the repo itself carries no node_modules. Exits 1 if anything clips.
 */
import { createRequire } from 'node:module';
const require = createRequire(process.env.PW_DIR ? `${process.env.PW_DIR}/` : import.meta.url);
const { chromium } = require('playwright');

const BASE   = process.env.BASE   || 'http://127.0.0.1:8899';
const SHEETS = ['overall', 'discover', 'design', 'deploy'];
const SIZES  = [{ width: 1587, height: 1123 },   // A3 landscape at 96dpi
                { width: 1191, height:  842 }];  // A4 landscape at 96dpi

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
let bad = 0;

for (const vp of SIZES) {
  console.log(`\n${vp.width}x${vp.height}`);
  for (const name of SHEETS) {
    const page = await browser.newPage({ viewport: vp });
    await page.goto(`${BASE}/on-a-page-${name}.html?cb=${Math.random()}`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(300);

    const r = await page.evaluate(() => {
      const sheet = document.querySelector('.oap');
      if (!sheet) return { error: 'no .oap element' };
      const clipped = [...sheet.querySelectorAll('*')]
        .filter(el => el.scrollHeight - el.clientHeight > 2
                   && getComputedStyle(el).overflow !== 'visible')
        .map(el => ({ cls: el.className, px: el.scrollHeight - el.clientHeight,
                      text: (el.innerText || '').replace(/\s+/g, ' ').slice(0, 60) }));
      return { spill: sheet.scrollHeight - sheet.clientHeight, clipped };
    });

    if (r.error) { console.log(`  ${name.padEnd(9)} ${r.error}`); bad++; }
    else if (r.spill > 2 || r.clipped.length) {
      bad++;
      console.log(`  ${name.padEnd(9)} FAIL  sheet spill ${r.spill}px, ${r.clipped.length} clipped`);
      for (const c of r.clipped) console.log(`      ${c.px}px hidden in .${c.cls} — "${c.text}"`);
    } else {
      console.log(`  ${name.padEnd(9)} ok`);
    }
    await page.close();
  }
}

await browser.close();
console.log(bad ? `\n${bad} sheet/size combinations clip content.` : '\nAll sheets clean at every size.');
process.exit(bad ? 1 : 0);
