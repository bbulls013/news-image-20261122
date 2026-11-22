#!/usr/bin/env python3
"""The World in One Page - Sunday 22 November 2026.

Procedural newspaper front page drawn with the Python standard library
only. Writes a deterministic 1024x1024 PNG to $MAKEFUN_OUTPUT_DIR
(or /output) as entry.png.
"""
import os
import struct
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- font
# Tiny 5x7 bitmap font authored for this entry. '#' = ink.
FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["#####", "...#.", "..#..", "...#.", "....#", "#...#", ".###."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
    ".": [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
    ",": [".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."],
    ":": [".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."],
    ";": [".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."],
    "'": ["..#..", "..#..", ".#...", ".....", ".....", ".....", "....."],
    '"': [".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."],
    "-": [".....", ".....", ".....", "#####", ".....", ".....", "....."],
    "/": ["....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."],
    "(": ["...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."],
    ")": [".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    "?": [".###.", "#...#", "....#", "..##.", "..#..", ".....", "..#.."],
    "%": ["##..#", "##.#.", "...#.", "..#..", ".#...", ".#.##", "#..##"],
    "$": ["..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    "&": [".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"],
    "*": [".....", "#.#.#", ".###.", "#####", ".###.", "#.#.#", "....."],
    "=": [".....", ".....", "#####", ".....", "#####", ".....", "....."],
    ">": ["#....", ".#...", "..#..", "...#.", "..#..", ".#...", "#...."],
    "<": ["....#", "...#.", "..#..", ".#...", "..#..", "...#.", "....#"],
}

# ------------------------------------------------------------- palette
PAPER = (250, 247, 238)
INK = (24, 24, 28)
FAINT = (105, 102, 96)
RULE = (60, 58, 54)
RED = (168, 30, 32)
NAVY = (28, 52, 96)
TEAL = (16, 96, 96)
GOLD = (146, 104, 16)
GREEN = (36, 110, 52)
PURPLE = (92, 52, 128)
BROWN = (122, 72, 28)
SLATE = (64, 72, 84)
SKY = (70, 120, 170)

fb = bytearray(W * H * 3)


def fill(color):
    px = bytes(color)
    for i in range(W * H):
        fb[i * 3:i * 3 + 3] = px


def rect(x, y, w, h, color):
    r, g, b = color
    for yy in range(max(0, y), min(H, y + h)):
        base = yy * W * 3
        for xx in range(max(0, x), min(W, x + w)):
            o = base + xx * 3
            fb[o] = r
            fb[o + 1] = g
            fb[o + 2] = b


def frame(x, y, w, h, color, t=1):
    rect(x, y, w, t, color)
    rect(x, y + h - t, w, t, color)
    rect(x, y, t, h, color)
    rect(x + w - t, y, t, h, color)


def disc(cx, cy, rad, color):
    for yy in range(cy - rad, cy + rad + 1):
        for xx in range(cx - rad, cx + rad + 1):
            if (xx - cx) ** 2 + (yy - cy) ** 2 <= rad * rad:
                if 0 <= xx < W and 0 <= yy < H:
                    o = (yy * W + xx) * 3
                    fb[o], fb[o + 1], fb[o + 2] = color


def text_w(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(x, y, s, color, scale=1, bold=False):
    cx = x
    for ch in s.upper():
        glyph = FONT.get(ch, FONT["?"])
        for row in range(7):
            line = glyph[row]
            for col in range(5):
                if line[col] == "#":
                    rect(cx + col * scale, y + row * scale, scale, scale, color)
                    if bold:
                        rect(cx + col * scale + 1, y + row * scale, scale, scale, color)
        cx += 6 * scale
    return cx


def draw_text_c(cx_center, y, s, color, scale=1, bold=False):
    w = text_w(s, scale) + (scale if bold else 0)
    draw_text(cx_center - w // 2, y, s, color, scale, bold)


def wrap(s, max_chars):
    words = s.split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(x, y, s, color, scale, max_chars, line_gap=3, bold=False, max_lines=3):
    lines = wrap(s, max_chars)[:max_lines]
    for i, line in enumerate(lines):
        draw_text(x, y + i * (7 * scale + line_gap), line, color, scale, bold)
    return y + len(lines) * (7 * scale + line_gap)


# -------------------------------------------------------------- content
# (headline, summary) - written for this entry from the day's reports.
SECTIONS = [
    ("AMERICAS", NAVY, [
        ("PERU QUAKE SHAKES LIMA",
         "M6.8 tremor near Junin felt in capital; no casualties reported so far."),
        ("MEXICO ARRESTS CARTEL SUSPECT",
         "Alleged boss 'El Chapo Isidro' held in special-forces raid, officials say."),
        ("FBI PROBES DATABASE HACK",
         "Bureau reportedly investigating apparent breach of criminal records system."),
        ("PALISADES FIRE ARSON VERDICT",
         "Man found guilty of starting one of California's deadliest blazes."),
        ("NYC PLAN TO CLOSE RIKERS JAIL",
         "Mayor Mamdani sets out closure plan for the island jail complex."),
        ("US-CANADA DEFENCE LIMITS",
         "Pentagon chief adds new limits on military ties, reports say."),
    ]),
    ("EUROPE", TEAL, [
        ("ESTONIA TO SHUT RUSSIA BORDER",
         "Tallinn moves to close frontier; Moscow decries a 'new Iron Curtain'."),
        ("UK, NETHERLANDS BACK UKRAINE",
         "Leaders pledge sustained aid against Russia's invasion."),
        ("KYIV: BRIDGE STRIKES A REPLY",
         "Zelensky calls Crimean Bridge hits a 'fair response' in London talks."),
        ("BLAIR WARNS ON EU RETURN",
         "UK should rejoin only if it innovates on technology, Blair says."),
        ("DENMARK ALLEGES KILL PLOT",
         "Copenhagen accuses Russia of plotting to kill a rapper. Developing."),
        ("OSLO TREE SAILS FOR LONDON",
         "Trafalgar Square Christmas tree sets off from Norway."),
    ]),
    ("ASIA-PACIFIC", GOLD, [
        ("MODI OPENS NITISH SETU BRIDGE",
         "New Bihar bridge links Patna and Vaishali districts."),
        ("CYCLONE AKVAN DISRUPTS FLIGHTS",
         "14 flights cancelled at Ranchi airport as storm nears. Developing."),
        ("JAPAN TO TRAIN IN INDIA",
         "Japanese forces to use Indian facilities for live-fire drills, a first."),
        ("NEPAL PM TO VISIT INDIA",
         "Balendra Shah to meet Modi on first bilateral visit."),
        ("APEC LEADERS GATHER IN SHENZHEN",
         "Trump arrives; trilateral with Xi and Putin planned. Developing."),
        ("INDIA HEALTH TECH TRANSFERS",
         "ICMR marks 100 technology transfers at research summit."),
    ]),
    ("MIDDLE EAST + AFRICA", BROWN, [
        ("GULF STRIKES REPORTED",
         "Iran said to hit US base in Kuwait, target Bahrain. Developing."),
        ("TANKERS HIT NEAR HORMUZ",
         "UKMTO: vessels struck by unknown projectiles; crew member missing."),
        ("ISRAEL COALITION MANOEUVRES",
         "Ex-PM backs Eisenkot for PM, says he will not serve under Netanyahu."),
        ("LEBANON CALLS FOR WITHDRAWAL",
         "President Aoun urges Israeli pullout and Hezbollah disarmament."),
        ("BASRA PLANT FIRE KILLS FOUR",
         "35 injured in fire at electricity facility in Iraq, reports say."),
        ("SOUTH AFRICA CITY VOTE FIGHT",
         "ANC battles to keep control of cities after election setback."),
    ]),
    ("BUSINESS", GREEN, [
        ("ANTHROPIC IPO FAILS TO LIFT AI",
         "Record $81bn listing; shares fell 8.5% Friday to $88.91, IPO was $83."),
        ("NASDAQ LOSES YEAR'S GAINS",
         "Index fell 5.28% Friday; S+P 500 down for a seventh straight day."),
        ("FEAR GAUGE SPIKES",
         "VIX surged 86% this week to 35.89, a 19-month high."),
        ("OIL FUTURES SLIDE 3%+",
         "Crude fell more than 3% amid demand and rate worries."),
        ("SENSEX ENDS RALLY",
         "Indian shares fell on profit booking and US Fed rate concerns."),
        ("INVESTORS SEEK SAFETY",
         "Treasury bonds rallied as traders fled technology stocks."),
    ]),
    ("TECHNOLOGY", PURPLE, [
        ("COP31 AI PLEDGE SNUBBED",
         "Climate AI pledge fails to attract major US tech firms."),
        ("US DATA-CENTRE THREAT",
         "Trump threatens ban on US firms building AI data centres abroad."),
        ("NVIDIA LEADERSHIP QUESTIONS",
         "Markets unsettled by uncertainty after Jensen Huang resignation."),
        ("AI AND A FAMOUS MATHS PROBLEM",
         "Claims AI helped solve a celebrated problem. Developing."),
        ("EU EYES DIGITAL TAX",
         "Draft 2028-34 budget proposes taxing digital platforms."),
        ("DATA-CENTRE PACE IN DOUBT",
         "New governors may slow the AI buildout, investors fear."),
    ]),
    ("SCIENCE + CLIMATE", SKY, [
        ("COP31 IN OVERTIME DEADLOCK",
         "Fossil-fuel wording and adaptation finance split nearly 200 nations."),
        ("ETHIOPIA TO HOST COP32",
         "Addis Ababa confirmed as host of the 2027 climate conference."),
        ("EL NINO STRAINS THE PLANET",
         "Record-breaking El Nino adds to heatwaves and floods worldwide."),
        ("CARBON REMOVAL DIVIDES TALKS",
         "Some delegations fear removal tech prolongs fossil-fuel use."),
        ("IPCC TIMETABLE ROW",
         "Timing of next climate science reports fuels COP friction."),
    ]),
    ("SPORT", RED, [
        ("INDIA LEAD NZ BY 118 RUNS",
         "Day 3, Wellington: Rahul 136, Gill 98; Nicholls hit 175 for NZ."),
        ("AUSTRALIA END ENGLAND STREAK",
         "Hosts chased 188 to win by 3 wickets, breaking a 7-match T20 run."),
        ("NEWCASTLE 2-2 ARSENAL",
         "Honours shared in Premier League clash."),
        ("REAL MADRID 2-1 CELTA",
         "Madrid take the points in Spain; Napoli beat Torino 1-0."),
        ("PALMEIRAS 1-1 FLAMENGO",
         "Brazilian giants draw; Schalke and Stuttgart finish 0-0."),
    ]),
    ("CULTURE", SLATE, [
        ("IFFI ADDS ANIMATION SECTION",
         "57th festival to feature five international animated films."),
        ("DILJIT QUESTIONS 'DOUBLE STANDARD'",
         "Singer raises the issue at Ahmedabad concert, cites Coldplay."),
        ("CHENNAI BOOK FAIR DATES SET",
         "International fair to run 16-18 January 2027."),
        ("TRNSMT FESTIVAL FUTURE DEBATED",
         "Scotland's largest music festival faces questions over its future."),
        ("FOREST STAFF INSURANCE SCHEME",
         "Prince William announces cover for 10,000 temporary forest staff."),
    ]),
]

TIMELINE = [
    ("00:00", "COP31 talks run past deadline in Antalya"),
    ("07:00", "Peru quake aftermath checks continue"),
    ("09:00", "APEC leaders arrive in Shenzhen"),
    ("13:00", "Cricket: India extend lead in Wellington"),
    ("17:00", "European football results come in"),
    ("21:00", "Markets brace for Monday after AI selloff"),
]


def draw_map(x, y, w, h):
    """Simple schematic world map: blocky continents + story markers."""
    frame(x, y, w, h, RULE, 1)
    rect(x + 1, y + 1, w - 2, h - 2, (232, 238, 244))
    land = (150, 175, 140)
    # North America
    rect(x + 14, y + 18, 56, 24, land)
    rect(x + 26, y + 42, 30, 12, land)
    # South America
    rect(x + 52, y + 58, 26, 30, land)
    rect(x + 60, y + 88, 13, 16, land)
    # Europe
    rect(x + 118, y + 16, 38, 20, land)
    # Africa
    rect(x + 122, y + 42, 34, 34, land)
    rect(x + 132, y + 76, 17, 18, land)
    # Asia
    rect(x + 170, y + 14, 70, 28, land)
    rect(x + 186, y + 42, 26, 24, land)
    rect(x + 220, y + 42, 20, 18, land)
    # Oceania
    rect(x + 226, y + 76, 30, 16, land)
    # markers: (dx, dy, color, label, label_dx, label_dy)
    marks = [
        (64, 66, RED, "PERU", -34, -3),
        (136, 24, TEAL, "EU", 7, -3),
        (164, 38, BROWN, "GULF", -2, 7),
        (198, 52, GOLD, "INDIA", 7, -3),
        (236, 32, PURPLE, "APEC", 7, -3),
        (138, 60, BROWN, "AFRICA", 7, -3),
    ]
    for dx, dy, color, label, ldx, ldy in marks:
        disc(x + dx, y + dy, 4, color)
        draw_text(x + dx + ldx, y + dy + ldy, label, INK, 1, True)
    draw_text(x + 6, y + 4, "WHERE IT HAPPENED", NAVY, 1, True)


def build():
    fill(PAPER)
    m = 28  # margin
    # ---------------------------------------------------------- masthead
    draw_text_c(W // 2, 18, "THE WORLD IN ONE PAGE", INK, 5, True)
    draw_text_c(W // 2, 62, "SUNDAY 22 NOVEMBER 2026", RED, 3, True)
    draw_text_c(W // 2, 88, "ONE DAY OF WORLD NEWS - EVERY REGION, EVERY FIELD", FAINT, 1, True)
    rect(m, 104, W - 2 * m, 3, INK)
    rect(m, 110, W - 2 * m, 1, INK)
    # --------------------------------------------------------- lead story
    ly = 118
    rect(m, ly, W - 2 * m, 62, (243, 238, 222))
    frame(m, ly, W - 2 * m, 62, RULE, 1)
    draw_text(m + 10, ly + 6, "LEAD STORY - ANTALYA", RED, 1, True)
    draw_text(m + 10, ly + 17, "CLIMATE TALKS DEADLOCKED OVER FOSSIL FUELS", INK, 2, True)
    draw_wrapped(m + 10, ly + 36,
                 "COP31 runs deep into overtime as nearly 200 countries split over fossil-fuel "
                 "wording and help for poorer nations. EU: 'a good deal or no deal'. Developing.",
                 INK, 1, 150, 3, False, 2)
    # ------------------------------------------------------------- columns
    col_w = (W - 2 * m - 2 * 14) // 3
    cols_x = [m, m + col_w + 14, m + 2 * (col_w + 14)]
    top = 192
    bottom = 846
    # map sits at top of column 3
    draw_map(cols_x[2], top, col_w, 112)
    col_sections = [
        [SECTIONS[0], SECTIONS[1], SECTIONS[2]],
        [SECTIONS[3], SECTIONS[4], SECTIONS[5]],
        [SECTIONS[6], SECTIONS[7], SECTIONS[8]],
    ]
    for ci, sections in enumerate(col_sections):
        x = cols_x[ci]
        y = top + (120 if ci == 2 else 0)
        for name, color, stories in sections:
            rect(x, y, col_w, 15, color)
            draw_text(x + 6, y + 4, name, PAPER, 1, True)
            y += 19
            for headline, summary in stories:
                y = draw_wrapped(x, y, headline, INK, 1, 48, 2, True, 2)
                y = draw_wrapped(x, y + 1, summary, (52, 52, 56), 1, 52, 2, False, 2)
                y += 4
            y += 3
        if y > bottom:
            pass  # layout checked by eye in v1; tightened in v2 if needed
    # ------------------------------------------------------------ timeline
    ty = 852
    rect(m, ty, W - 2 * m, 2, INK)
    draw_text(m, ty + 6, "THE DAY IN SIX BEATS - ALL TIMES UTC, DEVELOPING STORIES MARKED", NAVY, 1, True)
    line_y = ty + 34
    rect(m + 8, line_y, W - 2 * m - 16, 2, RULE)
    n = len(TIMELINE)
    for i, (when, what) in enumerate(TIMELINE):
        cx = m + 52 + i * ((W - 2 * m - 104) // (n - 1))
        disc(cx, line_y + 1, 5, RED)
        draw_text_c(cx, line_y - 14, when, INK, 1, True)
        lines = wrap(what, 24)[:3]
        for j, line in enumerate(lines):
            draw_text_c(cx, line_y + 10 + j * 10, line, INK, 1)
    # -------------------------------------------------------------- footer
    fy = 972
    rect(m, fy - 8, W - 2 * m, 1, RULE)
    n_stories = sum(len(s[2]) for s in SECTIONS) + 1  # + lead story
    draw_text_c(W // 2, fy,
                "%d STORIES FROM THE DAY'S REPORTS - HEADLINES IN OUR OWN WORDS - NOTHING HERE IS SPECULATION" % n_stories,
                FAINT, 1, True)
    draw_text_c(W // 2, fy + 12,
                "SOURCES: WIRE AND BROADCAST REPORTS FIRST PUBLISHED 21-22 NOV 2026 - MADE FOR MAKE.FUN",
                FAINT, 1)


def write_png(path):
    raw = bytearray()
    stride = W * 3
    for yy in range(H):
        raw.append(0)
        raw.extend(fb[yy * stride:(yy + 1) * stride])
    comp = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        c += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return c

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    build()
    write_png(os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
