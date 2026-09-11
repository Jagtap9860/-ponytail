"""Chapter 2 EXTENDED edition: 40+ filled pages (derivations + masterclass + banks).

Usage:  python3 modal-notes/make_ch2_full.py   (run from repo root)
Output: modal-notes/chapter-02-handwritten-notes.pdf  (overwrites 12-page ed.)
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from reportlab.graphics.shapes import Drawing, Line, PolyLine, Rect, String
from reportlab.lib import colors

import make_handwritten_pdf as _MHW
_MHW.CHAPTER_LABEL = "Ch.2"

from make_ch2_pdf import (arrow, panel, S, sdof_sketch, splane_sketch,
                          dynamp_sketch, halfpower_sketch, forcebalance_sketch,
                          nyquist_sketch, regions_sketch, mdofsum_sketch,
                          xform_sketch, domains_sketch, fullloop_sketch)
from make_handwritten_pdf import (BLUE, FRAME_W, GREEN, INK, MB, ML, MR, MT,
                                  PALE_BLUE, PALE_GREEN, PALE_PINK,
                                  PALE_YELLOW, RED, bg, body, box, bullet,
                                  center, cover_sub, cover_title, F,
                                  formula_text, h3, heading, hl, key, lab,
                                  link, P, small, tbl, trap, tryit, B)

HERE = pathlib.Path(__file__).parent
OUT = HERE / "chapter-02-handwritten-notes.pdf"
GRAY = colors.HexColor("#44507A")


# ---------- new sketches ----------
def migration4_sketch() -> Drawing:
    w, h = FRAME_W, 172
    d = panel(w, h, "my sketch: pole migration vs damping (4 fates)")
    titles = ["z = 0: undamped", "0<z<1: under", "z = 1: critical", "z > 1: over"]
    subs = ["poles ON jw", "pair LEFT", "collide on real", "split real x2"]
    waves = [
        [0, 50, 15, 75, 30, 50, 45, 25, 60, 50, 75, 75, 90, 50],
        [0, 50, 15, 68, 30, 50, 45, 36, 60, 50, 72, 60, 84, 50, 90, 46],
        [0, 78, 20, 60, 40, 50, 60, 46, 90, 44],
        [0, 78, 30, 70, 60, 60, 90, 52],
    ]
    resps = ["eternal sine", "ring-down!", "fastest, no ring", "slow creep"]
    for i, (t, sb, wv, rp) in enumerate(zip(titles, subs, waves, resps)):
        x = 14 + i * 117
        d.add(Rect(x, 14, 108, 128, fillColor=None, strokeColor=GRAY,
                   strokeWidth=1.0))
        S(d, x + 6, 126, t, 8.5, INK, True)
        ox, oy = x + 34, 96
        d.add(Line(ox - 22, oy, ox + 22, oy, strokeColor=INK, strokeWidth=1.1))
        d.add(Line(ox, oy - 16, ox, oy + 16, strokeColor=INK, strokeWidth=1.1))
        if i == 0:
            pts = [(ox, oy + 12), (ox, oy - 12)]
        elif i == 1:
            pts = [(ox - 8, oy + 10), (ox - 8, oy - 10)]
        elif i == 2:
            pts = [(ox - 12, oy), (ox - 12, oy)]
        else:
            pts = [(ox - 16, oy), (ox - 5, oy)]
        for qx, qy in pts:
            d.add(Line(qx - 4, qy - 4, qx + 4, qy + 4, strokeColor=RED,
                       strokeWidth=2.0))
            d.add(Line(qx - 4, qy + 4, qx + 4, qy - 4, strokeColor=RED,
                       strokeWidth=2.0))
        S(d, x + 6, 72, sb, 8, RED)
        shifted = [c + (x + 8 if k % 2 == 0 else -14) for k, c in
                   enumerate(wv)]
        d.add(PolyLine(shifted, strokeColor=BLUE, strokeWidth=1.8,
                       strokeLineJoin=1))
        S(d, x + 6, 20, rp, 8, BLUE)
    return d


def twodof_sketch() -> Drawing:
    w, h = FRAME_W, 168
    d = panel(w, h, "my sketch: 2DOF masterclass rig (m1=m2=1, k1=k2=100)")
    d.add(Line(40, 110, 40, 160, strokeColor=INK, strokeWidth=2.2))
    for yy in (118, 130, 142, 154):
        d.add(Line(40, yy, 30, yy - 6, strokeColor=INK, strokeWidth=1.1))
    d.add(PolyLine([40, 142, 52, 150, 64, 134, 76, 150, 88, 134, 100, 142],
                   strokeColor=BLUE, strokeWidth=2.0, strokeLineJoin=1))
    S(d, 58, 154, "k1=100", 8.5, BLUE)
    d.add(Rect(100, 118, 70, 48, fillColor=PALE_BLUE, strokeColor=INK,
               strokeWidth=2.0))
    S(d, 122, 138, "m1=1", 10, INK, True)
    d.add(PolyLine([170, 142, 182, 150, 194, 134, 206, 150, 218, 134, 230,
                    142], strokeColor=BLUE, strokeWidth=2.0,
                   strokeLineJoin=1))
    S(d, 188, 154, "k2=100", 8.5, BLUE)
    d.add(Rect(230, 118, 70, 48, fillColor=PALE_BLUE, strokeColor=INK,
               strokeWidth=2.0))
    S(d, 252, 138, "m2=1", 10, INK, True)
    arrow(d, 125, 108, 125, 88, RED, 1.8)
    S(d, 130, 94, "f1", 9, RED, True)
    arrow(d, 265, 108, 265, 88, RED, 1.8)
    S(d, 270, 94, "f2", 9, RED, True)
    S(d, 320, 150, "MODE 1: 0.98 Hz", 9.5, BLUE, True)
    arrow(d, 330, 140, 330, 118, BLUE, 2.2)
    arrow(d, 360, 140, 360, 104, BLUE, 2.6)
    S(d, 318, 88, "1 : 1.618", 9, BLUE, True)
    S(d, 320, 76, "(together!)", 8.5)
    S(d, 320, 60, "MODE 2: 2.58 Hz", 9.5, RED, True)
    arrow(d, 330, 50, 330, 28, RED, 2.2)
    arrow(d, 360, 28, 360, 42, RED, 2.0)
    S(d, 318, 14, "1 : -0.618", 9, RED, True)
    S(d, 30, 14, "golden ratio hides here: 1.618 = PHI!", 9, GREEN, True)
    return d


def coverup_sketch() -> Drawing:
    w, h = FRAME_W, 128
    d = panel(w, h, "my sketch: cover-up method for residues (SDOF)")
    S(d, 20, 96, "H(s) = (1/m) / [(s-p1)(s-p2)]", 11, INK, True)
    d.add(Rect(230, 88, 90, 26, fillColor=HL if False else PALE_YELLOW,
               strokeColor=RED, strokeWidth=1.6))
    S(d, 236, 96, "cover (s-p1)!", 9, RED, True)
    arrow(d, 150, 82, 150, 62, INK, 1.8)
    S(d, 20, 44, "set s = p1  ->  A1 = (1/m) / (p1 - p2)", 11, INK, True)
    arrow(d, 360, 52, 400, 52, GREEN, 1.8)
    S(d, 20, 20, "p1 - p2 = j2wd, so  A1 = 1 / (j 2 m wd)", 11, GREEN, True)
    return d


def surface_slice_sketch() -> Drawing:
    w, h = FRAME_W, 158
    d = panel(w, h, "my sketch: transfer surface side-view + the jw slice")
    arrow(d, 40, 26, 440, 26, INK, 1.5)
    S(d, 180, 10, "frequency along jw ->", 9)
    arrow(d, 40, 26, 40, h - 20, INK, 1.5)
    S(d, 8, h - 30, "|H|", 9)
    pl = PolyLine([40, 40, 120, 40, 170, 44, 195, 90, 205, 140, 215, 90,
                   240, 44, 300, 38, 440, 34], strokeColor=BLUE,
                  strokeWidth=2.4, strokeLineJoin=1)
    d.add(pl)
    d.add(Line(205, 26, 205, 140, strokeColor=RED, strokeWidth=1.2))
    S(d, 214, 122, "pole spike!", 9, RED, True)
    S(d, 214, 110, "(pole hides just", 8.5)
    S(d, 214, 100, "behind paper)", 8.5)
    d.add(Rect(290, 84, 140, 40, fillColor=PALE_YELLOW, strokeColor=GREEN,
               strokeWidth=1.6))
    S(d, 298, 108, "knife = s = jw", 9, GREEN, True)
    S(d, 298, 94, "cut edge = FRF!", 9, GREEN, True)
    S(d, 60, 60, "light damping:", 8.5, BLUE)
    S(d, 60, 49, "tall sharp slice", 8.5, BLUE)
    return d
PALE = None  # (kept namespace tidy; palette comes from ch1 imports)


def filterbank_sketch() -> Drawing:
    w, h = FRAME_W, 148
    d = panel(w, h, "my sketch: modal filter bank (input x shapes -> sum)")
    arrow(d, 14, 74, 70, 74, RED, 2.2)
    S(d, 16, 82, "F at j", 9, RED, True)
    S(d, 16, 58, "(x ujr!)", 8.5)
    boxes = [(90, BLUE, "M1 SDOF", "x uir"), (210, RED, "M2 SDOF", "x uir"),
             (330, GREEN, "M3 SDOF", "x uir")]
    for x, col, t1, t2 in boxes:
        d.add(Rect(x, 44, 96, 60, fillColor=colors.white,
                   strokeColor=col, strokeWidth=2.0))
        S(d, x + 8, 84, t1, 9, col, True)
        S(d, x + 8, 68, "1/(wr2-w2+..)", 7.5)
        S(d, x + 8, 54, t2, 8.5)
    d.add(Line(70, 74, 90, 88, strokeColor=INK, strokeWidth=1.4))
    d.add(Line(70, 74, 210, 74, strokeColor=INK, strokeWidth=1.4))
    d.add(Line(70, 74, 330, 60, strokeColor=INK, strokeWidth=1.4))
    for x in (186, 306, 426):
        arrow(d, x, 74, x + 22 if x < 400 else x, 74, INK, 1.4)
    S(d, 428, 78, "SUM", 9, INK, True)
    S(d, 428, 64, "= hij", 9, INK, True)
    arrow(d, 444, 52, 470, 52, BLUE, 2.0)
    S(d, 430, 36, "out at i", 8.5, BLUE)
    return d


def cantilever3_sketch() -> Drawing:
    w, h = FRAME_W, 168
    d = panel(w, h, "my sketch: cantilever, 3 sensors, 3 shapes + nodes")
    d.add(Line(60, 30, 60, 150, strokeColor=INK, strokeWidth=3.0))
    for yy in (44, 66, 88, 110, 132):
        d.add(Line(60, yy, 48, yy - 8, strokeColor=INK, strokeWidth=1.2))
    for i, (yy, col, lab_) in enumerate(
            [(128, BLUE, "M1: bend-1 (no node!)"),
             (88, RED, "M2: bend-2 (1 node o)"),
             (48, GREEN, "M3: bend-3 (2 nodes oo)")]):
        d.add(Line(60, yy, 330, yy, strokeColor=GRAY, strokeWidth=0.8))
        if i == 0:
            pts = [60, yy, 120, yy + 2, 180, yy + 8, 240, yy + 18, 300, yy + 32]
        elif i == 1:
            pts = [60, yy, 120, yy + 10, 190, yy, 250, yy - 12, 300, yy - 20]
        else:
            pts = [60, yy, 110, yy + 10, 160, yy, 210, yy - 10, 260, yy,
                   300, yy + 12]
        d.add(PolyLine(pts, strokeColor=col, strokeWidth=2.4,
                       strokeLineJoin=1))
        S(d, 336, yy - 4, lab_, 8.5, col, True)
    for sx in (150, 240, 330 - 30):
        d.add(Rect(sx - 4, 124, 8, 8, fillColor=RED, strokeColor=RED))
    S(d, 140, 140, "sensors 1-2-3 ->", 8.5, RED)
    d.add(Line(190, 88, 190, 88, strokeColor=RED, strokeWidth=1.0))
    from reportlab.graphics.shapes import Circle as _C
    d.add(_C(190, 88, 4, fillColor=colors.white, strokeColor=RED,
             strokeWidth=2.0))
    d.add(_C(160, 48, 3.5, fillColor=colors.white, strokeColor=RED,
             strokeWidth=2.0))
    d.add(_C(260, 48, 3.5, fillColor=colors.white, strokeColor=RED,
             strokeWidth=2.0))
    S(d, 60, 14, "node here = that mode INVISIBLE to a sensor parked on it!", 9,
      RED, True)
    return d


def waterfall_sketch() -> Drawing:
    w, h = FRAME_W, 148
    d = panel(w, h, "my sketch: waterfall - ridges ARE the shapes")
    for r in range(4):
        y0 = 30 + r * 24
        peak = [120, 200, 300]
        pk = [66 - r * 6, 52 + r * 4, 60 - r * 10]
        pts = [40, y0, 80, y0]
        for px, ph in zip(peak, pk):
            pts += [px - 22, y0, px, y0 + ph, px + 22, y0]
        pts += [400, y0, 445, y0]
        d.add(PolyLine(pts, strokeColor=INK, strokeWidth=1.6,
                       strokeLineJoin=1))
        S(d, 16, y0 - 4, f"p{r + 1}", 8.5)
    for px in (120, 200, 300):
        rl = Line(px, 30, px, 30 + 3 * 24 + 40, strokeColor=RED,
                  strokeWidth=1.2)
        rl.strokeDashArray = [4, 3]
        d.add(rl)
    S(d, 100, h - 28, "ridge = M1", 8.5, RED, True)
    S(d, 190, h - 28, "M2", 8.5, RED, True)
    S(d, 290, h - 28, "M3", 8.5, RED, True)
    S(d, 330, 60, "read DOWN a", 8.5)
    S(d, 330, 48, "ridge = shape!", 8.5, BLUE, True)
    return d


def halfpower_cq_sketch() -> Drawing:
    w, h = FRAME_W, 148
    d = panel(w, h, "my sketch: half-power on co-quad (real + imag agree!)")
    arrow(d, 24, 50, 225, 50, INK, 1.3)
    d.add(PolyLine([24, 50, 70, 50, 100, 78, 124, 50, 148, 22, 178, 50,
                    225, 50], strokeColor=BLUE, strokeWidth=2.2,
                   strokeLineJoin=1))
    S(d, 30, h - 28, "REAL: 0 at reso, peaks = hp pts", 9, BLUE, True)
    d.add(Line(124, 26, 124, 100, strokeColor=GRAY, strokeWidth=1.0))
    arrow(d, 258, 30, 459, 30, INK, 1.3)
    d.add(PolyLine([258, 32, 310, 34, 345, 70, 368, 108, 391, 70, 426, 34,
                    459, 32], strokeColor=RED, strokeWidth=2.2,
                   strokeLineJoin=1))
    hl = Line(258, 70, 459, 70, strokeColor=GREEN, strokeWidth=1.2)
    hl.strokeDashArray = [4, 3]
    d.add(hl)
    S(d, 264, h - 28, "IMAG: peak; half pts = hp", 9, RED, True)
    S(d, 264, 14, "same w1, w2 both sides!", 8.5, GREEN, True)
    return d

# ---------- deep-cut sketches ----------
def peakshift_sketch() -> Drawing:
    w, h = FRAME_W, 148
    d = panel(w, h, "my sketch: D, V, A peak at DIFFERENT spots (z = 0.3!)")
    arrow(d, 40, 26, 440, 26, INK, 1.5)
    S(d, 200, 10, "frequency -> (wn marked)", 9)
    wl = Line(240, 26, 240, 120, strokeColor=GRAY, strokeWidth=1.0)
    wl.strokeDashArray = [4, 3]
    d.add(wl)
    S(d, 228, 124, "wn", 9, INK, True)
    d.add(PolyLine([40, 40, 120, 42, 170, 60, 205, 108, 230, 70, 280, 44,
                    360, 38, 440, 36], strokeColor=BLUE, strokeWidth=2.4,
                   strokeLineJoin=1))
    S(d, 120, 116, "D/F peaks LOW", 9, BLUE, True)
    d.add(PolyLine([40, 34, 130, 36, 190, 58, 240, 112, 290, 58, 350, 38,
                    440, 34], strokeColor=GREEN, strokeWidth=2.2,
                   strokeLineJoin=1))
    S(d, 252, 100, "V/F peaks AT wn", 9, GREEN, True)
    d.add(PolyLine([40, 32, 140, 34, 210, 50, 275, 108, 310, 66, 370, 40,
                    440, 36], strokeColor=RED, strokeWidth=2.0,
                   strokeLineJoin=1))
    S(d, 292, 116, "A/F peaks HIGH", 9, RED, True)
    return d


def rayleigh_sketch() -> Drawing:
    w, h = FRAME_W, 148
    d = panel(w, h, "my sketch: Rayleigh damping U-curve (fit in-band!)")
    arrow(d, 40, 26, 440, 26, INK, 1.5)
    arrow(d, 40, 26, 40, h - 20, INK, 1.5)
    S(d, 200, 10, "frequency w ->", 9)
    S(d, 8, h - 28, "z", 9)
    d.add(PolyLine([40, 120, 90, 70, 140, 48, 200, 44, 260, 48, 320, 62,
                    380, 84, 440, 112], strokeColor=BLUE, strokeWidth=2.4,
                   strokeLineJoin=1))
    from reportlab.graphics.shapes import Circle as _C
    d.add(_C(140, 48, 4, fillColor=RED, strokeColor=RED))
    d.add(_C(260, 48, 4, fillColor=RED, strokeColor=RED))
    S(d, 100, 60, "fit z1", 8.5, RED, True)
    S(d, 268, 60, "fit z2", 8.5, RED, True)
    S(d, 330, 100, "high modes:", 8.5, BLUE)
    S(d, 330, 88, "OVERDAMPED!", 9, BLUE, True)
    S(d, 52, 100, "mass-term", 8.5)
    S(d, 52, 88, "a/w side", 8.5)
    return d


def read60_sketch() -> Drawing:
    w, h = FRAME_W, 168
    d = panel(w, h, "my sketch: read any FRF in 60 seconds (7 checkpoints)")
    arrow(d, 36, 30, 444, 30, INK, 1.5)
    d.add(PolyLine([36, 70, 100, 70, 140, 66, 168, 44, 186, 128, 204, 50,
                    240, 62, 268, 44, 286, 118, 304, 52, 340, 60, 380, 56,
                    444, 52], strokeColor=BLUE, strokeWidth=2.4,
                   strokeLineJoin=1))
    S(d, 44, 82, "1 slopes->form", 8.5, GREEN, True)
    S(d, 150, 136, "2 peaks?", 8.5, RED, True)
    S(d, 268, 128, "3 phase 90?", 8.5, RED, True)
    d.add(Line(168, 40, 204, 40, strokeColor=RED, strokeWidth=1.2))
    S(d, 160, 108, "4 width->z", 8.5, RED, True)
    S(d, 232, 76, "5 valley?", 8.5)
    S(d, 330, 76, "6 imag +/-?", 8.5)
    S(d, 330, 40, "7 coherence?", 8.5)
    d.add(Line(186, 30, 186, 128, strokeColor=GRAY, strokeWidth=1.0))
    d.add(Line(286, 30, 286, 118, strokeColor=GRAY, strokeWidth=1.0)
    )
    return d


def bode_master_sketch() -> Drawing:
    w, h = FRAME_W, 168
    d = panel(w, h, "my sketch: Bode asymptotes (dashed) vs exact (solid)")
    arrow(d, 30, 30, 235, 30, INK, 1.4)
    S(d, 36, h - 28, "MAG: flat 1/k -> corner -> -2 slope", 9)
    a1 = PolyLine([30, 110, 132, 110, 235, 40], strokeColor=GRAY,
                  strokeWidth=1.4)
    a1.strokeDashArray = [5, 3]
    d.add(a1)
    d.add(PolyLine([30, 110, 90, 110, 118, 112, 132, 138, 146, 112, 175, 84,
                    235, 40], strokeColor=BLUE, strokeWidth=2.4,
                   strokeLineJoin=1))
    S(d, 100, 142, "Q peak!", 9, BLUE, True)
    S(d, 126, 96, "wn", 8.5)
    S(d, 36, 96, "1/k", 8.5)
    arrow(d, 265, 30, 460, 30, INK, 1.4)
    S(d, 271, h - 28, "PHASE: 0 -> 90 -> 180 deg", 9)
    d.add(PolyLine([265, 120, 310, 118, 345, 100, 362, 75, 379, 50, 414, 32,
                    460, 30], strokeColor=RED, strokeWidth=2.4,
                   strokeLineJoin=1))
    S(d, 366, 79, "90!", 9, RED, True)
    S(d, 271, 108, "0 deg", 8.5)
    S(d, 420, 40, "180", 8.5)
    return d


# ---------- content ----------
def build_story() -> list:
    from reportlab.platypus import PageBreak, Paragraph, Spacer, KeepTogether
    s: list = []

    # ===== COVER =====
    s += [Spacer(1, 22),
          P("Modal Testing: A Practitioner's Guide", cover_sub),
          P("Ch. 2 - General Theory<br/>of Experimental Modal Analysis",
            cover_title),
          P("EXTENDED edition: 40+ pages - derivations, masterclass, banks",
            cover_sub),
          Spacer(1, 6),
          box("Whole chapter in 1 line:",
              "Everything measured (FRF) = <b>POLES</b> (where modes live: "
              "damping + frequency) + <b>RESIDUES</b> (how strongly each "
              "mode shows at each point). Curvefitting = hunting these two. "
              "This edition PROVES every claim Ch.1 only showed.",
              BLUE, PALE_BLUE),
          box("How to use this extended edition:",
              "<b>Pass 1 (intuition):</b> read S0, all [KEY] boxes, all "
              "sketches, revision. <b>Pass 2 (hands):</b> do EX-A to EX-S "
              "with a calculator - check every number. <b>Pass 3 (steel):</b> "
              "derivations + practice problems + interview bank. Exam/lab in "
              "a week? Pass 1 + formula bank + FAQ.",
              GREEN, PALE_GREEN),
          P("<b>Legend:</b> <font color=\"#2F6FED\"><b>[KEY]</b></font> key "
            "&nbsp; <font color=\"#1F9D55\"><b>[LAB]</b></font> lab"
            " &nbsp; <font color=\"#E5484D\"><b>[TRAP]</b></font> trap"
            " &nbsp; <font color=\"#7A4FD0\"><b>[LINK]</b></font> bridge"
            " &nbsp; <font color=\"#B26A00\"><b>[TRY]/EX</b></font> do it"
            " &nbsp; <b>DERIVE</b> proof steps", center),
          P("Council crew: Dr. Meera K. (theory) - Dr. Viktor H. (lab) - "
            "Dr. Lena F. (signals) - Prof. Arjun D. (pedagogy) - "
            "Dr. Sofia M. (field) &nbsp;|&nbsp; 11 Sep 2026", small)]
    s.append(PageBreak())

    # ===== MAP =====
    s += heading("(Map)", "Chapter roadmap - where the 40 pages go")
    s.append(tbl([
        ["Block", "Pages do", "Council owner"],
        ["S0 Primer XXL", "Ch.1 pictures -> Ch.2 machines; math crash kit", "Arjun"],
        ["2.1 Two models", "FEM vs EMA, history, why theory pays", "Sofia"],
        ["2.2 SDOF (half the book)", "Poles, S-plane, forcing, damping, vectors, Laplace, FRF, D/V/A", "Meera + Lena"],
        ["2.3 MDOF (the summit)", "2DOF masterclass, eigen, uncoupling, FRF sums, beam, domains", "Meera + Viktor"],
        ["2.4 The loop", "Whole EMA map, forward vs backward paths", "Sofia"],
        ["Banks", "Formulas, symbols, FAQ, interviews, problems, revision, test, glossary", "All five"],
    ], [FRAME_W * 0.26, FRAME_W * 0.5, FRAME_W * 0.24]))
    s.append(P(link("How chapters chain: Ch.2 machines -> <b>Ch.3</b> measure "
                    "right (sampling/leakage) -> <b>Ch.4</b> excite right "
                    "(hammer/shaker) -> <b>Ch.5</b> extract right "
                    "(estimators). Theory first, craft after.")))

    # ===== S0 XXL =====
    s += heading("(0)", "Primer XXL - pictures become machines")
    s.append(tbl([
        ["Ch.1 picture", "Ch.2 machine", "You will compute"],
        ["FRF peaks at fn", "POLES s = -z wn + j wd", "EX-B: poles from m/c/k"],
        ["Imag heights trace shape", "RESIDUES ~ shape x shape", "EX-R: shape from a column"],
        ["One row/column enough", "Transfer-matrix SYMMETRY", "Reciprocity proof sketch"],
        ["Hidden SDOFs summed", "hij = SUM modal SDOFs", "EX-M: full 2DOF FRF"],
        ["Curvefit finds f,z,shape", "Curvefit finds POLES+RESIDUES", "Self-test + interview bank"],
    ], [FRAME_W * 0.26, FRAME_W * 0.4, FRAME_W * 0.34]))
    s.append(box("Math crash kit (all Ch.2 needs):",
                 "<b>1. Complex numbers:</b> j = sqrt(-1); magnitude = "
                 "sqrt(re^2+im^2); multiplying by j = +90 deg rotation; by "
                 "-1 = 180 flip.<br/><b>2. e^(jwt):</b> spinning arrow at w "
                 "rad/s; derivative = multiply by jw (velocity leads "
                 "displacement 90 deg; acceleration leads 180).<br/><b>3. "
                 "dB:</b> 20 log10(ratio); half power = -3 dB = divide by "
                 "sqrt(2).<br/><b>4. Matrices:</b> [M]{x} couples equations; "
                 "symmetric = hij-able; determinant = 0 finds eigenvalues.",
                 BLUE, PALE_BLUE))
    s.append(box("Ch.1 callback quiz (60 seconds):",
                 tryit("1. FRF = ? <i>X/F in freq domain.</i> 2. Drive-point "
                 "trio? <i>Alternate peaks/valleys, -/+180 phase, imag same "
                 "side.</i> 3. Reference on node? <i>Mode vanishes.</i> 4. "
                 "Hammer vs shaker? <i>ROW vs COLUMN.</i> 5. Leakage cure? "
                 "<i>Windows (the tax).</i> All green? Climb on."), GREEN,
                 PALE_GREEN))

    # ===== 2.1 XXL =====
    s += heading("(2.1)", "Two models, one truth - extended")
    s.append(tbl([
        ["", "FEM (analytical)", "EMA (experimental)"],
        ["Starts from", "Assumed M, K layout + BCs", "Measured force + response"],
        ["Engine", "EIGENSOLUTION of big matrices", "CURVEFITTING of FRFs"],
        ["Gives", "Freqs + shapes (no damping!)", "f, z, shapes (WITH damping)"],
        ["Strength", "Design-stage what-ifs, zero hardware", "Ground truth incl. joints/damping"],
        ["Weakness", "Wrong assumptions/BCs = fiction", "Bad FRFs = fiction with error bars"],
        ["Costs", "Engineer time + compute", "Sensors, analyzer, rig, lab days"],
    ], [FRAME_W * 0.16, FRAME_W * 0.42, FRAME_W * 0.42]))
    s.append(box("Why FEM needs EMA (Sofia's war story):",
                 "A bracket FEM said 1st mode 210 Hz; test said 164 Hz. "
                 "Culprit: bolted joint modeled as welded (infinite "
                 "stiffness). Fix: bushing elements tuned to test, error "
                 "210 -> 166 Hz. " + key("Joints, welds, gaskets, "
                 "preload: FEM guesses, EMA KNOWS. Damping is never "
                 "predicted - only measured."), GREEN, PALE_GREEN))
    s.append(tbl([
        ["Era", "What changed for modal testing"],
        ["1980s", "FFT analyzers + IMAC conferences; EMA becomes routine"],
        ["1990s", "MIMO acquisition + better estimators; big structures testable"],
        ["2000s", "OMA (no-force methods); laser vibrometry spreads"],
        ["2010s+", "High-channel counts, model updating + UQ pipelines"],
    ], [FRAME_W * 0.2, FRAME_W * 0.8]))
    s.append(P("Book's promise for Ch.2: NOT every derivation - the equations "
               "that change how you TEST, with proofs only where they "
               "protect you from mistakes. " + trap("Vibration textbooks "
               "derive; this chapter ARMS. Different goal - read "
               "accordingly.")))

    # ===== 2.2A =====
    s += heading("(2.2A)", "SDOF I: equation, poles, S-plane")
    s += [P("The equation + its honest assumptions:", h3)]
    s.append(F(formula_text("m x'' + c x' + k x = f(t)   (linear, time-invariant)")))
    s.append(tbl([
        ["Assumption", "Means", "Breaks when"],
        ["Lumped m", "Mass acts at a point", "Distributed inertia matters (beams at high f)"],
        ["Linear k x", "Stiffness constant", "Gaps, hardening springs, buckling"],
        ["Viscous c x'", "Damping ~ velocity", "Friction (Coulomb), joints, air pumping"],
        ["Time-invariant", "m/c/k frozen", "Fuel burn, heat, wear, opening cracks"],
    ], [FRAME_W * 0.2, FRAME_W * 0.4, FRAME_W * 0.4]))
    s.append(P(trap("Everything in Ch.2 dies with nonlinearity - but note the "
                    "mercy: lightly nonlinear structures still give USEFUL "
                    "linear fits per amplitude. Later chapters teach "
                    "detecting the lie (distorted Nyquist, level-dependent "
                    "freqs).")))
    s.append(KeepTogether(sdof_sketch()))
    s.append(box("EX-A: quarter-car suspension (feel real numbers):",
                 "<b>m = 400 kg, k = 30 kN/m, c = 2 kN s/m.</b> wn = "
                 "sqrt(30000/400) = 8.66 rad/s -> <b>fn = 1.38 Hz</b> "
                 "(that floaty car feel!). cc = 2*400*8.66 = 6928. z = "
                 "2000/6928 = <b>0.29</b> - comfy AND controlled. Static "
                 "sag under weight: 400*9.81/30000 = <b>13 cm</b>. Now you "
                 "know why speedbreakers at 1.4 Hz bounce hurt.",
                 colors.HexColor("#B26A00"), PALE_YELLOW))
    s += [P("DERIVE: characteristic equation to poles (follow with pencil):",
            h3)]
    s.append(B("Step 1: free vibration, f = 0: m x'' + c x' + k x = 0."))
    s.append(B("Step 2: try x = X e^(st): x' = sX e^(st), x'' = s2 X e^(st)."))
    s.append(B("Step 3: factor X e^(st) [never zero] -> <b>m s2 + c s + k = "
               "0</b>. THE characteristic equation."))
    s.append(B("Step 4: quadratic formula: s = [-c +- sqrt(c2 - 4mk)] / 2m."))
    s.append(B("Step 5: underdamped (c2 &lt; 4mk): sqrt gives j: s = -c/2m "
               "+- j sqrt(4mk-c2)/2m."))
    s.append(B("Step 6: name c/2m = z wn and the imag part wd -> <b>s = -z "
               "wn +- j wd</b>. DONE - poles derived, not memorized."))
    s.append(F(formula_text("wn = sqrt(k/m),  cc = 2 m wn,  z = c/cc,  wd = wn sqrt(1-z^2)")))
    s.append(box("EX-B: pole drill (three fates - compute, then check):",
                 "(a) m=0.5, k=2000, c=2: wn=63.2, cc=63.2, z=0.032, poles "
                 "<b>-2 +- j63.2</b> (rings ~10 Hz, light).<br/>(b) m=10, "
                 "k=40000, c=400: wn=63.2, cc=1265, z=<b>0.316</b>, wd=60.0, "
                 "poles <b>-20 +- j60</b> (heavy - shock absorber territory)."
                 "<br/>(c) c = cc exactly: <b>double real pole -wn</b> - "
                 "critical, the border crossing.",
                 colors.HexColor("#B26A00"), PALE_YELLOW))
    s.append(box("Pole anatomy - tattoo this:",
                 key("<b>Real (-z wn)</b> = decay rate. <b>Imag (wd)</b> = "
                 "ring freq. <b>Conjugate pairs</b> always (real system!). "
                 "z &lt; 0.1: wd ~ wn (error under 0.5%). wn NEVER depends "
                 "on damping - only wd does."), BLUE, PALE_BLUE))
    s += [P("S-plane deep map:", h3)]
    s.append(KeepTogether(splane_sketch()))
    s.append(KeepTogether(migration4_sketch()))
    s.append(B("Read the 4 fates: <b>undamped</b> ON jw (eternal sine); "
               "<b>under</b> left-shifted pair (ring-down + sharp peak); "
               "<b>critical</b> merged on real axis (fastest return, zero "
               "overshoot); <b>over</b> split real pair (slow creep)."))
    s.append(P(key("<b>Radius origin-to-pole = wn, ALWAYS.</b> Damping "
                   "rotates the pole west along the circle; stiffness "
                   "scales the circle. ") + link("MAP reading: cities "
                   "(poles) west = damped, north = stiff. Your FRF = the "
                   "view driving up the jw highway.")))
    s.append(P(tryit("EX-C: sketch S-planes for EX-B (a) and (b) - same "
                     "radius 63.2, but (b) sits MUCH further west. Which "
                     "rings longer? (a), by 10x - decay time 1/(z wn): "
                     "0.5 s vs 0.05 s.")))
    s += [P("Forced response: amplification DERIVED (not gifted):", h3)]
    s.append(B("Step 1: f = F e^(jwt), guess x = X e^(jwt) -> (-m w2 + j c w "
               "+ k) X = F."))
    s.append(B("Step 2: X/F = 1 / [(k - m w2) + j c w]. Divide top+bottom by "
               "k; set b = w/wn, c w/k = 2 z b."))
    s.append(B("Step 3: X/Xstatic = 1 / [(1-b2) + j 2 z b]. Magnitude: "
               "<b>1/sqrt((1-b2)2 + (2zb)2)</b>. Phase: "
               "<b>atan2(2zb, 1-b2)</b>." ))
    s.append(KeepTogether(dynamp_sketch()))
    s.append(box("EX-D: amplification table (compute ONE row, trust the rest):",
                 "z=0.02: b=0.9 -> <b>5.17</b>; b=1 -> <b>25.0</b>; b=1.1 -> "
                 "<b>4.66</b>.<br/>z=0.05: 4.76 / <b>10.0</b> / 4.22.<br/>"
                 "z=0.10: 3.82 / <b>5.0</b> / 3.29.<br/>" + key("Moral: "
                 "peak height ~ 1/(2z) - doubling damping HALVES the peak. "
                 "Off-resonance (b=0.9/1.1) damping barely matters - "
                 "stiffness/mass rule there."), colors.HexColor("#B26A00"),
                 PALE_YELLOW))
    s.append(box("Phase: the 90-degree signature:",
                 key("Lag 0 deg (static, moves WITH force) -> <b>90 deg AT "
                 "resonance</b> -> 180 deg (moves AGAINST force). ") +
                 lab("Peaks lie (noise/leakage); <b>90 deg rarely lies</b>. "
                 "No 90 crossing = no resonance, whatever the bump says. - "
                 "Lena") + "<br/>" + tryit("EX-E: z=0.02, b=0.9: phase = "
                 "atan2(0.036, 0.19) = <b>10.7 deg</b>. b=1.1: atan2(0.044, "
                 "-0.21) = <b>168 deg</b>. Feel the snap across resonance!"),
                 BLUE, PALE_BLUE))

    # ===== 2.2B =====
    s += heading("(2.2B)", "SDOF II: damping, vectors, Laplace, FRF")
    s += [P("Half-power: DERIVED in 4 steps (small-z approx):", h3)]
    s.append(KeepTogether(halfpower_sketch()))
    s.append(B("Step 1: peak |H| ~ 1/(2z) at b=1. Half-power: |H|2 = half of "
               "peak2 -> |H| = peak/sqrt(2) (-3 dB)."))
    s.append(B("Step 2: solve 1/[(1-b2)2+(2zb)2] = (1/2)(1/(2z)2) near b=1: "
               "write b = 1+e, keep first order: (2e)2 + (2z)2 = 2(2z)2."))
    s.append(B("Step 3: e2 = z2 -> e = +-z -> <b>b1,2 = 1 -+ z</b>."))
    s.append(B("Step 4: bandwidth Db = 2z -> <b>z = (w2-w1)/(2wn)</b>. "
               "Wider peak = more damping. Q.E.D."))
    s.append(F(formula_text("z ~ Dw/(2 wn) = (f2 - f1)/(2 fn),   Q = 1/(2z)")))
    s.append(KeepTogether(halfpower_cq_sketch()))
    s.append(B("Co-quad witnesses: <b>REAL peaks sit exactly at hp points, "
               "REAL = 0 at resonance; IMAG peaks at resonance, half-height "
               "at hp.</b> Nyquist: hp points <b>90 deg around the circle</b> "
               "from resonance. Three portraits, one verdict."))
    s.append(P(tryit("EX-F: peak 100 Hz, hp at 99/101 -> z = 2/200 = <b>1%</b>"
                     ", Q = 50. Peak 100 Hz, hp at 96/104 -> z = <b>4%</b>, "
                     "Q = 12.5. Same fn, 4x the damping - SEE the width!")))
    s += [P("Log-decrement: DERIVED + measured right:", h3)]
    s.append(B("Free ring: x(t) = A e^(-z wn t) sin(wd t). One period later "
               "(Td = 2pi/wd): ratio x1/x2 = e^(z wn Td) = e^(2 pi z / "
               "sqrt(1-z2)) ~ e^(2 pi z). Take ln: <b>d = ln(x1/x2) ~ 2 pi "
               "z</b>." ))
    s.append(B("Pro move: average over n cycles: d = ln(x1/xn+1)/n - kills "
               "reading noise. Plot ln(peak) vs cycle: <b>straight line = "
               "linear viscous</b>; curving = amplitude-dependent "
               "(nonlinear!) damping."))
    s.append(F(formula_text("d = ln(x1/x2) ~ 2 pi z   (small z, single mode!)")))
    s.append(box("EX-G: ring-down table (single mode, 5 Hz):",
                 "Peaks: 10.0, 8.2, 6.7, 5.5 mm. d1 = ln(10/8.2) = 0.198; "
                 "d2 = ln(8.2/6.7) = 0.202; d3 = ln(6.7/5.5) = 0.198. Steady "
                 "~ <b>0.20</b> -> z = 0.20/(2 pi) = <b>3.2%</b>. " +
                 trap("If d DRIFTED (0.2, 0.25, 0.35...) - suspect friction "
                 "or multi-mode beating, NOT viscous damping."),
                 colors.HexColor("#B26A00"), PALE_YELLOW))
    s.append(box("Museum verdict (read twice):",
                 trap("Half-power + log-dec: exam-favorite, history-honored "
                 "- but real responses are multi-mode, so they mislead. ") +
                 lab("<b>Pros fit poles+residues (least squares)</b>. "
                 "Quickies for sanity + interviews; estimators for "
                 "paychecks. - Viktor"), RED, PALE_PINK))
    s.append(tbl([
        ["Language", "Formula", "EX-G value"],
        ["Damping ratio z", "c/cc", "3.2%"],
        ["Q factor", "1/(2z)", "~16"],
        ["Bandwidth", "Dw = 2 z wn", "2.0 rad/s"],
        ["Log-dec d", "2 pi z", "0.20"],
        ["Loss per cycle", "~ 4 pi z (small z)", "~40% amplitude/cycle? NO: ~18% (e^-0.2)"]],
    [FRAME_W * 0.24, FRAME_W * 0.34, FRAME_W * 0.42]))
    s.append(P(tryit("EX-H: z = 1% &lt;-> Q = 50, d = 0.0628. z = 5% &lt;-> Q = 10, "
                     "d = 0.314. Memorize the pairs (1/50), (2/25), (5/10) - "
                     "fluent damping in 3 numbers.")))
    s += [P("Force balance: the vector war, with math:", h3)]
    s.append(KeepTogether(forcebalance_sketch()))
    s.append(B("Phasors (all at w): elastic KX at 0 deg; damping c w X at +90; "
               "inertia m w2 X at 180. Sum + F = 0 ALWAYS."))
    s.append(B("Below reso: KX huge vs m w2 X -> F ~ KX (static-like). "
               "Above: m w2 X wins -> F ~ m w2 X. AT reso: KX = m w2 X "
               "exactly (that IS wn2 = k/m!) -> they annihilate -> "
               "<b>F = c w X alone</b>."))
    s.append(box("Deepest insight + numbers:",
                 key("Resonance peak measures DAMPING and nothing else - "
                 "because stiffness and inertia signed a mutual "
                 "destruction pact.")
                 + "<br/><b>EX3:</b> m=2, k=8000 at wn=63.2, X=1mm: KX = 8 "
                 "N UP, inertia = 8 N DOWN, damping = 0.5 N. 8 vs 0.5: who "
                 "is holding the bridge?<br/><b>EX-I:</b> same rig at w = "
                 "20 (b=0.32): KX = 8, inertia = 2*400*0.001 = 0.8, damping "
                 "= 8*20*0.001 = 0.16. F ~ 8 - 0.8 = 7.2 N: 90% stiffness. "
                 "AT w=200: inertia = 80 N dominates: mass world.",
                 BLUE, PALE_BLUE))
    s += [P("Laplace: 3 costumes, zero new physics:", h3)]
    s.append(tbl([
        ["Form", "Looks like", "Best for"],
        ["Polynomial", "H = 1/(m s2 + c s + k)", "Seeing the equation"],
        ["Pole-zero", "H = (1/m)/[(s-p1)(s-p2)]", "Seeing the poles"],
        ["Partial fraction", "H = A1/(s-p1) + A2/(s-p2)", "TESTING: poles + residues!"],
    ], [FRAME_W * 0.2, FRAME_W * 0.44, FRAME_W * 0.36]))
    s.append(KeepTogether(coverup_sketch()))
    s.append(P("Cover-up = limit trick: A1 = lim (s-p1) H(s) as s->p1. For "
               "SDOF: A1 = (1/m)/(p1-p2) = <b>1/(j 2 m wd)</b> (pure "
               "imaginary!). " + key("Pole + residue = DNA: rebuild H(s) "
               "everywhere + FRF at every f.")))
    s.append(P(tryit("EX-J: EX3 rig (m=2, wd=63.2): A1 = 1/(j*2*2*63.2) = "
                     "-j 0.00198. Tiny? It multiplies 1/(jw-p1) which is "
                     "HUGE near resonance - product = the giant peak.")))
    s += [P("FRF = slice at s = jw (see it!):", h3)]
    s.append(KeepTogether(surface_slice_sketch()))
    s.append(tbl([
        ["Portrait", "Shows", "Resonance reads as"],
        ["Bode (mag + phase)", "Peak + 90 deg, 180 total flip", "Peak + 90 crossing"],
        ["Co-quad (real + imag)", "Real crosses ZERO, imag PEAKS", "Imag peak, real = 0"],
        ["Nyquist (imag vs real)", "Near-CIRCLE", "Opposite origin; hp 90 deg around"],
    ], [FRAME_W * 0.26, FRAME_W * 0.4, FRAME_W * 0.34]))
    s.append(KeepTogether(nyquist_sketch()))
    s.append(P(lab("Circle = clean mode. POTATO = overlap/noise/"
                   "nonlinearity. Sweep direction + speed also talks: data "
                   "points bunch AT resonance (fast phase change) - sparse "
                   "elsewhere. - Lena")))
    s.append(P(tryit("EX-K: Nyquist top point reads (0.00, 2.5). hp points at "
                     "(+-1.25, 1.25). Peak imag = 2.5, hp at half height "
                     "1.25 with |real| = 1.25: textbook SDOF. If hp reals "
                     "were 0.4/2.1 (asymmetric) - neighbor mode leaking in!")))
    s += [P("Regions + D/V/A: the slope detective kit:", h3)]
    s.append(KeepTogether(regions_sketch()))
    s.append(tbl([
        ["Name", "Symbol", "From D/F", "Stiff slope", "Mass slope"],
        ["Compliance", "D/F", "-", "0 (flat)", "-2"],
        ["Mobility", "V/F", "x jw", "+1", "-1"],
        ["Inertance", "A/F", "x -w2", "+2", "0 (flat)"],
    ], [FRAME_W * 0.2, FRAME_W * 0.14, FRAME_W * 0.28, FRAME_W * 0.19,
        FRAME_W * 0.19]))
    s.append(P(key("Each jw multiply: +1 to BOTH slopes, +90 phase. A/F = "
                   "-w2 (D/F): 180 apart, w2 scaled. ") + lab("Unlabeled "
                   "plot? Far slopes (0,-2)=D, (+1,-1)=V, (+2,0)=A. "
                   "Seconds, not meetings.")))
    s.append(box("EX-L: slope detective quiz (answers inline, think first!):",
                 "1. Flat left, -2 right -> <b>D/F</b>. 2. +1 left, -1 right "
                 "-> <b>V/F</b>. 3. +2 left, flat right -> <b>A/F</b> (your "
                 "hammer+accel daily driver). 4. Someone's 'A/F' shows -2 "
                 "far right -> <b>MISLABELED: it is D/F.</b> Caught!",
                 GREEN, PALE_GREEN))
    s.append(box("EX-M0: convert across forms (50 Hz, D = 2e-6 m/N at -170 "
                 "deg):",
                 "w = 314. V/F = jw x D: mag 314*2e-6 = <b>6.28e-4</b>, "
                 "phase -170+90 = <b>-80 deg</b>. A/F = -w2 x D: mag "
                 "98696*2e-6 = <b>0.197</b>, phase -170+180 = <b>+10 "
                 "deg</b>. One measurement, three costumes.",
                 colors.HexColor("#B26A00"), PALE_YELLOW))
    s.append(box("Nuance most books bury: THREE different peaks!",
                 trap("D/F peaks at <b>wd-ish BELOW wn</b>; V/F peaks "
                 "<b>EXACTLY at wn</b>; A/F peaks <b>ABOVE wn</b>. Light "
                 "damping: all ~wn (relax). Heavy damping (z=0.3): D peaks "
                 "~0.90 wn, A peaks ~1.10 wn - <b>20% apart!</b> Always say "
                 "WHICH FRF your 'resonance' came from."),
                 RED, PALE_PINK))

    # ===== 2.3A: MASTERCLASS =====
    s.append(PageBreak())
    s += heading("(2.3A)", "MDOF I: 2DOF masterclass - solved by hand")
    s.append(P("The rig: m1 = m2 = 1 kg, k1 = k2 = 100 N/m (m2 free at the "
               "end). Small enough to solve on paper, rich enough to show "
               "EVERYTHING. Follow with a calculator - trust nothing."))
    s.append(KeepTogether(twodof_sketch()))
    s += [P("Step 1 - equations of motion (force balance per mass):", h3)]
    s.append(F(formula_text("m1 x1'' + (k1+k2) x1 - k2 x2 = f1")))
    s.append(F(formula_text("m2 x2'' - k2 x1 + k2 x2 = f2")))
    s.append(P("In matrices: M = [[1,0],[0,1]], K = [[200,-100],[-100,100]]. "
               + key("Off-diagonals (-100) = the coupling springs talking. "
               "Both matrices SYMMETRIC - reciprocity is already baked in.")))
    s += [P("Step 2 - eigenvalues (free vibration, assume e^(jwt)):", h3)]
    s.append(B("det(K - L M) = (200-L)(100-L) - 10000 = L2 - 300 L + 10000 "
               "= 0."))
    s.append(B("L = [300 +- sqrt(90000-40000)]/2 = [300 +- 223.6]/2."))
    s.append(F(formula_text("L1 = 38.2 -> w1 = 6.18 rad/s (f1 = 0.98 Hz)")))
    s.append(F(formula_text("L2 = 261.8 -> w2 = 16.18 rad/s (f2 = 2.58 Hz)")))
    s += [P("Step 3 - eigenvectors (shapes): back-substitute each L:", h3)]
    s.append(B("Row 1: (200-L) u1 - 100 u2 = 0 -> u2/u1 = (200-L)/100."))
    s.append(B("Mode 1: (200-38.2)/100 = <b>1.618</b> -> u1 = [1, 1.618] "
               "(together, mass 2 swings 62% MORE)."))
    s.append(B("Mode 2: (200-261.8)/100 = <b>-0.618</b> -> u2 = [1, -0.618] "
               "(opposite, mass 2 swings less)."))
    s.append(box("Golden ratio Easter egg:",
                 key("1.618 = PHI, and 0.618 = 1/PHI. Not a coincidence of "
                 "YOUR rig only - symmetric 2DOF systems breed golden "
                 "ratios. Nature signs her work."), GREEN, PALE_GREEN))
    s += [P("Step 4 - orthogonality CHECK (prove it, don't quote it):", h3)]
    s.append(F(formula_text("u1(T) M u2 = 1x1 + 1.618x(-0.618) = 1 - 1.000 = 0. VERIFIED.")))
    s.append(P("If this were NOT ~0, your eigensolver (or arithmetic) lied. "
               + lab("Pros run this as <b>pseudo-orthogonality</b>: test "
               "shapes vs FEM shapes through FEM mass matrix. Off-diagonal "
               "~0 = shapes agree; big values = somebody is wrong.")))
    s += [P("Step 5 - modal masses + stiffnesses:", h3)]
    s.append(tbl([
        ["Mode", "mi = u(T)Mu", "ki = u(T)Ku", "Check: wi2 x mi"],
        ["1", "1 + 1.618^2 = 3.618", "138.2", "38.2 x 3.618 = 138.2 OK"],
        ["2", "1 + 0.618^2 = 1.382", "361.8", "261.8 x 1.382 = 361.8 OK"],
    ], [FRAME_W * 0.14, FRAME_W * 0.32, FRAME_W * 0.22, FRAME_W * 0.32]))
    s.append(P("ki = wi2 mi MUST hold (it is the same eigenfact, weighed). "
               "Two independent computations agreeing = you are safe."))
    s += [P("Step 6 - mass-normalize (divide by sqrt(mi)):", h3)]
    s.append(F(formula_text("PHI1 = [0.526, 0.851],   PHI2 = [0.851, -0.526]")))
    s.append(P("Unity modal mass (PHI(T) M PHI = 1) is THE standard scaling: "
               "residues become clean shape-products. " + trap("Unscaled "
               "shapes ([1, 1.618]) show PATTERN only; scaled shapes give "
               "correct RESPONSE levels. Mixing them = wrong amplitudes!")))
    s += [P("Step 7 - residues (shape-product table - REAL numbers):", h3)]
    s.append(tbl([
        ["", "h11", "h12 = h21", "h22"],
        ["Mode 1 (A)", "0.276", "+0.447", "0.724"],
        ["Mode 2 (A)", "0.724", "-0.447", "0.276"],
    ], [FRAME_W * 0.24, FRAME_W * 0.25, FRAME_W * 0.26, FRAME_W * 0.25]))
    s.append(P(key("Reciprocity VISIBLE: A12 = A21 in EVERY mode (+0.447 / "
                   "-0.447). Residue SIGN = peak direction: mode 2's h12 "
                   "imag peak points DOWN. Negative peaks are not errors!")))
    s += [P("Step 8 - STATICS verify DYNAMICS (the mic-drop check):", h3)]
    s.append(F(formula_text("h11(0) = 0.276/38.2 + 0.724/261.8 = 0.00724 + 0.00276 = 0.0100")))
    s.append(P("Push m1 statically: ONLY k1 stretches (m2 rides free) -> x1 "
               "= F/100 = <b>0.01</b>. Modal sum says 0.0100. EXACT. " +
               key("Two alien math worlds agree to 4 decimals - the theory "
               "is TRUE, not just pretty.")))
    s.append(B("Mode 1 alone gives 0.00724 (72%); mode 2 contributes 28% as "
               "<b>residual stiffness</b>. Truncate mode 2 and you lose over "
               "a quarter of static answer - residuals MATTER (1.7 "
               "callback!)."))
    s += [P("Step 9 - full FRF near resonance (z1 = 2%, z2 = 3%, w = 6):",
            h3)]
    s.append(B("Mode 1 denom: (38.2-36) + j(2x0.02x6.18x6) = 2.2 + j1.48; "
               "term = 0.276/2.657 at -34 deg = 0.104 at -34 deg."))
    s.append(B("Mode 2 denom: (261.8-36) + j(2x0.03x16.18x6) = 225.8 + "
               "j5.83; term = 0.0032 at -1.5 deg (negligible!)."))
    s.append(F(formula_text("h11(6 rad/s) ~ 0.089 - j0.058  (|.| ~ 0.107, angle -33 deg)")))
    s.append(P(key("At 6 rad/s (3% below mode 1): response is 97% MODE 1. "
                   "Off-resonance modes answer quasi-statically - small, "
                   "real, in-phase. THIS is why truncation + residuals "
                   "works.")))
    s.append(box("Masterclass graduation:",
                 "You just: wrote EOMs, solved eigen by hand, verified "
                 "orthogonality, weighed modal m/k, normalized shapes, built "
                 "residues, verified against statics, and evaluated a damped "
                 "FRF. That is literally Ch.2's whole engine, fingerprinted. "
                 + tryit("Victory lap: recompute h22(0) = 0.724/38.2 + "
                 "0.276/261.8 = 0.0200. Static check: push m2: k1 AND k2 in "
                 "series -> x2 = F(1/100+1/100) = <b>0.02</b>. Again exact. "
                 "Cry a little."), GREEN, PALE_GREEN))

    # ===== 2.3B =====
    s += heading("(2.3B)", "MDOF II: eigen to FRF sums")
    s += [P("Eigensolution, conceptually (the book's walk-through):", h3)]
    s.append(B("Step 1: det(K - L M) = 0 -> polynomial -> roots = eigenvalues "
               "(w2). Small rigs: Jacobi/Givens/Householder (direct, ALL "
               "modes). Giant FEM: subspace/Lanczos (iterative, LOWEST modes "
               "only - the ones that matter)."))
    s.append(B("Step 2: plug L1 back, solve (Crout/Cholesky/LDL) -> vector = "
               "shape 1. Repeat. (EX-M did this by hand - same moves!)"))
    s.append(B("Step 3: physics at each root: elastic = inertial forces "
               "(DYNAMIC EQUILIBRIUM), nodes with equal +/- lobes."))
    s.append(tbl([
        ["Solver family", "Gets", "Use when"],
        ["Direct (Jacobi, Givens, Householder)", "ALL eigenpairs, exact-ish", "Small matrices, teaching, checks"],
        ["Iterative (subspace, Lanczos)", "Lowest m modes", "100k+ DOF FEM (cars, planes)"],
        ["Root polish (Newton/Secant)", "Refines det roots", "Inside hybrid codes"],
    ], [FRAME_W * 0.34, FRAME_W * 0.32, FRAME_W * 0.34]))
    s.append(box("EX-N: 2DOF intuition (say it in words):",
                 "Mode 1 (0.98 Hz): masses TOGETHER, middle spring lazy -> "
                 "soft -> LOW f. Mode 2 (2.58 Hz): masses OPPOSED, middle "
                 "spring stretched double -> stiff -> HIGH f. " + key("Every "
                 "MDOF mode = an independent dance move; every real motion "
                 "= a mix. (EX-M proved the numbers; this is the story.)"),
                 GREEN, PALE_GREEN))
    s += [P("DERIVE: orthogonality in 5 lines (the book p145-146):", h3)]
    s.append(B("Line 1: K ui = wi2 M ui (eigen-i). Line 2: pre-multiply by "
               "uj(T): uj(T) K ui = wi2 uj(T) M ui."))
    s.append(B("Line 3: same with i,j swapped: ui(T) K uj = wj2 ui(T) M uj."))
    s.append(B("Line 4: transpose line 3 (K, M symmetric!): uj(T) K ui = wj2 "
               "uj(T) M ui."))
    s.append(B("Line 5: subtract from line 2: 0 = (wi2 - wj2) uj(T) M ui -> "
               "wi != wj forces <b>uj(T) M ui = 0</b>. SAME for K. DONE."))
    s.append(F(formula_text("i != j: uj(T)M ui = 0, uj(T)K uj-ish = 0.  i=j: mi, ki (modal m, k).")))
    s.append(P(trap("SYMMETRY did all the work (line 4). No symmetry (gyros, "
                    "control feedback) = no clean orthogonality = complex "
                    "modes (preview, not Ch.2).")))
    s += [P("Modal transformation: the uncoupling machine:", h3)]
    s.append(F(formula_text("{x} = [U]{p}   ->   mi p'' + ci p' + ki p = fi = ui(T){F}")))
    s.append(KeepTogether(xform_sketch()))
    s.append(B("Why it works: pre-multiply EOM by [U](T): [U](T)[M][U] = "
               "diag(mi) and [U](T)[K][U] = diag(ki) BY orthogonality. "
               "Damping needs <b>proportional C</b> (aM + bK) to join the "
               "diagonal party."))
    s.append(B("Modal force fi = ui(T) F: dot product = how ALIGNED the push "
               "is with shape i. Push at a node -> fi = 0 -> mode sleeps. "
               "(Node rule, third birth certificate!)"))
    s.append(P(tryit("EX-P: EX-M rig, F = [1, 0] (push m1 only). Modal "
                     "forces (unnormalized u): f1 = 1x1 + 1.618x0 = 1.0; f2 "
                     "= 1x1 + (-0.618)x0 = 1.0. Push m2 only, F=[0,1]: f1 = "
                     "1.618 (mode 1 LOVES tip pushes), f2 = -0.618. Same "
                     "newton, different music!")))
    s += [P("Truncation + residuals: why m &lt;&lt; n works:", h3)]
    s.append(B("Keep modes to ~1.5-2x your max frequency of interest. Higher "
               "modes answer quasi-STATICALLY (they never resonate in-band) "
               "-> fold them into <b>residual stiffness/mass terms</b> (Ch.1 "
               "1.7 callback: the curvefitter's 'residuals' input!)."))
    s.append(B("EX-M receipt: mode-1-only statics = 72%; + mode-2 residual = "
               "100%. Drop high modes WITHOUT residuals = lose statics. "
               "Drop WITH = engineering."))
    s.append(box("EX-Q: blade to 50 Hz (modes 8/22/47/130/260 Hz):",
                 "Keep 3 (m = 3, n = thousands). Modes 4-5 contribute "
                 "stiffness-like leftovers -> residual term. Response error "
                 "~1-2% in-band. " + key("This paragraph justifies every "
                 "modal reduction in industry."), BLUE, PALE_BLUE))
    s += [P("Laplace MDOF: global poles PROVEN by example:", h3)]
    s.append(F(formula_text("[H(s)] = adj[B(s)] / det[B(s)]   (B symmetric -> H symmetric!)")))
    s.append(tbl([
        ["FRF", "Poles (global!)", "Residues (local)"],
        ["h11", "-z1w1+-jw1, -z2w2+-jw2", "M1: 0.276, M2: 0.724"],
        ["h12 = h21", "SAME poles", "M1: +0.447, M2: -0.447"],
        ["h22", "SAME poles", "M1: 0.724, M2: 0.276"],
    ], [FRAME_W * 0.2, FRAME_W * 0.4, FRAME_W * 0.4]))
    s.append(P(key("POLES identical down the column (denominator shared); "
                   "RESIDUES all different (numerators per i,j). Global vs "
                   "local - now a TABLE, not a slogan. ") + lab("Fit giving "
                   "different freqs per FRF? Your estimator is sick - poles "
                   "are global, enforce it (global curvefitting, Ch.5).")))
    s.append(B("Reciprocity sketch: B symmetric -> adj(B) symmetric -> H "
               "symmetric -> <b>Hij = Hji</b>. Ch.1's row/column rule, "
               "derived from matrix symmetry in ONE line."))


    # ===== 2.3C =====
    s += heading("(2.3C)", "MDOF III: sums, beam, domains")
    s += [P("FRF summation: read it like a story:", h3)]
    s.append(F(formula_text("hij(jw) = SUM_r  Aijr/(jw - Lr)  [+ conj]   (residue face)")))
    s.append(F(formula_text("hij(jw) = SUM_r  uir ujr / [mr(wr2-w2+j2zrw rw)]   (shape face)")))
    s.append(KeepTogether(filterbank_sketch()))
    s.append(B("Input filter <b>ujr</b>: shape at the HAMMER (push a node -> "
               "mode starves). SDOF amplifier: part 2.2, peaks at wr. "
               "Output filter <b>uir</b>: shape at the SENSOR (sense a node "
               "-> mode hides)."))
    s.append(KeepTogether(mdofsum_sketch()))
    s.append(P(key("The summed curve is what you MEASURE; the humps are what "
                   "you EXTRACT. Curvefitting = unmixing paint back to "
                   "primary colors.")))
    s += [P("Sine at any frequency: who answers? (book's 2DOF demo):", h3)]
    s.append(tbl([
        ["Excitation", "Mode 1 says", "Mode 2 says", "Total looks like"],
        ["Below both", "Leads (soft, big)", "Follows weakly", "~ Mode 1"],
        ["Near mode 2", "Quasi-static leftover", "RESONATES", "~ Mode 2"],
        ["Between", "Fades with phase", "Rises with phase", "Hybrid (Ch.1 ODS!)"],
        ["Above both", "Mass-like, tiny", "Mass-like, tiny", "Small, mass-ruled"],
    ], [FRAME_W * 0.2, FRAME_W * 0.26, FRAME_W * 0.26, FRAME_W * 0.28]))
    s.append(P("Time traces below each case (book Figs 2.35-37): single "
               "clean sine near a mode (one singer), beating/complex "
               "between (two singers arguing). " + link("Frequency domain "
               "separates the singers; time domain mashes them - Ch.1's "
               "lesson, quantified.")))
    s += [P("Cantilever beam, 3 points: guided tour:", h3)]
    s.append(KeepTogether(cantilever3_sketch()))
    s.append(tbl([
        ["FRF", "Role", "Watch for"],
        ["h33 (drive, tip)", "Sum of oscillators; peak-valley alternation", "Per-mode decomposition beneath"],
        ["h32, h31 (cross)", "Same poles, new residue weights", "A mode shrinks as force nears its node"],
        ["ROW (roving hammer)", "Fixed accel reference", "Ch.1 rule: DERIVED now"],
        ["COLUMN (fixed shaker)", "Fixed force reference", "Read mode 1 down column 3!"],
    ], [FRAME_W * 0.24, FRAME_W * 0.4, FRAME_W * 0.36]))
    s.append(P("Illustrative shapes (book-style): M1 = [0.25, 0.65, 1.0], M2 "
               "= [0.6, 1.0, -0.4] (node between 2-3!), M3 = [1.0, -0.5, "
               "0.3]. " + key("M2's TIP value is NEGATIVE: every mode-2 "
               "imag peak with tip involved flips DOWN. Sign = shape "
               "polarity, not error.")))
    s.append(KeepTogether(waterfall_sketch()))
    s.append(box("EX-R: read the waterfall:",
                 "Four FRFs (tip ref), M1 ridge heights [0.5, 1.2, 2.1, "
                 "3.0] -> normalize: [0.17, 0.4, 0.7, 1.0] = bending shape. "
                 "M2 ridge: [0.9, 1.5, 0.2, -1.1] -> node between points "
                 "3-4! " + lab("Read DOWN a ridge = shape. Read ACROSS a "
                 "curve = spectrum. Two readings, one plot."), GREEN,
                 PALE_GREEN))
    s += [P("Time-frequency-modal: three doors, one room:", h3)]
    s.append(KeepTogether(domains_sketch()))
    s.append(tbl([
        ["Door", "Math object", "Convert with"],
        ["Time", "x(t) = SUM PHIr pr(t): decaying sines", "Laplace/FFT -> freq"],
        ["Frequency", "H(jw) = SUM SDOF humps", "Inverse FFT -> time"],
        ["Modal", "mi p'' + ci p' + ki p = fi + shapes", "[U] both ways"],
    ], [FRAME_W * 0.18, FRAME_W * 0.46, FRAME_W * 0.36]))
    s += [P("Turbine blade: the full computation (2.3.9):", h3)]
    s.append(B("Impulse near root (cantilever model), tip response wanted: "
               "eigensolve FEM -> modal m/c/k + modal force per mode -> "
               "solve 3 trivial SDOF time responses -> PROJECT BACK with "
               "shapes -> add. Total tip trace with each mode's share "
               "beneath."))
    s.append(P(key("This loop is EVERY commercial solver's inner core "
                   "(Nastran/Ansys/Abaqus modal dynamics). The book's GIF "
                   "animation shows the shares evolving - motion beats "
                   "equations for gut feel.")))
    s.append(P(tryit("EX-S: blade modes 8/22/47 Hz (z = 1/1.5/2%). Hit near "
                     "root (all modal forces strong). Which mode rings "
                     "LONGEST? 8 Hz (lowest z x w: decay 1/(z w) = 2.0 s vs "
                     "0.48/0.17 s). Tip trace after 1 s ~= pure mode 1 - "
                     "high modes already asleep!")))

    # ===== 2.4 =====
    s.append(PageBreak())
    s += heading("(2.4)", "The whole EMA loop - block by block")
    s.append(KeepTogether(fullloop_sketch()))
    s.append(tbl([
        ["Block", "Does", "Owns the error if wrong"],
        ["FEM assume", "Guesses M, K, BCs", "Joints/BCs (Sofia's bracket!)"],
        ["Eigensolve", "Freqs + shapes, NO damping", "Mesh too coarse, missed modes"],
        ["Laplace H(s)", "adj/det -> poles + residues", "Non-proportional damping model"],
        ["Synthesize FRF", "Predict ANY hij", "Truncation without residuals"],
        ["Measure + FFT", "Real F, real X", "Leakage, mass loading, bad cal"],
        ["Curvefit", "Extract poles + residues", "Wrong mode count, narrow band"],
        ["Validate", "Test vs FEM, update", "Skipping it (the actual sin)"],
    ], [FRAME_W * 0.2, FRAME_W * 0.44, FRAME_W * 0.36]))
    s.append(P(key("Forward = predict from assumptions. Backward = identify "
                   "from data. SAME objects (poles/residues) both ways. The "
                   "gap = modeling + measurement error. Career = shrinking "
                   "both. Next: Ch.3 signals, Ch.4 excitation, Ch.5 "
                   "estimators.")))

    # ===== DEEP-1 =====
    s.append(PageBreak())
    s += heading("(Deep 1)", "SDOF derivations - earn every formula")
    s += [P("How wrong is wd ~ wn? (error table - quote with confidence):", h3)]
    s.append(tbl([
        ["z", "1%", "2%", "5%", "10%", "20%", "30%"],
        ["wd/wn", "0.99995", "0.99980", "0.99875", "0.99499", "0.97980", "0.95394"],
        ["Error of ~", "0.005%", "0.02%", "0.13%", "0.5%", "2.0%", "4.6%"],
    ], [FRAME_W * 0.16, FRAME_W * 0.14, FRAME_W * 0.14, FRAME_W * 0.14,
        FRAME_W * 0.14, FRAME_W * 0.14, FRAME_W * 0.14]))
    s.append(P(key("Steel structures (z ~ 1-3%): wd = wn for all practical "
                   "purposes. Rubber mounts (z ~ 15%+): do the sqrt - 1%+ "
                   "error bites in tuning.")))
    s += [P("DERIVE: where each peak REALLY sits (d/dw = 0):", h3)]
    s.append(B("D/F: minimize (1-b2)2+(2zb)2: derivative 4b(b2-1+2z2) = 0 -> "
               "<b>b_D = sqrt(1-2z2)</b> (needs z &lt; 0.707 or NO peak!)."))
    s.append(B("V/F: maximize b2/denom -> <b>b_V = 1 EXACTLY</b> (velocity "
               "resonance = undamped fn - the purist's resonance)."))
    s.append(B("A/F: maximize b4/denom -> <b>b_A = 1/sqrt(1-2z2)</b> "
               "(mirror of D above wn)."))
    s.append(KeepTogether(peakshift_sketch()))
    s.append(tbl([
        ["z", "5%: b_D / b_A", "10%: b_D / b_A", "30%: b_D / b_A"],
        ["Peak spots", "0.9975 / 1.0025", "0.9899 / 1.0102", "0.9055 / 1.1044"],
    ], [FRAME_W * 0.14, FRAME_W * 0.28, FRAME_W * 0.28, FRAME_W * 0.30]))
    s.append(P(trap("At z = 30% the D and A 'resonances' sit 20% APART. "
                    "'Resonance at 100 Hz' without naming the FRF form is "
                    "meaningless past z ~ 10%.")))
    s += [P("DERIVE: real/imag split (co-quad from algebra):", h3)]
    s.append(B("H = 1/[(k-mw2) + j(cw)]: multiply top+bottom by conjugate:"))
    s.append(F(formula_text("Re = (k-mw2)/D,  Im = -(cw)/D,  D = (k-mw2)^2+(cw)^2")))
    s.append(B("At w = wn: k-mw2 = 0 -> <b>Re = 0, Im = -1/(c wn)</b> (pure "
               "imag peak!). Below: Re > 0 (stiffness-like). Above: Re &lt; "
               "0 (mass-like). The zero-crossing IS the resonance."))
    s.append(box("EX-T: full complex FRF at 3 spots (m=2, k=8000, c=8):",
                 "Static: 1/8000 = 1.25e-4.<br/>w=30: den 6200+j240 -> "
                 "<b>Re 1.61e-4, Im -6.2e-6</b>, |.| 1.61e-4, phase -2.2 "
                 "deg (static-like, tiny lag).<br/>w=63.25 (reso): den j506 "
                 "-> <b>Re 0, Im -1.98e-3</b>, phase <b>-90 deg</b>, 15.8x "
                 "static (= Q. of course).<br/>w=120: den -20800+j960 -> "
                 "<b>Re -4.80e-5, Im -2.2e-6</b>, phase -177 deg (mass "
                 "world, nearly flipped).<br/>" + key("Watch Re change SIGN "
                 "across reso while Im stays negative and peaks: THE "
                 "co-quad signature, computed not drawn."), BLUE,
                 PALE_BLUE))
    s.append(P(tryit("EX-U: velocity resonance is EXACTLY wn - verify: |V| = "
                     "w|H|. w=60: 60x1.072e-3 = 0.0643. w=63.25: "
                     "63.25/506 = <b>0.125 = 1/c</b>. w=66: 66x1.128e-3 = "
                     "0.0744. Peak AT wn, value 1/c: mobility resonance in "
                     "one line.")))
    s += [P("SKETCH-PROOF: why Nyquist is a circle (mobility):", h3)]
    s.append(B("V/F = jw/(k-mw2+jcw). With a page of algebra it rearranges to "
               "|V - 1/(2c)| = 1/(2c): points equidistant from (1/2c, 0) = "
               "<b>CIRCLE diameter 1/c</b> through origin + top."))
    s.append(B("Resonance = TOP of circle (max imag, fastest sweep). "
               "Diameter reads damping DIRECTLY (big circle = light "
               "damping). Circle-fit = the grandfather of estimators."))
    s.append(P(lab("Sweep-speed trick: equal-freq data points BUNCH at "
                   "resonance (phase rushing) and spread elsewhere. Bunch "
                   "location = resonance even before you fit. - Lena")))

    # ===== DEEP-2 =====
    s.append(PageBreak())
    s += heading("(Deep 2)", "Damping lab + reading protocol")
    s += [P("Rayleigh damping: fit z at TWO freqs, get C for free:", h3)]
    s.append(B("Assume C = aM + bK -> modal: ci = a mi + b ki -> divide by "
               "2 mi wi: <b>zr = a/(2wr) + b wr/2</b> (mass-term falls, "
               "stiffness-term rises: U-curve!)."))
    s.append(KeepTogether(rayleigh_sketch()))
    s.append(box("EX-V: fit z1=2% at w1=6.18, z2=3% at w2=16.18:",
                 "a/12.36 + 3.09 b = 0.02; a/32.36 + 8.09 b = 0.03. Solve: "
                 "<b>b = 0.00324, a = 0.124</b>. Check mode 2: "
                 "0.124/32.36 + 0.00324x8.09 = 0.0038+0.0262 = 0.030. "
                 "EXACT.<br/>Extrapolate: w=30 -> z = 5.1%; w=60 -> "
                 "<b>9.8%</b>! " + trap("Stiffness-term overdamps high "
                 "modes. Rayleigh is a LOCAL fit: trust it INSIDE [w1, w2], "
                 "nowhere else. - Meera"), colors.HexColor("#B26A00"),
                 PALE_YELLOW))
    s.append(tbl([
        ["Damping model", "Force law", "zr vs w", "Use when"],
        ["Viscous", "c x' (ellipse ~ w)", "You set per mode", "Default; Ch.2 world"],
        ["Rayleigh", "aM + bK", "U-curve (fit 2 pts)", "Time simulation needing C"],
        ["Hysteretic", "k(1+j n) (ellipse const)", "~ n/2 flat", "Rubber/joints; freq-domain only!"],
    ], [FRAME_W * 0.2, FRAME_W * 0.3, FRAME_W * 0.24, FRAME_W * 0.26]))
    s.append(P("Hysteretic (structural) damping: stiffness carries a constant "
               "imag part n (loss factor, n ~ 2z at reso). Loop area per "
               "cycle = pi n k X2 (amplitude-INDEPENDENT, unlike viscous pi "
               "c w X2). " + trap("H(jw) = 1/(k-mw2+j n k) has NO causal "
               "time twin - freq-domain ONLY. Time-sim it and physics "
               "breaks.")))
    s += [P("Shape scaling: 3 normalizations, same pattern:", h3)]
    s.append(tbl([
        ["Scaling", "Mode-1 shape (EX-M)", "Residue A11,1", "Use"],
        ["Unscaled (u1 = 1)", "[1, 1.618], m = 3.618", "1x1/3.618 = 0.276", "Sketching pattern"],
        ["Max = 1", "[0.618, 1.0]", "Same 0.276 (scale cancels!)", "Plots, slides"],
        ["Mass-normalized", "[0.526, 0.851], m = 1", "0.526x0.526 = 0.276", "RESPONSE math, residues"],
    ], [FRAME_W * 0.22, FRAME_W * 0.3, FRAME_W * 0.28, FRAME_W * 0.2]))
    s.append(P(key("Residues are scaling-INVARIANT: (a u)(a u)/(a2 m) = same "
                   "A. Shapes carry PATTERN; residues carry LEVEL. ") +
               tryit("EX-X: verify A22,1 all three ways: 1.6182/3.618 = "
               "12/1 = 0.8512 = <b>0.724</b>. Three doors, one number.")))
    s += [P("PROTOCOL: read any FRF in 60 seconds:", h3)]
    s.append(KeepTogether(read60_sketch()))
    s.append(tbl([
        ["#", "Check", "How", "Fail means"],
        ["1", "Form?", "Far slopes (0,-2)/(+1,-1)/(+2,0)", "Mislabeled channels"],
        ["2", "Peak candidates?", "Local maxima", "Candidate only, not verdict!"],
        ["3", "Resonance?", "Phase ~90 crossing", "No 90 = no resonance"],
        ["4", "Damping?", "Width -> z ~ Dw/2w", "Too sharp? leakage suspects"],
        ["5", "Drive?", "Valleys alternate?", "Cross FRF or contaminated drive"],
        ["6", "Polarity?", "Imag sign per mode", "Sign flip = shape node crossed"],
        ["7", "Trust?", "Coherence ~ 1 + repeat", "Retest, do not fit garbage"],
    ], [FRAME_W * 0.08, FRAME_W * 0.2, FRAME_W * 0.38, FRAME_W * 0.34]))
    s.append(box("Drive-point failure gallery (diagnose in seconds):",
                 "<b>Case A - valley MISSING between peaks:</b> neighbor "
                 "mode flooding in, or overload flattening. Fix: finer "
                 "resolution, check input levels.<br/><b>Case B - imag peaks "
                 "opposite sides on a 'drive' FRF:</b> channels SWAPPED "
                 "(force/response crossed) or wrong DOF. Fix: re-label, "
                 "re-measure.<br/><b>Case C - phase mushy, no clean flip:</b> "
                 "leakage / noise / nonlinearity. Fix: window, average, "
                 "burst/chirp, lower level.", RED, PALE_PINK))

    # ===== DEEP-3 =====
    s.append(PageBreak())
    s += heading("(Deep 3)", "MDOF extras + Ch.3 bridge")
    s += [P("Rigid-body modes: the zeros that matter:", h3)]
    s.append(B("Free-free (no constraints): K SINGULAR -> 6 ZERO eigenvalues "
               "(3 translate + 3 rotate). Shapes = rigid motions (no strain, "
               "no stress). FRF low end = mass line -1/(m w2)."))
    s.append(B("Test trick: hang the part on SOFT bungees (suspension f &lt; "
               "10% of first flex mode) -> rigid modes park near 0 Hz, "
               "flex modes untouched. Stiff support = free-free LOST."))
    s.append(P(trap("Zero-frequency 'resonance' with flat shape = rigid mode, "
                    "NOT a flex mode. Fitting it as elastic bends neighbors. "
                    "- Viktor")))
    s += [P("Beyond proportional: complex modes + checks (honest boxes):", h3)]
    s.append(box("Real vs complex modes:",
                 "Proportional C -> shapes REAL (all DOFs in/180 deg "
                 "together). General viscous C (real joints!) -> shapes "
                 "COMPLEX (traveling-wave phase spread). " + key("Ch.2 "
                 "assumes proportional; Ch.5 estimators + Ch.9 cases handle "
                 "the wild. If your 'shape' will not animate cleanly - "
                 "complex-mode suspect."), BLUE, PALE_BLUE))
    s.append(box("Pseudo-orthogonality + MAC (preview with teeth):",
                 "Check test shapes {e} against FEM: {e}(T) [Mfem] {e} "
                 "should be ~diagonal (pseudo-orthogonality). MAC = "
                 "normalized shape correlation 0-1 (diagonal ~1 = match). "
                 "Full MAC + validation = Ch.5 territory; the FORMULAS live "
                 "here because Ch.2 owns orthogonality.", GREEN,
                 PALE_GREEN))
    s += [P("BRIDGE to Ch.3: damping DICTATES your measurement:", h3)]
    s.append(P("To resolve a peak you need SEVERAL spectral lines inside its "
               "half-power bandwidth: rule of thumb <b>Df &lt;= (2 z fn)/5 "
               "</b> (5+ lines across Dw). Light damping = LONG records "
               "(T = 1/Df) or leakage eats you."))
    s.append(tbl([
        ["fn = 100 Hz, z", "Bandwidth Dw", "Need Df &lt;=", "Record T >=", "Verdict"],
        ["0.5%", "1.0 Hz", "0.2 Hz", "5 s", "Long + averaging!"],
        ["1%", "2.0 Hz", "0.4 Hz", "2.5 s", "Careful windows"],
        ["2%", "4.0 Hz", "0.8 Hz", "1.25 s", "Routine"],
        ["5%", "10 Hz", "2 Hz", "0.5 s", "Easy peak"],
    ], [FRAME_W * 0.22, FRAME_W * 0.18, FRAME_W * 0.2, FRAME_W * 0.18,
        FRAME_W * 0.22]))
    s.append(P(key("THIS table is why Ch.2 comes before Ch.3: theory tells "
                   "you what resolution to BUY. z = 0.5% with Df = 1 Hz = "
                   "measuring a needle with a ruler.")))
    s.append(box("EX-Y: residual bookkeeping (EX-M h11):",
                 "Exact static 0.0100. Mode-1-only: 0.00724. Residual R = "
                 "0.00276 (mode-2's quasi-static gift). In fitting: hij ~ "
                 "SDOF1 + R (+ mass-residual at high f). " + lab("Always "
                 "plot data-vs-synthesis OUTSIDE the fit band: drift = "
                 "missing/broken residuals. - Viktor"),
                 colors.HexColor("#B26A00"), PALE_YELLOW))
    s.append(box("EX-Z: the wandering pole (diagnose!):",
                 "Fit says f1 = 50.1 Hz from h11 but 51.3 from h22. "
                 "Checklist: (1) band too tight around 50? (2) neighbor at "
                 "~55 hiding? (3) reference/level changed between runs? (4) "
                 "temperature drift? (5) coherence dip at 51? " +
                 key("Fix: widen band, include neighbor, GLOBAL refit. Poles "
                 "are global - wandering poles indict the FIT, not physics."),
                 RED, PALE_PINK))
    s += [P("Exam + lab traps (the wall of pain):", h3)]
    s.append(tbl([
        ["Trap", "Truth"],
        ["rad/s vs Hz in formulas", "wn, wd, Dw: rad/s. fn, Df: Hz. Convert: w = 2 pi f. #1 exam killer."],
        ["z = 2 vs 2%", "z = 0.02! Percent/decimal slips move poles 100x."],
        ["-3 dB from WHERE", "From the PEAK, not full-scale. Wrong ref = fantasy z."],
        ["Log-dec on multi-mode", "Beating fakes decay. Single-mode ONLY (or filter first)."],
        ["kN/mm to N/m", "x1e6! 30 N/mm = 30,000 N/m. Units kill FEMs daily."],
        ["Phase sign", "Lags are negative (response AFTER force). Say 'lag 90', not '-90 or +270?'."],
        ["Nyquist direction", "Sweep passes resonance counter...: note YOUR analyzer's convention once, keep it."],
        ["Coherence = calibration?", "NO: coherence 1.0 with wrong sensitivity = precisely wrong. Calibrate!"],
    ], [FRAME_W * 0.26, FRAME_W * 0.74]))
    s.append(P(link("Solver gotchas (from the chooser table): Lanczos can "
                    "SKIP close modes (shift + verify count!); rigid modes "
                    "come out ~1e-3 Hz not 0 (numerical dust - fine); "
                    "always compare mode COUNT vs expected in-band.")))

    # ===== DEEP-4 =====
    s.append(PageBreak())
    s += heading("(Deep 4)", "Zeros, synthesis, transients")
    s += [P("Zeros: where drive-point FRFs touch ZERO (derived!):", h3)]
    s.append(B("Undamped h11 = A1/(w12-w2) + A2/(w22-w2). Set = 0: A1(w22-w2) "
               "+ A2(w12-w2) = 0 -> w2 = (A1 w22 + A2 w12)/(A1+A2)."))
    s.append(box("EX-AA: the anti-resonance of EX-M (compute it!):",
                 "A1 = 0.276, A2 = 0.724, w12 = 38.2, w22 = 261.8: w2 = "
                 "(0.276x261.8 + 0.724x38.2)/1.0 = (72.36+27.64) = <b>100.0"
                 "</b> -> wz = <b>10.0 rad/s (1.59 Hz)</b>.<br/>" +
                 key("Sits BETWEEN w1 = 6.18 and w2 = 16.18: poles and "
                 "zeros INTERLACE (drive points only!). Valley depth -> "
                 "infinity undamped; damping fills it in. You just "
                 "PREDICTED a valley from residues."),
                 colors.HexColor("#B26A00"), PALE_YELLOW))
    s.append(P("Physics of zeros: at wz the two modal contributions are "
               "EQUAL and OPPOSITE - the drive point stands STILL while the "
               "rest moves (vibration absorber principle!). " +
               trap("Cross FRFs: zeros wander anywhere - no interlacing, no "
               "alternation. Alternation is a DRIVE-POINT privilege.")))
    s += [P("EX-AB: synthesize h12 AT mode-2 resonance (phase flip!):", h3)]
    s.append(B("w = 16.18, z1 = 2%, z2 = 3%. Mode 1: 0.4472/(-223.6+j4.0) ~ "
               "-0.0020 (real leftover). Mode 2: -0.4472/(j15.71) = "
               "<b>+j0.0285</b> (NEGATIVE residue!)."))
    s.append(F(formula_text("h12(16.18) ~ -0.0020 + j0.0285  (|.| 0.0286, angle +94 deg)")))
    s.append(P(key("Usual resonance: -90 deg. NEGATIVE residue: +94 deg - "
                   "phase FLIPPED 180. Cross-FRF phases read residue SIGNS: "
                   "your phase plot is a shape-polarity map.")))
    s += [P("Transient trio: impulse, step, release (formulas + feel):", h3)]
    s.append(tbl([
        ["Input", "Response x(t) (underdamped)", "Signature"],
        ["Initial x0 (release)", "x0 e^(-zwnt)[cos wdt + z/sqrt(1-z2) sin wdt]", "Ring-down (log-dec lives here)"],
        ["Impulse I", "(I/mwd) e^(-zwnt) sin wdt", "Pure sine envelope: THE impulse response"],
        ["Step F0", "(F0/k)[1 - e^(-zwnt)(cos wdt + ...)]", "Overshoot ~ e^(-pi z/sqrt(1-z2))"],
    ], [FRAME_W * 0.2, FRAME_W * 0.5, FRAME_W * 0.3]))
    s.append(box("EX-AC: release EX3 rig from 5 mm (z = 3.16%):",
                 "Td = 2 pi/63.24 = 0.0993 s. Half-period decay: "
                 "e^(-0.0316x63.25x0.0497) = e^-0.0993 = 0.905. First "
                 "negative peak ~ <b>-4.5 mm</b> at 0.0497 s. Each swing "
                 "keeps ~90%: after 10 cycles ~35% left. " +
                 tryit("Count swings to half amplitude: ln2/(2 pi z) = "
                 "3.5 cycles. Quick lab estimate of z from ANY ring-down!"),
                 colors.HexColor("#B26A00"), PALE_YELLOW))
    s.append(box("Beats: why log-dec dies on close modes:",
                 "x = sin(2 pi 10 t) + sin(2 pi 10.5 t) = 2 cos(2 pi 0.25 t) "
                 "sin(2 pi 10.25 t): 10.25 Hz carrier inside a <b>2-second "
                 "breathing envelope</b>. Peaks wobble from INTERFERENCE, "
                 "not damping. " + trap("Log-dec on beats = random numbers. "
                 "Frequency domain separates the singers; time domain "
                 "records their argument."), RED, PALE_PINK))

    # ===== DEEP-5 =====
    s.append(PageBreak())
    s += heading("(Deep 5)", "State-space, MIMO, units, links")
    s += [P("State-space: first-order form (where estimators live):", h3)]
    s.append(B("Stack y = [x; v]: then y' = A y + B f with A = [[0, I], "
               "[-inv(M)K, -inv(M)C]]. n 2nd-order eqns -> 2n 1st-order."))
    s.append(B("Eigenvalues of A = THE 2n POLES (complex pairs, always). "
               "Eigenvectors = complex modes + conjugates. Real-modes world "
               "(Ch.2) = special symmetric case of this general machine."))
    s.append(P(link("Why care NOW: every modern estimator (Ch.5: LSCE, ERA, "
                    "PolyMAX...) fits THIS form, then translates back to "
                    "freqs/shapes. Ch.2 is the translation dictionary.")))
    s += [P("DERIVE: proportional damping diagonalizes (3 lines):", h3)]
    s.append(B("Given C = aM + bK: U(T) C U = a U(T)M U + b U(T)K U = a "
               "diag(m) + b diag(k) = <b>diag(c)</b>. DONE - orthogonality "
               "did it again."))
    s.append(F(formula_text("ci = a mi + b ki,   zi = ci/(2 mi wi) = a/(2wi) + b wi/2")))
    s.append(P(tryit("EX-AD: EX-M with z1 = 2%, z2 = 3%: c1 = 2x0.02x6.18"
                     "x3.618 = <b>0.894</b>; c2 = 2x0.03x16.18x1.382 = "
                     "<b>1.342</b> (modal units!). Test gives z; models eat "
                     "c - this line converts.")))
    s += [P("Test alphabet: SISO to MIMO (what you buy per setup):", h3)]
    s.append(tbl([
        ["Setup", "Inputs x Outputs", "You get", "Kills"],
        ["SISO", "1 hammer + 1 accel", "ONE hij (spot checks)", "Quick looks, tiny rigs"],
        ["SIMO", "1 fixed shaker x roving accels", "ONE COLUMN", "Single-ref shapes"],
        ["MISO", "Roving hammer x 1 accel", "ONE ROW", "Fast field surveys"],
        ["MIMO", "Many shakers x many accels", "MANY rows/cols", "Close modes, big iron"],
    ], [FRAME_W * 0.14, FRAME_W * 0.3, FRAME_W * 0.28, FRAME_W * 0.28]))
    s.append(P(key("MIMO costs rigs + channels but SEPARATES close/coupled "
                   "modes single-ref tests fuse. Ch.4 picks; Ch.2 explains "
                   "WHY (independent columns = independent equations).")))
    s += [P("Units cheat sheet (SI modal survival):", h3)]
    s.append(tbl([
        ["Qty", "Unit", "Trap"],
        ["Force", "N", "Hammer tips rated in N - respect them"],
        ["Disp / Vel / Acc", "m / m-s / m-s2 (or mm, g!)", "mm vs m = 1000x; g = 9.81"],
        ["Stiffness", "N/m", "N/mm x1000! kN/mm x1e6!"],
        ["Freq", "Hz (f) vs rad/s (w)", "w = 2 pi f. Formulas want w."],
        ["FRF mag", "m/N, (m/s)/N, (m/s2)/N", "Compare ONLY same form!"],
        ["dB", "20 log10(|H|/ref)", "No ref stated = graffiti, not data"],
    ], [FRAME_W * 0.24, FRAME_W * 0.34, FRAME_W * 0.42]))
    s += [P("Ch.2 results -> where they get USED (dependency map):", h3)]
    s.append(tbl([
        ["Ch.2 result", "Used in", "As"],
        ["Poles (global)", "Ch.5 estimators", "Fit targets (stabilization!)"],
        ["Residues/shapes", "Ch.5 + animation", "Shape extraction + display"],
        ["Bandwidth Dw", "Ch.3 acquisition", "Resolution + record length spec"],
        ["Reciprocity", "Ch.4 MIMO checks", "hij-vs-hji quality gate"],
        ["Orthogonality", "Ch.5 validation", "Pseudo-orth + MAC vs FEM"],
        ["Modal superposition", "Every solver", "Transient/forced response core"],
        ["D/V/A slopes", "Every test day", "First-plot channel detective"],
    ], [FRAME_W * 0.24, FRAME_W * 0.24, FRAME_W * 0.52]))
    s += [P("Practice round 2 (P9-P16) + answers:", h3)]
    probs = [
        "EX-M h11 zero: recompute blind, then state the interlacing rule. [A: wz = 10.0 rad/s; drive zeros sit BETWEEN poles.]",
        "Fit Rayleigh through z = 1.5% at 5 Hz and 2.5% at 20 Hz. Give a, b. [A: w = 31.4/125.7: b = 2.86e-4, a = 0.795. Check both!]",
        "h12 at mode-2 reso gave +94 deg. Explain the sign to a fresher. [A: Negative residue (shapes oppose) rotates phase 180 from the usual -90.]",
        "Ring-down halves in 3.5 swings. z? [A: ln2/(n 2 pi) with n = 3.5: z ~ 3.15%.]",
        "10 + 10.4 Hz equal sines: beat period? [A: Envelope |cos| at 0.2 Hz: 5 s breathing. Log-dec = garbage here.]",
        "Stiffness 45 N/mm in N/m? Static sag of 200 kg on it? [A: 45,000 N/m; sag = 1962/45000 = 43.6 mm.]",
        "V/F peak reads 60.0 Hz, A/F peak 60.5 Hz. z estimate? [A: b_A = 1/sqrt(1-2z2) = 60.5/60 -> z ~ 9.1%. (Heavy! rubber mount?)]",
        "MIMO vs SIMO for a symmetric plate with twin modes? [A: MIMO - single ref fuses repeated roots; independent columns split them.]",
    ]
    for i, a in enumerate(probs, 9):
        s.append(Paragraph(f"<b>P{i}.</b> {a}", bullet, bulletText="*"))

    # ===== DEEP-6 =====
    s.append(PageBreak())
    s += heading("(Deep 6)", "Bode, transients, isolation")
    s += [P("Bode sketching masterclass (D/F, log-log):", h3)]
    s.append(KeepTogether(bode_master_sketch()))
    s.append(tbl([
        ["Piece", "Rule", "EX3 rig values"],
        ["Low-f asymptote", "Flat at 1/k", "1/8000 = 1.25e-4"],
        ["Corner", "At wn (10.07 Hz here)", "63.25 rad/s"],
        ["High-f asymptote", "-2 slope (-40 dB/dec)", "Mass line 1/(m w2)"],
        ["Peak (light z)", "Q = 1/(2z) above corner crossing", "15.8x -> 1.98e-3"],
        ["Phase", "0 far low, 90 AT corner, 180 far high", "~1 decade each side"],
    ], [FRAME_W * 0.2, FRAME_W * 0.44, FRAME_W * 0.36]))
    s.append(P(tryit("EX-AE: sketch EX3 D/F from asymptotes ONLY, then check "
                     "3 exact points: w=30 (1.61e-4 vs flat-ish 1.3e-4: "
                     "close!), w=63.25 (peak, asymptotes useless - that IS "
                     "the lesson), w=120 (4.8e-5 vs mass-line 1/(2x14400) = "
                     "3.5e-5: same street). Asymptotes navigate; exact math "
                     "docks.")))
    s.append(P(trap("Bode peak error: asymptotes MISS the peak by design - "
                    "that gap IS Q. Never read damping off asymptotes; read "
                    "it off the exact peak/hp width.")))
    s += [P("Complex pair = ONE real sine (why pairs matter):", h3)]
    s.append(B("x = A e^(p1 t) + A* e^(p2 t), p1,2 = -z wn +- j wd. Pair them: "
               "x = 2|A| e^(-z wn t) cos(wd t + angle). Imaginary parts "
               "CANCEL - reality restored!"))
    s.append(P(key("This is WHY poles come in pairs: lone complex pole = "
                   "complex (impossible) response. Conjugates are reality's "
                   "bodyguards.")))
    s += [P("Transient + steady-state: how long to WAIT (lab gold):", h3)]
    s.append(B("Start a sine: x = transient (decays e^(-t/tau), tau = "
               "1/(z wn)) + steady sine. Measure during transient = polluted "
               "FRF. Rule: wait <b>4-5 tau</b> (2% left)."))
    s.append(box("EX-AF: EX3 rig (z = 3.16%, wn = 63.25):",
                 "tau = 1/(0.0316x63.25) = <b>0.50 s</b>. Wait 2-2.5 s "
                 "before trusting sine-dwell data. " + lab("Burst-random "
                 "record length rule (Ch.4 preview): capture 4-5 tau of "
                 "DECAY inside one record -> leakage-free WITHOUT windows. "
                 "Theory just sized your acquisition! - Lena"),
                 GREEN, PALE_GREEN))
    s.append(tbl([
        ["z at 10 Hz", "tau", "Wait 4 tau", "Lesson"],
        ["0.5%", "3.2 s", "13 s (!!)", "Bells need patience"],
        ["2%", "0.8 s", "3.2 s", "Typical steel"],
        ["10%", "0.16 s", "0.6 s", "Rubber: quick + easy"],
    ], [FRAME_W * 0.24, FRAME_W * 0.22, FRAME_W * 0.24, FRAME_W * 0.3]))
    s += [P("COUNCIL EXTENSION: transmissibility (isolation design):", h3)]
    s.append(B("Force to ground (or ground to mass): T = sqrt(1+(2zb)2) / "
               "sqrt((1-b2)2+(2zb)2). Isolate (T &lt; 1) needs <b>b &gt; "
               "sqrt(2)</b> - mounts tuned BELOW 0.7x the disturbance!"))
    s.append(box("EX-AG: isolate a 25 Hz machine (want 88% cut):",
                 "Pick mounts fn = 8 Hz (b = 3.125), z = 0.05: T = "
                 "sqrt(1.0977)/sqrt(76.93) = 1.048/8.77 = <b>0.119</b> -> "
                 "88% isolated. " + trap("More damping WORSENS high-f "
                 "isolation (numerator grows)! Soft + light beats stiff + "
                 "dead. Designers get this backwards yearly."),
                 colors.HexColor("#B26A00"), PALE_YELLOW))
    s.append(P(link("Dwell link (Ch.1 plate!): sine-dwell AT reso = "
                    "steady-state sine after transients die: response = "
                    "|H| F at 90 deg lag. Ch.1's experiment was Ch.2's "
                    "forced-response page, performed live.")))

    # ===== DEEP-7 =====
    s.append(PageBreak())
    s += heading("(Deep 7)", "Quotient, absorber, stability, plans")
    s += [P("Rayleigh quotient: guess a shape, bound w1 (from ABOVE!):", h3)]
    s.append(F(formula_text("w^2(u) = [u(T) K u] / [u(T) M u]  >=  w1^2   (ANY u!)")))
    s.append(B("Any guessed shape gives freq ABOVE true mode-1 (energy "
               "truth: wrong shapes strain extra). Better guess -> tighter "
               "bound. Pre-computer engineers lived by this."))
    s.append(box("EX-AH: bound EX-M mode 1 (true w12 = 38.2):",
                 "Guess [1, 1]: Ku = [100, 0] -> u(T)Ku = 100; u(T)Mu = 2 -> "
                 "w2 = <b>50.0</b> (bound, 31% high).<br/>Guess [1, 1.5]: "
                 "Ku = [50, 50] -> 125; mass 3.25 -> w2 = <b>38.46</b> "
                 "(0.7% high!). " + key("Close guess -> near-exact freq. "
                 "Quotient turns sketches into numbers."), BLUE,
                 PALE_BLUE))
    s += [P("Zeros at work: the tuned absorber (design it!):", h3)]
    s.append(B("Attach small (ma, ka) tuned to the trouble freq: drive-point "
               "zero lands ON it -> main mass stands STILL (its energy "
               "parked in the absorber). Skyscrapers + crankshafts run on "
               "this."))
    s.append(box("EX-AI: calm a 100 kg machine shaking at 25 Hz:",
                 "Tune absorber wn,a = 25 Hz: (2 pi 25)2 = 24674. Pick ma = "
                 "5 kg -> ka = 5 x 24674 = <b>123 kN/m</b>. Result: zero at "
                 "25 Hz on the machine (two NEW poles straddle it - check "
                 "they are harmless!). " + trap("Absorbers SPLIT one peak "
                 "into two: retune the band, or trade one problem for two."),
                 GREEN, PALE_GREEN))
    s.append(P("Zero physics you can FEEL: tuning-fork handle nearly still "
               "while tines scream (drive near a zero!); loudspeaker "
               "cabinet dead-spots; the 'node' of Ch.1 = zero of that FRF. "
               "Zeros are not valleys on paper - they are STILLNESS in "
               "metal."))
    s += [P("Stability: poles must live LEFT (negative real!):", h3)]
    s.append(tbl([
        ["Pole home", "Time says", "Meaning"],
        ["Left half (real &lt; 0)", "Decays", "Stable: all Ch.2 systems"],
        ["jω axis (real = 0)", "Rings forever", "Undamped ideal / flutter edge"],
        ["Right half (real &gt; 0)", "GROWS (e^+t)", "UNSTABLE: flutter, chatter, squeal!"],
    ], [FRAME_W * 0.3, FRAME_W * 0.34, FRAME_W * 0.36]))
    s.append(P(key("Brake squeal, wing flutter, tool chatter = poles DEFECTED "
                   "right (friction/aero feeding energy). Modal test + "
                   "stability map = diagnosis. Ch.2's S-plane is also a "
                   "stability radar.")))
    s += [P("Read animated shapes like a pro:", h3)]
    s.append(B("1. Find NODES first (still lines) - they count the mode "
               "order. 2. Check phase colors: two-color flip-flop = real "
               "mode; rainbow crawl = complex/close modes. 3. Amplitude "
               "scale LIES (auto-scaled!) - compare within one animation "
               "only. 4. Slow the loop: twisting vs bending hides at "
               "speed."))
    s.append(P(trap("Peak-picking error audit: neighbor leakage bends BOTH "
                    "height and apparent freq. Close modes (Dw overlap) + "
                    "strong neighbors = fit, do not pick. EX-M was kind "
                    "(4x apart); real life often is not.")))
    s += [P("Study plans (pick your battle):", h3)]
    s.append(tbl([
        ["Plan", "Do", "Skip (for now)"],
        ["1-day sprint", "Map + KEY boxes + sketches + Banks 1-2 + revision", "Derivations, masterclass arithmetic"],
        ["1-week steel", "All EX by hand + Deep 1-3 + Problems P1-P16", "Deep 4-7 (second pass)"],
        ["Interview armor", "FAQ + rapid-fire + protocol + traps + EX-M story", "Hysteretic/state-space detail"],
        ["Lab ready", "Protocol + failure gallery + resolution table + checklist", "Proofs (keep as backup)"],
    ], [FRAME_W * 0.22, FRAME_W * 0.44, FRAME_W * 0.34]))
    s.append(P(link("Where Ch.2 NEVER goes (honest borders): nonlinear "
                    "systems, rotating machinery (gyroscopics), acoustics, "
                    "control-structure interaction. It conquers linear "
                    "stationary vibration - which is 90% of paid modal "
                    "work.")))

    # ===== DEEP-8 =====
    s.append(PageBreak())
    s += heading("(Deep 8)", "Core proofs, fully shown")
    s += [P("PROOF: orthogonality (the engine room):", h3)]
    s.append(B("Modes r, s satisfy (K - wr2 M) ur = 0 and (K - ws2 M) us = 0. "
               "Premultiply mode-r eq by us(T): us(T)K ur = wr2 us(T)M ur."))
    s.append(B("Premultiply mode-s eq by ur(T), transpose (K, M symmetric): "
               "us(T)K ur = ws2 us(T)M ur. SUBTRACT: 0 = (wr2 - ws2) "
               "us(T)M ur."))
    s.append(F(formula_text("wr != ws   =>   us(T) M ur = 0   (and us(T) K ur = 0)")))
    s.append(P(key("Distinct freqs -> automatic M/K-orthogonality. Repeated "
                   "roots: orthogonality must be ENFORCED (Gram-Schmidt) - "
                   "one more reason twins are trouble.")))
    s += [P("PROOF: modal FRF sum from the matrix equation:", h3)]
    s.append(B("Start: (-w2 M + jw C + K) X = F. Expand X = U q "
               "(shape combo!), premultiply by ur(T): orthogonality kills "
               "ALL terms except r:"))
    s.append(F(formula_text("(-w^2 mr + jw cr + kr) qr = ur(T) F   (ONE scalar eqn!)")))
    s.append(B("Solve qr, substitute back X = SUM ur qr:"))
    s.append(F(formula_text("H(w) = SUM_r  ur ur(T) / (kr - w^2 mr + jw cr)")))
    s.append(P(key("The whole chapter in 4 lines: expand, project, solve "
                   "scalars, recombine. Residues ARE ur ur(T)/mr. "
                   "Memorize THIS derivation, not the formula.")))
    s += [P("PROOF: log-dec formula (peaks one period apart):", h3)]
    s.append(B("x(t) ~ e^(-z wn t) cos(...): peaks at t, t+Td: ratio x1/x2 = "
               "e^(z wn Td), Td = 2pi/wd = 2pi/(wn sqrt(1-z2)). Take ln:"))
    s.append(F(formula_text("d = ln(x1/x2) = 2 pi z / sqrt(1-z^2)  ~=  2 pi z")))
    s.append(B("Over n cycles: d = (1/n) ln(x1/xn+1) (averages noise). "
               "Invert: z = d/sqrt(4pi2+d2)."))
    s += [P("PROOF SKETCH: Q = 1/(2z) from half-power:", h3)]
    s.append(B("|H|2 peak = 1/(2zb)2...: half-power where denom doubles: "
               "(1-b2)2 + (2zb)2 = 2(2z)2 (light z, b~1). Solve: b2 ~ 1 +- "
               "2z -> Db ~ 2z -> Dw = 2z wn. Q = wn/Dw = <b>1/(2z)</b>."))

    # ===== DEEP-9 =====
    s.append(PageBreak())
    s += heading("(Deep 9)", "EX-M capstone + full index")
    s += [P("Pole-zero map of EX-M (every number placed):", h3)]
    s.append(B("Poles (z1 = 2%, z2 = 3%): p1 = <b>-0.124 +- j6.179</b>, p2 = "
               "<b>-0.485 +- j16.173</b> (left-half, stable, ringing)."))
    s.append(B("Zeros of h11 (undamped): <b>+- j10.0</b> (ON the axis: "
               "perfect stillness possible). h12: NO finite zeros (its "
               "numerator never vanishes - cross privilege lost!)."))
    s.append(tbl([
        ["FRF", "Mode 1 residue -> phase", "Mode 2 residue -> phase"],
        ["h11 (drive)", "+0.276 -> -90 deg", "+0.724 -> -90 deg"],
        ["h12 = h21 (cross)", "+0.447 -> -90 deg", "-0.447 -> +90 deg (FLIP!)"],
        ["h22 (drive)", "+0.724 -> -90 deg", "+0.276 -> -90 deg"],
    ], [FRAME_W * 0.26, FRAME_W * 0.37, FRAME_W * 0.37]))
    s.append(P(key("This 3x3 IS the whole rig: poles say WHEN/DECAY, "
                   "residues say WHERE/HOW MUCH, signs say WHICH WAY. "
                   "Everything else is commentary.")))
    s.append(box("Cross-check clinic: FIVE routes, one truth (h11 static):",
                 "(1) Invert K: 100/10000 = <b>0.0100</b>. (2) Residue sum: "
                 "0.00724+0.00276 = <b>0.0100</b>. (3) Zero-formula check: "
                 "(A1w22+A2w12) = 100.0 = w z2 x 1.0: consistent. (4) Low-f "
                 "Bode asymptote -> flexibility line. (5) Quotient bounds "
                 "w1 from above. " + key("When 5 independent paths agree, "
                 "you do not HAVE the answer - you OWN it."),
                 colors.HexColor("#B26A00"), PALE_YELLOW))
    s += [P("Every worked example in this book (34 total):", h3)]
    s.append(tbl([
        ["EX", "Topic", "Lives in"],
        ["A", "Quarter-car suspension (real numbers)", "2.2A"],
        ["B", "Pole drill: three fates", "2.2A"],
        ["C", "Sketch S-planes", "2.2A"],
        ["D", "Amplification table", "2.2A"],
        ["E", "Phase arithmetic", "2.2A"],
        ["F", "Half-power z from 100 Hz peak", "2.2B"],
        ["G", "Ring-down table", "2.2B"],
        ["H", "z-Q-d conversions", "2.2B"],
        ["I", "Same rig, off-resonance FRF", "2.2B"],
        ["J", "Residue from modal mass", "2.2B"],
        ["K", "Nyquist top + hp points", "2.2B"],
        ["L", "Slope detective quiz", "2.2B"],
        ["M0", "D/V/A conversion at 50 Hz", "2.2B"],
        ["M", "2DOF MASTERCLASS (full FRF)", "2.3A"],
        ["N", "2DOF intuition in words", "2.3B"],
        ["P", "Modal forces F=[1,0]", "2.3B"],
        ["Q", "Blade modes to 50 Hz", "2.3C"],
        ["R", "Read the waterfall", "2.3C"],
        ["S", "Blade hit: which modes sing", "2.3C"],
        ["T", "Complex FRF at 3 spots", "Deep-1"],
        ["U", "V-resonance exactly wn", "Deep-1"],
        ["V", "Rayleigh fit (a, b)", "Deep-2"],
        ["X", "Scaling invariance of A", "Deep-2"],
        ["Y", "Residual bookkeeping", "Deep-3"],
        ["Z", "Wandering-pole diagnosis", "Deep-3"],
        ["AA", "Anti-resonance wz = 10", "Deep-4"],
        ["AB", "Synthesis + phase flip", "Deep-4"],
        ["AC", "5 mm release decay", "Deep-4"],
        ["AD", "Modal c from test z", "Deep-5"],
        ["AE", "Bode asymptotes vs exact", "Deep-6"],
        ["AF", "Wait-time from tau", "Deep-6"],
        ["AG", "Isolation design (88%)", "Deep-6"],
        ["AH", "Rayleigh quotient bound", "Deep-7"],
        ["AI", "Absorber design", "Deep-7"],
    ], [FRAME_W * 0.12, FRAME_W * 0.6, FRAME_W * 0.28]))
    s.append(P("(Letters O and W unused: O confuses with 0, W with w. "
               "Notation hygiene!)"))
    s += [P("FAQ round 2 (deep cuts):", h3)]
    for i, (q, a) in enumerate([
        ("Why do drive zeros interlace but cross zeros wander?",
         "Drive numerator is constrained by collocation (force+response same DOF): signs alternate. Cross numerators are free. - shared"),
        ("Can residues be complex?", "With proportional damping: real. General viscous: complex (phase spread). Real A = real modes. - shared"),
        ("Why does Rayleigh overdamp high modes?", "b w/2 term grows unbounded. Fit band edges are trust edges. - Meera"),
        ("Bode vs Nyquist vs FRF: which do I plot first?", "Bode mag (slopes+peaks), then phase (confirm), Nyquist only when fitting circles. - Lena"),
        ("Absorber vs isolation mount: opposite?", "YES: mounts push reso DOWN (avoid); absorbers plant a ZERO on the trouble. - shared"),
        ("One-line Ch.2?", "Poles say when, residues say where, shapes say how - everything else is bookkeeping. - council"),
    ], 1):
        s.append(P(f"<b>Q{i}. {q}</b><br/>A: {a}", body))
    s += [P("Notation decoder (never confuse again):", h3)]
    s.append(tbl([
        ["Symbol", "Means", "Symbol", "Means"],
        ["w / W", "rad/s freq / matrix", "z", "DAMPING RATIO (star!)"],
        ["u / U", "shape vector / modal matrix", "q", "modal coordinate"],
        ["m / M", "modal mass / mass matrix", "H / h", "FRF matrix / one FRF"],
        ["A", "residue (modal strength)", "p / l", "pole / eigenvalue (w2)"],
    ], [FRAME_W * 0.18, FRAME_W * 0.32, FRAME_W * 0.18, FRAME_W * 0.32]))

    # ===== FORMULA BANK =====
    s.append(PageBreak())
    s += heading("(Bank 1)", "Formula bank - tear-out pages")
    s.append(P("SDOF core:", h3))
    for f in ["m x'' + c x' + k x = f(t)",
              "wn = sqrt(k/m),  cc = 2 m wn,  z = c/cc",
              "s = -z wn +- j wd,  wd = wn sqrt(1-z^2)",
              "X/Xst = 1/sqrt((1-b^2)^2+(2zb)^2),  b = w/wn",
              "phase = atan2(2zb, 1-b^2): 0 -> 90 -> 180 deg",
              "z ~ Dw/(2wn),  Q = 1/(2z),  d = ln(x1/x2) ~ 2 pi z",
              "H(s) = 1/(ms^2+cs+k) = A1/(s-p1) + A2/(s-p2)",
              "A1 = 1/(j 2 m wd)  (cover-up)",
              "V/F = jw(D/F),  A/F = -w2(D/F)"]:
        s.append(F(formula_text(f)))
    s.append(P("MDOF core:", h3))
    for f in ["[M]{x''}+[C]{x'}+[K]{x} = {F}",
              "det([K]-L[M]) = 0 -> Lr = wr^2 (eigenvalues)",
              "([K]-wr^2[M]){ur} = 0 (eigenvectors/shapes)",
              "ui(T)[M]uj = mi dij,  ui(T)[K]uj = ki dij",
              "{x} = [U]{p}:  mi p''+ci p'+ki p = fi = ui(T){F}",
              "[H(s)] = adj[B(s)]/det[B(s)]: poles GLOBAL",
              "hij = SUM uir ujr / [mr(wr2-w2+j2zrw rw)]",
              "Aijr = uir ujr / mr (mass-normalized: uir ujr)",
              "Hij = Hji (symmetry -> reciprocity)"]:
        s.append(F(formula_text(f)))
    s += [P("Symbols (nomenclature):", h3)]
    s.append(tbl([
        ["Symbol", "Name", "Unit / note"],
        ["m, c, k / M, C, K", "Mass, damping, stiffness (scalar/matrix)", "kg, Ns/m, N/m"],
        ["wn, wd, fn", "Natural / damped freq", "rad/s, rad/s, Hz (fn = wn/2pi)"],
        ["z, cc, Q, d", "Ratio, critical c, quality, log-dec", "-, Ns/m, -, -"],
        ["s, p1/p2, L", "Laplace var, poles, eigenvalue", "1/s; L = w^2"],
        ["A, Aijr", "Residue (SDOF / MDOF pair)", "Carries shape product"],
        ["U, u, p, f", "Modal matrix, shape, modal resp/force", "x = [U]p"],
        ["H(s), H(jw), hij", "Transfer, FRF, i-j term", "Response/input"],
        ["b", "Frequency ratio w/wn", "Tuning knob of Ch.2"],
    ], [FRAME_W * 0.3, FRAME_W * 0.4, FRAME_W * 0.3]))

    # ===== FAQ =====
    s += heading("(Bank 2)", "Misconceptions FAQ - the council's hit list")
    faqs = [
        ("Is the peak exactly at fn?", "NO (mostly). D/F peaks slightly BELOW wn, V/F EXACTLY at wn, A/F ABOVE. Light z: all ~wn. Say WHICH FRF!"),
        ("Does damping lower the natural frequency?", "wn NEVER moves. wd = wn sqrt(1-z^2) dips slightly. z=0.3 -> wd = 0.95 wn."),
        ("Negative imag peak = broken data?", "NO - residue SIGN = shape polarity (EX-M mode-2 cross terms). All-same-side rule applies ONLY to drive points!"),
        ("ODS = mode shape?", "Only when exciting AT an isolated resonance (then ODS ~ that mode). Elsewhere: a MIX (Ch.1 1.8, now with equations)."),
        ("Can poles differ between FRFs?", "True poles: NEVER (global). Fitted poles wandering = estimator/band trouble - enforce global fits (Ch.5)."),
        ("More modes always better?", "NO - wrong count bends neighbors. Right count + residuals beats mode-soup. (Viktor: 'fitting 6 modes into 3 peaks is astrology.')"),
        ("Is 90-deg phase enough to claim resonance?", "Nearly - plus peak + coherence + repeatability. Phase is the lie detector, not the whole court."),
        ("Why do shapes need scaling?", "Pattern vs LEVEL: [1,1.618] draws right; mass-normalized [0.526,0.851] RESPONDS right. Residues carry scale."),
        ("Zeros = anti-resonances?", "At DRIVE points, FRF zeros sit between poles = valleys. Cross FRFs: zeros wander (no alternation rule)."),
        ("Complex modes - when?", "Non-proportional damping (real joints!) breaks real-mode math. Ch.2 assumes proportional; Ch.5+ handles the wild."),
    ]
    for i, (q, a) in enumerate(faqs, 1):
        s.append(P(f"<b>Q{i}. {q}</b><br/>{a}", body))

    # ===== INTERVIEW =====
    s += heading("(Bank 3)", "Interview rapid-fire (12)")
    ivs = [
        "Poles? Roots of char. eq: damping (real) + freq (imag), conjugate pairs.",
        "Residues? Pole strengths; MDOF: shape-i x shape-j. With poles: full DNA.",
        "Why one row/column? H symmetric (M/C/K symmetric) -> Hij = Hji.",
        "Node reference? ujr = 0 zeroes the mode in the whole row/column.",
        "Half-power? z = Dw/(2wn). Quick, single-mode-only, pros fit instead.",
        "90 degrees? Force-response lag AT resonance; most robust detector.",
        "D vs V vs A? x jw per step; slopes (0,-2)/(+1,-1)/(+2,0).",
        "Global vs local? Poles shared (denominator); residues per pair.",
        "Orthogonality? Shapes decouple M,K -> modal masses/stiffnesses.",
        "m &lt;&lt; n? Keep in-band modes; fold rest into residuals. Industry runs on this.",
        "EMA vs FEM? Test = truth + damping; FEM = what-ifs. Loop them.",
        "Nyquist potato? Overlap, noise/leakage, or nonlinearity. Investigate!",
    ]
    for i, a in enumerate(ivs, 1):
        s.append(Paragraph(f"<b>I{i}.</b> {a}", bullet, bulletText="*"))

    # ===== PROBLEMS =====
    s += heading("(Bank 4)", "Practice problems (8) + answers")
    probs = [
        "m=4, k=9000, c=24. Find fn, z, poles, Q. [A: wn=47.4, fn=7.55Hz, cc=379, z=6.3%, poles -3+j47.3, Q~7.9]",
        "Peak 200 Hz, hp at 198.5/201.5. z? Q? Light/heavy? [A: z=0.75%, Q=67, light - mind leakage!]",
        "Ring-down peaks 5.0, 4.1, 3.36. z? [A: d~ln(5/4.1)=0.198 avg -> z~3.15%]",
        "D/F at 25 Hz = 4e-6 at -160 deg. Give V/F and A/F (mag + phase). [A: w=157: V=6.28e-4 at -70; A=0.0986 at +20]",
        "2x2 rig EX-M: verify k2 = w2^2 m2 numerically. [A: 261.8x1.382=361.8 = u2(T)Ku2. Done in text - redo blind!]",
        "Why does h12 mode-2 imag peak point down in EX-M? [A: A12,2 = -0.447 &lt; 0: shapes oppose (1 x -0.618). Sign, not error.]",
        "Your fit gives f1 = 50.1 Hz from h11 but 51.3 from h22. Verdict? [A: Reject - poles are GLOBAL. Widen band, fix count, refit globally.]",
        "Blade to 50 Hz keeps 3 modes; statics off 8%. Fix? [A: Add residual stiffness (upper) + check lower out-of-band; do NOT add fake modes.]",
    ]
    for i, a in enumerate(probs, 1):
        s.append(Paragraph(f"<b>P{i}.</b> {a}", bullet, bulletText="*"))

    # ===== REVISION =====
    s.append(PageBreak())
    s += heading("(Revision)", "One-page recap")
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
        ["16", "Masterclass receipt", "2DOF statics matched to 4 decimals"],
    ], [FRAME_W * 0.08, FRAME_W * 0.3, FRAME_W * 0.62]))
    s.append(F(formula_text("wn=sqrt(k/m) - s=-zwn+-jwd - z~Dw/2wn - ([K]-w2[M])u=0 - x=[U]p")))

    # ===== SELF-TEST =====
    s.append(PageBreak())
    s += heading("(Self-test)", "12 questions - no peeking!")
    qs = [
        "Pole at -3 +- j40. Give z, wn, wd. Light or heavy?",
        "Why does the resonance peak measure damping and nothing else?",
        "Half-power at 49.5/50.5 Hz, peak 50 Hz. Estimate z and Q.",
        "Real part zero + imaginary peak at some frequency. What is it?",
        "Nyquist looks like a potato. List 3 suspects.",
        "Unlabeled FRF: flat low end, -2 slope high end. Which form? Get V/F?",
        "Why are poles 'global' but residues 'local'?",
        "Reference at a mode's node kills it - prove in one line from hij.",
        "200k-DOF FEM, response to 100 Hz, 12 modes below. How many equations? Rest?",
        "FEM says 88 Hz, test says 82 Hz. One modeling + one test suspect?",
        "D/F peaks below fn but A/F peaks above - contradiction?",
        "Fit gives different f1 per FRF. Accept? Fix?",
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
        "No: D peaks below wn, V at wn, A above (three-peaks nuance). Say which FRF!",
        "Reject: poles are global. Widen band, fix mode count, global refit.",
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
    s += heading("(Glossary)", "Ch.2 definitions XXL")
    glossary = [
        ("Pole", "root of char. equation; -z wn +- j wd; damping + freq."),
        ("Residue", "pole's finite strength; MDOF: shape-i x shape-j."),
        ("Zero", "numerator root; drive-point zeros = anti-resonances."),
        ("S-plane", "real-vs-imag pole map; jw axis hosts FRFs."),
        ("Dynamic amplification", "X/Xstatic vs b; peak ~ 1/(2z) = Q."),
        ("Phase lag", "force->response: 0 -> 90 (reso) -> 180 deg."),
        ("Half-power / log-dec", "freq-/time-domain damping quickies."),
        ("Q factor", "1/(2z); peak gain; sharpness."),
        ("Transfer function H(s)", "response/input in Laplace land; S-plane surface."),
        ("Partial fractions", "H(s) as SUM residue/(s-pole); test-ready form."),
        ("Cover-up", "A = lim (s-p)H(s): residue limit trick."),
        ("Bode / co-quad / Nyquist", "mag-phase / re-im-vs-f / im-vs-re portraits."),
        ("Compliance/mobility/inertance", "D/F, V/F, A/F (+ stiffness/impedance/mass inverses)."),
        ("Stiffness/damping/mass regions", "low-f / reso / high-f FRF rulers."),
        ("Eigenvalue/vector/pair", "w2 / shape / the pair; det([K]-L[M])=0."),
        ("Orthogonality", "shapes decouple M and K; gives modal m, k."),
        ("Modal matrix [U]", "shapes as columns; x=[U]p uncouples."),
        ("Modal force", "u(T)F: how hard input pushes each mode."),
        ("Modal superposition", "solve tiny modal SDOFs, project back, add."),
        ("Mass normalization", "PHI(T)M PHI = 1: scale for correct levels."),
        ("Truncation + residuals", "keep m&lt;&lt;n modes; fold rest quasi-statically."),
        ("System matrix [B(s)]", "s-domain coefficient matrix; symmetric."),
        ("Global vs local", "poles shared; residues per i,j."),
        ("Reciprocity", "Hij = Hji from symmetry."),
        ("Pseudo-orthogonality", "test-vs-FEM shapes check via mass matrix."),
        ("EMA loop", "FEM->predict vs test->extract; same poles/residues."),
    ]
    for term, defn in glossary:
        s.append(P(f"<b>{term}</b> - {defn}", small))
    s.append(Spacer(1, 10))
    s.append(P("Council sign-off: Meera (theory) ok - Viktor (lab) ok - Lena "
               "(signals) ok - Arjun (pedagogy) ok - Sofia (field) ok. "
               "Extended edition: every page earned. Next: Ch.3 signals!",
               center))
    return s


def main() -> None:
    from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
    from reportlab.lib.pagesizes import A4
    from make_handwritten_pdf import PAGE_H as _PH
    doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=ML,
                          rightMargin=MR, topMargin=MT, bottomMargin=MB,
                          title="Ch.2 Handwritten Notes EXTENDED - Modal Testing",
                          author="Modal Notes Council")
    frame = Frame(ML, MB, FRAME_W, _PH - MT - MB, id="main")
    doc.addPageTemplates([PageTemplate(id="pg", frames=[frame], onPage=bg)])
    doc.build(build_story())
    print(f"Wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
