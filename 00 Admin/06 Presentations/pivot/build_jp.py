"""Build JP_TapThat_ThePivot_v03, the Jewell Projects branded deck.

Same content as the Tap That branded v02, rebuilt to jp-brand-presentation.
Prepares screen copies of the artwork, hands the copy to build_jp.js, renders
every slide, and refuses to finish if a word from the never-use list survived.

    python3 build_jp.py            # deck + QA renders + vocabulary check
    python3 build_jp.py --no-qa    # deck only
"""

import json
import os
import pathlib
import re
import subprocess
import sys

from PIL import Image, ImageEnhance, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PHOTOS = ROOT / "01 Discover" / "01 Inputs" / "site-visit-photos"
FLYERS = ROOT / "02 Design" / "03 Assets" / "event-flyers"
CONCEPTS = ROOT / "02 Design" / "03 Assets" / "concept-renders"
DECK = ROOT / "00 Admin" / "06 Presentations" / "JP_TapThat_ThePivot_v03.pptx"
BUILD = HERE / "build-jp"

NODE_MODULES = os.environ.get(
    "PIVOT_NODE_MODULES",
    "/tmp/claude-0/-home-user-tapthatbrewery/aff657a1-809f-5111-b96e-244c77408e59"
    "/scratchpad/pivot/node_modules",
)

sys.path.insert(0, str(HERE))
import jp_content as JP  # noqa: E402

# jp-brand-presentation/references/voice-and-vocabulary.md, "NEVER use these".
# "honest" is on the list as honest/honestly, so it is matched as a whole word.
FORBIDDEN = [
    "synergise", "disrupt", "innovative", "cutting-edge", "game-changing",
    "world-class", "holistic", "leverage", "utilise", "seamlessly", "honest",
    "honestly", "passion", "ecosystem", "journey", "magic", "unlock", "ninja",
    "rockstar", "deep dive", "circle back", "thought leader",
]


POPPINS_MED = "/usr/share/fonts/truetype/poppins/Poppins-500.ttf"


def head_lines(text, pt=42, width_in=11.333):
    """How many lines a 42pt headline actually takes.

    Guessing this wrong is what pushed two-line headlines through the first
    row of content on half the slides, so it is measured against the real
    Poppins metrics rather than an average character width.
    """
    try:
        font = ImageFont.truetype(POPPINS_MED, round(pt * 96 / 72))
    except OSError:                      # Poppins not installed on this box
        return 2 if len(text) > 48 else 1
    limit = width_in * 96
    lines, cur = 1, ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if font.getlength(trial) <= limit:
            cur = trial
        else:
            lines += 1
            cur = word
    return lines


# jp-brand-presentation imagery direction: real rooms, available daylight,
# documentary over editorial, cool and slightly desaturated. The venue shoots
# warm under its own festoon lighting, so the grade is doing real work here,
# not styling for its own sake.
COOL = (74, 84, 98)


def graded(src, out_name, aspect, darken=1.0, tint=0.10, crop_bias=0.4,
           px=1800):
    """Crop to an aspect, then put the photograph into the JP grade.

    crop_bias applies on whichever axis is being trimmed, so a landscape frame
    cropped to portrait keeps the part of the room worth keeping.
    """
    im = Image.open(PHOTOS / src).convert("RGB")
    w, h = im.size
    if w / h > aspect:
        nw = int(h * aspect)
        left = int((w - nw) * crop_bias)
        im = im.crop((left, 0, left + nw, h))
    else:
        nh = int(w / aspect)
        top = int((h - nh) * crop_bias)
        im = im.crop((0, top, w, top + nh))
    im = im.resize((px, round(px / aspect)), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(0.34)
    im = Image.blend(im, Image.new("RGB", im.size, COOL), tint)
    if darken != 1.0:
        im = ImageEnhance.Brightness(im).enhance(darken)
    out = BUILD / out_name
    im.save(out, "JPEG", quality=88)
    return str(out)


# Where the divider's type sits, as a fraction of the plate. The scrim and the
# legibility check both work against this box rather than the whole frame.
TYPE_ZONE = (0.0, 0.26, 0.64, 0.76)


def divider_plate(src, out_name, crop_bias=0.35):
    """A divider photograph, taken down until Cream at 120pt is unmissable.

    A flat brightness cut is not enough. A busy frame like the coolroom board
    stays legible as a board and fights the word sitting on it, so the plate
    also gets a scrim that runs dark on the left, where the type is, and opens
    up on the right. Then the type zone's mean luminance is measured and the
    whole plate is scaled until it passes. Eyeballing this is what let the
    Execution divider through the first time.
    """
    path = graded(src, out_name, 13.333 / 7.5, darken=0.34, tint=0.16,
                  crop_bias=crop_bias, px=2000)
    im = Image.open(path).convert("RGB")
    w, h = im.size

    # Horizontal scrim: 0.16 at the left edge, easing to 1.0 by 92% across.
    ramp = Image.linear_gradient("L").rotate(-90, expand=True).resize((w, h))
    scrim = ramp.point(lambda v: round(255 * min(0.70, 0.14 + 0.72 * max(
        0.0, (v / 255 - 0.28) / 0.64) ** 1.5)))
    im = Image.composite(im, Image.new("RGB", (w, h), (0, 0, 0)), scrim)

    x0, y0, x1, y1 = TYPE_ZONE
    for _ in range(6):
        zone = im.convert("L").crop((int(x0 * w), int(y0 * h),
                                     int(x1 * w), int(y1 * h)))
        mean = sum(i * n for i, n in enumerate(zone.histogram())) / (
            zone.width * zone.height)
        if mean <= 26:
            break
        im = ImageEnhance.Brightness(im).enhance(max(0.5, 26 / mean))
    im.save(path, "JPEG", quality=88)
    return path


def for_screen(src, out_name, px):
    """Downsample print artwork for the deck. Originals stay at 200 dpi."""
    out = BUILD / out_name
    im = Image.open(src).convert("RGB")
    im = im.resize((px, round(px * im.height / im.width)), Image.LANCZOS)
    im.save(out, "JPEG", quality=88)
    return str(out)


def content_json():
    keys = ["TITLE", "DIVIDERS", "FINDINGS_A", "FINDINGS_B", "EVIDENCE",
            "NUMBERS", "CAUTIONS", "CORE", "MORE", "FLYERS_SLIDE", "WEDDING",
            "CONCEPTS", "HOUSEKEEPING", "HELP", "CLOSER"]
    data = {k: getattr(JP, k) for k in keys}
    # Every content slide lays itself out below its own headline.
    for v in data.values():
        if isinstance(v, dict) and "head" in v:
            v["headLines"] = head_lines(v["head"])
    names = ["01-weddings", "02-bucks-and-hens", "03-work-functions",
             "04-tours-and-tastings"]
    for n in names:
        if not (FLYERS / f"{n}.png").exists():
            sys.exit(f"missing flyer {n} -- run build_flyers.py first")
    data["_assets"] = {
        "flyers": [for_screen(FLYERS / f"{n}.png", f"jp-{n}.jpg", 800)
                   for n in names],
        "flyerLarge": for_screen(FLYERS / "01-weddings.png",
                                 "jp-01-weddings-lg.jpg", 1100),
        "concepts": {f.name: for_screen(f, f"jp-{f.stem}.jpg", 1100)
                     for f in sorted(CONCEPTS.glob("*.png"))},
        "dividerPhotos": {
            "context": divider_plate("16-beer-menu-screen-abv-prices.jpg",
                                     "jp-div-context.jpg"),
            "direction": divider_plate("05-tap-wall-right-rtds-seltzers.jpg",
                                       "jp-div-direction.jpg"),
            "collateral": divider_plate("20-taproom-bar-merch-wall.jpg",
                                        "jp-div-collateral.jpg"),
            "execution": divider_plate("18-coolroom-kegged-and-ready-board.jpg",
                                       "jp-div-execution.jpg"),
        },
        "evidence": [graded(src, f"jp-ev-{i}.jpg", 4 / 5, darken=0.96,
                            crop_bias=bias, px=900)
                     for i, ((src, _), bias) in enumerate(
                         zip(JP.EVIDENCE["shots"], (0.28, 0.5, 0.5, 0.5)))],
    }
    p = BUILD / "content.json"
    p.write_text(json.dumps(data, indent=1))
    return p


def check_voice():
    """House-voice gate. Cheap to run, and the words are easy to reintroduce
    on the next copy edit."""
    from pptx import Presentation
    blob = "\n".join(
        sh.text_frame.text
        for s in Presentation(str(DECK)).slides for sh in s.shapes
        if sh.has_text_frame)
    for tbl in Presentation(str(DECK)).slides:
        for sh in tbl.shapes:
            if sh.has_table:
                blob += "\n" + "\n".join(c.text for r in sh.table.rows
                                         for c in r.cells)
    bad = sorted({w for w in FORBIDDEN
                  if re.search(rf"\b{re.escape(w)}\b", blob, re.I)})
    if bad:
        sys.exit("never-use words on the slides: " + ", ".join(bad))
    if "—" in blob:
        sys.exit("em dash on a slide; JP copy uses periods and commas")
    if "!" in blob:
        sys.exit("exclamation mark on a slide")
    print("voice check clean")


def qa():
    env = dict(os.environ, HOME="/tmp/lohome")
    subprocess.run(
        ["soffice", "--headless", "--norestore",
         "-env:UserInstallation=file:///tmp/louser-jp",
         "--convert-to", "pdf", "--outdir", str(BUILD), str(DECK)],
        capture_output=True, text=True, env=env)
    pdf = BUILD / (DECK.stem + ".pdf")
    if not pdf.exists():
        sys.exit("could not render the deck for QA "
                 "(apt-get install libreoffice-impress)")
    for old in BUILD.glob("slide-*.jpg"):
        old.unlink()
    subprocess.run(["pdftoppm", "-jpeg", "-r", "110", str(pdf),
                    str(BUILD / "slide")], check=True)
    print("QA renders in", BUILD)


def main():
    BUILD.mkdir(exist_ok=True)
    cj = content_json()
    env = dict(os.environ, NODE_PATH=NODE_MODULES)
    r = subprocess.run(["node", str(HERE / "build_jp.js"), str(cj), str(DECK)],
                       capture_output=True, text=True, env=env,
                       cwd=str(pathlib.Path(NODE_MODULES).parent))
    print(r.stdout, r.stderr, sep="")
    if r.returncode:
        sys.exit(r.returncode)
    check_voice()
    if "--no-qa" not in sys.argv:
        qa()


if __name__ == "__main__":
    main()
