import math, sys

W, H = 1920, 1080
CX, CY = W/2, H/2

ARCANE   = "#bd24df"
ARCANE_4 = "#cd55e6"
ARCANE_3 = "#dc85ec"
BLUE     = "#2d6ade"
BLUE_4   = "#5b8ce8"
GOLD     = "#d6a844"
GOLD_3   = "#f4d994"
TEAL     = "#62aeb8"
VOID     = "#07080d"
NIGHT    = "#0b0d14"

def ring(r, sw, stroke, op, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="{stroke}" '
            f'stroke-width="{sw}" opacity="{op}"{d}/>')

def ticks(r_in, r_out, n, stroke, sw, op, phase=0.0):
    out = []
    for i in range(n):
        a = phase + 2*math.pi*i/n
        x1, y1 = CX + r_in*math.cos(a), CY + r_in*math.sin(a)
        x2, y2 = CX + r_out*math.cos(a), CY + r_out*math.sin(a)
        out.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                   f'stroke="{stroke}" stroke-width="{sw}" opacity="{op}" stroke-linecap="round"/>')
    return "".join(out)

def polygram(r, n, step, stroke, sw, op, phase=-math.pi/2):
    pts = [(CX + r*math.cos(phase + 2*math.pi*i/n), CY + r*math.sin(phase + 2*math.pi*i/n)) for i in range(n)]
    order, i = [], 0
    for _ in range(n):
        order.append(pts[i]); i = (i + step) % n
    d = "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in order) + " Z"
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" opacity="{op}" stroke-linejoin="round"/>'

def runes(r, n, stroke, op, seed=7):
    """Small geometric glyphs placed on a ring — deterministic pseudo-random."""
    out = []
    s = seed
    def rnd():
        nonlocal s
        s = (s*1103515245 + 12345) % 2147483648
        return s / 2147483648
    for i in range(n):
        a = 2*math.pi*i/n - math.pi/2
        x, y = CX + r*math.cos(a), CY + r*math.sin(a)
        rot = math.degrees(a) + 90
        k = int(rnd()*5)
        g = ['<path d="M -7 -11 L -7 11 M -7 0 L 7 -8" />',
             '<path d="M 0 -12 L 0 12 M -7 -5 L 7 -12 M -7 5 L 7 -2" />',
             '<path d="M -8 -11 L 0 11 L 8 -11" />',
             '<path d="M -7 -11 L 7 -11 L -7 11 L 7 11" />',
             '<path d="M 0 -12 L 0 12 M -7 -3 L 0 4 L 7 -3" />'][k]
        out.append(f'<g transform="translate({x:.2f},{y:.2f}) rotate({rot:.2f})" '
                   f'stroke="{stroke}" stroke-width="1.6" fill="none" opacity="{op}" '
                   f'stroke-linecap="round">{g}</g>')
    return "".join(out)

def motes(n, seed, color, rmin=0.6, rmax=2.2, op=0.5):
    out, s = [], seed
    def rnd():
        nonlocal s
        s = (s*1103515245 + 12345) % 2147483648
        return s / 2147483648
    for _ in range(n):
        x, y, r = rnd()*W, rnd()*H, rmin + rnd()*(rmax-rmin)
        o = op * (0.25 + rnd()*0.75)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{color}" opacity="{o:.2f}"/>')
    return "".join(out)

DEFS = f'''<defs>
  <radialGradient id="void" cx="50%" cy="46%" r="78%">
    <stop offset="0%" stop-color="#151a2e"/>
    <stop offset="45%" stop-color="{NIGHT}"/>
    <stop offset="100%" stop-color="{VOID}"/>
  </radialGradient>
  <radialGradient id="arcaneGlow" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="{ARCANE}" stop-opacity="0.55"/>
    <stop offset="55%" stop-color="{ARCANE}" stop-opacity="0.14"/>
    <stop offset="100%" stop-color="{ARCANE}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="blueGlow" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="{BLUE}" stop-opacity="0.42"/>
    <stop offset="60%" stop-color="{BLUE}" stop-opacity="0.10"/>
    <stop offset="100%" stop-color="{BLUE}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="sigil" x1="0" y1="1" x2="0" y2="0">
    <stop offset="0%" stop-color="{BLUE}"/>
    <stop offset="50%" stop-color="{ARCANE_4}"/>
    <stop offset="100%" stop-color="{ARCANE}"/>
  </linearGradient>
  <linearGradient id="brand" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#e1b65f"/>
    <stop offset="48%" stop-color="#aa7ade"/>
    <stop offset="100%" stop-color="{TEAL}"/>
  </linearGradient>
  <radialGradient id="vignette" cx="50%" cy="50%" r="72%">
    <stop offset="55%" stop-color="#000000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000000" stop-opacity="0.72"/>
  </radialGradient>
  <filter id="soft" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="9"/>
  </filter>
  <filter id="hairGlow" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="2.4"/>
  </filter>
  <filter id="wide" x="-80%" y="-80%" width="260%" height="260%">
    <feGaussianBlur stdDeviation="34"/>
  </filter>
</defs>'''

def wrap(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}">{DEFS}{body}</svg>')

# ---------------------------------------------------------------- sigil
def sigil():
    core = "".join([
        ring(430, 1.6, "url(#sigil)", 0.85),
        ring(414, 0.8, ARCANE_3, 0.35),
        ring(352, 1.1, "url(#sigil)", 0.5, dash="2 14"),
        ring(300, 1.4, "url(#sigil)", 0.8),
        ring(196, 1.0, BLUE_4, 0.55, dash="26 18"),
        ring(150, 1.6, "url(#sigil)", 0.9),
        ring(64, 1.0, GOLD, 0.55),
        ticks(430, 462, 72, ARCANE_4, 1.2, 0.32),
        ticks(300, 352, 12, "url(#sigil)", 1.4, 0.55),
        ticks(150, 196, 24, BLUE_4, 1.0, 0.35),
        polygram(300, 7, 3, "url(#sigil)", 1.5, 0.75),
        polygram(196, 5, 2, GOLD, 1.2, 0.42),
        polygram(150, 3, 1, ARCANE_3, 1.2, 0.5),
        runes(382, 24, ARCANE_3, 0.55),
        f'<circle cx="{CX}" cy="{CY}" r="8" fill="{GOLD_3}" opacity="0.9"/>',
    ])
    return wrap(
        f'<rect width="{W}" height="{H}" fill="url(#void)"/>'
        f'<g transform="translate({CX} {CY}) scale(2.1) translate({-CX} {-CY})">'
        f'<circle cx="{CX}" cy="{CY}" r="430" fill="url(#arcaneGlow)" opacity="0.5"/></g>'
        f'<circle cx="{CX}" cy="{CY}" r="300" fill="url(#blueGlow)" opacity="0.55"/>'
        + motes(230, 11, ARCANE_3, op=0.45)
        + motes(120, 29, GOLD_3, rmax=1.6, op=0.35)
        + f'<g filter="url(#wide)" opacity="0.55">{core}</g>'
        + f'<g filter="url(#soft)" opacity="0.7">{core}</g>'
        + core
        + f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>'
    )

# ---------------------------------------------------------------- veil
def veil():
    """Minimal portal with flowing curtains; the left half stays workspace-safe."""
    vx, vy = W*0.68, H*0.50
    streams = []
    for i in range(13):
        x = vx - 360 + i*58
        bend = (i - 6) * 16
        streams.append(
            f'<path d="M {x:.1f} -40 C {x-bend:.1f} 260, {x+bend:.1f} 700, {x-bend*0.35:.1f} 1120" '
            f'fill="none" stroke="url(#sigil)" stroke-width="{0.7 + (i%3)*0.35:.2f}" '
            f'opacity="{0.07 + 0.025*(i%4):.3f}"/>')
    horizons = []
    for i in range(7):
        y = 250 + i*105
        w = 420 + (i % 3)*135
        horizons.append(f'<rect x="{vx-w/2:.0f}" y="{y}" width="{w}" height="1" '
                        f'fill="url(#brand)" opacity="{0.035 + 0.018*(i%3):.3f}"/>')
    orb = (f'<circle cx="{CX}" cy="{CY}" r="140" fill="none" stroke="url(#sigil)" stroke-width="1.4" opacity="0.8"/>'
           f'<circle cx="{CX}" cy="{CY}" r="112" fill="none" stroke="{GOLD}" stroke-width="0.9" opacity="0.45" stroke-dasharray="3 12"/>'
           + polygram(140, 6, 2, "url(#sigil)", 1.2, 0.55)
           + ticks(140, 168, 36, ARCANE_4, 1.0, 0.3))
    shifted_orb = f'<g transform="translate({vx-CX:.1f} {vy-CY:.1f})">{orb}</g>'
    return wrap(
        f'<rect width="{W}" height="{H}" fill="url(#void)"/>'
        f'<ellipse cx="{vx}" cy="{vy}" rx="560" ry="760" fill="url(#arcaneGlow)" opacity="0.38"/>'
        f'<circle cx="{W*0.15:.0f}" cy="{H*0.82:.0f}" r="420" fill="url(#blueGlow)" opacity="0.34"/>'
        + motes(170, 5, ARCANE_3, op=0.32)
        + "".join(streams) + "".join(horizons)
        + f'<g filter="url(#soft)" opacity="0.48">{shifted_orb}</g>{shifted_orb}'
        + f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>'
    )

# ---------------------------------------------------------------- rift
def rift():
    """Diagonal fracture with a compact seal, breaking the collection's centered rhythm."""
    rx, ry = W*0.63, H*0.48
    shards = []
    for i in range(34):
        y = -120 + i*42
        x = rx + (y-ry)*0.36
        span = 85 + (i % 7)*31
        shards.append(
            f'<path d="M {x-span:.1f} {y+span*0.18:.1f} L {x-18:.1f} {y:.1f} '
            f'L {x+span:.1f} {y-span*0.24:.1f}" fill="none" stroke="url(#sigil)" '
            f'stroke-width="{0.75 + (i%3)*0.35:.2f}" opacity="{0.11 + 0.035*(i%4):.3f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')
    fissure = (f'<path d="M {rx-350:.1f} -80 L {rx-205:.1f} 245 L {rx-245:.1f} 430 '
               f'L {rx+25:.1f} 620 L {rx-40:.1f} 830 L {rx+220:.1f} 1160" '
               f'fill="none" stroke="url(#sigil)" stroke-width="2.4" opacity="0.72"/>')
    core = (ring(232, 1.5, "url(#sigil)", 0.85)
            + ring(180, 0.9, GOLD, 0.4, dash="4 16")
            + polygram(232, 8, 3, "url(#sigil)", 1.1, 0.5)
            + runes(268, 18, ARCANE_3, 0.4, seed=13)
            + f'<circle cx="{CX}" cy="{CY}" r="6" fill="{GOLD_3}" opacity="0.85"/>')
    shifted_core = f'<g transform="translate({rx-CX:.1f} {ry-CY:.1f}) scale(.78)">{core}</g>'
    return wrap(
        f'<rect width="{W}" height="{H}" fill="url(#void)"/>'
        f'<ellipse cx="{rx}" cy="{ry}" rx="520" ry="720" fill="url(#arcaneGlow)" opacity="0.38"/>'
        f'<circle cx="{W*0.20:.0f}" cy="{H*0.78:.0f}" r="470" fill="url(#blueGlow)" opacity="0.31"/>'
        + motes(190, 41, ARCANE_3, op=0.33)
        + "".join(shards) + fissure
        + f'<g filter="url(#hairGlow)" opacity="0.62">{fissure}{shifted_core}</g>{shifted_core}'
        + f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>'
    )

SCENES = {"sigil": sigil, "veil": veil, "rift": rift}

# ================================================================ extra scenes

def _rng(seed):
    s = seed
    def rnd():
        nonlocal s
        s = (s*1103515245 + 12345) % 2147483648
        return s / 2147483648
    return rnd

# ---------------------------------------------------------------- constellation
def constellation():
    """Arcane star map: nodes + edges, evolution-tree feel. Detail sits high-left."""
    rnd = _rng(97)
    nodes = []
    for i in range(46):
        # cluster loosely around a diagonal band, keep the lower-right calm
        t = rnd()
        x = 140 + t*(W-420) + (rnd()-0.5)*260
        y = 120 + (1-t)*(H-360) + (rnd()-0.5)*300
        nodes.append((max(60, min(W-60, x)), max(60, min(H-60, y)), 2.0 + rnd()*3.4))
    edges = []
    for i, (x1, y1, _) in enumerate(nodes):
        d = sorted(((math.hypot(x1-x2, y1-y2), j) for j, (x2, y2, _) in enumerate(nodes) if j != i))
        for dist, j in d[:2]:
            if dist < 330 and (j, i) not in edges:
                edges.append((i, j))
    ed = "".join(
        f'<line x1="{nodes[a][0]:.1f}" y1="{nodes[a][1]:.1f}" x2="{nodes[b][0]:.1f}" y2="{nodes[b][1]:.1f}" '
        f'stroke="url(#sigil)" stroke-width="0.9" opacity="0.22"/>' for a, b in edges)
    nd = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{ARCANE_3 if i%9 else GOLD_3}" opacity="0.85"/>'
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*3.4:.2f}" fill="{ARCANE_4 if i%9 else GOLD}" opacity="0.13"/>'
        for i, (x, y, r) in enumerate(nodes))
    body = ed + nd
    return wrap(
        f'<rect width="{W}" height="{H}" fill="url(#void)"/>'
        f'<circle cx="{W*0.3:.0f}" cy="{H*0.34:.0f}" r="520" fill="url(#arcaneGlow)" opacity="0.32"/>'
        f'<circle cx="{W*0.74:.0f}" cy="{H*0.72:.0f}" r="460" fill="url(#blueGlow)" opacity="0.30"/>'
        + motes(340, 63, ARCANE_3, op=0.4)
        + f'<g filter="url(#soft)" opacity="0.55">{body}</g>{body}'
        + f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>')

# ---------------------------------------------------------------- ley lines
def leylines():
    """Right-weighted ley-line lattice with one restrained convergence seal."""
    cells, nodes = [], []
    R, i = 96, 0
    dy = R * math.sqrt(3) / 2
    lx, ly = W*0.68, H*0.56
    for row in range(-2, int(H/dy) + 3):
        for col in range(-2, int(W/(1.5*R)) + 3):
            cx = col * 1.5 * R
            cy = row * 2 * dy + (dy if col % 2 else 0)
            d = math.hypot(cx - lx, cy - ly) / math.hypot(CX, CY)
            op = max(0.0, 0.55 * (1 - d*1.05))
            if op <= 0.01:
                continue
            pts = [(cx + R*math.cos(math.pi/3*k), cy + R*math.sin(math.pi/3*k)) for k in range(6)]
            d_attr = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
            cells.append(f'<path d="{d_attr}" fill="none" stroke="url(#sigil)" '
                         f'stroke-width="1.0" opacity="{op:.3f}"/>')
            if ((row*7 + col*13) * 2654435761) % 9 == 0 and op > 0.12:
                nodes.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.4" fill="{GOLD_3}" opacity="0.85"/>'
                             f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="20" fill="{ARCANE_4}" opacity="0.18"/>')
            i += 1
    core = (ring(268, 1.8, "url(#sigil)", 0.9)
            + ring(240, 0.9, GOLD, 0.4, dash="3 15")
            + ring(150, 1.4, "url(#sigil)", 0.7)
            + polygram(268, 6, 2, "url(#sigil)", 1.3, 0.55)
            + polygram(150, 3, 1, ARCANE_3, 1.1, 0.45)
            + ticks(268, 300, 36, ARCANE_4, 1.1, 0.35)
            + runes(320, 18, ARCANE_3, 0.45, seed=17)
            + f'<circle cx="{CX}" cy="{CY}" r="7" fill="{GOLD_3}" opacity="0.9"/>')
    shifted_core = f'<g transform="translate({lx-CX:.1f} {ly-CY:.1f}) scale(.72)">{core}</g>'
    return wrap(
        f'<rect width="{W}" height="{H}" fill="url(#void)"/>'
        f'<ellipse cx="{lx}" cy="{ly}" rx="660" ry="520" fill="url(#arcaneGlow)" opacity="0.18"/>'
        f'<circle cx="{W*0.18:.0f}" cy="{H*0.75:.0f}" r="420" fill="url(#blueGlow)" opacity="0.22"/>'
        + "".join(cells) + "".join(nodes)
        + motes(120, 71, ARCANE_3, op=0.26)
        + f'<g filter="url(#hairGlow)" opacity="0.58">{shifted_core}</g>{shifted_core}'
        + f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>')

# ---------------------------------------------------------------- eclipse
def eclipse():
    """Offset arcane orb with corona; blue counterlight. Left third stays clean."""
    ox, oy, r = W*0.7, H*0.44, 300
    def oring(rr, sw, st, op, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<circle cx="{ox}" cy="{oy}" r="{rr}" fill="none" stroke="{st}" '
                f'stroke-width="{sw}" opacity="{op}"{d}/>')
    corona = []
    for k in range(120):
        a = 2*math.pi*k/120
        l = 26 + (k % 7)*22
        x1, y1 = ox + (r+10)*math.cos(a), oy + (r+10)*math.sin(a)
        x2, y2 = ox + (r+10+l)*math.cos(a), oy + (r+10+l)*math.sin(a)
        corona.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                      f'stroke="url(#sigil)" stroke-width="1" opacity="{0.10 + 0.05*(k%5):.2f}" '
                      f'stroke-linecap="round"/>')
    core = (oring(r, 2.0, "url(#sigil)", 0.9)
            + oring(r-34, 0.9, GOLD, 0.4, dash="2 13")
            + oring(r*0.55, 1.2, ARCANE_3, 0.45)
            + "".join(corona))
    return wrap(
        f'<rect width="{W}" height="{H}" fill="url(#void)"/>'
        f'<g transform="translate({ox} {oy}) scale(2.2) translate({-ox} {-oy})">'
        f'<circle cx="{ox}" cy="{oy}" r="{r}" fill="url(#arcaneGlow)" opacity="0.5"/></g>'
        f'<circle cx="{W*0.18:.0f}" cy="{H*0.8:.0f}" r="480" fill="url(#blueGlow)" opacity="0.42"/>'
        + motes(300, 83, ARCANE_3, op=0.4)
        + f'<circle cx="{ox}" cy="{oy}" r="{r}" fill="{VOID}" opacity="0.92"/>'
        + f'<g filter="url(#wide)" opacity="0.5">{core}</g>'
        + f'<g filter="url(#soft)" opacity="0.6">{core}</g>{core}'
        + f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>')

# ---------------------------------------------------------------- grimoire
def grimoire():
    """Open-grimoire page: ceremonial frame, arcane hairlines, gold tick."""
    y0 = H*0.5
    m = 96
    frame = (f'<rect x="{m}" y="{m}" width="{W-2*m}" height="{H-2*m}" fill="none" '
             f'stroke="url(#sigil)" stroke-width="1.2" opacity="0.45"/>'
             f'<rect x="{m+14}" y="{m+14}" width="{W-2*m-28}" height="{H-2*m-28}" fill="none" '
             f'stroke="{GOLD}" stroke-width="0.7" opacity="0.22"/>')
    corners = "".join(
        f'<g transform="translate({x} {y}) rotate({rot})">'
        f'<path d="M 0 46 L 0 0 L 46 0" fill="none" stroke="url(#brand)" stroke-width="2" opacity="0.75"/>'
        f'<path d="M 0 74 L 0 0 L 74 0" fill="none" stroke="{ARCANE_4}" stroke-width="0.8" opacity="0.3"/>'
        f'</g>'
        for x, y, rot in ((m, m, 0), (W-m, m, 90), (W-m, H-m, 180), (m, H-m, 270)))
    hair = "".join(
        f'<rect x="{(W-w)/2:.0f}" y="{y0 + off:.0f}" width="{w:.0f}" height="1.4" '
        f'fill="url(#brand)" opacity="{op}"/>' for off, w, op in
        ((-230, W*0.56, 0.5), (-196, W*0.44, 0.25), (196, W*0.44, 0.25), (230, W*0.56, 0.5)))
    diam = (f'<g transform="translate({CX} {y0}) rotate(45)">'
            f'<rect x="-34" y="-34" width="68" height="68" fill="none" stroke="url(#brand)" '
            f'stroke-width="2.4" opacity="0.95"/>'
            f'<rect x="-62" y="-62" width="124" height="124" fill="none" stroke="{ARCANE_4}" '
            f'stroke-width="1.1" opacity="0.5"/>'
            f'<rect x="-96" y="-96" width="192" height="192" fill="none" stroke="{GOLD}" '
            f'stroke-width="0.8" opacity="0.28" stroke-dasharray="4 16"/></g>')
    halo = (ring(300, 1.2, "url(#sigil)", 0.35, dash="1 18")
            + ticks(300, 322, 48, ARCANE_4, 1.0, 0.22))
    ornament = "".join(
        f'<circle cx="{CX + s*d}" cy="{y0}" r="{rr}" fill="{c}" opacity="{op}"/>'
        for s in (-1, 1) for d, rr, c, op in ((150, 4.0, GOLD_3, 0.85), (196, 2.6, ARCANE_3, 0.6),
                                              (238, 1.6, TEAL, 0.45)))
    glow = f'<g filter="url(#soft)" opacity="0.75">{diam}{ornament}</g>'
    return wrap(
        f'<rect width="{W}" height="{H}" fill="url(#void)"/>'
        f'<g transform="translate({CX} {y0}) scale(3.0) translate({-CX} {-y0})">'
        f'<circle cx="{CX}" cy="{y0}" r="240" fill="url(#arcaneGlow)" opacity="0.4"/></g>'
        f'<circle cx="{CX}" cy="{y0}" r="600" fill="url(#blueGlow)" opacity="0.3"/>'
        + motes(240, 101, ARCANE_3, op=0.35)
        + frame + corners + halo + hair + glow + diam + ornament
        + f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>')

# ---------------------------------------------------------------- summoning
def summoning():
    """Triquetra of overlapping rune circles — the busiest, most ritual one."""
    r, off = 250, 150
    centers = [(CX, CY - off), (CX - off*0.87, CY + off*0.5), (CX + off*0.87, CY + off*0.5)]
    parts = []
    for k, (x, y) in enumerate(centers):
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" '
                     f'stroke="url(#sigil)" stroke-width="1.5" opacity="0.8"/>')
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r-22}" fill="none" stroke="{GOLD}" '
                     f'stroke-width="0.8" opacity="0.3" stroke-dasharray="3 14"/>')
        for i in range(30):
            a = 2*math.pi*i/30
            x1, y1 = x + (r+6)*math.cos(a), y + (r+6)*math.sin(a)
            x2, y2 = x + (r+22)*math.cos(a), y + (r+22)*math.sin(a)
            parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                         f'stroke="{ARCANE_4}" stroke-width="1" opacity="0.25" stroke-linecap="round"/>')
    outer = (ring(430, 1.4, "url(#sigil)", 0.6)
             + ring(452, 0.8, ARCANE_3, 0.25, dash="1 12")
             + runes(408, 30, ARCANE_3, 0.4, seed=23)
             + ticks(430, 452, 90, ARCANE_4, 1.0, 0.18))
    core = "".join(parts) + outer + f'<circle cx="{CX}" cy="{CY}" r="7" fill="{GOLD_3}" opacity="0.9"/>'
    sx, sy = W*0.67, H*0.52
    shifted_core = f'<g transform="translate({sx-CX:.1f} {sy-CY:.1f}) scale(1.06)">{core}</g>'
    return wrap(
        f'<rect width="{W}" height="{H}" fill="url(#void)"/>'
        f'<ellipse cx="{sx}" cy="{sy}" rx="720" ry="650" fill="url(#arcaneGlow)" opacity="0.38"/>'
        f'<circle cx="{W*0.15:.0f}" cy="{H*0.84:.0f}" r="460" fill="url(#blueGlow)" opacity="0.30"/>'
        + motes(185, 131, ARCANE_3, op=0.32)
        + f'<g filter="url(#soft)" opacity="0.48">{shifted_core}</g>{shifted_core}'
        + f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>')

SCENES.update({"constellation": constellation, "leylines": leylines, "eclipse": eclipse,
               "grimoire": grimoire, "summoning": summoning})

if __name__ == "__main__":
    print(SCENES[sys.argv[1]]())
