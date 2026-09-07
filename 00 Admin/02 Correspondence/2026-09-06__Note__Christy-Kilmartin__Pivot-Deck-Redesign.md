# Note to Christy — The Pivot, rebuilt in JP brand, and the event flyers

**Date** 6 September 2026
**From** Jewell Projects
**Re** Tap_That_The_Pivot.pptx, returned as JP_TapThat_ThePivot_v03.pptx
**Status** Draft. Not sent.

---

Hi Christy,

Deck's back, rebuilt in our brand rather than the default template it came in
on. Words are yours. The edits are listed at the bottom. And I had a go at the
event examples, which is the more interesting half of this.

## The brand split, because it is deliberate

**The deck is ours. The flyers are theirs.**

The deck is a Jewell Projects deliverable, so it is built to Brand Book Edition
02: Cream ground, Jewell Black type, Poppins, Signal Blue as the single accent
and used on exactly one slide. The five slide types and nothing else. No icons,
no accent bars, no decoration.

The flyers inside it stay in Tap That's green and gold, because they are Tap
That's collateral. Putting client artwork in our palette would make it useless
to them. Slide 12 says so on the slide.

## The flyers, and the better way you asked about

The reason no LLM nails a promotional flyer is that image models cannot set
type. Ask one for a whole flyer and you get a picture of a flyer, with
letterforms that look right until you read them. It will never be fixable,
because the words are pixels.

So split the job.

1. **The format is already Tap That's.** Site-visit photo 22 is their own
   in-venue flyer, "FUNCTIONS & KEG SYSTEM HIRE". Photo band up top with the
   headline over it, torn edge, badge on the seam, dark green ground, gold
   sub-heads, contact and QR at the foot. I copied it. The new flyers look like
   they came from the same place as the one already on their bar, because in
   format terms they did.

2. **The plates are commissioned, and there are two sets.** The set in the
   deck is generated concept photography: the keg on the reception table, the
   tasting paddle, the long table set up in the brewhouse, the fermenters.
   Product and room, no people, no set type, composed for the format. A second
   set built on August site-visit photography sits in
   `02 Design/03 Assets/event-flyers-venue/`.

   **Which set goes out matters.** Tap That's own guidelines (34, section 5)
   rule out anything that could not have been taken at Burleigh Heads. The
   generated set is the better-looking one and it is the right thing to show
   in a concept deck. If these become real venue marketing, either shoot the
   four frames properly or run the venue set. Do not let a generated plate go
   out labelled as their brewery.

3. **The type is set in code, so it is exact and it is editable.** Copy lives
   in `pivot/flyer_content.py`, separate from the layout. Change a headline,
   re-run, get a new A4 at 200 dpi. No re-prompting, no lottery.

4. **The typefaces are the ones the brand asks for.** Section 3 of the
   guidelines wants bold condensed sans headlines over a plain workhorse sans,
   and rules out scripts and serifs. Oswald over Barlow. Reference layouts of
   this kind usually set the sub-heads in a serif, because it photographs
   nicely. It is off-brand here, so the sub-heads are condensed sans and the
   warmth comes from the gold instead.

Four of them: weddings, bucks and hens, work functions, tours and tastings.
Print-ready A4 PNGs plus a combined PDF are in
`02 Design/03 Assets/event-flyers/`. Copy is a first pass and expects your edit.

One thing worth flagging on the originals. The two flyer artworks on the old
slide 6 were embedded as **EMF vector**. That renders in PowerPoint on Windows
and nowhere else. It comes up blank in Keynote, in Google Slides, in preview
thumbnails, and in any PDF export not made by PowerPoint itself. If those had
gone to Justin as a PDF he would have seen two empty pages. The replacements
are PNG.

## Type, and a warning about opening it

Two weights and nothing else. Poppins SemiBold carries every heading, figure
and label. Poppins Regular carries every line meant to be read as a sentence.
Light and Medium are gone from the deck entirely, so nothing can drift back to
a third weight on the next edit.

Everything now aligns hard to the one inch margin. The big type used to carry
small optical nudges, which meant three different left edges across the deck
depending on the slide. One margin, no exceptions.

**Poppins is not installed on most machines.** The deck names the font, it does
not carry it, so anything that does not have Poppins will substitute. WPS
Office picked a handwriting face. Three ways round it, in order of least
effort:

1. **Open it in Google Slides.** Drop the file into Google Drive, right click,
   Open with, Google Slides. Poppins is a Google font, so Slides serves it and
   the deck looks correct with nothing installed.
2. **Send the PDF.** Fonts are baked in. This is the right format for anything
   going to Justin that does not need editing.
3. **Install Poppins.** Free from Google Fonts. Needed on any machine that will
   edit the .pptx and see it properly.

## The photography

Eight of eighteen slides carry an image. The deck's own photography, meaning
the title, the four dividers and the evidence slide, is all August site visit.
The flyer plates on slides 12 and 13 are generated, and the slide says so.

Each of the four dividers is a room graded back almost to Jewell Black, so the
slide still reads as a word on black and the venue is just present behind it.
There is a new slide in Part 01, four photographs of what we actually walked
into: the tap wall, the price board, the tour poster already on the wall, the
referral sign already running. Captions state what is in the frame and nothing
that is not. The title slide is type on Cream, no image.

Everything is in the house grade, cool and desaturated, which is doing real work
here rather than styling for its own sake. The venue shoots warm under its own
festoon lighting and reads as a different brand entirely if you leave it alone.

## What the rebuild changed

The draft was eleven undifferentiated slides. It is now eighteen: a title,
four dividers, eleven content slides and a closer. Same argument, house
structure.

| Slide | Change | Why |
|---|---|---|
| all | Rebuilt into the five JP slide types | a JP deck has no sixth type |
| 03, 04 | Six findings split across two slides | the sixth ran off the bottom of the slide in the draft, and one idea per slide is the house rule |
| 09, 10 | The ten moves set as hairline tables | a content slide is never bulleted |
| 12 | Two EMF artworks replaced with four PNG flyers | EMF renders blank outside PowerPoint |
| 07 | Census stated as **49** people, not about 50 | the raw response file has 49 rows, and the sample size is the whole argument for treating it as colour rather than a map |
| 13 | The wireframe can and keg replaced with the flyer | it is the thing that would actually go out |
| 18 | Closer added | we close on the next action, never on the last content slide |
| 14 | Concept renders regridded to a true 16:9 with the caveat in its own column | they were being cover-cropped into a 2.8:1 letterbox that sliced the tops and bottoms off the units |

## Five phrases had to change

These are on the never-use list in our voice guide, so they could not survive
into a JP deck. Meaning is unchanged.

| Was | Now |
|---|---|
| Focus and shape is the **unlock** | Focus is the part that is missing |
| THE **ECOSYSTEM** EFFECT | THE COMPOUND EFFECT |
| **Passion** for brews is real | The interest in the brews is real |
| THE 4-STEP **JOURNEY** | The four steps |
| **leverage** social proof | carry social proof |

The build now fails if any of them come back, so a later copy edit cannot
reintroduce them by accident.

## Three for you

- **The closer needs a date.** It reads "Wording finalised with Christy, then
  this deck goes to Justin." I have not invented a date for that. Clent sets it
  before it goes.
- **Slide 14, the co-branded systems.** DeWalt, Ford Raptor and Harley marks on
  renders nobody has licensed, and no one has been approached. There is a line
  on the slide saying exactly that. Worth keeping for the reaction it gets in
  the room, worth not putting in anything that leaves it.
- **Slide 17.** I added "event flyer and campaign artwork, in the format shown"
  to the also-worth-adding column, on the basis that the flyers make the case
  themselves. Cut it if it reads as selling.

The Tap That branded version is still in the folder as
`TapThat_The-Pivot_v02.pptx` if you would rather present in the client's brand
than ours. Same content, same fixes.

Cheers,
Jewell Projects
