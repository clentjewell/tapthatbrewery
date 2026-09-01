"""Single source of truth for the Tap That client deck.

Both build_deck.py (pptx) and build_deck_html.py (the Cloudflare page) read
from here, so the two renderings cannot drift apart.

Voice rules from jp-brand-presentation: British English, no em dashes in
client-facing copy, no exclamation marks, one idea per sentence.
"""

BAR   = "JP · TAP THAT BREWERY · WHERE YOU ARE"
TITLE = "Where you are, and the three things to do about it"
DATE  = "28 August 2026"

SLIDES = [
 dict(type="title", bar=BAR,
      title="Where you are, and the\nthree things to do about it.",
      subtitle="Prepared for Justin Mistry and Harry. The detail sits behind every slide.",
      date=DATE),

 dict(type="divider", num="Part 01", title="Where you are",
      strapline="We have looked at this properly. This is the read."),

 dict(type="content", eyebrow="The read", head_size=36,
      headline="You are running two businesses that\ncancel each other out.",
      stats=[("206","Systems in your database"),
             ("96 to 113","Active customers. Your own documents define active three ways"),
             ("56%","Bought their system somewhere else and refill with you anyway"),
             ("~9x","The climb to 1,000 from where you actually are")]),

 dict(type="content", eyebrow="The problem underneath",
      headline="The taproom and the refill model\nwork against each other.",
      body="Refills are a subscription business. It works when people stay home and the keg runs "
           "out. The taproom is a hospitality business. It works when people come in. For eighteen "
           "months the attention went to the taproom, because a venue is visible and always "
           "urgent, and it is the half that loses money. This is not a marketing problem. It is a "
           "decision about what the taproom is for."),

 dict(type="content", eyebrow="The gap underneath everything",
      headline="Nobody has priced any of it.",
      body="There is no cost of goods, no figure for what carrying twenty seven taps costs in "
           "ingredients, kegs, storage and refrigeration, and no number for what the taproom "
           "loses each month. Until those land, everything we have written for you is a revenue "
           "plan. We would rather say that than dress it up as a business case."),

 dict(type="content", eyebrow="Before anything else", headline="What we got wrong.",
      rows=[("We never said it","Nothing in seventy nine documents said the business is losing money."),
            ("The taproom","We treated it as a funnel when it is also a cost."),
            ("A number we used","The 20 to 30 per cent taproom conversion has never been measured."),
            ("The census","Forty nine self selected people cannot carry a strategy on their own."),
            ("Your marketing lead","We called Harry by the wrong name in a hundred and sixty places.")],
      row_top=3.1, row_col=3.4),

 dict(type="divider", num="Part 02", title="What to do",
      strapline="Three moves, ranked. And one we have ranked below them."),

 dict(type="content", eyebrow="Move 01",
      headline="Buy the databases of people who\nalready own a system.",
      body="Harvey Norman lists six kegerator models plus a tap unit. Keg Land, Kegmaster and "
           "BenchTop hold buyer lists of their own. Every name on those lists owns hardware, so "
           "the price of the system, the most expensive objection your marketing fights, is "
           "already cleared. At about seventy dollars gross a keg, the data pays for itself "
           "quickly."),

 dict(type="content", eyebrow="Move 02",
      headline="Do a deal with Harvey Norman\ndirectly.",
      body="A QR code at the point of sale. A referral rebate on each keg. Or a free keg with "
           "purchase if the liquor rules allow it. Monk is one of their closest allies and holds "
           "point contacts. This is a conversation, not a campaign, and it is worth having "
           "before any budget moves."),

 dict(type="content", eyebrow="Move 03",
      headline="Go at the tour operators, and run\nwholesale properly.",
      body="Hop On, Urban Legends and Pineapple Tours all let the customer choose which "
           "breweries to visit. So your write up decides whether you get picked, and yours does "
           "not mention Midnight in Tokyo while Balter gets the imagery. On wholesale, one "
           "commercial account is worth about ten households, and it currently has no structure, "
           "no targets and nobody carrying it."),

 dict(type="content", eyebrow="And one we have ranked below them",
      headline="Pulling people into the taproom\nthrough social media.",
      body="That was close to the centre of the plan we wrote for you. On this read it should "
           "not be. If the taproom is the half that loses money, spending the marketing budget "
           "filling it is the wrong instinct, however good the content is."),

 dict(type="content", eyebrow="The opportunity nobody has worked",
      headline="Four in ten of your customers have\nquietly slowed down.",
      stats=[("10%","Buy about every month. Already at their ceiling"),
             ("60%","Buy about every three months. This is the core"),
             ("40%","Take longer than that. The system is still in the backyard"),
             ("1 in 3","Of your taps are not beer, which is the answer to this")],
      body="They have cut back on beer, not on thirst. A lighter or lower alcohol line puts "
           "something back in their taps without asking anyone to drink more. Where they are "
           "also members, they are paying for something they have stopped using."),

 dict(type="content", eyebrow="Your website",
      headline="Four business units, given equal\nbilling, and the award is buried.",
      rows=[("Above the fold","Nothing arresting. The film cuts too fast to read the message under it."),
            ("The award","Brewer's Choice at Crafted is not the first thing a visitor sees. It should be."),
            ("Fits any system","Your cheapest source of customers, and the site does not say it on arrival."),
            ("Reviews","Behind click dots that do not scroll, so nobody reaches them."),
            ("Wholesale","No margin argument, no white label, no cuisine matching. Nothing to say yes to.")],
      row_top=2.9, row_col=3.0, row_step=0.72),

 dict(type="content", eyebrow="What we need from you · six of eight decisions",
      headline="The six decisions that most change the plan.",
      rows=[("The taproom","Tasting and event venue, or keep paying for a drop in."),
            ("The range","Six core beers, or twenty seven taps."),
            ("Membership price","Two posters, two prices, both live in your venue today."),
            ("Active customer","Forty five, seventy five or ninety days. It decides every number we report."),
            ("Which plan is live","Three of your documents name three different core metrics."),
            ("Model A or B","Sell more systems, or convert the 116 who bought elsewhere."),
            ("Two more behind these","Whether cost is on the table at all, and the name against the signage.")],
      row_top=2.5, row_col=3.4, row_step=0.64),

 dict(type="content", eyebrow="How this splits",
      headline="Harry takes these. We would do these for you.",
      rows=[("Harry","Tour operator outreach. Fresh copy, photos, reviews and the award to each "
                     "operator. The referral reward nobody knows about."),
            ("Justin","The Harvey Norman conversation. Wholesale structure and targets. The six "
                      "decisions above."),
            ("Jewell","Database acquisition and the campaign against it. The Urban Legends "
                      "booking tool. Tracking, so you can see what any of it did.")],
      row_top=3.2, row_col=2.6),

 dict(type="closer",
      action="Decisions back by Friday 4 September. We will scope the three moves against them.",
      owner="Clent Jewell · clent@jewellprojects.com · Jewell Projects"),
]
