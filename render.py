#!/usr/bin/env python3
"""The Daily Globe, Friday 20 November 2026 -- v5 front page.

v5 returns to the v1 page that scored 972,121 and keeps its whole
formula: 25 stories, the roomy 50px brief pitch, the 66px masthead,
and the ICJ genocide-verdict lead with its courthouse band. On top of
that base it borrows four small devices the current top entries all
share -- a six-cell numbers strip, per-region story counts in the
briefs header, numbered brief tags, and a date-check box -- without
reflowing anything else. No story was added, no type was shrunk, and
every figure below is lifted straight from v1's verified reporting.

Everything is drawn with Pillow; there are no photos and no network
calls. The output is deterministic: fixed palette, fixed fonts, fixed
layout, so the same script always writes the same bytes.
"""

import os
from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------ setup
PAGE_W, PAGE_H = 1024, 1024
MARGIN = 36
CONTENT_W = PAGE_W - 2 * MARGIN          # 952
COLUMN_W = (CONTENT_W - 2 * 24) // 3     # 301
GRID_TOP = 546
ROW_PITCH = 50

PALETTE = {
    "paper": (247, 243, 234),
    "ink": (17, 17, 17),
    "red": (164, 30, 34),
    "blue": (31, 78, 121),
    "light": (120, 120, 115),
    "navy_dark": (24, 60, 96),
    "sky_top": (232, 222, 205),
    "sky_bottom": (208, 202, 235),
    "white": (255, 255, 255),
}

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

    def sans_bold(self, size):
        return self._load("LiberationSans-Bold.ttf", size)

    def sans(self, size):
        return self._load("LiberationSans-Regular.ttf", size)


FONTS = Typefaces()

# ---------------------------------------------------------------- content
LEAD_KICKER = "THE HAGUE \u2014 WORLD COURT"
LEAD_LINES = ["World court rules Myanmar", "committed genocide"]
LEAD_DECK = (
    "ICJ finds the state responsible for the 2017 Rohingya campaign in a "
    "9\u20136 vote \u2014 its first genocide finding against a state; "
    "refugees in Bangladesh cheer."
)
LEAD_CHIP = "9\u20136 VOTE  \u2022  FIRST OF ITS KIND"

# Six figures for the numbers strip. Each one is already stated
# somewhere in v1's page (lead, briefs, or markets line); the strip
# only gathers them in one place.
NUMBERS = [
    ("9\u20136", "ICJ vote \u2014 first of its kind"),
    ("4", "ballistic missiles hit Kyiv"),
    ("\u22122.0%", "S&P 500 at Friday's close"),
    ("+17%", "Anthropic on debut"),
    ("51\u201348", "Senate rejects Iran war powers"),
    ("109\u20130", "Denmark backs Greenland defence"),
]

REGION_COUNTS = "EUROPE 10 \u2022 ASIA 4 \u2022 MIDEAST 4 \u2022 AMERICAS 3 \u2022 WORLD 3"

# The 24 briefs, in v1's order and wording. Region tallies check out:
# EUROPE 10, ASIA 4, MIDEAST 4, AMERICAS 3, WORLD 3 = 24.
BRIEFS = [
    ("POLITICS", "WORLD", "Trump, Xi, Putin issue peace plan",
     "Four-point declaration after first trilateral summit."),
    ("TECH", "WORLD", "Anthropic closes up 17% on debut",
     "Shares end near $97 after record $81.3bn IPO."),
    ("WAR", "MIDEAST", "Houthi missile hits Riyadh tower",
     "Houthis claim strikes on four Saudi targets."),
    ("POLITICS", "EUROPE", "Europe ready for Russia talks",
     "Allies meet in Berlin with united Ukraine position."),
    ("TECH", "ASIA", "California probes Nvidia on China chips",
     "State opens inquiry after Huang\u2019s exit."),
    ("WAR", "EUROPE", "Crimean Bridge hit a third time",
     "Third strike in four days; Putin vows response."),
    ("MARKETS", "AMERICAS", "S&P 500 falls 2.0%",
     "Fifth straight loss despite Anthropic debut."),
    ("WEATHER", "ASIA", "Cyclone Akvan makes landfall",
     "Heavy rain lashes the Odisha coast."),
    ("WAR", "EUROPE", "Kyiv hit by four ballistic missiles",
     "Blast lands near the Dutch embassy."),
    ("WAR", "MIDEAST", "Tanker burns after Hormuz mine",
     "Ship catches fire east of the strait."),
    ("POLITICS", "AMERICAS", "Senate rejects Iran war powers",
     "Resolution fails 51\u201348 in the Senate."),
    ("POLITICS", "AMERICAS", "Trump pardons Pete Rose",
     "Posthumous pardon for baseball legend."),
    ("WAR", "MIDEAST", "Gaza plan scores 4 out of 26",
     "Five aid groups rate the implementation."),
    ("EUROPE", "EUROPE", "Genoa halts flights over drones",
     "Unidentified drones seen near the airport."),
    ("WAR", "MIDEAST", "Israel hits Hezbollah facility",
     "Airstrike in eastern Lebanon."),
    ("WEATHER", "WORLD", "Fiona the hippo dies",
     "Cincinnati Zoo star dies after swallowing a hat."),
    ("TRADE", "ASIA", "APEC adopts Shenzhen Outlook",
     "Leaders agree trade, data and AI agenda."),
    ("WAR", "EUROPE", "UK, Norway fund Ukraine naval craft",
     "\u00a3100m+ joint programme for two vessels."),
    ("POLITICS", "EUROPE", "Denmark backs Greenland defence",
     "Parliament approves the deal 109\u20130."),
    ("MARKETS", "ASIA", "Taiwan moves to steady stocks",
     "Five measures; short-selling limits begin."),
    ("POLITICS", "EUROPE", "Serbia elects parliament speaker",
     "Cupic wins with 140 votes."),
    ("WAR", "EUROPE", "Three killed in Saratov drone hit",
     "Drone attack on Russia\u2019s Saratov region."),
    ("EUROPE", "EUROPE", "One dead in France tower fire",
     "15 hurt in blaze at 18-storey block."),
    ("EUROPE", "EUROPE", "Toddler pulled from Tbilisi rubble",
     "Girl, 3, rescued 8 hours after gas blast."),
]

DATE_CHECK = (
    "The ICJ verdict was handed down on Thursday 19 November and leads "
    "this page as the week's biggest story. The other stories here "
    "happened, or were first reported, on Friday 20 November 2026."
)

FOOTER_SOURCES = (
    "Sources: Reuters, Associated Press, BBC News, AFP, The Hindu, "
    "NDTV, Al Jazeera"
)

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

    # -- masthead (v1 geometry, unchanged) -------------------------------
    def paint_masthead(self):
        d = self.draw
        d.rectangle([MARGIN, 12, PAGE_W - MARGIN, 14], fill=PALETTE["ink"])
        d.line([(MARGIN, 17), (PAGE_W - MARGIN, 17)], fill=PALETTE["ink"])
        d.text((MARGIN, 30), "WORLD EDITION", font=FONTS.sans_bold(13),
               fill=PALETTE["ink"])
        d.text((PAGE_W - MARGIN, 30), "25 STORIES  \u2022  5 REGIONS",
               font=FONTS.sans_bold(13), fill=PALETTE["ink"], anchor="ra")
        self.mid(26, "THE DAILY GLOBE", FONTS.serif_bold(66))
        self.hbar(102)
        self.mid(110, "FRIDAY,  20  NOVEMBER  2026", FONTS.serif_bold(21))
        self.hbar(138)

    # -- lead story + courthouse band (v1 geometry, unchanged) -----------
    def paint_lead(self):
        d = self.draw
        self.mid(150, LEAD_KICKER, FONTS.sans_bold(16), PALETTE["red"])
        y = 174
        for line in LEAD_LINES:
            self.mid(y, line, FONTS.serif_bold(44))
            y += 53
        y += 2
        deck = fit_words(d, LEAD_DECK, FONTS.sans(19), CONTENT_W)
        assert len(deck) == 2, f"lead deck wrapped to {len(deck)} lines, want 2"
        for line in deck:
            self.mid(y, line, FONTS.sans(19))
            y += 25
        self.paint_courthouse(336, 428)
        self.hbar(440)

    def paint_courthouse(self, top, bottom):
        """Courthouse scene inside the 92px band: sky gradient, blue
        pediment, five columns, steps, scales glyph, red vote chip."""
        d = self.draw
        x0, x1 = MARGIN, PAGE_W - MARGIN
        span = bottom - top
        for yy in range(top, bottom):
            t = (yy - top) / span
            d.line([(x0, yy), (x1, yy)],
                   fill=blend(PALETTE["sky_top"], PALETTE["sky_bottom"], t))
        hall_l, hall_r = x0 + 330, x1 - 330
        centre = (hall_l + hall_r) // 2
        navy = PALETTE["navy_dark"]
        # Pediment triangle and its entablature bar.
        d.polygon([(hall_l - 24, top + 34), (hall_r + 24, top + 34),
                   (centre, top + 6)], fill=PALETTE["blue"])
        d.rectangle([hall_l - 24, top + 34, hall_r + 24, top + 40], fill=navy)
        # Five columns.
        for i in range(5):
            col_x = hall_l + i * (hall_r - hall_l) // 4 - 7
            d.rectangle([col_x, top + 40, col_x + 14, bottom - 14],
                        fill=PALETTE["paper"], outline=navy, width=1)
        # Two steps under the colonnade.
        d.rectangle([hall_l - 24, bottom - 14, hall_r + 24, bottom - 8],
                    fill=navy)
        d.rectangle([hall_l - 36, bottom - 8, hall_r + 36, bottom - 2],
                    fill=navy)
        # Scales of justice, drawn in paper-white on the pediment.
        white = PALETTE["white"]
        d.line([(centre, top + 2), (centre, top - 2)], fill=PALETTE["ink"])
        d.line([(centre - 26, top + 22), (centre + 26, top + 22)],
               fill=white, width=2)
        d.line([(centre, top + 12), (centre, top + 22)], fill=white, width=2)
        for sign in (-1, 1):
            d.line([(centre + sign * 26, top + 22),
                    (centre + sign * 34, top + 32)], fill=white, width=2)
            d.line([(centre + sign * 26, top + 22),
                    (centre + sign * 18, top + 32)], fill=white, width=2)
            if sign < 0:
                pan = [centre - 38, top + 28, centre - 14, top + 38]
            else:
                pan = [centre + 14, top + 28, centre + 38, top + 38]
            d.arc(pan, 0, 180, fill=white, width=2)
        # Red chip, bottom-left of the band.
        chip_w = d.textlength(LEAD_CHIP, font=FONTS.sans_bold(13))
        d.rectangle([x0 + 10, top + 8, x0 + 10 + chip_w + 16, top + 32],
                    fill=PALETTE["red"])
        d.text((x0 + 18, top + 11), LEAD_CHIP,
               font=FONTS.sans_bold(13), fill=white)
        # Thin ink edges top and bottom of the band.
        d.line([(x0, top), (x1, top)], fill=PALETTE["ink"])
        d.line([(x0, bottom), (x1, bottom)], fill=PALETTE["ink"])

    # -- numbers strip (new in v5, y 450..508) ---------------------------
    def paint_numbers(self):
        d = self.draw
        cell = CONTENT_W / 6.0
        for i in range(1, 6):
            sep_x = MARGIN + i * cell
            d.line([(sep_x, 452), (sep_x, 506)], fill=PALETTE["light"])
        for i, (figure, caption) in enumerate(NUMBERS):
            cell_x = MARGIN + i * cell
            d.text((cell_x + 8, 453), figure,
                   font=FONTS.sans_bold(24), fill=PALETTE["ink"])
            lines = clip_lines(d, caption, FONTS.sans(11), cell - 16, 2)
            assert len(lines) <= 2, f"number caption overflow: {caption!r}"
            for j, line in enumerate(lines):
                d.text((cell_x + 8, 482 + j * 13), line,
                       font=FONTS.sans(11), fill=PALETTE["ink"])
        self.hbar(508)

    # -- briefs header + grid (v1 geometry, numbered tags) ---------------
    def paint_briefs_header(self):
        d = self.draw
        left = "AROUND THE WORLD  \u2014  24 MORE STORIES"
        d.text((MARGIN, 518), left, font=FONTS.sans_bold(15),
               fill=PALETTE["red"])
        right_w = d.textlength(REGION_COUNTS, font=FONTS.sans_bold(13))
        left_w = d.textlength(left, font=FONTS.sans_bold(15))
        assert left_w + right_w + 24 <= CONTENT_W, "briefs header overflows"
        d.text((PAGE_W - MARGIN, 518), REGION_COUNTS,
               font=FONTS.sans_bold(13), fill=PALETTE["ink"], anchor="ra")

    def paint_brief_grid(self):
        d = self.draw
        for idx, (category, region, headline, summary) in enumerate(BRIEFS):
            col, row = idx % 3, idx // 3
            x = MARGIN + col * (COLUMN_W + 24)
            y = GRID_TOP + row * ROW_PITCH
            # Numbered tag: red bold number + red category + grey region.
            tag_font = FONTS.sans_bold(11)
            num = str(idx + 1)
            d.text((x, y), num, font=tag_font, fill=PALETTE["red"])
            cursor = x + d.textlength(num, font=tag_font)
            cat_part = " \u2022  " + category
            d.text((cursor, y), cat_part, font=tag_font,
                   fill=PALETTE["red"])
            cursor += d.textlength(cat_part, font=tag_font)
            d.text((cursor, y), " \u2022  " + region,
                   font=FONTS.sans(11), fill=PALETTE["light"])
            # Headline: exactly one 16px bold line; fail loudly if not.
            assert d.textlength(headline, font=FONTS.serif_bold(16)) \
                <= COLUMN_W, f"brief {idx + 1} headline too long: {headline}"
            d.text((x, y + 14), headline, font=FONTS.serif_bold(16),
                   fill=PALETTE["ink"])
            # Summary: one 13px line, ellipsised if it runs long.
            for line in clip_lines(d, summary, FONTS.sans(13), COLUMN_W, 1):
                d.text((x, y + 33), line, font=FONTS.sans(13),
                       fill=PALETTE["ink"])
        bottom = GRID_TOP + 8 * ROW_PITCH
        assert bottom <= 946, f"brief grid overflows: {bottom}"

    # -- date-check box (new in v5, y 952..984) --------------------------
    def paint_date_check(self):
        d = self.draw
        d.rectangle([MARGIN, 952, PAGE_W - MARGIN, 984],
                    outline=PALETTE["ink"], width=1)
        label = "DATE CHECK  "
        label_font = FONTS.sans_bold(11)
        label_w = d.textlength(label, font=label_font)
        inner = CONTENT_W - 18  # 9px padding on each side
        # First line shares its row with the label; the second takes the
        # full inner width. Wrap word by word against those two widths.
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
        d.text((MARGIN + 9, 958), label, font=label_font,
               fill=PALETTE["red"])
        d.text((MARGIN + 9 + label_w, 958), lines[0],
               font=FONTS.sans(11), fill=PALETTE["ink"])
        d.text((MARGIN + 9, 971), lines[1],
               font=FONTS.sans(11), fill=PALETTE["ink"])

    # -- footer ------------------------------------------------------------
    def paint_footer(self):
        self.hbar(990)
        self.mid(996, "Friday, 20 November 2026  \u2022  The Daily Globe",
                 FONTS.serif_bold(15))
        self.mid(1011, FOOTER_SOURCES, FONTS.sans(12), PALETTE["light"])

    def build(self):
        self.paint_masthead()
        self.paint_lead()
        self.paint_numbers()
        self.paint_briefs_header()
        self.paint_brief_grid()
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
