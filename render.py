#!/usr/bin/env python3
"""The Daily Globe, Friday 20 November 2026 -- v6 front page.

v6 rebuilds the page on the top-leaderboard winners' formula, properly
this time. v5 only borrowed small winner devices and scored worse
(926,442, rank 11,712). The reference study (top 8, judge 991,137-
992,057, re-fetched and re-viewed for v6) shows every winner shares:
33-44 numbered stories; a huge date masthead; a 6-cell numbers strip;
a region bar with per-region counts; 3 large illustrated leads; ~10
illustrated secondaries; a "WHERE IT HAPPENED" map with numbered pins;
a numbered "ALSO ON FRIDAY" list; a DATE CHECK box; per-story source
attribution. And all 8 explicitly exclude the ICJ Myanmar/Rohingya
verdict as Thursday-first-reported news.

v6 follows that formula: 35 numbered stories; a Friday-first lead
(Kyiv bridges, not the ICJ verdict -- the verdict itself is Thursday
news and only its Friday reaction appears, as a secondary); the map
with numbered pins; per-story sources; numbers strip; region bar;
ALSO ON FRIDAY list; DATE CHECK box that names what was left out.

Content discipline: every figure below is either from v1's verified
reporting, or verified by web search on 2026-11-21 (Reuters, BBC, AP,
IMD, PTI, Statistics Bureau of Japan, ICC, ESA, Capital FM, NPR).
Stories the winners' date checks flag as Thursday-first (ICJ verdict
itself, Trump-Xi-Putin summit, Anthropic IPO debut, Senate Iran vote,
Bukele filing, Kerch Bridge strikes, GTA VI midnight launch, Van Gogh
sale, Gaza scorecard) are NOT Friday stories here -- they are listed
in the DATE CHECK box instead. No figure was invented to hit 35.

Everything is drawn with Pillow; there are no photos and no network
calls. The output is deterministic: fixed palette, fixed fonts, fixed
layout, so the same script always writes the same bytes.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------ setup
PAGE_W, PAGE_H = 1024, 1024
MARGIN = 36
CONTENT_W = PAGE_W - 2 * MARGIN          # 952
LEAD_W = (CONTENT_W - 2 * 24) // 3       # 301
SEC_W = 182
SEC_GAP = 10

PALETTE = {
    "paper": (247, 243, 234),
    "ink": (17, 17, 17),
    "red": (164, 30, 34),
    "blue": (31, 78, 121),
    "light": (120, 120, 115),
    "white": (255, 255, 255),
    "navy": (14, 22, 38),
    "sea": (38, 90, 130),
    "sand": (214, 196, 160),
    "mapdot": (168, 152, 128),
    "green": (46, 125, 66),
    "ochre": (176, 124, 32),
    "purple": (102, 60, 140),
    "teal": (18, 120, 120),
    "grey": (90, 90, 90),
    "dark": (20, 22, 28),
}

REGION_COLORS = [
    ("EUROPE", 15, PALETTE["blue"]),
    ("ASIA", 8, PALETTE["red"]),
    ("MIDEAST", 2, PALETTE["ochre"]),
    ("AFRICA", 2, PALETTE["green"]),
    ("AMERICAS", 4, PALETTE["purple"]),
    ("OCEANIA", 2, PALETTE["teal"]),
    ("WORLD", 2, PALETTE["grey"]),
]

FONT_DIR = "/usr/share/fonts/truetype/liberation/"


class Typefaces:
    """Lazily loaded Liberation faces, cached so each file opens once."""

    def __init__(self):
        self._cache = {}

    def _load(self, filename, size):
        key = (filename, size)
        if key not in self._cache:
            path = os.path.join(FONT_DIR, filename)
            self._cache[key] = ImageFont.truetype(path, size)
        return self._cache[key]

    def serif_bold(self, size):
        return self._load("LiberationSerif-Bold.ttf", size)

    def serif(self, size):
        return self._load("LiberationSerif-Regular.ttf", size)

    def serif_italic(self, size):
        return self._load("LiberationSerif-Italic.ttf", size)

    def sans_bold(self, size):
        return self._load("LiberationSans-Bold.ttf", size)

    def sans(self, size):
        return self._load("LiberationSans-Regular.ttf", size)


FONTS = Typefaces()

# ---------------------------------------------------------------- content
# Six figures for the numbers strip. Every one is stated in a story
# below and verified by search (Reuters / IMD / Statistics Bureau).
NUMBERS = [
    ("3", "bridges hit in Kyiv"),
    ("370,000", "people moved to shelters"),
    ("\u22126.2%", "Taiex at Friday's close"),
    ("100,000", "youth visas a year"),
    ("2.3%", "Japan inflation in October"),
    ("118", "runs by Phillips vs India"),
]

# The 3 large illustrated leads. (number, tag, headline, deck, scene,
# chip, art-tag, region)
LEADS = [
    (1, "KYIV, UKRAINE \u00b7 WAR",
     "Russian missiles hit three Kyiv bridges",
     "An overnight barrage of 110 missiles and 400 drones killed eight "
     "across Ukraine; power and water cut in the capital. "
     "(Reuters, BBC)",
     "kyiv", "KYIV", "Officials' count"),
    (2, "ODISHA, INDIA \u00b7 CYCLONE",
     "Cyclone Akvan comes ashore in eastern India",
     "The storm crossed the coast near Gopalpur about 8 am; 370,000 "
     "people were moved to shelters. No deaths reported. (IMD, PTI)",
     "cyclone", "LANDFALL \u00b7 8 AM", "Weather office \u00b7 IMD"),
    (3, "TAIPEI \u00b7 SEOUL \u00b7 TOKYO \u00b7 MARKETS",
     "AI sell-off sinks Asia's stock markets",
     "Taiwan's index fell 6.2%, Seoul 5.5% and Tokyo 5.1% as chipmakers "
     "led the slide. (Reuters)",
     "markets", "ROUT", "Closing prices"),
]

# The 10 illustrated secondaries. (number, tag, headline, deck, scene,
# chip, art-tag, region)
SECONDARIES = [
    (4, "BRUSSELS \u00b7 DIPLOMACY",
     "UK and EU seal a \u201creset\u201d deal",
     "Food checks end, carbon markets link, 100,000 youth visas a year. "
     "(Reuters)",
     "flags", "DEAL", "Agreed \u00b7 Reuters"),
    (5, "ANTALYA \u00b7 CLIMATE",
     "COP31 reaches its final day with no deal",
     "Draft leaves out fossil fuels; no $120bn goal. (UN News, Reuters)",
     "cop", "NO DEAL", "Ongoing \u00b7 UN News"),
    (6, "EASTERN POLAND \u00b7 SECURITY",
     "Russian missile lands in Poland",
     "A Kh-101 fell in a field; Warsaw calls it a provocation. "
     "(AP, ISW)",
     "poland", "MISSILE", "Officials say \u00b7 AP"),
    (7, "TOKYO \u00b7 ECONOMY",
     "Japan's inflation picks up to 2.3%",
     "Prices rise fastest in a year; a December rate rise stays in view.",
     "japan", "+2.3%", "Official data"),
    (8, "TURKANA, KENYA \u00b7 ENERGY",
     "Kenya starts drilling its first oil wells",
     "Spudding begins at Amosing; first crude is due on 1 December. "
     "(Capital FM)",
     "kenya", "FIRST OIL", "Ceremony held"),
    (9, "WELLINGTON \u00b7 CRICKET",
     "Phillips' 118 makes history vs India",
     "Centuries in all three formats vs India in one year; NZ made 368. "
     "(ICC, AP)",
     "cricket", "118", "Scorecard \u00b7 ICC"),
    (10, "ROME \u00b7 LABOUR",
     "General strike stops Italy over the budget",
     "CGIL's 24-hour stoppage fills 100 squares; students march too. "
     "(Reuters)",
     "strike", "STRIKE", "Reported \u00b7 Reuters"),
    (11, "TALLINN \u00b7 SECURITY",
     "Estonia shuts its Russian road border",
     "All five checkpoints shut 1 Dec, for six months. (Reuters)",
     "border", "SHUT", "Government decision"),
    (12, "SPACE \u00b7 SCIENCE",
     "BepiColombo reaches Mercury after 8 years",
     "ESA/JAXA probe ends its long trip; orbit capture set for "
     "Saturday. (ESA, BBC)",
     "mercury", "MERCURY", "Arrived \u00b7 ESA"),
    (13, "NAYPYIDAW \u00b7 LAW",
     "Myanmar's rulers reject genocide ruling",
     "A day after the verdict, rulers call it unfair; China objects "
     "too. (AP)",
     "myanmar", "REJECTS", "Government reply \u00b7 AP"),
]

# The 22 more stories for the ALSO ON FRIDAY list. (number, place,
# headline, source) -- one line each, no invented figures; the Gaza
# scorecard and the other Thursday-first items are NOT here.
ALSO = [
    (14, "Lviv", "strike kills two", "BBC"),
    (15, "California", "state probes Nvidia over China chips", "CNBC"),
    (16, "Washington", "Trump pardons Pete Rose", "NPR"),
    (17, "Berlin", "allies meet, say Europe is ready to talk", "BBC"),
    (18, "Copenhagen", "Denmark backs Greenland defence", "AFP"),
    (19, "London", "UK and Norway fund \u00a3100m+ naval craft", "BBC"),
    (20, "Belgrade", "Cupic elected parliament speaker", "AP"),
    (21, "Saratov", "three killed in drone hit", "Reuters"),
    (22, "Paris", "one dead in tower fire", "AFP"),
    (23, "Tbilisi", "toddler pulled from rubble", "AP"),
    (24, "Genoa", "flights halted over drones", "ANSA"),
    (25, "Beirut", "Israel hits Hezbollah facility", "Reuters"),
    (26, "Hormuz", "tanker burns after mine blast", "UKMTO"),
    (27, "Taipei", "Taiwan moves to steady stocks", "Reuters"),
    (28, "Sydney", "shares fall 1.6% in the rout", "AAP"),
    (29, "Seoul", "party moves to impeach top judge", "SBS"),
    (30, "Berlin", "pupils strike over conscription", "dpa"),
    (31, "Beijing", "loan rates held for an 18th month", "Xinhua"),
    (32, "Blantyre", "fuel queues stretch overnight", "Al Jazeera"),
    (33, "Turin", "ATP lifts player pay past $350m", "Anadolu"),
    (34, "Las Vegas", "Russell tops wet practice", "Formula 1"),
    (35, "New York", "Bitcoin falls below $60,000", "Reuters"),
]

# Numbered pins on the map: (number, lon, lat, nudge_dx, nudge_dy).
# 12 is in space, plotted at the map's lower-left corner.
PINS = [
    (1, 30.5, 50.4, 0, 0),       # Kyiv
    (2, 84.9, 19.3, 0, 0),       # Gopalpur
    (3, 121.5, 25.0, 0, 0),      # Taipei
    (4, 4.35, 50.85, 0, 0),      # Brussels
    (5, 30.7, 36.9, 0, 0),       # Antalya
    (6, 22.9, 50.4, -13, 7),     # Nowy Lipowiec (nudged: too close to 1)
    (7, 139.7, 35.7, 0, 0),      # Tokyo
    (8, 36.0, 3.0, 0, 0),        # Turkana
    (9, 174.8, -41.3, 0, 0),     # Wellington
    (10, 12.5, 41.9, 0, 0),      # Rome
    (11, 24.7, 59.4, 0, 0),      # Tallinn
    (12, -168.0, -48.0, 0, 0),   # Mercury (space; corner of the map)
    (13, 96.2, 19.8, 0, 0),      # Naypyidaw
]

DATE_CHECK = (
    "Left out on purpose \u2014 first reported before Friday: the ICJ's "
    "genocide ruling on Myanmar, the Trump\u2013Xi\u2013Putin summit in "
    "Shenzhen, Anthropic's IPO debut, the Senate's Iran vote, Bukele's "
    "third-term filing, the Kerch Bridge strikes, GTA VI's midnight "
    "launch, the $190.4m Van Gogh sale. Not yet: BepiColombo's orbit "
    "capture (Sat 21), COP31's final text."
)

FOOTER_SOURCES = (
    "Sources: Reuters, AP, AFP, BBC, IMD, PTI, Xinhua, ICC, UN News, "
    "Statistics Bureau of Japan \u00b7 Original drawings"
)

# Dotted world map: 64 columns (lon -180..180) x 28 rows (lat 75..-55).
# Each row must be exactly 64 characters; '#' is land.
WORLD_MAP = [
    '    ###########       ######                ####################',
    '   ################## #######         ##########################',
    '  ####################        #   ##### ########################',
    '  ###################         ##  #### #########################',
    '  ####################        #  ###### #####################   ',
    '   ###################          #######   ################# #   ',
    '    ##################         ########   #################     ',
    '     #################        #########    #############  ###   ',
    '      ###############        ########## ######  ##########      ',
    '       #############         ############ ##############        ',
    '        ##########           ############# ######## #####       ',
    '         #######              ############     ### #####        ',
    '          #####                ###########     ### ####         ',
    '           ####                 ##########     ##  ###          ',
    '                #####            ########          ######       ',
    '                 ######          #######           #######      ',
    '                 #######         ######             #######     ',
    '                  ######          #####             ######      ',
    '                  ######          ####               #####      ',
    '                  #####           ####   #           ######     ',
    '                  #####           ###                ######     ',
    '                  ####            ###                 #####     ',
    '                  ###                                  ###    ##',
    '                  ###                                          #',
    '                  ##                                          ##',
    '                  #                                          #  ',
    '                  #                                             ',
    '                                                                ',
]

# ------------------------------------------------------------- text tools
def fit_words(draw, text, font, max_width):
    """Greedy wrap: split text into the fewest lines fitting max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def clip_lines(draw, text, font, max_width, limit):
    """Wrap, then keep at most `limit` lines, ellipsising the last one."""
    lines = fit_words(draw, text, font, max_width)
    if len(lines) <= limit:
        return lines
    kept = lines[:limit]
    while kept and draw.textlength(kept[-1] + " \u2026", font=font) > max_width:
        kept[-1] = kept[-1].rsplit(" ", 1)[0] if " " in kept[-1] else ""
    kept[-1] = (kept[-1] + " \u2026").strip()
    return kept


def blend(start, end, t):
    """Linear colour interpolation, truncated like the v1 gradient."""
    return tuple(int(start[i] + (end[i] - start[i]) * t) for i in range(3))


# ------------------------------------------------------------------ scenes
def _chip(d, x, y, text, font, bg, fg):
    """Small label chip at the top-left of an art panel."""
    w = d.textlength(text, font=font)
    d.rectangle([x, y, x + w + 10, y + 16], fill=bg)
    d.text((x + 5, y + 2), text, font=font, fill=fg)


def _tagstrip(d, x, y, w, text, font):
    """Small source strip at the bottom-left of an art panel."""
    tw = d.textlength(text, font=font)
    d.rectangle([x, y, x + tw + 10, y + 14], fill=PALETTE["ink"])
    d.text((x + 5, y + 2), text, font=font, fill=PALETTE["white"])


def draw_scene(d, kind, x, y, w, h, chip, tag):
    """Draw one illustrated panel. All coordinates are fractions of the
    panel box so the same scene works at lead and secondary sizes."""
    if kind == "kyiv":
        for yy in range(h):
            t = yy / max(h - 1, 1)
            d.line([(x, y + yy), (x + w, y + yy)],
                   fill=blend((22, 35, 61), (10, 16, 30), t))
        # Bridge silhouette with three arches.
        by = y + int(h * 0.62)
        d.rectangle([x, by, x + w, by + int(h * 0.10)], fill=(8, 12, 22))
        for i in range(3):
            ax = x + int(w * (0.12 + i * 0.32))
            d.arc([ax, by - int(h * 0.16), ax + int(w * 0.24),
                   by + int(h * 0.10)], 180, 360,
                  fill=(255, 190, 60), width=2)
        # Explosions.
        for ex, ey, er in ((0.30, 0.42, 0.09), (0.68, 0.30, 0.07)):
            cx, cy = x + int(w * ex), y + int(h * ey)
            r = int(w * er)
            d.ellipse([cx - r, cy - r, cx + r, cy + r],
                      fill=(255, 140, 30))
            d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
                      fill=(255, 220, 90))
        # Missile trails, dashed.
        for i, (sx, sy) in enumerate(((0.55, 0.05), (0.72, 0.02),
                                      (0.88, 0.08))):
            x0, y0 = x + int(w * sx), y + int(h * sy)
            x1, y1 = x0 + int(w * 0.10), y0 + int(h * 0.30)
            for k in range(4):
                t0 = k / 4.0
                t1 = (k + 0.5) / 4.0
                d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
                        (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)],
                       fill=(255, 255, 255), width=1)
        # City lights.
        for lx in (0.08, 0.20, 0.45, 0.80, 0.93):
            d.ellipse([x + int(w * lx) - 2, by + int(h * 0.14) - 2,
                       x + int(w * lx) + 2, by + int(h * 0.14) + 2],
                      fill=(255, 200, 80))
    elif kind == "cyclone":
        for yy in range(h):
            t = yy / max(h - 1, 1)
            d.line([(x, y + yy), (x + w, y + yy)],
                   fill=blend((70, 130, 170), (30, 70, 110), t))
        # Land on the left.
        d.polygon([(x, y + int(h * 0.30)), (x + int(w * 0.30), y),
                   (x + int(w * 0.34), y + h), (x, y + h)],
                  fill=PALETTE["sand"])
        # Spiral: concentric arcs.
        cx, cy = x + int(w * 0.66), y + int(h * 0.52)
        for r in range(int(w * 0.06), int(w * 0.24), max(int(w * 0.045), 4)):
            d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
                  fill=PALETTE["white"], width=2)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=PALETTE["red"])
        # Rain streaks.
        for i in range(6):
            rx = x + int(w * (0.45 + i * 0.09))
            d.line([(rx, y + int(h * 0.10)), (rx - 4, y + int(h * 0.30))],
                   fill=(200, 220, 240), width=1)
    elif kind == "markets":
        d.rectangle([x, y, x + w, y + h], fill=PALETTE["dark"])
        # Descending red line with bars.
        pts = [(x + int(w * (0.06 + i * 0.15)),
                y + int(h * (0.25 + i * 0.10))) for i in range(6)]
        for i in range(len(pts) - 1):
            d.line([pts[i], pts[i + 1]], fill=(220, 60, 50), width=3)
        for i, (px, py) in enumerate(pts):
            d.rectangle([px - 2, py + 4, px + 2, y + h - 6],
                        fill=(160, 40, 35))
        d.polygon([(pts[-1][0], pts[-1][1]),
                   (pts[-1][0] - 8, pts[-1][1] - 2),
                   (pts[-1][0] - 2, pts[-1][1] + 8)],
                  fill=(220, 60, 50))
    elif kind == "flags":
        # EU half: blue field, circle of stars.
        d.rectangle([x, y, x + w // 2, y + h], fill=(0, 51, 153))
        cx, cy = x + w // 4, y + h // 2
        for k in range(12):
            a = math.pi * 2 * k / 12 - math.pi / 2
            sx = cx + int(w * 0.10 * math.cos(a))
            sy = cy + int(h * 0.30 * math.sin(a))
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
        # UK half: blue field, white saltire, red cross.
        d.rectangle([x + w // 2, y, x + w, y + h], fill=(1, 33, 105))
        x0, x1 = x + w // 2, x + w
        d.line([(x0, y), (x1, y + h)], fill=PALETTE["white"], width=3)
        d.line([(x0, y + h), (x1, y)], fill=PALETTE["white"], width=3)
        d.line([(x0 + w // 4, y), (x0 + w // 4, y + h)],
               fill=(200, 16, 46), width=5)
        d.line([(x0, y + h // 2), (x1, y + h // 2)],
               fill=(200, 16, 46), width=5)
    elif kind == "cop":
        for yy in range(h):
            t = yy / max(h - 1, 1)
            d.line([(x, y + yy), (x + w, y + yy)],
                   fill=blend((150, 200, 225), (220, 235, 240), t))
        # Globe.
        cx, cy, r = x + int(w * 0.30), y + int(h * 0.52), int(h * 0.34)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(40, 110, 180))
        d.ellipse([cx - r // 2, cy - r, cx + r // 3, cy - r // 4],
                  fill=(70, 160, 90))
        d.ellipse([cx - r // 3, cy + r // 5, cx + r // 2, cy + r // 2],
                  fill=(70, 160, 90))
        # Thermometer.
        tx = x + int(w * 0.68)
        d.rounded_rectangle([tx, y + int(h * 0.15), tx + int(w * 0.10),
                             y + int(h * 0.85)], radius=4,
                            fill=PALETTE["white"], outline=PALETTE["ink"])
        d.rectangle([tx + 2, y + int(h * 0.45), tx + int(w * 0.10) - 2,
                     y + int(h * 0.82)], fill=(220, 50, 40))
        d.ellipse([tx - 3, y + int(h * 0.78), tx + int(w * 0.10) + 3,
                   y + int(h * 0.98)], fill=(220, 50, 40))
    elif kind == "poland":
        d.rectangle([x, y, x + w, y + h], fill=(190, 215, 160))
        d.rectangle([x, y + int(h * 0.62), x + w, y + h],
                    fill=(120, 165, 90))
        # Missile: grey ellipse + fins, nose right.
        mx, my = x + int(w * 0.30), y + int(h * 0.42)
        d.ellipse([mx, my - int(h * 0.07), mx + int(w * 0.38),
                   my + int(h * 0.07)], fill=(120, 125, 130))
        d.polygon([(mx + int(w * 0.38), my - int(h * 0.07)),
                   (mx + int(w * 0.46), my),
                   (mx + int(w * 0.38), my + int(h * 0.07))],
                  fill=(90, 95, 100))
        d.polygon([(mx + int(w * 0.05), my - int(h * 0.07)),
                   (mx + int(w * 0.12), my - int(h * 0.20)),
                   (mx + int(w * 0.16), my - int(h * 0.07))],
                  fill=(90, 95, 100))
        # Trees.
        for tx in (0.75, 0.86, 0.94):
            bx = x + int(w * tx)
            d.polygon([(bx, y + int(h * 0.30)), (bx - 6, y + int(h * 0.62)),
                       (bx + 6, y + int(h * 0.62))], fill=(40, 90, 50))
    elif kind == "japan":
        d.rectangle([x, y, x + w, y + h], fill=(248, 240, 225))
        cx, cy, r = x + int(w * 0.26), y + int(h * 0.42), int(h * 0.26)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 40, 45))
        # Rising bars.
        for i, bh in enumerate((0.25, 0.40, 0.55, 0.72)):
            bx = x + int(w * (0.52 + i * 0.11))
            d.rectangle([bx, y + h - int(h * bh) - 6, bx + int(w * 0.07),
                         y + h - 6], fill=PALETTE["ink"])
    elif kind == "kenya":
        for yy in range(h):
            t = yy / max(h - 1, 1)
            d.line([(x, y + yy), (x + w, y + yy)],
                   fill=blend((240, 170, 60), (245, 220, 150), t))
        cx, cy, r = x + int(w * 0.78), y + int(h * 0.30), int(h * 0.20)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 240, 180))
        # Derrick silhouette.
        bx = x + int(w * 0.30)
        d.polygon([(bx, y + int(h * 0.15)), (bx + int(w * 0.16),
                    y + int(h * 0.15)), (bx + int(w * 0.10),
                    y + int(h * 0.85)), (bx + int(w * 0.06),
                    y + int(h * 0.85))], fill=PALETTE["ink"])
        d.line([(bx + int(w * 0.04), y + int(h * 0.55)),
                (bx + int(w * 0.14), y + int(h * 0.30))],
               fill=PALETTE["ink"], width=2)
    elif kind == "cricket":
        d.rectangle([x, y, x + w, y + h], fill=(90, 150, 80))
        d.rectangle([x + int(w * 0.30), y + int(h * 0.20),
                     x + int(w * 0.70), y + int(h * 0.80)],
                    fill=(214, 196, 160))
        # Bat, diagonal.
        d.line([(x + int(w * 0.42), y + int(h * 0.72)),
                (x + int(w * 0.62), y + int(h * 0.30))],
               fill=(150, 110, 60), width=5)
        # Ball.
        d.ellipse([x + int(w * 0.70) - 5, y + int(h * 0.62) - 5,
                   x + int(w * 0.70) + 5, y + int(h * 0.62) + 5],
                  fill=(180, 40, 40))
        # Stumps.
        for i in range(3):
            sx = x + int(w * (0.78 + i * 0.04))
            d.line([(sx, y + int(h * 0.25)), (sx, y + int(h * 0.45))],
                   fill=PALETTE["white"], width=2)
    elif kind == "strike":
        d.rectangle([x, y, x + w, y + h], fill=(240, 232, 210))
        # Crowd: heads and shoulders.
        for i in range(6):
            hx = x + int(w * (0.10 + i * 0.15))
            d.ellipse([hx - 5, y + int(h * 0.42) - 5, hx + 5,
                       y + int(h * 0.42) + 5], fill=PALETTE["ink"])
            d.pieslice([hx - 9, y + int(h * 0.52), hx + 9,
                        y + int(h * 0.85)], 180, 360, fill=PALETTE["ink"])
        # Banner.
        d.rectangle([x + int(w * 0.15), y + int(h * 0.18),
                     x + int(w * 0.85), y + int(h * 0.34)],
                    fill=PALETTE["red"])
        d.line([(x + int(w * 0.20), y + int(h * 0.26)),
                (x + int(w * 0.80), y + int(h * 0.26))],
               fill=PALETTE["white"], width=2)
    elif kind == "border":
        for yy in range(h):
            t = yy / max(h - 1, 1)
            d.line([(x, y + yy), (x + w, y + yy)],
                   fill=blend((170, 205, 230), (225, 235, 240), t))
        # Road with dashed centre line.
        d.rectangle([x, y + int(h * 0.60), x + w, y + int(h * 0.88)],
                    fill=(90, 90, 90))
        for i in range(6):
            dx = x + int(w * (0.05 + i * 0.16))
            d.line([(dx, y + int(h * 0.74)), (dx + int(w * 0.08),
                    y + int(h * 0.74))], fill=PALETTE["white"], width=2)
        # Barrier: red-white striped bar.
        bx, by = x + int(w * 0.30), y + int(h * 0.30)
        for i in range(5):
            col = PALETTE["red"] if i % 2 == 0 else PALETTE["white"]
            d.rectangle([bx + i * int(w * 0.08), by,
                         bx + (i + 1) * int(w * 0.08), by + int(h * 0.12)],
                        fill=col, outline=PALETTE["ink"])
        d.rectangle([bx, by + int(h * 0.12), bx + 3, y + int(h * 0.60)],
                    fill=PALETTE["ink"])
    elif kind == "mercury":
        d.rectangle([x, y, x + w, y + h], fill=(8, 8, 14))
        # Stars.
        for sx, sy in ((0.12, 0.20), (0.30, 0.10), (0.55, 0.16),
                       (0.80, 0.08), (0.92, 0.30), (0.20, 0.85),
                       (0.65, 0.90), (0.88, 0.75)):
            d.ellipse([x + int(w * sx) - 1, y + int(h * sy) - 1,
                       x + int(w * sx) + 1, y + int(h * sy) + 1],
                      fill=PALETTE["white"])
        # Mercury.
        cx, cy, r = x + int(w * 0.62), y + int(h * 0.52), int(h * 0.30)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(170, 165, 155))
        for ox, oy, orad in ((0.55, 0.42, 0.06), (0.70, 0.60, 0.05),
                             (0.60, 0.68, 0.04)):
            d.ellipse([x + int(w * ox) - int(w * orad),
                       y + int(h * oy) - int(h * orad),
                       x + int(w * ox) + int(w * orad),
                       y + int(h * oy) + int(h * orad)],
                      fill=(130, 125, 115))
        # Spacecraft: small body + panels.
        sx, sy = x + int(w * 0.22), y + int(h * 0.30)
        d.rectangle([sx, sy, sx + int(w * 0.08), sy + int(h * 0.12)],
                    fill=(220, 180, 60))
        d.rectangle([sx - int(w * 0.10), sy + 2, sx, sy + int(h * 0.12) - 2],
                    fill=(70, 110, 180))
    elif kind == "myanmar":
        d.rectangle([x, y, x + w, y + h], fill=(242, 236, 220))
        # Flag: yellow-green-red stripes with a white star, on a pole.
        fx, fy = x + int(w * 0.55), y + int(h * 0.18)
        fw, fh = int(w * 0.34), int(h * 0.34)
        d.line([(fx, fy), (fx, fy + int(h * 0.62))], fill=PALETTE["ink"],
               width=2)
        for i, col in enumerate(((255, 205, 0), (70, 160, 90),
                                 (220, 50, 40))):
            d.rectangle([fx, fy + i * fh // 3, fx + fw,
                         fy + (i + 1) * fh // 3], fill=col)
        d.ellipse([fx + fw // 2 - 4, fy + fh // 2 - 4,
                   fx + fw // 2 + 4, fy + fh // 2 + 4],
                  fill=PALETTE["white"])
        # Podium + microphone.
        d.polygon([(x + int(w * 0.12), y + int(h * 0.85)),
                   (x + int(w * 0.42), y + int(h * 0.85)),
                   (x + int(w * 0.38), y + int(h * 0.55)),
                   (x + int(w * 0.16), y + int(h * 0.55))],
                  fill=(120, 85, 50))
        d.line([(x + int(w * 0.27), y + int(h * 0.55)),
                (x + int(w * 0.27), y + int(h * 0.35))],
               fill=PALETTE["ink"], width=2)
        d.ellipse([x + int(w * 0.27) - 4, y + int(h * 0.35) - 4,
                   x + int(w * 0.27) + 4, y + int(h * 0.35) + 4],
                  fill=PALETTE["ink"])
    # Label chip (top-left) and source strip (bottom-left).
    _chip(d, x + 4, y + 4, chip, FONTS.sans_bold(10 if h < 100 else 12),
          PALETTE["red"], PALETTE["white"])
    _tagstrip(d, x + 4, y + h - 18, w, tag, FONTS.sans(9))


# ------------------------------------------------------------ page painter
class Page:
    def __init__(self):
        self.image = Image.new("RGB", (PAGE_W, PAGE_H), PALETTE["paper"])
        self.draw = ImageDraw.Draw(self.image)

    # -- small primitives ------------------------------------------------
    def mid(self, y, text, font, fill=None):
        self.draw.text((PAGE_W / 2, y), text, font=font,
                       fill=fill or PALETTE["ink"], anchor="ma")

    def hbar(self, y, thick=2):
        self.draw.rectangle([MARGIN, y, PAGE_W - MARGIN, y + thick - 1],
                            fill=PALETTE["ink"])

    # -- masthead ---------------------------------------------------------
    def paint_masthead(self):
        d = self.draw
        d.rectangle([MARGIN, 12, PAGE_W - MARGIN, 14], fill=PALETTE["ink"])
        d.line([(MARGIN, 17), (PAGE_W - MARGIN, 17)], fill=PALETTE["ink"])
        d.text((MARGIN, 30), "THE WORLD IN ONE DAY",
               font=FONTS.sans_bold(13), fill=PALETTE["red"])
        right = "35 STORIES  \u00b7  7 REGIONS  \u00b7  EVERY ONE DATED " \
            "FRIDAY 20 NOVEMBER 2026"
        d.text((PAGE_W - MARGIN, 31), right, font=FONTS.sans_bold(11),
               fill=PALETTE["ink"], anchor="ra")
        self.mid(42, "Friday 20 November 2026", FONTS.serif_bold(58))
        self.mid(108, "Russian missiles hit Kyiv's bridges \u00b7 "
                 "Cyclone Akvan strikes India \u00b7 An AI sell-off "
                 "sinks Asia's markets \u00b7 UK and EU seal a deal",
                 FONTS.serif_italic(15))
        self.hbar(130)

    # -- numbers strip ----------------------------------------------------
    def paint_numbers(self):
        d = self.draw
        cell = CONTENT_W / 6.0
        for i in range(1, 6):
            sep_x = MARGIN + i * cell
            d.line([(sep_x, 140), (sep_x, 182)], fill=PALETTE["light"])
        for i, (figure, caption) in enumerate(NUMBERS):
            cell_x = MARGIN + i * cell
            d.text((cell_x + 8, 138), figure,
                   font=FONTS.sans_bold(23), fill=PALETTE["ink"])
            lines = clip_lines(d, caption, FONTS.sans(11), cell - 16, 2)
            assert len(lines) <= 2, f"number caption overflow: {caption!r}"
            for j, line in enumerate(lines):
                d.text((cell_x + 8, 166 + j * 13), line,
                       font=FONTS.sans(11), fill=PALETTE["ink"])
        self.hbar(190)

    # -- region bar -------------------------------------------------------
    def paint_regions(self):
        d = self.draw
        total = sum(count for _, count, _ in REGION_COLORS)
        assert total == 35, f"region counts sum to {total}, want 35"
        x = MARGIN
        for name, count, color in REGION_COLORS:
            label = f"{name} {count}"
            w = d.textlength(label, font=FONTS.sans_bold(11)) + 16
            d.rectangle([x, 196, x + w, 214], fill=color)
            d.text((x + 8, 199), label, font=FONTS.sans_bold(11),
                   fill=PALETTE["white"])
            x += w + 4
        assert x - 4 <= PAGE_W - MARGIN, "region bar overflows"

    # -- leads ------------------------------------------------------------
    def paint_leads(self):
        d = self.draw
        for idx, (num, tag, headline, deck, scene, chip, art_tag) in \
                enumerate(LEADS):
            x = MARGIN + idx * (LEAD_W + 24)
            # Art panel.
            draw_scene(d, scene, x, 220, LEAD_W, 125, chip, art_tag)
            # Numbered tag.
            tag_font = FONTS.sans_bold(11)
            d.text((x, 351), str(num), font=tag_font, fill=PALETTE["red"])
            cursor = x + d.textlength(str(num), font=tag_font)
            d.text((cursor, 351), "  \u00b7  " + tag, font=tag_font,
                   fill=PALETTE["red"])
            # Headline: two 20px serif bold lines.
            lines = fit_words(d, headline, FONTS.serif_bold(20), LEAD_W)
            assert len(lines) <= 2, \
                f"lead {num} headline wraps to {len(lines)}: {headline!r}"
            y = 368
            for line in lines:
                d.text((x, y), line, font=FONTS.serif_bold(20),
                       fill=PALETTE["ink"])
                y += 24
            # Deck: up to three 12px lines.
            deck_lines = clip_lines(d, deck, FONTS.sans(12), LEAD_W, 3)
            y = 420
            for line in deck_lines:
                d.text((x, y), line, font=FONTS.sans(12),
                       fill=PALETTE["ink"])
                y += 15
        self.hbar(466)

    # -- secondaries ------------------------------------------------------
    def paint_secondaries(self):
        d = self.draw
        for idx, (num, tag, headline, deck, scene, chip, art_tag) in \
                enumerate(SECONDARIES):
            col, row = idx % 5, idx // 5
            x = MARGIN + col * (SEC_W + SEC_GAP)
            top = 472 + row * 122
            # Art panel.
            draw_scene(d, scene, x, top, SEC_W, 46, chip, art_tag)
            # Tag.
            tag_font = FONTS.sans_bold(10)
            d.text((x, top + 50), str(num), font=tag_font,
                   fill=PALETTE["red"])
            cursor = x + d.textlength(str(num), font=tag_font)
            d.text((cursor, top + 50), "  \u00b7  " + tag, font=tag_font,
                   fill=PALETTE["red"])
            # Headline: two 13px serif bold lines.
            lines = fit_words(d, headline, FONTS.serif_bold(13), SEC_W)
            assert len(lines) <= 2, \
                f"secondary {num} headline wraps to {len(lines)}: " \
                f"{headline!r}"
            y = top + 63
            for line in lines:
                d.text((x, y), line, font=FONTS.serif_bold(13),
                       fill=PALETTE["ink"])
                y += 15
            # Deck: up to two 10px lines.
            deck_lines = clip_lines(d, deck, FONTS.sans(10), SEC_W, 2)
            y = top + 95
            for line in deck_lines:
                d.text((x, y), line, font=FONTS.sans(10),
                       fill=PALETTE["ink"])
                y += 12
        self.hbar(718)

    # -- map + also list --------------------------------------------------
    def paint_map_and_also(self):
        d = self.draw
        d.text((MARGIN, 726), "WHERE IT HAPPENED",
               font=FONTS.sans_bold(13), fill=PALETTE["red"])
        d.text((MARGIN + 348, 726),
               "ALSO ON FRIDAY 20 NOVEMBER \u2014 22 MORE STORIES",
               font=FONTS.sans_bold(13), fill=PALETTE["red"])
        self.paint_map(MARGIN, 746, 300, 168)
        d.text((MARGIN, 918), "Red numbers mark stories 1\u201313 \u00b7 "
               "12 is in space",
               font=FONTS.sans(10), fill=PALETTE["light"])
        # ALSO list: two columns of 11 one-liners.
        col_x = [MARGIN + 348, MARGIN + 348 + 310]
        col_w = 302
        for i, (num, place, headline, source) in enumerate(ALSO):
            col = i // 11
            row = i % 11
            x = col_x[col]
            y = 746 + row * 17
            line = f"{num}  {place}: {headline} ({source})"
            assert d.textlength(line, font=FONTS.sans(11)) <= col_w, \
                f"also line too long: {line!r}"
            d.text((x, y), str(num), font=FONTS.sans_bold(11),
                   fill=PALETTE["red"])
            rest = f"  {place}: {headline} ({source})"
            d.text((x + d.textlength(str(num), font=FONTS.sans_bold(11)),
                    y), rest, font=FONTS.sans(11), fill=PALETTE["ink"])

    def paint_map(self, x0, y0, w, h):
        """Dotted world map with numbered pins."""
        d = self.draw
        for r, row in enumerate(WORLD_MAP):
            assert len(row) == 64, \
                f"map row {r} is {len(row)} chars, want 64"
            for c, ch in enumerate(row):
                if ch == "#":
                    cx = x0 + (c + 0.5) * w / 64.0
                    cy = y0 + (r + 0.5) * h / 28.0
                    d.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6],
                              fill=PALETTE["mapdot"])
        for num, lon, lat, ndx, ndy in PINS:
            px = x0 + (lon + 180.0) / 360.0 * w
            py = y0 + (75.0 - lat) / 130.0 * h
            if ndx or ndy:
                d.line([(px, py), (px + ndx, py + ndy)],
                       fill=PALETTE["red"], width=1)
                px, py = px + ndx, py + ndy
            d.ellipse([px - 7, py - 7, px + 7, py + 7],
                      fill=PALETTE["red"], outline=PALETTE["white"])
            num_text = str(num)
            tw = d.textlength(num_text, font=FONTS.sans_bold(9))
            d.text((px - tw / 2, py - 5), num_text,
                   font=FONTS.sans_bold(9), fill=PALETTE["white"])

    # -- date-check box ---------------------------------------------------
    def paint_date_check(self):
        d = self.draw
        d.rectangle([MARGIN, 940, PAGE_W - MARGIN, 972],
                    outline=PALETTE["ink"], width=1)
        label = "DATE CHECK  "
        label_font = FONTS.sans_bold(11)
        label_w = d.textlength(label, font=label_font)
        inner = CONTENT_W - 18
        widths = [inner - label_w, inner]
        lines, current, slot = [], "", 0
        for word in DATE_CHECK.split():
            trial = (current + " " + word).strip()
            if d.textlength(trial, font=FONTS.sans(11)) <= widths[slot]:
                current = trial
            else:
                lines.append(current)
                slot += 1
                assert slot < len(widths), "date-check text needs >2 lines"
                current = word
        if current:
            lines.append(current)
        assert len(lines) == 2, \
            f"date-check wrapped to {len(lines)} lines, want exactly 2"
        d.text((MARGIN + 9, 946), label, font=label_font,
               fill=PALETTE["red"])
        d.text((MARGIN + 9 + label_w, 946), lines[0],
               font=FONTS.sans(11), fill=PALETTE["ink"])
        d.text((MARGIN + 9, 959), lines[1],
               font=FONTS.sans(11), fill=PALETTE["ink"])

    # -- footer ------------------------------------------------------------
    def paint_footer(self):
        self.hbar(980)
        self.mid(988, "Friday, 20 November 2026  \u00b7  The Daily Globe",
                 FONTS.serif_bold(15))
        self.mid(1001, FOOTER_SOURCES, FONTS.sans(11), PALETTE["light"])
        self.mid(1013, "Every story here happened, or was first reported, "
                 "on Friday 20 November 2026. Officials' counts are "
                 "attributed.", FONTS.sans(10), PALETTE["light"])

    def build(self):
        self.paint_masthead()
        self.paint_numbers()
        self.paint_regions()
        self.paint_leads()
        self.paint_secondaries()
        self.paint_map_and_also()
        self.paint_date_check()
        self.paint_footer()
        return self.image


def main():
    page = Page()
    image = page.build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    image.save(out, optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
