#!/usr/bin/env python3
"""Emits every SVG for the profile README in dark and light, plus the README itself.

Design position: nothing on the page is labelled. No markdown headings, no "$ command"
prompt strips, no counts. Exactly one object has a frame and a colour, the CRT panel
where a snake eats the contribution graph, and everything else is greyscale type printed
straight onto the page. The only "$" is the real one at the top, being typed.

Reads data/contributions.json if present (written by fetch_contributions.py),
otherwise seeded sample data. Run from repo root: python3 scripts/gen.py
"""
import hashlib, json, math, os, random, sys
from functools import lru_cache
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icons import ICONS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://personal-website.miguelpimienta19.workers.dev"
W = 860                 # the one column width everything snaps to
PAD = 28                # the one inner margin
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
GM = "'Geist Mono'," + MONO
CW = 0.6                # Geist Mono advance width, in em
RM = ("@media (prefers-reduced-motion:reduce){*{animation:none!important;opacity:1!important;"
      "transform:none!important;stroke-dashoffset:0!important;clip-path:none!important}}")

# The accent is the phosphor green of the panel, so the cursor, the links and the
# "now" marker all belong to the one coloured thing on the page instead of adding a blue.
THEMES = {
    "dark":  dict(bg="#0d1117", border="#21262d", rule="#21262d", text="#e6edf3", body="#adbac7",
                  mute="#8b949e", label="#636c76", accent="#2fd267", sweep="#86ffb0"),
    "light": dict(bg="#ffffff", border="#d0d7de", rule="#d8dee4", text="#1f2328", body="#40484f",
                  mute="#656d76", label="#8c959f", accent="#1a7f37", sweep="#1a7f37"),
}

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

FONT = open(os.path.join(ROOT, "assets", "geistmono.b64")).read().strip()
FACE = ("@font-face{font-family:'Geist Mono';font-style:normal;font-weight:100 900;"
        "src:url(data:font/woff2;base64," + FONT + ") format('woff2')}")

def svg(w, h, body, label, css="", T=None, face=False):
    """One transparent strip. Nothing on the page draws its own frame except the CRT."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
            f'<style>{FACE if face else ""}text{{font-family:{SANS}}}.m{{font-family:{GM}}}{css}</style>{body}</svg>')

def icon(name, x, y, size, fill):
    return f'<g transform="translate({x},{y}) scale({size/24:.4f})" fill="{fill}"><path d="{ICONS[name]}"/></g>'

FIN = '.row{animation:fin .35s ease-out forwards}@keyframes fin{to{opacity:1}}'
def row(i, inner, step=0.08, start=0.15):
    return f'<g class="row" style="animation-delay:{start+i*step:.2f}s" opacity="0">{inner}</g>'

# ---------- data ----------
def load_days():
    p = os.path.join(ROOT, "data", "contributions.json")
    if os.path.exists(p):
        d = json.load(open(p)); return [(date.fromisoformat(x["date"]), int(x["count"])) for x in d["days"]], True
    random.seed(7); today = date.today(); out = []
    for i in range(371):
        dt = today - timedelta(days=370 - i)
        v = 0 if random.random() > (0.5 if dt.weekday() >= 5 else 0.8) else int(random.expovariate(1/3)) + 1
        if 150 < i < 250: v = int(v * 1.8)
        out.append((dt, v))
    return out, False
DAYS, REAL = load_days()
MX = max(v for _, v in DAYS) or 1
def lvl(v): return 0 if v == 0 else min(4, 1 + int(4 * math.log1p(v) / math.log1p(MX)))

# ---------- 1. the typed line ----------
HEADLINES = ["new grad swe · cs + data science, university of oregon, 2026",
             "swe intern at podium · full-time from february 2027"]
def typing(T):
    H = 40; fs = 15; cw = fs*CW; per = 6.0; n = len(HEADLINES); total = per*n
    steps = max(len(l) for l in HEADLINES) + 2
    b = []
    for i, line in enumerate(HEADLINES):
        w = (2 + len(line))*cw; x = W/2 - w/2
        b.append(f'<clipPath id="t{i}"><rect class="c" style="animation-delay:{i*per:.1f}s;transform-origin:{x:.1f}px 0" x="{x:.1f}" y="0" width="{w+6:.1f}" height="{H}"/></clipPath>')
        b.append(f'<text clip-path="url(#t{i})" class="m h{i}" x="{x:.1f}" y="{H/2+5.5}" font-size="{fs}" xml:space="preserve">'
                 f'<tspan fill="{T["label"]}">$ </tspan><tspan fill="{T["text"]}">{esc(line)}</tspan></text>')
        b.append(f'<rect class="cu" style="animation-delay:{i*per:.1f}s,{i*per:.1f}s" x="{x+w+1:.1f}" y="{H/2-6.3:.1f}" width="{cw*0.8:.1f}" height="{fs*0.92:.1f}" fill="{T["accent"]}"/>')
    a, bb, c = 2.2/total*100, (per-0.8)/total*100, (per-0.15)/total*100
    css = (f'.c{{transform:scaleX(0);transform-box:view-box;animation:ty {total:.1f}s steps({steps},end) infinite}}'
           f'@keyframes ty{{0%{{transform:scaleX(0)}}{a:.2f}%{{transform:scaleX(1)}}{bb:.2f}%{{transform:scaleX(1)}}'
           f'{c:.2f}%{{transform:scaleX(0)}}100%{{transform:scaleX(0)}}}}'
           f'.cu{{visibility:hidden;animation:bl .95s steps(1,end) infinite,cv {total:.1f}s infinite}}'
           f'@keyframes bl{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}'
           f'@keyframes cv{{0%{{visibility:hidden}}{a:.2f}%{{visibility:visible}}{bb:.2f}%{{visibility:hidden}}100%{{visibility:hidden}}}}'
           '@media (prefers-reduced-motion:reduce){.c{animation:none;transform:none}.h1{display:none}.cu{animation:none;visibility:hidden}}')
    return svg(W, H, "".join(b), " / ".join(HEADLINES), css, T=T, face=True)

# ---------- 2. the nameplate ----------
# figlet "Standard", glyphs verbatim from standard.flf ($ is the hardblank), with the
# font's own horizontal smushing (layout 15: rules 1 to 4). The previous build butted
# the raw glyph cells together with no smushing, which is why the name read "M I GUEL":
# figlet never prints it that way.
FIG = {
'A': ["    _    ", "   / \\   ", "  / _ \\  ", " / ___ \\ ", "/_/   \\_\\"],
'E': [" _____ ", "| ____|", "|  _|  ", "| |___ ", "|_____|"],
'G': ["   ____ ", "  / ___|", " | |  _ ", " | |_| |", "  \\____|"],
'I': [" ___ ", "|_ _|", " | | ", " | | ", "|___|"],
'L': [" _     ", "| |    ", "| |    ", "| |___ ", "|_____|"],
'M': [" __  __ ", "|  \\/  |", "| |\\/| |", "| |  | |", "|_|  |_|"],
'N': [" _   _ ", "| \\ | |", "|  \\| |", "| |\\  |", "|_| \\_|"],
'P': [" ____  ", "|  _ \\ ", "| |_) |", "|  __/ ", "|_|    "],
'T': [" _____ ", "|_   _|", "  | |  ", "  | |  ", "  |_|  "],
'U': [" _   _ ", "| | | |", "| | | |", "| |_| |", " \\___/ "],
' ': [" $"]*5}
HIER = "|/\\[]{}()<>"
def smush(a, b):
    if a == " ": return b
    if b == " ": return a
    if "$" in (a, b): return None
    if a == b: return a
    if a == "_" and b in HIER: return b
    if b == "_" and a in HIER: return a
    ca = (HIER.index(a)+1)//2 if a in HIER else -1; cb = (HIER.index(b)+1)//2 if b in HIER else -1
    if ca >= 0 and cb >= 0 and ca != cb: return a if ca > cb else b
    if a + b in ("[]", "][", "{}", "}{", "()", ")("): return "|"
    return None
def figlet(text):
    rows = None
    for ch in text.upper():
        g = FIG[ch]
        if rows is None: rows = list(g); continue
        amt = None
        for L, R in zip(rows, g):
            ts = len(L) - len(L.rstrip(" ")); ls = len(R) - len(R.lstrip(" ")); k = ts + ls
            if ts < len(L) and ls < len(R) and smush(L[len(L)-ts-1], R[ls]) is not None: k += 1
            amt = k if amt is None else min(amt, k)
        out = []
        for L, R in zip(rows, g):
            k = min(amt, len(L), len(R)); ov = ""
            for i in range(k):
                x, y = L[len(L)-k+i], R[i]; m = smush(x, y); ov += m if m is not None else x
            out.append(L[:len(L)-k] + ov + R[k:])
        rows = out
    return [r.replace("$", " ").rstrip() for r in rows]

SWEEP = 9.0      # seconds a pass takes, most of it spent offstage
def nameplate(T):
    """One line of smushed figlet Standard, bold, at terminal size, wiping in left to
    right like a terminal drawing it. No info rows: the typed line above already says
    what he is, and saying it again as key/value pairs was the weakest thing here.

    The letters catch the screen's light. A second copy of every row sits on top in the
    panel's green, masked by a narrow gradient band that travels left to right, so a
    rake crosses the name every nine seconds. On dark it is the panel's brightest
    phosphor, the same lightness as the base fill with a hard hue shift, so it reads as
    light moving over the letters rather than as a highlighter. On white that mint would
    disappear against near-black type, so light uses its own darker green instead. Either
    way the name stops being dead type once its wipe is done, and it is what ties the top
    of the page to the screen under it. Nothing labels it."""
    NAME = figlet("MIGUEL PIMIENTA"); fs = 15.5; lh = fs; x = PAD; y0 = 26
    wide = max(len(r) for r in NAME)*fs*CW
    H = int(y0 + (len(NAME)-1)*lh + 14)
    band = ('<linearGradient id="sw" gradientUnits="objectBoundingBox" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset=".40" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset=".47" stop-color="#fff" stop-opacity=".85"/>'
            '<stop offset=".50" stop-color="#fff" stop-opacity="1"/>'
            '<stop offset=".53" stop-color="#fff" stop-opacity=".85"/>'
            '<stop offset=".60" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#fff" stop-opacity="0"/>'
            f'<animateTransform attributeName="gradientTransform" type="translate" from="-1.5 0" to="1.5 0"'
            f' dur="{SWEEP:.0f}s" repeatCount="indefinite"/></linearGradient>'
            f'<mask id="swm" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#sw)"/></mask>')
    def rows(fill):
        y = y0; out = []
        for r, line in enumerate(NAME):
            out.append(f'<text clip-path="url(#w{r})" x="{x}" y="{y:.1f}" class="m" font-size="{fs}"'
                       f' font-weight="700" fill="{fill}" xml:space="preserve">{esc(line)}</text>')
            y += lh
        return "".join(out)
    clips, y = [], y0
    for r in range(len(NAME)):
        clips.append(f'<clipPath id="w{r}"><rect class="wl" style="animation-delay:{0.1+r*0.07:.2f}s;transform-origin:{x}px 0" '
                     f'x="{x}" y="{y-fs*0.86:.1f}" width="{wide+6:.1f}" height="{lh+2:.1f}"/></clipPath>')
        y += lh
    b = [f'<defs>{"".join(clips)}{band}</defs>', rows(T["text"]),
         f'<g class="sweep" mask="url(#swm)">{rows(T["sweep"])}</g>']
    css = ('.wl{transform:scaleX(0);transform-box:view-box;animation:wipe .34s steps(28,end) forwards}'
           '@keyframes wipe{to{transform:scaleX(1)}}' + RM
           + '@media (prefers-reduced-motion:reduce){.sweep{display:none}}')
    return svg(W, H, "".join(b), "Miguel Pimienta", css, T=T, face=True)

# ---------- 3. contributions: the snake actually eats the graph ----------
# Timing contract, and the bug this replaces:
#   The head reaches the centre of cell i at t0(i) seconds into the lap. A cell's
#   eat animation must therefore run with animation-delay:+t0, so keyframe 0% lands
#   under the head. The previous build used -t0, which puts 0% at LAP-t0: every cell
#   drained at an unrelated moment and the snake read as driving over a grid that
#   happened to be blinking. One sign.
LAP = 32.0          # seconds per lap
BODY_CELLS = 9.0    # body length, measured in cell pitches
K = 14              # body segments
REGROW = 0.30       # lap fractions between the bite and the regrowth

# phosphor palette: the panel is a dark screen in both themes
GREEN = ["#08160e", "#0f5c2c", "#18994a", "#2fd267", "#86ffb0"]
PHOS = dict(bg="#04090b", text="#d9ffe6", body="#7ff2a6", mute="#3aa05f", label="#2f7a49",
            rule="#0d2417", border="#123320", head="#ccffdf", tail="#0c6b32", flash="#ffffff", grid=GREEN)

def _rgb(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))

@lru_cache(maxsize=8)
def geom(y0, cs=11, gap=3):
    """Grid metrics, the boustrophedon path, and the instant the head reaches each cell."""
    pitch = cs + gap
    weeks = [DAYS[i:i+7] for i in range(0, len(DAYS), 7)]; nw = len(weeks)
    x0 = round((W - (nw*pitch - gap))/2)
    cx = lambda w: x0 + w*pitch + cs/2
    cy = lambda d: y0 + d*pitch + cs/2
    # row-major: seven long sweeps with six hairpins. Column-major zigzags read as scribble.
    order = []
    for d in range(7):
        order += [(w, d) for w in (range(nw) if d % 2 == 0 else range(nw-1, -1, -1))]
    idx = {c: i for i, c in enumerate(order)}
    way = [order[0]]
    for i in range(1, len(order)-1):
        (pw, pd), (w, d), (nx, nd) = order[i-1], order[i], order[i+1]
        if (w-pw, d-pd) != (nx-w, nd-d): way.append(order[i])
    way.append(order[-1])
    rr = pitch*0.5
    pt = lambda c: (cx(c[0]), cy(c[1]))
    parts = ["M%.1f,%.1f" % pt(way[0])]; segs = []; prev = pt(way[0])
    for i in range(1, len(way)-1):
        ax, ay = pt(way[i-1]); qx, qy = pt(way[i]); bx, by = pt(way[i+1])
        ux, uy = qx-ax, qy-ay; L = math.hypot(ux, uy); ux, uy = ux/L, uy/L
        vx, vy = bx-qx, by-qy; L = math.hypot(vx, vy); vx, vy = vx/L, vy/L
        a = (round(qx-ux*rr, 1), round(qy-uy*rr, 1)); bpt = (round(qx+vx*rr, 1), round(qy+vy*rr, 1))
        parts += [f"L{a[0]},{a[1]}", f"Q{qx:.1f},{qy:.1f} {bpt[0]},{bpt[1]}"]
        segs += [("L", prev, a), ("Q", a, (qx, qy), bpt)]; prev = bpt
    parts.append("L%.1f,%.1f" % pt(way[-1]))
    segs.append(("L", prev, pt(way[-1])))
    # Exact arc-length parameterisation. animateMotion paces by real distance along the
    # path, so the eat has to be timed against the real length. The old closed form
    # (straight run minus a circular-arc corner allowance) treated the quadratic corners
    # as quarter circles, which they are not: 4.4px short over a lap, a third of a cell
    # of drift by the far end. Sampling costs nothing here and removes it.
    poly = [(segs[0][1][0], segs[0][1][1], 0.0)]; cum = 0.0
    for sg in segs:
        if sg[0] == "L":
            (px, py), (qx, qy) = sg[1], sg[2]
            n = max(1, int(math.hypot(qx-px, qy-py)/0.4))
            pts = [(px+(qx-px)*k/n, py+(qy-py)*k/n) for k in range(1, n+1)]
        else:
            (px, py), (mx, my), (qx, qy) = sg[1], sg[2], sg[3]
            n = 96
            pts = [((1-t)**2*px + 2*(1-t)*t*mx + t*t*qx, (1-t)**2*py + 2*(1-t)*t*my + t*t*qy)
                   for t in (k/n for k in range(1, n+1))]
        for x, y in pts:
            cum += math.hypot(x-poly[-1][0], y-poly[-1][1]); poly.append((x, y, cum))
    total = cum
    # cells come in path order, so a forward window finds each nearest sample cheaply
    t0 = {}; j = 0
    for c in order:
        tx, ty = pt(c); best = None
        for k in range(j, min(j+400, len(poly))):
            x, y, L = poly[k]; dd = (x-tx)**2 + (y-ty)**2
            if best is None or dd < best[0]: best = (dd, L, k)
        t0[c] = best[1]/total*LAP; j = best[2]
    return dict(pitch=pitch, cs=cs, weeks=weeks, nw=nw, x0=x0, y0=y0, cx=cx, cy=cy,
                order=order, idx=idx, path=" ".join(parts), total=total, t0=t0)

def snake_body(G, T, glow=False):
    """K butted dashes chained behind the head, each narrower and further down the
    head-to-tail ramp than the one ahead of it. Round caps overlap the joins, so the
    segments read as one tapered body."""
    PL = 1000.0; B = BODY_CELLS*G["pitch"]/G["total"]*PL; cs = G["cs"]
    hr, hg, hb = _rgb(T["head"]); tr, tg, tb = _rgb(T["tail"])
    def seg(j, mul, op, col=None):
        f = (j + 0.5)/K
        c = col or "#%02x%02x%02x" % (round(hr+(tr-hr)*f), round(hg+(tg-hg)*f), round(hb+(tb-hb)*f))
        sw = cs*(1.02 - 0.66*f)*mul; d = B/K; o0 = (j+1)*d
        return (f'<path class="snk" d="{G["path"]}" pathLength="{PL:.0f}" fill="none" stroke="{c}"'
                f' stroke-width="{sw:.2f}" stroke-linecap="round" stroke-linejoin="round"'
                + (f' opacity="{op}"' if op else "") +
                f' stroke-dasharray="{d:.3f} {PL-d:.3f}" stroke-dashoffset="{o0:.3f}">'
                f'<animate attributeName="stroke-dashoffset" from="{o0:.3f}" to="{o0-PL:.3f}"'
                f' dur="{LAP:.0f}s" repeatCount="indefinite"/></path>')
    b = []
    if glow:   # two fake bloom passes, cheaper and safer than feGaussianBlur over 14 dashes
        for mul, op in ((2.6, "0.08"), (1.7, "0.14")):
            b += [seg(j, mul, op, T["head"]) for j in range(K-1, -1, -1)]
    b += [seg(j, 1.0, None) for j in range(K-1, -1, -1)]
    return "".join(b)

def snake_head(G, T):
    """Eyes ride the path with rotate=auto so the head always faces its direction."""
    return (f'<g class="snk"><animateMotion dur="{LAP:.0f}s" repeatCount="indefinite" rotate="auto"'
            f' path="{G["path"]}"/><circle cx="1.5" cy="-2.5" r="1.25" fill="{T["bg"]}"/>'
            f'<circle cx="1.5" cy="2.5" r="1.25" fill="{T["bg"]}"/></g>')

def halo(G):
    """A soft phosphor bloom riding under the head. A gradient disc on animateMotion:
    no filter, no transform."""
    return (f'<circle class="snk" r="17" fill="url(#halo)"><animateMotion dur="{LAP:.0f}s" repeatCount="indefinite"'
            f' path="{G["path"]}"/></circle>')

def bite_rings(G, T, cells):
    """The bite, drawn ON TOP of the body as an expanding ring so it punches out from
    under the head instead of happening invisibly beneath it. Animates r / stroke-width /
    opacity only: no transform, so nothing depends on transform-box support."""
    b = [f'<circle class="fl" style="animation-delay:{G["t0"][c]:.2f}s" cx="{G["cx"](c[0]):.1f}"'
         f' cy="{G["cy"](c[1]):.1f}" r="5" fill="none" stroke="{T["flash"]}"/>' for c in cells]
    css = (f'.fl{{opacity:0;stroke-width:1.8px;animation:fl {LAP:.0f}s linear infinite}}'
           f'@keyframes fl{{0%{{r:3.5px;opacity:.95;stroke-width:2.2px}}'
           f'0.16%{{opacity:.8}}0.42%{{r:14px;opacity:0;stroke-width:.7px}}'
           f'100%{{r:14px;opacity:0;stroke-width:.7px}}}}')
    return "".join(b), css

def eat_css(T):
    """One keyframe set per level. 0% is the bite, so every cell just phase-shifts into
    its own slot with animation-delay:+t0. Four rules instead of 371.

    A struck cell snaps to the empty colour in about 110ms, while the head is still on
    top of it. A phosphor-persistence version was tried and reverted: decaying down the
    green ramp over 1.6s put an 18-cell band behind the head in colours brighter than most
    of the grid's resting levels, so the wake outshone the snake and there was nothing for
    the eye to lock onto. The dark ribbon IS the legibility. Green ahead of the head, black
    behind it, and the boundary exactly at the head is the whole read; anything that softens
    that boundary costs more than it adds."""
    empty = T["grid"][0]; g0, g1 = REGROW*100, REGROW*100 + 1.4
    out = []
    for L in range(1, 5):
        col = T["grid"][L]
        out.append(f'@keyframes e{L}{{0%{{fill:{T["flash"]}}}0.11%{{fill:{T["flash"]}}}'
                   f'0.34%{{fill:{empty}}}{g0:.1f}%{{fill:{empty}}}'
                   f'{g0+0.3:.1f}%{{fill:{T["flash"]}}}{g1:.1f}%{{fill:{col}}}100%{{fill:{col}}}}}'
                   f'.a{L}{{animation:e{L} {LAP:.0f}s linear infinite}}')
    return "".join(out)

def legend(T, b, fy, pitch, cs):
    lx = W - PAD - 5*pitch - 34
    b.append(f'<text x="{lx-7}" y="{fy}" text-anchor="end" class="m" font-size="9" fill="{T["label"]}">less</text>')
    for i, c in enumerate(T["grid"]):
        b.append(f'<rect x="{lx+i*pitch}" y="{fy-9}" width="{cs}" height="{cs}" rx="2.5" fill="{c}"/>')
    b.append(f'<text x="{lx+5*pitch+2}" y="{fy}" class="m" font-size="9" fill="{T["label"]}">more</text>')

def months(G, T, b):
    seen = set()
    for w, week in enumerate(G["weeks"]):
        dt = week[0][0]
        if dt.month not in seen and dt.day <= 7:
            seen.add(dt.month)
            b.append(f'<text x="{G["x0"]+w*G["pitch"]}" y="{G["y0"]-9}" class="m" font-size="9"'
                     f' fill="{T["label"]}">{dt.strftime("%b").lower()}</text>')

def contrib(T):
    """The contribution graph on a CRT. No heading and no count: the grid shape and the
    month labels already say what it is, and a visitor who works that out for themselves
    is the point. Bigger cells than GitHub's, a glowing snake,
    a bloom under its head, scanlines, one slow roll bar and a vignette. Dark screen in
    both themes: it is the one framed, coloured object on the page."""
    P = dict(PHOS); P["border"] = T["border"]
    G = geom(56, cs=12, gap=3); cs, pitch = G["cs"], G["pitch"]
    H = G["y0"] + 7*pitch + 58
    b = [f'<defs><clipPath id="crt"><rect class="pwr" x="1" y="1" width="{W-2}" height="{H-2}" rx="11"/></clipPath>'
         f'<radialGradient id="halo"><stop offset="0" stop-color="{GREEN[4]}" stop-opacity=".5"/>'
         f'<stop offset="1" stop-color="{GREEN[4]}" stop-opacity="0"/></radialGradient>'
         f'<radialGradient id="vig" cx="50%" cy="50%" r="72%"><stop offset=".55" stop-color="#000" stop-opacity="0"/>'
         f'<stop offset="1" stop-color="#000" stop-opacity=".5"/></radialGradient></defs>',
         f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{P["bg"]}" stroke="{P["border"]}"/>',
         '<g clip-path="url(#crt)">']
    months(G, P, b)
    fed = []
    for w, week in enumerate(G["weeks"]):
        for d, (dt, v) in enumerate(week):
            px, py = G["x0"]+w*pitch, G["y0"]+d*pitch
            L = lvl(v)
            if not v:
                b.append(f'<rect x="{px}" y="{py}" width="{cs}" height="{cs}" rx="2.5" fill="{GREEN[0]}"/>')
                continue
            fed.append((w, d))
            b.append(f'<rect class="a{L}" style="animation-delay:{G["t0"][(w,d)]:.2f}s" x="{px}" y="{py}"'
                     f' width="{cs}" height="{cs}" rx="2.5" fill="{GREEN[L]}"/>')
    tw, td = divmod(len(DAYS)-1, 7)                       # today, the last day in the window
    tx, ty = G["x0"]+tw*pitch, G["y0"]+td*pitch
    b.append(f'<rect x="{tx-1}" y="{ty-1}" width="{cs+2}" height="{cs+2}" rx="3.5" fill="none"'
             f' stroke="{GREEN[4]}" stroke-opacity=".5"/>')
    b.append(halo(G))
    b.append(snake_body(G, P, glow=True))
    rings, rcss = bite_rings(G, P, fed)
    b.append(rings); b.append(snake_head(G, P)); b.append('</g>')
    fy = G["y0"] + 7*pitch + 30
    b.append('<g clip-path="url(#crt)">')
    if not REAL:                      # the one note worth keeping: these are not his numbers yet
        b.append(f'<text x="{PAD}" y="{fy}" class="m" font-size="10" fill="{P["label"]}">'
                 f'sample data until the action runs</text>')
    legend(P, b, fy, pitch, cs)
    b.append('</g>')
    # scanlines, one slow roll bar and a vignette over the whole screen: the three things
    # that say CRT without saying box-drawing TUI
    b.append('<g clip-path="url(#crt)"><g fill="#7ff2a6" opacity="0.055">' +
             "".join(f'<rect x="1" y="{yy}" width="{W-2}" height="1"/>' for yy in range(2, int(H), 3)) +
             f'</g><rect class="roll" x="1" y="0" width="{W-2}" height="34" fill="#86ffb0" opacity="0.035"/>'
             f'<rect x="1" y="1" width="{W-2}" height="{H-2}" fill="url(#vig)"/></g>')
    # CRT power-on: a bright line snaps on at mid height and opens vertically into the
    # screen. A monitor doing this is the whole reference, and nothing on the page says so.
    cy = H/2
    b.append(f'<rect class="pline" x="1" y="{cy-1:.1f}" width="{W-2}" height="2" fill="#eaffef" opacity="0"/>'
             f'<rect class="pwash" x="1" y="1" width="{W-2}" height="{H-2}" rx="11" fill="#86ffb0" opacity="0"/>')
    pwr = (f'@keyframes pwr{{0%{{y:{cy-1:.1f}px;height:2px}}12%{{y:{cy-1:.1f}px;height:2px}}'
           f'58%{{y:1px;height:{H-2}px}}100%{{y:1px;height:{H-2}px}}}}'
           f'.pwr{{animation:pwr .62s cubic-bezier(.16,.84,.26,1) both}}'
           f'@keyframes pline{{0%{{opacity:0}}6%{{opacity:.95}}20%{{opacity:.8}}52%{{opacity:.25}}'
           f'78%{{opacity:0}}100%{{opacity:0}}}}.pline{{animation:pline .62s linear both}}'
           f'@keyframes pwash{{0%{{opacity:.28}}45%{{opacity:.14}}100%{{opacity:0}}}}'
           f'.pwash{{animation:pwash .9s ease-out both}}')
    css = (eat_css(P) + rcss + pwr +
           f'.roll{{animation:roll 7s linear infinite}}@keyframes roll{{from{{transform:translateY(-40px)}}to{{transform:translateY({H+10}px)}}}}' +
           RM + "@media (prefers-reduced-motion:reduce){.snk,.fl,.roll,.pline,.pwash{display:none}.pwr{animation:none}}")
    return svg(W, int(H), "".join(b), "a year of contributions, eaten and regrown by a snake",
               css, T=P, face=True)

# ---------- 6. history, printed like real shell history ----------
STEPS = [("2026", "university of oregon", "b.s. cs + data science"),
         ("2026", "podium", "swe intern, hvac vertical")]
def journey(T):
    fs = 13; rh = 26; y = 20; b = []
    for i, (yr, org, sub) in enumerate(STEPS):
        ry = y + i*rh; now = i == len(STEPS)-1
        b.append(row(i, f'<text x="{PAD}" y="{ry}" class="m" font-size="{fs}" fill="{T["label"]}">{yr}</text>'
                        f'<text x="{PAD+62}" y="{ry}" class="m" font-size="{fs}" fill="{T["text"] if now else T["body"]}" font-weight="{600 if now else 400}">{esc(org)}</text>'
                        f'<text x="{PAD+270}" y="{ry}" class="m" font-size="{fs}" fill="{T["mute"] if now else T["label"]}">{esc(sub)}</text>'))
    ry = y + (len(STEPS)-1)*rh
    # A shell prints its next prompt on the line after the last line of output, so the
    # cursor sits alone at the left margin, not tacked onto the end of a sentence. It also
    # means no position depends on the font's advance width, which this file does not embed.
    cy = ry + rh
    b.append(f'<rect class="cu" x="{PAD}" y="{cy-fs*0.86:.1f}" width="{fs*CW*0.8:.1f}" height="{fs*0.92:.1f}" fill="{T["accent"]}"/>')
    H = int(cy + 6)
    css = ('.cu{animation:bl .95s steps(1,end) infinite}@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:0}}'
           + FIN + RM + '@media (prefers-reduced-motion:reduce){.cu{animation:none;opacity:1}}')
    return svg(W, H, "".join(b), "history. " + " ".join(f"{yr} {org}, {sub}." for yr, org, sub in STEPS), css, T=T)

# ---------- 7. links ----------
LINKS = [("site", "globe", SITE), ("linkedin", "linkedin", "https://linkedin.com/in/miguel-pimienta-bernal"),
         ("github", "github", "https://github.com/MiguelPimienta19"), ("email", "gmail", "mailto:MiguelPimienta19@gmail.com")]
def link(T, text, ic):
    fs = 12; w = int(len(text)*fs*CW + 32); h = 19
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(text)}">'
            f'<style>.m{{font-family:{GM}}}</style>{icon(ic, 3, 3.5, 12, T["label"])}'
            f'<text x="21" y="13.5" class="m" font-size="{fs}" fill="{T["body"]}">{esc(text)}</text></svg>')

# ---------- write ----------
for th in THEMES:
    d = os.path.join(ROOT, "assets", th); os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        if f.endswith(".svg"): os.remove(os.path.join(d, f))
def out(th, name, s): open(os.path.join(ROOT, "assets", th, name), "w").write(s)
count = 0
for th, T in THEMES.items():
    files = {"typing.svg": typing(T), "name.svg": nameplate(T), "contrib.svg": contrib(T), "journey.svg": journey(T)}
    for l, ic, _ in LINKS: files[f"link-{l}.svg"] = link(T, l, ic)
    for name, s in files.items(): out(th, name, s); count += 1
print("wrote", count, "svgs")

def ver(th, name):
    """Content hash, appended to every asset URL. GitHub proxies README images and caches
    them hard, up to a year by default, so a file regenerated daily under the same path can
    keep serving old bytes to visitors long after the workflow ran. Hashing the contents
    means the URL changes exactly when the image does and never otherwise."""
    with open(os.path.join(ROOT, "assets", th, name), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]

def pic(name, alt, width=None, height=None, href=None):
    a = (f' width="{width}"' if width else '') + (f' height="{height}"' if height else '')
    d, l = f"{name}?v={ver('dark', name)}", f"{name}?v={ver('light', name)}"
    p = (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/{d}">'
         f'<source media="(prefers-color-scheme: light)" srcset="assets/light/{l}">'
         f'<img src="assets/dark/{d}" alt="{esc(alt)}"{a}></picture>')
    return f'<a href="{href}">{p}</a>' if href else p
md = ['<div align="center">', '',
      pic("typing.svg", " / ".join(HEADLINES), W), '',
      pic("name.svg", "Miguel Pimienta", W), '',
      pic("contrib.svg", "a year of contributions, eaten and regrown by a snake", W), '',
      pic("journey.svg", "History", W), '',
      " &nbsp;&nbsp; ".join(pic(f"link-{l}.svg", l, height=19, href=u) for l, _, u in LINKS), '',
      '</div>', '']
open(os.path.join(ROOT, "README.md"), "w").write("\n".join(md)); print("wrote README.md")
