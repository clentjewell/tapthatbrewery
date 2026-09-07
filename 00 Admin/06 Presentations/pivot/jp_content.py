"""Words for JP_TapThat_ThePivot_v03.

Christy's draft, restructured into the five JP slide types and put through the
house voice. Three of her phrases are on the never-use list in
jp-brand-presentation/references/voice-and-vocabulary.md and had to change;
they are recorded in VOICE_EDITS so nothing looks like it went missing.

British English. No em dashes. No exclamation marks. Never bullet a content
slide, so the lists in the draft are hairline-ruled rows and tables instead.
"""

VOICE_EDITS = [
    ("unlock", "Focus and shape is the unlock",
     "The overall plan is sound. Focus is the part that is missing."),
    ("ecosystem", "THE ECOSYSTEM EFFECT", "THE COMPOUND EFFECT"),
    ("passion", "Passion for brews is real",
     "The interest in the brews is real"),
    ("journey", "THE 4-STEP JOURNEY", "The four steps"),
    ("leverage", "leverage social proof", "carry social proof"),
]

CHANGES = [
    ("all", "Rebuilt into the five JP slide types",
     "11 undifferentiated slides became a title, four dividers, ten content "
     "slides and a closer"),
    ("03, 04", "Six findings split across two slides",
     "the sixth ran off the bottom of the slide in the draft, and one idea per "
     "slide is the house rule"),
    ("08, 09", "The ten moves set as hairline tables",
     "a JP content slide is never bulleted"),
    ("11", "Two EMF flyer artworks replaced with four PNG flyers",
     "EMF renders blank outside PowerPoint on Windows"),
    ("06", "Census sample stated as 49, not about 50",
     "the raw response file has 49 rows, and the sample size is the argument"),
    ("17", "Closer added",
     "a JP deck closes on the next action, never on the last content slide"),
]

TITLE = {
    "topbar": "JP · TAP THAT · THE PIVOT",
    "title": "The Pivot",
    "sub": "From vanity to sanity. A strategic evolution, not a rebrand.",
    "date": "6 September 2026",
}

DIVIDERS = {
    "context": ("PART 01", "Context.",
                "What the numbers and the site visit actually say."),
    "direction": ("PART 02", "Direction.",
                  "Ten moves. Five of them come first."),
    "collateral": ("PART 03", "Collateral.",
                   "What the destination business looks like on paper."),
    "execution": ("PART 04", "Execution.",
                  "The small fixes, and where we can help."),
}

# ------------------------------------------------------------ slides 03, 04
FINDINGS_A = {
    "eyebrow": "PART 01 · CONTEXT",
    "head": "The overall plan is sound. Focus is the part that is missing.",
    "items": [
        ("01", "The strategy is sound. The shape is not.",
         "Comprehensive, and Justin's mental model that everything feeds "
         "refills is right. But it reads as AI theoretical. Too much "
         "equivalence, too many directions, and its own best insights are "
         "buried."),
        ("02", "Two business units cancelling each other out.",
         "Thought to be complementary, in reality pulling opposite ways. A "
         "good refill business takes traffic out of the Tap Room, which means "
         "more spend to replace it at a high cost per customer."),
        ("03", "The weakest unit is getting the support.",
         "Refills are at MVP, and only refills, and only beer. Marketing's "
         "time goes to propping up the unit that does not work, at the cost "
         "of the ones that do."),
    ],
}

FINDINGS_B = {
    "eyebrow": "PART 01 · CONTEXT",
    "head": "Three more, and the last one is the reason to move now.",
    "items": [
        ("04", "The offer is good. The stars cannot shine.",
         "We suspect a long tail of beer options is driving cost of goods. We "
         "also think it is causing choice paralysis at the point of sale."),
        ("05", "Chasing two rabbits, catching neither.",
         "For all the right reasons, marketing explores an idea, quits, and "
         "moves on. Nothing gets the run it needs to prove itself either way."),
        ("06", "In danger of dying with a beautiful corpse.",
         "Running a brewery is hard. Hospitality is harder. Both on a skeleton "
         "staff is unreasonable. Permission is needed to reshape the "
         "business."),
    ],
}

# ------------------------------------------------------------------ slide 05
# Documentary evidence, not decoration. Every caption states what is in the
# photograph and nothing that is not.
EVIDENCE = {
    "eyebrow": "PART 01 · CONTEXT",
    "head": "The room the strategy has to work in.",
    "shots": [
        ("04-tap-wall-left-craft-range.jpg",
         "27 taps, and a third of them are not beer"),
        ("03-taproom-price-board.jpg",
         "The price board, as it stands"),
        ("26-hop-on-brewery-tours-poster.jpg",
         "The tour circuit already comes past"),
        ("17-corny-keg-referral-rewards-sign.jpg",
         "Referral rewards, already running"),
    ],
    "foot": "Site visit, August 2026. Twenty-seven photographs on file.",
}

# ------------------------------------------------------------------ slide 06
NUMBERS = {
    "eyebrow": "PART 01 · CONTEXT",
    "head": "Tap Room is vanity. Refills are sanity.",
    "stats": [
        ("96-113", "Active refill customers, ordering repeatedly. That is MVP "
                   "status, and it was reached without a push."),
        ("56%", "of refill customers bought their tap system somewhere else. "
                "The refill proposition is already validated."),
        ("20%", "of system buyers are said to have visited the Tap Room. That "
                "is correlation, not proven causation."),
    ],
    "foot": "The Tap Room works as an event and function destination. It does "
            "not work as a walk-in, because the footfall is not there. The "
            "task now is to edit the losers hard and invest in what is proven.",
}

# ------------------------------------------------------------------ slide 06
CAUTIONS = {
    "eyebrow": "PART 01 · CONTEXT",
    "head": "Two things to hold on to before anything is decided.",
    "cols": [
        ("Who is the real enemy?",
         "Overpriced pubs. Not the duopoly, not A&A, not the keg delivery "
         "operators. Speak in unit economics everywhere, and do not get pulled "
         "into a keg price war you do not need to fight."),
        ("Handle the census with care",
         "49 people, forced-choice answers. People do not always know, or say, "
         "why they buy. Status, wanting to be seen as successful, compensating "
         "for something else. Real drivers, rarely spoken. Useful colour. Not "
         "a strategy map."),
    ],
}

# ------------------------------------------------------------ slides 08, 09
CORE = {
    "eyebrow": "PART 02 · DIRECTION",
    "head": "Get the core right, then go for more.",
    "cols": ["MOVE", "THE SHIFT", "PROOF", "FIRST STEPS"],
    "rows": [
        ("01  Tap Room: pause and pivot",
         "Pause walk-in trading. Go all in on destination demand.",
         "Event and function nights are already profitable.",
         "PR to tourism, event and wedding planners. Own the tour circuit: "
         "Urban Legends booking tool, Pineapple Tours, the Crafted award. "
         "Ticketed events and collabs. Party rental, with minimum-guarantee "
         "kegs covering the rental cost."),
        ("02  Convert the owners already sold",
         "Objections are already overcome for existing kegerator owners.",
         "56% bought their system elsewhere.",
         "Harvey Norman gift-with-purchase and point-of-sale tie-up, plus the "
         "buyer database. Buy Kegland and corny keg owner databases. Official "
         "Benchy partnership. Co-branded outdoor BBQ and system bundle."),
        ("03  Remove all friction in refills",
         "Every extra step in the refill process costs a sale.",
         "10% reorder monthly, 40% far later. One clock fails both.",
         "Free delivery always works, and margin comes back in dollars, not "
         "percent. Replace the blanket 90-day SMS with consumption-triggered "
         "reminders. Lead on no CO2, pick up and go. Simplify membership. Get "
         "Justin off the bar and onto the road."),
        ("04  Rationalise the range",
         "Create hero products that carry social proof, and cut the "
         "non-productive tail.",
         "About 19 brew choices loses both curation and best-in-class.",
         "Deeper product marketing on the brews that remain. Social proof cues "
         "such as most popular. Free the shelf space and the brewing time for "
         "the heroes."),
        ("05  Ride the wellness wave",
         "Also the way back to lapsed customers.",
         "40% of lapsed customers cite cutting back.",
         "Low, non-alcoholic, low-carb and protein range. Wellness influencer "
         "collabs, amplify or co-develop. Reframe for the cutting-back cohort "
         "as a healthier alternative, not less beer."),
    ],
}

MORE = {
    "eyebrow": "PART 02 · DIRECTION",
    "head": "Once the core is running, extend it.",
    "cols": ["MOVE", "THE SHIFT", "PROOF", "FIRST STEPS"],
    "rows": [
        ("06  Full press on wholesale",
         "Resourced, structured and measured. No more falling through the "
         "cracks.",
         "One wholesale account is worth about ten households.",
         "Hire a full-timer or an agent. Set targets and KPIs. Custom systems "
         "for sporting clubs, with minimum-guarantee kegs per season. Move "
         "rigs from footy to cricket for year-round occupancy."),
        ("07  Design for her",
         "Covered is not the same as catered for.",
         "The interest in the brews is real. The range does not reflect it.",
         "Romance the RTD properly. Build the hydration story through the "
         "wellness and light range. Products she is proud to serve. Systems "
         "designed to sit in eyesight at home."),
        ("08  Personalise comms and lifetime value",
         "This needs a process, not a message.",
         "Buying cycle: about 60% within three months, 40% longer.",
         "Track consumption to predict the next refill. Re-engage lapsed "
         "customers by actual reason, cutting back versus forgot. "
         "Trigger-based outreach, not calendar-based. Personal details: "
         "anniversaries, footy finals."),
        ("09  Make the kegerator worth writing about",
         "Turn the system itself into demand.",
         "1,000 giveaway entries is proven demand.",
         "User-generated content mechanic: tag Tap That, get a discount. Own "
         "your keg personalisation, like a whisky bottle. Explore short-term "
         "and occasion rental for parties."),
        ("10  Package around the duopoly",
         "Locked-in venues still have real pain points.",
         "Contractual lock-in is not the same as satisfaction.",
         "A packaged offer that works around existing contracts. Find the judo "
         "move that uses their size against them: no lock-in, profit share, "
         "white labelling."),
    ],
}

# ------------------------------------------------------------------ slide 11
FLYERS_SLIDE = {
    "eyebrow": "PART 03 · COLLATERAL",
    "head": "The destination business, sold the way the venue already sells it.",
    "body": "Format taken from Tap That's own in-venue flyer. The plates are "
            "commissioned concept photography: product and room, no people, no "
            "set type. A second set built on August site-visit photography is "
            "in the folder, for anything that goes out as their own marketing. "
            "These sit in Tap That's brand, not ours, because they are the "
            "client's collateral. Print-ready A4 at 200 dpi.",
    "captions": ["Weddings", "Bucks and hens", "Work functions",
                 "Tours and tastings"],
}

# ------------------------------------------------------------------ slide 12
WEDDING = {
    "eyebrow": "PART 03 · COLLATERAL",
    "head": "Turning hens and bucks days into wedding day volume.",
    "body": "One private session captures premium venue hire upfront, secures "
            "pre-sold volume for the reception, and puts branded product into "
            "the hands of every guest.",
    "steps": [
        ("01", "The Tap Room event",
         "Private hens or bucks session. Guided flight tasting across 27 taps, "
         "with interactive ingredient blending."),
        ("02", "Bespoke branding",
         "Co-branded custom label, naming, and beverage style selection: beer, "
         "sour, seltzer or RTD spirit."),
        ("03", "Wedding day reception",
         "Bulk supply delivered in 20L kegs or custom cans for the main event."),
        ("04", "Take-home compound",
         "Every guest goes home with a branded sample and a QR code."),
    ],
    "strap": "THE COMPOUND EFFECT",
    "strapbody": "Every wedding is a self-funding activation that reaches 100 "
                 "or more targeted consumers.",
}

# ------------------------------------------------------------------ slide 13
CONCEPTS = {
    "eyebrow": "PART 03 · COLLATERAL",
    "head": "What a co-branded system could look like.",
    "body": "Concept renders for discussion. No approach has been made to any "
            "brand shown, and none of these marks are licensed. Worth showing "
            "for the reaction. Not for anything that leaves the room.",
    "images": [
        ("dewalt-collab.png", "Trade and worksite"),
        ("raptor-collab.png", "Four-wheel drive and touring"),
        ("harley-collab.png", "Motorcycle clubs"),
        ("tap-truck.png", "Mobile bar for events"),
    ],
}

# ------------------------------------------------------------------ slide 15
HOUSEKEEPING = {
    "eyebrow": "PART 04 · EXECUTION",
    "head": "Small fixes, disproportionate impact.",
    "rows": [
        ("Above the fold",
         "No hook, background film cut too fast to read, copy pollution, "
         "low-resolution static logo."),
        ("Missing proof",
         "The Crafted Brewers' Choice award, the fits-any-system callout and "
         "strong reviews are all buried below the fold."),
        ("Hierarchy",
         "Four business units treated equally. Prioritise the moments that "
         "matter: family, friends, the proud provider role."),
        ("Category",
         "Commercial brewer invites mainstream price and product comparisons. "
         "It needs an elevated category name of its own."),
        ("Channel language",
         "Wholesale should speak directly to restaurants and sporting clubs. "
         "Cuisine matching, club-branded kegs, straight to the margin story."),
    ],
}

# ------------------------------------------------------------------ slide 16
HELP = {
    "eyebrow": "PART 04 · EXECUTION",
    "head": "What we can pick up from here.",
    "cols": [
        ("FROM THE BRIEF", [
            "Website design optimisation",
            "SEO and GEO best-practice implementation",
            "PR outreach to tourism operators and experiential platforms",
            "Influencer outreach",
            "Partnerships outreach and project management",
            "Urban Legends collaborative booking tool",
        ]),
        ("ALSO WORTH ADDING", [
            "Trigger-based CRM and lifecycle build, which fixes the 90-day "
            "SMS problem",
            "Membership programme redesign",
            "Wholesale structure and KPI framework",
            "Event flyer and campaign artwork, in the format shown",
        ]),
    ],
}

# ------------------------------------------------------------------ slide 17
CLOSER = {
    "word": "Next.",
    # No invented date. The action is real; the date is Clent's to set before
    # this goes to Justin.
    "line1": "Wording finalised with Christy, then this deck goes to Justin.",
    "line2": "Clent Jewell · clent@jewellprojects.com",
}
