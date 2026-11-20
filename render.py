#!/usr/bin/env python3
"""Render 'The Daily Globe - 20 November 2026', v4.

v4 goes back to the v1 formula that scored 972,121: 25 stories, a roomy
50px brief pitch, a 66px masthead and a 92px lead-art band. The single
visual upgrade kept from v3 is its richer courthouse scene, redrawn
inside the same 92px band, so it costs no density at all. No stories
were added, no type was shrunk, no figures were invented: every headline
and number below comes from the verified 20 November 2026 reporting
already used by v1/v2/v3.

Drawn with Pillow only. Deterministic: same input, same bytes out.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952
GAP = 12            # air between sections
GRID_PITCH = 51     # brief row pitch (v1 used 50)

INK = (26, 26, 26)
NAVY = (27, 42, 74)
CRIMSON = (179, 38, 30)
GREY = (110, 110, 110)
RULE = (180, 180, 180)
PAPER = (253, 252, 247)
GOLD = (201, 162, 39)
SKY_TOP = (29, 44, 78)
SKY_MID = (126, 143, 181)
SKY_BOT = (220, 217, 234)
STONE = (240, 234, 216)
STONE_DARK = (213, 205, 180)
FLUTE = (200, 192, 166)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(size):
    return font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return font("DejaVuSerif.ttf", size)


def sans_b(size):
    return font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def wrap(text, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if f.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ---------------------------------------------------------------- content
# All stories and figures verified against 20 November 2026 reporting
# (same set v1 used, plus nothing new).

LEAD_HEAD = ["World court rules Myanmar", "committed genocide"]
LEAD_SUMMARY = (
    "The International Court of Justice finds the state responsible for "
    "the 2017 Rohingya campaign in a 9\u20136 vote \u2014 its first genocide "
    "finding against a state. Refugees in Bangladesh cheer."
)
CHIP_LEFT = "9\u20136 VOTE \u2022 FIRST OF ITS KIND"
CHIP_RIGHT = "GAMBIA v. MYANMAR"

TIMELINE = [
    "Houthi missile hits Riyadh \u2022 Kyiv struck by four missiles \u2022 S&P 500 falls 2.0%",
    "Senate rejects Iran war powers 51\u201348 \u2022 Anthropic closes up 17% \u2022 Cyclone Akvan lands",
]

# 24 briefs, 3 columns x 8 rows. Headlines kept short enough for one
# 16px bold line in a 301px column; summaries fit two 13px lines.
BRIEFS = [
    ("Trump, Xi, Putin declare peace",
     "The three leaders issue a joint declaration after summit talks."),
    ("Anthropic soars 17% on debut",
     "Shares close near $97 after an $81.3bn IPO, the year's biggest listing."),
    ("Houthi missile hits Riyadh",
     "A missile fired from Yemen strikes a tower in the Saudi capital."),
    ("Europe ready for Russia talks",
     "Leaders in Berlin say they are prepared to open talks with Moscow."),
    ("California probes Nvidia chips",
     "The state investigates Nvidia over chips reaching China despite controls."),
    ("Crimean Bridge hit again",
     "The bridge linking Russia to Crimea is struck again, halting traffic."),
    ("S&P 500 falls 2.0% again",
     "The index notches a fifth straight loss as the sell-off deepens."),
    ("Cyclone Akvan hits Odisha",
     "The storm makes landfall on India's east coast, flooding coastal districts."),
    ("Kyiv hit by four missiles",
     "Ballistic missiles strike the Ukrainian capital overnight."),
    ("Tanker burns after Hormuz mine",
     "A tanker catches fire in the Strait of Hormuz after striking a mine."),
    ("Senate rejects Iran war powers",
     "The Senate votes 51\u201348 against curbing the president's war powers."),
    ("Trump pardons Pete Rose",
     "The late baseball star receives a posthumous pardon."),
    ("Gaza plan scores 4 out of 26",
     "An assessment finds the Gaza plan meets only four of 26 benchmarks."),
    ("Genoa halts flights over drones",
     "Drone sightings shut the airport as flights are suspended."),
    ("Israel hits Hezbollah facility",
     "An Israeli strike targets a Hezbollah facility in southern Lebanon."),
    ("Fiona the hippo dies",
     "The Cincinnati Zoo hippo dies, mourned by fans worldwide."),
    ("APEC adopts Shenzhen Outlook",
     "Asia-Pacific leaders endorse a new economic outlook in Shenzhen."),
    ("UK, Norway fund Ukraine craft",
     "London and Oslo pledge over \u00a3100m for Ukrainian naval vessels."),
    ("Denmark backs Greenland",
     "Parliament votes 109\u20130 to strengthen the defence of Greenland."),
    ("Taiwan moves to steady stocks",
     "Taipei acts to calm markets after a sharp sell-off."),
    ("Serbia elects speaker Cupic",
     "Cupic wins the speakership with 140 votes in parliament."),
    ("Three killed in Saratov strike",
     "A drone hit kills three in the Russian city of Saratov."),
    ("One dead in France tower fire",
     "A fire in a French tower block claims one life."),
    ("Toddler saved in Tbilisi rubble",
     "Rescuers pull a toddler alive from a collapsed building."),
]

MARKETS = (
    "MARKETS  \u2014  S&P 500 \u22122.0% (5th straight loss)  \u2022  "
    "Anthropic +17% (~$97)  \u2022  Oil flat as Hormuz offsets oversupply"
)
FOOTER = (
    "Friday, 20 November 2026  \u2022  The Daily Globe  \u2022  "
    "Sources: BBC, The Hindu, One Turn, AppiSToS"
)


# ---------------------------------------------------------------- drawing
class FrontPage:
    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.warnings = []

    def rule(self, y, x0=MARGIN, x1=W - MARGIN, width=1, fill=RULE):
        self.d.line([(x0, y), (x1, y)], fill=fill, width=width)

    def centred(self, y, text, f, fill=INK):
        w = f.getlength(text)
        self.d.text(((W - w) / 2, y), text, font=f, fill=fill)

    # -- sections ------------------------------------------------------
    def masthead(self, y):
        self.rule(y)
        f = serif_b(66)
        w = f.getlength("THE DAILY GLOBE")
        self.d.text(((W - w) / 2, y + 8), "THE DAILY GLOBE", font=f, fill=INK)
        y += 8 + 66 + 10
        self.centred(y, "FRIDAY, 20 NOVEMBER 2026  \u2022  25 STORIES  \u2022  5 REGIONS",
                     sans_b(13), fill=NAVY)
        y += 13 + 10
        self.rule(y, width=2, fill=INK)
        return y + 2

    def lead(self, y):
        f = serif_b(40)
        for line in LEAD_HEAD:
            self.centred(y, line, f)
            y += 46
        y += 4
        f2 = serif(15)
        for line in wrap(LEAD_SUMMARY, f2, CW):
            self.centred(y, line, f2)
            y += 19
        return y

    def artwork(self, y):
        """Courthouse scene (v3's treatment) inside v1's 92px band."""
        y0, y1 = y, y + 92
        # dusk-sky gradient, two segments
        for i in range(92):
            t = i / 91.0
            if t < 0.5:
                col = lerp(SKY_TOP, SKY_MID, t / 0.5)
            else:
                col = lerp(SKY_MID, SKY_BOT, (t - 0.5) / 0.5)
            self.d.line([(MARGIN, y0 + i), (W - MARGIN, y0 + i)], fill=col)
        cx = W // 2
        # pediment: shallow triangle with gold outline, white scales medallion
        self.d.polygon([(cx, y0 + 8), (cx + 170, y0 + 34), (cx - 170, y0 + 34)],
                       fill=(38, 53, 92), outline=GOLD, width=2)
        self.d.ellipse([cx - 10, y0 + 15, cx + 10, y0 + 35], fill=(255, 255, 255))
        # tiny scales glyph inside the medallion
        self.d.line([(cx, y0 + 19), (cx, y0 + 31)], fill=NAVY, width=1)
        self.d.line([(cx - 7, y0 + 21), (cx + 7, y0 + 21)], fill=NAVY, width=1)
        self.d.polygon([(cx - 9, y0 + 27), (cx - 5, y0 + 27), (cx - 7, y0 + 31)], fill=NAVY)
        self.d.polygon([(cx + 5, y0 + 27), (cx + 9, y0 + 27), (cx + 7, y0 + 31)], fill=NAVY)
        # entablature
        self.d.rectangle([cx - 162, y0 + 34, cx + 162, y0 + 42], fill=STONE)
        # four fluted columns with capitals and bases
        for ccx in (cx - 120, cx - 40, cx + 40, cx + 120):
            self.d.rectangle([ccx - 15, y0 + 42, ccx + 15, y0 + 46], fill=STONE_DARK)
            self.d.rectangle([ccx - 12, y0 + 46, ccx + 12, y0 + 74], fill=(240, 234, 216))
            for fx in (-5, 0, 5):
                self.d.line([(ccx + fx, y0 + 48), (ccx + fx, y0 + 72)], fill=FLUTE, width=1)
            self.d.rectangle([ccx - 15, y0 + 74, ccx + 15, y0 + 78], fill=STONE_DARK)
        # three-step base
        self.d.rectangle([cx - 182, y0 + 78, cx + 182, y0 + 82], fill=STONE_DARK)
        self.d.rectangle([cx - 190, y0 + 82, cx + 190, y0 + 87], fill=(203, 195, 170))
        self.d.rectangle([cx - 198, y0 + 87, cx + 198, y0 + 92], fill=(193, 185, 160))
        # crimson flags just outside the courthouse
        for px, direction in ((cx - 212, -1), (cx + 212, 1)):
            self.d.rectangle([px - 1, y0 + 10, px + 1, y0 + 88], fill=(58, 58, 58))
            self.d.polygon([(px, y0 + 10), (px, y0 + 24), (px + 24 * direction, y0 + 17)],
                           fill=CRIMSON)
        # caption chips at the bottom corners of the band
        self.chip(MARGIN + 8, y1 - 28, CHIP_LEFT, CRIMSON)
        self.chip(W - MARGIN - 8, y1 - 28, CHIP_RIGHT, NAVY, right=True)
        return y1

    def chip(self, x, y, text, bg, right=False):
        f = sans_b(11)
        tw = f.getlength(text)
        w = int(tw) + 18
        if right:
            x = x - w
        self.d.rounded_rectangle([x, y, x + w, y + 20], radius=3, fill=bg,
                                 outline=(255, 255, 255) if bg == NAVY else None,
                                 width=1 if bg == NAVY else 0)
        self.d.text((x + 9, y + 4), text, font=f, fill=(255, 255, 255))

    def timeline(self, y):
        self.d.text((MARGIN, y), "THE DAY IN BRIEF", font=sans_b(11), fill=GREY)
        y += 18
        f = sans(13)
        for line in TIMELINE:
            self.d.text((MARGIN, y), line, font=f, fill=INK)
            y += 17
        return y

    def section_head(self, y, text):
        self.d.text((MARGIN, y), text, font=sans_b(15), fill=NAVY)
        y += 22
        self.rule(y)
        return y + 1

    def brief_grid(self, y):
        col_w = (CW - 2 * 24) // 3  # 301
        xs = [MARGIN, MARGIN + col_w + 24, MARGIN + 2 * (col_w + 24)]
        fh, fs = sans_b(16), sans(13)
        for row in range(8):
            for col in range(3):
                idx = row * 3 + col
                head, summ = BRIEFS[idx]
                x = xs[col]
                hl = wrap(head, fh, col_w)
                sl = wrap(summ, fs, col_w)
                if len(hl) > 1 or len(sl) > 2:
                    self.warnings.append(
                        f"brief {idx + 1} overflow: {len(hl)} headline lines, "
                        f"{len(sl)} summary lines")
                yy = y + row * GRID_PITCH
                for i, line in enumerate(hl[:2]):
                    self.d.text((x, yy + i * 19), line, font=fh, fill=INK)
                sy = yy + len(hl[:2]) * 19 + 1
                for i, line in enumerate(sl[:2]):
                    self.d.text((x, sy + i * 15), line, font=fs, fill=(60, 60, 60))
        return y + 8 * GRID_PITCH

    def markets(self, y):
        self.rule(y)
        y += 8
        f = sans(13)
        self.d.text((MARGIN, y), MARKETS, font=f, fill=INK)
        return y + 17

    def footer(self, y):
        self.rule(y)
        y += 8
        self.centred(y, FOOTER, sans(12), fill=GREY)
        return y + 14

    def render(self):
        y = 22
        y = self.masthead(y)
        y += GAP
        y = self.lead(y)
        y += GAP
        y = self.artwork(y)
        y += GAP
        y = self.timeline(y)
        y += GAP
        y = self.section_head(y, "AROUND THE WORLD")
        y += GAP
        y = self.brief_grid(y)
        y += GAP
        y = self.markets(y)
        y += GAP
        y = self.footer(y)
        return y


def main():
    page = FrontPage()
    bottom = page.render()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    page.img.save(out)
    print("bottom y:", bottom, "of", H, "| slack:", H - bottom)
    for w in page.warnings:
        print("WARNING:", w)
    print("wrote", out)


if __name__ == "__main__":
    main()
