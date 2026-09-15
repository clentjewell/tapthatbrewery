"""Pull the plan sheets' content out of the A3 fragments as structured JSON.

The PowerPoint version has to carry exactly the same words as the A3 sheets.
Retyping them into a second file is how the two drift apart, and this pack has
been bitten by hand-authored copies of generated content more than once. So the
HTML fragments stay the single source of truth and the deck is built from what
this reads out of them.

Layout is not extracted. Grid positions live in oap-plan.css for the sheets and
in build_plan_pptx.js for the deck, because those are genuinely two different
media and a shared position map would fit neither.

    python3 plan_extract.py > build-plan/content.json
"""

import json
import pathlib
import sys

from lxml import html as LH

HERE = pathlib.Path(__file__).resolve().parent
FRAGS = [
    ("summary", "summary.html"),
    ("business", "business.html"),
    ("brand", "brand.html"),
    ("sales", "sales.html"),
    ("activation", "activation.html"),
]


def runs(el):
    """Flatten an element's inline content into bold / plain runs.

    Whitespace between runs matters. "<strong>First step:</strong> Justin"
    has its space in the tail of the strong, and normalising each run on its
    own throws it away, which is how the first deck printed "First step:Justin".
    """
    out = []

    def push(text, bold):
        if not text:
            return
        lead, trail = text[:1].isspace(), text[-1:].isspace()
        t = " ".join(text.split())
        if not t:                                # pure whitespace between tags
            if out and not out[-1]["t"].endswith(" "):
                out[-1]["t"] += " "
            return
        if lead and out and not out[-1]["t"].endswith(" "):
            out[-1]["t"] += " "
        if out and out[-1]["b"] == bold:
            out[-1]["t"] += t
        else:
            out.append({"t": t, "b": bold})
        if trail:
            out[-1]["t"] += " "

    push(el.text, False)
    for child in el:
        if child.tag == "br":                # a real line break, not a space
            out.append({"t": "", "b": False, "br": True})
            push(child.tail, False)
            continue
        bold = child.tag in ("strong", "b")
        push(child.text, bold)
        for g in child:                      # one level is all these use
            push(g.text, bold)
            push(g.tail, bold)
        push(child.tail, False)
    if out:
        out[-1]["t"] = out[-1]["t"].rstrip()
    return [r for r in out if r["t"] or r.get("br")]


def table(el):
    rows = []
    for tr in el.iter("tr"):
        cells, header = [], False
        for td in tr:
            if td.tag == "th":
                header = True
            cells.append({"runs": runs(td)})
        rows.append({"header": header, "cells": cells})
    return rows


def block_for(el):
    cls = el.get("class") or ""
    tag = el.tag

    if tag == "p" and "statement" in cls:
        return {"k": "statement", "runs": runs(el)}
    if tag == "p" and "note-line" in cls:
        return {"k": "note", "runs": runs(el)}
    if tag == "p" and "lead" in cls:
        return {"k": "lead", "runs": runs(el)}
    if tag == "p":
        return {"k": "para", "runs": runs(el)}
    if tag == "ul":
        return {"k": "list", "items": [runs(li) for li in el.findall("li")]}
    if tag == "table":
        return {"k": "table", "rows": table(el)}
    if "kpis" in cls:
        return {"k": "kpis", "items": [
            {"num": " ".join(k.find_class("num")[0].text_content().split()),
             "lbl": " ".join(k.find_class("lbl")[0].text_content().split())}
            for k in el.find_class("kpi")]}
    if "plan-grid" in cls or "flow" in cls or "band-grid" in cls:
        cells = []
        for c in el:
            head = c.find("h4")
            kick = c.find_class("fk") or c.find_class("bk")
            cells.append({
                "head": (head.text_content().strip() if head is not None
                         else kick[0].text_content().strip() if kick else ""),
                "blocks": [block_for(x) for x in c
                           if x.tag in ("p", "ul") or x.tag == "table"],
            })
        return {"k": "cells", "cells": cells}
    if "seq" in cls.split():
        rows = []
        for r in el.find_class("seq-row"):
            rows.append({"k": r.find_class("seq-k")[0].text_content().strip(),
                         "runs": runs(r.find("p"))})
        return {"k": "seq", "rows": rows}
    return None


def main():
    sheets = []
    for key, fname in FRAGS:
        doc = LH.fromstring((HERE / "oap-plan" / fname).read_text(encoding="utf-8"))
        head = doc.find_class("sheet-head")[0]
        boxes = []
        for box in doc.find_class("box"):
            cls = [c for c in (box.get("class") or "").split()
                   if c.startswith("b-")]
            label_el = box.find_class("box-label")[0]
            sub = label_el.find("span")
            blocks = [b for b in (block_for(x) for x in box
                                  if x.get("class") != "box-label")
                      if b is not None]
            boxes.append({
                "cls": cls[0] if cls else "",
                "label": (label_el.text or "").strip(),
                "sub": " ".join(sub.text_content().split()) if sub is not None else "",
                "accent": "rule-top" in (box.get("class") or ""),
                "blocks": blocks,
            })
        sheets.append({
            "key": key,
            "title": " ".join(head.find("div").find("h1").text_content().split()),
            "chips": [" ".join(c.text_content().split())
                      for c in head.find_class("chip")],
            "boxes": boxes,
        })
    json.dump({"sheets": sheets}, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
