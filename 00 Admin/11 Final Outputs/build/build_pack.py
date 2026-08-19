#!/usr/bin/env python3
"""Build the Tap That complete 3D Process pack — all 65 documents on one page."""
import os, re, glob, html
import markdown

ROOT = "/home/user/tapthatbrewery"
OUT = os.path.join(ROOT, "00 Admin/11 Final Outputs/site/index.html")

# catalogue number -> (title, phase, slug)
CAT = {
 1:("Deal Memo","Onboarding","deal-memo"),
 2:("Proposal","Onboarding","proposal"),
 3:("Welcome Pack","Onboarding","welcome-pack"),
 4:("Audience Teardown","Discover","audience-teardown"),
 5:("Customer Segments","Discover","customer-segments"),
 6:("Customer Pain Points","Discover","customer-pain-points"),
 7:("Buying Triggers & Barriers","Discover","buying-triggers-barriers"),
 8:("Jobs To Be Done","Discover","jobs-to-be-done"),
 9:("Competitor Analysis","Discover","competitor-analysis"),
 10:("Category Positioning","Discover","category-positioning"),
 11:("Market Gaps","Discover","market-gaps"),
 12:("Differentiation Opportunities","Discover","differentiation-opportunities"),
 13:("Offer Worksheet","Discover","offer-worksheet"),
 14:("Product / Service Review","Discover","product-service-review"),
 15:("Pricing / Packaging Notes","Discover","pricing-packaging-notes"),
 16:("Sales Process Review","Discover","sales-process-review"),
 17:("Funnel Review","Discover","funnel-review"),
 18:("Success Definition","Discover","success-definition"),
 19:("Objectives & Key Results","Discover","okrs"),
 20:("Discover Summary (CP1)","Discover","discover-summary"),
 21:("Priority Problems To Solve","Discover","priority-problems"),
 22:("Recommended Next Moves","Discover","recommended-next-moves"),
 23:("Business Plan","Design","business-plan"),
 24:("Strategic Priorities","Design","strategic-priorities"),
 25:("Growth Roadmap","Design","growth-roadmap"),
 26:("Measurement Plan","Design","measurement-plan"),
 27:("Customer Profile","Design","customer-profile"),
 28:("Customer Journey","Design","customer-journey"),
 29:("Messaging by Stage","Design","messaging-by-stage"),
 30:("Conversion Pathway","Design","conversion-pathway"),
 31:("Brand Strategy","Design","brand-strategy"),
 32:("Positioning","Design","positioning"),
 33:("Messaging & Offer Architecture","Design","messaging-offer-architecture"),
 34:("Brand Guidelines","Design","brand-guidelines"),
 35:("Brand Copy Workbook","Design","brand-copy-workbook"),
 36:("Logo Brief","Design","logo-brief"),
 37:("Website Strategy","Design","website-strategy"),
 38:("Sitemap","Design","sitemap"),
 39:("Page Strategy","Design","page-strategy"),
 40:("SEO Strategy","Design","seo-strategy"),
 41:("Social Strategy","Design","social-strategy"),
 42:("Content Strategy","Design","content-strategy"),
 43:("In-Market Activation Plan","Design","activation-plan"),
 44:("Partnership / Referral Plan","Design","partnership-referral-plan"),
 45:("Campaign Calendar","Design","campaign-calendar"),
 46:("Paid Media Plan","Design","paid-media-plan"),
 47:("EDM Plan","Design","edm-plan"),
 48:("CRM Plan","Design","crm-plan"),
 49:("PR Plan","Design","pr-plan"),
 50:("Events Plan","Design","events-plan"),
 51:("Traditional Media Plan","Design","traditional-media-plan"),
 52:("Design Brief","Design","design-brief"),
 53:("Website Brief","Design","website-brief"),
 54:("Photo & Video Brief","Design","photo-video-brief"),
 55:("SEO Brief","Design","seo-brief"),
 56:("Paid Media Brief","Design","paid-media-brief"),
 57:("EDM Brief","Design","edm-brief"),
 58:("CRM Brief","Design","crm-brief"),
 59:("PR Brief","Design","pr-brief"),
 60:("Events Brief","Design","events-brief"),
 61:("Final Brief Pack","Design","final-brief-pack"),
 62:("IMC Summary","Design","imc-summary"),
 63:("Strategy Summary (CP2)","Design","strategy-summary"),
 64:("Approved Roadmap","Design","approved-roadmap"),
 65:("Case Study / Evidence Pack","Deploy","case-study"),
}

SIGNOFF = {2,20,34,36,61,62,63}
LEGACY = {"D02":4, "D03":9, "D05":13, "D06":20}

def find_files():
    found = {}
    dirs = ["00 Admin/04 Commercial + SOW", "01 Discover/02 Working Drafts",
            "02 Design/02 Working Drafts", "03 Deploy/02 Working Drafts"]
    for d in dirs:
        for p in glob.glob(os.path.join(ROOT, d, "*.md")):
            base = os.path.basename(p)
            m = re.match(r'^(\d{2})__', base)
            if m:
                found[int(m.group(1))] = p; continue
            m = re.match(r'^(D\d{2})__', base)
            if m and m.group(1) in LEGACY:
                found[LEGACY[m.group(1)]] = p
    return found

def convert(path):
    raw = open(path, encoding="utf-8").read()
    # drop the leading H1 (we render our own title) and any immediate H2 subtitle
    lines = raw.split("\n")
    out, dropped_h1 = [], False
    for ln in lines:
        if not dropped_h1 and ln.startswith("# "):
            dropped_h1 = True; continue
        if dropped_h1 and len(out) == 0 and ln.startswith("## "):
            continue
        out.append(ln)
    body = "\n".join(out)
    h = markdown.markdown(body, extensions=["tables", "sane_lists", "attr_list"])
    # demote headings one level so the doc title stays h2
    for a, b in [(5,6),(4,5),(3,4),(2,3)]:
        h = h.replace(f"<h{a}>", f"<h{b}>").replace(f"</h{a}>", f"</h{b}>")
    # wrap tables for horizontal scroll
    h = h.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    return h

def main():
    files = find_files()
    missing = [n for n in CAT if n not in files]
    if missing:
        print("MISSING:", missing)
    docs = []
    for n in sorted(CAT):
        if n not in files: continue
        title, phase, slug = CAT[n]
        docs.append(dict(n=n, title=title, phase=phase, slug=slug,
                         html=convert(files[n]), signoff=n in SIGNOFF))
    total = len(docs)

    # ---- sidebar nav ----
    nav, last_phase = [], None
    nav.append('<a class="nav-link edge" href="#top"><span class="nav-num">·</span><span>Welcome</span></a>')
    for d in docs:
        if d["phase"] != last_phase:
            nav.append(f'<p class="nav-phase">{d["phase"]}</p>')
            last_phase = d["phase"]
        star = '<span class="sig" title="Client sign-off">&bull;</span>' if d["signoff"] else ''
        nav.append(
            f'<a class="nav-link" href="#{d["slug"]}" data-t="{html.escape(d["title"].lower())}">'
            f'<span class="nav-num">{d["n"]:02d}</span><span>{html.escape(d["title"])}{star}</span></a>')
    nav_html = "\n".join(nav)

    # ---- documents ----
    arts = []
    for i, d in enumerate(docs):
        prev_d = docs[i-1] if i > 0 else None
        next_d = docs[i+1] if i < total-1 else None
        pn = (f'<a class="dn-btn prev" href="#{prev_d["slug"]}"><span>Previous</span>'
              f'<strong>{html.escape(prev_d["title"])}</strong></a>') if prev_d else '<span class="dn-sp"></span>'
        nx = (f'<a class="dn-btn next" href="#{next_d["slug"]}"><span>Next</span>'
              f'<strong>{html.escape(next_d["title"])}</strong></a>') if next_d else \
             '<a class="dn-btn next" href="#top"><span>Back to</span><strong>Welcome</strong></a>'
        sig = '<span class="pill sign">Sign-off</span>' if d["signoff"] else ''
        arts.append(f'''
<article class="doc" id="{d["slug"]}">
  <div class="doc-head">
    <div class="doc-head-l"><span class="doc-chip">{d["phase"]}</span>{sig}<span class="pill draft">Draft v01</span></div>
    <span class="doc-count">Document {d["n"]:02d} of {total}</span>
  </div>
  <h2 class="doc-title">{html.escape(d["title"])}</h2>
  <div class="prose">{d["html"]}</div>
  <nav class="doc-nav">{pn}{nx}</nav>
</article>''')
    arts_html = "\n".join(arts)

    counts = {}
    for d in docs: counts[d["phase"]] = counts.get(d["phase"], 0) + 1

    page = TEMPLATE.replace("{{NAV}}", nav_html).replace("{{DOCS}}", arts_html) \
                   .replace("{{TOTAL}}", str(total)) \
                   .replace("{{N_ON}}", str(counts.get("Onboarding",0))) \
                   .replace("{{N_DI}}", str(counts.get("Discover",0))) \
                   .replace("{{N_DE}}", str(counts.get("Design",0))) \
                   .replace("{{N_DP}}", str(counts.get("Deploy",0)))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(page)
    print(f"wrote {OUT}  ({len(page):,} chars, {total} documents)")

TEMPLATE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pack_template.html"), encoding="utf-8").read()

if __name__ == "__main__":
    main()
