"""Build creative handwritten-style PDF notes for Chapter 2 (theory chapter).

Usage:  python3 modal-notes/make_ch2_pdf.py   (run from repo root)
Output: modal-notes/chapter-02-handwritten-notes.pdf
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from reportlab.graphics.shapes import (Circle, Drawing, Line, PolyLine, Rect,
                                       String)
from reportlab.lib import colors

import make_handwritten_pdf as _MHW
_MHW.CHAPTER_LABEL = "Ch.2"

from make_handwritten_pdf import (BLUE, FRAME_W, GREEN, INK, MB, ML, MR, MT,
                                  PALE_BLUE, PALE_GREEN, PALE_PINK,
                                  PALE_YELLOW, PAPER, RED, bg, body, box,
                                  bullet, center, cover_sub, cover_title, F,
                                  formula_text, h3, heading, hl, key, lab,
                                  link, P, small, tbl, trap, tryit, B)

HERE = pathlib.Path(__file__).parent
OUT = HERE / "chapter-02-handwritten-notes.pdf"
GRAY = colors.HexColor("#44507A")


def panel(w: float, h: float, caption: str) -> Drawing:
    d = Drawing(w, h)
    d.add(Rect(0, 0, w, h, fillColor=colors.white, strokeColor=INK,
               strokeWidth=1.2))
    d.add(String(8, h - 15, caption, fontName="Kalam", fontSize=9,
                 fillColor=GRAY))
    return d


def S(d: Drawing, x: float, y: float, t: str, size: float = 9.5,
      color=INK, bold: bool = False) -> None:
    d.add(String(x, y, t, fontName="KalamB" if bold else "Kalam",
                 fontSize=size, fillColor=color))


def arrow(d: Drawing, x1: float, y1: float, x2: float, y2: float,
          color=INK, width: float = 1.8) -> None:
    d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=width))
    dx, dy = x2 - x1, y2 - y1
    L = max(1e-6, (dx * dx + dy * dy) ** 0.5)
    ux, uy = dx / L, dy / L
    s = 7
    d.add(Line(x2, y2, x2 - ux * s - uy * s * 0.45,
               y2 - uy * s + ux * s * 0.45, strokeColor=color,
               strokeWidth=width))
    d.add(Line(x2, y2, x2 - ux * s + uy * s * 0.45,
               y2 - uy * s - ux * s * 0.45, strokeColor=color,
               strokeWidth=width))


# ---------- sketches 1-6 ----------
def sdof_sketch() -> Drawing:
    w, h = FRAME_W, 148
    d = panel(w, h, "my sketch: the SDOF machine")
    d.add(Line(60, 30, 60, 115, strokeColor=INK, strokeWidth=2.4))  # wall
    for yy in (38, 52, 66, 80, 94, 108):
        d.add(Line(60, yy, 48, yy - 8, strokeColor=INK, strokeWidth=1.2))
    spring = [60, 96, 72, 104, 84, 88, 96, 104, 108, 88, 120, 104, 132, 88,
              144, 104, 156, 96]
    d.add(PolyLine(spring, strokeColor=BLUE, strokeWidth=2.2,
                   strokeLineJoin=1))
    S(d, 92, 110, "k", 11, BLUE, True)
    d.add(Line(60, 52, 120, 52, strokeColor=GREEN, strokeWidth=2.2))
    d.add(Line(120, 40, 120, 64, strokeColor=GREEN, strokeWidth=2.2))
    d.add(Rect(120, 40, 36, 24, fillColor=None, strokeColor=GREEN,
               strokeWidth=2.2))
    d.add(Line(156, 52, 170, 52, strokeColor=GREEN, strokeWidth=2.2))
    S(d, 100, 30, "c", 11, GREEN, True)
    d.add(Rect(170, 34, 110, 76, fillColor=PALE_BLUE, strokeColor=INK,
               strokeWidth=2.4))
    S(d, 208, 66, "m", 14, INK, True)
    arrow(d, 300, 72, 360, 72, RED, 2.4)
    S(d, 366, 68, "f(t)", 11, RED, True)
    arrow(d, 200, 22, 260, 22, INK, 1.8)
    S(d, 266, 18, "x(t)", 10)
    S(d, 300, 100, "m x'' + c x' + k x = f", 10, INK, True)
    return d


def splane_sketch() -> Drawing:
    w, h = FRAME_W, 168
    d = panel(w, h, "my sketch: S-plane, where poles live")
    ox, oy = 150, 70
    arrow(d, 40, oy, 300, oy, INK, 1.6)
    arrow(d, ox, 18, ox, h - 22, INK, 1.6)
    S(d, 228, oy - 15, "real (damping)", 9)
    S(d, ox + 14, h - 22, "imag (freq) jw", 9)
    S(d, ox + 4, oy + 5, "0", 9)
    px, py = 105, 122  # pole upper
    for (qx, qy) in ((px, py), (px, 2 * oy - py)):
        d.add(Line(qx - 6, qy - 6, qx + 6, qy + 6, strokeColor=RED,
                   strokeWidth=2.6))
        d.add(Line(qx - 6, qy + 6, qx + 6, qy - 6, strokeColor=RED,
                   strokeWidth=2.6))
    d.add(Line(ox, oy, px, py, strokeColor=BLUE, strokeWidth=1.6))
    S(d, 118, 88, "radius = wn", 9, BLUE)
    arc = []
    import math
    R = ((ox - px) ** 2 + (py - oy) ** 2) ** 0.5
    a0 = math.atan2(py - oy, px - ox)
    for k in range(13):
        a = a0 + (math.pi / 2 - a0) * k / 12
        arc += [ox + R * math.cos(a), oy + R * math.sin(a)]
    pl = PolyLine(arc, strokeColor=GREEN, strokeWidth=1.8)
    pl.strokeDashArray = [4, 3]
    d.add(pl)
    S(d, 168, 128, "more damping: pole marches west", 9, GREEN)
    S(d, 318, 110, "pole =", 10, RED, True)
    S(d, 318, 96, "-z wn + j wd", 10, RED, True)
    S(d, 318, 74, "real: decay", 9)
    S(d, 318, 60, "imag: ring freq", 9)
    S(d, 318, 38, "undamped: ON jw!", 9, GREEN)
    return d


def dynamp_sketch() -> Drawing:
    w, h = FRAME_W, 158
    d = panel(w, h, "my sketch: dynamic amplification + phase (3 dampings)")
    arrow(d, 30, 24, 225, 24, INK, 1.4)
    arrow(d, 30, 24, 30, h - 24, INK, 1.4)
    S(d, 36, h - 30, "X/Xst vs b=w/wn", 9)
    curves = [([30, 30, 70, 34, 100, 55, 118, 118, 136, 55, 170, 32, 210, 28],
               RED, "z=.05"),
              ([30, 30, 70, 33, 100, 48, 118, 74, 136, 48, 170, 31, 210, 28],
               BLUE, "z=.2"),
              ([30, 30, 80, 32, 118, 42, 160, 34, 210, 28], GREEN, "z=.7")]
    for pts, col, lab_ in curves:
        d.add(PolyLine(pts, strokeColor=col, strokeWidth=2.2,
                       strokeLineJoin=1))
    S(d, 150, 108, "z=.05", 9, RED)
    S(d, 150, 70, "z=.2", 9, BLUE)
    S(d, 228 - 60, 24 + 130, "", 9)
    arrow(d, 255, 24, 450, 24, INK, 1.4)
    arrow(d, 255, 24, 255, h - 24, INK, 1.4)
    S(d, 261, h - 30, "phase: 0 -> 90 -> 180 deg", 9)
    d.add(PolyLine([255, 118, 300, 116, 335, 100, 352, 72, 369, 44, 404, 28,
                    450, 26], strokeColor=RED, strokeWidth=2.2,
                   strokeLineJoin=1))
    d.add(PolyLine([255, 118, 290, 112, 330, 88, 352, 72, 375, 56, 415, 34,
                    450, 30], strokeColor=BLUE, strokeWidth=1.8,
                   strokeLineJoin=1))
    dl = Line(352, 24, 352, 118, strokeColor=INK, strokeWidth=1.2)
    dl.strokeDashArray = [4, 3]
    d.add(dl)
    S(d, 356, 76, "90 deg!", 9, RED, True)
    S(d, 228, 8, "b = w/wn ->", 9)
    return d


def halfpower_sketch() -> Drawing:
    w, h = FRAME_W, 148
    d = panel(w, h, "my sketch: half-power + log-dec (damping quickies)")
    arrow(d, 24, 26, 230, 26, INK, 1.4)
    d.add(PolyLine([24, 30, 70, 32, 105, 70, 127, 118, 149, 70, 184, 32,
                    230, 30], strokeColor=BLUE, strokeWidth=2.4,
                   strokeLineJoin=1))
    pk = 118
    hp = 30 + (pk - 30) / 1.414
    hl = Line(24, hp, 230, hp, strokeColor=RED, strokeWidth=1.2)
    hl.strokeDashArray = [4, 3]
    d.add(hl)
    for xx in (105, 149):
        vl = Line(xx, 26, xx, hp, strokeColor=RED, strokeWidth=1.2)
        vl.strokeDashArray = [3, 3]
        d.add(vl)
    S(d, 92, 12, "w1", 9, RED)
    S(d, 142, 12, "w2", 9, RED)
    arrow(d, 105, 44, 149, 44, RED, 1.4)
    S(d, 100, 50, "Dw", 9, RED, True)
    S(d, 30, h - 28, "z = Dw/(2wn)", 9.5, RED, True)
    arrow(d, 258, 60, 452, 60, INK, 1.4)
    d.add(PolyLine([258, 60, 275, 100, 292, 60, 309, 96, 326, 60, 343, 90,
                    360, 60, 377, 84, 394, 60, 411, 79, 428, 60, 445, 75],
                   strokeColor=GREEN, strokeWidth=2.0, strokeLineJoin=1))
    S(d, 264, h - 28, "log-dec: d = ln(x1/x2)", 9.5, GREEN, True)
    arrow(d, 275, 88, 275, 100, GREEN, 1.2)
    S(d, 278, 92, "x1", 8, GREEN)
    arrow(d, 309, 84, 309, 96, GREEN, 1.2)
    S(d, 312, 88, "x2", 8, GREEN)
    return d


def forcebalance_sketch() -> Drawing:
    w, h = FRAME_W, 158
    d = panel(w, h, "my sketch: who balances F? (force vectors)")
    titles = ["w << wn: STATIC-like", "w = wn: DAMPING only!", "w >> wn: MASS rules"]
    cols = [30, 180, 330]
    descs = [["F ->", "opposed by Kx"], ["Kx, inertia", "CANCEL: only c"], ["F ->", "opposed by m w2x"]]
    for t, x, dd in zip(titles, cols, descs):
        S(d, x, h - 30, t, 8.5, INK, True)
        d.add(Rect(x - 6, 22, 138, 92, fillColor=None, strokeColor=GRAY,
                   strokeWidth=1.0))
        S(d, x, 88, dd[0], 9, RED, True)
        S(d, x, 72, dd[1], 9, BLUE)
    arrow(d, 36, 50, 110, 50, RED, 2.6)
    S(d, 112, 46, "F", 9, RED, True)
    arrow(d, 150, 50, 76, 50, BLUE, 2.6)
    S(d, 60, 56, "Kx", 9, BLUE, True)
    arrow(d, 186, 50, 230, 50, RED, 2.2)
    S(d, 232, 46, "F", 9, RED, True)
    arrow(d, 300, 50, 262, 50, GREEN, 2.2)
    S(d, 268, 56, "cwx", 9, GREEN, True)
    arrow(d, 243, 62, 243, 88, BLUE, 1.6)
    S(d, 246, 78, "Kx", 8, BLUE)
    arrow(d, 243, 40, 243, 14 + 0, BLUE, 1.6)
    S(d, 246, 26, "mwx", 8, BLUE)
    S(d, 186, 100, "cancel!", 8.5, RED, True)
    arrow(d, 336, 50, 410, 50, RED, 2.6)
    S(d, 412, 46, "F", 9, RED, True)
    arrow(d, 452, 50, 378, 50, BLUE, 2.6)
    S(d, 380, 56, "mwx", 9, BLUE, True)
    return d


def nyquist_sketch() -> Drawing:
    w, h = FRAME_W, 148
    d = panel(w, h, "my sketch: Nyquist circle (imag vs real)")
    arrow(d, 60, 40, 300, 40, INK, 1.5)
    arrow(d, 110, 20, 110, h - 20, INK, 1.5)
    S(d, 302, 36, "real", 9)
    S(d, 114, h - 24, "imag", 9)
    import math
    cx, cy, R = 180, 62, 44
    pts = []
    for k in range(25):
        a = -math.pi / 2 + 2 * math.pi * k / 24
        pts += [cx + R * math.cos(a), cy + R * math.sin(a)]
    d.add(PolyLine(pts, strokeColor=BLUE, strokeWidth=2.4,
                   strokeLineJoin=1))
    d.add(Circle(cx, cy + R, 3.5, fillColor=RED, strokeColor=RED))
    S(d, cx + 8, cy + R - 2, "RES: max imag, real=0", 9, RED, True)
    d.add(Circle(cx - R, cy, 3, fillColor=GREEN, strokeColor=GREEN))
    d.add(Circle(cx + R, cy, 3, fillColor=GREEN, strokeColor=GREEN))
    S(d, cx - R - 58, cy + 6, "hp", 9, GREEN, True)
    S(d, cx + R + 4, cy - 12, "hp", 9, GREEN, True)
    S(d, cx - 30, cy - 30, "90 deg apart!", 9, GREEN)
    d.add(Circle(110, 40, 2.5, fillColor=INK, strokeColor=INK))
    S(d, 116, 28, "origin", 8.5)
    S(d, 330, 100, "clean circle =", 10, BLUE, True)
    S(d, 330, 86, "clean mode!", 10, BLUE, True)
    S(d, 330, 64, "potato = trouble", 9.5, RED, True)
    S(d, 330, 50, "(overlap/noise/", 8.5)
    S(d, 330, 38, "nonlinearity)", 8.5)
    return d

# ---------- sketches 7-11 ----------
def regions_sketch() -> Drawing:
    w, h = FRAME_W, 158
    d = panel(w, h, "my sketch: D/F regions + slopes (log-log)")
    arrow(d, 40, 26, 440, 26, INK, 1.5)
    arrow(d, 40, 26, 40, h - 20, INK, 1.5)
    d.add(PolyLine([40, 96, 130, 96, 175, 92, 205, 82, 222, 128, 239, 74,
                    270, 56, 340, 44, 430, 32], strokeColor=BLUE,
                   strokeWidth=2.4, strokeLineJoin=1))
    for xx in (196, 248):
        zl = Line(xx, 26, xx, 118, strokeColor=GRAY, strokeWidth=1.0)
        zl.strokeDashArray = [4, 3]
        d.add(zl)
    S(d, 62, 102, "STIFFNESS", 9.5, BLUE, True)
    S(d, 82, 90, "slope 0", 8.5)
    S(d, 196, 132, "DAMPING", 8.5, RED, True)
    S(d, 300, 66, "MASS", 9.5, BLUE, True)
    S(d, 292, 54, "slope -2", 8.5)
    S(d, 150, 10, "frequency (log) ->", 9)
    S(d, 276, h - 28, "V/F: +1/-1  A/F: +2/0", 9, GREEN, True)
    return d


def mdofsum_sketch() -> Drawing:
    w, h = FRAME_W, 168
    d = panel(w, h, "my sketch: FRF = sum of modal SDOF humps")
    d.add(PolyLine([40, 118, 90, 118, 120, 90, 140, 140, 160, 100, 200, 116,
                    230, 88, 250, 136, 270, 100, 310, 114, 335, 94, 355, 130,
                    375, 104, 420, 112, 450, 112], strokeColor=INK,
                   strokeWidth=2.4, strokeLineJoin=1))
    S(d, 46, 146, "SUMMED FRF (what you measure)", 9, INK, True)
    humps = [([40, 30, 90, 30, 120, 60, 140, 92, 160, 60, 200, 30], BLUE, "M1"),
             ([200, 30, 230, 55, 250, 88, 270, 55, 310, 30], RED, "M2"),
             ([310, 30, 335, 52, 355, 80, 375, 52, 420, 30], GREEN, "M3")]
    for pts, col, lab_ in humps:
        d.add(PolyLine(pts, strokeColor=col, strokeWidth=2.2,
                       strokeLineJoin=1))
        S(d, pts[4] - 8, 14, lab_, 9, col, True)
    S(d, 188, 52, "+", 12, INK, True)
    S(d, 296, 52, "+", 12, INK, True)
    S(d, 428, 52, "=", 12, INK, True)
    arrow(d, 448, 60, 448, 112, INK, 1.6)
    return d


def xform_sketch() -> Drawing:
    w, h = FRAME_W, 128
    d = panel(w, h, "my sketch: modal transformation round-trip")
    boxes = [("COUPLED:", "[M]x''+[C]x'+[K]x=F", BLUE),
             ("UNCOUPLE:", "x = [U] p", GREEN),
             ("m tiny SDOFs:", "mi p''+ci p'+ki p=fi", RED)]
    xs = [14, 180, 322]
    for (t1, t2, col), x in zip(boxes, xs):
        d.add(Rect(x, 40, 140, 56, fillColor=colors.white,
                   strokeColor=col, strokeWidth=2.0))
        S(d, x + 8, 78, t1, 8.5, col, True)
        S(d, x + 8, 62, t2, 8.5)
    arrow(d, 154, 68, 180, 68, INK, 1.8)
    arrow(d, 320 - 18 + 18, 68, 322, 68, INK, 1.8)
    S(d, 150, 100, "modal superposition!", 10, INK, True)
    back = Line(392, 40, 392, 22, strokeColor=RED, strokeWidth=1.4)
    back.strokeDashArray = [4, 3]
    d.add(back)
    d.add(Line(392, 22, 84, 22, strokeColor=RED, strokeWidth=1.4))
    d.add(Line(84, 22, 84, 40, strokeColor=RED, strokeWidth=1.4))
    S(d, 200, 8, "project back: x = [U]p, then ADD", 9, RED, True)
    return d


def domains_sketch() -> Drawing:
    w, h = FRAME_W, 118
    d = panel(w, h, "my sketch: 3 doors, 1 room")
    boxes = [("TIME", "sum of decaying", "sines", BLUE),
             ("FREQUENCY", "sum of SDOF", "oscillators", RED),
             ("MODAL", "shapes + SDOF", "engines", GREEN)]
    xs = [14, 180, 346]
    for (t1, t2, t3, col), x in zip(boxes, xs):
        d.add(Rect(x, 22, 120, 66, fillColor=colors.white,
                   strokeColor=col, strokeWidth=2.0))
        S(d, x + 8, 70, t1, 9.5, col, True)
        S(d, x + 8, 56, t2, 8.5)
        S(d, x + 8, 43, t3, 8.5)
    for x1, x2 in ((134, 180), (300, 346)):
        arrow(d, x1, 62, x2, 62, INK, 1.4)
        arrow(d, x2, 48, x1, 48, INK, 1.4)
    return d


def fullloop_sketch() -> Drawing:
    w, h = FRAME_W, 168
    d = panel(w, h, "my sketch: the whole EMA loop (Fig-2.55 spirit)")
    top = [("FEM", "assume M,K"), ("EIG", "freq+shape"), ("LAPLACE", "H(s)"),
           ("POLES+RES", "extract"), ("FRF", "synthesize")]
    x = 12
    for t1, t2 in top:
        d.add(Rect(x, 96, 84, 44, fillColor=PALE_BLUE, strokeColor=BLUE,
                   strokeWidth=1.6))
        S(d, x + 6, 124, t1, 8.5, BLUE, True)
        S(d, x + 6, 110, t2, 8)
        x += 92
    for xa, xb in ((96, 104), (188, 196), (280, 288), (372, 380)):
        arrow(d, xa, 118, xb, 118, BLUE, 1.4)
    S(d, 12, 146, "FORWARD: predict", 9, BLUE, True)
    bot = [("MEASURE", "F + X"), ("FFT", "time->freq"), ("RATIO", "H=X/F"),
           ("CURVEFIT", "poles+res"), ("VALIDATE", "fix FEM")]
    x = 12
    for t1, t2 in bot:
        d.add(Rect(x, 26, 84, 44, fillColor=PALE_YELLOW, strokeColor=GREEN,
                   strokeWidth=1.6))
        S(d, x + 6, 54, t1, 8.5, GREEN, True)
        S(d, x + 6, 40, t2, 8)
        x += 92
    for xa, xb in ((96, 104), (188, 196), (280, 288), (372, 380)):
        arrow(d, xa, 48, xb, 48, GREEN, 1.4)
    S(d, 12, 76, "BACKWARD: identify", 9, GREEN, True)
    arrow(d, 440, 100, 440, 66, RED, 1.8)
    arrow(d, 452, 66, 452, 100, RED, 1.8)
    S(d, 408, 80, "compare!", 8.5, RED, True)
    return d

# ---------- content A ----------
def build_story() -> list:
    from reportlab.platypus import PageBreak, Paragraph, Spacer, KeepTogether
    s: list = []

    # ===== COVER =====
    s += [Spacer(1, 26),
          P("Modal Testing: A Practitioner's Guide", cover_sub),
          P("Ch. 2 - General Theory<br/>of Experimental Modal Analysis",
            cover_title),
          P("detailed handwritten-style notes - equations that run the lab",
            cover_sub),
          Spacer(1, 8),
          box("Whole chapter in 1 line:",
              "Everything measured (FRF) = <b>POLES</b> (where modes live: "
              "damping + frequency) + <b>RESIDUES</b> (how strongly each "
              "mode shows at each point). Curvefitting = hunting these two. "
              "Ch.1 pictures become Ch.2 machines.", BLUE, PALE_BLUE),
          box("How to use:",
              "Read S0, then 2.2 slowly (SDOF is the alphabet), then 2.3 "
              "(MDOF = teams of SDOFs). Do every [TRY] and worked example "
              "EX1-EX7 with a calculator. End with the self-test!",
              GREEN, PALE_GREEN),
          P("<b>Legend:</b> <font color=\"#2F6FED\"><b>[KEY]</b></font> key "
            "&nbsp; <font color=\"#1F9D55\"><b>[LAB]</b></font> lab"
            " &nbsp; <font color=\"#E5484D\"><b>[TRAP]</b></font> trap"
            " &nbsp; <font color=\"#7A4FD0\"><b>[LINK]</b></font> bridge"
            " &nbsp; <font color=\"#B26A00\"><b>[TRY]/EX</b></font> do it",
            center),
          P("Council crew: Dr. Meera K. (theory) - Dr. Viktor H. (lab) - "
            "Dr. Lena F. (signals) - Prof. Arjun D. (pedagogy) - "
            "Dr. Sofia M. (field) &nbsp;|&nbsp; 11 Sep 2026", small)]
    s.append(PageBreak())

    # ===== S0 =====
    s += heading("(0)", "Primer - Ch.1 pictures become Ch.2 machines")
    s.append(tbl([
        ["Ch.1 picture", "Ch.2 machine"],
        ["FRF peaks at natural frequencies", "POLES s = -z wn + j wd (damping + freq)"],
        ["Imag-peak heights trace shape", "RESIDUES Aijr ~ shape-i x shape-j"],
        ["One row/column is enough", "PROVEN by transfer-matrix symmetry"],
        ["FRF = hidden SDOFs summed", "DERIVED: hij = sum over modes"],
        ["Curvefitting finds f, z, shapes", "Curvefitting finds POLES + RESIDUES"],
    ], [FRAME_W * 0.42, FRAME_W * 0.58]))
    s.append(box("Warm-up:",
                 tryit("Write your SDOF equation from memory: "
                 "<b>m x'' + c x' + k x = f(t)</b>. Every 2.2 equation is "
                 "this one in costume; every 2.3 equation is a TEAM of "
                 "these, uncoupled by a clever coordinate change."),
                 GREEN, PALE_GREEN))

    # ===== 2.1 =====
    s += heading("(2.1)", "Introduction - two models, one truth")
    s.append(tbl([
        ["", "FEM (analytical)", "EMA (experimental)"],
        ["Starts from", "Assumed M, K layout", "Measured force + response"],
        ["Gives", "Freqs + shapes via EIGENSOLUTION", "f, z, shapes via CURVEFITTING"],
        ["Strength", "Design-stage what-ifs, no hardware", "Ground truth of real structure"],
        ["Weakness", "Wrong assumptions = wrong modes", "Bad measurements = wrong params"],
    ], [FRAME_W * 0.18, FRAME_W * 0.41, FRAME_W * 0.41]))
    s.append(box("The loop that matters:",
                 key("Build FEM -> predict -> TEST -> <b>verify/correct FEM "
                 "with modal data</b> -> trusted model. EMA boomed since "
                 "the 1980s (cheap analyzers, MIMO, better estimators, "
                 "OMA). Ch.2 is the theory core making it legitimate.")
                 + "<br/>Sofia: 'Nobody pays for theory. They pay for the "
                 "moment the test proves the FEM wrong BEFORE the prototype "
                 "fails.'", BLUE, PALE_BLUE))

    # ===== 2.2 =====
    s += heading("(2.2)", "SDOF theory - the alphabet")
    s.append(F(formula_text("m x'' + c x' + k x = f(t)   (linear, time-invariant)")))
    s.append(P("Lumped mass m, linear spring k x, viscous damper c x'. "
               + trap("<b>All of Ch.2 assumes LINEARITY.</b> Gaps, friction, "
               "loose joints break it - later chapters teach detecting that. "
               "For now: linear or nothing works.")))
    s.append(KeepTogether(sdof_sketch()))
    s.append(P("Free vibration trial x = X e^(st) gives the <b>characteristic "
               "equation</b> and two roots = <b>poles</b>. Three damping "
               "cases exist; your career lives in <b>underdamped (z &lt; 1)</b>:" ))
    s.append(F(formula_text("poles: s = -z wn +- j wd,   wd = wn sqrt(1-z^2)")))
    s.append(F(formula_text("wn = sqrt(k/m),   z = c/cc,   cc = 2 m wn = 2 sqrt(k m)")))
    s.append(box("Pole anatomy - tattoo this:",
                 key("<b>Real part (-z wn)</b> = decay rate = damping. "
                 "<b>Imag part (wd)</b> = ringing frequency. Poles come in "
                 "<b>complex-conjugate pairs</b>. Light damping (under 10%): "
                 "wd ~ wn. And wn itself does not care about damping!"),
                 BLUE, PALE_BLUE))
    s.append(box("EX1 - feel the numbers:",
                 "<b>m = 2 kg, k = 8000 N/m, c = 8:</b> wn = sqrt(8000/2) = "
                 "63.2 rad/s -> fn ~ 10.1 Hz. cc = 2*2*63.2 ~ 253. "
                 "z = 8/253 ~ 0.032 (3.2% - typical welded steel!). Poles: "
                 "-2 +- j63.2. Peak gain Q ~ 1/(2z) ~ <b>16x</b>. THAT is "
                 "why resonance breaks things.",
                 colors.HexColor("#B26A00"), PALE_YELLOW))
    s += heading("(S-plane)", "Where poles live")
    s.append(KeepTogether(splane_sketch()))
    s.append(B("<b>Undamped:</b> poles ON the jw axis (eternal sine - never "
               "real, shown for completeness)."))
    s.append(B("<b>More damping:</b> poles march <b>left</b> on a "
               "<b>circular arc</b>; wd shrinks. Critical: pair collides on "
               "the real axis. Overdamped: splits into two real poles."))
    s.append(P(key("<b>Radius origin-to-pole = wn.</b> Angle encodes z. ") +
               link("The S-plane is a MAP, poles are CITIES. Damping pushes "
               "cities west; stiffness pushes them north. Your FRF is the "
               "view from the jw highway.")))
    s += heading("(Forced)", "Amplification + the 90-degree signature")
    s.append(F(formula_text("X/Xstatic = 1/sqrt((1-b^2)^2 + (2 z b)^2),  b = w/wn")))
    s.append(KeepTogether(dynamp_sketch()))
    s.append(B("Light damping: peak at wd ~ wn with height ~ 1/(2z). Phase "
               "lag force->response: 0 deg -> <b>90 deg AT resonance</b> -> "
               "180 deg."))
    s.append(P(key("The <b>90-degree lag at resonance</b> is your most "
                   "robust resonance detector - peaks can lie (noise, "
                   "leakage), 90 deg rarely does.")))
    s += heading("(Damping)", "Half-power + log-dec: know, then outgrow")
    s.append(KeepTogether(halfpower_sketch()))
    s.append(F(formula_text("HALF-POWER: z ~ (w2 - w1)/(2 wn) = Dw/(2wn)")))
    s.append(F(formula_text("LOG-DEC: d = ln(x1/x2) ~ 2 pi z")))
    s.append(B("<b>Half-power (freq):</b> peak/sqrt(2) points w1, w2. Wider "
               "peak = more damping. On IMAG part: half-height points; same "
               "points = REAL-part peaks; on Nyquist: <b>90 deg around the "
               "circle</b> from resonance."))
    s.append(B("<b>Log-dec (time):</b> pluck it, watch ring-down over n "
               "cycles: d = ln(x1/xn+1)/n."))
    s.append(box("The book's honest verdict:",
                 trap("Historically important, exam-favorite - but real "
                 "responses are almost never single-mode, so single-mode "
                 "tricks mislead. ") + lab("The professional answer: "
                 "<b>modal parameter estimation</b> (least-squares fit of "
                 "poles + residues). Quickies for sanity checks and "
                 "interviews; curvefitters for paychecks. - Viktor"),
                 RED, PALE_PINK))
    s.append(P(tryit("EX2 - 10 seconds: peak 100 Hz, half-power at 99/101: "
                     "z ~ (101-99)/(2*100) = 1%. Q ~ 50. Lightly damped - "
                     "mind your leakage (Ch.1 flashback)!")))
    s += heading("(Forces)", "Why resonance is a damping-only fight")
    s.append(KeepTogether(forcebalance_sketch()))
    s.append(tbl([
        ["Excitation", "Balance", "FRF region"],
        ["w &lt;&lt; wn", "F ~ Kx (looks STATIC)", "Stiffness-controlled"],
        ["w = wn", "Kx and m w2x CANCEL - only damping opposes F", "Damping-controlled"],
        ["w >> wn", "F ~ m w2x (inertia rules)", "Mass-controlled"],
    ], [FRAME_W * 0.2, FRAME_W * 0.48, FRAME_W * 0.32]))
    s.append(box("Deepest insight of 2.2:",
                 key("At resonance, <b>stiffness and inertia annihilate each "
                 "other; damping alone holds the bridge.</b> That is why the "
                 "peak measures damping and NOTHING else.")
                 + "<br/><b>EX3 with numbers</b> (EX1 at wn=63.2, X=1mm): "
                 "elastic KX = 8 N; inertia m w2 X = 8 N - equal, opposite, "
                 "GONE. Damping c w X ~ 0.5 N balances everything. 8 N vs "
                 "0.5 N: light damping = giant response.",
                 BLUE, PALE_BLUE))
    s += heading("(Laplace)", "One system, three costumes")
    s.append(B("<b>1. Polynomial:</b> H(s) = 1/(m s2 + c s + k) - straight "
               "from the equation."))
    s.append(B("<b>2. Pole-zero:</b> factored, roots exposed - poles = "
               "denominator roots."))
    s.append(B("<b>3. Partial fraction:</b> sum of residue/(s - pole) - "
               "screams 'ready for modal testing.'"))
    s.append(P(key("Same information, three outfits - NO new physics, just "
                   "convenience. Inverse-Laplace the impulse: decaying "
                   "exponentials e^(-z wn t) sin(wd t) - time-domain twin.")))
    s.append(box("Residue = the number that carries the shape:",
                 "H(s) explodes AT its poles (divide by zero) - the "
                 "<b>residue theorem</b> extracts each pole's finite "
                 "strength. SDOF: a constant. MDOF: a MATRIX carrying every "
                 "mode shape. " + hl("POLE + RESIDUE = complete DNA: "
                 "rebuild the surface everywhere + the FRF at every f."),
                 BLUE, PALE_BLUE))
    s += heading("(FRF)", "A slice of the surface at s = jw")
    s.append(P("Picture H(s) as a tent over the S-plane with infinite spikes "
               "over each pole. The FRF is the <b>slice along the jw "
               "axis</b> - walk it with a knife; the cut edge is your "
               "measurement. Near-axis poles (light damping) = tall sharp "
               "slices."))
    s.append(tbl([
        ["Portrait", "Shows", "Resonance reads as"],
        ["Bode (mag + phase)", "Peak + 90 deg, 180 total flip", "Peak + 90 deg crossing"],
        ["Co-quad (real + imag)", "Real crosses ZERO, imag PEAKS", "Imag peak, real = 0"],
        ["Nyquist (imag vs real)", "Near-CIRCLE", "Opposite origin; hp pts 90 deg around"],
    ], [FRAME_W * 0.26, FRAME_W * 0.4, FRAME_W * 0.34]))
    s.append(KeepTogether(nyquist_sketch()))
    s.append(P(lab("Learn to love Nyquist. Clean circle = clean mode. A "
                   "POTATO = overlapping modes, noise, or nonlinearity "
                   "telling you to slow down. - Lena")))
    s += heading("(Forms)", "D/F, V/F, A/F: the slope detective kit")
    s.append(KeepTogether(regions_sketch()))
    s.append(tbl([
        ["Name", "Symbol", "From D/F", "Stiff slope", "Mass slope"],
        ["Compliance", "D/F", "-", "0 (flat)", "-2"],
        ["Mobility", "V/F", "x jw", "+1", "-1"],
        ["Inertance", "A/F", "x (jw)^2 = -w2", "+2", "0 (flat)"],
    ], [FRAME_W * 0.2, FRAME_W * 0.14, FRAME_W * 0.28, FRAME_W * 0.19,
        FRAME_W * 0.19]))
    s.append(P(key("A/F = -w2 (D/F): acceleration and displacement are "
                   "<b>180 deg apart</b>, scaled by w2. ") +
               lab("<b>Detective trick:</b> unlabeled plot? Far-left/right "
               "slopes (0,-2)=D, (+1,-1)=V, (+2,0)=A. Catches instrument "
               "mix-ups in seconds.")))
    s.append(P(tryit("EX4 - name that plot: low end rises +2/decade, high "
                     "end flat -> A/F accelerance - your everyday "
                     "hammer + accelerometer FRF!")))

    # ===== 2.3 =====
    s.append(PageBreak())
    s += heading("(2.3)", "MDOF theory - the main event")
    s += [P("Coupled equations in matrix form (start: 2DOF):", h3)]
    s.append(F(formula_text("[M]{x''} + [C]{x'} + [K]{x} = {F}")))
    s.append(P("Mass-1's equation contains mass-2's motion and back - "
               "<b>coupled</b>. " + key("<b>Off-diagonals of C and K ARE "
               "the coupling.</b> All matrices <b>square + symmetric</b> - "
               "the seed of reciprocity and of Ch.1's one-row/column rule. "
               "Linear + time-invariant, same honesty clause.")))
    s += [P("Eigensolution: frequencies + shapes fall out together:", h3)]
    s.append(F(formula_text("([K] - w2[M]){u} = 0   ->   det([K] - L[M]) = 0")))
    s.append(B("<b>1. Determinant</b> = polynomial -> roots = eigenvalues "
               "(freqs squared). Small: Jacobi/Givens/Householder. Giant "
               "FEM: iterative, lowest modes only (subspace/Lanczos)."))
    s.append(B("<b>2. Substitute</b> L1 = w1^2 back, solve (Crout/Cholesky/"
               "LDL) -> vector IS <b>mode shape 1</b>. Repeat per mode."))
    s.append(B("<b>3. Physics:</b> at each solution elastic = inertial "
               "forces: <b>dynamic equilibrium</b>, oscillating about "
               "<b>nodes</b>, equal +/- lobes. Mode 1 blue, mode 2 red - "
               "book colors kept!"))
    s.append(P(key("Frequency + vector = <b>EIGENPAIR</b>. Shapes are "
                   "<b>linearly independent + orthogonal</b> wrt M and K - "
                   "the miracle this chapter rides on.")))
    s.append(box("EX5 - 2DOF intuition:",
                 "Two floor masses, three springs. <b>Mode 1:</b> masses "
                 "move TOGETHER (low f, middle spring lazy). <b>Mode 2:</b> "
                 "masses move OPPOSITE (high f, middle spring works hard). "
                 "Two independent dance moves; every real motion = a mix. "
                 "That sentence scales to a million DOFs.",
                 GREEN, PALE_GREEN))
    s += [P("Orthogonality: the uncoupling keys:", h3)]
    s.append(F(formula_text("ui(T)[M]uj = 0,  ui(T)[K]uj = 0   (i != j)")))
    s.append(F(formula_text("ui(T)[M]ui = mi (modal mass),  ui(T)[K]ui = ki")))
    s.append(P("Stack shapes as columns -> <b>modal matrix [U]</b>. Change "
               "coordinates:"))
    s.append(F(formula_text("{x} = [U]{p}   ->   mi p'' + ci p' + ki p = fi")))
    s.append(P("Modal force <b>fi = ui(T) {F}</b>: how hard F pushes mode i. "))
    s.append(KeepTogether(xform_sketch()))
    s.append(box("Why this is THE trick:",
                 key("<b>Each mode becomes its own SDOF.</b> Solve m tiny "
                 "equations (often <b>m &lt;&lt; n</b>: a handful of modes runs a "
                 "million-DOF FEM!), project back with [U], ADD. That "
                 "round-trip = <b>modal superposition</b>, the most-used "
                 "algorithm in structural dynamics.")
                 + "<br/>Viktor: 'Test engineers walk it BACKWARDS: measure "
                 "FRFs -> extract poles/residues -> animate shapes. Same "
                 "bridge.'", BLUE, PALE_BLUE))
    s += [P("Laplace for MDOF: global poles, shape-carrying residues:", h3)]
    s.append(F(formula_text("[H(s)] = [B(s)]^-1 = adj[B(s)] / det[B(s)]")))
    s.append(B("System matrix <b>[B(s)] symmetric</b> (M/C/K are) -> <b>2n "
               "poles</b>, pairs per mode."))
    s.append(P(key("<b>Denominator -> poles: IDENTICAL for every FRF</b> "
                   "(same roots wherever you measure) = <b>GLOBAL "
                   "properties</b>. Numerator -> residue matrix: symmetric, "
                   "gives <b>reciprocity</b>, and at each pole vectors ~ "
                   "the <b>mode shapes</b> - EVERY row AND column valid!")))
    s.append(P(trap("Ch.1's node rule, birth certificate found: reference at "
                    "a node zeroes that mode's residue across the whole "
                    "row/column.")))
    s += [P("The FRF summation - two faces, one equation:", h3)]
    s.append(F(formula_text("hij(jw) = SUM_r  Aijr/(jw - Lr)  [+ conj]  (residue face)")))
    s.append(F(formula_text("hij(jw) = SUM_r  uir ujr / [mr(wr2-w2+j2zrwrw)]  (shape face)")))
    s.append(P("Read the shape face like a story: each mode = its "
               "<b>SDOF amplifier</b> (pure 2.2!) x <b>uir x ujr</b> "
               "(output-shape x input-shape FILTERS). Weak shape at hammer "
               "OR sensor -> mode hides in that FRF."))
    s.append(KeepTogether(mdofsum_sketch()))
    s.append(P("Sine at any f = SUM of modal responses: <b>below all "
               "modes</b> -> mode 1 leads; <b>near mode 2</b> -> mode 2 "
               "takes over; <b>between</b> -> Ch.1's hybrid. Same moral, "
               "now with equations."))
    s += [P("Cantilever, 3 points: the theory on one page:", h3)]
    s.append(tbl([
        ["FRF", "Role", "Watch for"],
        ["h33 (drive, tip)", "Sum of all modal oscillators; peak-valley alternation", "Per-mode decomposition underneath"],
        ["h32, h31 (cross)", "Same poles, new residue weights", "A mode shrinks as force nears its node"],
        ["ROW (roving hammer)", "Fixed accel reference", "Ch.1 table: DERIVED now"],
        ["COLUMN (fixed shaker)", "Fixed force reference", "Read mode 1 down column 3!"],
    ], [FRAME_W * 0.24, FRAME_W * 0.4, FRAME_W * 0.36]))
    s.append(P("Imag-waterfall (tip ref) draws all three shapes in the air. "
               + key("<b>Any row/column works.</b>")))
    s.append(box("EX6 - estimate by hand:",
                 "Mode-1 imag peaks down column 3: [0.4, 1.1, 2.0] -> divide "
                 "by tip: <b>[0.2, 0.55, 1.0]</b> - first-bending shape, "
                 "root to tip. You just did modal parameter estimation with "
                 "a pencil.",
                 colors.HexColor("#B26A00"), PALE_YELLOW))
    s += [P("Time-frequency-modal: three doors, one room:", h3)]
    s.append(KeepTogether(domains_sketch()))
    s.append(P("<b>Time:</b> tip = sum of decaying sines. <b>Freq:</b> FRF = "
               "sum of SDOF oscillators. <b>Modal:</b> decoupled SDOF "
               "engines + shapes. Convert freely - physics never changes, "
               "only your clothes do."))
    s += [P("Turbine blade: the full computation (2.3.9):", h3)]
    s.append(P("Impulse near root (cantilever model), tip response wanted: "
               "eigensolve FEM -> modal m/c/k + modal force per mode -> "
               "solve 3 trivial SDOF time responses -> <b>project back with "
               "shapes</b> -> add. Total tip trace with each mode's share "
               "beneath. " + key("This is EVERY commercial solver's inner "
               "loop.")))
    s.append(P(tryit("EX7 - why truncation works: blade needs 0-50 Hz; "
                     "modes at 8, 22, 47, 130, 260 Hz... keep 3 (m=3 &lt;&lt; n); "
                     "higher modes answer quasi-statically - hello, "
                     "residuals (1.7 callback)!")))

    # ===== 2.4 + REVISION =====
    s += heading("(2.4 + Revision)", "The whole EMA loop + recap")
    s.append(KeepTogether(fullloop_sketch()))
    s.append(B("<b>Forward (predict):</b> assume M,K -> eigensolve -> "
               "Laplace H(s)=adj/det -> poles + residues -> synthesize ANY "
               "FRF."))
    s.append(B("<b>Backward (identify):</b> measure F+X -> FFT -> H=X/F -> "
               "curvefit poles + residues -> validate FEM. SAME math "
               "objects, opposite direction!"))
    s.append(P(key("The gap = modeling error + measurement error. Your "
                   "career = shrinking both. Next: <b>Ch.3</b> signals "
                   "(sampling/leakage/windows), <b>Ch.4</b> excitation "
                   "mastery, <b>Ch.5</b> the curvefitting zoo.")))
    s.append(tbl([
        ["#", "Big idea", "Punchline"],
        ["1", "Pole anatomy", "Real = damping, imag = freq; pairs"],
        ["2", "S-plane map", "Damping pushes west on circle; r = wn"],
        ["3", "Resonance signature", "90 deg lag; K/x cancel; damping resists"],
        ["4", "Damping quickies", "z~Dw/2wn; d~2 pi z; pros fit"],
        ["5", "3 costumes", "Polynomial / pole-zero / partial fractions"],
        ["6", "Residue", "Pole strength; pole+residue = DNA"],
        ["7", "FRF = slice", "H(jw) cut along jw axis"],
        ["8", "3 portraits", "Bode / co-quad / Nyquist circle"],
        ["9", "Regions", "Low stiff, reso damp, high mass"],
        ["10", "D/V/A slopes", "(0,-2)/(+1,-1)/(+2,0): ID any plot"],
        ["11", "Eigensolution", "det->freqs->shapes; equilib.+nodes"],
        ["12", "Uncouple", "x=[U]p; m SDOFs replace n (m&lt;&lt;n)"],
        ["13", "Global poles", "Same denom; residues=shapes+reciprocity"],
        ["14", "FRF sum", "hij = SUM shape-x-shape x SDOF"],
        ["15", "Full loop", "FEM->predict vs test->extract; same objects"],
    ], [FRAME_W * 0.08, FRAME_W * 0.3, FRAME_W * 0.62]))
    s.append(F(formula_text("wn=sqrt(k/m) - s=-zwn+-jwd - z~Dw/2wn - ([K]-w2[M])u=0 - x=[U]p")))

    # ===== SELF-TEST =====
    s.append(PageBreak())
    s += heading("(Self-test)", "10 questions - no peeking!")
    qs = [
        "Pole at -3 +- j40. Give z, wn, wd. Light or heavy damping?",
        "Why does the resonance peak measure damping and nothing else?",
        "Half-power at 49.5/50.5 Hz, peak 50 Hz. Estimate z and Q.",
        "Real part zero + imaginary peak at some frequency. What is it?",
        "Nyquist looks like a potato, not a circle. List 3 suspects.",
        "Unlabeled FRF: flat low end, -2 slope high end. Which form? Get V/F?",
        "Why are poles 'global' but residues 'local'?",
        "Reference at a mode's node kills it - prove in one line from hij.",
        "200k-DOF FEM, response to 100 Hz, 12 modes below. How many equations? Rest?",
        "FEM says 88 Hz, test says 82 Hz. One modeling + one test suspect?",
    ]
    for i, q in enumerate(qs, 1):
        s.append(Paragraph(f"<b>Q{i}.</b> {q}", bullet, bulletText="*"))
    s += [P("Answers (really no peeking!):", h3)]
    ans = [
        "wd=40, z wn=3 -> wn~40.1, z~7.5% - moderate.",
        "At wn, elastic/inertial forces cancel exactly; only c w X opposes F.",
        "z~(50.5-49.5)/(2*50)=1%; Q~50.",
        "Resonance on a co-quad plot (clean, separated mode).",
        "Overlapping modes, noise/leakage, nonlinearity (or calibration).",
        "D/F compliance. Multiply by jw.",
        "Poles = denominator roots, same all i,j; residues = numerator, per pair.",
        "ujr = 0 at node -> every uir x ujr = 0 for mode r. QED.",
        "12 modal SDOFs; higher modes quasi-static via residuals.",
        "Modeling: wrong BCs / M-K layout. Test: mass loading, calibration, temperature.",
    ]
    for i, a in enumerate(ans, 1):
        s.append(P(f"<b>A{i}.</b> {a}", small))
    s.append(box("Theory-to-lab checklist:",
                 "<b>Before:</b> predict band + mode count? reference off "
                 "expected nodes? A/F or V/F - slope-check first plot?"
                 "<br/><b>During:</b> 90 deg at every claimed resonance? "
                 "Nyquist circles? drive-point alternation? coherence ~ 1?"
                 "<br/><b>After:</b> poles stable across rows/columns "
                 "(global!)? shapes orthogonal-ish? FEM updated + "
                 "re-compared?", GREEN, PALE_GREEN))

    # ===== GLOSSARY =====
    s.append(PageBreak())
    s += heading("(Glossary)", "Ch.2 definitions")
    glossary = [
        ("Pole", "root of char. equation; -z wn +- j wd; damping + freq."),
        ("Residue", "pole's finite strength; MDOF: shape-i x shape-j."),
        ("S-plane", "real-vs-imag pole map; jw axis hosts FRFs."),
        ("Dynamic amplification", "X/Xstatic vs b; peak ~ 1/(2z) = Q."),
        ("Half-power / log-dec", "freq-/time-domain damping quickies."),
        ("Transfer function H(s)", "response/input in Laplace land; S-plane surface."),
        ("Partial fractions", "H(s) as SUM residue/(s-pole); test-ready form."),
        ("Bode / co-quad / Nyquist", "mag-phase / re-im-vs-f / im-vs-re portraits."),
        ("Compliance/mobility/inertance", "D/F, V/F, A/F (+ stiffness/impedance/mass inverses)."),
        ("Eigenvalue/vector/pair", "w2 / shape / the pair; det([K]-L[M])=0."),
        ("Orthogonality", "shapes decouple M and K; gives modal m, k."),
        ("Modal matrix [U]", "shapes as columns; x=[U]p uncouples."),
        ("Modal force", "u(T)F: how hard input pushes each mode."),
        ("Modal superposition", "solve tiny modal SDOFs, project back, add."),
        ("System matrix [B(s)]", "s-domain coefficient matrix; symmetric."),
        ("Global property", "same for all FRFs (poles, freqs, damping)."),
        ("Truncation", "keeping m&lt;&lt;n modes + residual compensation."),
    ]
    for term, defn in glossary:
        s.append(P(f"<b>{term}</b> - {defn}", small))
    s.append(Spacer(1, 10))
    s.append(P("Council sign-off: Meera (theory) ok - Viktor (lab) ok - Lena "
               "(signals) ok - Arjun (pedagogy) ok - Sofia (field) ok. "
               "Next stop: Ch.3 signals - sampling, leakage, windows!",
               center))
    return s


def main() -> None:
    from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
    from reportlab.lib.pagesizes import A4
    doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=ML,
                          rightMargin=MR, topMargin=MT, bottomMargin=MB,
                          title="Ch.2 Handwritten Notes - Modal Testing",
                          author="Modal Notes Council")
    from make_handwritten_pdf import PAGE_H as _PH
    frame = Frame(ML, MB, FRAME_W, _PH - MT - MB, id="main")
    doc.addPageTemplates([PageTemplate(id="pg", frames=[frame], onPage=bg)])
    doc.build(build_story())
    print(f"Wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
