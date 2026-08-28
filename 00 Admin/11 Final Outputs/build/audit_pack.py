#!/usr/bin/env python3
"""
Fact-check the Tap That Brewery pack against a register of established truths.

Every rule below traces to a primary source: the client's business records, the
census, #20A (evidence reconciliation) or #20B (advisory review). The point is
that the set's consistency stops depending on anyone's memory -- run this after
any edit and it will say what drifted.

    python3 audit_pack.py            # report
    python3 audit_pack.py --quiet    # exit code only, for a pre-deploy gate
"""
import glob, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Files that are allowed to contain superseded language because they are either
# the verbatim source record or the document that names the error.
EXEMPT = ("advisory-review", "20B__", "20A__", "/uploads/", "/meetings/",
          "Output-Tracker", "audit_pack.py", "/build/", "node_modules")

def docs():
    """The 79-document set, as markdown."""
    for stage in ("01 Discover/02 Working Drafts", "02 Design/02 Working Drafts",
                  "03 Deploy/02 Working Drafts", "00 Admin"):
        for f in sorted(glob.glob(os.path.join(ROOT, stage, "**", "*.md"), recursive=True)):
            if not any(x in f for x in EXEMPT):
                yield f

def surfaces():
    """Client-facing renderings: the four sheets, the summary, the deck source."""
    base = os.path.join(ROOT, "00 Admin/11 Final Outputs")
    for f in sorted(glob.glob(os.path.join(base, "build/oap/*.html"))):
        yield f
    yield os.path.join(base, "delivery-summary.html")
    yield os.path.join(ROOT, "00 Admin/06 Presentations/deck_content.py")

FINDINGS = []
# Rules that report outstanding work rather than a defect. Something on this
# list is not wrong, it is not finished -- so it is reported but does not fail
# the gate. Everything else is a defect: the set says something untrue.
BACKLOG = {"pre-review-interpretation"}

def flag(rule, path, detail):
    FINDINGS.append((rule, os.path.relpath(path, ROOT), detail))

def lines(path):
    with open(path, encoding="utf-8", errors="ignore") as fh:
        return fh.read().splitlines()

# --------------------------------------------------------------------------
# Rules over the document set
# --------------------------------------------------------------------------
# Claims the delivery summary must carry. The open-items section is generated,
# and regenerating it once silently dropped the baseline correction -- the most
# consequential finding in the engagement -- because the band that held it lived
# inside the replaced region. A generator that rebuilds a region can quietly
# lose anything that was in it, so the load-bearing claims are asserted here.
SUMMARY_MUST_SAY = {
    "the growth multiple":      r"9&times;|~9&times;",
    "the multiple it replaces": r"4\.5&times;",
    "corrections applied":      r"46 documents",
    "the switcher figure":      r"116 of 206",
    "the loss is named":        r"losing money|loss[- ]making",
    "the taproom tension":      r"taproom as a funnel|also a cost|zero[- ]sum",
    "the unmeasured rate":      r"never observed|nobody has measured|unmeasured",
    "open item count":          r"Nineteen open items",
    "document count":           r"Seventy-nine",
    "price claim pulled":       r"pull the claim, not to swap",
    "the deck":                 r'href="/deck"',
}

def rule_wholesale_promoted(path, ls):
    """#24 P4 reversed after the review: commercial and wholesale went from
    opportunism to a ranked priority with an owner. Reworking one document and
    not its dependants is how a set starts contradicting itself."""
    text = "\n".join(ls)
    for m in re.finditer(r"opportunis\w*|white[- ]label only", text):
        window = near(text, m, 200)
        if re.search(r"wholesale|commercial", window, re.I) and not re.search(
                r"reversed|previously|no longer|first draft|rather than|resourced|"
                r"one offer inside|not opportunism", window, re.I):
            flag("wholesale-still-opportunism", path,
                 f"line {line_of(text, m.start())}: wholesale framed as opportunism")

def rule_lifecycle_cadence(path, ls):
    """The lifecycle clock is per-customer after the review, not a flat 60/75/90.
    A document may still name those days as a fallback, but not as the design."""
    text = "\n".join(ls)
    for m in re.finditer(r"60/75/90|day[- ]?60/75/90", text):
        if not re.search(r"own (reorder )?interval|their interval|per[- ]customer|"
                         r"fallback|flat|interim|rails", near(text, m, 320), re.I):
            flag("flat-lifecycle-clock", path,
                 f"line {line_of(text, m.start())}: flat 60/75/90 stated as the design")

def rule_summary_completeness(path, ls):
    if not path.endswith("delivery-summary.html"):
        return
    body = "\n".join(ls)
    for label, pat in SUMMARY_MUST_SAY.items():
        if not re.search(pat, body, re.I):
            flag("summary-lost-a-claim", path, f"the summary no longer says: {label}")

def rule_no_ingestion_banner(path, ls):
    """Dated ingestion banners were removed from the set on 28 August. They were
    scaffolding for us, not information for the client, and by then they were
    also wrong -- the figures no longer predated the census, they had been
    corrected in place. 20A keeps its own correction log; it IS the record."""
    for i, l in enumerate(ls, 1):
        if l.lstrip().startswith(">") and re.search(
                r"Evidence note|predate the client|figures in this draft", l, re.I):
            flag("ingestion-banner", path, f"line {i}: dated ingestion banner is back")

def rule_stale_census_tense(path, ls):
    """The census arrived 19 August and was worked through on 20 August. Nothing
    may still speak of it as a future event."""
    for i, l in enumerate(ls, 1):
        if re.search(r"census (detail )?pending|pending census|awaiting the census|"
                     r"when the census lands|until the census (lands|arrives)|once the census (lands|arrives)",
                     l, re.I):
            flag("census-still-future", path, f"line {i}: treats the census as not yet arrived")

# Whether a document has absorbed the 27 August review, measured by content
# rather than by whether it happens to cite #20B -- a one-line flag cites it
# too. Each marker is a finding the review actually made.
# Each marker must match the review's FINDING, not merely the noun it concerns.
# Lease-to-buy was already in the plan; the finding was to reframe it as a
# monthly that removes the upfront barrier. Hop On was already a known traffic
# source; the finding was that the operator picks the venues, so the write-up
# converts. Matching the noun counted documents as reworked when they were not.
REVIEW_MARKERS = {
    "loss-making":       r"\bloss[- ]making\b|\blos(e|es|ing) money\b",
    "buy-the-databases": r"buy the database|buyer list|database of (buyers|system owners)|"
                         r"bought lists|buy the lists",
    "cadence":           r"\b10/60/40\b|cut back, not defected|own (reorder )?interval|"
                         r"before the reorder|their interval",
    "commercial-x10":    r"\bten households\b|worth roughly ten",
    "taproom-zero-sum":  r"\bzero[- ]sum\b|built on people \*?not\*? coming|work against each other",
    "census-demoted":    r"\bself[- ]report|will never surface|too small and too self|"
                         r"say out loud|what people will say",
    "catered-vs-covered": r"covered rather than catered|catered to rather than|blokes will follow",
    "tour-operators":    r"operator picks|customer (choose|pick)s? which brewer|write-up decides|"
                         r"\bUrban Legends\b|\bPineapple Tours\b",
    "low-alcohol":       r"\blow[- ]alcohol\b|hydration not beer|healthier line|healthy or low",
    "range-decision":    r"\bsix core beers\b|cut to (about )?six\b|decision anxiety",
    "premium-beats-middle": r"\bSecond Earth\b|\bmiddle ground\b|neither cheap nor",
    "website-teardown":  r"\babove the fold\b|\bDrink Hopper\b|\bclick-dots\b|"
                         r"four business units|low-resolution logo|background film",
    "competitor-weaker": r"domain is suspended|\bBurleigh Homebrew\b",
    "wholesale-wiifm":   r"\bWIIFM\b|\bwhite label\b|cuisine matching",
    "one-membership":    r"\bone membership\b|membership should span|spanning the taproom",
    "puppy-dog":         r"\bpuppy[- ]dog\b|system in a booth",
    "loyalty-simplified": r"every tenth keg|tenth keg free",
    "events-drive-a-week": r"week of taproom trade|week of trade\b",
    "lease-to-buy-reframed": r"\bgym membership\b|razor[- ]and[- ]blades|"
                             r"remove the upfront barrier|upfront barrier",
    "unsaid-drivers":    r"\bego\b|seen as (more )?successful|not (be )?said out loud|"
                         r"out of the house|unsaid driver",
    "three-ranked-moves": r"three (ranked )?moves|ranked (first|above|explicitly below)|"
                          r"rank above|outrank this sprint",
    "franchise-consent":  r"franchise.{0,60}consent|said publicly|open item #6\b",
    "conversion-unmeasured": r"never been (measured|observed)|has never been measured|"
                             r"pay people to walk in",
    "driver-order-open":  r"provisional pending CP1|order people will say|"
                          r"what people will say|stated order",
    "award-unused":       r"not on the (website|landing)|does not appear on the (website|landing)|"
                          r"award is not being used|absent from the brewery write-ups",
}



# Documents where a specific review finding clearly applies. Each entry names
# the finding, so the list is auditable rather than a matter of opinion. A
# document leaves this list by absorbing the finding, not by being removed.
# Documents where a specific review finding applies, and the marker that shows
# the finding actually landed. Checking one named finding per document beats a
# generic "any two markers" threshold: a document can absorb exactly what the
# review said about it and still not mention the other findings.
REVIEW_BEARS_ON = {
    "06": ("the unsaid drivers -- ego, status, wanting to be out of the house", "unsaid-drivers"),
    "07": ("the partner reframed from veto to audience to cater for", "catered-vs-covered"),
    "08": ("the hydration and health job for lapsed owners", "low-alcohol"),
    "10": ("the competitor is weaker; premium beats the middle ground", "premium-beats-middle"),
    "12": ("one commercial account is worth about ten households", "commercial-x10"),
    "14": ("the range decision, the RTD range, the low-alcohol line", "range-decision"),
    "15": ("reverse razor-and-blades, lease-to-buy, delivery as a benefit", "lease-to-buy-reframed"),
    "16": ("the puppy-dog close, and buying the system-owner databases", "puppy-dog"),
    "17": ("the taproom and refill model are zero-sum", "taproom-zero-sum"),
    "21": ("the cost drivers are the largest gap", "loss-making"),
    "23": ("the business is loss-making and its costs are unknown", "loss-making"),
    "24": ("the three ranked moves reorder the priorities", "three-ranked-moves"),
    "27": ("the unsaid drivers a self-report will not surface", "unsaid-drivers"),
    "28": ("cadence: 10 percent monthly, 60 quarterly, 40 longer", "cadence"),
    "29": ("the stage copy follows the superseded driver order", "driver-order-open"),
    "30": ("the 20-30 percent conversion is unmeasured", "conversion-unmeasured"),
    "31": ("the census is one input, not the anchor", "census-demoted"),
    "32": ("Second Earth as the counter-example -- premium beats the middle", "premium-beats-middle"),
    "33": ("whether cost is on the table at all", "driver-order-open"),
    "37": ("the full website teardown, and Drink Hopper as the reference", "website-teardown"),
    "39": ("the above-the-fold findings from the teardown", "website-teardown"),
    "40": ("the competitor domain is suspended; check what resolves", "competitor-weaker"),
    "43": ("taproom traffic by social is ranked below the three moves", "three-ranked-moves"),
    "46": ("the prior Meta ad account, and the reordered priorities", "three-ranked-moves"),
    "47": ("the blanket clock is tone-deaf against real reorder patterns", "cadence"),
    "48": ("personalised reorder timing, and every tenth keg free", "loyalty-simplified"),
    "50": ("one event drives a week of taproom trade", "events-drive-a-week"),
    "64": ("the roadmap order changes with the three moves", "three-ranked-moves"),
    "71": ("franchise-story consent, and the awards that are not being used", "franchise-consent"),
    "77": ("the sprint order follows the three ranked moves", "three-ranked-moves"),
}


def review_markers(text):
    return [k for k, pat in REVIEW_MARKERS.items() if re.search(pat, text, re.I)]

def rule_review_absorbed(path, ls):
    """Removing the dated evidence banners took away the only visible signal
    that a document predates the review. It lives here instead: internal,
    specific about what is missing, and it shrinks as the work is done."""
    num = os.path.basename(path).split("__")[0]
    if num not in REVIEW_BEARS_ON:
        return
    finding, marker = REVIEW_BEARS_ON[num]
    if not re.search(REVIEW_MARKERS[marker], "\n".join(ls), re.I):
        flag("pre-review-interpretation", path,
             f"#{num} predates the review -- missing: {finding}")

def rule_competitor_closed(path, ls):
    """Open item #3 closed 27 Aug: the competitor is Aardvark and Arrow."""
    doubt = r"unverified|confirm spelling|confirm the competitor|verify before|carries that caveat"
    for i, l in enumerate(ls, 1):
        for m in re.finditer(r"Aardvark|Ardbach", l):
            # The caveat has to attach to the NAME. Elsewhere on the line it is
            # almost certainly hedging a different figure.
            near = l[max(0, m.start() - 90): m.end() + 90]
            if re.search(doubt, near, re.I):
                flag("competitor-name-closed", path, f"line {i}: still treated as unverified")
                break

def rule_no_raef(path, ls):
    """The client's marketing lead is Harry. Raef is a Jewell Projects resource."""
    if "contacts.md" in path:
        return
    for i, l in enumerate(ls, 1):
        # A line that names the mistake is the correction, not an instance of it.
        if re.search(r"\bRaef\b", l) and not re.search(
                r"called Harry|not Harry|Harry.{0,40}Raef|Raef.{0,40}Harry|"
                r"Jewell Projects resource|conflated|naming error|in 160 places|"
                r"a hundred and sixty", l, re.I):
            flag("raef-not-harry", path, f"line {i}: {l.strip()[:80]}")

def rule_dead_baseline(path, ls):
    """The 220 active-customer baseline never existed; records show 96-113."""
    for i, l in enumerate(ls, 1):
        if re.search(r"\b220\b", l) and not re.search(
                r"never existed|void|rebas|discredit|no longer|withdrawn|not a real|"
                r"superseded|replaced|the old one|corrected|was built on", l, re.I):
            flag("dead-220-baseline", path, f"line {i}: 220 used without the correction")

def rule_growth_multiple(path, ls):
    """From 96-113 the climb to 1,000 is ~9x, not the ~4.5x the plan assumed."""
    text = "\n".join(ls)
    ok = r"not\b|rather than|assumed|superseded|was\b|old figure|to ~?9|replaced|no longer"
    for m in re.finditer(r"4\.5\s*(x|&times;|×)", text):
        if not re.search(ok, near(text, m), re.I):
            flag("growth-multiple", path,
                 f"line {line_of(text, m.start())}: ~4.5x asserted as current")

def rule_taproom_conversion(path, ls):
    """20-30% is the client's estimate, never measured (#20B). Must be flagged."""
    for i, l in enumerate(ls, 1):
        if re.search(r"20\s*(&ndash;|–|-)\s*30\s*%", l) and not re.search(
                r"unverified|unmeasured|estimate|not measured|#20B|never measured|claimed", l, re.I):
            flag("taproom-conversion-unflagged", path, f"line {i}: used as fact")

def rule_mangled_cadence(path, ls):
    """An earlier find/replace spliced ~1.55 into the keg cadence string."""
    for i, l in enumerate(ls, 1):
        if re.search(r"1\s*(&ndash;|–|-)\s*~?1\.55", l):
            flag("mangled-cadence", path, f"line {i}: corrupted cadence figure")

def rule_loss_making_named(path, ls):
    """#20B: strategy documents must not describe the business without naming
    that it is loss-making. Applies to the synthesis and strategy tier only."""
    key = ("20__Discover-Summary", "D06__Discovery-Pack", "23__Business-Plan",
           "24__Strategic-Priorities", "22__Recommended-Next-Moves")
    if not any(k in path for k in key):
        return
    body = "\n".join(ls)
    if not re.search(r"loss[- ]making|los(?:e|es|ing) money|not profitable|unprofitable|"
                     r"cannot fund|red at the bottom", body, re.I):
        flag("loss-making-unnamed", path, "strategy document never names the loss")

def near(text, m, span=280):
    """The window a caveat may live in. HTML wraps a paragraph across several
    lines, so a line-bound check reads a qualified claim as an unqualified one."""
    return text[max(0, m.start() - span): m.end() + span]

def line_of(text, pos):
    return text.count("\n", 0, pos) + 1

def rule_schooner_price(path, ls):
    """Open item #19. Three incompatible sets of maths are in circulation:
    $2.70 ($120/44), $2.98 and $2.34 ($140/47, less the $30 member discount),
    and $2.55/$3.19 (verified price list, $120/$150 at 47). It is the most
    quotable number in the business, so no document may state one flat."""
    text = "\n".join(ls)
    ok = (r"open item|unsettled|unresolved|#19\b|three (different|sets)|in circulation|"
          r"settle|verified price list|reconcil|pull the|rather than re-pricing|not settled")
    for m in re.finditer(r"\$2\.(34|98|70|55)|\$3\.19", text):
        if not re.search(ok, near(text, m), re.I):
            flag("schooner-price-unflagged", path,
                 f"line {line_of(text, m.start())}: states a per-schooner price as settled")

def rule_membership_price(path, ls):
    """Open item #2. Two membership posters are live in the venue and disagree:
    $250/yr against $300 plus a $120 renewal."""
    for i, l in enumerate(ls, 1):
        if re.search(r"\$250\s*(/|\s)\s*(yr|year|pa)|\$250/yr", l) and not re.search(
                r"open item|unresolved|conflict|disagree|two (live |)poster|which poster|"
                r"reconcil|unconfirmed|\$300", l, re.I):
            flag("membership-price-unflagged", path, f"line {i}: quotes one membership price as settled")

def rule_discover_is_input(path, ls):
    """#20B: Discover became an input to the next step, not the output awaiting
    CP1. Any document still promising CP1 as the next deliverable is stale."""
    for i, l in enumerate(ls, 1):
        if re.search(r"(next deliverable|the deliverable)[^.]{0,60}(CP1|Gate 1)", l, re.I) and \
           not re.search(r"was\b|superseded|no longer|replaced|instead|rather than", l, re.I):
            flag("cp1-superseded", path, f"line {i}: still names CP1 as the next deliverable")

def rule_ranked_moves_order(path, ls):
    """#20B ranked the three moves, and ranked taproom-via-social below them.
    A document that presents taproom social as a leading move contradicts it."""
    body = "\n".join(ls)
    if re.search(r"(lead|first|primary|top) (move|priority|recommendation)[^.]{0,80}"
                 r"(taproom|social media)", body, re.I) and "#20B" not in body:
        flag("ranked-moves-order", path, "leads with taproom/social, which #20B ranked below")

DOC_RULES = [rule_competitor_closed, rule_no_raef, rule_dead_baseline,
             rule_growth_multiple, rule_taproom_conversion, rule_mangled_cadence,
             rule_loss_making_named, rule_schooner_price, rule_membership_price,
             rule_discover_is_input, rule_ranked_moves_order,
             rule_no_ingestion_banner, rule_stale_census_tense, rule_review_absorbed,
             rule_summary_completeness, rule_wholesale_promoted, rule_lifecycle_cadence]

# --------------------------------------------------------------------------
# Rules over the counts, checked against the generator and the tracker
# --------------------------------------------------------------------------
def catalogue_counts():
    src = open(os.path.join(ROOT, "00 Admin/11 Final Outputs/build/build_pack.py"),
               encoding="utf-8").read()
    ns = {}
    exec(re.search(r"CAT = \{.*?\n\}", src, re.S).group(0), ns)
    cat = ns["CAT"]
    by = {}
    for v in cat.values():
        by[v[1]] = by.get(v[1], 0) + 1
    return len(cat), by

def open_item_counts():
    p = os.path.join(ROOT, "00 Admin/05 Timelines + Project Control/Maxxim-Output-Tracker.md")
    sec = open(p, encoding="utf-8").read().split("## Open items carried across the set")[1].split("\n## ")[0]
    rows = [r for r in sec.splitlines() if re.match(r"^\|\s*\d+\s*\|", r)]
    live = [r for r in rows if "CLOSED" not in r]
    founders = [r for r in live if "Founders" in r.split("|")[3]]
    return len(rows), len(live), len(founders)

WORDS = {1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight",
         9:"nine",10:"ten",13:"thirteen",15:"fifteen",19:"nineteen",20:"twenty",21:"twenty-one",
         42:"forty-two",77:"seventy-seven",78:"seventy-eight",79:"seventy-nine",80:"eighty"}

def rule_counts(path, ls):
    total, by = catalogue_counts()
    _, live, _ = open_item_counts()
    body = "\n".join(ls)
    # any spelled or numeric document total that is not the real one
    for n, w in WORDS.items():
        if n == total or n not in (77, 78, 80):
            continue
        for m in re.finditer(rf"(?i)\b{w}\b[^.<]{{0,40}}documents", body):
            flag("document-count", path, f"says {w} documents, catalogue has {total}")
        for m in re.finditer(rf"\b{n}\b\s*(documents|working documents)", body):
            flag("document-count", path, f"says {n} documents, catalogue has {total}")
    # open items
    for n, w in WORDS.items():
        if n == live:
            continue
        if re.search(rf"(?i)\b({w}|{n})\b\s+open items", body):
            flag("open-item-count", path, f"says {w}/{n} open items, tracker has {live}")

SURFACE_RULES = DOC_RULES + [rule_counts]

# --------------------------------------------------------------------------
def main():
    quiet = "--quiet" in sys.argv
    nd = ns = 0
    for f in docs():
        nd += 1
        ls = lines(f)
        for r in DOC_RULES:
            r(f, ls)
    for f in surfaces():
        if not os.path.exists(f):
            continue
        ns += 1
        ls = lines(f)
        for r in SURFACE_RULES:
            r(f, ls)

    defects  = [f for f in FINDINGS if f[0] not in BACKLOG]
    backlog  = [f for f in FINDINGS if f[0] in BACKLOG]

    if not quiet:
        print(f"Audited {nd} source documents and {ns} client-facing surfaces.\n")

        def block(title, rows):
            by_rule = {}
            for rule, path, detail in rows:
                by_rule.setdefault(rule, []).append((path, detail))
            print(f"{title}\n")
            for rule in sorted(by_rule, key=lambda k: -len(by_rule[k])):
                hits = by_rule[rule]
                print(f"## {rule} — {len(hits)}")
                for path, detail in hits:
                    print(f"   {path.split('/')[-1][:46]:<48} {detail}")
                print()

        if defects:
            block("DEFECTS — the set says something untrue. These fail the gate.", defects)
        else:
            print("DEFECTS: none. Every correctness rule holds across the set.\n")

        if backlog:
            block("OUTSTANDING — not wrong, not finished. Reported, does not fail the gate.",
                  backlog)

        print(f"{len(defects)} defects, {len(backlog)} outstanding.")
    return 1 if defects else 0

if __name__ == "__main__":
    sys.exit(main())
