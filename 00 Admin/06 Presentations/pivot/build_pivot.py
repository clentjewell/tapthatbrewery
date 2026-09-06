"""Build Tap That -- The Pivot.

Prepares the image assets, hands the copy to build_pivot.js as JSON, and
renders the result to images so the deck can actually be looked at before it
goes anywhere.

    python3 build_pivot.py           # deck + QA renders
    python3 build_pivot.py --no-qa   # deck only
"""

import json
import os
import pathlib
import subprocess
import sys

from PIL import Image, ImageEnhance

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PHOTOS = ROOT / "01 Discover" / "01 Inputs" / "site-visit-photos"
BRAND = ROOT / "00 Admin" / "11 Final Outputs" / "brand-source"
FLYERS = ROOT / "02 Design" / "03 Assets" / "event-flyers"
CONCEPTS = ROOT / "02 Design" / "03 Assets" / "concept-renders"
DECK = ROOT / "00 Admin" / "06 Presentations" / "TapThat_The-Pivot_v02.pptx"
BUILD = HERE / "build"

NODE_MODULES = os.environ.get(
    "PIVOT_NODE_MODULES",
    "/tmp/claude-0/-home-user-tapthatbrewery/aff657a1-809f-5111-b96e-244c77408e59"
    "/scratchpad/pivot/node_modules",
)

sys.path.insert(0, str(HERE))
import pivot_content as PC  # noqa: E402

GREEN = (20, 54, 29)


def title_background():
    """The brewhouse, dropped back far enough to read type over it.

    Doing the darkening here rather than with a translucent shape on the slide
    keeps it out of Christy's way when she edits: one picture, no stack of
    overlays to select through.
    """
    out = BUILD / "title-bg.jpg"
    im = Image.open(PHOTOS / "14-taproom-interior-brewhouse.jpg").convert("RGB")
    target = 13.333 / 7.5
    w, h = im.size
    if w / h > target:
        nw = int(h * target)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / target)
        im = im.crop((0, int((h - nh) * 0.35), w, int((h - nh) * 0.35) + nh))
    im = im.resize((2400, 1350), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(0.35)
    im = ImageEnhance.Brightness(im).enhance(0.42)
    im = Image.blend(im, Image.new("RGB", im.size, GREEN), 0.58)
    im.save(out, "JPEG", quality=90)
    return out


def badge_on_green():
    """Flatten the transparent badge onto the slide green.

    PowerPoint renders the PNG alpha correctly, but flattening removes any
    chance of a halo when someone drags the badge onto a lighter panel later.
    """
    out = BUILD / "badge.png"
    im = Image.open(BRAND / "tapthat-logo-hires.png").convert("RGBA")
    bg = Image.new("RGBA", im.size, GREEN + (255,))
    bg.alpha_composite(im)
    bg.convert("RGB").save(out, "PNG")
    return out


def for_screen(src, out_name, px):
    """Downsample a print asset for use in the deck.

    The A4 flyers are 200 dpi because they have to print. Dropped into the deck
    at full size they made a 15MB file that no one can email, for detail no
    projector can show. The print-resolution originals stay where they are.
    """
    out = BUILD / out_name
    im = Image.open(src).convert("RGB")
    im = im.resize((px, round(px * im.height / im.width)), Image.LANCZOS)
    im.save(out, "JPEG", quality=88)
    return str(out)


def content_json():
    keys = ["TITLE", "SAW_HEARD", "VANITY", "CORE", "MORE", "FLYERS_SLIDE",
            "WEDDING", "CONCEPTS", "NOTES", "HOUSEKEEPING", "HELP"]
    data = {k: getattr(PC, k) for k in keys}
    data["_assets"] = {
        "titleBg": str(title_background()),
        "badge": str(badge_on_green()),
        "badgeAlpha": str(BRAND / "tapthat-logo-hires.png"),
    }
    names = ["01-weddings", "02-bucks-and-hens", "03-work-functions",
             "04-tours-and-tastings"]
    for n in names:
        if not (FLYERS / f"{n}.png").exists():
            sys.exit(f"missing flyer {n} -- run build_flyers.py first")
    # 2.9in wide on the slide, so 900px is already past what any projector
    # resolves, and 1200px covers the larger placement on slide 07.
    data["_assets"]["flyers"] = [
        for_screen(FLYERS / f"{n}.png", f"deck-{n}.jpg", 900) for n in names]
    data["_assets"]["flyerLarge"] = for_screen(
        FLYERS / "01-weddings.png", "deck-01-weddings-lg.jpg", 1200)
    data["_assets"]["concepts"] = {
        f.name: for_screen(f, f"deck-{f.stem}.jpg", 1100)
        for f in sorted(CONCEPTS.glob("*.png"))}
    p = BUILD / "content.json"
    p.write_text(json.dumps(data, indent=1))
    return p


def qa():
    """Render every slide to an image. LibreOffice needs libreoffice-impress;
    without it the convert fails with 'source file could not be loaded', which
    reads like a corrupt deck and is not one."""
    env = dict(os.environ, HOME="/tmp/lohome")
    r = subprocess.run(
        ["soffice", "--headless", "--norestore",
         "-env:UserInstallation=file:///tmp/louser-pivot",
         "--convert-to", "pdf", "--outdir", str(BUILD), str(DECK)],
        capture_output=True, text=True, env=env)
    pdf = BUILD / (DECK.stem + ".pdf")
    if not pdf.exists():
        print(r.stdout, r.stderr)
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
    r = subprocess.run(["node", str(HERE / "build_pivot.js"), str(cj), str(DECK)],
                       capture_output=True, text=True, env=env,
                       cwd=str(pathlib.Path(NODE_MODULES).parent))
    print(r.stdout, r.stderr, sep="")
    if r.returncode:
        sys.exit(r.returncode)
    if "--no-qa" not in sys.argv:
        qa()


if __name__ == "__main__":
    main()
