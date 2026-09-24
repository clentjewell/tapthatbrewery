"""
Proposal v03 for Tap That Brewery as a Jewell Projects presentation.

The docx is the contract and the deck is how it gets walked through, so the
two must not drift. Every figure on a money slide is read out of the proposal
markdown rather than typed here; build_proposal.js does the same for the docx.
Slide copy is condensed by hand, because a table cell is not a paragraph.

House rules come from the jp-brand-presentation skill, Brand Book Edition 02:
Cream ground, Jewell Black type, Signal Blue on the decision slide only, no
bullets on a content slide, no icons, no decoration.

    python3 build_proposal_deck.py <out.pptx>
"""

import os
import re
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "02__Proposal__Tap-That-Brewery__Client__Draft__v03.md")

# ---- locked palette, Edition 02 ---------------------------------------
JEWELL_BLACK = RGBColor(0x11, 0x11, 0x11)
CALM_GREY = RGBColor(0xED, 0xEB, 0xEA)
CREAM = RGBColor(0xFA, 0xF8, 0xF4)
SIGNAL_BLUE = RGBColor(0x2D, 0x5B, 0xFF)
GREY_TEXT = RGBColor(0x66, 0x66, 0x66)
RULE = RGBColor(0xD4, 0xD2, 0xD0)

POPPINS = "Poppins"
SLIDE_W, SLIDE_H = Inches(13.333), Inches(7.5)
MARGIN = Inches(1.0)
COL_W = Inches(11.333)          # SLIDE_W - 2 * MARGIN


# ---- helpers ----------------------------------------------------------

def set_background(slide, rgb):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb


def add_textbox(slide, left, top, width, height, text, size_pt=14,
                bold=False, color=JEWELL_BLACK, uppercase=False,
                align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
                line_spacing=1.5, tracking=None, space_after=0):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, "margin_" + side, 0)
    tf.vertical_anchor = anchor

    for i, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        if space_after:
            p.space_after = Pt(space_after)
        run = p.add_run()
        run.text = line.upper() if uppercase else line
        f = run.font
        f.name = POPPINS
        f.size = Pt(size_pt)
        f.bold = bold
        f.color.rgb = color
        if tracking is not None:
            run._r.get_or_add_rPr().set("spc", str(tracking))
    return box


def add_hairline(slide, left, top, width, color=RULE, weight_pt=0.75):
    line = slide.shapes.add_connector(1, left, top, left + width, top)
    line.line.color.rgb = color
    line.line.width = Pt(weight_pt)
    return line


_FONTS = {
    False: "/usr/share/fonts/truetype/poppins/Poppins-400.ttf",
    True: "/usr/share/fonts/truetype/poppins/Poppins-600.ttf",
}
_font_cache = {}


def _font(size_pt, bold):
    key = (size_pt, bold)
    if key not in _font_cache:
        from PIL import ImageFont
        try:
            # Measure at 10x and divide, so rounding in PIL's integer sizing
            # does not accumulate at the small point sizes these tables use.
            _font_cache[key] = ImageFont.truetype(_FONTS[bold], int(size_pt * 10))
        except OSError:
            sys.exit(
                "Poppins is not installed, so row heights cannot be measured "
                "and the PDF would clip its own tables. Install it first:\n"
                "  mkdir -p /usr/share/fonts/truetype/poppins\n"
                "  # fetch Poppins 400 and 600 from Google Fonts into that "
                "directory as Poppins-400.ttf and Poppins-600.ttf\n"
                "  fc-cache -f")
    return _font_cache[key]


def wrapped_lines(text, width_pt, size_pt, bold=False):
    """Line count for text laid out in a column width_pt points wide."""
    font = _font(size_pt, bold)
    limit = width_pt * 10
    total = 0
    for para in text.split("\n"):
        words, line, n = para.split(), "", 1
        for w in words:
            trial = w if not line else line + " " + w
            if font.getlength(trial) <= limit or not line:
                line = trial
            else:
                n += 1
                line = w
        total += n
    return total


def _cell_border(cell, edge, color, weight_pt):
    """python-pptx exposes no border API, so write the a:ln* element."""
    tcPr = cell._tc.get_or_add_tcPr()
    tag = qn("a:ln" + edge)
    for old in tcPr.findall(tag):
        tcPr.remove(old)
    ln = tcPr.makeelement(tag, {
        "w": str(int(weight_pt * 12700)), "cap": "flat",
        "cmpd": "sng", "algn": "ctr",
    })
    fill = ln.makeelement(qn("a:solidFill"), {})
    clr = ln.makeelement(qn("a:srgbClr"), {"val": "%02X%02X%02X" % (color[0], color[1], color[2])})
    fill.append(clr)
    ln.append(fill)
    # Order matters in the schema: lnL, lnR, lnT, lnB come before any fill.
    tcPr.insert(0, ln)


def add_table(slide, top, headers, rows, col_fractions, row_h=Inches(0.34),
              head_h=Inches(0.3), size_pt=11):
    """A table carrying hairline rules and nothing else. No fills, no style."""
    n_rows, n_cols = len(rows) + 1, len(headers)
    shape = slide.shapes.add_table(n_rows, n_cols, MARGIN, top, COL_W, head_h + row_h * len(rows))
    tbl = shape.table

    # Strip PowerPoint's default banded style.
    tblPr = tbl._tbl.tblPr
    tblPr.set("firstRow", "0")
    tblPr.set("bandRow", "0")
    for styleId in tblPr.findall(qn("a:tableStyleId")):
        tblPr.remove(styleId)
    el = tblPr.makeelement(qn("a:tableStyleId"), {})
    el.text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"   # No Style, No Grid
    tblPr.append(el)

    total = sum(col_fractions)
    widths_in = [11.333 * frac / total for frac in col_fractions]
    for i, w in enumerate(widths_in):
        tbl.columns[i].width = Inches(w)
    tbl.rows[0].height = head_h

    # A rendered line is not size_pt * line_spacing. Poppins carries a natural
    # line box of about 1.22em (hhea 1050/-350 on a 1000 upem), and proportional
    # line spacing multiplies that, so 11pt at 1.34 sets an 18pt line, not a
    # 14.7pt one. Sizing rows off the wrong number is what clipped Option B.
    LINE_PT = size_pt * 1.22 * 1.34
    PAD_PT = 8.0                       # cell top and bottom margin, plus slack
    RIGHT_MARGIN_PT = 0.14 * 72
    for r in range(1, n_rows):
        lines = 1
        for c, w in enumerate(widths_in):
            usable = w * 72 - RIGHT_MARGIN_PT
            lines = max(lines, wrapped_lines(rows[r - 1][c], usable, size_pt,
                                             bold=(c == 0)))
        need = Inches((lines * LINE_PT + PAD_PT) / 72.0)
        tbl.rows[r].height = max(row_h, need)

    for r in range(n_rows):
        for c in range(n_cols):
            cell = tbl.cell(r, c)
            cell.fill.background()
            cell.margin_left = Inches(0)
            cell.margin_right = Inches(0.14)
            cell.margin_top = Inches(0.04)
            cell.margin_bottom = Inches(0.06)
            cell.vertical_anchor = MSO_ANCHOR.TOP
            for edge in ("L", "R", "T"):
                _cell_border(cell, edge, CREAM, 0.0)
            _cell_border(cell, "B", RULE, 0.75)

            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.line_spacing = 1.34
            run = p.add_run()
            is_head = r == 0
            run.text = headers[c].upper() if is_head else rows[r - 1][c]
            f = run.font
            f.name = POPPINS
            f.size = Pt(9 if is_head else size_pt)
            f.bold = False
            f.color.rgb = GREY_TEXT if is_head else JEWELL_BLACK
            if is_head:
                run._r.get_or_add_rPr().set("spc", "200")
            elif c == 0:
                f.bold = True
    return tbl


def footer(slide, text):
    add_textbox(slide, MARGIN, SLIDE_H - Inches(0.62), COL_W, Inches(0.3),
                text, size_pt=9, color=GREY_TEXT, line_spacing=1.0)


# ---- slide types ------------------------------------------------------

def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def title_slide(prs, topbar, title, subtitle=None, date_line=None):
    s = blank(prs)
    set_background(s, CREAM)
    add_textbox(s, MARGIN, Inches(0.5), COL_W, Inches(0.3), topbar,
                size_pt=9, uppercase=True, tracking=200, line_spacing=1.0)
    add_textbox(s, MARGIN, SLIDE_H - MARGIN - Inches(3.1), COL_W, Inches(2.6),
                title, size_pt=72, bold=True, line_spacing=1.02,
                anchor=MSO_ANCHOR.BOTTOM)
    if subtitle:
        add_textbox(s, MARGIN, SLIDE_H - Inches(1.15), COL_W, Inches(0.5),
                    subtitle, size_pt=20, line_spacing=1.2)
    if date_line:
        add_textbox(s, Inches(8.0), SLIDE_H - Inches(0.62), Inches(4.333),
                    Inches(0.3), date_line, size_pt=11, color=GREY_TEXT,
                    align=PP_ALIGN.RIGHT, line_spacing=1.0)
    return s


def content_slide(prs, eyebrow, headline, body=None, foot=None):
    s = blank(prs)
    set_background(s, CREAM)
    add_textbox(s, MARGIN, MARGIN, COL_W, Inches(0.3), eyebrow,
                size_pt=9, uppercase=True, tracking=200, line_spacing=1.0)
    add_textbox(s, MARGIN, Inches(1.85), COL_W, Inches(2.3), headline,
                size_pt=42, line_spacing=1.12)
    if body:
        add_textbox(s, MARGIN, Inches(4.5), Inches(8.6), Inches(2.2), body,
                    size_pt=14, line_spacing=1.5, space_after=8)
    if foot:
        footer(s, foot)
    return s


def table_slide(prs, eyebrow, headline, headers, rows, col_fractions,
                lead=None, foot=None, row_h=Inches(0.34), size_pt=11):
    s = blank(prs)
    set_background(s, CREAM)
    add_textbox(s, MARGIN, MARGIN, COL_W, Inches(0.3), eyebrow,
                size_pt=9, uppercase=True, tracking=200, line_spacing=1.0)
    add_textbox(s, MARGIN, Inches(1.5), COL_W, Inches(0.7), headline,
                size_pt=28, line_spacing=1.12)
    top = Inches(2.4)
    if lead:
        add_textbox(s, MARGIN, Inches(2.28), Inches(9.6), Inches(0.6), lead,
                    size_pt=13, color=GREY_TEXT, line_spacing=1.4)
        top = Inches(3.15)
    add_table(s, top, headers, rows, col_fractions, row_h=row_h, size_pt=size_pt)
    if foot:
        footer(s, foot)
    return s


def divider_slide(prs, part, title, strapline=None):
    s = blank(prs)
    set_background(s, JEWELL_BLACK)
    add_textbox(s, MARGIN, MARGIN, COL_W, Inches(0.3), part,
                size_pt=14, color=CREAM, uppercase=True, tracking=200,
                line_spacing=1.0)
    add_textbox(s, MARGIN, Inches(2.4), COL_W, Inches(2.6), title,
                size_pt=96, color=CREAM, line_spacing=1.0,
                anchor=MSO_ANCHOR.MIDDLE)
    if strapline:
        add_textbox(s, MARGIN, Inches(5.7), COL_W, Inches(0.5), strapline,
                    size_pt=16, color=CREAM, line_spacing=1.3)
    return s


def gate_slide(prs, eyebrow, decision, body, rows, left_sign, right_sign):
    s = blank(prs)
    set_background(s, SIGNAL_BLUE)
    add_textbox(s, MARGIN, MARGIN, COL_W, Inches(0.3), eyebrow,
                size_pt=9, color=CREAM, uppercase=True, tracking=200,
                line_spacing=1.0)
    add_textbox(s, MARGIN, Inches(1.7), COL_W, Inches(1.0), decision,
                size_pt=32, bold=True, color=CREAM, line_spacing=1.2)
    add_textbox(s, MARGIN, Inches(2.75), Inches(9.6), Inches(0.8), body,
                size_pt=14, color=CREAM, line_spacing=1.5)
    y = Inches(3.75)
    for n, text in rows:
        add_textbox(s, MARGIN, y, Inches(0.5), Inches(0.4), n,
                    size_pt=14, bold=True, color=CREAM, line_spacing=1.3)
        add_textbox(s, Inches(1.5), y, Inches(10.3), Inches(0.4), text,
                    size_pt=14, color=CREAM, line_spacing=1.3)
        y += Inches(0.52)
    add_hairline(s, MARGIN, Inches(6.55), COL_W, color=CREAM, weight_pt=0.5)
    add_textbox(s, MARGIN, Inches(6.72), Inches(5.6), Inches(0.3), left_sign,
                size_pt=11, color=CREAM, line_spacing=1.0)
    add_textbox(s, Inches(7.2), Inches(6.72), Inches(5.133), Inches(0.3),
                right_sign, size_pt=11, color=CREAM, align=PP_ALIGN.RIGHT,
                line_spacing=1.0)
    return s


def closer_slide(prs, action, owner):
    s = blank(prs)
    set_background(s, CREAM)
    add_textbox(s, MARGIN, Inches(2.2), COL_W, Inches(2.2), "Next.",
                size_pt=120, bold=True, line_spacing=1.0)
    add_textbox(s, MARGIN, Inches(4.8), COL_W, Inches(0.4), action,
                size_pt=14, line_spacing=1.4)
    add_textbox(s, MARGIN, Inches(5.25), COL_W, Inches(0.4), owner,
                size_pt=14, line_spacing=1.4)
    return s


# ---- figures, read out of the proposal rather than retyped ------------

def money():
    md = open(SRC, encoding="utf-8").read()

    def grab(pattern, label):
        m = re.search(pattern, md)
        if not m:
            raise SystemExit("proposal figure not found: " + label)
        return m.group(1)

    f = {
        "a_total": grab(r"\*\*Option A total\*\* \| \*\*\$([\d,]+) \+ GST", "Option A"),
        "a_rack": grab(r"Option A total.*normally \$([\d,]+)", "Option A rack"),
        "b_total": grab(r"\*\*Option B total\*\* \| \*\*\$([\d,]+) a month", "Option B"),
        "b_rack": grab(r"Option B total.*normally \$([\d,]+)", "Option B rack"),
        "b_year": grab(r"Option B total.*?· \$([\d,]+) over twelve months", "Option B year"),
        "gate": grab(r"Charged at \*\*\$([\d,]+)\*\*", "Discover and Design"),
        "rack": grab(r"Rack value \$([\d,]+)", "rack value"),
        "cd": grab(r"Client Director \$([\d,]+) a day", "Client Director"),
        "cm": grab(r"Client Manager \$([\d,]+) a day", "Client Manager"),
        "found": grab(r"three campaign landing pages\. \| \$([\d,]+)", "foundation"),
        "prog": grab(r"Oktoberfest and the giveaway campaign\. \| \$([\d,]+)", "programme"),
        "run_mo": grab(r"the report\. \| \$([\d,]+) a month", "run monthly"),
        "run_tot": grab(r"the report\. \| \$[\d,]+ a month, \$([\d,]+)", "run total"),
    }
    return f


# ---- the deck ---------------------------------------------------------

def build(out_path):
    f = money()
    prs = Presentation()
    prs.slide_width, prs.slide_height = SLIDE_W, SLIDE_H

    title_slide(
        prs,
        "JP · TAP THAT BREWERY · PROPOSAL",
        "Executing the\nplan on a page.",
        "Marketing strategy and execution. Twelve months.",
        "v03 · 23 September 2026",
    )

    # ---- Part 01 -------------------------------------------------------
    divider_slide(prs, "Part 01", "Where you are.",
                  "The diagnosis, and what the catch-up settled.")

    content_slide(
        prs, "The diagnosis",
        "You do not have a strategy problem. You have an execution problem.",
        "Three weeks on, that still holds. The refill business reached 96 to 113 active "
        "customers without a marketing push. Meta ads are working and there is nowhere "
        "to send the traffic. The website, POS and CRM do not talk to each other, so "
        "every campaign underperforms before it launches.\n"
        "The constraint is hands, not ideas. We said that in August. Nothing since has "
        "changed it.",
    )

    table_slide(
        prs, "Where you start from", "Six numbers the plan runs on.",
        ["The number", "What it is"],
        [["96 to 113", "Active refill customers, reached with no marketing push"],
         ["56%", "Of them bought their system somewhere else and switched anyway"],
         ["250", "Active refillers at six months. March 2027, or Christmas"],
         ["1,000", "Active refillers by year three, across three regions"],
         ["$2.55 vs $12+", "A schooner at home against a schooner at the pub"],
         ["1 : 10", "One wholesale account is worth about ten households"]],
        [0.22, 0.78],
        foot="A system that is not refilling is worth nothing. Every activity in this "
             "proposal is tested against the refiller number.",
    )

    content_slide(
        prs, "Settled 18 September · one of three",
        "The room is a destination, not a walk-in bar.",
        "The Tap Room makes money on events and functions and loses it on walk-in trade. "
        "You settled that in principle: it is an events and local business venue. Your own "
        "words, that Oktoberfest is a sugar hit and you would take week-on-week revenue "
        "over it, are the clearest statement of strategy in three weeks of conversation.\n"
        "What is left is whether the room reads as a showroom or an event space. That is "
        "your call inside 30 days, and everything here works under either.",
    )

    content_slide(
        prs, "Settled 18 September · two of three",
        "Home entertainment, not beer.",
        "Every household deserves beer on tap is your line and it stays as the ambition. "
        "The brand idea underneath it is what the product does to an ordinary Saturday, "
        "which is turn a catch-up into the one people talk about.\n"
        "That puts the kegerator beside the outdoor kitchen, the high-end barbecue and the "
        "coffee machine, rather than beside the bar fridge. It changes who will partner "
        "with you and what the hardware has to look like. Christy owns the wording.",
    )

    content_slide(
        prs, "The position",
        "Tap That is not in the beer business.",
        "It is in home entertainment, and in the business of bringing people together. The "
        "product does not just put beer in a glass at home. It turns an ordinary get-together "
        "into an occasion worth hosting.\n"
        "Every household deserves beer on tap stays as the ambition. It describes what you "
        "want to be true rather than why anyone buys. The brand idea sits underneath it, and "
        "it is the one that sells.",
    )

    content_slide(
        prs, "The position · what it changes",
        "A design brief as much as a marketing one.",
        "If the category is home entertainment, a keg system belongs beside the outdoor "
        "kitchen, the high-end barbecue and the coffee machine, rather than beside the bar "
        "fridge.\n"
        "The systems on the market today read as appliances. Stand one next to a premium "
        "outdoor kitchen and it looks like equipment rather than something you chose. The "
        "comparison worth studying is the premium filtered-water tap: people pay for it "
        "because it looks right on the bench and they show it to visitors.",
    )

    content_slide(
        prs, "The position · the line",
        "The best night in, on tap.",
        "Chosen on 24 September from three drafts. It leans on occasion and hosting, which is "
        "the closest of the three to the idea underneath it and the easiest to build a "
        "campaign around.\n"
        "The two it beat name arguments the work still has to carry: social proof and the "
        "be-the-envy-of-your-friends register, and the beer quality argument for the people "
        "who buy on taste. Christy works the line into key messaging inside 30 days.",
    )

    content_slide(
        prs, "Settled 18 September · three of three",
        "250 refillers is also the money number.",
        "Break-even is about $50,000 a month against a current run rate of $35,000 to "
        "$45,000, and one month has already hit it. You confirmed that 250 active "
        "refillers clears it. The six-month number and the money number are the same "
        "number.\n"
        "Which opens the one question this proposal cannot answer for you. Christy has put "
        "250 by Christmas on the table given the outdoor entertaining season. March 2027 "
        "or Christmas 2026 should be settled before this is signed.",
    )

    # ---- Part 02 -------------------------------------------------------
    divider_slide(prs, "Part 02", "The work.",
                  "Seven workstreams, on your horizons.")

    table_slide(
        prs, "At a glance", "Seven workstreams. The first carries the other six.",
        ["", "Workstream", "The move"],
        [["01", "Connect the system", "Nothing compounds until the website, POS and CRM talk"],
         ["02", "Switch existing owners", "Your number one. They have already bought the hardware"],
         ["03", "Referrals, JVPs, ambassadors", "18% of sales already, on a programme nobody can hold"],
         ["04", "The Tap Room as a destination", "Events, functions, ticketed music and local business"],
         ["05", "Wholesale as a function", "Demand exists. Follow-up does not"],
         ["06", "Brand, range and proof", "Sharpened, not rebuilt. Proof you own and barely use"],
         ["07", "Governance", "Four numbers, one page, one rhythm"]],
        [0.05, 0.28, 0.67],
        foot="Horizons are your own: 30 days to mid-October, three months to mid-December, "
             "six months to March 2027, one year to September 2027.",
    )

    table_slide(
        prs, "Workstream 01", "Connect the system.",
        ["Activity", "What we deliver", "When"],
        [["Website upgrade", "A CMS you run yourself, wired to GoTab, Fishbowl, the Pixel and the CRM. Integrations proven before launch, not promised", "3 months"],
         ["SEM", "Search on the category nobody on the Gold Coast owns: beer at home, keg refills, keg systems", "3 months"],
         ["GoTab and Fishbowl", "Every sale writes back to the customer record. We ready the CRM and the site so nothing is built twice", "3 months"],
         ["Trigger-based CRM", "Consumption-timed reminders replace the blanket 90-day SMS. Four segments, one re-engagement flow", "3 months"],
         ["Meta Ads split", "Switcher, giveaway, destination and retargeting, with a landing page for each rather than a home page for all", "30 days"],
         ["One monthly report", "Four numbers on one page. Active refiller defined once, before the first report", "30 days"]],
        [0.20, 0.66, 0.14],
        lead="Spending more on ads before this is fixed buys traffic the business cannot catch.",
    )

    table_slide(
        prs, "Workstream 02", "Switch the owners who already have a system.",
        ["Activity", "What we deliver", "When"],
        [["National retail, to explore", "Harvey Norman, JB Hi-Fi and The Good Guys. A gift-with-purchase or first keg free at franchisee level, plus the buyer database", "3 months"],
         ["Kegland and Benchy", "Buy or partner for the owner databases. A refill voucher in the box", "3 months"],
         ["Switcher campaign", "The lead priority. One offer, one page: you already have the hardware, we are the beer, first keg on us", "3 months"],
         ["Switcher offer conditions", "Compatibility check, one offer per household or venue, proof of ownership, liquor promotion wording, Meta targeting 18 and over", "3 months"],
         ["Lease-to-buy and delivery", "Your launch items. Offer page, CRM flow and launch creative for both", "3 months"],
         ["Outdoor kitchen specification", "A keg-and-tap unit as a standard inclusion. Visuals and a demand test before anything is manufactured", "6 months"]],
        [0.22, 0.64, 0.14],
        lead="The lead priority. They have bought the hardware and overcome every objection already.",
    )

    table_slide(
        prs, "Workstream 03", "Referrals, JVPs and ambassadors.",
        ["Activity", "What we deliver", "When"],
        [["Referral programme", "Tokens do not travel. A reward worth passing on does. Rebuilt around a free keg and a QR card an owner hands to a mate", "3 months"],
         ["Internal referral programme", "The same mechanic pointed at keg system sales, for the team and for existing customers. Tracked so it can be paid", "3 months"],
         ["JVPs and partners", "The list, offer, outreach and follow-up from the CRM. Mark's venues, Never Quit and the tour operators", "3 months"],
         ["Trades as a referral force", "Plumbers and kitchen installers carry the same card, with a kickback and the tracking that lets you pay it", "3 months"],
         ["UGC and ambassadors", "Kurt, Troy, Mitch, Aden and Ash. The brief, the shoot plan, the release schedule, the rights", "3 months"],
         ["Hosted tasting nights, to test", "A test, not a commitment. An owner hosts at home and earns a free keg or credit on anything sold", "6 months"],
         ["Service networks, to explore", "East coast technician routes already visiting thousands of businesses. A referral on a service visit", "6 months"]],
        [0.22, 0.64, 0.14],
    )

    table_slide(
        prs, "Workstream 04", "The Tap Room as a destination.",
        ["Activity", "What we deliver", "When"],
        [["Oktoberfest and the giveaway", "The first dated event. Campaign, artwork, entry mechanics into the CRM, and the follow-up that converts entries", "30 days"],
         ["Competitions, twice a year", "About thirty systems each. The insider offer lands the moment someone enters", "3 months"],
         ["Local business programme", "Lunch and after-work trade from the industrial area: offer, outreach list, collateral", "3 months"],
         ["Ticketed music and calendar", "A replicable calendar, with the promotion built once and reused", "3 months"],
         ["Tours and tastings", "Onto the circuit. The award and the bus parking are the reasons to stop here", "3 months"],
         ["Weddings and functions", "Hens and bucks through to reception supply. Mark's roughly 300 weddings a year", "6 months"],
         ["Party rental and membership", "A minimum keg guarantee replaces the $75 barrier. One membership, not two", "6 months"]],
        [0.22, 0.64, 0.14],
        lead="Settled: the room is a destination. Showroom or event space is still your call.",
    )

    table_slide(
        prs, "Workstream 05", "Wholesale as a function.",
        ["Activity", "What we deliver", "When"],
        [["Structure and KPIs", "Targets, pipeline stages and reporting in the CRM, so the function exists before the person does. A brief for the next hire", "3 months"],
         ["Venue outreach", "Event venues, niched venues and sporting clubs: the list, the offer, the twelve-touch sequence, run from the CRM", "3 months"],
         ["Club and venue offers", "Club-branded kegs, season minimum guarantees, and rigs that move from footy to cricket", "6 months"]],
        [0.20, 0.66, 0.14],
        lead="Bars have approached you and it has not converted. That is not a demand problem.",
    )

    table_slide(
        prs, "Workstream 06", "Brand, range and proof.",
        ["Activity", "What we deliver", "When"],
        [["Where the category sits", "Settled: the best night in, on tap. Christy works it into key messaging and into every brief", "30 days"],
         ["Key messaging by market", "One page per segment: what we say, what we prove, what we ask", "30 days"],
         ["Customer journey mapped", "First contact to first refill to reorder, with the CRM trigger at each step", "30 days"],
         ["Proof assets", "The Crafted award, the reviews, no CO2, and the integrated units already selling and nowhere on the site", "3 months"],
         ["Designing for her", "A product and design brief, not a campaign. The range, the RTD, the light and hydration story", "6 months"],
         ["The unit as an object", "A design direction for hardware that earns a place on the bench or in the outdoor kitchen", "6 months"],
         ["Range and heroes", "Social proof at the point of sale: most popular, award winner, what to eat with it", "6 months"],
         ["Campaign artwork", "Oktoberfest, the switcher, the referral programme, the ambassadors and the calendar", "Ongoing"]],
        [0.22, 0.64, 0.14],
        lead="Not rebuilt. Sharpened around one enemy, overpriced pubs, and your own line.",
    )

    table_slide(
        prs, "Workstream 07", "Governance.",
        ["Activity", "What we deliver", "When"],
        [["Meeting rhythm", "A weekly 45 minutes with Harry and Justin, led by Christy. A monthly hour with both founders against the four numbers", "30 days"],
         ["Who does what", "The responsibility matrix, agreed and dated. It stays a draft until you and Chris return the split", "30 days"],
         ["Reviews on your ladder", "Mid-October, mid-December, March 2027, September 2027. Every review asks first whether active refillers moved", "As dated"]],
        [0.20, 0.66, 0.14],
        lead="Agreed on 18 September. Ronnie locks the standing day.",
    )

    content_slide(
        prs, "Beyond this engagement",
        "Two of these are briefs, not the work itself.",
        "Designing for her, and the unit as an object worth owning. Writing a brief is a "
        "month. Acting on one is product and industrial design, with different people in it "
        "and a different order of spend.\n"
        "Both are scoped as a separate project in the Product Design Brief, on the delivery "
        "site at /product-design-brief. It runs alongside this engagement rather than inside "
        "it and is quoted separately. Nothing in it changes what is covered here or what it "
        "costs.",
        foot="The decision it needs first is whether Tap That makes hardware, specifies it "
             "with a manufacturer, or licences the design.",
    )

    # ---- Part 03 -------------------------------------------------------
    divider_slide(prs, "Part 03", "How it runs.",
                  "The first sprint, the ladder, and what we need from you.")

    table_slide(
        prs, "The first 30 days", "Your own 30-day list is the first sprint.",
        ["", "What closes"],
        [["01", "The shape decision, finished. Showroom or event space"],
         ["02", "Residential versus commercial. Where the energy goes"],
         ["03", "Key messaging and the customer journey. Delivered by us, signed by you"],
         ["04", "KPIs and the meeting rhythm. Four numbers, one definition of active refiller"],
         ["05", "The Jewell split. What we own, what Harry and Justin keep"],
         ["06", "Ambassadors named, Oktoberfest run, giveaway entries in the CRM"],
         ["07", "Settle $2.55 as the per-schooner figure on the live ad"],
         ["08", "The 250 date. March 2027 or Christmas 2026"]],
        [0.05, 0.95],
        foot="We work it with you rather than around you.",
    )

    table_slide(
        prs, "Timeline", "On your ladder, not ours.",
        ["Horizon", "What is true at the end of it"],
        [["30 days\nMid-October", "Showroom or event space decided, and the Jewell split agreed. Messaging and journey signed on the home entertainment position. KPIs and the weekly rhythm set. Oktoberfest run. The 250 date chosen"],
         ["3 months\nMid-December", "Website and SEM live. GoTab and Fishbowl connected, CRM triggers replacing the 90-day SMS. Lease-to-buy and delivery launched. Referral programme live, with trades carrying cards. Wholesale pipeline in the CRM. Next hire decided"],
         ["6 months\nMarch 2027", "250 active keg refillers, or December if you take the Christmas date. Weddings and functions selling. Membership redesigned. Designing-for-her and hardware-as-object briefs in market"],
         ["1 year\nSeptember 2027", "Referrals, JVPs and online driving most system sales. Replicable events calendar running. Cashflow positive, Justin on a wage"]],
        [0.17, 0.83],
        foot="Three years, five years and the exit sit on the summary sheet. This covers the "
             "first year of the climb.",
    )

    table_slide(
        prs, "Ways of working", "Who does what, and how often.",
        ["", "How it runs"],
        [["Christy runs it", "Christy Kilmartin leads the engagement: strategy, direction, and the call on what gets built next. Your first call on anything"],
         ["Harry executes", "Harry is the operator inside Tap That. Everything we design is built to be run from that seat"],
         ["Weekly", "Forty-five minutes with Harry and Justin, led by Christy. Ronnie locks the standing day"],
         ["Monthly", "One hour with both founders on the four numbers. Decisions taken in the room and recorded"],
         ["Reviews", "Mid-October, mid-December, March, September. A written review and a stop-or-continue conversation at each"],
         ["Sign-off", "One named person approves messaging, offers and anything that goes to market. We suggest Justin, with Chris consulted on brand and product"]],
        [0.18, 0.82],
    )

    table_slide(
        prs, "What we need from you", "Seven inputs, and when.",
        ["Input", "Why, and when"],
        [["Showroom or event space", "The last piece of the shape decision. Within 30 days"],
         ["The 250 date", "March 2027 or Christmas 2026. It changes the shape of the first three months. Before this is signed"],
         ["The Jewell split", "Your mark-up of the workstreams: what we own, what Harry and Justin keep. At the first weekly check-in"],
         ["One definition of active refiller", "Before the first monthly report, or the number gets argued about instead of acted on"],
         ["$2.55 as the per-schooner figure", "Confirmed on the live ad, and the other maths retired. Within 30 days"],
         ["GoTab and Fishbowl timeline", "It sequences the CRM build. Before the three-month sprint starts"],
         ["Introductions", "The ambassadors, Mark's venues, and the Kegland and Benchy contacts"]],
        [0.26, 0.74],
    )

    # ---- Part 04 -------------------------------------------------------
    divider_slide(prs, "Part 04", "Investment.",
                  "Two options, one plan, one rhythm.")

    table_slide(
        prs, "Option A", "The ninety-day sprint.",
        ["Line", "Fee"],
        [["Foundation builds. Website rebuild with the buy path and proof pages, SEM set-up, trigger-based CRM with segments, three campaign landing pages", "$" + f["found"]],
         ["Programme design. Switcher offer and partner approach, referral programme, wholesale structure and hire brief, key messaging and the customer journey, Oktoberfest", "$" + f["prog"]],
         ["Running the sprint, three months. SEM and Meta management, JVP and wholesale outreach, content and artwork, the rhythm and the report", "$%s a month, $%s" % (f["run_mo"], f["run_tot"])],
         ["Option A total", "$%s + GST\nnormally $%s" % (f["a_total"], f["a_rack"])]],
        [0.78, 0.22],
        lead="Discover and Design already delivered, rack value $%s, charged at $%s on acceptance of either option." % (f["rack"], f["gate"]),
        foot="50%% on acceptance, 50%% at the mid-December review. Stop or continue at that "
             "review. The line fees are the standard rate and sum to $%s; the discount is "
             "applied to the total." % f["a_rack"],
    )

    table_slide(
        prs, "Option B", "Twelve months.",
        ["Line", "Fee"],
        [["Everything in Option A, delivered in the first three months", "Included"],
         ["Months four to twelve. Weddings and functions, membership redesign, the designing-for-her brief, range and hero marketing, club and venue offers, the events calendar, SEM, outreach, content and artwork continuing, the reviews at March and September", "Included"],
         ["Option B total", "$%s a month + GST\nnormally $%s\n$%s over twelve months" % (f["b_total"], f["b_rack"], f["b_year"])]],
        [0.68, 0.32],
        lead="An active refill customer is worth about $2,400 a year. Option B pays for itself at thirteen additional refillers held for a year, and your own six-month target adds about 145.",
        foot="Monthly in advance. Minimum three months, then stop at any review with a "
             "month's notice. Rates behind every figure: Client Director $%s a day, "
             "Client Manager $%s a day." % (f["cd"], f["cm"]),
    )

    table_slide(
        prs, "Not included", "What sits outside the fee.",
        ["Item", "How it is handled"],
        [["Media spend", "Billed directly by Meta and Google. Management of spend above $5,000 a month at 10% of the excess"],
         ["Photography and video", "$1,250 a day, quoted per shoot"],
         ["The Urban Legends booking widget", "Scoped separately once the operator agrees to carry it"],
         ["Third-party software and print", "GoTab, Fishbowl, any booking tool licence, and print runs"]],
        [0.28, 0.72],
        foot="All figures are Australian dollars, exclude GST, and include project "
             "management and administration.",
    )

    # ---- decision ------------------------------------------------------
    gate_slide(
        prs,
        "Decision · proposal v03",
        "Four decisions, and we start.",
        "We propose the week of 28 September, which puts Oktoberfest on 1 October inside "
        "the first week and closes the 30-day sprint before the end of October.",
        [("01", "Which option, A or B."),
         ("02", "Who signs for Tap That Brewery."),
         ("03", "The 250 date: March 2027, or Christmas 2026."),
         ("04", "A start date.")],
        "Accepted for Tap That Brewery:",
        "For Jewell Projects: Clent Jewell",
    )

    closer_slide(
        prs,
        "Signed proposal back, and the first weekly check-in booked.",
        "Christy Kilmartin leads it · Clent Jewell · clent@jewellprojects.com",
    )

    prs.save(out_path)
    return prs


def check(prs):
    """Report any shape whose content will not fit the box it was given.

    Same guard as the A3 sheets: a deck that silently clips a line is worse
    than one that fails the build.
    """
    EMU = 914400.0
    bad = []
    for i, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            if shape.has_table:
                tbl = shape.table
                bottom = (shape.top + sum(r.height for r in tbl.rows)) / EMU
                if bottom > 6.86:                      # footer baseline
                    bad.append("slide %d: table runs to %.2fin, past the footer"
                               % (i, bottom))
                continue
            if not shape.has_text_frame or not shape.text_frame.text.strip():
                continue
            tf = shape.text_frame
            size_pt = tf.paragraphs[0].runs[0].font.size
            if size_pt is None:
                continue
            size_pt = size_pt.pt
            spacing = tf.paragraphs[0].line_spacing or 1.0
            bold = bool(tf.paragraphs[0].runs[0].font.bold)
            usable = shape.width / EMU * 72
            lines = sum(wrapped_lines(p.runs[0].text, usable, size_pt, bold)
                        for p in tf.paragraphs if p.runs)
            need = lines * size_pt * 1.22 * spacing / 72.0
            have = shape.height / EMU
            # Bottom-anchored boxes are sized deliberately loose; only flag a
            # box whose text genuinely exceeds it.
            if need > have + 0.02:
                bad.append("slide %d: text needs %.2fin in a %.2fin box (%r)"
                           % (i, need, have, tf.text[:44]))
            if shape.top / EMU + need > 7.34:
                bad.append("slide %d: text runs off the bottom (%r)"
                           % (i, tf.text[:44]))
    return bad


if __name__ == "__main__":
    out = sys.argv[1]
    p = build(out)
    problems = check(p)
    for line in problems:
        print("OVERFLOW " + line)
    print("every shape fits" if not problems else "%d overflow(s)" % len(problems))
    print("wrote %s (%d slides, %s bytes)"
          % (out, len(p.slides._sldIdLst), format(os.path.getsize(out), ",")))
