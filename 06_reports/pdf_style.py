"""Shared ReportLab styling for the three project documents."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, Image, KeepTogether,
                                NextPageTemplate, PageBreak)

NAVY  = colors.HexColor("#0B2545")
NAVY2 = colors.HexColor("#13315C")
GOLD  = colors.HexColor("#C9A227")
TEAL  = colors.HexColor("#1B7F79")
SLATE = colors.HexColor("#5A6B7B")
RUST  = colors.HexColor("#A6432F")
LINE  = colors.HexColor("#DCE2E9")
BG    = colors.HexColor("#F4F6F9")
CREAM = colors.HexColor("#FFF9E8")
MINT  = colors.HexColor("#EEF6F5")
BLUSH = colors.HexColor("#FBEFEC")

ss = getSampleStyleSheet()
def S(name, **kw):
    base = kw.pop("parent", ss["BodyText"])
    return ParagraphStyle(name, parent=base, **kw)

TITLE   = S("t", fontName="Helvetica-Bold", fontSize=26, leading=30, textColor=colors.white, spaceAfter=6)
SUBTITLE= S("st", fontName="Helvetica", fontSize=12.5, leading=17, textColor=colors.HexColor("#D6DEE8"))
H1      = S("h1", fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=NAVY, spaceBefore=16, spaceAfter=8)
H2      = S("h2", fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=NAVY2, spaceBefore=12, spaceAfter=5)
H3      = S("h3", fontName="Helvetica-Bold", fontSize=10.5, leading=14, textColor=TEAL, spaceBefore=9, spaceAfter=3)
BODY    = S("b", fontName="Helvetica", fontSize=9.7, leading=14.4, alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#1A2A3A"), spaceAfter=6)
BODYL   = S("bl", parent=BODY, alignment=TA_LEFT)
LEAD    = S("lead", parent=BODY, fontSize=11, leading=16, textColor=NAVY)
BULLET  = S("bu", parent=BODY, leftIndent=13, bulletIndent=3, spaceAfter=3.5)
NUMB    = S("nu", parent=BODY, leftIndent=15, bulletIndent=3, spaceAfter=3.5)
SMALL   = S("sm", fontName="Helvetica", fontSize=8.2, leading=11.4, textColor=SLATE)
CAPTION = S("cap", fontName="Helvetica-Oblique", fontSize=8.2, leading=11, textColor=SLATE,
            alignment=TA_CENTER, spaceBefore=3, spaceAfter=10)
QUOTE   = S("q", parent=BODY, leftIndent=10, rightIndent=8, fontName="Helvetica-Oblique",
            textColor=NAVY2)
CELL    = S("c", fontName="Helvetica", fontSize=8.3, leading=11.2, textColor=colors.HexColor("#1A2A3A"))
CELLB   = S("cb", parent=CELL, fontName="Helvetica-Bold")
CELLH   = S("ch", fontName="Helvetica-Bold", fontSize=8.2, leading=11, textColor=colors.white)


class DocTemplate(BaseDocTemplate):
    def __init__(self, filename, title, running_head, **kw):
        super().__init__(filename, pagesize=A4, title=title, author="bann",
                         leftMargin=20*mm, rightMargin=20*mm,
                         topMargin=22*mm, bottomMargin=18*mm, **kw)
        self.running_head = running_head
        self.doc_title = title
        frame = Frame(self.leftMargin, self.bottomMargin,
                      self.width, self.height, id="main")
        cover = Frame(0, 0, A4[0], A4[1], id="cover",
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="Cover", frames=[cover], onPage=self._cover_bg),
            PageTemplate(id="Body",  frames=[frame], onPage=self._chrome),
        ])

    def _cover_bg(self, canv, doc):
        canv.saveState()
        canv.setFillColor(NAVY); canv.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        canv.setFillColor(NAVY2)
        canv.rect(0, A4[1]-120*mm, A4[0], 120*mm, fill=1, stroke=0)
        canv.setFillColor(GOLD)
        canv.rect(0, A4[1]-122*mm, A4[0], 2.4*mm, fill=1, stroke=0)
        for i, r in enumerate([46, 34, 22]):
            canv.setFillColor(colors.HexColor("#1B3A63" if i % 2 == 0 else "#16324F"))
            canv.circle(A4[0]-24*mm, 40*mm, r*mm, fill=1, stroke=0)
        canv.restoreState()

    def _chrome(self, canv, doc):
        canv.saveState()
        canv.setStrokeColor(LINE); canv.setLineWidth(0.6)
        canv.line(20*mm, A4[1]-16*mm, A4[0]-20*mm, A4[1]-16*mm)
        canv.setFont("Helvetica", 7.6); canv.setFillColor(SLATE)
        canv.drawString(20*mm, A4[1]-14*mm, self.running_head)
        canv.drawRightString(A4[0]-20*mm, A4[1]-14*mm, "Mubadala Portfolio Strategy Project")
        canv.line(20*mm, 13*mm, A4[0]-20*mm, 13*mm)
        canv.setFont("Helvetica", 7.6)
        canv.drawString(20*mm, 9*mm, "bann  |  August 2026")
        canv.setFillColor(NAVY); canv.setFont("Helvetica-Bold", 8.4)
        canv.drawRightString(A4[0]-20*mm, 9*mm, str(canv.getPageNumber()-1))
        canv.restoreState()


def cover(title, subtitle, meta_lines, kicker="EQUITY RESEARCH"):
    F = []
    F.append(Spacer(1, 46*mm))
    F.append(Table([[Paragraph(f'<font color="#C9A227"><b>{kicker}</b></font>',
              S("k", fontName="Helvetica-Bold", fontSize=10.5, textColor=GOLD))]],
              colWidths=[A4[0]-40*mm], style=TableStyle([
              ("LEFTPADDING",(0,0),(-1,-1),20*mm),("RIGHTPADDING",(0,0),(-1,-1),0),
              ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),8)])))
    for txt, st in [(title, TITLE), (subtitle, SUBTITLE)]:
        F.append(Table([[Paragraph(txt, st)]], colWidths=[A4[0]-40*mm],
                 style=TableStyle([("LEFTPADDING",(0,0),(-1,-1),20*mm),
                 ("RIGHTPADDING",(0,0),(-1,-1),10*mm),("TOPPADDING",(0,0),(-1,-1),0),
                 ("BOTTOMPADDING",(0,0),(-1,-1),10)])))
    F.append(Spacer(1, 44*mm))
    rows = [[Paragraph(f'<font color="#8FA3BC">{a}</font>',
             S("m1", fontName="Helvetica", fontSize=8.6, textColor=colors.HexColor("#8FA3BC"))),
             Paragraph(f'<font color="#FFFFFF">{b}</font>',
             S("m2", fontName="Helvetica-Bold", fontSize=8.9, textColor=colors.white))]
            for a, b in meta_lines]
    F.append(Table(rows, colWidths=[44*mm, 106*mm], style=TableStyle([
        ("LEFTPADDING",(0,0),(0,-1),20*mm),("TOPPADDING",(0,0),(-1,-1),3.4),
        ("BOTTOMPADDING",(0,0),(-1,-1),3.4),("VALIGN",(0,0),(-1,-1),"TOP")])))
    F.append(NextPageTemplate("Body")); F.append(PageBreak())
    return F


def table(data, widths, header=True, align=None, zebra=True, fontsize=8.3):
    rows = []
    for i, row in enumerate(data):
        out = []
        for j, c in enumerate(row):
            if isinstance(c, Paragraph): out.append(c)
            elif i == 0 and header: out.append(Paragraph(str(c), CELLH))
            else: out.append(Paragraph(str(c), CELL))
        rows.append(out)
    st = [("GRID",(0,0),(-1,-1),0.4,LINE),
          ("VALIGN",(0,0),(-1,-1),"TOP"),
          ("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),
          ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]
    if header:
        st += [("BACKGROUND",(0,0),(-1,0),NAVY),("TOPPADDING",(0,0),(-1,0),5),
               ("BOTTOMPADDING",(0,0),(-1,0),5)]
    if zebra:
        for i in range(1, len(rows)):
            if i % 2 == 0: st.append(("BACKGROUND",(0,i),(-1,i),colors.HexColor("#F7F9FB")))
    if align:
        for col, a in align.items(): st.append(("ALIGN",(col,0),(col,-1),a))
    return Table(rows, colWidths=widths, style=TableStyle(st), repeatRows=1 if header else 0)


def callout(title, text, kind="note"):
    bg, bar = {"note":(CREAM,GOLD), "find":(MINT,TEAL), "warn":(BLUSH,RUST)}[kind]
    body = Paragraph(f"<b>{title}</b>  {text}",
                     S("co", fontName="Helvetica", fontSize=9.2, leading=13.2,
                       textColor=colors.HexColor("#2A2A2A"), alignment=TA_JUSTIFY))
    t = Table([["", body]], colWidths=[2.6*mm, None], style=TableStyle([
        ("BACKGROUND",(0,0),(0,0),bar), ("BACKGROUND",(1,0),(1,0),bg),
        ("LEFTPADDING",(0,0),(0,0),0), ("RIGHTPADDING",(0,0),(0,0),0),
        ("LEFTPADDING",(1,0),(1,0),8), ("RIGHTPADDING",(1,0),(1,0),8),
        ("TOPPADDING",(0,0),(-1,-1),7), ("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    return KeepTogether([Spacer(1,3), t, Spacer(1,7)])


def figure(path, caption, width_mm=155):
    from PIL import Image as PILImage
    try:
        w, h = PILImage.open(path).size
    except Exception:
        w, h = 1000, 600
    W = width_mm*mm; H = W*h/w
    return KeepTogether([Spacer(1,4), Image(path, width=W, height=H),
                         Paragraph(caption, CAPTION)])


def kpi_strip(items):
    cells = []
    for label, value, note in items:
        cells.append(Paragraph(
            f'<font size="7.2" color="#5A6B7B"><b>{label.upper()}</b></font><br/>'
            f'<font size="16" color="#0B2545"><b>{value}</b></font><br/>'
            f'<font size="7.4" color="#1B7F79"><b>{note}</b></font>',
            S("kp", fontName="Helvetica", fontSize=9, leading=13, alignment=TA_CENTER)))
    t = Table([cells], colWidths=[(170*mm)/len(cells)]*len(cells), style=TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),BG), ("BOX",(0,0),(-1,-1),0.5,LINE),
        ("INNERGRID",(0,0),(-1,-1),0.5,LINE), ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),9), ("BOTTOMPADDING",(0,0),(-1,-1),9)]))
    return KeepTogether([Spacer(1,4), t, Spacer(1,9)])


def bullets(items, style=BULLET, char="•"):
    return [Paragraph(t, style, bulletText=char) for t in items]

def numbered(items, style=NUMB):
    return [Paragraph(t, style, bulletText=f"{i+1}.") for i, t in enumerate(items)]
