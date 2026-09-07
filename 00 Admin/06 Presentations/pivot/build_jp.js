/*
 * JP_TapThat_ThePivot_v03 -- layout only. Words come from jp_content.py.
 *
 * Built to jp-brand-presentation, Brand Book Edition 02, locked May 2026.
 * Cream ground, Jewell Black type, Signal Blue as the single accent and only
 * on the three numbers that carry the argument. Poppins throughout, addressed
 * by its real installed family names (Poppins Light / Medium / SemiBold)
 * rather than by weight flags, which is how Office resolves it too.
 *
 * Five slide types and no others: title, content, divider, gate, closer. No
 * gate here, because nothing in this deck is being signed off.
 *
 * Type and space first, colour third, decoration never. There are no icons,
 * no accent bars and no shapes that are not carrying content. Rules are 0.75pt
 * hairlines and they separate; they never decorate.
 */

const pptxgen = require('pptxgenjs');
const fs = require('fs');

const C = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const OUT = process.argv[3];
const A = C._assets;

const CREAM = 'FAF8F4';
const BLACK = '111111';
const GREY = '666666';
const CALM = 'EDEBEA';
const HAIR = 'D8D4CF';       // Calm Grey a shade down, so a 0.75pt rule reads
const BLUE = '2D5BFF';       // Signal Blue. Slide 05 only.

// Two weights, as briefed. SemiBold carries every heading, figure and label;
// Regular carries every line meant to be read as a sentence. Poppins Light and
// Medium are deliberately absent, so nothing can drift back to a third weight.
const REG = 'Poppins';
const SEMI = 'Poppins SemiBold';

const W = 13.333, H = 7.5, M = 1.0;
const COL = W - 2 * M;       // 11.333

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.author = 'Jewell Projects';
pres.company = 'Jewell Projects';
pres.title = 'Tap That -- The Pivot';

const cream = () => {
  const s = pres.addSlide();
  s.background = { color: CREAM };
  return s;
};

/* A 0.75pt hairline. The only rule this deck draws. */
function rule(s, x, y, w, color) {
  s.addShape(pres.ShapeType.line, {
    x, y, w, h: 0, line: { color: color || HAIR, width: 0.75 },
  });
}

/* Content slides open with a tracked eyebrow and a 42pt headline, and the
   48px gap between them is the brand book's, not a guess. */
function content(d) {
  const s = cream();
  s.addText(d.eyebrow.toUpperCase(), {
    x: M, y: 0.42, w: COL, h: 0.22, isTextBox: true, margin: 0,
    fontFace: SEMI, fontSize: 9, color: BLACK, charSpacing: 2,
  });
  const lines = d.headLines || 1;
  const headH = lines * 0.62;
  s.addText(d.head, {
    x: M, y: 0.86, w: COL, h: headH, isTextBox: true, margin: 0,
    fontFace: SEMI, fontSize: 42, color: BLACK, valign: 'top',
    lineSpacingMultiple: 1.06,
  });
  // 48px below the headline, per the brand book spacing scale.
  s.y0 = 0.86 + headH + 0.5;
  return s;
}

/* A grey note that sits at the foot rather than crowding the headline. */
function footnote(s, text) {
  s.addText(text, {
    x: M, y: 6.72, w: COL, h: 0.5, isTextBox: true, margin: 0,
    fontFace: REG, fontSize: 11, color: GREY, lineSpacingMultiple: 1.3,
  });
}

function divider(key) {
  const [part, title, strap] = C.DIVIDERS[key];
  const s = pres.addSlide();
  s.background = { color: BLACK };
  // Full bleed, graded almost to the Jewell Black ground it replaces. The
  // slide still reads as type on black; the room is just present behind it.
  s.addImage({ path: A.dividerPhotos[key], x: 0, y: 0, w: W, h: H });
  s.addText(part, {
    x: M, y: 0.42, w: COL, h: 0.28, isTextBox: true, margin: 0,
    fontFace: SEMI, fontSize: 14, color: CREAM, charSpacing: 3,
  });
  s.addText(title, {
    x: M, y: 2.5, w: COL, h: 1.9, isTextBox: true, margin: 0,
    fontFace: SEMI, fontSize: 120, color: CREAM, valign: 'middle',
  });
  s.addText(strap, {
    x: M, y: 4.68, w: 8.5, h: 0.4, isTextBox: true, margin: 0,
    fontFace: SEMI, fontSize: 16, color: CREAM,
  });
  return s;
}

/* ------------------------------------------------------------- 01 title */
{
  const s = cream();
  const tw = COL;
  s.addText(C.TITLE.topbar, {
    x: M, y: 0.4, w: tw, h: 0.24, isTextBox: true, margin: 0,
    fontFace: SEMI, fontSize: 9, color: BLACK, charSpacing: 2,
  });
  s.addText(C.TITLE.title, {
    x: M, y: 4.42, w: tw, h: 1.15, isTextBox: true, margin: 0,
    fontFace: SEMI, fontSize: 72, color: BLACK,
  });
  // Subtitle is a sentence, so it reads in Regular even at 28pt.
  s.addText(C.TITLE.sub, {
    x: M, y: 5.68, w: tw, h: 0.5, isTextBox: true, margin: 0,
    fontFace: REG, fontSize: 28, color: BLACK,
  });
  s.addText(C.TITLE.date, {
    x: M, y: 6.5, w: tw, h: 0.3, isTextBox: true, margin: 0,
    fontFace: REG, fontSize: 11, color: GREY,
  });
  s.addNotes('The plan is sound. The shape is the problem, and that is a much '
    + 'better problem to have. Everything after this is about focus.');
}

/* ------------------------------------------------------------ 02 divider */
divider('context').addNotes('Part one is what the numbers say, and what they '
  + 'do not say.');

/* -------------------------------------------------------- 03, 04 findings */
function findingsSlide(d) {
  const s = content(d);
  const rowH = 1.5;
  d.items.forEach((it, i) => {
    const y = s.y0 + i * rowH;
    rule(s, M, y, COL);
    s.addText(it[0], {
      x: M, y: y + 0.16, w: 0.7, h: 0.42, isTextBox: true, margin: 0,
      fontFace: SEMI, fontSize: 24, color: GREY,
    });
    s.addText(it[1], {
      x: M + 0.85, y: y + 0.16, w: 3.9, h: 0.9, isTextBox: true, margin: 0,
      fontFace: SEMI, fontSize: 15, color: BLACK, lineSpacingMultiple: 1.14,
    });
    s.addText(it[2], {
      x: M + 5.05, y: y + 0.16, w: COL - 5.05, h: 1.1, isTextBox: true,
      margin: 0, fontFace: REG, fontSize: 12.5, color: BLACK,
      lineSpacingMultiple: 1.34,
    });
  });
  rule(s, M, s.y0 + d.items.length * rowH, COL);
  return s;
}
findingsSlide(C.FINDINGS_A).addNotes('The second finding is the whole deck. '
  + 'The two units cancel each other out.');
findingsSlide(C.FINDINGS_B).addNotes('Six is the one that gives permission to '
  + 'change the shape of the business.');

/* ----------------------------------------------------------- 05 evidence */
{
  const d = C.EVIDENCE;
  const s = content(d);
  const iw = (COL - 3 * 0.34) / 4, ih = iw * 5 / 4;
  d.shots.forEach((shot, i) => {
    const x = M + i * (iw + 0.34);
    s.addImage({ path: A.evidence[i], x, y: s.y0, w: iw, h: ih });
    rule(s, x, s.y0 + ih + 0.22, iw);
    s.addText(shot[1], {
      x, y: s.y0 + ih + 0.34, w: iw, h: 0.7, isTextBox: true, margin: 0,
      fontFace: REG, fontSize: 12, color: BLACK, lineSpacingMultiple: 1.28,
    });
  });
  footnote(s, d.foot);
  s.addNotes('Everything in this deck comes out of this room. Worth a beat '
    + 'before the numbers.');
}

/* ------------------------------------------------------------ 06 numbers */
{
  const d = C.NUMBERS;
  const s = content(d);
  const cw = (COL - 1.2) / 3;
  d.stats.forEach((st, i) => {
    const x = M + i * (cw + 0.6);
    rule(s, x, s.y0, cw);
    // The one place Signal Blue appears. These three figures are the argument.
    s.addText(st[0], {
      x, y: s.y0 + 0.16, w: cw, h: 1.0, isTextBox: true, margin: 0,
      fontFace: SEMI, fontSize: 60, color: BLUE,
    });
    s.addText(st[1], {
      x, y: s.y0 + 1.28, w: cw, h: 1.3, isTextBox: true, margin: 0,
      fontFace: REG, fontSize: 13, color: BLACK, lineSpacingMultiple: 1.4,
    });
  });
  rule(s, M, s.y0 + 2.94, COL);
  s.addText(d.foot, {
    x: M, y: s.y0 + 3.16, w: 9.8, h: 1.0, isTextBox: true, margin: 0,
    fontFace: REG, fontSize: 14, color: BLACK, lineSpacingMultiple: 1.42,
  });
  s.addNotes('96 to 113 active refill customers, reached without a push. That '
    + 'is the proof the model works. The 20% is the number to be careful with.');
}

/* ----------------------------------------------------------- 06 cautions */
{
  const d = C.CAUTIONS;
  const s = content(d);
  const cw = COL * 0.48, gap = COL * 0.04;
  d.cols.forEach((c, i) => {
    const x = M + i * (cw + gap);
    rule(s, x, s.y0, cw);
    s.addText(c[0], {
      x, y: s.y0 + 0.2, w: cw, h: 0.34, isTextBox: true, margin: 0,
      fontFace: SEMI, fontSize: 14, color: BLACK,
    });
    s.addText(c[1], {
      x, y: s.y0 + 0.66, w: cw, h: 2.0, isTextBox: true, margin: 0,
      fontFace: REG, fontSize: 14, color: BLACK, lineSpacingMultiple: 1.5,
    });
  });
  s.addNotes('The census is 49 people answering forced-choice questions. It '
    + 'is colour, not a map.');
}

/* ------------------------------------------------------------ 07 divider */
divider('direction').addNotes('Ten moves. The first five change the shape of '
  + 'the business, the rest extend it.');

/* -------------------------------------------------------- 08, 09 the moves */
function movesSlide(d) {
  const s = content(d);
  const widths = [2.5, 2.35, 2.25, 4.233];
  const head = d.cols.map((t) => ({
    text: t,
    options: { fontFace: SEMI, fontSize: 9, color: BLACK, charSpacing: 2,
               fill: { color: CALM }, margin: [6, 8, 6, 8], valign: 'middle' },
  }));
  const body = d.rows.map((r) => r.map((cell, k) => ({
    text: cell,
    options: {
      fontFace: k === 0 ? SEMI : REG, fontSize: k === 0 ? 11 : 9.5,
      color: BLACK, margin: [9, 8, 9, 8], valign: 'top',
      lineSpacing: k === 0 ? 14 : 12,
    },
  })));
  s.addTable([head, ...body], {
    x: M, y: s.y0, w: COL, colW: widths, autoPage: false,
    border: [{ type: 'none' }, { type: 'none' },
             { type: 'solid', color: HAIR, pt: 0.75 }, { type: 'none' }],
  });
  return s;
}
movesSlide(C.CORE).addNotes('Moves one and three are the ones that change the '
  + 'shape of the business. Everything else waits on them.');
movesSlide(C.MORE).addNotes('Six has the best return per hour once the core '
  + 'five are running.');

/* ------------------------------------------------------------ 10 divider */
divider('collateral').addNotes('The artwork is in Tap That brand, not ours. '
  + 'It is their collateral.');

/* ------------------------------------------------------------- 11 flyers */
{
  const d = C.FLYERS_SLIDE;
  const s = content(d);
  footnote(s, d.body);
  const fw = 2.42, fh = fw * 297 / 210, gap = 0.42;
  const x0 = (W - (4 * fw + 3 * gap)) / 2;
  A.flyers.forEach((p, i) => {
    const x = x0 + i * (fw + gap);
    s.addImage({ path: p, x, y: s.y0, w: fw, h: fh });
    s.addText(d.captions[i], {
      x, y: s.y0 + fh + 0.08, w: fw, h: 0.26, isTextBox: true, margin: 0,
      fontFace: SEMI, fontSize: 10, color: BLACK,
    });
  });
  s.addNotes('These replace the two flyer artworks in the earlier draft, which '
    + 'were embedded as EMF vector and render blank anywhere other than '
    + 'PowerPoint on Windows. These are 200 dpi PNG, print-ready at A4.');
}

/* ------------------------------------------------------------ 12 wedding */
{
  const d = C.WEDDING;
  const s = content(d);
  const ih = 3.52, iw = ih * 210 / 297;
  s.addImage({ path: A.flyerLarge, x: M, y: s.y0, w: iw, h: ih });
  s.addText('The artwork, ready to send', {
    x: M, y: s.y0 + ih + 0.1, w: iw, h: 0.26, isTextBox: true, margin: 0,
    fontFace: SEMI, fontSize: 10, color: BLACK,
  });

  const x2 = M + iw + 0.75, cw = W - M - x2;
  d.steps.forEach((st, i) => {
    const y = s.y0 + i * 0.86;
    rule(s, x2, y, cw);
    s.addText(st[0], {
      x: x2, y: y + 0.12, w: 0.55, h: 0.3, isTextBox: true, margin: 0,
      fontFace: SEMI, fontSize: 16, color: GREY,
    });
    s.addText(st[1], {
      x: x2 + 0.6, y: y + 0.12, w: 2.5, h: 0.32, isTextBox: true, margin: 0,
      fontFace: SEMI, fontSize: 13, color: BLACK,
    });
    s.addText(st[2], {
      x: x2 + 3.2, y: y + 0.12, w: cw - 3.2, h: 0.62, isTextBox: true,
      margin: 0, fontFace: REG, fontSize: 11, color: BLACK,
      lineSpacingMultiple: 1.28,
    });
  });
  rule(s, x2, s.y0 + 4 * 0.86, cw);

  s.addText(d.strap, {
    x: x2, y: s.y0 + 3.66, w: cw, h: 0.24, isTextBox: true, margin: 0,
    fontFace: SEMI, fontSize: 9, color: BLACK, charSpacing: 2,
  });
  s.addText(d.body, {
    x: x2, y: s.y0 + 3.94, w: cw, h: 0.6, isTextBox: true, margin: 0,
    fontFace: REG, fontSize: 12, color: BLACK, lineSpacingMultiple: 1.32,
  });
  s.addNotes('The left column used to be a wireframe of a can and a keg. It is '
    + 'now the flyer that would actually go out.');
}

/* ----------------------------------------------------------- 13 concepts */
{
  const d = C.CONCEPTS;
  const s = content(d);
  // The renders were being cover-cropped into a 2.8:1 letterbox to make two
  // full-width rows fit, which sliced the tops and bottoms off the units and
  // read as stretched. The grid now holds a true 16:9 and takes the left two
  // thirds; the caveat moves into a right-hand column rather than the foot,
  // which is what pays for the width the images give up.
  const iw = 3.10, ih = iw * 9 / 16, gap = 0.26, rowGap = 0.55;
  d.images.forEach((im, i) => {
    const x = M + (i % 2) * (iw + gap);
    const y = s.y0 + Math.floor(i / 2) * (ih + rowGap);
    s.addImage({
      path: A.concepts[im[0]], x, y, w: iw, h: ih,
      sizing: { type: 'cover', w: iw, h: ih },
    });
    s.addText(im[1], {
      x, y: y + ih + 0.1, w: iw, h: 0.26, isTextBox: true, margin: 0,
      fontFace: SEMI, fontSize: 10, color: BLACK,
    });
  });
  const nx = M + 2 * iw + gap + 0.8;
  rule(s, nx, s.y0, W - M - nx);
  s.addText(d.body, {
    x: nx, y: s.y0 + 0.14, w: W - M - nx, h: 3.2, isTextBox: true, margin: 0,
    fontFace: REG, fontSize: 13, color: BLACK, lineSpacingMultiple: 1.4,
  });
  s.addNotes('Concepts only. Nobody has been approached and the marks are not '
    + 'licensed. Worth showing because the reaction tells you which '
    + 'partnership is worth chasing first.');
}

/* ------------------------------------------------------------ 14 divider */
divider('execution').addNotes('None of these is a big job. All of them are '
  + 'being paid for daily in conversion.');

/* ------------------------------------------------------- 15 housekeeping */
{
  const d = C.HOUSEKEEPING;
  const s = content(d);
  const rowH = 0.86;
  d.rows.forEach((r, i) => {
    const y = s.y0 + i * rowH;
    rule(s, M, y, COL);
    s.addText(r[0], {
      x: M, y: y + 0.16, w: 2.6, h: 0.34, isTextBox: true, margin: 0,
      fontFace: SEMI, fontSize: 14, color: BLACK,
    });
    s.addText(r[1], {
      x: M + 2.8, y: y + 0.16, w: COL - 2.8, h: 0.62, isTextBox: true,
      margin: 0, fontFace: REG, fontSize: 13, color: BLACK,
      lineSpacingMultiple: 1.32,
    });
  });
  rule(s, M, s.y0 + d.rows.length * rowH, COL);
}

/* ------------------------------------------------------------- 16 the ask */
{
  const d = C.HELP;
  const s = content(d);
  const cw = COL * 0.48, gap = COL * 0.04;
  d.cols.forEach((col, i) => {
    const x = M + i * (cw + gap);
    s.addText(col[0], {
      x, y: s.y0, w: cw, h: 0.26, isTextBox: true, margin: 0,
      fontFace: SEMI, fontSize: 9, color: BLACK, charSpacing: 2,
    });
    col[1].forEach((item, k) => {
      const y = s.y0 + 0.38 + k * 0.62;
      rule(s, x, y, cw);
      s.addText(item, {
        x, y: y + 0.13, w: cw, h: 0.46, isTextBox: true, margin: 0,
        fontFace: REG, fontSize: 13, color: BLACK, lineSpacingMultiple: 1.24,
      });
    });
    rule(s, x, s.y0 + 0.38 + col[1].length * 0.62, cw);
  });
  s.addNotes('Left is what the brief asked for. Right is what we would add. '
    + 'The CRM build has the shortest payback.');
}

/* -------------------------------------------------------------- 17 closer */
{
  const d = C.CLOSER;
  const s = cream();
  s.addText(d.word, {
    x: M, y: 2.4, w: COL, h: 1.9, isTextBox: true, margin: 0,
    fontFace: SEMI, fontSize: 120, color: BLACK, valign: 'middle',
  });
  s.addText(d.line1, {
    x: M, y: 4.68, w: 9, h: 0.3, isTextBox: true, margin: 0,
    fontFace: REG, fontSize: 14, color: BLACK,
  });
  s.addText(d.line2, {
    x: M, y: 5.02, w: 9, h: 0.3, isTextBox: true, margin: 0,
    fontFace: REG, fontSize: 14, color: BLACK,
  });
  s.addNotes('The date on line one needs setting before this goes to Justin.');
}

pres.writeFile({ fileName: OUT }).then(() => console.log('wrote ' + OUT));
