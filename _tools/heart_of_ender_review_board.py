"""M3 对照页排版：仅最近邻缩放、合成灰底和标签，不修改参考或渲染内容。"""
from __future__ import annotations
import argparse
import html
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from heart_of_ender_blockbench import REF

BG=(55,60,70,255)

def font(size):
    return ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',size)

def fit(image, size):
    im=image.convert('RGBA')
    w,h=size
    factor=min(w/im.width,h/im.height)
    scaled=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.NEAREST)
    out=Image.new('RGBA',size,BG)
    out.alpha_composite(scaled,((w-scaled.width)//2,(h-scaled.height)//2))
    return out

def resolve(path):
    p=(REF/path).resolve()
    if not p.is_relative_to(REF.resolve()):raise ValueError('图像路径越界')
    return p

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('index',type=Path)
    args=ap.parse_args()
    index=json.loads(args.index.read_text('utf8'))
    output=REF/'m3_preview/boards'
    output.mkdir(parents=True,exist_ok=True)
    written=[]
    for section in index['sections']:
        rows=section['pairs']
        for page,start in enumerate(range(0,len(rows),6),1):
            chunk=rows[start:start+6]
            canvas=Image.new('RGBA',(1040,100+math.ceil(len(chunk)/2)*336),BG)
            d=ImageDraw.Draw(canvas)
            d.text((16,8),section['title']+f'  {page}/{math.ceil(len(rows)/6)}',font=font(24),fill='white')
            d.text((16,48),section.get('subtitle','左：来源；右：保存模型的 Blockbench 原生渲染'),font=font(17),fill=(212,217,225))
            for i,row in enumerate(chunk):
                x=8+(i%2)*516;y=100+(i//2)*336
                d.text((x+4,y),row['label'],font=font(17),fill='white')
                d.text((x+4,y+28),row.get('source_label','参考图'),font=font(15),fill=(197,200,207))
                d.text((x+260,y+28),row.get('model_label','Blockbench'),font=font(15),fill=(197,200,207))
                for col,key in enumerate(('source','model')):
                    im=Image.open(resolve(row[key]))
                    if row.get(key+'_crop'):im=im.crop(row[key+'_crop'])
                    canvas.alpha_composite(fit(im,(250,250)),(x+col*256,y+55))
                if row.get('note'):d.text((x+4,y+307),row['note'],font=font(14),fill=(230,190,140))
            name=f"{section['id']}_{page:02d}.png"
            canvas.convert('RGB').save(output/name)
            written.append({'section':section['id'],'title':section['title'],'file':'boards/'+name})
    seen=set();links='';nav=[]
    for x in written:
        anchor=''
        if x['section'] not in seen:
            seen.add(x['section']);anchor=f' id="{x["section"]}"'
            nav.append(f'<a href="#{x["section"]}">{html.escape(x["title"])}</a>')
        links+=f'<figure{anchor}><figcaption>{html.escape(x["title"])}</figcaption><a href="{x["file"]}"><img loading="lazy" src="{x["file"]}"></a></figure>'
    movies='<h2>连续预览（12.5 fps）</h2>'+''.join(f'<details><summary>{name}</summary><img loading="lazy" src="{name}.gif"></details>' for name in ('idle','walk','mortar','cross_beam','sink','rise','death'))
    page='''<!doctype html><meta charset="utf-8"><title>Heart of Ender M3 动作对照</title>
<style>body{background:#20242a;color:#eee;font:17px system-ui;max-width:1120px;margin:32px auto;padding:0 20px}a{color:#cfa5ff}img{max-width:100%;display:block;margin:12px 0}figure{margin:35px 0}h1{font-size:28px}p{line-height:1.65}</style>
<h1>Heart of Ender · M3 动作对照</h1><p>已选择 R2 静态造型。左边是原素材，右边从保存的 .bbmodel 经 Blockbench 真实时间轴渲染。灰底仅供查看；没有在渲染图上补画光晕。推断动作使用依据截图，不冒充同帧原作动画。</p>
<p><a href="../M3_REPORT.md">阶段报告与局限</a> · <a href="../heart_of_ender.bbmodel">模型源文件</a> · <a href="render_evidence.json">相机、时点与渲染证据</a></p>
<p>需要重点审阅：<a href="b_f015_options/comparison.png">待机 0.6 秒肢端位置/方向两方案</a>；<a href="f45_options/comparison.png">小人 Fourside 第45帧的两个深度方案</a>。主稿保留端点优先，F45暂选E1；都不冒称已取得原作隐藏骨骼。</p>
<a href="overview.png"><img src="overview.png" alt="七段动作关键姿态总览"></a>'''+movies+'<h2>逐关键姿态与正侧背</h2><p>'+' · '.join(nav)+'</p>'+links
    (REF/'m3_preview/index.html').write_text(page,encoding='utf8')
    (output/'index.json').write_text(json.dumps(written,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(f'已生成 {len(written)} 页原始素材/模型对照')

if __name__=='__main__':main()
