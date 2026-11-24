"""Export generated artwork to native pixels; never transforms original game art."""
from pathlib import Path
from collections import Counter
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent


def export(spec):
    source_path = Path(spec['source'])
    if not source_path.is_absolute():
        source_path = HERE / source_path
    source = Image.open(source_path).convert('RGBA')
    bbox = source.getchannel('A').point(lambda a: 255 if a >= 128 else 0).getbbox()
    cropped = source.crop(bbox)
    scale = 14 / max(cropped.size)
    size = tuple(max(1, round(n * scale)) for n in cropped.size)
    if 'sample_size' in spec:
        size = tuple(spec['sample_size'])
        assert len(size) == 2 and all(isinstance(n, int) and 1 <= n <= 14 for n in size)
    phase = spec.get('sampling_phase', [0, 0])
    palette = [tuple(bytes.fromhex(c.lstrip('#'))) for c in spec['palette']]
    native = Image.new('RGBA', (16, 16))
    ox, oy = ((16 - n) // 2 for n in size)
    for y in range(size[1]):
        for x in range(size[0]):
            sx = max(0, min(cropped.width-1, int((x+.5+phase[0])*cropped.width/size[0])))
            sy = max(0, min(cropped.height-1, int((y+.5+phase[1])*cropped.height/size[1])))
            pixel = cropped.getpixel((sx, sy))
            if pixel[3] < 128:
                continue
            color = min(palette, key=lambda p: sum((p[k]-pixel[k])**2 for k in range(3)))
            native.putpixel((ox+x, oy+y), color+(255,))
    native.save(HERE / (spec['id'] + '.png'))
    return validate(spec, bbox, list(source.size))


def validate(spec, source_bbox=None, source_size=None):
    path = HERE / (spec['id'] + '.png')
    im = Image.open(path).convert('RGBA')
    alpha = Counter(im.getchannel('A').get_flattened_data())
    colors = Counter(p[:3] for p in im.get_flattened_data() if p[3])
    allowed = {tuple(bytes.fromhex(c.lstrip('#'))) for c in spec['palette']}
    assert im.size == (16, 16)
    assert set(alpha) == {0, 255}
    assert set(colors) <= allowed
    assert len(colors) <= (3 if spec['title'] else 32)
    assert (0, 0, 0) not in colors
    if spec['id'] == 'sin_shard':
        assert all(r == g == b for r, g, b in colors)
    return dict(id=spec['id'], size=list(im.size), colors=len(colors),
                alpha=sorted(alpha), opaque_pixels=alpha[255], bbox=im.getbbox(),
                source_bbox=source_bbox, source_size=source_size,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def preview(specs):
    font_path = 'C:/Windows/Fonts/msyh.ttc'
    font = ImageFont.truetype(font_path, 17)
    small = ImageFont.truetype(font_path, 12)
    columns, cw, ch = 6, 184, 225
    board = Image.new('RGB', (columns*cw, 3*ch+65), '#191D25')
    draw = ImageDraw.Draw(board)
    draw.text((16, 12), '世界掉落与锻造 · 原图优先 / 新绘原生16×16', font=font, fill='#F0E8D5')
    order = ['elite_badge','sin_shard','blueprint_fragment','blueprint_epic','blueprint_legend','star_fragment',
             'wind_essence','abyss_tear','molten_core','mountain_heart','temple_bronze','grave_soil',
             'title_gate','title_ledger','title_waverer','title_grandmaster','title_meteor','title_merchant']
    by_id = {s['id']: s for s in specs}
    for i, name in enumerate(order):
        x, y = i % columns*cw, i // columns*ch+65
        original = name == 'blueprint_fragment'
        label = '图纸碎片 · 原图' if original else by_id[name]['name']
        path = HERE/'dungeons/T_Paper_Graph_02.png' if original else HERE/(name+'.png')
        icon = Image.open(path).convert('RGBA')
        side = icon.width * (4 if original else 8)
        draw.rectangle((x+8,y,x+cw-8,y+135), fill='#303643')
        board.paste(icon.resize((side,side),Image.Resampling.NEAREST),(x+(cw-side)//2,y+3),icon.resize((side,side),Image.Resampling.NEAREST))
        draw.text((x+10,y+141),label,font=font,fill='#EFE7D9')
        draw.rectangle((x+10,y+170,x+cw-10,y+202),fill='#D7CBAF')
        board.paste(icon,(x+25,y+170),icon)
        if not original:
            board.paste(icon.resize((32,32),Image.Resampling.NEAREST),(x+60,y+170),icon.resize((32,32),Image.Resampling.NEAREST))
            if name.startswith('title_'):
                tiny=icon.resize((8,8),Image.Resampling.NEAREST)
                board.paste(tiny,(x+112,y+181),tiny)
        draw.text((x+10,y+206),'原图32×32 · 未缩放' if original else '16×16 · 原尺寸 / 2倍',font=small,fill='#AAB6C7')
    board.save(HERE/'PREVIEW.png')


if __name__ == '__main__':
    specs = json.loads((HERE/'generation_manifest.json').read_text(encoding='utf-8'))
    rows = [export(s) for s in specs]
    (HERE/'validation.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    preview(specs)
    print(json.dumps([dict(id=r['id'],colors=r['colors'],opaque=r['opaque_pixels']) for r in rows]))
