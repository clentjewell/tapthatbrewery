/*
 * The five plan sheets as an editable PowerPoint, for Justin to modify.
 *
 * Slide size is a true A3 landscape, 420 x 297mm, so a slide and a printed
 * sheet are the same artefact at the same size rather than two versions of it.
 * Everything is a real text box, a real table or a real shape. Nothing is a
 * picture of a sheet, because the point of this file is that it can be edited.
 *
 * Words come from build-plan/content.json, which plan_extract.py reads out of
 * the A3 fragments. Type sizes mirror oap.css and oap-plan.css. Only the grid
 * positions live here.
 *
 * Heights are measured, not guessed. The first cut estimated line counts from
 * character counts and every dense box overlapped itself, so every run of text
 * is laid out in Chromium at the same point size, line height and column width
 * the slide will use, and the measured line count sets the height. Line spacing
 * goes into the file as exact points rather than a multiplier, so PowerPoint
 * cannot re-flow it against its own idea of a Poppins line.
 *
 *   node build_plan_pptx.js build-plan/content.json <out.pptx>
 */

const pptxgen = require('pptxgenjs');
const { chromium } = require('playwright');
const fs = require('fs');

const C = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const OUT = process.argv[3];

/* Palette carried over from oap.css so the deck and the sheets match. */
const INK = '0E171F';
const ACCENT = '0066FF';
const MUTED = '4A5565';
const LINE = 'E3E7EC';
const TINT = 'F5F7FA';
const PAPER = 'FFFFFF';

// One family, weight by the bold flag. Naming a weight in the family name is
// what put an earlier deck into a handwriting face in WPS.
const FONT = 'Poppins';

const W = 16.535, H = 11.693;      // 420 x 297mm
const M = 0.354, G = 0.118;        // 9mm side margin, 3mm grid gap
const COLW = (W - 2 * M - 11 * G) / 12;
const MM = 1 / 25.4;

const colX = (c) => M + (c - 1) * (COLW + G);
const colW = (a, b) => (b - a) * (COLW + G) - G;

const CANVAS_TOP = 1.22;
const CANVAS_BOT = H - 6 * MM;

/* Grid placement, mirroring oap-plan.css. [colStart, colEnd, row] */
const LAYOUT = {
  summary: { rows: [0.94, 1.16, 1.10], boxes: {
    'b-north': [1, 8, 1], 'b-numbers': [8, 13, 1], 'b-plans': [1, 13, 2],
    'b-sequence': [1, 5, 3], 'b-owners': [5, 9, 3], 'b-decisions': [9, 13, 3] } },
  business: { rows: [1.04, 1.06, 1.02], boxes: {
    'b-model': [1, 7, 1], 'b-units': [7, 13, 1], 'b-maths': [1, 5, 2],
    'b-econ': [5, 9, 2], 'b-canning': [9, 13, 2], 'b-decisions': [1, 7, 3],
    'b-risks': [7, 13, 3] } },
  brand: { rows: [0.96, 1.15, 1.01], boxes: {
    'b-position': [1, 7, 1], 'b-enemy': [7, 13, 1], 'b-range': [1, 5, 2],
    'b-her': [5, 9, 2], 'b-proof': [9, 13, 2], 'b-open': [1, 7, 3],
    'b-voice': [7, 13, 3] } },
  sales: { rows: [0.84, 1.33, 1.03], boxes: {
    'b-engine': [1, 13, 1], 'b-segments': [1, 6, 2], 'b-convert': [6, 13, 2],
    'b-wholesale': [1, 5, 3], 'b-search': [5, 9, 3], 'b-measure': [9, 13, 3] } },
  activation: { rows: [0.96, 1.24, 0.94], boxes: {
    'b-90': [1, 13, 1], 'b-destination': [1, 4, 2], 'b-partners': [4, 9, 2],
    'b-campaign': [9, 13, 2], 'b-raci': [1, 9, 3], 'b-check': [9, 13, 3] } },
};

/* Type, straight out of the two stylesheets. [size in pt, line height]. */
const T = {
  label:     [6.8, 1.3],
  statement: [13, 1.24],
  lead:      [9.2, 1.38],
  para:      [8.1, 1.5],
  li:        [8, 1.46],
  note:      [7, 1.35],
  th:        [6.2, 1.25],
  td:        [7.1, 1.36],
  kpiNum:    [16, 1.0],
  kpiLbl:    [5.8, 1.3],
};

/* Per-box overrides, same as the data-sheet rules in oap-plan.css. */
const OVER = {
  'summary/b-north':        { statement: [14, 1.24] },
  'summary/b-numbers':      { kpiNum: [14, 1.0], kpiLbl: [5.6, 1.28] },
  'summary/b-owners':       { td: [6.6, 1.36], pad: 1.3 },
  'summary/b-decisions':    { li: [7.3, 1.4] },
  'business/b-model':       { statement: [13, 1.24] },
  'business/b-units':       { td: [6.9, 1.36], pad: 1.5 },
  'business/b-maths':       { kpiNum: [13, 1.0], kpiLbl: [5.5, 1.26] },
  'brand/b-position':       { statement: [13.4, 1.24] },
  'brand/b-proof':          { li: [7.2, 1.4] },
  'brand/b-open':           { li: [7.3, 1.42] },
  'sales/b-engine':         { statement: [12.4, 1.24] },
  'sales/b-segments':       { td: [6.8, 1.36], pad: 1.4 },
  'sales/b-convert':        { lead: [8.6, 1.38] },
  'sales/b-measure':        { kpiNum: [11, 1.0], kpiLbl: [5.5, 1.26] },
  'activation/b-partners':  { td: [6.6, 1.36], pad: 1.3 },
  'activation/b-raci':      { td: [6.7, 1.36], pad: 1.4 },
  'activation/b-check':     { li: [7.3, 1.4] },
};

/* The tinted mini-boxes: four plans, five systems, four sprint bands. */
const CELL = {
  'summary/b-plans':  { head: [6.8, ACCENT, 0.14], lead: [9.6, 1.28],
                        para: [7.9, 1.48], li: [7.9, 1.46] },
  'sales/b-engine':   { head: [6.6, INK, 0.10], lead: [8.6, 1.38],
                        para: [7.4, 1.44], li: [7.4, 1.42] },
  'activation/b-90':  { head: [6.5, ACCENT, 0.10], lead: [8.6, 1.38],
                        para: [7.4, 1.42], li: [7.4, 1.42] },
};

/* Boxes whose numbers sit two-up rather than three-up. */
const KPI_COLS = { 'b-numbers': 3, 'b-maths': 3, 'b-measure': 2 };

/* Tables whose columns after the first are single marks, centred. */
const CENTRED = new Set(['activation/b-raci']);

/* ---------------------------------------------------------------- measuring */

let page;

async function openMeasure() {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  page = await browser.newPage();
  await page.setContent(
    '<style>html,body{margin:0;padding:0}'
    + '#m{position:absolute;left:0;top:0;font-family:Poppins,sans-serif;'
    + 'font-weight:400;word-wrap:break-word;}'
    + '#m b{font-weight:600}</style><div id="m"></div>');
  await page.evaluate(() => Promise.all([
    document.fonts.load('400 10pt Poppins'),
    document.fonts.load('600 10pt Poppins'),
  ]));
  return browser;
}

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const htmlFor = (runs) => runs
  .map((r) => (r.br ? '<br>' : '') + (r.b ? '<b>' + esc(r.t) + '</b>' : esc(r.t)))
  .join('');

const cache = new Map();

/* Lines a run of text takes at a given size and column width. */
async function lines(runs, fsPt, wIn, opts) {
  const o = opts || {};
  let html = htmlFor(runs);
  if (o.upper) html = html.toUpperCase().replace(/<B>/g, '<b>').replace(/<\/B>/g, '</b>');
  const key = html + '|' + fsPt + '|' + wIn.toFixed(4) + '|' + (o.track || 0);
  if (cache.has(key)) return cache.get(key);
  const n = await page.evaluate((a) => {
    const m = document.getElementById('m');
    m.style.whiteSpace = 'normal';
    m.style.width = a.wPx + 'px';
    m.style.fontSize = a.fsPx + 'px';
    m.style.lineHeight = '100px';
    m.style.letterSpacing = a.ls + 'px';
    m.innerHTML = a.html;
    return Math.max(1, Math.round(m.getBoundingClientRect().height / 100));
  }, { html: html, fsPx: fsPt * 96 / 72,
       // Chromium and PowerPoint do not always break a line in the same place.
       // Measuring against a slightly narrower column means a break that lands
       // differently there costs a little more white space, never an overlap.
       wPx: Math.max(wIn * 0.975, 0.2) * 96,
       ls: (o.track || 0) * fsPt * 96 / 72 });
  cache.set(key, n);
  return n;
}

/* Width of a run set on one line, for chips and table columns. */
async function runWidth(runs, fsPt, track, upper) {
  let html = htmlFor(runs);
  if (upper) html = html.toUpperCase().replace(/<B>/g, '<b>').replace(/<\/B>/g, '</b>');
  const key = 'W|' + html + '|' + fsPt + '|' + (track || 0);
  if (cache.has(key)) return cache.get(key);
  const w = await page.evaluate((a) => {
    const m = document.getElementById('m');
    m.style.whiteSpace = 'nowrap';
    m.style.width = 'auto';
    m.style.fontSize = a.fsPx + 'px';
    m.style.lineHeight = '100px';
    m.style.letterSpacing = a.ls + 'px';
    m.innerHTML = a.html;
    const w = m.getBoundingClientRect().width;
    m.style.whiteSpace = 'normal';
    return w / 96;
  }, { html: html, fsPx: fsPt * 96 / 72, ls: (track || 0) * fsPt * 96 / 72 });
  cache.set(key, w);
  return w;
}

/* Height in inches of a paragraph, given its type spec. */
async function textH(runs, spec, wIn, opts) {
  const n = await lines(runs, spec[0], wIn, opts);
  return n * spec[0] * spec[1] / 72;
}

const txt = (runs) => runs.map((r) => r.t).join('');

/* --------------------------------------------------------------- the deck */

const pres = new pptxgen();
pres.defineLayout({ name: 'A3LAND', width: W, height: H });
pres.layout = 'A3LAND';
pres.author = 'Jewell Projects';
pres.company = 'Jewell Projects';
pres.title = 'Tap That Brewery - the plan on a page';

/* A run carrying br starts a new line, which pptxgenjs expresses as a break
   on the run before it. The segments table depends on this: its first cell is
   a name over a figure, not a name run into one. */
function rich(runs, color, extra) {
  const out = [];
  runs.forEach((r) => {
    if (r.br && out.length) out[out.length - 1].options.breakLine = true;
    if (!r.t) return;
    out.push({ text: r.t,
      options: Object.assign({ bold: !!r.b,
        color: r.b ? INK : (color || MUTED) }, extra || {}) });
  });
  return out;
}

/* pptxgenjs only emits a real bullet for plain-string text, and taking that
   path would cost the bold inside list items, where the emphasis is carrying
   the dates and the labels. The sheet's marker is a CSS pseudo-element square
   rather than a list bullet in the first place, so it is drawn here the same
   way: a shape beside a text box that stays fully editable. Poppins has no
   U+25AA either, so a character bullet could not have matched it anyway. */
const BULL_IN = 3 * MM;            // li padding-left in oap.css
const BULL_SZ = 1.4 * MM;

function bulletMark(s, x, y, spec) {
  s.addShape(pres.ShapeType.rect, {
    x: x, y: y + (spec[0] * spec[1] / 72 - BULL_SZ) / 2 - 0.004,
    w: BULL_SZ, h: BULL_SZ, fill: { color: ACCENT }, line: { width: 0 },
  });
}

/* Every text box in this file is set the same way: no autofit, no inset, and
   line spacing in points so nothing re-flows against the measurement. */
const body = (spec, extra) => Object.assign({
  isTextBox: true, margin: 0, fontFace: FONT, fontSize: spec[0],
  lineSpacing: spec[0] * spec[1], valign: 'top', fit: 'none',
}, extra || {});

function rowGeom(rows) {
  const total = rows.reduce((a, b) => a + b, 0);
  const space = CANVAS_BOT - CANVAS_TOP - (rows.length - 1) * G;
  let y = CANVAS_TOP;
  return rows.map((f) => {
    const h = space * (f / total);
    const out = { y: y, h: h };
    y += h + G;
    return out;
  });
}

const LOGO = '../site/brand/tapthat-icon.png';
const JPMARK = '../site/brand/jewell-wordmark.png';
const JPMARK_H = 5.4 * MM;              // matches .jp-mark in oap-plan.css
const JPMARK_W = JPMARK_H * 720 / 159;  // the wordmark's own aspect

async function header(s, sheet) {
  s.addImage({ path: LOGO, x: M, y: 0.33, w: 10 * MM, h: 10 * MM });
  s.addText(sheet.title, {
    x: M + 14 * MM, y: 0.34, w: 9, h: 0.44, isTextBox: true, margin: 0,
    fontFace: FONT, bold: true, fontSize: 21, color: INK, valign: 'bottom',
    fit: 'none',
  });
  s.addImage({ path: JPMARK, x: W - M - JPMARK_W, y: 0.40 + (0.275 - JPMARK_H) / 2,
               w: JPMARK_W, h: JPMARK_H });
  // Chips run right to left, starting back from the mark on the margin.
  let x = W - M - JPMARK_W - 2 * MM;
  const chips = [].concat(sheet.chips).reverse();
  for (let i = 0; i < chips.length; i += 1) {
    const chip = chips[i];
    const label = chip.t;
    const w = await runWidth([{ t: label, b: true }], 6.5, 0.12, true) + 7 * MM;
    x -= w;
    s.addShape(pres.ShapeType.roundRect, {
      x: x, y: 0.40, w: w, h: 0.275, rectRadius: 0.1375,
      fill: { color: PAPER },
      line: { color: chip.gate ? ACCENT : LINE, width: 0.75 },
    });
    s.addText(label.toUpperCase(), {
      x: x, y: 0.40, w: w, h: 0.275, isTextBox: true, margin: 0, fit: 'none',
      fontFace: FONT, bold: true, fontSize: 6.5, charSpacing: 6.5 * 0.12,
      color: chip.gate ? ACCENT : MUTED, align: 'center', valign: 'middle',
    });
    x -= 2.5 * MM;
  }
  s.addShape(pres.ShapeType.line, {
    x: M, y: 1.06, w: W - 2 * M, h: 0, line: { color: INK, width: 2 },
  });
}

/* ------------------------------------------------------------------ tables */

/* Column widths from the real text, so the RACI letters get narrow columns
   and the workstream names get the room they need. */
async function tableGeom(b, spec, thSpec, padIn, wIn) {
  const cols = b.rows[0].cells.length;
  const weights = [];
  for (let c = 0; c < cols; c += 1) {
    let max = 0;
    for (let r = 0; r < b.rows.length; r += 1) {
      const row = b.rows[r];
      const cell = row.cells[c];
      if (!cell) continue;
      const s = row.header ? thSpec : spec;
      const w = await runWidth(cell.runs, s[0], row.header ? 0.1 : 0, row.header);
      max = Math.max(max, Math.min(w, 2.2));
    }
    weights.push(Math.max(max, 0.26) + 2 * padIn);
  }
  const sum = weights.reduce((a, x) => a + x, 0);
  const colWs = weights.map((x) => x / sum * wIn);

  const rowHs = [];
  for (let r = 0; r < b.rows.length; r += 1) {
    const row = b.rows[r];
    const s = row.header ? thSpec : spec;
    let n = 1;
    for (let c = 0; c < cols; c += 1) {
      const cell = row.cells[c];
      if (!cell) continue;
      n = Math.max(n, await lines(cell.runs, s[0], colWs[c] - 2 * padIn - 0.02,
        { track: row.header ? 0.1 : 0, upper: row.header }));
    }
    rowHs.push(n * s[0] * s[1] / 72 + 2 * padIn);
  }
  return { colWs: colWs, rowHs: rowHs,
           h: rowHs.reduce((a, x) => a + x, 0) };
}

function drawTable(s, b, geom, spec, thSpec, padIn, x, y, stretch, centred) {
  const extra = stretch / b.rows.length;
  const rows = b.rows.map((r, ri) => r.cells.map((c, ci) => ({
    text: rich(c.runs, r.header ? PAPER : MUTED,
      r.header ? { bold: true, color: PAPER } : {}),
    options: {
      fill: { color: r.header ? INK : (ri % 2 === 0 ? PAPER : TINT) },
      fontSize: r.header ? thSpec[0] : spec[0],
      charSpacing: r.header ? thSpec[0] * 0.1 : 0,
      lineSpacing: r.header ? thSpec[0] * thSpec[1] : spec[0] * spec[1],
      margin: [padIn * 72, padIn * 72, padIn * 72, padIn * 72],
      valign: r.header ? 'middle' : 'top',
      align: (centred && ci > 0) ? 'center' : 'left',
    },
  })));
  s.addTable(rows, {
    x: x, y: y, colW: geom.colWs, rowH: geom.rowHs.map((h) => h + extra),
    autoPage: false, fontFace: FONT,
    border: [{ type: 'none' }, { type: 'none' },
             { type: 'solid', color: LINE, pt: 0.6 }, { type: 'none' }],
  });
}

/* ------------------------------------------------------------- mini-boxes */

async function cellsGeom(b, key, wIn) {
  const spec = CELL[key];
  const n = b.cells.length;
  const cw = (wIn - (n - 1) * G) / n;
  const pad = 2.6 * MM;
  const iw = cw - 2 * pad;
  let tallest = 0;
  const per = [];
  for (let i = 0; i < b.cells.length; i += 1) {
    const cell = b.cells[i];
    const headH = spec.head[0] * 1.3 / 72;
    let h = headH + 1.6 * MM;
    const blocks = [];
    for (let j = 0; j < cell.blocks.length; j += 1) {
      const blk = cell.blocks[j];
      if (blk.k === 'list') {
        const hs = [];
        let lh = 0;
        for (let k = 0; k < blk.items.length; k += 1) {
          const ih = await textH(blk.items[k], spec.li, iw - 2.6 * MM);
          hs.push(ih);
          lh += ih + 1.2 * MM;
        }
        blocks.push({ blk: blk, h: lh, hs: hs, spec: spec.li });
        h += lh;
      } else {
        const s = blk.k === 'lead' ? spec.lead : spec.para;
        const bh = await textH(blk.runs, s, iw);
        blocks.push({ blk: blk, h: bh, spec: s });
        h += bh + 1.8 * MM;
      }
    }
    per.push({ cell: cell, blocks: blocks, h: h, headH: headH });
    tallest = Math.max(tallest, h);
  }
  return { cw: cw, pad: pad, iw: iw, per: per, h: tallest + 2 * pad,
           spec: spec, n: n };
}

function drawCells(s, g, x, y, h) {
  g.per.forEach((p, i) => {
    const cx = x + i * (g.cw + G);
    s.addShape(pres.ShapeType.rect, {
      x: cx, y: y, w: g.cw, h: h, fill: { color: TINT },
      line: { color: LINE, width: 0.6 },
    });
    s.addShape(pres.ShapeType.rect, {
      x: cx, y: y, w: g.cw, h: 0.8 * MM, fill: { color: ACCENT },
      line: { width: 0 },
    });
    let cy = y + g.pad;
    s.addText(p.cell.head.toUpperCase(), Object.assign(
      body([g.spec.head[0], 1.3], { color: g.spec.head[1], bold: true,
        charSpacing: g.spec.head[0] * g.spec.head[2] }),
      { x: cx + g.pad, y: cy, w: g.iw, h: p.headH }));
    cy += p.headH + 1.6 * MM;
    p.blocks.forEach((bb) => {
      if (bb.blk.k === 'list') {
        let ly = cy;
        bb.blk.items.forEach((it, k) => {
          bulletMark(s, cx + g.pad, ly, bb.spec);
          s.addText(rich(it, MUTED), Object.assign(
            body(bb.spec, { color: MUTED }),
            { x: cx + g.pad + 2.6 * MM, y: ly, w: g.iw - 2.6 * MM,
              h: bb.hs[k] }));
          ly += bb.hs[k] + 1.2 * MM;
        });
        cy += bb.h;
      } else {
        const lead = bb.blk.k === 'lead';
        s.addText(rich(bb.blk.runs, lead ? INK : MUTED), Object.assign(
          body(bb.spec, { color: lead ? INK : MUTED, bold: lead }),
          { x: cx + g.pad, y: cy, w: g.iw, h: bb.h }));
        cy += bb.h + 1.8 * MM;
      }
    });
  });
}

/* ------------------------------------------------------------------ boxes */

async function measureBox(box, key, wIn, avail) {
  const o = OVER[key] || {};
  const spec = (k) => o[k] || T[k];
  const pad = 3.2 * MM;
  const iw = wIn - 2 * pad;
  const out = { pad: pad, iw: iw, blocks: [], spec: spec };

  out.labelH = spec('label')[0] * spec('label')[1] / 72;

  const note = box.blocks.filter((b) => b.k === 'note')[0];
  out.note = note || null;
  out.noteH = note
    ? await textH(note.runs, spec('note'), iw) + 3.4 * MM : 0;

  for (let i = 0; i < box.blocks.length; i += 1) {
    const b = box.blocks[i];
    if (b.k === 'note') continue;
    if (b.k === 'statement') {
      out.blocks.push({ b: b, h: await textH(b.runs, spec('statement'), iw),
        s: spec('statement'), grow: 0 });
    } else if (b.k === 'lead' || b.k === 'para') {
      const s = b.k === 'lead' ? spec('lead') : spec('para');
      out.blocks.push({ b: b, h: await textH(b.runs, s, iw), s: s, grow: 0 });
    } else if (b.k === 'list') {
      const s = spec('li');
      let h = 0;
      const hs = [];
      for (let k = 0; k < b.items.length; k += 1) {
        const ih = await textH(b.items[k], s, iw - BULL_IN);
        hs.push(ih);
        h += ih;
      }
      out.blocks.push({ b: b, h: h, hs: hs, s: s, grow: 1.6 });
    } else if (b.k === 'table') {
      const padIn = (o.pad || 1.4) * MM;
      const g = await tableGeom(b, spec('td'), spec('th'), padIn, iw);
      out.blocks.push({ b: b, h: g.h, g: g, padIn: padIn, s: spec('td'),
        th: spec('th'), centred: CENTRED.has(key), grow: 1 });
    } else if (b.k === 'kpis') {
      const cols = KPI_COLS[box.cls] || 3;
      const rowsN = Math.ceil(b.items.length / cols);
      const kw = (iw - (cols - 1) * 2 * MM) / cols;
      const num = spec('kpiNum');
      const lbl = spec('kpiLbl');
      let lblLines = 1;
      for (let k = 0; k < b.items.length; k += 1) {
        lblLines = Math.max(lblLines, await lines(
          [{ t: b.items[k].lbl, b: true }], lbl[0], kw - 6 * MM - 0.02,
          { track: 0.1, upper: true }));
      }
      const kh = num[0] / 72 + 1.6 * MM + lblLines * lbl[0] * lbl[1] / 72
        + 4.8 * MM;
      out.blocks.push({ b: b, h: rowsN * kh + (rowsN - 1) * 2 * MM, cols: cols,
        rowsN: rowsN, kw: kw, kh: kh, num: num, lbl: lbl,
        grow: key === 'summary/b-numbers' ? 1 : 0,
        h0lbl: lblLines * lbl[0] * lbl[1] / 72 });
    } else if (b.k === 'cells') {
      const g = await cellsGeom(b, key, iw);
      out.blocks.push({ b: b, h: g.h, g: g, grow: 1.4 });
    } else if (b.k === 'seq') {
      const s = spec('para');
      let kw = 0;
      for (let k = 0; k < b.rows.length; k += 1) {
        kw = Math.max(kw, await runWidth([{ t: b.rows[k].k, b: true }],
          6.4, 0.1, true));
      }
      kw = Math.max(0.6, kw + 5.2 * MM);          // the pill's own padding
      const gutter = kw + 0.18;
      let h = 0;
      const hs = [];
      for (let k = 0; k < b.rows.length; k += 1) {
        const rh = Math.max(await textH(b.rows[k].runs, s, iw - gutter), 0.26);
        hs.push(rh);
        h += rh;
      }
      out.blocks.push({ b: b, h: h, hs: hs, s: s, kw: kw, gutter: gutter,
        grow: 2 });
    }
  }

  const gapN = Math.max(out.blocks.length - 1, 0);
  out.natural = out.labelH + 1.6 * MM + out.noteH + 2 * pad
    + out.blocks.reduce((a, x) => a + x.h, 0) + gapN * 1.6 * MM;
  out.avail = avail;
  return out;
}

function drawBox(s, box, m, geom) {
  const x = geom.x, y = geom.y, w = geom.w, h = geom.h;
  const pad = m.pad, iw = m.iw, spec = m.spec;
  s.addShape(pres.ShapeType.rect, {
    x: x, y: y, w: w, h: h, fill: { color: PAPER },
    line: { color: LINE, width: 0.6 },
  });
  if (box.accent) {
    s.addShape(pres.ShapeType.rect, {
      x: x, y: y, w: w, h: 1 * MM, fill: { color: ACCENT }, line: { width: 0 },
    });
  }

  let cy = y + pad;
  s.addText([
    { text: box.label.toUpperCase(), options: { color: ACCENT, bold: true } },
  ].concat(box.sub ? [{ text: '  ' + box.sub,
      options: { color: MUTED, bold: false,
                 charSpacing: spec('label')[0] * 0.04 } }] : []),
    Object.assign(body(spec('label'), {
      charSpacing: spec('label')[0] * 0.14,
    }), { x: x + pad, y: cy, w: iw, h: m.labelH }));
  cy += m.labelH + 1.6 * MM;

  // Slack goes to the blocks that stretch on the sheet, and to the gaps
  // between them, which is what the space-evenly rules in the CSS do.
  const bottom = y + h - pad - m.noteH;
  const slack = Math.max(0, (bottom - cy)
    - m.blocks.reduce((a, b) => a + b.h, 0)
    - Math.max(m.blocks.length - 1, 0) * 1.6 * MM);
  const growTotal = m.blocks.reduce((a, b) => a + b.grow, 0);
  const perGap = m.blocks.length > 1
    ? Math.min(slack * 0.45 / (m.blocks.length - 1), 3 * MM) : 0;
  const pool = Math.max(0, slack - perGap * Math.max(m.blocks.length - 1, 0));

  m.blocks.forEach((blk, i) => {
    const grow = growTotal > 0 ? pool * (blk.grow / growTotal) : 0;
    const b = blk.b;
    if (b.k === 'statement') {
      s.addText(rich(b.runs, INK), Object.assign(
        body(blk.s, { color: INK, bold: true }),
        { x: x + pad, y: cy, w: iw, h: blk.h }));
      cy += blk.h;
    } else if (b.k === 'lead' || b.k === 'para') {
      const lead = b.k === 'lead';
      s.addText(rich(b.runs, lead ? INK : MUTED), Object.assign(
        body(blk.s, { color: lead ? INK : MUTED, bold: lead }),
        { x: x + pad, y: cy, w: iw, h: blk.h }));
      cy += blk.h + grow;
    } else if (b.k === 'list') {
      const lead = grow / Math.max(b.items.length - 1, 1);
      let ly = cy;
      b.items.forEach((it, k) => {
        bulletMark(s, x + pad, ly, blk.s);
        s.addText(rich(it, MUTED), Object.assign(
          body(blk.s, { color: MUTED }),
          { x: x + pad + BULL_IN, y: ly, w: iw - BULL_IN, h: blk.hs[k] }));
        ly += blk.hs[k] + lead;
      });
      cy += blk.h + grow;
    } else if (b.k === 'table') {
      drawTable(s, b, blk.g, blk.s, blk.th, blk.padIn, x + pad, cy, grow,
        blk.centred);
      cy += blk.h + grow;
    } else if (b.k === 'kpis') {
      const gap = 2 * MM;
      const kh = blk.kh + grow / blk.rowsN;
      b.items.forEach((k, idx) => {
        const kx = x + pad + (idx % blk.cols) * (blk.kw + gap);
        const ky = cy + Math.floor(idx / blk.cols) * (kh + gap);
        s.addShape(pres.ShapeType.rect, {
          x: kx, y: ky, w: blk.kw, h: kh, fill: { color: TINT },
          line: { color: LINE, width: 0.6 },
        });
        const numH = blk.num[0] / 72 + 0.05;
        const lblH = blk.h0lbl;
        const ty = ky + Math.max(2.4 * MM, (kh - numH - 1.6 * MM - lblH) / 2);
        s.addText(k.num, Object.assign(
          body(blk.num, { bold: true, color: ACCENT }),
          { x: kx + 3 * MM, y: ty, w: blk.kw - 6 * MM, h: numH }));
        s.addText(k.lbl.toUpperCase(), Object.assign(
          body(blk.lbl, { bold: true, color: MUTED,
            charSpacing: blk.lbl[0] * 0.1 }),
          { x: kx + 3 * MM, y: ty + numH + 1.6 * MM,
            w: blk.kw - 6 * MM, h: lblH }));
      });
      cy += blk.h + grow;
    } else if (b.k === 'cells') {
      drawCells(s, blk.g, x + pad, cy, blk.h + grow);
      cy += blk.h + grow;
    } else if (b.k === 'seq') {
      const lead = grow / Math.max(b.rows.length - 1, 1);
      let ry = cy;
      b.rows.forEach((r, k) => {
        s.addShape(pres.ShapeType.roundRect, {
          x: x + pad, y: ry, w: blk.kw, h: 0.225, rectRadius: 0.1125,
          fill: { color: INK }, line: { width: 0 },
        });
        s.addText(r.k.toUpperCase(), {
          x: x + pad, y: ry, w: blk.kw, h: 0.225, isTextBox: true, margin: 0,
          fontFace: FONT, bold: true, fontSize: 6.4, charSpacing: 0.64,
          color: PAPER, align: 'center', valign: 'middle', fit: 'none',
        });
        s.addText(rich(r.runs, MUTED), Object.assign(
          body(blk.s, { color: MUTED }),
          { x: x + pad + blk.gutter, y: ry - 0.014, w: iw - blk.gutter,
            h: blk.hs[k] }));
        ry += blk.hs[k] + lead;
      });
      cy += blk.h + grow;
    }
    if (i < m.blocks.length - 1) cy += 1.6 * MM + perGap;
  });

  if (m.note) {
    const ny = y + h - pad - m.noteH + 3.4 * MM;
    s.addShape(pres.ShapeType.line, {
      x: x + pad, y: ny - 1.6 * MM, w: iw, h: 0,
      line: { color: LINE, width: 0.6 },
    });
    s.addText(txt(m.note.runs), Object.assign(
      body(spec('note'), { italic: true, color: MUTED }),
      { x: x + pad, y: ny, w: iw, h: m.noteH - 3.4 * MM }));
  }
}

/* -------------------------------------------------------------------- run */

(async () => {
  const browser = await openMeasure();
  const warnings = [];

  for (let si = 0; si < C.sheets.length; si += 1) {
    const sheet = C.sheets[si];
    const L = LAYOUT[sheet.key];
    const s = pres.addSlide();
    s.background = { color: PAPER };
    await header(s, sheet);
    const rows = rowGeom(L.rows);
    for (let bi = 0; bi < sheet.boxes.length; bi += 1) {
      const box = sheet.boxes[bi];
      const p = L.boxes[box.cls];
      if (!p) throw new Error('no layout for ' + sheet.key + ' ' + box.cls);
      const geom = { x: colX(p[0]), y: rows[p[2] - 1].y,
                     w: colW(p[0], p[1]), h: rows[p[2] - 1].h };
      const m = await measureBox(box, sheet.key + '/' + box.cls, geom.w, geom.h);
      if (m.natural > geom.h + 0.01) {
        warnings.push(sheet.key + '/' + box.cls + ' over by '
          + ((m.natural - geom.h) * 25.4).toFixed(1) + 'mm');
      }
      drawBox(s, box, m, geom);
    }
    s.addNotes('Editable. Text boxes and tables, not pictures. Words match the '
      + 'A3 sheet of the same name; if you change them here, tell us so the '
      + 'printed sheet is rebuilt to match.');
  }

  await browser.close();
  if (warnings.length) {
    console.error('OVERSET:');
    warnings.forEach((w) => console.error('  ' + w));
  } else {
    console.error('every box fits its row');
  }
  await pres.writeFile({ fileName: OUT });
  console.log('wrote ' + OUT);
})();
