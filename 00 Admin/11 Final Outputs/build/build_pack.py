#!/usr/bin/env python3
"""Build the Tap That 3D Process pack — a landing page plus one page per document."""
import os, re, glob, html
import markdown

ROOT = "/home/user/tapthatbrewery"
SITE = os.path.join(ROOT, "00 Admin/11 Final Outputs/site")

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
 205:("Evidence Reconciliation (20A)","Discover","evidence-reconciliation"),
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
 66:("Campaign Launch Runbook","Deploy","campaign-launch"),
 67:("Social Content Rollout","Deploy","social-content-rollout"),
 68:("Paid Media Launch","Deploy","paid-media-launch"),
 69:("EDM Deployment","Deploy","edm-deployment"),
 70:("CRM Workflow Deployment","Deploy","crm-workflow-deployment"),
 71:("PR Outreach","Deploy","pr-outreach"),
 72:("Events Activation","Deploy","events-activation"),
 73:("Partnership Outreach","Deploy","partnership-outreach"),
 74:("Traditional Media Rollout","Deploy","traditional-media-rollout"),
 75:("Tracking Setup","Deploy","tracking-setup"),
 76:("Optimisation Backlog","Deploy","optimisation-backlog"),
 77:("Next Sprint Priorities","Deploy","next-sprint-priorities"),
}

SIGNOFF = {2,20,34,36,61,62,63}
LEGACY = {"D02":4, "D03":9, "D05":13, "D06":20}
# 20A sorts immediately after 20 by using 205 as its sort key

def find_files():
    found = {}
    dirs = ["00 Admin/04 Commercial + SOW", "01 Discover/02 Working Drafts",
            "02 Design/02 Working Drafts", "03 Deploy/02 Working Drafts"]
    for d in dirs:
        for p in glob.glob(os.path.join(ROOT, d, "*.md")):
            base = os.path.basename(p)
            m = re.match(r'^20A__', base)
            if m:
                found[205] = p; continue
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
    # the front-matter tables have an empty header row — drop it rather than
    # render an empty grey band at the top of every document
    h = re.sub(r'<thead>\s*<tr>(?:\s*<th[^>]*>\s*</th>)+\s*</tr>\s*</thead>', '', h)
    # wrap tables for horizontal scroll
    h = h.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    return h

HERO = """    <section id="top">
      <div class="eyebrow">Jewell Projects &middot; Tap That Brewery &middot; Prepared for Chris Smith and Justin Mistry</div>
      <h1 class="h-hero">The complete<br>3D Process.</h1>
      <p class="lead">Every document in the set, end to end. Onboarding, Discover, Design and Deploy &mdash; built from one discovery session, one site visit, and every price on your walls. Pick a document from the contents, or from the index below.</p>

      <div class="stats">
        <div class="stat"><div class="stat-n">{TOTAL}</div><div class="stat-l">Documents</div></div>
        <div class="stat"><div class="stat-n">{N_DI}</div><div class="stat-l">Discover</div></div>
        <div class="stat"><div class="stat-n">{N_DE}</div><div class="stat-l">Design</div></div>
        <div class="stat"><div class="stat-n">{N_DP}</div><div class="stat-l">Deploy</div></div>
      </div>

      <div class="callout">
        <div class="k">The read everything is built on</div>
        <div class="q">Tap That Brewery is a refill subscription business being run with a hospitality venue's attention.</div>
        <p class="b">206 keg systems in the database and somewhere between 96 and 113 active customers &mdash; your own documents give both numbers, because they define &ldquo;active&rdquo; three different ways. Systems go out at cost and all the margin sits in refills, but eighteen months of attention went to the taproom, which loses money and was only ever meant to be the shopfront. And roughly 116 of those 206 owners &mdash; <strong>56%</strong> &mdash; bought their system somewhere else and came to you for beer anyway, with no campaign at all.</p>
        <p class="b">Everything downstream follows from that. For the short version of this pack &mdash; what's here, what isn't, and what's blocking sign-off &mdash; see the <a href="/summary">delivery summary</a>.</p>
      </div>

      <p class="note">Status: every document is a working draft at v01, AI-assisted, and none are approved. Deploy runbooks were written ahead of both checkpoints and say so on their face &mdash; they are ready to run, not authorised to run. The Design phase was written ahead of Discover sign-off so the whole shape could be seen at once. Where a figure is an estimate, a single source or an open question, it is marked rather than smoothed over.</p>
    </section>
"""


def build_nav(docs, active_slug):
    """Sidebar contents. active_slug is '' for the landing page."""
    out = ['<a class="nav-link edge%s" href="/"><span class="nav-num">&middot;</span><span>Welcome</span></a>'
           % ('' if active_slug else ' active')]
    last_phase = None
    for d in docs:
        if d["phase"] != last_phase:
            out.append(f'<p class="nav-phase">{d["phase"]}</p>')
            last_phase = d["phase"]
        star = '<span class="sig" title="Client sign-off">&bull;</span>' if d["signoff"] else ''
        on = ' active' if d["slug"] == active_slug else ''
        out.append(
            f'<a class="nav-link{on}" href="/{d["slug"]}" data-t="{html.escape(d["title"].lower())}">'
            f'<span class="nav-num">{d["label"]}</span><span>{html.escape(d["title"])}{star}</span></a>')
    return "\n".join(out)


def build_index_main(docs, counts, total):
    """Landing page: hero plus a phase-grouped card index."""
    parts = [HERO.format(TOTAL=total, N_DI=counts.get("Discover", 0),
                         N_DE=counts.get("Design", 0), N_DP=counts.get("Deploy", 0))]
    last_phase = None
    for d in docs:
        if d["phase"] != last_phase:
            if last_phase is not None:
                parts.append("</div></section>")
            parts.append(f'<section class="ph"><div class="ph-h"><span class="ph-n">{d["phase"]}</span>'
                         f'<span class="ph-c">{counts.get(d["phase"], 0)} documents</span></div>'
                         f'<div class="cards">')
            last_phase = d["phase"]
        sig = '<span class="card-s">Sign-off</span>' if d["signoff"] else ''
        parts.append(f'<a class="card" href="/{d["slug"]}"><span class="card-n">{d["label"]}</span>'
                     f'<span class="card-t">{html.escape(d["title"])}</span>{sig}</a>')
    if last_phase is not None:
        parts.append("</div></section>")
    return "\n".join(parts)


def build_doc_main(d, i, docs, total):
    prev_d = docs[i - 1] if i > 0 else None
    next_d = docs[i + 1] if i < total - 1 else None
    pn = (f'<a class="dn-btn prev" href="/{prev_d["slug"]}"><span>Previous</span>'
          f'<strong>{html.escape(prev_d["title"])}</strong></a>') if prev_d else \
         '<a class="dn-btn prev" href="/"><span>Back to</span><strong>Welcome</strong></a>'
    nx = (f'<a class="dn-btn next" href="/{next_d["slug"]}"><span>Next</span>'
          f'<strong>{html.escape(next_d["title"])}</strong></a>') if next_d else \
         '<a class="dn-btn next" href="/"><span>Back to</span><strong>Welcome</strong></a>'
    sig = '<span class="pill sign">Sign-off</span>' if d["signoff"] else ''
    return f'''<article class="doc" id="{d["slug"]}">
  <div class="doc-head">
    <div class="doc-head-l"><span class="doc-chip">{d["phase"]}</span>{sig}<span class="pill draft">Draft v01</span></div>
    <span class="doc-count">Document {d["label"]} of {total}</span>
  </div>
  <h2 class="doc-title">{html.escape(d["title"])}</h2>
  <div class="prose">{d["html"]}</div>
  <nav class="doc-nav">{pn}{nx}</nav>
</article>'''


def render(title, nav, main, total):
    return (TEMPLATE.replace("{{TITLE}}", title)
                    .replace("{{NAV}}", nav)
                    .replace("{{MAIN}}", main)
                    .replace("{{TOTAL}}", str(total)))


def main():
    files = find_files()
    missing = [n for n in CAT if n not in files]
    if missing:
        print("MISSING:", missing)
    docs = []
    for n in sorted(CAT, key=lambda k: 20.5 if k == 205 else k):
        if n not in files:
            continue
        title, phase, slug = CAT[n]
        label = "20A" if n == 205 else f"{n:02d}"
        docs.append(dict(n=n, label=label, title=title, phase=phase, slug=slug,
                         html=convert(files[n]), signoff=n in SIGNOFF))
    total = len(docs)

    counts = {}
    for d in docs:
        counts[d["phase"]] = counts.get(d["phase"], 0) + 1

    os.makedirs(SITE, exist_ok=True)

    # landing
    page = render("Tap That Brewery &middot; Complete 3D Process",
                  build_nav(docs, ""), build_index_main(docs, counts, total), total)
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(page)
    written, biggest = 1, 0

    # one page per document
    slugs = set()
    for i, d in enumerate(docs):
        if d["slug"] in slugs:
            raise SystemExit(f"duplicate slug: {d['slug']}")
        slugs.add(d["slug"])
        page = render(f'{html.escape(d["title"])} &middot; Tap That Brewery',
                      build_nav(docs, d["slug"]), build_doc_main(d, i, docs, total), total)
        open(os.path.join(SITE, d["slug"] + ".html"), "w", encoding="utf-8").write(page)
        written += 1
        biggest = max(biggest, len(page))

    print(f"wrote {written} pages to {SITE} ({total} documents, largest page {biggest:,} chars)")


TEMPLATE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pack_template.html"), encoding="utf-8").read()

if __name__ == "__main__":
    main()
