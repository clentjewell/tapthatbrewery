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
  ['STATUS', 'Draft v03 – client-facing, with scoped costs'],
  ['AUDIENCE', 'Justin Mistry and Chris Smith, Tap That Brewery'],
  ['DATE', '23 September 2026'],
  ['SUPERSEDES', 'Proposal v02, 16 September 2026'],
  ['PREPARED BY', 'Jewell Projects'],
]);

const body = [];

body.push(H('Purpose'));
body.push(P('This proposal sets out the work Jewell Projects will do with Tap That Brewery over the next twelve months, and what it costs. It replaces the 16 September draft, which was written before the catch-up on 18 September settled the shape of the room, the brand position and the meeting rhythm. Everything in it runs on your plan: your north star, your horizons, your priorities. Where we recommend something you have not yet adopted, it is marked as our recommendation.'));

body.push(H('Where You Are'));
body.push(P('Three weeks ago the diagnosis was that you did not have a strategy problem, you had an execution problem. That still holds, and the catch-up on 15 September sharpened it. The refill business is at MVP with 96 to 113 active customers reached without a marketing push. 56% of them bought their system somewhere else and switched to you anyway. The Tap Room makes money on events and functions and loses it as a walk-in venue. On 18 September you settled that in principle: the room is an events and local business venue, not a walk-in bar. Your own words, that Oktoberfest is a sugar hit and you would take week-on-week revenue over it, are the clearest statement of strategy in three weeks of conversation. Meta ads are finally working and there is nowhere to send the traffic. The website, POS and CRM do not talk to each other, so every campaign is set up to underperform before it launches.'));
body.push(P([
  run('Your own plan, received on 16 September, puts the north star where it belongs: '),
  b('1,000 active keg refillers'),
  run(' across the Gold Coast, Brisbane and Northern Rivers by year three, with '),
  b('250 by March 2027'),
  run('. Not systems in the market, refillers. A system that is not refilling is worth nothing. Every activity below is tested against whether it moves that number.'),
]));
body.push(P('On 18 September you also closed the money question. Break-even is about $50,000 a month against a current run rate of $35,000 to $45,000, and one month has already hit it. You confirmed that 250 active refillers clears it, so the six-month number and the money number are the same number. Christy has put 250 by Christmas on the table given the outdoor entertaining season. You have not chosen between Christmas and March, and that date should be settled before this is signed.'));
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
  ['Website upgrade', ['A CMS you run yourself, so the shop page stops being someone else’s ticket. Wired to GoTab, Fishbowl, the Meta Pixel and the CRM, built around a buy path for systems and refills, with proof above the fold: the Crafted Brewers’ Choice award, fits-any-system, no CO2, strong reviews, and the integrated units that are selling now and are nowhere on the site. About, FAQ and awards pages so both people and AI search can read it. Category language of its own rather than “commercial brewer”. Platform-agnostic: Shopify if it fits, custom if it integrates better. The last rebuild missed its Easter launch on broken integrations, so the acceptance test here is that every integration is proven before launch, not promised.'], ['3 months']],
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
  ['Outdoor kitchen and appliance specification', ['Get a compact keg-and-tap unit specified as a standard inclusion in outdoor kitchens, the way the bar fridge already is. Renders and visuals first, tested on social for demand before anything is manufactured. It opens the outdoor living aisle, where keg systems do not currently appear at all.'], ['6 months']],
  ['Kegland, corny keg and Benchy', ['Buy or partner for the owner databases. Formalise the Benchy partnership. A voucher for a Tap That refill in the box.'], ['3 months']],
  ['Switcher campaign', ['One offer, one message, one landing page: “You already have the hardware. We are the beer. First keg on us.” Run across Meta, search and the CRM.'], ['3 months']],
  ['Lease-to-buy and delivery', ['Your launch items. We build the offer page, the CRM flow and the launch creative for lease-to-buy systems and the keg delivery service.'], ['3 months']],
]));

body.push(SUB('3. Referrals, JVPs and ambassadors'));
body.push(P('Your priority three and your one-year marker: referrals, JVPs and online driving the majority of system sales.'));
body.push(activityTable([
  ['Referral programme and Bring a Mate', ['Referral is already 18% of acquisition, on a programme nobody can hold in their hand: 1,000 tap tokens, about $50 or half a keg, for a system or wholesale referral, and 500 for a refill customer. Tokens do not travel. A free keg does. We rebuild it as a free keg and a card with a QR code an owner can hand to a mate, with the CRM automation and the creative behind both. The cheapest campaign on this list.'], ['3 months']],
  ['JVP and referral partner programme', ['The list, the offer, the outreach and the follow-up, run from the CRM. Starts with the contacts already named: Mark’s two wedding venues, the Zip water network, Value H2O and its east coast service base, Jim’s Mowing for the backyard, Never Quit, and the tour operators.'], ['3 months, ongoing']],
  ['Trades as a referral force', ['Plumbers, kitchen installers and outdoor living fitters are in the room when the decision gets made. They carry the same card the owners carry, with a kickback or beer for every referral that converts, and the tracking that lets you pay it.'], ['3 months']],
  ['Host a tasting', ['Turn owners into the sales force. They pour for about twenty friends at home, we supply the kit, the invitation and the mechanics, and they earn on anything sold. The referral runs at their table rather than in your inbox.'], ['6 months']],
  ['UGC and brand ambassador content', ['A content programme with your named ambassadors, Kurt, Troy, Mitch, Aden and Ash: the brief, the shoot plan, the release schedule, the rights. Ready to deploy within three months.'], ['3 months']],
]));

body.push(SUB('4. The Tap Room as a destination'));
body.push(P('Your priority four. Local business, functions and ticketed music. Settled on 18 September: the room is a destination, not a walk-in bar. Whether it reads as a showroom or an event space is still your call inside 30 days, and the programme below works under either.'));
body.push(activityTable([
  ['Oktoberfest and the keg system giveaway', ['The first dated event. Campaign, artwork, entry mechanics that feed the CRM, and the follow-up sequence that turns a thousand entries into system sales over the three-month buying cycle.'], ['30 days']],
  ['Competitions, twice a year', ['Each keg system giveaway moves about thirty systems. Your call is two a year, not three. We build the insider offer so it lands the moment someone enters, and repeat the Crafted Festival funnel: free taste and paddle, entry, automation.'], ['3 months, then twice yearly']],
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
body.push(P('The brand is not being rebuilt. It is being sharpened around one enemy, overpriced pubs, and one line, yours: every household in Australia deserves beer on tap. On 18 September you adopted the one addition we recommended, which is where the category sits. It changes who will partner with you and what the hardware has to look like.'));
body.push(activityTable([
  ['Key messaging by target market', ['Your 30-day item. One page per segment: what we say, what we prove, what we ask. Built on $2.55 a schooner against $12 at the pub.'], ['30 days']],
  ['Where the category sits', ['Adopted on 18 September. Home entertainment, not beer. Your line stays as the ambition; the brand idea underneath it is what the product does to an ordinary Saturday, which is turn a catch-up into the one people talk about. That puts the kegerator beside the outdoor kitchen, the high-end barbecue and the coffee machine, rather than beside the bar fridge. Christy owns the wording and leads the rewrite of key messaging on that basis.'], ['30 days']],
  ['Customer journey mapped', ['Your 30-day item. From first contact to first refill to reorder, with the CRM trigger at each step.'], ['30 days']],
  ['Proof assets', ['The Crafted award, the reviews, fits-any-system and no CO2, and the integrated units already selling, three to four plumbed-in systems with only the font showing and none of them on the website. Produced for the website, the venue, the tap decals and social. Owned already, barely used.'], ['3 months']],
  ['Designing for her', ['A product and design brief, not a campaign: the range, the RTD, the hydration and light story, and a system that sits in eyesight at home. Wellness influencer collaborations as the first proof.'], ['6 months']],
  ['The unit as an object worth owning', ['A design direction for the hardware and how it is presented, so it earns a place on the bench or in the outdoor kitchen. A Zip HydroTap sells at around $10,000 largely on how it looks. Runs alongside designing for her, and it is what gets a keg system into the outdoor living aisle instead of the appliance aisle.'], ['6 months']],
  ['Range and heroes', ['Support the cut to hero brews with the product marketing behind them: social proof cues at the point of sale, most popular, award winner, what to eat with it.'], ['6 months']],
  ['Campaign artwork', ['Four event flyers are built. Next: Oktoberfest, the switcher campaign, the referral programme, the ambassador content, and everything the calendar needs, in Tap That’s own format.'], ['Ongoing']],
]));

body.push(SUB('7. Governance'));
body.push(activityTable([
  ['Meeting rhythm', ['Your 30-day item, agreed on 18 September. A weekly 45 minutes with Harry and Justin, led by Christy; a monthly hour with both founders against the four numbers; and a review at each rung of your ladder. Ronnie locks the standing day.'], ['30 days, ongoing']],
  ['Who does what', ['The responsibility matrix on the Activation sheet, agreed and dated, so nothing sits with everybody. It is a draft until you and Chris return the split of what Jewell owns and what Harry and Justin keep.'], ['30 days']],
  ['Reviews on your ladder', ['Mid-October, mid-December, March 2027, September 2027. Every review asks first whether active refillers moved.'], ['As dated']],
]));

body.push(H('The First 30 Days'));
body.push(P('Your own 30-day list is the first sprint. We work it with you rather than around you.'));
const s1 = 'jp-num-1';
body.push(numbered([b('The shape decision, finished. '), run('Settled in principle on 18 September: the room is an events and local business venue. What is left is whether it reads as a showroom or an event space. Your call, and everything below works under either.')], s1));
body.push(numbered([b('Residential versus commercial. '), run('Where the energy goes. The refill data can answer this in a week once the CRM can be read.')], s1));
body.push(numbered([b('Key messaging and the customer journey. '), run('Delivered by us, signed by you.')], s1));
body.push(numbered([b('KPIs and the meeting rhythm. '), run('Four numbers, one definition of active refiller, one weekly and one monthly meeting.')], s1));
body.push(numbered([b('The Jewell split. '), run('This proposal is what Jewell owns. You and Chris mark it up: what stays with Harry and Justin, what waits for the hire. Agreed at the first weekly check-in.')], s1));
body.push(numbered([b('Ambassadors named, Oktoberfest run. '), run('The giveaway mechanics feed the CRM from day one.')], s1));
body.push(numbered([b('Settle $2.55. '), run('One per-schooner figure on the live ad and on every piece of collateral, and the other sets of maths retired.')], s1));
body.push(numbered([b('The 250 date. '), run('March 2027, or Christmas 2026 if you take Christy\u2019s date.')], s1));

body.push(H('Timeline, on Your Ladder'));
body.push(twoCol([
  ['Horizon', ['What is true at the end of it']],
  ['30 days – mid-October', ['Showroom or event space decided, and the Jewell split agreed. Messaging and journey signed, on the home entertainment position. KPIs, definitions and the weekly rhythm set. Oktoberfest run, giveaway entries in the CRM. $2.55 on the ad. The 250 date chosen.']],
  ['3 months – mid-December', ['Website and SEM live. GoTab and Fishbowl connected, CRM triggers replacing the 90-day SMS. Lease-to-buy and delivery launched. Harvey Norman and Kegland conversations open. Referral programme and Bring a Mate live, with trades carrying cards. Ambassador content deploying. Wholesale pipeline in the CRM. Next hire decided.']],
  ['6 months – March 2027', ['250 active keg refillers, or December if you take the Christmas date. Wedding and functions programme selling. Membership redesigned. Designing-for-her and the hardware-as-object briefs in market. Outdoor kitchen and host-a-tasting pilots running. Career pathways for Chris and Harry defined.']],
  ['1 year – September 2027', ['Referrals, JVPs and online driving most system sales. Replicable events calendar running. Cashflow positive, Justin on a wage.']],
]));
body.push(Note('The longer horizons on your plan, 1,000 refillers and proprietary system supply at three years, expansion and a production facility at five, an exit at ten to twelve, are on the summary sheet. This proposal covers the first year of the climb.'));

body.push(H('Ways of Working'));
body.push(bullet([b('Christy runs it. '), run('Christy Kilmartin leads the engagement for Jewell Projects: strategy, direction, and the call on what gets built next. Your first call on anything.')]));
body.push(bullet([b('Harry executes. '), run('Harry is the operator inside Tap That. Everything we design is built to be run from that seat, and the day-to-day sits with him.')]));
body.push(bullet([b('Weekly with Harry and Justin. '), run('Forty-five minutes, led by Christy: progress, blockers, what we need next. Both of you in the room, so direction and execution do not drift apart between meetings. Ronnie locks the standing day; you have said Thursday or Friday works, and we would prefer earlier in the week.')]));
body.push(bullet([b('Monthly against the numbers. '), run('One hour with both founders on the four numbers. Decisions taken in the room and recorded.')]));
body.push(bullet([b('Reviews on your ladder. '), run('Mid-October, mid-December, March, September. A written review at each, and a stop-or-continue conversation at each.')]));
body.push(bullet([b('One source of truth. '), run('Everything lives in the shared engagement folder and on the plan on a page. Nothing important travels only by text.')]));
body.push(bullet([b('Sign-off. '), run('One named person on your side, our suggestion is Justin with Chris consulted on brand and product, approves messaging, offers and anything that goes to market.')]));

body.push(H('What We Need From You'));
body.push(twoCol([
  ['Input', ['Why, and when']],
  ['Showroom or event space', ['The last piece of the shape decision. Everything on the Business sheet follows from it. Within 30 days.']],
  ['One definition of active keg refiller', ['Before the first monthly report, or the number gets argued about instead of acted on.']],
  ['$2.55 as the per-schooner figure', ['Confirmed as the number on the live ad, and the other maths retired. Within 30 days.']],
  ['GoTab and Fishbowl timeline', ['It sequences the CRM build. Before the three-month sprint starts.']],
  ['Introductions', ['Kurt, Troy, Mitch, Aden and Ash; Mark’s venues; the Kegland and Benchy contacts. As the workstreams open.']],
  ['The 250 date', ['March 2027, or Christmas 2026 if you take Christy\u2019s date. It changes the shape of the first three months. Before this is signed.']],
  ['The Jewell split', ['Your mark-up of the workstreams above: what Jewell owns, what Harry and Justin keep. At the first weekly check-in.']],
  ['A named sign-off holder', ['One signature that closes each checkpoint. At kick-off.']],
]));

body.push(H('Investment and Terms'));
body.push(P('Two options. Both run on the same plan and the same rhythm. All figures are Australian dollars, exclude GST, and include project management and administration. Ad spend is paid by Tap That directly to Meta and Google.'));
body.push(twoCol([
  ['The basis', ['']],
  ['Discover and Design, already delivered', ['The Discovery pack, the Pivot, the plan on a page and four event flyers. Rack value $20,000. Charged at $4,995, payable on acceptance of either option.']],
  ['The rates behind every figure below', ['Client Director $1,500 a day. Client Manager $1,250 a day.']],
], [3000, 6026]));
body.push(SUB('Option A – the ninety-day sprint'));
body.push(twoCol([
  ['Line', ['Fee']],
  ['Foundation builds', ['Website rebuild with the buy path and proof pages; SEM set-up; trigger-based CRM with segments; three campaign landing pages. $9,250']],
  ['Programme design', ['Switcher offer and the partner approach; referral programme and Bring a Mate; wholesale structure, pipeline and hire brief; key messaging and the customer journey; Oktoberfest and the giveaway campaign. $8,500']],
  ['Running the sprint, three months', ['SEM and Meta management; JVP, partner and wholesale outreach; content and campaign artwork; the weekly and monthly rhythm and the report. $3,250 a month, $9,750']],
  ['Option A total', [[b('$12,500 + GST'), run('  \u00b7  normally $27,500')]]],
], [3000, 6026]));
body.push(P('Payment: 50% on acceptance, 50% at the mid-December review. Stop or continue at that review. The line fees above are the standard rate and sum to $27,500; the discount is applied to the total.'));
body.push(SUB('Option B – twelve months'));
body.push(twoCol([
  ['Line', ['Fee']],
  ['Everything in Option A', ['Delivered in the first three months. Included.']],
  ['Months four to twelve', ['The weddings and functions programme; membership redesign; the designing-for-her brief; range and hero product marketing; club and venue offers; the events calendar; SEM, outreach, content and artwork continuing; the reviews at March and September. Included.']],
  ['Option B total', [[b('$2,500 a month + GST'), run('  \u00b7  normally $5,500  \u00b7  $30,000 over twelve months')]]],
], [3000, 6026]));
body.push(P('Payment: monthly in advance. Minimum three months, then stop at any review with a month’s notice.'));
body.push(SUB('What it has to earn'));
body.push(P([run('Option A is $4,167 a month for three months with no commitment beyond it. Option B is $2,500 a month with the builds spread across the year. An active refill customer is worth about $2,400 a year at roughly $200 a month. '), b('Option B pays for itself at thirteen additional active refillers held for a year.'), run(' Your own six-month target adds about 145.')]));
body.push(twoCol([
  ['Not included', ['']],
  ['Media spend', ['Billed directly by Meta and Google. Management of spend above $5,000 a month at 10% of the excess.']],
  ['Photography and video', ['$1,250 a day, quoted per shoot.']],
  ['The Urban Legends booking widget', ['Scoped separately once the operator agrees to carry it.']],
  ['Third-party software and print', ['GoTab, Fishbowl, any booking tool licence, and print runs.']],
], [3000, 6026]));
body.push(Note('The struck-through figures are the standard rate, built on what Jewell Projects charges today: Client Director $1,500 a day, Client Manager $1,250 a day. The discounted rate is what we are putting on the table for this engagement, and it holds for its term.'));

body.push(H('Decisions This Proposal Needs'));
const s2 = 'jp-num-2';
body.push(numbered('Which option, A or B.', s2));
body.push(numbered('Who signs for Tap That Brewery.', s2));
body.push(numbered('The 250 date: March 2027, or Christmas 2026.', s2));
body.push(numbered('A start date. We propose the week of 28 September, which puts Oktoberfest on 1 October inside the first week and closes the 30-day sprint before the end of October.', s2));

body.push(H('Sign-off'));
body.push(twoCol([
  ['Accepted for Tap That Brewery', ['Name: ____________________   Signature: ____________________   Date: __________']],
  ['For Jewell Projects', ['Name: Clent Jewell   Signature: ____________________   Date: __________']],
], [3000, 6026], false));

body.push(H('Appendix A – What Is Already Delivered'));
body.push(P('All of the following exist, are in the shared folder, and are the basis for this proposal.'));
body.push(bullet([b('The Discovery pack. '), run('Audience, competitors, offers, economics and the six priority problems, with the census worked through it.')]));
body.push(bullet([b('The Pivot. '), run('Eighteen slides presented on 15 September: six findings, ten moves, the collateral, the small fixes and the scope.')]));
body.push(bullet([b('The plan on a page. '), run('Five A3 sheets, v03, reworked on 23 September around your own plan and the 18 September catch-up: the summary, business, brand, sales and marketing, activation. Editable PowerPoint and print master.')]));
body.push(bullet([b('Four event flyers. '), run('Weddings, bucks and hens, work functions, tours and tastings. Print-ready A4 in Tap That’s own format, in two image sets.')]));
body.push(bullet([b('The catch-up transcripts. '), run('Verbatim, filed, and the reference where anything above is in question.')]));

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
