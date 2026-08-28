"""JP_TapThat_WhereYouAre_v01 — adapted from the jp-brand-presentation reference generator."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

JEWELL_BLACK = RGBColor(0x11,0x11,0x11); CREAM = RGBColor(0xFA,0xF8,0xF4)
SIGNAL_BLUE  = RGBColor(0x2D,0x5B,0xFF); CALM_GREY = RGBColor(0xED,0xEB,0xEA)
GREY_TEXT    = RGBColor(0x66,0x66,0x66)
POPPINS="Poppins"; SLIDE_W=Inches(13.333); SLIDE_H=Inches(7.5); MARGIN=Inches(1.0)

def bg(slide,c):
    f=slide.background.fill; f.solid(); f.fore_color.rgb=c

def tb(slide,left,top,width,height,text,size_pt=14,bold=False,color=JEWELL_BLACK,
       uppercase=False,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,line_spacing=1.5,tracking=None):
    box=slide.shapes.add_textbox(left,top,width,height); tf=box.text_frame
    tf.word_wrap=True; tf.margin_left=0; tf.margin_right=0; tf.margin_top=0; tf.margin_bottom=0
    tf.vertical_anchor=anchor
    for i,line in enumerate(text.split("\n")):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment=align; p.line_spacing=line_spacing
        r=p.add_run(); r.text=line.upper() if uppercase else line
        f=r.font; f.name=POPPINS; f.size=Pt(size_pt); f.bold=bold; f.color.rgb=color
        if tracking is not None: r._r.get_or_add_rPr().set("spc",str(tracking))
    return box

def hairline(slide,left,top,width,color=CALM_GREY,weight_pt=0.75):
    ln=slide.shapes.add_connector(1,left,top,left+width,top)
    ln.line.color.rgb=color; ln.line.width=Pt(weight_pt); return ln

def s_title(prs,bar,title,subtitle=None,date_line=None):
    s=prs.slides.add_slide(prs.slide_layouts[6]); bg(s,CREAM)
    tb(s,MARGIN,Inches(0.4),Inches(11.3),Inches(0.3),bar,9,uppercase=True,tracking=200)
    tb(s,MARGIN,SLIDE_H-MARGIN-Inches(2.6),Inches(11.3),Inches(2.0),title,60,bold=True,
       line_spacing=1.05,anchor=MSO_ANCHOR.BOTTOM)
    if subtitle: tb(s,MARGIN,SLIDE_H-Inches(1.35),Inches(11.3),Inches(0.6),subtitle,20)
    if date_line: tb(s,Inches(9.0),SLIDE_H-Inches(0.6),Inches(3.3),Inches(0.3),date_line,11,
                     color=GREY_TEXT,align=PP_ALIGN.RIGHT)
    return s

def s_content(prs,eyebrow,headline,body=None,head_size=38,body_top=4.5,body_w=10.0):
    s=prs.slides.add_slide(prs.slide_layouts[6]); bg(s,CREAM)
    tb(s,MARGIN,MARGIN,Inches(11.3),Inches(0.3),eyebrow,9,uppercase=True,tracking=200)
    tb(s,MARGIN,Inches(1.9),Inches(11.3),Inches(2.3),headline,head_size,line_spacing=1.12)
    if body: tb(s,MARGIN,Inches(body_top),Inches(body_w),Inches(2.4),body,14,line_spacing=1.55)
    return s

def s_divider(prs,num,title,strapline=None):
    s=prs.slides.add_slide(prs.slide_layouts[6]); bg(s,JEWELL_BLACK)
    tb(s,MARGIN,MARGIN,Inches(11.3),Inches(0.3),num,12,color=CREAM,uppercase=True,tracking=200)
    tb(s,MARGIN,Inches(2.3),Inches(11.3),Inches(3.0),title,96,color=CREAM,
       line_spacing=1.0,anchor=MSO_ANCHOR.MIDDLE)
    if strapline: tb(s,MARGIN,Inches(5.9),Inches(11.3),Inches(0.6),strapline,16,color=CREAM)
    return s

def s_closer(prs,action,owner):
    s=prs.slides.add_slide(prs.slide_layouts[6]); bg(s,CREAM)
    tb(s,MARGIN,Inches(2.0),Inches(11.3),Inches(2.0),"Next.",96,bold=True,line_spacing=1.0)
    tb(s,MARGIN,Inches(4.5),Inches(11.3),Inches(0.5),action,14)
    tb(s,MARGIN,Inches(5.0),Inches(11.3),Inches(0.5),owner,14)
    return s

def stat_row(slide,items,top=4.4):
    """Three or four figures with a label. Type and space, no chart furniture."""
    n=len(items); w=11.3/n
    for i,(num,lbl) in enumerate(items):
        L=MARGIN+Inches(w*i)
        hairline(slide,L,Inches(top),Inches(w-0.4))
        tb(slide,L,Inches(top+0.18),Inches(w-0.4),Inches(0.7),num,32,bold=True,line_spacing=1.0)
        tb(slide,L,Inches(top+0.95),Inches(w-0.5),Inches(0.9),lbl,11,color=GREY_TEXT,line_spacing=1.35)

def rule_table(slide,rows,top=2.6,col=4.4,size=13,step=0.78):
    """Rows separated by hairlines. Replaces bullets, which the deck standard bans."""
    y=top; h=step-0.06
    for k,v in rows:
        hairline(slide,MARGIN,Inches(y),Inches(11.3))
        tb(slide,MARGIN,Inches(y+0.14),Inches(col-0.3),Inches(h),k,size,bold=True,line_spacing=1.3)
        tb(slide,MARGIN+Inches(col),Inches(y+0.14),Inches(11.3-col),Inches(h),v,size,
           color=GREY_TEXT,line_spacing=1.38)
        y+=step
    hairline(slide,MARGIN,Inches(y),Inches(11.3))
    assert y<=7.05, f"rule_table overruns the slide: last rule at {y:.2f}in"

from deck_content import SLIDES

prs=Presentation(); prs.slide_width=SLIDE_W; prs.slide_height=SLIDE_H
for d in SLIDES:
    t=d["type"]
    if t=="title":
        s_title(prs,d["bar"],d["title"],d.get("subtitle"),d.get("date"))
    elif t=="divider":
        s_divider(prs,d["num"],d["title"],d.get("strapline"))
    elif t=="closer":
        s_closer(prs,d["action"],d["owner"])
    else:
        sl=s_content(prs,d["eyebrow"],d["headline"],d.get("body"),
                     head_size=d.get("head_size",38))
        if d.get("stats"): stat_row(sl,d["stats"])
        if d.get("rows"):
            rule_table(sl,d["rows"],top=d.get("row_top",2.6),col=d.get("row_col",4.4),
                       step=d.get("row_step",0.78))

out="JP_TapThat_WhereYouAre_v01.pptx"
prs.save(out); print(f"{out}: {len(prs.slides.__iter__.__self__._sldIdLst)} slides")
