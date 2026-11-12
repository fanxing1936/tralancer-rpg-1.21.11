"""Native 16 x 16, hand-placed pixels. Run with Python + Pillow.

All outputs stay beside this file. No resizing or quantizing of draft art.
The final BRIEF16 material requirements supersede its earlier 12-colour cap;
seals use only the explicitly permitted nine greys.
"""
from pathlib import Path
import hashlib
import json
from PIL import Image

HERE = Path(__file__).resolve().parent
PILLARS = {
    'lucifer': ('00491C', '5FD68C'),
    'leviathan': ('1B4F72', '4F9EF0'),
    'abaddon': ('6A6A70', 'A7AFC9'),
    'beelzebub': ('5A6B1E', 'B5D957'),
    'samael': ('7B241C', 'FF5C52'),
    'belial': ('5B2C6F', 'D97AD9'),
    'mammon': ('B7950B', 'E6A23C'),
}

def rgb(s):
    return tuple(bytes.fromhex(s))

def mix(a, b, t):
    return tuple(round(x * (1-t) + y * t) for x, y in zip(a, b))

def rgba(c):
    return (*c, 255)

def blank():
    return Image.new('RGBA', (16, 16))

def put(im, xy, c):
    im.putpixel(xy, rgba(c))

def matrix(rows, palette):
    assert len(rows) == 16 and all(len(r) == 16 for r in rows)
    im = blank()
    for y, row in enumerate(rows):
        for x, key in enumerate(row):
            if key != '.':
                put(im, (x, y), palette[key])
    return im

# All seven books share these material IDs, not merely the alpha silhouette.
# 0..6 leather; a..e bevelled metal; p..u stacked paper.
BOOK = [
    '................',
    '........00......',
    '......00aeb.....',
    '....00a6540b....',
    '..00a6554430b...',
    '.0ab665544330b..',
    '.aed655443321ab.',
    '.b65534433210eb.',
    '.0544332210tuc0.',
    '.023443210tups0.',
    '.0123210tupsp0..',
    '..0120tupspq0...',
    '...00tupspq0....',
    '....0spqrs0.....',
    '.....00000......',
    '................',
]
GOLD = dict(zip('abcde', map(rgb, ['51401F', '8F7430', 'B08C36', 'D4AF37', 'FFE59A'])))
PAPER = dict(zip('pqrstu', map(rgb, ['D5C89B', '91805B', '564A36', 'AF9D73', 'EFE3B8', 'FFF4D5'])))

def book_palette(deep, lit):
    d, l = rgb(deep), rgb(lit)
    leather = [mix(d, (12, 9, 18), .67), mix(d, (12, 9, 18), .37),
               d, mix(d, l, .24), mix(d, l, .46), mix(d, l, .70), l]
    return dict(zip('0123456', leather)) | GOLD | PAPER | {
        'v': mix(d, l, .83), 'w': mix(l, (255, 255, 255), .57),
        'z': (255, 255, 255)}

def book(deep, lit, tier):
    pal = book_palette(deep, lit)
    if tier == 1:
        # Same leather/paper IDs and geometry; all metal is cold iron.
        pal.update(dict(zip('abcde', map(rgb, [
            '3A3A40', '6A6A72', '6A6A72', 'A0A0A8', 'A0A0A8']))))
    im = matrix(BOOK, pal)
    # Four separate raised clasps: a bright upper pixel, mid face, dark foot.
    clasps = [((8, 2), (9, 2), (9, 3)), ((2, 5), (3, 5), (3, 6)),
              ((13, 6), (14, 6), (14, 7)), ((5, 10), (6, 10), (6, 11))]
    for hi, face, shade in clasps:
        for xy, key in ((hi, 'e'), (face, 'c'), (shade, 'a')):
            put(im, xy, pal[key])
    if tier == 3:
        # The same book, with an uninterrupted upper and lower gold binding.
        for xy in [(4, 4), (5, 3), (6, 3), (7, 2), (10, 3), (11, 4),
                   (12, 5), (13, 5), (4, 10), (7, 10), (8, 9), (9, 9),
                   (10, 8), (11, 8), (12, 7)]:
            put(im, xy, pal['d' if sum(xy) % 3 else 'c'])
        # Three one-pixel crown tips, attached to the upper diagonal edge.
        for tip, base in [((4, 2), (4, 3)), ((7, 1), (7, 2)), ((10, 1), (10, 2))]:
            put(im, tip, pal['e'])
            put(im, base, pal['b'])
        glyph = {(8, y) for y in range(4, 9)} | {(x, 6) for x in range(6, 11)}
        # Dark recessed bed then a one-pixel symmetric luminous cross.
        core = {(8, y) for y in range(5, 8)} | {(x, 6) for x in range(7, 10)}
    else:
        glyph = {(8, 4), (7, 5), (8, 5), (9, 5), (8, 6)}
        core = {(8, 5)}
    for x, y in sorted(glyph):
        for dx, dy in [(0, -1), (-1, 0), (1, 0), (0, 1), (1, 1)]:
            if (x+dx, y+dy) not in glyph:
                put(im, (x+dx, y+dy), pal['0' if dx+dy < 2 else '1'])
    for xy in sorted(glyph):
        if tier == 1:
            # Recessed stamp with one upper-left lip; no luminous core.
            put(im, xy, pal['3' if xy == (8, 4) else '1'])
        else:
            put(im, xy, pal['w' if xy in core else 'v'])
    if tier == 3:
        put(im, (8, 5), pal['z'])
    return im

# Curl at top right; dark torn/burnt edges; selected fibre clusters, no noise.
PAGE = [
    '................',
    '....abbbbbb.....',
    '...acijkijla....',
    '..acjijkjifga...',
    '.abijijijkfhga..',
    '..acijjjijkhba..',
    '..bijjjjjjjjca..',
    '.abijjjjjjjjica.',
    '.acjjjjjjjjjjba.',
    '.abjjjjjjjjjjca.',
    '.acjjjjjjjjjjba.',
    '.abijjjjjjjjica.',
    '..bcjijjkijjca..',
    '..abijijkjicba..',
    '...abbbbcbbba...',
    '................',
]
PAGE_PALETTE = dict(zip('abcfghijkl', map(rgb, [
    '503923', '7D5832', 'AD8247', '655039', '9E855C', 'C3A771',
    'D6BD86', 'E8D39E', 'F7E9BB', 'FFF4D5'])))

# 7 x 8 source glyphs. A flat-topped crown, anchor, hourglass, insect,
# sword, eye, and coin. Shape is independent of colour mapping.
SYMBOLS = [
    ['#..#..#', '#..#..#', '##.#.##', '.#####.', '.#####.', '.#####.', '.......', '.......'],
    ['..###..', '..#.#..', '...#...', '.#####.', '...#...', '#..#..#', '##.#.##', '.#####.'],
    ['#######', '.#...#.', '..#.#..', '...#...', '..#.#..', '.#...#.', '.#####.', '#######'],
    ['..#.#..', '...#...', '##.#.##', '##.#.##', '##.#.##', '..###..', '.#.#.#.', '...#...'],
    ['...#...', '..###..', '..###..', '..###..', '..###..', '.#####.', '...#...', '...#...'],
    ['.......', '..###..', '.#...#.', '#..#..#', '.#...#.', '..###..', '.......', '.......'],
    ['..###..', '.#####.', '###.###', '##...##', '###.###', '.#####.', '..###..', '.......'],
]

def page(deep, lit, glyph):
    im = matrix(PAGE, PAGE_PALETTE)
    d, l = rgb(deep), rgb(lit)
    ink = [mix(d, (19, 13, 25), .60), mix(d, (19, 13, 25), .24),
           d, mix(d, l, .32), mix(d, l, .68), l,
           mix(l, (255, 244, 213), .38)]
    mask = {(x+5, y+5) for y, row in enumerate(glyph) for x, c in enumerate(row) if c == '#'}
    for x, y in sorted(mask):
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            if (x+dx, y+dy) not in mask:
                put(im, (x+dx, y+dy), ink[0 if dx+dy < 0 else 1])
    for x, y in sorted(mask):
        index = (6 if x <= 7 else 5) if y <= 7 else (3 if x < 8 else 2) if y >= 10 else (4 if x <= 8 else 3)
        put(im, (x, y), ink[index])
    if glyph == SYMBOLS[3]:
        # Separate two broad wings from the insect's narrow head/thorax.
        for xy, index in [((8, 6), 6), ((8, 7), 2), ((8, 8), 4),
                          ((8, 9), 2), ((8, 10), 2), ((8, 11), 2), ((8, 12), 1),
                          ((5, 7), 6), ((6, 7), 6), ((5, 8), 5), ((6, 8), 5),
                          ((5, 9), 4), ((6, 9), 4), ((10, 7), 5), ((11, 7), 5),
                          ((10, 8), 4), ((11, 8), 4), ((10, 9), 3), ((11, 9), 3)]:
            put(im, xy, ink[index])
    return im

GREYS = list(map(rgb, ['141414', '2E2E2E', '4A4A4A', '666666', '808080', 'A0A0A0', 'BEBEBE', 'DEDEDE', 'FFFFFF']))
SEAL = [
    '................',
    '.....011110.....',
    '...0167776510...',
    '..017865554310..',
    '..168655544321..',
    '.01665555443310.',
    '.17855554443320.',
    '.17655444433320.',
    '.16554444333210.',
    '.16554443333210.',
    '.01544433332210.',
    '..134433332210..',
    '..013333322110..',
    '...0122222110...',
    '.....011110.....',
    '................',
]
SEAL_GLYPHS = [
    ['#######', '#.....#', '#.....#', '#.....#', '.#...#.', '..#.#..', '...#...'],
    ['....###', '.....##', '....#.#', '...#...', '..#....', '.#.....', '#......'],
    ['#.....#', '#.....#', '.#...#.', '..###..', '...#...', '...#...', '.#####.'],
    ['.......', '..###..', '.#...#.', '#..#..#', '.#...#.', '..###..', '.......'],
    ['...#...', '...####', '...####', '...###.', '...#...', '...#...', '...#...'],
]

def seal(glyph):
    im = matrix(SEAL, dict(zip('012345678', GREYS)))
    mask = {(x+4, y+4) for y, row in enumerate(glyph) for x, c in enumerate(row) if c == '#'}
    # Incision: shadow on upper-left lip, caught light on lower-right lip.
    for x, y in sorted(mask):
        for dx, dy, shade in [(-1, 0, 1), (0, -1, 1), (1, 0, 6), (0, 1, 6)]:
            if (x+dx, y+dy) not in mask:
                put(im, (x+dx, y+dy), GREYS[shade])
    for x, y in sorted(mask):
        put(im, (x, y), GREYS[2 if y <= 7 else 3])
    return im

def reference():
    # The supplied sheet is 7 cells x 2 rows, 380 pixels per cell.
    # Native sprites are enlarged 20x inside a 320-square canvas at (30, 30).
    ref = Image.open(HERE.parent / 'raw16/ref_style.png').convert('RGBA')
    return ref.crop((2*380+30, 380+30, 2*380+350, 380+350)).resize((16, 16), Image.Resampling.NEAREST)

def preview(assets):
    # 32 native pixels (two icon widths) of fully transparent separation.
    board = Image.new('RGBA', (16 + 7*48, 16 + 5*48))
    groups = [[assets[f'pact_{n}.png'] for n in PILLARS],
              [assets[f'pact_{n}_t2.png'] for n in PILLARS],
              [assets[f'pact_{n}_t3.png'] for n in PILLARS],
              [assets[f'page_{n}.png'] for n in PILLARS],
              [assets[f'seal_{n}.png'] for n in range(1, 6)]]
    for row, group in enumerate(groups):
        for col, im in enumerate(group):
            board.paste(im, (8+48*col, 8+48*row))
    board.resize((board.width*6, board.height*6), Image.Resampling.NEAREST).save(HERE / 'preview.png')
    compare = Image.new('RGBA', (16+8*48, 32))
    for i, im in enumerate(groups[1] + [reference()]):
        compare.paste(im, (8+i*48, 8))
    compare.resize((compare.width*6, compare.height*6), Image.Resampling.NEAREST).save(HERE / 'comparison_t2.png')
    detail = Image.new('RGBA', (160, 32))
    for i, name in enumerate(('pact_lucifer_t2.png', 'pact_lucifer_t3.png', 'page_beelzebub.png')):
        detail.paste(assets[name], (8+i*48, 8))
    detail.resize((1600, 320), Image.Resampling.NEAREST).save(HERE / 'review_detail.png')

def main():
    # This task only generates tier one. In particular, the accepted seal
    # rework on disk is newer than seal() and the original validation entries.
    validation_path = HERE / 'validation.json'
    validation = json.loads(validation_path.read_text(encoding='utf-8'))
    names = ([f'pact_{n}_t{tier}.png' for n in PILLARS for tier in (2, 3)]
             + [f'page_{n}.png' for n in PILLARS]
             + [f'seal_{i}.png' for i in range(1, 6)])
    before = {n: hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in names}
    original_mismatches = [n for n in names
                           if before[n] != validation['assets'][n]['sha256']]
    # Do not silently bless a changed book or page. Existing seal discrepancies
    # are recorded separately without replacing the historical SHA-256 values.
    assert all(n.startswith('seal_') for n in original_mismatches), original_mismatches
    assets = {n: Image.open(HERE/n).convert('RGBA') for n in names}
    report = {}
    patterns = []
    for name, (deep, lit) in PILLARS.items():
        filename = f'pact_{name}.png'
        im = book(deep, lit, 1)
        colors = {p[:3] for p in im.getdata() if p[3]}
        assert im.size == (16, 16)
        assert {p[3] for p in im.getdata()} == {0, 255}
        assert 14 <= len(colors) <= 22, (filename, len(colors))
        assert not (colors & set(GOLD.values())), filename
        assert im.getchannel('A').tobytes() == assets[f'pact_{name}_t2.png'].getchannel('A').tobytes()
        assert book(deep, lit, 2).tobytes() == assets[f'pact_{name}_t2.png'].tobytes()
        # Only iron and the recessed glyph may differ from tier two.
        leather_paper = {rgba(book_palette(deep, lit)[k]) for k in '0123456pqrstu'}
        t2 = assets[f'pact_{name}_t2.png']
        glyph_area = {(x, y) for y in range(3, 8) for x in range(6, 11)}
        for y in range(16):
            for x in range(16):
                if (x, y) not in glyph_area and t2.getpixel((x, y)) in leather_paper:
                    assert im.getpixel((x, y)) == t2.getpixel((x, y))
        seen = {}
        patterns.append([seen.setdefault(p, len(seen)) for p in im.getdata()])
        im.save(HERE / filename)
        assets[filename] = im
        report[filename] = {
            'size': [16, 16], 'opaque_colors': len(colors), 'alpha': [0, 255],
            'bbox': im.getbbox(),
            'sha256': hashlib.sha256((HERE/filename).read_bytes()).hexdigest()}
    assert all(p == patterns[0] for p in patterns)
    preview(assets)
    tiers = Image.new('RGBA', (16 + 7*48, 16 + 3*48))
    for row, suffix in enumerate(('.png', '_t2.png', '_t3.png')):
        for col, name in enumerate(PILLARS):
            tiers.paste(assets[f'pact_{name}{suffix}'], (8+48*col, 8+48*row))
    tiers.resize((tiers.width*6, tiers.height*6), Image.Resampling.NEAREST).save(HERE / 'preview_tiers.png')
    after = {n: hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in names}
    assert after == before
    validation['tier1_2026_11_07'] = {
        'assets': report,
        'checks': {'native_grid': True, 'binary_alpha': True,
                   'opaque_colors_14_to_22': True, 'no_gold_metal': True,
                   't2_silhouette_identical': True,
                   'shared_color_structure': True,
                   'existing_files_unchanged': before == after},
        'existing_sha256': after,
        'preexisting_original_validation_mismatches': original_mismatches}
    validation_path.write_text(json.dumps(validation, indent=2) + '\n', encoding='utf-8')
    print('Tier one: ' + ', '.join(f'{n}: {v["opaque_colors"]}' for n, v in report.items()))
    print(f'Existing files unchanged: {len(names)}/{len(names)}; pre-existing validation mismatches: {original_mismatches}')

if __name__ == '__main__':
    main()
