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
def flag(rule, path, detail):
    FINDINGS.append((rule, os.path.relpath(path, ROOT), detail))

def lines(path):
    with open(path, encoding="utf-8", errors="ignore") as fh:
        return fh.read().splitlines()

# --------------------------------------------------------------------------
# Rules over the document set
# --------------------------------------------------------------------------
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
    for i, l in enumerate(ls, 1):
        if re.search(r"4\.5\s*(x|&times;|×)", l) and not re.search(
                r"not|rather than|assumed|superseded|was\b", l, re.I):
            flag("growth-multiple", path, f"line {i}: ~4.5x asserted as current")

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

def rule_schooner_price(path, ls):
    """Open item #19. Three incompatible sets of maths are in circulation:
    $2.70 ($120/44), $2.98 and $2.34 ($140/47, less the $30 member discount),
    and $2.55/$3.19 (verified price list, $120/$150 at 47). It is the most
    quotable number in the business, so no document may state one flat."""
    for i, l in enumerate(ls, 1):
        if re.search(r"\$2\.(34|98|70|55)|\$3\.19", l) and not re.search(
                r"open item|unsettled|unresolved|#19\b|three (different|sets)|"
                r"in circulation|settle|verified price list|reconcil|pull the|rather than re-pricing",
                l, re.I):
            flag("schooner-price-unflagged", path, f"line {i}: states a per-schooner price as settled")

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
             rule_discover_is_input, rule_ranked_moves_order]

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

    if not quiet:
        print(f"Audited {nd} source documents and {ns} client-facing surfaces.\n")
        if not FINDINGS:
            print("No findings. Every rule in the register holds across the set.")
        else:
            by_rule = {}
            for rule, path, detail in FINDINGS:
                by_rule.setdefault(rule, []).append((path, detail))
            for rule in sorted(by_rule, key=lambda k: -len(by_rule[k])):
                hits = by_rule[rule]
                print(f"## {rule} — {len(hits)}")
                for path, detail in hits:
                    print(f"   {path.split('/')[-1][:52]:<54} {detail}")
                print()
            print(f"TOTAL: {len(FINDINGS)} findings")
    return 1 if FINDINGS else 0

if __name__ == "__main__":
    sys.exit(main())
