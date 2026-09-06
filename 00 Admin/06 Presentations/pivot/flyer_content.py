"""Copy for the four event flyers on slide 06 of The Pivot.

Kept apart from the renderer so Christy can rewrite the words without
touching layout code. Every claim here is either already on Tap That's own
in-venue collateral or comes out of the Discover pack.
"""

# Voice notes, per 34 Brand Guidelines section 4:
#   puns for names and moments, plain talk for money, service and responsibility.
#   Australian, first-person plural, talks with drinkers not at them.

CONTACT = "cheers@tapthatbrewery.com.au"
SITE = "https://tapthatbrewery.com.au/"

FLYERS = [
    {
        "slug": "01-weddings",
        # Real venue photography only -- 34 Brand Guidelines section 5 rules
        # out stock models and studio gloss.
        "photo": "04-tap-wall-left-craft-range.jpg",
        "kicker": "WEDDINGS AT TAP THAT",
        "head": ["A BEER WITH", "YOUR NAMES ON IT"],
        "gold_word": "YOUR NAMES",
        "blocks": [
            {
                "title": "Brew it together",
                "body": "Come in for a tasting, blend it your way, name it, "
                        "put your own label on it. One session, one beer that "
                        "is nobody else's.",
            },
            {
                "title": "Pour it on the day",
                "body": "We deliver it to your reception in 20L kegs or "
                        "500ml cans. Your beer, your names, on tap in front "
                        "of everyone you invited.",
            },
        ],
        "strap": "Every guest goes home with one.",
        "cta": "Talk to us about a wedding brew",
    },
    {
        "slug": "02-bucks-and-hens",
        "photo": "05-tap-wall-right-rtds-seltzers.jpg",
        "kicker": "BUCKS & HENS AT TAP THAT",
        "head": ["THE LAST ROUND", "BEFORE THE BIG ONE"],
        "gold_word": "THE BIG ONE",
        "blocks": [
            {
                "title": "The room is yours",
                "body": "A private session across 27 taps. Beer, sours, "
                        "seltzers and RTD spirits, so nobody in the group is "
                        "stuck drinking something they don't like.",
            },
            {
                "title": "Blend your own",
                "body": "Guided flight tasting, then everyone has a go at "
                        "building the brew. Winner gets their name on the "
                        "label.",
            },
        ],
        "strap": "Then we kegged it for the wedding.",
        "cta": "Book a bucks or hens session",
    },
    {
        "slug": "03-work-functions",
        "photo": "20-taproom-bar-merch-wall.jpg",
        "kicker": "WORK FUNCTIONS AT TAP THAT",
        "head": ["THE WORK DO,", "DONE PROPERLY"],
        "gold_word": "DONE PROPERLY",
        "blocks": [
            {
                "title": "Book the mezzanine or the lot",
                "body": "Christmas parties, end of financial year, team "
                        "nights, client events. Drinks packages sorted, "
                        "Ammazza pizza on the menu.",
            },
            {
                "title": "Or we bring the pub to you",
                "body": "Hire a Tap That keg system filled with whatever "
                        "your team actually drinks, and run it at your own "
                        "place.",
            },
        ],
        "strap": "A working brewery beats a function room.",
        "cta": "Ask us about venue hire",
    },
    {
        "slug": "04-tours-and-tastings",
        "photo": "14-taproom-interior-brewhouse.jpg",
        "kicker": "TOURS & TASTINGS AT TAP THAT",
        "head": ["STAND IN THE", "BREWHOUSE"],
        "gold_word": "BREWHOUSE",
        "blocks": [
            {
                "title": "Not a tasting room. The brewery.",
                "body": "The fermenters are right there. You taste what came "
                        "out of them, standing next to them, with the head "
                        "brewer telling you how it got there.",
            },
            {
                "title": "Paddle, flight or full tour",
                "body": "Tasting paddle from $18. Group tours by "
                        "arrangement, and we work with the Gold Coast "
                        "brewery tour operators.",
            },
        ],
        "strap": "Crafted Brewers' Choice award winner.",
        "cta": "Book a tour or a tasting",
    },
]
