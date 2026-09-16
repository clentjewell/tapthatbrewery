/*
 * Proposal v02 for Tap That Brewery, in the Jewell Projects document format.
 *
 * Supersedes the 28 August draft, which was written before the Pivot was
 * presented, before Justin's own plan arrived, and before the plan on a page
 * existed. This one proposes the execution engagement against that plan: the
 * set of activities, on Justin's horizons, with the fees left for Clent to
 * set because no rate card exists in this repository and none should be
 * invented.
 *
 *   NODE_PATH=<scratch>/node_modules node build_proposal.js <out.docx>
 */

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, BorderStyle, AlignmentType, TabStopType, PageNumber, Footer,
  ImageRun, LevelFormat, ShadingType, VerticalAlign,
} = require('docx');

const OUT = process.argv[2];
const LOGO = path.resolve(__dirname, '../../11 Final Outputs/brand-source/jewell-logo-source.png');

const BLUE = '0066FF', BLACK = '000000', GREY = '666666', RULE = 'D9D9D9';
const FONT = 'Poppins';
const A4 = { width: 11906, height: 16838 };
const MARGIN = 1440;
const TEXT_W = A4.width - 2 * MARGIN;         // 9026 DXA

/* ---- helpers ------------------------------------------------------- */

const run = (t, o = {}) => new TextRun(Object.assign({ text: t, font: FONT, size: 22, color: BLACK }, o));
const b = (t) => run(t, { bold: true });
const i = (t) => run(t, { italics: true });

const P = (children, o = {}) => new Paragraph(Object.assign({
  children: Array.isArray(children) ? children : [run(children)],
  spacing: { line: 360, after: 120 },
}, o));

const H = (t) => new Paragraph({
  children: [run(t, { bold: true, size: 28, color: BLUE })],
  spacing: { before: 360, after: 160 },
  keepNext: true,
});

const SUB = (t) => new Paragraph({
  children: [run(t, { bold: true, size: 22 })],
  spacing: { before: 200, after: 80, line: 300 },
  keepNext: true,
});

const Note = (t) => P([run('– ' + t, { italics: true })]);

const bullet = (children, ref = 'jp-bullets') => new Paragraph({
  children: Array.isArray(children) ? children : [run(children)],
  numbering: { reference: ref, level: 0 },
  spacing: { line: 360, after: 80 },
});
const numbered = (children, ref) => new Paragraph({
  children: Array.isArray(children) ? children : [run(children)],
  numbering: { reference: ref, level: 0 },
  spacing: { line: 360, after: 80 },
});

const rule = () => new Paragraph({
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BLACK, space: 1 } },
  spacing: { before: 120, after: 240 },
});

const noBorder = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const lightBorder = { style: BorderStyle.SINGLE, size: 4, color: RULE };

function cell(children, w, opts = {}) {
  const paras = (Array.isArray(children) ? children : [children]).map((c) =>
    c instanceof Paragraph ? c : new Paragraph({
      children: Array.isArray(c) ? c : [run(c, opts.runOpts || {})],
      spacing: { line: 300, after: 40 },
    }));
  return new TableCell({
    children: paras,
    width: { size: w, type: WidthType.DXA },
    borders: opts.borderless
      ? { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder }
      : { top: lightBorder, bottom: lightBorder, left: lightBorder, right: lightBorder },
    shading: opts.shade ? { type: ShadingType.CLEAR, fill: 'F2F2F2', color: 'auto' } : undefined,
    margins: { top: 80, bottom: 80, left: 100, right: 100 },
    verticalAlign: VerticalAlign.TOP,
  });
}

/* A standard three-column activity table: what, deliverable, horizon. */
function activityTable(rows, widths = [2700, 4626, 1700]) {
  const head = new TableRow({
    tableHeader: true,
    children: [
      cell([[b('Activity')]], widths[0], { shade: true }),
      cell([[b('What we deliver')]], widths[1], { shade: true }),
      cell([[b('When')]], widths[2], { shade: true }),
    ],
  });
  const body = rows.map((r) => new TableRow({
    children: [
      cell([[b(r[0])]], widths[0]),
      cell(r[1], widths[1]),
      cell(r[2], widths[2]),
    ],
  }));
  return new Table({
    width: { size: TEXT_W, type: WidthType.DXA },
    columnWidths: widths,
    rows: [head, ...body],
  });
}

function twoCol(rows, widths = [3000, 6026], shadeHead = true) {
  const body = rows.map((r, idx) => new TableRow({
    tableHeader: idx === 0 && shadeHead,
    children: [
      cell([[b(r[0])]], widths[0], { shade: idx === 0 && shadeHead }),
      cell(r[1], widths[1], { shade: idx === 0 && shadeHead }),
    ],
  }));
  return new Table({ width: { size: TEXT_W, type: WidthType.DXA }, columnWidths: widths, rows: body });
}

function metaTable(rows) {
  const widths = [2400, 6626];
  return new Table({
    width: { size: TEXT_W, type: WidthType.DXA },
    columnWidths: widths,
    rows: rows.map(([k, v]) => new TableRow({
      children: [
        cell([[run(k, { bold: true, size: 20 })]], widths[0], { borderless: true }),
        cell([[run(v, { size: 22 })]], widths[1], { borderless: true }),
      ],
    })),
  });
}

/* ---- content ------------------------------------------------------- */

const logo = new ImageRun({
  type: 'png',
  data: fs.readFileSync(LOGO),
  transformation: { width: 210, height: Math.round(210 * 734 / 3334) },
});

const brandBlock = [
  new Paragraph({ children: [logo], spacing: { after: 240 } }),
  new Paragraph({ children: [run('Proposal', { bold: true, size: 48, color: BLUE })], spacing: { after: 0 } }),
  new Paragraph({ children: [run('Executing the plan on a page', { bold: true, size: 48, color: BLUE })], spacing: { after: 240 } }),
];

const meta = metaTable([
  ['ENGAGEMENT', 'Tap That Brewery – marketing strategy and execution'],
  ['STATUS', 'Draft v02 – client-facing; investment to be confirmed'],
  ['AUDIENCE', 'Justin Mistry and Chris Smith, Tap That Brewery'],
  ['DATE', '16 September 2026'],
  ['SUPERSEDES', 'Proposal v01, 28 August 2026'],
  ['PREPARED BY', 'Jewell Projects'],
]);

const body = [];

body.push(H('Purpose'));
body.push(P('This proposal sets out the work Jewell Projects will do with Tap That Brewery over the next twelve months, and what it costs. It replaces the August proposal, which was written before the Pivot was presented on 15 September and before your own plan on a page arrived the following day. Everything in it now runs on your plan: your north star, your horizons, your priorities. Where we recommend something you have not yet adopted, it is marked as our recommendation.'));

body.push(H('Where You Are'));
body.push(P('Three weeks ago the diagnosis was that you did not have a strategy problem, you had an execution problem. That still holds, and the catch-up on 15 September sharpened it. The refill business is at MVP with 96 to 113 active customers reached without a marketing push. 56% of them bought their system somewhere else and switched to you anyway. The Tap Room makes money on events and functions and loses it as a walk-in venue. Meta ads are finally working and there is nowhere to send the traffic. The website, POS and CRM do not talk to each other, so every campaign is set up to underperform before it launches.'));
body.push(P([
  run('Your own plan, received on 16 September, puts the north star where it belongs: '),
  b('1,000 active keg refillers'),
  run(' across the Gold Coast, Brisbane and Northern Rivers by year three, with '),
  b('250 by March 2027'),
  run('. Not systems in the market, refillers. A system that is not refilling is worth nothing. Every activity below is tested against whether it moves that number.'),
]));
body.push(P([run('Your five priorities, in your words: find every existing keg system owner and switch them; website upgrade plus SEM; JVPs, referral partners and an internal referral programme; taproom traffic from local business, functions and ticketed music; wholesale. This proposal is built around those five, plus the foundations they all depend on.')]));

body.push(H('What We Are Proposing'));
body.push(P('Discover and Design are substantially done. The Discovery pack, the Pivot deck and the five-sheet plan on a page are delivered and in your hands. What is missing is the same thing it was in August: hands. One marketer at roughly seventy per cent capacity cannot run a switcher campaign, a referral programme, an events calendar, a wholesale pipeline and a CRM build at once, and Chris is trapped in production.'));
body.push(P('So this is a Deploy proposal. Jewell Projects becomes the delivery capacity around Harry for the next twelve months: we build, launch and run the activities below, to your plan, on your horizons, reporting one set of four numbers monthly. You keep every decision. We do the work between decisions.'));
body.push(P([i('The real constraint in this business is hands, not ideas. We said that in August. Nothing since has changed it.')]));

body.push(H('The Work, by Workstream'));
body.push(P('Seven workstreams. The first is the foundation the other six sit on. Each activity carries the horizon from your own plan on a page: 30 days to mid-October, three months to mid-December, six months to March 2027, one year to September 2027.'));

body.push(SUB('1. Connect the system'));
body.push(P('Nothing else compounds until this is done. Spending more on ads before it is fixed buys traffic the business cannot catch.'));
body.push(activityTable([
  ['Website upgrade', ['Rebuild around a buy path for systems and refills, with proof above the fold: the Crafted Brewers’ Choice award, fits-any-system, no CO2, strong reviews. About, FAQ and awards pages so both people and AI search can read it. Category language of its own rather than “commercial brewer”.'], ['3 months']],
  ['SEM', ['Search campaigns on the category nobody on the Gold Coast owns: beer at home, keg refills, keg systems. Budget and structure agreed with you; run by us; reported monthly.'], ['3 months']],
  ['GoTab and Fishbowl transition', ['Support the POS and inventory move so that every sale writes back to the customer record. We do not run the transition; we make sure the CRM and the website are ready for it and that nothing is built twice.'], ['3 months']],
  ['Trigger-based CRM', ['Replace the blanket 90-day SMS with reminders timed to each customer’s own consumption. Segments for owners who bought elsewhere, lapsed-forgot, lapsed-cutting-back and never-owned. A re-engagement flow for lapsed customers, split by reason once the CRM can tell us which.'], ['3 months']],
  ['Meta Ads budget breakdown', ['Confirmed split across switcher, giveaway, destination and retargeting, with a landing page for each rather than a home page for all.'], ['30 days']],
  ['One monthly report', ['Four numbers, one page: keg system sales, active keg refillers, wholesale accounts, and the lapse rate. Active refiller defined once, before the first report.'], ['30 days, then monthly']],
]));

body.push(SUB('2. Switch the owners who already have a system'));
body.push(P('Your number one, and ours. These people have already overcome every objection. They just buy their beer somewhere else.'));
body.push(activityTable([
  ['Harvey Norman', ['Gift-with-purchase or first-keg-free tied to keg system sales, at franchisee level. We hold contacts into Harvey Norman franchisees and a contact who has installed for Harvey Norman, JB Hi-Fi and The Good Guys at scale. The Bunnings-installer model: they sell the hardware, Tap That is the named first call for what goes in it.'], ['3 months']],
  ['Kegland, corny keg and Benchy', ['Buy or partner for the owner databases. Formalise the Benchy partnership. A voucher for a Tap That refill in the box.'], ['3 months']],
  ['Switcher campaign', ['One offer, one message, one landing page: “You already have the hardware. We are the beer. First keg on us.” Run across Meta, search and the CRM.'], ['3 months']],
  ['Lease-to-buy and delivery', ['Your launch items. We build the offer page, the CRM flow and the launch creative for lease-to-buy systems and the keg delivery service.'], ['3 months']],
]));

body.push(SUB('3. Referrals, JVPs and ambassadors'));
body.push(P('Your priority three and your one-year marker: referrals, JVPs and online driving the majority of system sales.'));
body.push(activityTable([
  ['Referral programme and Bring a Mate', ['Design, mechanics, CRM automation and creative. Referral is already 18% of acquisition and fewer than half the base knows a keg-system reward exists. Fixing that is the cheapest campaign on this list.'], ['3 months']],
  ['JVP and referral partner programme', ['The list, the offer, the outreach and the follow-up, run from the CRM. Starts with the contacts already named: Mark’s two wedding venues, the Zip water network, Never Quit, and the tour operators.'], ['3 months, ongoing']],
  ['UGC and brand ambassador content', ['A content programme with your named ambassadors, Kurt, Troy, Mitch, Aden and Ash: the brief, the shoot plan, the release schedule, the rights. Ready to deploy within three months.'], ['3 months']],
]));

body.push(SUB('4. The Tap Room as a destination'));
body.push(P('Your priority four. Local business, functions and ticketed music. The shape decision is yours; the programme below works under any of the three, and grows the room the way you want it grown.'));
body.push(activityTable([
  ['Oktoberfest and the keg system giveaway', ['The first dated event. Campaign, artwork, entry mechanics that feed the CRM, and the follow-up sequence that turns a thousand entries into system sales over the three-month buying cycle.'], ['30 days']],
  ['Local business programme', ['Lunch and after-work trade from the industrial area: the offer, the outreach list, the collateral.'], ['3 months']],
  ['Ticketed music and events calendar', ['A replicable calendar of ticketed events and collaborations, with the promotion built once and reused. Your one-year marker is a replicable events and promotions calendar; this is it.'], ['3 months, then quarterly']],
  ['Tours and tastings', ['Get onto the circuit: profiles updated with every operator, the award and the bus parking sold as the reasons to stop here, and a booking widget for Urban Legends so operators stop coordinating venue by venue.'], ['3 months']],
  ['Weddings and functions', ['The hens-and-bucks-to-wedding programme: tasting session, signature brew, reception supply, take-home sample. PR to planners, starting with Mark’s roughly 300 weddings a year.'], ['6 months']],
  ['Party rental and membership', ['Rethink party rental so a minimum keg guarantee replaces the $75 hire barrier. Redesign membership so one programme serves the refill business rather than two programmes serving two shapes.'], ['6 months']],
]));

body.push(SUB('5. Wholesale as a function'));
body.push(P('Bars have approached you and it has not converted. That is not a demand problem. It is the absence of follow-up, and about twelve touch points before a venue buys beer.'));
body.push(activityTable([
  ['Structure and KPIs', ['Targets, pipeline stages and reporting in the CRM, so the function exists before the person does. A one-page brief for the next hire, whichever way the brewer-versus-wholesale call goes.'], ['3 months']],
  ['Venue outreach programme', ['Event venues, niched venues and sporting clubs: the list, the offer, the twelve-touch sequence, run from the CRM until a hire takes it over.'], ['3 months, ongoing']],
  ['Club and venue offers', ['Club-branded kegs, season minimum guarantees, and rigs that move from footy to cricket. A packaged offer that works alongside duopoly contracts rather than against them.'], ['6 months']],
]));

body.push(SUB('6. Brand, range and proof'));
body.push(P('The brand is not being rebuilt. It is being sharpened around one enemy, overpriced pubs, and one line, yours: every household in Australia deserves beer on tap.'));
body.push(activityTable([
  ['Key messaging by target market', ['Your 30-day item. One page per segment: what we say, what we prove, what we ask. Built on $2.55 a schooner against $12 at the pub.'], ['30 days']],
  ['Customer journey mapped', ['Your 30-day item. From first contact to first refill to reorder, with the CRM trigger at each step.'], ['30 days']],
  ['Proof assets', ['The Crafted award, the reviews, fits-any-system and no CO2, produced for the website, the venue, the tap decals and social. Owned already, barely used.'], ['3 months']],
  ['Designing for her', ['A product and design brief, not a campaign: the range, the RTD, the hydration and light story, and a system that sits in eyesight at home. Wellness influencer collaborations as the first proof.'], ['6 months']],
  ['Range and heroes', ['Support the cut to hero brews with the product marketing behind them: social proof cues at the point of sale, most popular, award winner, what to eat with it.'], ['6 months']],
  ['Campaign artwork', ['Four event flyers are built. Next: Oktoberfest, the switcher campaign, the referral programme, the ambassador content, and everything the calendar needs, in Tap That’s own format.'], ['Ongoing']],
]));

body.push(SUB('7. Governance'));
body.push(activityTable([
  ['Meeting rhythm', ['Your 30-day item. A weekly 30 minutes with Harry, a monthly hour with the founders against the four numbers, and a review at each rung of your ladder.'], ['30 days, ongoing']],
  ['Who does what', ['The responsibility matrix on the Activation sheet, agreed and dated, so nothing sits with everybody.'], ['30 days']],
  ['Reviews on your ladder', ['Mid-October, mid-December, March 2027, September 2027. Every review asks first whether active refillers moved.'], ['As dated']],
]));

body.push(H('The First 30 Days'));
body.push(P('Your own 30-day list is the first sprint. We work it with you rather than around you.'));
const s1 = 'jp-num-1';
body.push(numbered([b('The shape decision. '), run('Taproom selling kegs, showroom selling beers, or event space doing both. Our recommendation stays on the table: pause walk-in trade and point the room at destination demand. Your call, and everything below works under any answer.')], s1));
body.push(numbered([b('Residential versus commercial. '), run('Where the energy goes. The refill data can answer this in a week once the CRM can be read.')], s1));
body.push(numbered([b('Key messaging and the customer journey. '), run('Delivered by us, signed by you.')], s1));
body.push(numbered([b('KPIs and the meeting rhythm. '), run('Four numbers, one definition of active refiller, one weekly and one monthly meeting.')], s1));
body.push(numbered([b('External support versus in-house. '), run('This proposal is the answer to that question. What we do, what Harry does, what waits for the hire.')], s1));
body.push(numbered([b('Ambassadors named, Oktoberfest run. '), run('The giveaway mechanics feed the CRM from day one.')], s1));
body.push(numbered([b('Settle $2.55. '), run('One per-schooner figure on the live ad and on every piece of collateral, and the other sets of maths retired.')], s1));

body.push(H('Timeline, on Your Ladder'));
body.push(twoCol([
  ['Horizon', ['What is true at the end of it']],
  ['30 days – mid-October', ['Shape decided. Messaging and journey signed. KPIs, definitions and meeting rhythm set. Oktoberfest run, giveaway entries in the CRM. $2.55 on the ad.']],
  ['3 months – mid-December', ['Website and SEM live. GoTab and Fishbowl connected, CRM triggers replacing the 90-day SMS. Lease-to-buy and delivery launched. Harvey Norman and Kegland conversations open. Referral programme and Bring a Mate live. Ambassador content deploying. Wholesale pipeline in the CRM. Next hire decided.']],
  ['6 months – March 2027', ['250 active keg refillers. Wedding and functions programme selling. Membership redesigned. Designing-for-her brief in market. Career pathways for Chris and Harry defined.']],
  ['1 year – September 2027', ['Referrals, JVPs and online driving most system sales. Replicable events calendar running. Cashflow positive, Justin on a wage.']],
]));
body.push(Note('The longer horizons on your plan, 1,000 refillers and proprietary system supply at three years, expansion and a production facility at five, an exit at ten to twelve, are on the summary sheet. This proposal covers the first year of the climb.'));

body.push(H('Ways of Working'));
body.push(bullet([b('Weekly with Harry. '), run('Thirty minutes: progress, blockers, what we need. Harry is the operator; everything we build is runnable by that seat.')]));
body.push(bullet([b('Monthly with the founders. '), run('One hour against the four numbers. Decisions taken in the room and recorded.')]));
body.push(bullet([b('Reviews on your ladder. '), run('Mid-October, mid-December, March, September. A written review at each, and a stop-or-continue conversation at each.')]));
body.push(bullet([b('One source of truth. '), run('Everything lives in the shared engagement folder and on the plan on a page. Nothing important travels only by text.')]));
body.push(bullet([b('Sign-off. '), run('One named person on your side, our suggestion is Justin with Chris consulted on brand and product, approves messaging, offers and anything that goes to market.')]));
body.push(bullet([b('Coverage. '), run('Clent is overseas from the end of September. The weekly rhythm continues online and Christy carries strategy in the room.')]));

body.push(H('What We Need From You'));
body.push(twoCol([
  ['Input', ['Why, and when']],
  ['The shape decision', ['Everything on the Business sheet follows from it. Within 30 days.']],
  ['One definition of active keg refiller', ['Before the first monthly report, or the number gets argued about instead of acted on.']],
  ['$2.55 as the per-schooner figure', ['Confirmed as the number on the live ad, and the other maths retired. Within 30 days.']],
  ['GoTab and Fishbowl timeline', ['It sequences the CRM build. Before the three-month sprint starts.']],
  ['Introductions', ['Kurt, Troy, Mitch, Aden and Ash; Mark’s venues; the Kegland and Benchy contacts. As the workstreams open.']],
  ['The breakeven period', ['Your one-page plan gives about $50k without saying per month or per year. One line back.']],
  ['A named sign-off holder', ['One signature that closes each checkpoint. At kick-off.']],
]));

body.push(H('Investment and Terms'));
body.push(P('Two options, so you can choose the commitment that fits a business that is not yet cashflow positive. Both run on the same plan and the same rhythm.'));
body.push(twoCol([
  ['Option', ['Structure']],
  ['A. Ninety-day sprint, then review', ['A fixed fee for the first 30-day and three-month horizons, ending at the mid-December review with a stop-or-continue decision. Fee: [to be confirmed]. Payment: [to be confirmed].']],
  ['B. Twelve-month retainer', ['A monthly fee for the full year to September 2027, reviewed at each rung of your ladder with the right to stop at any review. Fee: [to be confirmed] per month. Payment: [to be confirmed].']],
  ['Not included', ['Media spend (Meta, search), which is paid by Tap That directly and reported by us. Photography and video production days, quoted per shoot. Third-party software, including GoTab, Fishbowl and any booking tool licence. Print.']],
  ['Case study', ['We ask for the right to tell this story once the numbers have moved, with your approval of the final text.']],
], [3000, 6026]));
body.push(Note('Fees and payment terms are being confirmed and will be set before this proposal is issued. No figure in this document is an estimate of them.'));

body.push(H('Decisions This Proposal Needs'));
const s2 = 'jp-num-2';
body.push(numbered('Which option, A or B.', s2));
body.push(numbered('Who signs for Tap That Brewery.', s2));
body.push(numbered('A start date. We propose the week of 21 September, so the 30-day sprint lands before the end of October and Oktoberfest is inside it.', s2));

body.push(H('Sign-off'));
body.push(twoCol([
  ['Accepted for Tap That Brewery', ['Name: ____________________   Signature: ____________________   Date: __________']],
  ['For Jewell Projects', ['Name: Clent Jewell   Signature: ____________________   Date: __________']],
], [3000, 6026], false));

body.push(H('Appendix A – What Is Already Delivered'));
body.push(P('All of the following exist, are in the shared folder, and are the basis for this proposal.'));
body.push(bullet([b('The Discovery pack. '), run('Audience, competitors, offers, economics and the six priority problems, with the census worked through it.')]));
body.push(bullet([b('The Pivot. '), run('Eighteen slides presented on 15 September: six findings, ten moves, the collateral, the small fixes and the scope.')]));
body.push(bullet([b('The plan on a page. '), run('Five A3 sheets, v02, reworked on 16 September around your own plan: the summary, business, brand, sales and marketing, activation. Editable PowerPoint and print master.')]));
body.push(bullet([b('Four event flyers. '), run('Weddings, bucks and hens, work functions, tours and tastings. Print-ready A4 in Tap That’s own format, in two image sets.')]));
body.push(bullet([b('The catch-up transcript. '), run('Verbatim, filed, and the reference where anything above is in question.')]));

/* ---- document ------------------------------------------------------ */

const footer = new Footer({
  children: [new Paragraph({
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: BLACK, space: 4 } },
    tabStops: [
      { type: TabStopType.CENTER, position: Math.round(TEXT_W / 2) },
      { type: TabStopType.RIGHT, position: TEXT_W },
    ],
    children: [
      run('Jewell Projects', { size: 18, color: GREY }),
      run('\tProposal v02 – Tap That Brewery', { size: 18, color: GREY }),
      run('\tPage ', { size: 18, color: GREY }),
      new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18, color: GREY }),
      run(' of ', { size: 18, color: GREY }),
      new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT, size: 18, color: GREY }),
    ],
  })],
});

const bulletLevel = { level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
  style: { paragraph: { indent: { left: 540, hanging: 300 } } } };
const numLevel = { level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
  style: { paragraph: { indent: { left: 540, hanging: 360 } } } };

const doc = new Document({
  creator: 'Jewell Projects',
  title: 'Proposal – Executing the plan on a page – Tap That Brewery',
  styles: { default: { document: { run: { font: FONT, size: 22, color: BLACK } } } },
  numbering: { config: [
    { reference: 'jp-bullets', levels: [bulletLevel] },
    { reference: 'jp-num-1', levels: [numLevel] },
    { reference: 'jp-num-2', levels: [numLevel] },
  ] },
  sections: [{
    properties: { page: { size: A4, margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN } } },
    footers: { default: footer },
    children: [...brandBlock, meta, rule(), ...body],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log('wrote ' + OUT + ' (' + buf.length.toLocaleString() + ' bytes)');
});
