"""Build a portable review page with paired GIF and Blockbench frames."""

from html import escape

from PIL import Image, ImageDraw, ImageFont

from author import HERE, MODEL, read, sha
from preview import BG, FONT


LABELS = {
    'idle': '待机', 'walk': '行走', 'appear': '登场', 'death': '倒地',
    'forward_strike': '前冲重拳', 'fury_fist': '狂拳连击', 'launch': '跃起回场',
    'lightning_slam': '雷霆砸地', 'overcharge': '过载蓄力', 'hurt': '失衡受击', 'summon': '召唤',
}
EVENTS = {
    'landing': '登场落地', 'fall': '俯卧落定', 'strike': '最大前伸', 'first_forward_reach': '首轮前伸',
    'first_turning_reach': '首轮转身伸拳', 'second_first_reach': '次轮前伸', 'second_wide_reach': '次轮张臂',
    'second_turning_reach': '次轮转身伸拳', 'slam': '砸地', 'off_frame_begin': '离开画面',
    'return_landing': '回场落地', 'jump': '离地', 'charge_hold': '举拳蓄力',
    'recoil': '后仰失衡', 'raised_fists': '双拳举起',
}
NOTES = {
    'idle': '看后撤步拳架、抬肩和披风末段起伏。',
    'walk': '看交替支撑、摆臂方向以及循环接回首帧。',
    'appear': '原作 0–0.250 秒透明。模型用向上出画再落下复现；真实游戏显隐留待接入验证。',
    'death': '看失衡、几次撑起和最后俯卧，尤其是双拳、帽顶与披风的地面关系。',
    'forward_strike': '右拳出击时沿手臂长轴伸长，拳臂同时加粗。打开缩放对照查看出拳前后。',
    'fury_fist': '看两轮连击之间的收势，以及最后跃起再用双拳砸地。',
    'launch': '原作 1.130–2.210 秒全透明。模型离开固定镜头后回场，局部图保留画面空白。',
    'lightning_slam': '整幅图保留高跳和下坠的幅度。缩放对照用相同比例展示触地时拳臂的放大与回收。',
    'overcharge': '看生物左拳（站在角色自身角度）竖举、右拳压低。GIF 不给出电波的实际触发帧。',
    'hurt': '看先折身再后仰失衡、错步与回正。',
    'summon': '看前探、仰身举拳和再次回落。双拳举起是姿态锚点。',
}
CSS = '''
:root{color-scheme:dark;background:#171e28;color:#eaf0f8;font:16px/1.6 "Microsoft YaHei",sans-serif}
body{max-width:1100px;margin:auto;padding:24px} h1,h2,p{margin:.45em 0} h1{font-size:2rem} h2{font-size:1.5rem}
a{color:#94def1} a:focus-visible,summary:focus-visible{outline:2px solid #f4d08a;outline-offset:3px}
nav{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0} nav a{padding:4px 10px;background:#263348;border-radius:5px;text-decoration:none}
section{padding:18px 0 26px;border-top:1px solid #45536a} section img{display:block;width:100%;height:auto;max-width:960px}
.tag{font-weight:normal;color:#c0d3e6;font-size:.9rem;margin-left:.6em} .muted{color:#c0ccdc}
.options{display:flex;flex-wrap:wrap;gap:16px}.options details{flex:1 0 240px;margin-top:12px}
.options details[open]{flex-basis:100%} summary{cursor:pointer;color:#94def1}
.options .movie{width:auto;max-width:100%;margin-top:6px}
footer{border-top:1px solid #45536a;padding:1rem 0;overflow-wrap:anywhere}.out{color:#f4d08a}
'''


def build():
    meta = read(HERE/'clipmeta.json')
    validation = read(HERE/'validation.json')
    assert meta['model_sha256'] == validation['model_sha256'] == sha(MODEL)
    clips = meta['clips']
    evidence = read(HERE/'preview/render_evidence.json')['clips']
    playback = read(HERE/'preview/playback_evidence.json')
    assert playback['model_sha256'] == sha(MODEL)
    nav = ''.join(f'<a href="#{c["name"]}">{c["id"]+1:02d} {LABELS[c["name"]]}</a>' for c in clips)
    sections = []
    overview = Image.new('RGB', (1280, 72 + 228*((len(clips)+1)//2)), BG)
    draw = ImageDraw.Draw(overview)
    draw.text((16,10),'首席附魔师 · 11 段动作代表帧',font=ImageFont.truetype(FONT,26),fill='white')
    draw.text((17,47),'每组左侧：原作 GIF   ｜   右侧：同一时刻的 Blockbench 模型',
              font=ImageFont.truetype(FONT,17),fill='#c5d5e6')
    for c in clips:
        n = c['name']
        src = f'../originals/{escape(c["gif"], quote=True)}'
        first = f'preview/{n}'
        x, y = (c['id']%2)*640, 72+(c['id']//2)*228
        draw.line((x,y,x+639,y), fill='#536177')
        draw.text((x+16,y+6),f'{c["id"]+1:02d} {LABELS[n]} · {n}',
                  font=ImageFont.truetype(FONT,19),fill='white')
        with Image.open(HERE/first/'featured.jpg') as featured:
            overview.paste(featured.crop((0,64,960,353)).resize((640,193), Image.Resampling.LANCZOS),(x,y+32))
        compare = [('整幅时序对照', 'keyframes.jpg'), ('局部放大对照', 'details.jpg'), ('模型侧面与背面', 'side_back.jpg')]
        if c['scale_bones']:
            compare.insert(0, ('肢体放大前后对照', 'scale_comparison.jpg'))
        links = ' · '.join(f'<a href="{first}/{file}">{label}</a>' for label, file in compare)
        movie = f'{first}/playback.webp'
        assert sha(HERE/movie) == playback['clips'][n]['sha256']
        # The motion loop loads only when explicitly requested.
        options = (f'<details data-movie="{movie}"><summary>并排播放整段动作</summary>'
                   f'<noscript><a href="{movie}">打开并排动图</a></noscript></details>')
        for label, file in compare:
            with Image.open(HERE/first/file) as image:
                width, height = image.size
            options += (f'<details><summary>{label}</summary><a href="{first}/{file}">'
                        f'<img loading="lazy" src="{first}/{file}" width="{width}" height="{height}" alt="{n} {label}"></a></details>')
        cues = '；'.join(f'{EVENTS[q["event"]]} {q["start_ms"]/1000:.3f} 秒（第 {q["suggested_tick"]} tick）' for q in c['cues'])
        e = evidence[n]
        blank = ''
        if e['source_blank_samples']:
            assert e['model_blank_samples'] == e['source_blank_samples']
            full = playback['clips'][n]['source_blank_frames']
            blank = f'<p class="muted">已逐帧核对 f{full[0]}–{full[-1]} 的 {len(full)} 个空白源帧；模型画面也为空。</p>'
        sections.append(f'''<section id="{n}">
<h2>{c['id']+1:02d} {LABELS[n]} <span class="tag">{n} · 有动图</span></h2>
<p class="muted">GIF {c['source_duration_ms']/1000:.3f} 秒 · 动作 {c['length']:.2f} 秒（{c['ticks']} tick） · {'循环' if c['loop'] else '单次'} · {e['samples']} 组对照</p>
<p>{NOTES[n]}</p>{blank}
{f'<p>姿态锚点：{cues}</p>' if cues else ''}
<a href="{first}/featured.jpg"><img src="{first}/featured.jpg" loading="lazy" width="960" height="358" alt="{LABELS[n]}的代表帧，原作 GIF 和模型并排"></a>
<p>{links} · <a href="{movie}">并排动图</a> · <a href="{src}">原作 GIF</a></p>
<div class="options">{options}</div>
</section>''')
    total = sum(v['comparison_pairs'] for v in validation['clips'])
    doc = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>首席附魔师 · M3 动作对照</title><style>{CSS}</style></head>
<body><h1>首席附魔师 · M3 动作对照</h1>
<p>11 段动作由 Astra Ultra 按原作 GIF 重新摆姿。下面先看各段代表帧，再展开完整对照。左边是原作，右边是 Blockbench 在同一时间渲染的模型，共 {total} 组。</p>
<p class="muted">整幅对照在每段内固定机位，保留位移与空帧；局部放大便于核对肢体，不能用来判断移动距离。侧面与背面用于检查模型，原作 GIF 没有对应机位。</p>
<p><a href="../prime_enchanter.bbmodel">Blockbench 模型</a> · <a href="../M3_REVIEW.md">时长与制作报告</a> · <a href="../sockets.json">挂点数据</a> · <a href="../SOURCES.md">素材来源与署名</a></p>
<nav aria-label="跳到动作">{nav}</nav>
{''.join(sections)}
<footer><p class="out">未在真实游戏内看过。时刻仅按 GIF 姿态标注；实际技能触发、显示控制和接入属后续工作。</p>
<p class="muted">模型 SHA-256：{meta['model_sha256']}</p></footer>
<script>
document.querySelectorAll('details[data-movie]').forEach(d=>d.addEventListener('toggle',()=>{{
  if(!d.open){{d.querySelector('img')?.remove();return;}}
  const img=document.createElement('img');img.className='movie';img.alt='原作与模型并排播放';img.src=d.dataset.movie;d.append(img);
}}));
</script></body></html>'''
    (HERE/'index.html').write_text(doc, encoding='utf-8')
    overview.save(HERE/'overview.jpg', quality=92, subsampling=0)


if __name__ == '__main__':
    build()
