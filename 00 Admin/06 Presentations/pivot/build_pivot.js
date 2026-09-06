/*
 * Tap That -- The Pivot. Layout only; every word comes from pivot_content.py
 * via the JSON that build_pivot.py writes next to this file.
 *
 * Brand: 34 Brand Guidelines section 2. Brewery green is the ground on every
 * slide, gold accents it and never leads, off-white carries the reading. The
 * hexagon of the Tap That badge is the one repeated device -- it numbers the
 * moves and the journey steps, and nothing else on the deck is a shape for
 * decoration's sake.
 *
 * Type is Arial Narrow over Arial. Section 3 asks for bold condensed caps in
 * headlines, and Arial Narrow is the only genuinely condensed face that ships
 * with Office on both Windows and Mac, so the deck opens correctly on
 * Christy's machine and on Justin's.
 */

const pptxgen = require('pptxgenjs');
const fs = require('fs');

const C = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const OUT = process.argv[3];
const ASSETS = C._assets;

const GREEN = '14361D';      // Tap That Brewery green
const DEEP = '0C2113';       // card ground, a shade under the slide
const GOLD = 'CE9A49';
const WHITE = 'F4F2ED';
const OFF = 'DFDFDF';
const MUTED = 'A9B8AB';      // secondary reading, still 6:1 on the green

const HEAD = 'Arial Narrow';
const BODY = 'Arial';

const W = 13.333, H = 7.5, M = 0.55;
const COLW = W - 2 * M;

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.author = 'Jewell Projects';
pres.company = 'Jewell Projects';
pres.title = 'Tap That -- The Pivot';

function slide() {
  const s = pres.addSlide();
  s.background = { color: GREEN };
  return s;
}

/* Every content slide opens the same way: gold eyebrow, white headline. */
function header(s, eyebrow, head) {
  s.addText(eyebrow, {
    x: M, y: 0.34, w: COLW, h: 0.26, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 11, bold: true, color: GOLD, charSpacing: 3,
  });
  s.addText(head, {
    x: M, y: 0.62, w: COLW, h: 0.66, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 27, bold: true, color: WHITE, valign: 'top',
  });
  return s;
}

/* The badge hexagon, carrying a number. */
function hex(s, x, y, size, label, fs) {
  s.addShape(pres.ShapeType.hexagon, {
    x, y, w: size, h: size, fill: { color: GOLD }, line: { color: GOLD, width: 0 },
    rotate: 90,
  });
  s.addText(label, {
    x, y, w: size, h: size, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: fs, bold: true, color: DEEP,
    align: 'center', valign: 'middle',
  });
}

function card(s, x, y, w, h) {
  s.addShape(pres.ShapeType.rect, {
    x, y, w, h, fill: { color: DEEP }, line: { color: '25502F', width: 0.75 },
  });
}

/* ------------------------------------------------------------- 01 title */
{
  const s = slide();
  s.addImage({ path: ASSETS.titleBg, x: 0, y: 0, w: W, h: H });
  s.addImage({ path: ASSETS.badgeAlpha, x: M, y: 0.62, w: 1.72, h: 1.16 });
  s.addText(C.TITLE.brand, {
    x: M, y: 2.6, w: COLW, h: 0.44, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 22, bold: true, color: GOLD, charSpacing: 9,
  });
  s.addText(C.TITLE.head, {
    x: M - 0.06, y: 3.0, w: COLW, h: 1.5, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 96, bold: true, color: WHITE,
  });
  s.addText(C.TITLE.sub, {
    x: M, y: 4.6, w: 8.2, h: 0.5, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 16, color: OFF,
  });
  s.addText(C.TITLE.foot, {
    x: M, y: 6.62, w: 9, h: 0.34, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 11, color: MUTED, charSpacing: 2,
  });
  s.addNotes('The plan is sound. The shape is the problem, and that is a much '
    + 'better problem to have. Everything after this slide is about focus.');
}

/* ------------------------------------------------ 02 what we saw and heard */
{
  const d = C.SAW_HEARD;
  const s = header(slide(), d.eyebrow, d.head);
  const cw = (COLW - 0.5) / 2, rh = 1.92;
  d.items.forEach((it, i) => {
    const x = M + (i % 2) * (cw + 0.5);
    const y = 1.52 + Math.floor(i / 2) * rh;
    hex(s, x, y + 0.02, 0.32, String(i + 1), 12);
    s.addText(it[0], {
      x: x + 0.46, y, w: cw - 0.46, h: 0.3, isTextBox: true, margin: 0,
      fontFace: HEAD, fontSize: 14, bold: true, color: WHITE,
    });
    s.addText(it[1].map((t, k) => ({
      text: t, options: { breakLine: k < it[1].length - 1, paraSpaceAfter: 5 },
    })), {
      x: x + 0.46, y: y + 0.3, w: cw - 0.46, h: rh - 0.42, isTextBox: true,
      margin: 0, fontFace: BODY, fontSize: 11, color: MUTED, lineSpacingMultiple: 1.16,
    });
  });
  s.addNotes('Six findings. The second one is the whole deck: the two units '
    + 'cancel each other out.');
}

/* ------------------------------------------------------------- 03 vanity */
{
  const d = C.VANITY;
  const s = slide();
  s.addText(d.eyebrow, {
    x: M, y: 0.34, w: COLW, h: 0.26, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 11, bold: true, color: GOLD, charSpacing: 3,
  });
  s.addText(d.head, {
    x: M, y: 0.66, w: COLW, h: 1.5, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 46, bold: true, color: WHITE, lineSpacingMultiple: 0.94,
  });
  const cw = (COLW - 0.8) / 3;
  d.stats.forEach((st, i) => {
    const x = M + i * (cw + 0.4);
    card(s, x, 2.55, cw, 2.5);
    s.addText(st[0], {
      x: x + 0.24, y: 2.76, w: cw - 0.48, h: 0.95, isTextBox: true, margin: 0,
      fontFace: HEAD, fontSize: 54, bold: true, color: GOLD,
    });
    s.addText(st[1], {
      x: x + 0.24, y: 3.78, w: cw - 0.48, h: 1.1, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 11.5, color: OFF, lineSpacingMultiple: 1.2,
    });
  });
  s.addText(d.foot, {
    x: M, y: 5.5, w: COLW, h: 1.0, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 14, color: OFF, lineSpacingMultiple: 1.25,
  });
  s.addNotes('96-113 active refill customers, reached without a push. That is '
    + 'the proof the model works. The 20% is the number to be careful with.');
}

/* --------------------------------------------------- 04 and 05 the moves */
function movesSlide(d) {
  const s = header(slide(), d.eyebrow, d.head);
  const n = d.moves.length, gap = 0.16;
  const cw = (COLW - gap * (n - 1)) / n;
  d.moves.forEach((m, i) => {
    const x = M + i * (cw + gap);
    card(s, x, 1.46, cw, 5.6);
    hex(s, x + cw / 2 - 0.21, 1.68, 0.42, m.n, 15);
    s.addText(m.title, {
      x: x + 0.14, y: 2.3, w: cw - 0.28, h: 0.66, isTextBox: true, margin: 0,
      fontFace: HEAD, fontSize: 14.5, bold: true, color: WHITE,
      align: 'center', lineSpacingMultiple: 0.95,
    });
    s.addText(m.line, {
      x: x + 0.14, y: 3.02, w: cw - 0.28, h: 0.72, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 9.5, italic: true, color: MUTED,
      align: 'center', lineSpacingMultiple: 1.15,
    });
    s.addText([
      { text: 'PROOF  ', options: { bold: true, color: GOLD, fontFace: HEAD, charSpacing: 1.5 } },
      { text: m.proof, options: { color: OFF } },
    ], {
      x: x + 0.14, y: 3.8, w: cw - 0.28, h: 0.72, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 9, align: 'center', lineSpacingMultiple: 1.15,
    });
    s.addText(m.acts.map((a, k) => ({
      text: a,
      options: { bullet: true, breakLine: k < m.acts.length - 1, paraSpaceAfter: 6 },
    })), {
      x: x + 0.16, y: 4.6, w: cw - 0.3, h: 2.3, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 8.5, color: OFF, lineSpacingMultiple: 1.1,
    });
  });
  return s;
}
movesSlide(C.CORE).addNotes('Five moves, in order. One and three are the ones '
  + 'that change the shape of the business.');
movesSlide(C.MORE).addNotes('These only work once the core five are running. '
  + 'Six is the one with the best return per hour.');

/* ------------------------------------------------------- 06 event flyers */
{
  const d = C.FLYERS_SLIDE;
  const s = header(slide(), d.eyebrow, d.head);
  const fw = 2.9, fh = fw * 297 / 210, gap = 0.2;
  const total = 4 * fw + 3 * gap;
  const x0 = (W - total) / 2;
  ASSETS.flyers.forEach((p, i) => {
    const x = x0 + i * (fw + gap);
    s.addImage({ path: p, x, y: 1.72, w: fw, h: fh });
    s.addShape(pres.ShapeType.rect, {
      x, y: 1.72, w: fw, h: fh, fill: { type: 'none' },
      line: { color: '4A7A57', width: 0.75 },
    });
    s.addText(d.captions[i], {
      x, y: 1.86 + fh, w: fw, h: 0.28, isTextBox: true, margin: 0,
      fontFace: HEAD, fontSize: 12, bold: true, color: GOLD,
      align: 'center', charSpacing: 2,
    });
  });
  s.addText(d.note, {
    x: M, y: 6.6, w: COLW, h: 0.4, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 10, color: MUTED, align: 'center',
  });
  s.addNotes('These replace the two flyer artworks in the earlier draft. Those '
    + 'were embedded as EMF vector, which renders blank anywhere other than '
    + 'PowerPoint on Windows. These are 200 dpi PNG, print-ready at A4.');
}

/* ------------------------------------------------------ 07 wedding brew */
{
  const d = C.WEDDING;
  const s = header(slide(), d.eyebrow, d.head);
  const cw = (COLW - 0.7) / 3;

  // Left: the flyer itself, rather than a wireframe of one.
  const ih = 4.24, iw = ih * 210 / 297;
  s.addImage({ path: ASSETS.flyerLarge, x: M + (cw - iw) / 2, y: 1.58, w: iw, h: ih });
  s.addShape(pres.ShapeType.rect, {
    x: M + (cw - iw) / 2, y: 1.58, w: iw, h: ih, fill: { type: 'none' },
    line: { color: '4A7A57', width: 0.75 },
  });
  s.addText('The artwork, ready to send', {
    x: M, y: 5.92, w: cw, h: 0.3, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 12, bold: true, color: GOLD, align: 'center', charSpacing: 2,
  });

  // Middle: the four-step journey.
  const x2 = M + cw + 0.35;
  d.steps.forEach((st, i) => {
    const y = 1.58 + i * 1.14;
    hex(s, x2, y, 0.36, st[0], 13);
    s.addText(st[1], {
      x: x2 + 0.5, y: y - 0.02, w: cw - 0.5, h: 0.3, isTextBox: true, margin: 0,
      fontFace: HEAD, fontSize: 13.5, bold: true, color: WHITE,
    });
    s.addText(st[2], {
      x: x2 + 0.5, y: y + 0.27, w: cw - 0.5, h: 0.78, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 10, color: MUTED, lineSpacingMultiple: 1.16,
    });
  });

  // Right: what it earns.
  const x3 = M + 2 * (cw + 0.35);
  card(s, x3, 1.5, cw, 4.6);
  d.impact.forEach((im, i) => {
    s.addText([
      { text: im[0], options: { fontFace: HEAD, fontSize: 14, bold: true, color: GOLD, breakLine: true, paraSpaceAfter: 6 } },
      { text: im[1], options: { fontFace: BODY, fontSize: 10, color: OFF } },
    ], {
      x: x3 + 0.22, y: 1.66 + i * 1.44, w: cw - 0.44, h: 1.26, isTextBox: true,
      margin: 0, valign: 'middle', lineSpacingMultiple: 1.16,
    });
  });

  s.addShape(pres.ShapeType.rect, {
    x: 0, y: 6.44, w: W, h: 1.06, fill: { color: DEEP }, line: { width: 0 },
  });
  s.addText([
    { text: 'THE ECOSYSTEM EFFECT   ', options: { bold: true, color: GOLD, fontFace: HEAD, charSpacing: 2 } },
    { text: d.strap.replace('THE ECOSYSTEM EFFECT   ', ''), options: { color: OFF } },
  ], {
    x: M, y: 6.44, w: COLW, h: 1.0, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 11.5, valign: 'middle',
  });
  s.addNotes('The left-hand column used to be a wireframe of a can and a keg. '
    + 'It is now the flyer that would actually go out.');
}

/* --------------------------------------------------- 08 partnership concepts */
{
  const d = C.CONCEPTS;
  const s = header(slide(), d.eyebrow, d.head);
  const cw = (COLW - 0.3) / 2, ih = 2.16;
  d.images.forEach((im, i) => {
    const x = M + (i % 2) * (cw + 0.3);
    const y = 1.52 + Math.floor(i / 2) * (ih + 0.62);
    s.addImage({
      path: ASSETS.concepts[im[0]], x, y, w: cw, h: ih,
      sizing: { type: 'cover', w: cw, h: ih },
    });
    s.addText(im[1], {
      x, y: y + ih + 0.06, w: cw, h: 0.28, isTextBox: true, margin: 0,
      fontFace: HEAD, fontSize: 12, bold: true, color: GOLD, charSpacing: 2,
    });
  });
  s.addText(d.note, {
    x: M, y: 6.86, w: COLW, h: 0.34, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 10, color: MUTED,
  });
  s.addNotes('Concepts only. Nobody has been approached, and the marks are not '
    + 'licensed. Worth showing because the reaction to them tells you which '
    + 'partnership is worth chasing first.');
}

/* --------------------------------------------------------- 09 other notes */
{
  const d = C.NOTES;
  const s = header(slide(), d.eyebrow, d.head);
  const cw = (COLW - 0.4) / 2;
  d.cards.forEach((c, i) => {
    const x = M + i * (cw + 0.4);
    card(s, x, 1.72, cw, 3.9);
    s.addText([
      { text: c[0], options: { fontFace: HEAD, fontSize: 25, bold: true, color: GOLD, breakLine: true, paraSpaceAfter: 14 } },
      { text: c[1], options: { fontFace: BODY, fontSize: 15, color: OFF } },
    ], {
      x: x + 0.42, y: 1.72, w: cw - 0.84, h: 3.9, isTextBox: true, margin: 0,
      valign: 'middle', lineSpacingMultiple: 1.3,
    });
  });
  s.addNotes('The census is 49 people answering forced-choice questions. It is '
    + 'colour, not a map.');
}

/* -------------------------------------------------------- 10 housekeeping */
{
  const d = C.HOUSEKEEPING;
  const s = header(slide(), d.eyebrow, d.head);
  const labw = 2.15;
  d.rows.forEach((r, i) => {
    const y = 1.62 + i * 1.02;
    hex(s, M, y + 0.03, 0.3, String(i + 1), 11);
    s.addText(r[0], {
      x: M + 0.44, y, w: labw, h: 0.4, isTextBox: true, margin: 0,
      fontFace: HEAD, fontSize: 15, bold: true, color: WHITE, valign: 'top',
    });
    s.addText(r[1], {
      x: M + 0.44 + labw, y: y - 0.02, w: COLW - 0.44 - labw, h: 0.86, isTextBox: true,
      margin: 0, fontFace: BODY, fontSize: 12.5, color: OFF,
      lineSpacingMultiple: 1.18, valign: 'top',
    });
  });
  s.addNotes('None of these is a big job. All of them are being paid for daily '
    + 'in conversion.');
}

/* ------------------------------------------------------------- 11 the ask */
{
  const d = C.HELP;
  const s = header(slide(), d.eyebrow, d.head);
  const cw = (COLW - 0.6) / 2;
  d.cols.forEach((col, i) => {
    const x = M + i * (cw + 0.6);
    s.addText(col[0], {
      x, y: 1.62, w: cw, h: 0.32, isTextBox: true, margin: 0,
      fontFace: HEAD, fontSize: 13, bold: true, color: GOLD, charSpacing: 3,
    });
    col[1].forEach((item, k) => {
      const y = 2.16 + k * 0.78;
      s.addShape(pres.ShapeType.hexagon, {
        x, y: y + 0.13, w: 0.17, h: 0.17, rotate: 90,
        fill: { color: GOLD }, line: { width: 0 },
      });
      s.addText(item, {
        x: x + 0.34, y, w: cw - 0.34, h: 0.66, isTextBox: true, margin: 0,
        fontFace: BODY, fontSize: 12.5, color: OFF, lineSpacingMultiple: 1.2,
      });
    });
  });
  s.addNotes('Left is what the brief asked for. Right is what we would add, '
    + 'and the CRM build is the one with the shortest payback.');
}

pres.writeFile({ fileName: OUT }).then(() => console.log('wrote ' + OUT));
