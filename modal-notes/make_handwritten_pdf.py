"""Build creative handwritten-style PDF notes for Chapter 1 (stdlib + reportlab).

Usage:  python3 modal-notes/make_handwritten_pdf.py
Output: modal-notes/chapter-01-handwritten-notes.pdf
"""
from __future__ import annotations

import pathlib

from reportlab.graphics.shapes import Drawing, Line, PolyLine, Rect, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (HRFlowable, KeepTogether, PageBreak, Paragraph,
                                Spacer, Table, TableStyle)

HERE = pathlib.Path(__file__).parent
FONTS = HERE / "fonts"
OUT = HERE / "chapter-01-handwritten-notes.pdf"

# ---------- palette ----------
INK = colors.HexColor("#1F2A44")
BLUE = colors.HexColor("#2F6FED")
RED = colors.HexColor("#E5484D")
GREEN = colors.HexColor("#1F9D55")
HL = colors.HexColor("#FFF3A3")
PAPER = colors.HexColor("#FFFDF5")
RULE = colors.HexColor("#D8E3F2")
PALE_BLUE = colors.HexColor("#EFF4FF")
PALE_YELLOW = colors.HexColor("#FFFBEA")
PALE_PINK = colors.HexColor("#FFF0F2")
PALE_GREEN = colors.HexColor("#EDF9F0")

PAGE_W, PAGE_H = A4
ML, MR, MT, MB = 70, 45, 55, 55
FRAME_W = PAGE_W - ML - MR

# ---------- fonts ----------
registerFont(TTFont("Patrick", str(FONTS / "PatrickHand-Regular.ttf")))
registerFont(TTFont("Kalam", str(FONTS / "Kalam-Regular.ttf")))
registerFont(TTFont("KalamB", str(FONTS / "Kalam-Bold.ttf")))
registerFontFamily("hand", normal="Patrick", bold="KalamB",
                   italic="Patrick", boldItalic="KalamB")

# ---------- styles ----------
body = ParagraphStyle("body", fontName="Patrick", fontSize=11.5, leading=16,
                      textColor=INK, spaceAfter=5)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=20, bulletIndent=6,
                        spaceAfter=3)
center = ParagraphStyle("center", parent=body, alignment=1, spaceAfter=6)
formula = ParagraphStyle("formula", fontName="KalamB", fontSize=12.5,
                         leading=18, textColor=INK, alignment=1,
                         backColor=HL, borderPadding=6, spaceAfter=8,
                         spaceBefore=4)
sec = ParagraphStyle("sec", fontName="KalamB", fontSize=21, leading=24,
                     textColor=BLUE, spaceBefore=12, spaceAfter=2)
h3 = ParagraphStyle("h3", fontName="KalamB", fontSize=13.5, leading=17,
                    textColor=INK, spaceBefore=6, spaceAfter=3)
small = ParagraphStyle("small", parent=body, fontSize=10, leading=14)
cover_title = ParagraphStyle("ct", fontName="KalamB", fontSize=34, leading=36,
                             textColor=INK, alignment=1, spaceAfter=4)
cover_sub = ParagraphStyle("cs", parent=body, fontSize=13.5, leading=18,
                           alignment=1, textColor=colors.HexColor("#44507A"))


# ---------- helpers ----------
def hl(t: str) -> str:
    return f'<font backColor="#FFF3A3">{t}</font>'


def key(t: str) -> str:
    return f'<font color="#2F6FED"><b>[KEY]</b></font> {t}'


def lab(t: str) -> str:
    return f'<font color="#1F9D55"><b>[LAB]</b></font> {t}'


def trap(t: str) -> str:
    return f'<font color="#E5484D"><b>[TRAP]</b></font> {t}'


def link(t: str) -> str:
    return f'<font color="#7A4FD0"><b>[LINK]</b></font> {t}'


def tryit(t: str) -> str:
    return f'<font color="#B26A00"><b>[TRY]</b></font> {t}'


def formula_text(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;")


def P(t: str, style: ParagraphStyle = body) -> Paragraph:
    return Paragraph(t, style)


def F(t: str) -> Paragraph:
    return Paragraph(t, formula)


def B(t: str) -> Paragraph:
    return Paragraph(t, bullet, bulletText="->")


def box(title: str, text: str, color: colors.Color, bg: colors.Color) -> Table:
    inner = [[P(f"<b>{title}</b><br/>{text}")]]
    t = Table(inner, colWidths=[FRAME_W - 4])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("ROUNDEDCORNERS", [9, 9, 9, 9]),
        ("BOX", (0, 0), (-1, -1), 2.2, color),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    t.spaceBefore = 5
    t.spaceAfter = 7
    t.hAlign = "LEFT"
    return t


def tbl(rows: list[list[str]], widths: list[float], hdr: bool = True) -> Table:
    conv = [[P(f"<b>{c}</b>" if hdr and r == 0 else c, small) for c in row]
            for r, row in enumerate(rows)]
    t = Table(conv, colWidths=widths, repeatRows=1 if hdr else 0)
    style = [
        ("GRID", (0, 0), (-1, -1), 1, INK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1 if hdr else 0), (-1, -1),
         [colors.white, PALE_BLUE]),
    ]
    if hdr:
        style += [("BACKGROUND", (0, 0), (-1, 0), HL),
                  ("TEXTCOLOR", (0, 0), (-1, 0), INK)]
    t.setStyle(TableStyle(style))
    t.spaceBefore = 5
    t.spaceAfter = 7
    t.hAlign = "LEFT"
    return t


def heading(num: str, title: str) -> list:
    return [P(f"<font color=\"#E5484D\">{num}</font>  {title}", sec),
            HRFlowable(width="100%", thickness=1.6, color=RED,
                       spaceBefore=2, spaceAfter=6)]


# ---------- sketches ----------
def _base(w: float, h: float, caption: str) -> tuple[Drawing, float]:
    d = Drawing(w, h)
    d.add(Rect(0, 0, w, h, fillColor=colors.white, strokeColor=INK,
               strokeWidth=1.2))
    d.add(String(8, h - 15, caption, fontName="Kalam", fontSize=9,
                 fillColor=colors.HexColor("#44507A")))
    return d, h


def frf_sketch() -> Drawing:
    w, h = FRAME_W, 158
    d, _ = _base(w, h, "my sketch: plate FRF, 4 peaks")
    base, top = 26, h - 24
    d.add(Line(34, base, w - 14, base, strokeColor=INK, strokeWidth=1.6))
    d.add(Line(34, base, 34, top, strokeColor=INK, strokeWidth=1.6))
    xs = [40, 80, 105, 128, 152, 185, 208, 232, 258, 288, 308, 330,
          352, 372, 392, 415, 440]
    ys = [32, 32, 60, 118, 55, 34, 70, 108, 60, 33, 62, 92, 58, 34, 58, 78, 36]
    pts = [c for p in zip(xs, ys) for c in p]
    d.add(PolyLine(pts, strokeColor=RED, strokeWidth=2.6,
                   strokeLineJoin=1, strokeLineCap=1))
    for x, y, lab_ in [(128, 118, "M1 bend"), (232, 108, "M2 twist"),
                       (330, 92, "M3"), (415, 78, "M4")]:
        d.add(String(x - 24, y + 6, lab_, fontName="Kalam", fontSize=9,
                     fillColor=BLUE))
    d.add(String(w - 90, 8, "frequency ->", fontName="Kalam", fontSize=9))
    return d


def drive_cross_sketch() -> Drawing:
    w, h = FRAME_W, 140
    d, _ = _base(w, h, "drive point vs cross FRF")
    # left panel
    d.add(Line(20, 24, 210, 24, strokeColor=INK, strokeWidth=1.4))
    d.add(PolyLine([20, 30, 55, 30, 80, 95, 105, 34, 140, 32, 165, 90,
                    190, 32, 210, 32], strokeColor=GREEN, strokeWidth=2.4,
                   strokeLineJoin=1))
    d.add(String(30, h - 30, "drive h33: peak-v-peak!", fontName="Kalam",
                 fontSize=9.5, fillColor=GREEN))
    # right panel
    d.add(Line(250, 24, 440, 24, strokeColor=INK, strokeWidth=1.4))
    d.add(PolyLine([250, 30, 300, 30, 322, 88, 345, 40, 385, 36, 408, 70,
                    440, 34], strokeColor=BLUE, strokeWidth=2.4,
                   strokeLineJoin=1))
    d.add(String(262, h - 30, "cross: no alternation", fontName="Kalam",
                 fontSize=9.5, fillColor=BLUE))
    return d


def windows_sketch() -> Drawing:
    w, h = FRAME_W, 132
    d, _ = _base(w, h, "window shapes")
    d.add(Rect(30, 26, 100, 62, fillColor=None, strokeColor=INK,
               strokeWidth=2.2))
    d.add(String(40, 92, "uniform", fontName="Kalam", fontSize=9.5))
    bell = [170, 28, 185, 55, 205, 78, 225, 86, 245, 78, 265, 55, 280, 28]
    d.add(PolyLine(bell, strokeColor=INK, strokeWidth=2.2, strokeLineJoin=1))
    d.add(String(190, 92, "hanning bell", fontName="Kalam", fontSize=9.5))
    exp = [320, 86, 345, 66, 370, 52, 395, 42, 420, 35, 440, 31]
    d.add(PolyLine(exp, strokeColor=RED, strokeWidth=2.4, strokeLineJoin=1))
    d.add(String(330, 92, "exponential", fontName="Kalam", fontSize=9.5,
                 fillColor=RED))
    return d


def ods_sketch() -> Drawing:
    w, h = FRAME_W, 128
    d, _ = _base(w, h, "operating shape = mode 1 + mode 2 mixed!")
    d.add(PolyLine([20, 45, 45, 75, 70, 45, 95, 45], strokeColor=BLUE,
                   strokeWidth=2.6, strokeLineJoin=1))
    d.add(String(30, 80, "M1", fontName="KalamB", fontSize=11,
                 fillColor=BLUE))
    d.add(String(108, 52, "+", fontName="KalamB", fontSize=16))
    d.add(PolyLine([140, 45, 160, 72, 180, 45, 200, 20, 220, 45, 240, 45],
                   strokeColor=RED, strokeWidth=2.6, strokeLineJoin=1))
    d.add(String(175, 80, "M2", fontName="KalamB", fontSize=11,
                 fillColor=RED))
    d.add(String(252, 52, "=", fontName="KalamB", fontSize=16))
    d.add(PolyLine([285, 45, 305, 70, 325, 40, 345, 60, 365, 30, 385, 55,
                    405, 38, 425, 50], strokeColor=INK, strokeWidth=2.6,
                   strokeLineJoin=1))
    d.add(String(320, 80, "ODS ??", fontName="KalamB", fontSize=11))
    return d


def cover_star() -> Drawing:
    d = Drawing(FRAME_W, 92)
    cx = FRAME_W / 2
    pts = [(0, 34), (9, 12), (32, 12), (14, -2), (21, -24), (0, -10),
           (-21, -24), (-14, -2), (-32, 12), (-9, 12)]
    flat = [c for p in pts for c in (cx + p[0], 52 + p[1])]
    flat += flat[:2]
    d.add(PolyLine(flat, strokeColor=RED, strokeWidth=2.4, fillColor=HL,
                   strokeLineJoin=1))
    d.add(Line(60, 20, 150, 20, strokeColor=BLUE, strokeWidth=2))
    d.add(Line(150, 20, 138, 14, strokeColor=BLUE, strokeWidth=2))
    d.add(Line(150, 20, 138, 26, strokeColor=BLUE, strokeWidth=2))
    d.add(String(52, 30, "ch.1", fontName="Kalam", fontSize=11,
                 fillColor=BLUE))
    d.add(Line(FRAME_W - 150, 66, FRAME_W - 60, 66, strokeColor=GREEN,
               strokeWidth=2))
    d.add(Line(FRAME_W - 60, 66, FRAME_W - 72, 60, strokeColor=GREEN,
               strokeWidth=2))
    d.add(Line(FRAME_W - 60, 66, FRAME_W - 72, 72, strokeColor=GREEN,
               strokeWidth=2))
    d.add(String(FRAME_W - 150, 74, "lets go!", fontName="Kalam",
                 fontSize=11, fillColor=GREEN))
    return d


# ---------- page background ----------
def bg(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    # ruled lines
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.6)
    y = PAGE_H - MT + 8
    while y > MB - 10:
        canvas.line(ML - 14, y, PAGE_W - MR + 10, y)
        y -= 16
    # red margin
    canvas.setStrokeColor(colors.HexColor("#F3A3AB"))
    canvas.setLineWidth(1.6)
    canvas.line(52, MB - 14, 52, PAGE_H - MT + 14)
    # margin doodle (alternate by page)
    canvas.setStrokeColor(RED)
    canvas.setLineWidth(1.2)
    if doc.page % 2 == 0:
        x0, y0 = 26, PAGE_H / 2
        canvas.circle(x0, y0, 10, stroke=1, fill=0)
        canvas.setFillColor(RED)
        canvas.circle(x0 - 3.5, y0 + 2.5, 1.1, stroke=0, fill=1)
        canvas.circle(x0 + 3.5, y0 + 2.5, 1.1, stroke=0, fill=1)
        canvas.arc(x0 - 5, y0 - 6, x0 + 5, y0 + 2, startAng=200, extent=140)
    else:
        x0, y0 = 26, PAGE_H / 2
        canvas.line(x0 - 7, y0, x0 + 7, y0)
        canvas.line(x0, y0 - 7, x0, y0 + 7)
        canvas.line(x0 - 5, y0 - 5, x0 + 5, y0 + 5)
        canvas.line(x0 - 5, y0 + 5, x0 + 5, y0 - 5)
    # footer
    if doc.page > 1:
        canvas.setFont("Kalam", 9)
        canvas.setFillColor(colors.HexColor("#77809E"))
        canvas.drawString(ML, 32, "Ch.1 Modal Testing - handwritten notes")
        canvas.drawRightString(PAGE_W - MR, 32, f"p. {doc.page}")
    canvas.restoreState()


# ---------- content ----------
def build_story() -> list:
    s: list = []

    # ===== COVER =====
    s += [Spacer(1, 30), cover_star(),
          P("Modal Testing: A Practitioner's Guide", cover_sub),
          P("Ch. 1 - Experimental<br/>Modal Analysis <i>without tears</i>",
            cover_title),
          P("detailed handwritten-style notes - trial edition", cover_sub),
          Spacer(1, 8),
          box("Whole chapter in 1 line:",
              "a structure = a <b>team of SDOF oscillators</b> glued "
              "together. Modal analysis names each player: "
              "<b>frequency + damping + shape</b>. Everything else = "
              "<i>how to see them clearly</i>.", BLUE, PALE_BLUE),
          box("How to use:",
              "Made for a MechE fresher who knows basic vibrations. "
              "Start at S0, read in order, do every [TRY]. "
              "Finish with the self-test on the last pages!", GREEN,
              PALE_GREEN),
          P("<b>Legend:</b>  <font color=\"#2F6FED\"><b>[KEY]</b></font> key idea"
            " &nbsp; <font color=\"#1F9D55\"><b>[LAB]</b></font> lab tip"
            " &nbsp; <font color=\"#E5484D\"><b>[TRAP]</b></font> trap"
            " &nbsp; <font color=\"#7A4FD0\"><b>[LINK]</b></font> to basics"
            " &nbsp; <font color=\"#B26A00\"><b>[TRY]</b></font> try it",
            center),
          P("Council crew: Dr. Meera K. (theory) - Dr. Viktor H. (lab) - "
            "Dr. Lena F. (signals) - Prof. Arjun D. (pedagogy) - "
            "Dr. Sofia M. (field) &nbsp;&nbsp;|&nbsp;&nbsp; 11 Sep 2026",
            small)]
    s.append(PageBreak())

    # ===== S0 PRIMER =====
    s += heading("(0)", "Primer - from SDOF to modes")
    s.append(F(formula_text("m x'' + c x' + k x = f(t)  ->  "
                            "f(n) = (1 / 2 pi) x sqrt(k / m)")))
    s.append(box("Your upgrade map:",
                 link("You know <b>1 mass gives 1 peak</b>. A plate or beam "
                      "is many masses, so <b>many peaks</b>. Each peak = one "
                      "'hidden SDOF' = one <b>mode</b>. Resonance in SDOF "
                      "becomes: every mode resonates <b>in its own shape</b>, "
                      "with <b>its own damping</b>. Messy time traces become "
                      "clear peak plots after the <b>FFT</b>."), BLUE,
                 PALE_BLUE))
    s.append(tbl([
        ["You know (SDOF)", "This chapter adds (real structures)"],
        ["1 natural frequency", "MANY natural frequencies, one per mode"],
        ["Resonance = big response near fn", "Each mode resonates in its own shape"],
        ["Damping ratio sets peak height", "Every mode has its own damping"],
        ["FRF of 1 oscillator: 1 peak", "FRF of a structure: many peaks"],
        ["Time response tells the story", "Frequency domain (FFT) tells the story"],
    ], [FRAME_W * 0.42, FRAME_W * 0.58]))
    s.append(box("Kitchen modal test:",
                 tryit("Hum near a steel plate and hear it ring at certain "
                       "pitches - those are its natural frequencies. Tap "
                       "different spots to excite them differently. That IS "
                       "the plate experiment of S1.1, in your kitchen!"),
                 colors.HexColor("#B26A00"), PALE_YELLOW))

    # ===== 1.1 =====
    s += heading("(1.1)", "Could you explain modal analysis to me?")
    s.append(box("The 3-step engineering logic (cantilever story):",
                 "<b>1. Characteristics</b> (length, E, I, density...) "
                 "describe the beam but alone say nothing about deflection or "
                 "failure. <b>2. + Loads</b> gives response. "
                 "<b>3. + Design spec</b> gives pass/fail. Modal data is "
                 "step-1 data for dynamics: " + hl("powerful, but cannot "
                 "judge alone!") + " (In real troubleshooting, loads and "
                 "specs are often unknown - that is exactly when modal "
                 "thinking saves you.)", BLUE, PALE_BLUE))
    s.append(P(key("<b>Structural dynamics</b> = the full movie: all inputs "
                   "(fan, disk drive, bumps) give total response. "
                   "<b>Modal analysis</b> = the cast list: the system's own "
                   "modes. Time traces look chaotic, but in the "
                   "<b>frequency domain</b> the chaos separates into clear "
                   "peaks sitting at the modes.")))
    s.append(box("Modes are band-pass filters:",
                 "Each mode amplifies input energy near its own frequency "
                 "and ignores the rest. Measured response = sum over modes "
                 "of (mode filter x input). Uneven input spectrum gives "
                 "uneven peak heights - even a strong mode looks small if "
                 "starved of input energy there!", BLUE, PALE_BLUE))
    s += [P("<b>The plate experiment</b> (heart of S1.1): free plate, sine "
            "force of <b>constant peak, varying frequency</b> at one corner, "
            "accelerometer at another corner.",
            h3)]
    s.append(B("<b>Sine sweep in time:</b> response breathes up and down as "
               "excitation frequency slides - same force, wildly different "
               "response. Maxima = crossing a <b>resonance</b>."))
    s.append(B("<b>FFT gives the FRF:</b> 4 clean peaks (this plate, this "
               "band). Overlay time-sweep maxima on FRF peaks - they line "
               "up. " + trap("A <i>random</i> time trace would be unreadable; "
               "the FRF rescues us.")))
    s.append(B("<b>Dwell at each peak</b> with 45 accelerometers: freeze the "
               "excitation at one natural frequency and map deformation "
               "everywhere: M1 = 1st bending, M2 = 1st twist, M3 = 2nd "
               "bending, M4 = 2nd twist. Strictly these are operating "
               "deflections, practically they equal the mode shapes for "
               "well-separated modes."))
    s.append(KeepTogether(frf_sketch()))
    s.append(P(key("<b>Mass and stiffness place the modes; damping sizes "
                   "the peaks.</b> Designers use modes to <i>avoid</i> "
                   "resonances; test engineers use them to <i>diagnose</i> "
                   "noise and vibration failures.")))
    s.append(box("Two analogies - interview gold:",
                 "<b>Cookbook:</b> hundreds of ingredients, but each recipe "
                 "uses its own small subset in its own proportions. Each "
                 "loading 'cooks' its own subset of modes.<br/><b>100-piece "
                 "orchestra:</b> each score uses different instruments at "
                 "different intensities; one out-of-tune player ruins the "
                 "piece, and you find the culprit only by listening to "
                 "players <i>individually</i>. Total response hides the "
                 "fault; modes let you audition each player separately - "
                 "modal analysis's superpower!<br/><b>Council bonus, "
                 "playground swings:</b> random pushes = weak chaos "
                 "(broadband input, messy trace); pushing <i>in rhythm</i> "
                 "= giant motion (dwell at resonance). Two swings tied with "
                 "a rope = coupled modes, like bend + twist of the plate!",
                 GREEN, PALE_GREEN))
    s.append(P(tryit("Tap a ruler clamped to a table at different overhang "
                     "lengths - pitch drops as overhang grows (stiffness "
                     "falls). You just did 'mass and stiffness place the "
                     "modes' with stationery.")))

    # ===== 1.2 =====
    s += heading("(1.2)", "Just what are FRFs?")
    s.append(F(formula_text("H(f) = X(f) / F(f)   ...complex! "
                            "mag + phase = real + imag")))
    s.append(P("Measure <b>force AND response together</b> (response = "
               "displacement, velocity, or acceleration), FFT both, divide. "
               "All four views (magnitude, phase, real, imaginary) show the "
               "same truth."))
    s += [P("The 3-DOF beam gives a 3 x 3 FRF matrix:", h3)]
    s.append(tbl([
        ["", "force @ 1", "force @ 2", "force @ 3"],
        ["resp @ 1", "h11", "h12", "h13"],
        ["resp @ 2", "h21", "h22", "h23"],
        ["resp @ 3", "h31", "h32", "h33  <- ref 3 row"],
    ], [FRAME_W * 0.22, FRAME_W * 0.26, FRAME_W * 0.26, FRAME_W * 0.26]))
    s.append(P("Notation <b>h(out, in)</b>: matrix row = response point, "
               "column = force point. 3 push points x 3 measure points = "
               "<b>9 FRFs</b>."))
    s.append(box("Drive-point FRF (push + measure at SAME point, e.g. h33) - "
                 "memorize like a phone number:",
                 "1. Peaks (resonances) and valleys (anti-resonances) "
                 "<b>alternate</b>.<br/>2. Phase <b>drops 180 deg</b> over a "
                 "resonance, <b>gains 180 deg</b> over an anti-resonance.<br/>"
                 "3. All <b>imaginary-part peaks point the same way</b>.<br/>"
                 + lab("First check on any drive-point plot: peak-valley "
                 "alternation? Imag peaks same direction? If not, suspect "
                 "the <i>measurement</i>, not the theory. - Viktor"),
                 GREEN, PALE_GREEN))
    s.append(KeepTogether(drive_cross_sketch()))
    s.append(box("Reciprocity - you do NOT need all 9 FRFs:",
                 key("Because the M, C, K matrices are symmetric, "
                 "<b>h(ij) = h(ji)</b>: push at i / measure at j equals push "
                 "at j / measure at i. So <b>one row OR one column</b> of "
                 "the matrix is enough to get every mode shape. (The book's "
                 "15-point waterfall plot shows the same idea: imag-peak "
                 "ridges trace each shape.)"), BLUE, PALE_BLUE))
    s += [P("1.2.1 Why is only one row or column needed?", h3)]
    s.append(B("Read the <b>imaginary-peak heights</b> across one row and the "
               "shape pops out. Row 3 and row 2 both show mode 1; heights "
               "differ by a scale factor - the <i>shape</i> is what matters."))
    s.append(box("THE NODE RULE:",
                 trap("With the reference at point 2, <b>mode 2 vanishes</b> "
                      "- point 2 sits on mode 2's node (zero-motion line). "
                      + hl("Never put your reference on (or near) a node of "
                      "a mode you need!") + " Later chapters turn this into "
                      "reference-selection strategy."), RED, PALE_PINK))
    s.append(P(tryit("Micro-example: imag peaks [ +0.2, +0.9, +1.6 ] read "
                     "first-bending (same sign, growing). Peaks "
                     "[ +1.0, 0.0, -1.0 ] read second-mode-like with a node "
                     "in the middle - and warn you a reference <i>at</i> the "
                     "middle would miss this mode entirely.")))

    # ===== 1.3 =====
    s += heading("(1.3)", "Shaker test vs impact test?")
    s.append(tbl([
        ["", "Hammer (impact)", "Shaker"],
        ["You get", "One ROW (response ref fixed, hammer roves)", "One COLUMN (force ref fixed, accels rove)"],
        ["Theory", "identical!", "identical! (hij = hji)"],
        ["Best at", "Fast, portable, no attached hardware", "Controlled input; big / heavy / damped parts"],
        ["Main enemies", "Tip choice, double hits, leakage", "Mass loading, stinger effects"],
    ], [FRAME_W * 0.16, FRAME_W * 0.42, FRAME_W * 0.42]))
    s.append(box("The test article is bigger than you think:",
                 key("Test article = structure <b>+ everything touching "
                 "it</b>: suspension, cables, sensor masses, shaker + "
                 "stinger. Theory assumes massless sensors and perfect "
                 "forces - the lab does not.") + "<br/><b>1. Roving-mass "
                 "effect:</b> one accelerometer is nothing vs the whole "
                 "machine but huge vs a thin panel's local mass. Moving "
                 "sensors between readings <i>retunes</i> the structure "
                 "mid-test. " + lab("Fix: leave ALL accelerometers mounted "
                 "(use a few at a time), or add <b>dummy masses</b> at "
                 "unmeasured points.") + "<br/><b>2. Shaker / stinger:</b> "
                 "the stinger should push purely axially and <i>decouple</i> "
                 "shaker dynamics, but residual mass and stiffness effects "
                 "often survive. Impact tests dodge this entirely - hence "
                 "hammer-vs-shaker differences on the same part.", BLUE,
                 PALE_BLUE))
    s += [P("1.3.1 What do we measure to compute the FRF? (analyzer chain)",
            h3)]
    s.append(F(formula_text("sensor -> anti-alias -> ADC -> window -> FFT "
                            "-> avg spectra -> FRF + coherence")))
    s.append(tbl([
        ["Stage", "What happens", "Enemy"],
        ["Transducers", "Force cell + accel / vel / disp pickup", "Bad mounting, saturation"],
        ["ADC (12/16/24-bit)", "Digitizes the waveform", "Sampling (resolution) + quantization (amplitude steps)"],
        ["Window", "Weights record so FFT periodicity is nearly met", "Leakage if skipped wrongly"],
        ["FFT + averaged spectra", "Input/output auto-spectra + cross-spectrum", "Noise (averaging fights it)"],
        ["FRF + coherence", "FRF = cross/input (essentially); coherence 0-1", "Coherence well under 1: do not trust band"],
    ], [FRAME_W * 0.24, FRAME_W * 0.44, FRAME_W * 0.32]))
    s.append(box("LEAKAGE - villain no. 1:",
                 key("The FFT assumes your record covers all time or "
                 "<b>repeats forever</b>. A cut-off sine violates that, so "
                 "energy <i>leaks and smears</i> across frequencies. Fix = "
                 "<b>windows</b>: weighting functions that taper the record "
                 "so it <i>looks</i> periodic. Windows distort a little; "
                 "leakage distorts catastrophically. (S1.4 to S1.6 = the war "
                 "against leakage.)") + "<br/>Lena's one-liner: sample rate "
                 "picks your map's borders, bits pick its resolution, "
                 "windows pick your poison - leakage or taper. <i>Choose "
                 "taper.</i>", RED, PALE_PINK))

    # ===== 1.4 + 1.5 =====
    s += heading("(1.4 + 1.5)", "Impact and shaker essentials")
    s += [P("Impact testing: two headline items (full war stories in Ch.7):",
            h3)]
    s.append(box("Hammer-tip hardness = your frequency-range knob:",
                 lab("<b>Harder tip gives wider excited band</b> (short "
                 "sharp pulse); <b>softer tip gives narrower band</b> (long "
                 "gentle push). General rule with exceptions - verify on "
                 "screen. Good = flat-ish input spectrum + coherence near 1 "
                 "across the band. Bad = spectrum rolling off + coherence "
                 "and FRF dying in the upper half (you did not feed those "
                 "modes energy).") + "<br/>" + trap("A soft tip is not "
                 "'wrong' - only wrong if you needed the higher modes. If "
                 "your band of interest is the flat part, ship it!"), GREEN,
                 PALE_GREEN))
    s.append(box("The response must die before the record ends:",
                 "Lightly damped structures keep ringing past the sample "
                 "interval, which means leakage. Standard rescue = "
                 "<b>exponential window</b> on the response (decays the tail "
                 "toward zero).<br/>" + key("<b>Windows damage data - try "
                 "the cures first:</b> 1. <b>narrower frequency span</b> "
                 "(longer time record), 2. <b>more spectral lines</b> (finer "
                 "resolution, longer record). Both give the vibration more "
                 "time to decay naturally.") + "<br/>" + lab("Viktor's "
                 "pre-flight: tip? decay? coherence? - three glances before "
                 "I believe any hammer FRF. Plus: no <b>double hits</b>, hit "
                 "squarely, watch for filter ring and saturated sensors "
                 "(Ch.7 previews)."), BLUE, PALE_BLUE))
    s += [P("Shaker testing: pick an excitation that needs NO window:", h3)]
    s.append(tbl([
        ["Excitation", "Leakage?", "Window?", "Notes"],
        ["Burst random", "NO - transient + decay fit ONE record", "None", "Workhorse of modal testing"],
        ["Sine chirp", "NO - repeats exactly in record", "None", "Great control of the band"],
        ["Plain random", "YES - never periodic in window", "Hanning (must); still a bit distorted", "Easy to run, weakest data"],
    ], [FRAME_W * 0.2, FRAME_W * 0.34, FRAME_W * 0.24, FRAME_W * 0.22]))
    s.append(box("Memory hook:",
                 "Lena: 'Random + Hanning is the fast food of excitation: "
                 "convenient, satisfying, slightly guilty. Burst random and "
                 "chirp are home cooking.'<br/><b>B</b>urst and "
                 "<b>C</b>hirp = <b>B</b>ye-<b>C</b>iao windows! "
                 "(<b>B</b>urst fits the <b>B</b>ox; <b>C</b>hirp "
                 "<b>C</b>ycles exactly.)", colors.HexColor("#B26A00"),
                 PALE_YELLOW))

    # ===== 1.6 =====
    s += heading("(1.6)", "Tell me more about windows!")
    s.append(P("Motto: " + hl("no window if you can avoid it; the right "
               "window if you can't") + " (field testing and operating data "
               "often give no choice)."))
    s.append(tbl([
        ["Window", "Shape in words", "Use it when..."],
        ["Uniform (rect / boxcar / 'no window')", "Gain = 1 everywhere", "Signal fully in one record OR periodic-in-window"],
        ["Hanning", "Bell / cosine, ends forced to 0", "Random / field signals that break periodicity"],
        ["Flat-top", "Broad flat crown", "Pure sine of unknown period; amplitude accuracy matters"],
        ["Force + Exponential", "1 around hammer pulse; decaying curve", "Impact pair: isolate pulse + decay ringing tail"],
    ], [FRAME_W * 0.3, FRAME_W * 0.3, FRAME_W * 0.4]))
    s.append(P("Typical pairings: uniform with impact (pulse + decay fit), "
               "burst random, chirp, pseudo-random, stepped sine; Hanning "
               "with shaker random and operating data; flat-top with "
               "calibration and constant-speed (RPM) excitation."))
    s.append(KeepTogether(windows_sketch()))
    s.append(box("Price of every window:",
                 trap("Peak amplitudes get less accurate and the structure "
                 "<b>looks more damped than it is</b>. Acceptable - "
                 "leakage's smearing is far worse. Deep math lives in the "
                 "signal-processing chapter."), RED, PALE_PINK))
    s.append(P(tryit("One-question drill: burst random test - which window? "
                     "<i>Uniform / none.</i> Factory-floor random? "
                     "<i>Hanning.</i> Hammer test, response ringing past the "
                     "record? <i>Force + exponential.</i> Sine calibration? "
                     "<i>Flat-top.</i>")))

    # ===== 1.7 =====
    s += heading("(1.7)", "How do we get mode shapes from plate FRFs?")
    s += [P("Step 1 - peak-picking (the simple, honest start):", h3)]
    s.append(P("6 points give 6 x 6 = <b>36 possible FRFs</b>. Read the "
               "<b>imaginary-part peaks</b> mode by mode:"))
    s.append(B("<b>Mode 1 (bending):</b> points 1, 2, 5, 6 near -1; points 3, "
               "4 near +1. Classic first-bending arc (all 45 points confirm "
               "it)."))
    s.append(B("<b>Mode 2 (torsion):</b> 1:+2, 2:-2, 5:-2, 6:+2, and "
               "<b>3, 4 near 0</b>. Twist with a <b>node line through "
               "3-4</b>. Hello again, node rule from S1.2!"))
    s += [P("Step 2 - curvefitting (what software really does):", h3)]
    s.append(P("Peak-picking is fine for simple, well-separated modes. "
               "Production work uses <b>modal parameter estimation = "
               "curvefitting</b>: decompose the measured FRF into a "
               "<b>sum of SDOF oscillators</b> (the S0 mental model becomes "
               "literal):"))
    s.append(F(formula_text("measured FRF = SDOF(M1) + SDOF(M2) + ... + residuals")))
    s.append(box("The analyst's three inputs (your job; the algorithm does the rest):",
                 "<b>1. Frequency band</b> to fit (fit in bands, a few modes "
                 "at a time). <b>2. How many modes</b> live in that band "
                 "(hard when modes crowd - indicator tools help; full "
                 "toolbox in Ch.5 / Ch.9). <b>3. Residual terms</b> - "
                 "compensation for modes <i>outside</i> the band still "
                 "tugging on it.", BLUE, PALE_BLUE))
    s.append(P(trap("<b>Garbage in, garbage out:</b> curvefitting cannot "
                    "rescue bad FRFs - which is why S1.3-S1.6 (measurement "
                    "quality) come <i>before</i> estimation in a "
                    "practitioner's head. Sofia: 'I have never seen a "
                    "curvefitter fix a double-hit. I have seen many analysts "
                    "try.'")))

    # ===== 1.8 =====
    s += heading("(1.8)", "Modal data vs operating data - do not mix!")
    s += [P("1.8.1 What is operating data?", h3)]
    s.append(box("Operating data = response ONLY.",
                 key("The machine runs (forces unknown / unmeasured) and you "
                 "record vibration. Golden chain: ") +
                 "<b>response = FRF (system filter) x force (whatever it "
                 "is)</b>. The FRF and modes decide <i>how</i> the structure "
                 "wants to move; the operating force decides <i>which</i> "
                 "modes play and how loudly.", BLUE, PALE_BLUE))
    s.append(P("Plate demo with a single-sine force at one corner (2 modes "
               "for simplicity):"))
    s.append(B("<b>Excite near mode 1:</b> operating deflection shape looks "
               "like <b>mode 1</b> (+ a whisper of mode 2)."))
    s.append(B("<b>Excite near mode 2:</b> shape looks like <b>mode 2</b> "
               "(+ a whisper of mode 1)."))
    s.append(B("<b>Excite midway:</b> a strange hybrid nobody recognizes - "
               "until you decompose it: a little bending + a little "
               "torsion. " + hl("Operating shapes are linear combinations "
               "of mode shapes.") + " With broadband force, many modes join "
               "the sum."))
    s.append(KeepTogether(ods_sketch()))
    s.append(P(trap("With operating data you never measure the force or the "
                    "FRF - so you cannot see <i>why</i> the shape looks that "
                    "way. That is the whole argument for modal testing.")))
    s += [P("1.8.2 So what good is modal data? (payoff slide)", h3)]
    s.append(tbl([
        ["Superpower", "What it means", "Needs"],
        ["SDM (structural dynamic modification)", "Predict 'what if we add ribs / mass / damping HERE?' without cutting metal", "Modal model (f, damping, shapes)"],
        ["Forced-response simulation", "Predict response to ANY hypothetical force", "Modal model"],
        ["FEM correlation + updating", "Check and fix the finite-element model against reality", "Modal model + FEM"],
    ], [FRAME_W * 0.3, FRAME_W * 0.42, FRAME_W * 0.28]))
    s.append(P(key("<b>Modal data = the reusable model</b> of the system. "
                   "<b>Operating data = a snapshot</b> of one situation.")))
    s += [P("1.8.3 Should I collect modal or operating data?", h3)]
    s.append(P("<b>Both, whenever schedule and budget allow.</b> If forced to "
               "choose, know what you lose:"))
    s.append(tbl([
        ["", "Modal data", "Operating data"],
        ["Measures", "Force AND response -> FRF -> true f, damping, shapes", "Response only"],
        ["Gives", "System characteristics; SDM + simulation + FEM work", "True in-service behavior"],
        ["Cannot", "Judge pass/fail alone (needs loads + spec - S1.1!)", "Do SDM / sim; shapes often confuse"],
    ], [FRAME_W * 0.16, FRAME_W * 0.42, FRAME_W * 0.42]))
    s.append(box("Sofia's field rule + mini-case:",
                 "'Operating data tells you <b>where it hurts</b>; modal "
                 "data tells you <b>why, and what to change</b>. "
                 "Painkillers or cure - your call.'<br/><b>Mini-case:</b> a "
                 "car cabin drones at 2800 RPM. Operating test shows a hot "
                 "floor panel - but which fix: stiffen, damp, or move the "
                 "exhaust hanger? Modal test reveals a floor bending mode "
                 "exactly at that RPM's firing frequency with a belly at the "
                 "hot spot - targeted rib + damping patch. Operating found "
                 "the pain; modal prescribed the cure.", GREEN, PALE_GREEN))

    # ===== 1.9 + REVISION =====
    s.append(PageBreak())
    s += heading("(1.9 + Revision)", "Closing + one-page recap")
    s.append(P("Ch.1 gave the <b>non-mathematical intuition</b>: modes as "
               "filters, FRFs as the measurement, hammer vs shaker, leakage "
               "vs windows, peak-pick to curvefit, modal vs operating. Next: "
               "<b>Ch.2</b> - the math under the intuition (SDOF to MDOF "
               "theory); <b>Ch.3-5</b> - signal processing, excitation "
               "details, parameter estimation; <b>Ch.6+</b> - the "
               "practitioner's craft."))
    s.append(P(link("Your study loop from here: for every later equation, "
                    "ask 'which Ch.1 picture does this formalize?' - if you "
                    "can answer, you own the chapter.")))
    s.append(tbl([
        ["#", "Big idea", "Punchline"],
        ["1", "Modal analysis finds...", "f, damping, shape per mode: the dynamic fingerprint"],
        ["2", "...but cannot judge alone", "Needs loads + spec (cantilever lesson)"],
        ["3", "FRF", "Output / input in freq domain; complex"],
        ["4", "Drive point hii", "Alternate peak/valley; -/+180 deg flips; imag same side"],
        ["5", "Reciprocity", "hij = hji: one row OR column suffices"],
        ["6", "Node rule", "Reference on a node means mode invisible"],
        ["7", "Shaker vs hammer", "Theory same; practice differs (mass, stinger)"],
        ["8", "FRF chain", "Sense -> AA -> ADC -> window -> FFT -> FRF + coh"],
        ["9", "Leakage", "FFT demands periodicity; windows are the tax"],
        ["10", "Hammer tip = band knob", "Hard = wide; flat spectrum + coh near 1 = good"],
        ["11", "Ringing tail?", "Exponential window - or longer record"],
        ["12", "Best shaker inputs", "Burst random + sine chirp = window-free"],
        ["13", "Windows", "Uniform / Hanning / flat-top / force+exp"],
        ["14", "Curvefitting", "FRF = sum of SDOFs + residuals"],
        ["15", "Operating vs modal", "ODS = sum modes x force; modal = reusable model"],
    ], [FRAME_W * 0.08, FRAME_W * 0.3, FRAME_W * 0.62]))
    s.append(F(formula_text("fn=(1/2pi) sqrt(k/m)  -  H=X/F  -  hij=hji  -  resp=FRF x force  -  coh near 1 = trust")))

    # ===== SELF-TEST =====
    s.append(PageBreak())
    s += heading("(Self-test)", "10 questions - no peeking!")
    qs = [
        "Why can't modal data alone say a design is acceptable?",
        "Same peak force, swept frequency, yet response varies wildly. Why?",
        "FRF shows 4 peaks but the time trace is chaos. Which do you trust for natural frequencies, and why?",
        "Name the 3 drive-point signatures.",
        "Your reference accelerometer sits on a mode's node. What happens? Fix?",
        "Roving hammer gives a ___ of the FRF matrix; shaker gives a ___.",
        "Hammer spectrum rolls off and coherence dies above 800 Hz. Diagnose + fix.",
        "Which two shaker excitations need no window, and why is each leakage-free?",
        "Burst random / factory random / ringing hammer response / sine calibration: pick windows.",
        "ODS at 55 Hz looks like nothing seen before; modes sit at 50 and 60 Hz. Explain.",
    ]
    for i, q in enumerate(qs, 1):
        s.append(Paragraph(f"<b>Q{i}.</b> {q}", bullet, bulletText="*"))
    s += [P("Answers (really no peeking!):", h3)]
    ans = [
        "Modes are characteristics only; response needs loads, verdict needs spec (S1.1).",
        "You are crossing resonances - each mode amplifies input near its own frequency (modal filtering).",
        "The FRF - the FFT separates the modal filters; time superposition hides them.",
        "Peak/valley alternation; -180 deg at resonance / +180 at anti-resonance; imag peaks all same direction.",
        "That mode vanishes from every FRF. Move the reference off the node.",
        "Row; column (fixed response ref vs fixed force ref).",
        "Tip too soft - no energy up high. Use a harder tip (verify flat spectrum + coh near 1); if only under 800 Hz matters, it is fine.",
        "Burst random (whole transient + decay in one record) and sine chirp (exactly periodic in the record).",
        "Uniform / none; Hanning; force + exponential; flat-top.",
        "55 Hz sits between modes, so ODS = combination of both (mostly), not a pure mode shape.",
    ]
    for i, a in enumerate(ans, 1):
        s.append(P(f"<b>A{i}.</b> {a}", small))
    s.append(box("Tear-off lab checklist:",
                 "<b>Before:</b> band of interest? tip / excitation picked "
                 "for it? reference off all nodes? all sensors mounted (no "
                 "roving-mass surprise)? stinger aligned (shaker)?<br/>"
                 "<b>During:</b> no double hits, square impacts? response "
                 "decayed in-record (or windowed)? no overload / saturation? "
                 "coherence near 1 in band?<br/><b>After:</b> drive-point "
                 "checks pass? reciprocity spot-check (hij near hji)? "
                 "logbook filled (tip, span, lines, windows, averages)?",
                 GREEN, PALE_GREEN))

    # ===== GLOSSARY =====
    s.append(PageBreak())
    s += heading("(Glossary)", "First-use definitions, Ch.1")
    glossary = [
        ("Mode", "one natural pattern: frequency + damping + shape."),
        ("Natural frequency", "where the mode amplifies most."),
        ("Mode shape", "the pattern: relative amplitudes / phases."),
        ("Damping", "energy loss per cycle; sets peak width / height."),
        ("FRF", "complex output / input vs frequency."),
        ("Drive point", "FRF with force and response at the same DOF."),
        ("Cross FRF", "force and response at different DOFs."),
        ("Anti-resonance", "valley between peaks (drive-point)."),
        ("Reciprocity", "hij = hji."),
        ("Node", "zero-motion line / point of a mode."),
        ("Reference", "the fixed DOF of a row / column survey."),
        ("FFT", "time-to-frequency transform."),
        ("Leakage", "smearing when the record is not periodic-in-window."),
        ("Window", "taper weighting that fakes periodicity."),
        ("Aliasing", "high-frequency fold-back from bad sampling / filtering."),
        ("ADC / quantization", "digitizer; bit depth sets amplitude resolution."),
        ("Auto / cross spectrum", "averaged building blocks of FRF / coherence."),
        ("Coherence", "0-to-1 data-quality meter."),
        ("Burst random / sine chirp / random", "shaker signals (S1.5)."),
        ("Peak-picking", "reading shapes from imag-peak heights."),
        ("Curvefitting", "decomposing FRFs into SDOF contributions (+ residuals)."),
        ("Residual", "out-of-band modes' leftover influence."),
        ("ODS", "operating deflection shape: response-only shape at one frequency."),
        ("SDM", "predicting design changes from the modal model."),
        ("FEM correlation", "validating / updating simulation with modal test data."),
    ]
    for term, defn in glossary:
        s.append(P(f"<b>{term}</b> - {defn}", small))
    s.append(Spacer(1, 10))
    s.append(P("Council sign-off: Meera (theory) ok - Viktor (lab) ok - Lena "
               "(signals) ok - Arjun (pedagogy) ok - Sofia (field) ok. "
               "Notes are original summaries; approximations labelled. "
               "Next stop: Ch.2, the math!", center))
    return s


def main() -> None:
    from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
    doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=ML,
                          rightMargin=MR, topMargin=MT, bottomMargin=MB,
                          title="Ch.1 Handwritten Notes - Modal Testing",
                          author="Modal Notes Council")
    frame = Frame(ML, MB, FRAME_W, PAGE_H - MT - MB, id="main")
    doc.addPageTemplates([PageTemplate(id="pg", frames=[frame], onPage=bg)])
    doc.build(build_story())
    print(f"Wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
