"""
Generate the delivery summary's open-items section from the output tracker.

The summary is hand-authored, and this section is the part of it that goes
stale fastest -- it was still listing the closed competitor question as a live
decision, and had never picked up the taproom and range decisions at all.

So the tracker is the source. This reads its open-items table, groups the live
items by what each one actually needs, and pairs each with client-facing copy
below. If the tracker carries an open item with no copy here, the build FAILS
rather than quietly dropping it from the page.

    python3 open_items.py            # print the section HTML
    python3 open_items.py --splice   # write it into delivery-summary.html
"""
import os, re, sys

WORD = {1:"One",2:"Two",3:"Three",4:"Four",5:"Five",6:"Six",7:"Seven",8:"Eight",9:"Nine",
        10:"Ten",11:"Eleven",12:"Twelve",13:"Thirteen",14:"Fourteen",15:"Fifteen",
        16:"Sixteen",17:"Seventeen",18:"Eighteen",19:"Nineteen",20:"Twenty",21:"Twenty-one"}
def word(n, cap=False):
    w = WORD.get(n, str(n))
    return w if cap else w.lower()

ROOT    = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
TRACKER = os.path.join(ROOT, "00 Admin/05 Timelines + Project Control/Maxxim-Output-Tracker.md")
SUMMARY = os.path.join(ROOT, "00 Admin/11 Final Outputs/delivery-summary.html")

# How each live item is grouped on the page. "decision" means nobody can
# research it for the founders; "data" arrives with a file, a date or access;
# "joint" is the one Jewell and the client settle together.
GROUP = {
    2: "decision", 10: "decision", 11: "decision", 13: "decision",
    14: "decision", 15: "decision", 20: "decision", 21: "decision",
    4: "data",  5: "data",  6: "data",  7: "data",  8: "data",
    9: "data", 12: "data", 16: "data", 17: "data", 18: "data",
    19: "joint",
}

# Client-facing copy, keyed by tracker item number.
COPY = {
2: ("Which membership price is the real one.",
    "Two posters are live in the venue right now: one says Keg Crew is $250 a year, the other $300 plus a $120 renewal, and the token bonuses differ too. This is the single most-cited blocker in the set &ndash; it gates the website&rsquo;s membership page, every brief and all collateral, and it is worth fixing this week regardless of anything else here. While we are at it: break-even on the $250 version is <b>8.33 refills, not the six being quoted to staff</b>.",
    "Blocks: CP1, the website, all collateral"),
10: ("Name, or mark.",
    "Every document in this set says &ldquo;Tap That Brewery&rdquo;. Your badge and your venue signage say &ldquo;Tap That &middot; Brewery &amp; Keghouse&rdquo;. That is either a short-name decision or a re-brand decision, and it changes collateral either way. It is not on the deck, and it should be.",
    "Blocks: brand guidelines, logo brief, all collateral"),
11: ("What counts as an &ldquo;active&rdquo; customer.",
    "Your own documents give three answers &ndash; 45 days in the Customer Success System, 75 days in the One-Page Plan, and &ldquo;2&ndash;3 months&rdquo; elsewhere. That is the difference between an active base of <b>96 and 113</b>, and every target, trigger day and report line keys off it. Our recommendation is 75 days, because your existing lifecycle comms already run on it and changing the clock while building the engine makes failure unattributable.",
    "Blocks: every metric, the CRM build, the OKRs"),
13: ("Sell more systems, or convert the 116 who bought elsewhere.",
    "Both are defensible. They are not the same plan, and they send the budget to different places. The evidence leans toward the switchers &ndash; they already own the hardware, they found you unaided, and they cost nothing to acquire &ndash; but the call is yours, and everything from the growth roadmap to the paid media split waits on it.",
    "Blocks: business plan, roadmap, activation plan"),
14: ("Which of your three plans is the live one.",
    "Scaling Up names 250 active customers as the Critical Number. The growth playbook names 15 kegerators a month. The vision document names installed kegerators. Three documents, three core metrics, three horizons &ndash; and they cannot all be the one the business is run against.",
    "Blocks: success definition, OKRs, CP2"),
15: ("Is cost on the table, or off it.",
    "Scaling Up says never compete on price. Your census ranks cost the <b>second-strongest purchase driver at 2.75</b>, a hair behind taste at 2.19. Those two positions cannot both hold. This decides whether the maths runs in the open feed or stays in retargeting, and it reaches the brand strategy, the messaging architecture and every ad. It is not on the deck, and it should be.",
    "Blocks: brand strategy, positioning, messaging, paid media"),
20: ("The taproom: destination, or drop-in.",
    "This is the zero-sum question at the centre of the business. The refill model is built on people <em>not</em> coming in, so every campaign that fills the taproom fills the half that loses money. Restricting hours and running it as a tasting and event venue is our recommendation. Keeping it open as a drop-in is a choice to keep paying for it &ndash; a defensible choice, but it should be made deliberately rather than by default.",
    "Blocks: activation plan, campaign calendar, events, PR"),
21: ("Twenty-seven taps, or about six.",
    "Cutting to roughly six core beers plus seasonals removes decision anxiety at the board and takes real cost out of ingredients, kegs, storage and refrigeration on stock that may never move. Keeping 27 is a range strategy, and it needs to be paid for knowingly. Either way this is a live cost driver, not a menu preference.",
    "Blocks: product review, pricing, business plan, collateral"),
4: ("GoTab and Fishbowl integration dates.",
    "The lifecycle automation does more for the numbers than anything else in the strategy &ndash; replacing the manual monthly SMS with triggers keyed to each customer&rsquo;s own reorder pattern. Every automation runbook now ships with a manual interim path so nothing waits on this, but the real build needs a date.",
    "Blocks: CRM automation, EDM sequences 4&ndash;6"),
5: ("P&amp;L detail, by unit.",
    "Partly closed &ndash; the unit economics came through with your documents: about $70 gross per keg, $300 margin on a kegerator, lifetime gross profit around $2,100 residential and $21,840 for a venue account. Still missing: the P&amp;L itself, COGS, CAC and margin. Those would turn the business plan from a structure into a plan with numbers in it.",
    "Blocks: business plan, budget setting"),
6: ("Three founder confirmations.",
    "The timeframe you want the 1,000 target inside &ndash; without a date, no plan can be paced against it. How long the taproom&rsquo;s loss stays acceptable while the decision above is being made. And whether the franchise ambition can be said out loud in PR.",
    "Blocks: OKRs, PR plan, CP2"),
7: ("Brand source files.",
    "Partly closed &ndash; we pulled the badge and the TT mark off your website and sampled the palette from them: green #14361D, gold #CE9A49, off-white #DFDFDF, all now in the guidelines. Still needed: true vector artwork, and the typeface names and licences. The guidelines cannot lock without them.",
    "Blocks: brand guidelines, logo lock"),
8: ("One beer name.",
    "The coolroom board reads &ldquo;Bong Water IPA&rdquo; in one place and &ldquo;Bone Water&rdquo; in another. Small, but it will end up in copy.",
    "Blocks: menu and collateral copy"),
9: ("Giveaway cadence.",
    "To fit both giveaway closes inside the plan year, the calendar compresses them to about three and a half months apart &ndash; tighter than your historical rhythm. Tell us if that is too tight and it moves.",
    "Blocks: campaign calendar, activation plan"),
12: ("Square access &ndash; the refill history.",
    "The census measures how much people <em>drink</em>. It cannot tell us how often they <em>refill</em>, how long the gap runs before they lapse, or what a customer is actually worth. That is all sitting in Square, and until we have it every revenue-per-customer figure in the set is a construction rather than a measurement.",
    "Blocks: any revenue-per-customer figure, CAC"),
16: ("Access to the ad account your last agency ran.",
    "We only learned it existed from your growth playbook. There is history in there &ndash; creative that worked, creative that didn&rsquo;t, real cost-per-result numbers &ndash; and it is the one asset in this engagement that comes free. Recovering it is the first step of the paid media runbook, before a dollar moves.",
    "Blocks: paid media launch, creative testing"),
17: ("What it actually costs to run this business.",
    "COGS, the true cost of carrying 27 taps, and the taproom&rsquo;s monthly loss. This is the largest gap in the set. Without these figures every business recommendation we have made is a judgement rather than a business case, and we would rather say so than dress it up.",
    "Blocks: the business plan, and every recommendation that assumes the business can fund it"),
18: ("A taproom conversion rate somebody has measured.",
    "The 20&ndash;30% figure is your own estimate and has never been observed. It is an extraordinary rate for a $975 purchase, and a good deal of the strategy was leaning on it. Every use of it in the set now carries that flag. Replacing it with a counted number changes what the taproom is worth.",
    "Blocks: funnel review, conversion pathway, activation plan, the case study"),
19: ("What a schooner at home actually costs.",
    "Three sets of maths are in circulation and they cannot all be right: <b>$2.70</b> from a $120 keg at ~44 schooners, <b>$2.98</b> (and $2.34 for members) from a $140 keg at 47, and <b>$2.55 member / $3.19 non-member</b> from the verified price list at 47. Three keg prices, two schooner counts. This is the most quotable number in the business and there is a live ad running on one version of it. Until it is settled the instruction across the set is to pull the claim, not to re-price it.",
    "Blocks: all creative, paid media, the copy deck, the case study"),
}

HEADS = {
  "decision": ("Decisions &middot; nobody can research these for you",
               "Eight questions that need a call, not more work. Six of them are on the deck; "
               "<b>name-versus-mark</b> and <b>cost on or off the table</b> are not, and belong in the same conversation."),
  "data":     ("Data and access &middot; these arrive with a file, a date or a login",
               "Nothing here needs a meeting. Each one unlocks a specific piece of the set, and two of them "
               "&ndash; the cost drivers and the Square history &ndash; are what stand between a judgement and a business case."),
  "joint":    ("One we settle together",
               "Not yours alone and not ours. It needs your price list against our arithmetic, in one sitting."),
}

def parse():
    body = open(TRACKER, encoding="utf-8").read()
    sec  = body.split("## Open items carried across the set")[1].split("\n## ")[0]
    out  = []
    for row in sec.splitlines():
        if not re.match(r"^\|\s*\d+\s*\|", row):
            continue
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if "CLOSED" in row:                    # closed items never reach the page
            continue
        out.append({"n": int(cells[0]), "owner": cells[2],
                    "partly": "Partly closed" in row})
    return out

def render():
    items = parse()
    missing = [i["n"] for i in items if i["n"] not in COPY or i["n"] not in GROUP]
    if missing:
        raise SystemExit(f"Tracker has open items with no summary copy: {missing}. "
                         f"Add them to COPY and GROUP in {os.path.basename(__file__)}.")
    total = len(items)
    counts = {g: sum(1 for i in items if GROUP[i["n"]] == g) for g in ("decision", "data", "joint")}

    html = []
    html.append('    <section class="page" id="need">')
    html.append('      <div class="page-head"><span class="chip">What we still need from you</span>'
                '<span class="count">09 / 12</span></div>')
    html.append(f'      <h2 class="h-sec rv">{word(total, True)} open items. '
                f'{word(counts["decision"], True)} of them are decisions, not research.</h2>')
    html.append('      <p class="body mt28 rv">These are the questions the work is waiting on, every one of them, '
                'pulled straight from the tracker rather than summarised. Two have closed since we started: your census '
                'landed in August, and the advisory review settled the competitor&rsquo;s name. The rest split cleanly. '
                f'{word(counts["decision"], True)} need a decision from the two of you, and no amount of further work will produce one. '
                f'{word(counts["data"], True)} arrive the moment someone sends a file, a date or a login. One we settle together. '
                'Nothing below is padding &ndash; each item names what it blocks.</p>')

    html.append('''
      <div class="band rv">
        <div class="eyebrow on-dark">The two that would change the most</div>
        <p class="body on-dark mt20" style="max-width:66ch"><b>What the business actually costs to run</b>, and
        <b>a taproom conversion rate somebody has counted</b>. Between them they decide whether the taproom is a
        funnel or a cost, and whether this plan is affordable. Everything else here is smaller than these two,
        and we would rather flag that plainly than present a set that reads more certain than it is.</p>
      </div>''')

    n = 0
    for group in ("decision", "data", "joint"):
        head, blurb = HEADS[group]
        html.append(f'\n      <div class="eyebrow mt56 rv">{head}</div>')
        html.append(f'      <p class="body mt12 rv" style="max-width:70ch">{blurb}</p>')
        html.append('      <div class="items rv">')
        for it in sorted((i for i in items if GROUP[i["n"]] == group), key=lambda i: i["n"]):
            n += 1
            title, para, blocks = COPY[it["n"]]
            owner = {"Founders": "Chris &amp; Justin", "Jewell + Client": "Jewell &amp; Tap That"}\
                    .get(it["owner"], "Tap That Brewery")
            tag = ' <span class="pill pending">partly closed</span>' if it["partly"] else ""
            html.append(f'''        <div class="item">
          <div class="item-n">{n:02d}</div>
          <div>
            <div class="item-t">{title}{tag}</div>
            <div class="item-b">{para}</div>
            <div class="item-meta">Owner: {owner} &middot; {blocks} &middot; tracker #{it["n"]}</div>
          </div>
        </div>''')
        html.append('      </div>')

    html.append('''
      <div class="band deep rv">
        <div class="eyebrow on-dark">Two things worth fixing this week, whatever else happens</div>
        <p class="body on-dark mt20" style="max-width:66ch">Neither waits on a gate. The
        <b>&ldquo;$2.34 a schooner&rdquo;</b> claim currently running against a &ldquo;$14 at the pub&rdquo;
        comparison only holds for Keg Crew members. What a non-member actually pays is not settled &ndash; $2.70,
        $2.98 and $3.19 all follow from different keg prices and schooner counts in circulation &ndash; so the fix
        is to pull the claim, not to swap the number. And staff are being told Keg Crew breaks even at six refills
        when the arithmetic says <b>8.33</b>. The first is advertising-standards exposure on a live ad; the second
        is a promise your team is making in good faith that the numbers don&rsquo;t keep.</p>
      </div>
    </section>''')
    return "\n".join(html), total, counts

def main():
    section, total, counts = render()
    if "--splice" not in sys.argv:
        print(section); return
    s = open(SUMMARY, encoding="utf-8").read()
    start = s.index('    <section class="page" id="need">')
    end   = s.index('<section class="page" id="access">')
    end   = s.rindex("\n", start, end)                 # keep the comment above ACCESS
    tail  = s[start:end]
    keep  = tail[tail.rindex("</section>") + len("</section>"):]
    open(SUMMARY, "w", encoding="utf-8").write(s[:start] + section + keep + s[end:])
    print(f"spliced: {total} open items ({counts['decision']} decisions, "
          f"{counts['data']} data, {counts['joint']} joint)")

if __name__ == "__main__":
    main()
