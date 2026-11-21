from pathlib import Path
import hashlib
import json

from PIL import Image


HERE = Path(__file__).resolve().parent
KEYS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def palette(text):
    return [tuple(bytes.fromhex(value)) + (255,) for value in text.split()]


def paint(rows, colors):
    canvas = Image.new('RGBA', (16, 16))
    for row_index, row in enumerate(rows.split(), 1):
        assert row_index <= 14 and len(row) <= 14, row
        for column, key in enumerate(row, 1):
            if key != '.':
                canvas.putpixel((column, row_index), colors[KEYS.index(key)])
    return canvas


MATERIALS = {
    'blank': ('''........4320
.....332566410
...32788A97632
..358969B71520
.3587636865D2
358B572977DE2
486A85867DEF2
39865466DEF2
286536CDEF2
2765CCDEF1
246CDEF1
15CDE21
04CD21
.0111''', '182127 302a2b 303d46 43535d 576975 647987 788f9a 8a9ca4 9cacb1 bac9c6 d0d9d3 535e62 704538 9d5337 bb6845 f09159'),
    'soul': ('''.......1
......190
.....1A920
..1..2B842..10
.180.3CA842271
.17A12DB98471
..18A4DCA95821
...4BDEB963310
..16BEA86327F0
.179B97421FHG0
18A87231FGI10
.121.1FHHG10
......0FG10
.......00''', '15172d 182f46 214459 255d70 277787 318795 42a5a8 55b6b8 67cbc7 80ddda 9beee6 b6fff1 54d8d0 d8fff8 f3fff8 292439 39304e 55406b 675281'),
    'forge_stone': ('''..3344445452
.3578889876432
3589A988657432
469A9848875432
36898487754852
24898576543262
37897B66653832
2689CDE5BC6542
248BCEDFDEF542
267DB8757DEDB2
257C767653BCD2
246577865433B2
1356455354321
.11212121221''', '21191b 322822 45372e 594941 6b594b 7b6856 8d775f a48b73 b7a189 cbb99d e0cdb0 702c27 a13727 d64b25 fe8032 ffc46d'),
    'wash_gem': ('''....023320
..0248976530
.1589AF875410
049AFGED984321
28AEFCBA9D9751
.28AGED9DBA652
..28DGCAB98720
...27DFGEBA3
....268FD942
.....27DAC2
......2682
.......62
.......20''', '102e46 0e4965 176780 207e99 298da9 36a9c1 3cbdd0 51cedc 66ddeb 7debf4 96f5f6 adfff9 5fe3f0 c8ffff ddfcfe f3ffff ffffff'),
    'gild_leaf': ('''.........0320
.......048A652
.....049ADBCF2
...039ACFECB2
..39ADDEC92320
.49ADEC9315972
38BFC942589DB2
29DB85268ADF2
.2753248BEA2
..03468DB73520
..26ABF9358DB2
.27DB83269CF2
369722469DB2
.220.023320''', '402b18 553514 664420 805522 9c6b24 af7525 c48c29 d69932 e6ad3e f0c457 ffd76a ffe283 fff09c b77e2a fff6ba 966225'),
}

SOURCE = '''....ABCDEA
..AC44556DDA
.B3568776658EA
AC46778764469A
B367898765433A
D478987654312A
E478876754221F
D467765543211F
C356654432100F
A534543321100F
.B6433322100F
..FF100010FF
....FFFFFF'''

RUNE = '''......00..000
....0B3300FAG0
...0C798898950
..0D7655666420
.0E76466765320
04764677765420
03754677865220
02744667764320
01643556653210
02743455542110
0164244332110
.03532222110
..033111110
...0000000'''

STONE = '''....AABEE0
..AB976874B0
.AB97989443C0
AB7978986433C0
AC7989887653C0
B68998987653C0
B68989776642C0
AC7897676542C0
.AC876765432C0
..AD6565432C0
...CD54322C0
....CD322C0
.....CDC00
......00'''

GOLD = palette('4c361c 69501f d4af37 f4d36c 9d7a30 3b2c20')
IRON = palette('282830 3a3a40 6a6a72 a0a0a8 53535a 212129')
SETTING = palette('5c4a1e 8f7430 d4af37 725722 ba9634')

SOURCES = {
    'faith': ('36170f 561907 701900 8a1c00 a52609 bf2b0d de3613 ff3300 ff6337 ffaa76', '...#.../...#.../.#####./...#.../...#.../...#...', 5, 4),
    'hope': ('37352e 575145 736e61 8f8a7a a9a38f bdb7a3 d4ceb8 f2eedc fff6de fffdf3', '...#.../...#.../..###../#######/..###../...#.../...#...', 5, 4),
    'resolve': ('3c2912 503510 65450d 7a5410 986a13 b68422 cc9734 e0a93a f4c352 ffe69f', '.#####./#######/#.###.#/##.#.##/.##.##./..###../...#...', 5, 4),
    'malice': ('291b39 3a204c 4b255e 5b2c6f 763480 91448f b158aa d97ad9 ec9ee4 fbc3f2', '..###../.##.##./###.###/.##.##./..###..', 5, 5),
    'hatred': ('341619 4b1919 641d1d 7b241c a12c27 bf3934 e04740 ff5c52 ff8073 ffb095', '##...##/.##.##./..###../..###../.##.##./##...##', 5, 4),
    'pride': ('0e241b 0e311f 124123 00491c 145e32 277944 36aa63 5fd68c 86efa6 c6ffce', '#..#..#/#.###.#/#######/.#####./.#.#.#./.#####.', 5, 4),
}

COPPER = '371f19 53261c 6b2e1a 82361e 974324 a8522e bc6338 d37546 e08a55 f6ab78 ffe0ad aa5635 bd6945 b05937 9a492e cc754b 91472d'
MOSS = '22291a 283719 2e4a1e 395b24 4b702d 5c8a3a 6e9c42 83b456 a8d27a d0eb9a eff8c2 537e36 79a04c 679044 507538 91ba61 466531'
STEEL = '192a3b 1b3047 1e3550 274669 315779 3e6a96 507fa7 6b9ac3 8fb8e0 b9def7 e6f7ff 487598 5e89ae 4a7496 365e80 7ca5cc 416685'

RUNES = {
    'ember': (COPPER, '...#.../...##../..###../..####./.##.##./.#####./..###..'),
    'echo': (COPPER, '#..#.../.#..#../..#..#./..#..#./..#..#./.#..#../#..#...'),
    'execute': (COPPER, '...###./..##.#./..####./...##../#####../######./.####..'),
    'backstab': (COPPER, '##...../.##.#../..###../.#####./..#.##./.....##/......#'),
    'bloodpact': (COPPER, '...#.../..###../..###../.#####./.##.##./.#####./..###..'),
    'poise': (COPPER, '.##..../.#.#.../.#..#../.#.#.#./.#..#../.#.#.../.##....'),
    'hunt': (MOSS, '...#.../..###../.#.#.#./##.#.##/.#.#.#./..###../...#...'),
    'split': (MOSS, '#..#..#/.#.#.#./..###../...#.../...#.../...#.../..###..'),
    'meteor': (MOSS, '##...../.##.#../..##.../.#..#../...###./..#####/...###.'),
    'recoil': (STEEL, '.#####./.#####./..###../#..#..#/.#...#./#.....#/.#...#.'),
    'lastbreath': (STEEL, '.##.##./###.###/##.####/###.###/.##.##./..#.#../...#...'),
    'stillwater': (STEEL, '...###./###..../......./..#####/......./.###.../....###'),
    'swift': (STEEL, '###..#./.##.##./...###./..###../.####../.######/..#####'),
}

STONES = {
    'rift': ('35251a 51351b 6b4a1e 825c22 9d732b b78b3d ca9b4e e0b060 f7d288 ffe9ab', '..##./..#../.##../..##./...#.'),
    'frost': ('192d42 1b3d56 1e4a6b 296283 387fa2 539fba 74bdd9 94d6ed bfe8ff edfcff', '#.#.#/.###./#####/.###./#.#.#'),
    'shadow': ('20182e 271b3d 2e1e4a 432d64 583976 6d4b8d 8060ad a88ae0 c9b0f4 efdeff', '..##./.##../.##../.###./..###'),
    'blood': ('2e151d 3b1118 4a0e12 651d26 872735 a83643 c94552 e0505a fc7881 ffb8b3', '.####/.####/..###/..##./.#...'),
    'gale': ('132d2e 1d4040 2e5a5a 367676 46908d 62a9a0 83c4b8 b0e0d2 d8f4ec f2fff8', '..###./###.../..####/.##.../...###'),
    'volley': ('222d17 29391b 2e4a1e 426020 56772c 6e9335 83ad48 a0c85c b8e07a efffb2', '.#...#./.#...#./###.###/.#.#.#./...#.../..###../...#...'),
    'banner': ('3d271b 532d13 6b3a10 884e16 ab651c cb8327 e4a637 f0c050 ffdb7c ffefb0', '.####/.###./.####/.#.../.#...'),
}


def mark(canvas, rows, colors, origin, kind):
    left, top = origin
    points = { (left + column, top + row_index)
               for row_index, row in enumerate(rows.replace(' ', '').split('/'))
               for column, value in enumerate(row) if value == '#' }
    effects = ((-1, 0), (0, -1), (1, 0), (0, 1), (1, 1))
    for point_x, point_y in sorted(points):
        for delta_x, delta_y in effects:
            point = point_x + delta_x, point_y + delta_y
            if point in points or not canvas.getpixel(point)[3]:
                continue
            if kind == 'rune':
                canvas.putpixel(point, colors[2 if delta_x < 0 or delta_y < 0 else 1])
            elif kind == 'stone' and canvas.getpixel(point) in colors[4:9]:
                canvas.putpixel(point, colors[3 if delta_x > 0 or delta_y > 0 else 5])
            elif kind == 'source' and canvas.getpixel(point) in colors[3:9]:
                canvas.putpixel(point, colors[2])
    for point_x, point_y in points:
        point = point_x, point_y
        assert canvas.getpixel(point)[3], (kind, rows, point)
        highlight = (point_x, point_y - 1) not in points
        shade = 10 if kind == 'rune' and highlight else 9 if kind == 'stone' or highlight else 8
        canvas.putpixel(point, colors[shade])


def sprites():
    groups = [[(name, paint(rows, palette(values))) for name, (rows, values) in MATERIALS.items()]]
    groups.append([])
    for index, (name, (values, rows, left, top)) in enumerate(SOURCES.items()):
        colors = palette(values) + (GOLD if index < 3 else IRON)
        canvas = paint(SOURCE, colors)
        mark(canvas, rows, colors, (left, top), 'source')
        groups[-1].append(('source_' + name, canvas))
    groups.append([])
    for name, (values, rows) in RUNES.items():
        colors = palette(values)
        canvas = paint(RUNE, colors)
        mark(canvas, rows, colors, (4, 4), 'rune')
        groups[-1].append(('rune_' + name, canvas))
    groups.append([])
    for name, (values, rows) in STONES.items():
        colors = palette(values) + SETTING
        canvas = paint(STONE, colors)
        mark(canvas, rows, colors, (4 if name == 'volley' else 5, 5), 'stone')
        groups[-1].append(('stone_' + name, canvas))
    return groups


def main():
    groups = sprites()
    assert tuple(map(len, groups)) == (5, 6, 13, 7)
    report = {}
    for group_index, group in enumerate(groups):
        if group_index:
            assert len({canvas.getchannel('A').tobytes() for _, canvas in group}) == 1
        for name, canvas in group:
            colors = {pixel[:3] for pixel in canvas.getdata() if pixel[3]}
            alpha = sorted(set(canvas.getchannel('A').getdata()))
            bounds = canvas.getbbox()
            span = max(bounds[2] - bounds[0], bounds[3] - bounds[1])
            assert canvas.size == (16, 16) and alpha == [0, 255] and 13 <= span <= 15
            assert 14 <= len(colors) <= 24, (name, len(colors))
            path = HERE / (name + '.png')
            canvas.save(path)
            report[name] = {'size': list(canvas.size), 'opaque_rgb': len(colors), 'alpha': alpha,
                            'bbox_xyxy_exclusive': list(bounds), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    result = Image.new('RGBA', (3840, 384))
    with Image.open(HERE.parent / 'raw' / 'ref_style.png') as reference:
        for row, (group, ref_index) in enumerate(zip(groups, (3, 0, 6, 8))):
            left = 64 + 128 * ref_index
            ref = reference.crop((left, 64, left + 64, 128)).resize((16, 16), Image.Resampling.NEAREST)
            for column, (_, icon) in enumerate([*group, ('reference', ref)]):
                result.paste(icon.resize((96, 96), Image.Resampling.NEAREST), (column * 288, row * 96))
    result.save(HERE / 'preview.png')
    (HERE / 'validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'Validated {len(report)} sprites; preview {result.size}')


if __name__ == '__main__':
    main()
