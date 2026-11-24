"""Export only the eleven elite-affix glyphs; original game references remain untouched."""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont
from export_native import export

HERE=Path(__file__).resolve().parent


def preview(specs):
    font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',17)
    small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',12)
    tiny_font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',9)
    cw,ch,cols=184,238,6
    board=Image.new('RGB',(cw*cols,2*ch+68),'#191D25')
    d=ImageDraw.Draw(board)
    d.text((15,12),'精英词缀 · 16×16原图 / 8像素字号检查',font=font,fill='#F1E8D5')
    d.text((15,40),'每张2–3色 · 指定主色 · Alpha 0/255 · 所有放大均为最近邻',font=small,fill='#AAB6C7')
    for i,s in enumerate(specs):
        x,y=(i%cols)*cw,68+(i//cols)*ch
        im=Image.open(HERE/(s['id']+'.png')).convert('RGBA')
        tiny=im.resize((8,8),Image.Resampling.NEAREST)
        d.rectangle((x+8,y,x+176,y+132),fill='#303643')
        big=im.resize((128,128),Image.Resampling.NEAREST)
        board.paste(big,(x+28,y+2),big)
        d.text((x+12,y+138),s['name'],font=font,fill=s['main'])
        d.text((x+76,y+143),s['main'],font=small,fill='#AAB6C7')
        d.rectangle((x+10,y+166,x+174,y+211),fill='#D7CBAF')
        board.paste(im,(x+18,y+177),im)
        board.paste(tiny,(x+48,y+181),tiny)
        d.text((x+60,y+177),'僵尸',font=tiny_font,fill='#37343B')
        zoom=tiny.resize((32,32),Image.Resampling.NEAREST)
        board.paste(zoom,(x+127,y+172),zoom)
        d.text((x+12,y+215),'16px / 8px名牌 / 8px放大',font=small,fill='#AAB6C7')
    board.save(HERE/'AFFIX_PREVIEW.png')


def main():
    specs=json.loads((HERE/'affix_generation_manifest.json').read_text(encoding='utf-8'))
    assert len(specs)==11
    rows=[]
    for s in specs:
        row=export(s)
        im=Image.open(HERE/(s['id']+'.png')).convert('RGBA')
        counts={}
        for p in im.get_flattened_data():
            if p[3]: counts[p[:3]]=counts.get(p[:3],0)+1
        main=tuple(bytes.fromhex(s['main'][1:]))
        assert main in counts, s['id']+' missing exact main color'
        assert 2<=len(counts)<=3
        assert not any(im.getpixel((x,y))[3] for x,y in [(j,0) for j in range(16)]+[(j,15) for j in range(16)]+[(0,j) for j in range(16)]+[(15,j) for j in range(16)])
        row.update(main_color=s['main'],main_color_pixels=counts[main],sampling_phase=s.get('sampling_phase',[0,0]),sample_size=s.get('sample_size'))
        rows.append(row)
    (HERE/'affix_validation.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    preview(specs)
    print(json.dumps([dict(id=r['id'],colors=r['colors'],main_pixels=r['main_color_pixels'],opaque=r['opaque_pixels']) for r in rows]))


if __name__=='__main__':
    main()
