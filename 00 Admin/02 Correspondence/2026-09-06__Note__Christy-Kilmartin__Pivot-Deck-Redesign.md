# Note to Christy — The Pivot, design pass and the event flyers

**Date** 6 September 2026
**From** Jewell Projects
**Re** Tap_That_The_Pivot.pptx, returned as TapThat_The-Pivot_v02.pptx
**Status** Draft. Not sent.

---

Hi Christy,

Deck's back, restyled to Tap That's own brand rather than the default template.
Words are yours; I have only changed three things and they are listed at the
bottom. And I had a go at the event examples, which is the more interesting
half of this.

## The flyers, and the better way you asked about

The reason no LLM nails a promotional flyer is that image models cannot set
type. Ask one for a whole flyer and you get a picture of a flyer, with
letterforms that look right until you read them. It will never be fixable,
because the words are pixels.

So split the job. The photograph is a photograph, and the layout is a layout:

1. **The format is already Tap That's.** Site-visit photo 22 is their own
   in-venue flyer, "FUNCTIONS & KEG SYSTEM HIRE". Photo band up top with the
   headline over it, torn edge, badge on the seam, dark green ground, gold
   sub-heads, contact and QR at the foot. I copied it. It means the new flyers
   look like they came from the same place as the one already sitting on their
   bar, because in format terms they did.

2. **The imagery is real, and it is theirs.** All four use August site-visit
   photography: the tap wall twice, the bar, the brewhouse. Nothing generated,
   no stock. Their own brand guidelines rule stock models out anyway, and the
   venue is a better hero than a stock couple laughing at a beer — the venue is
   the thing being hired.

3. **The type is set in code, so it is exact and it is editable.** Copy lives
   in `pivot/flyer_content.py`, separate from the layout. Change a headline,
   re-run, get a new A4 at 200 dpi. No re-prompting, no lottery.

Four of them: weddings, bucks and hens, work functions, tours and tastings.
Print-ready A4 PNGs plus a combined PDF are in
`02 Design/03 Assets/event-flyers/`. Copy is a first pass and expects your edit.

One thing worth flagging on the originals. The two flyer artworks on the old
slide 6 were embedded as **EMF vector**. That renders in PowerPoint on Windows
and nowhere else — it comes up blank in Keynote, in Google Slides, in preview
thumbnails, and in any PDF export not made by PowerPoint itself. If those had
gone to Justin as a PDF he would have seen two empty pages. The replacements
are PNG.

## The design pass

Brand is Tap That's, taken from the badge artwork and documented in
`34 Brand Guidelines`: brewery green **#14361D** as the ground on every slide,
gold **#CE9A49** as the only accent, off-white for reading. Green leads and gold
never does, which is their rule, not mine. The badge hexagon is the one repeated
device — it numbers the six findings, the ten moves, the four journey steps and
nothing else.

Type is **Arial Narrow** over **Arial**. The guidelines call for bold condensed
caps in headlines and Arial Narrow is the only genuinely condensed face that
ships with Office on both Windows and Mac, so it opens correctly on your machine
and on Justin's rather than substituting to something round.

Also fixed while I was in there:

- Slide 2's sixth finding ran about 0.4in off the bottom of the slide in the
  draft. It is now two columns of three, and nothing is cut off.
- Slide 7's left column was a wireframe of a can and a keg with a drawn-on QR
  code. It is now the wedding flyer itself, which is the thing that would
  actually go out.
- The deck was going to be 15MB with print-resolution flyers in it. Screen
  copies are used on the slides and the print originals kept separately, so it
  is 3MB and emailable.
- Every slide has been rendered and looked at. Nothing overflows.

## The three content changes

| Slide | Change | Why |
|---|---|---|
| 02 | Six findings split into two columns of three | the sixth was off the slide |
| 06 | Two EMF artworks replaced with four PNG flyers | EMF renders blank outside PowerPoint |
| 09 | Census stated as **49** people, not ~50 | the raw response file has 49 rows, and the sample size is the whole argument for treating it as colour rather than a map |

Everything else is your wording, moved but not rewritten.

## Two for you to decide

- **Slide 8, the co-branded systems.** DeWalt, Ford Raptor and Harley marks are
  on renders nobody has licensed and no one has been approached. I have put a
  line on the slide saying exactly that. Worth keeping for the reaction it gets
  in the room, worth not putting in anything that leaves it.
- **Slide 11.** I added "event flyer and campaign artwork, in the format shown"
  to the also-worth-adding column, on the basis that the flyers make the case
  themselves. Cut it if it reads as selling.

Cheers,
Jewell Projects
