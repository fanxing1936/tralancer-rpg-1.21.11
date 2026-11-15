#!/usr/bin/env python3
"""教皇 M1：解码 GIF 真实帧时间、导出原帧和带时间联系表；不生成模型或动作。"""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent / 'pope_ref'
OUT = ROOT / 'm1' / 'motion'
SOURCES = {
    'idle': 'MCD_Arch-Illager_Idle.gif',
    'idle_front': 'MCD_Arch-Illager_Idle_Highblock_Halls_(front_view).gif',
    'walk': 'MCD_Arch-Illager_Run.gif',
    'attack': 'MCD_Arch-Illager_Basic_Attack.gif',
    'summon': 'MCD_Arch-Illager_Summon_Circle.gif',
    'cast': 'MCD_Arch-Illager_Summon_Single.gif',
    'appear': 'MCD_Arch-Illager_Appear.gif',
    'teleport': 'MCD_Arch-Illager_Teleport_(Appear_Short).gif',
    'whirlwind_game': 'MCD_Arch-Illager_Defeated_in_a_Whirlwind_in_game.gif',
    'whirlwind_full': 'MCD_Arch-Illager_Defeated_in_a_Whirlwind.gif',
}

def font(size):
    p = Path('C:/Windows/Fonts/msyh.ttc')
    return ImageFont.truetype(str(p), size) if p.exists() else ImageFont.load_default()

def board(key, frames, times, selected, suffix='contact', crop=None):
    cols = 5
    cell_w, cell_h = 270, 300
    canvas = Image.new('RGB', (cols*cell_w, 65+((len(selected)+cols-1)//cols)*cell_h), '#ece9df')
    d = ImageDraw.Draw(canvas)
    d.text((15,10), key+' 原作 GIF 抽帧（非本项目模型）', font=font(23), fill='#18222b')
    for j, i in enumerate(selected):
        im = frames[i].copy()
        if crop: im = im.crop(crop)
        im.thumbnail((cell_w-12, cell_h-52), Image.Resampling.LANCZOS)
        x,y = (j%cols)*cell_w,65+(j//cols)*cell_h
        bg=Image.new('RGBA', (cell_w-8,cell_h-48),'#35404b')
        bg.alpha_composite(im,((bg.width-im.width)//2,(bg.height-im.height)//2))
        canvas.paste(bg.convert('RGB'),(x+4,y))
        d.text((x+10,y+cell_h-45),f'帧 {i:03d}   {times[i]:.3f} 秒',font=font(18),fill='#18222b')
    path=OUT/(key+'_'+suffix+'.jpg')
    canvas.save(path,quality=93)
    return str(path.relative_to(ROOT))

def write_report(meta):
    authored=OUT/'clips.json'
    if not authored.exists(): return
    spec=json.loads(authored.read_text(encoding='utf-8'))
    lines=['# 教皇 M1：动作来源、时间与关键姿态', '',
        '本报告只做原始素材分析，没有制作 `pope.bbmodel`、最终关键帧、mcfunction 或 sockets。所有图均为原作 GIF 的解码帧，不是本项目模型渲染，不能用于声称还原度已通过。建议时长与候选出手点尚未获得阶段批准，M3 应在静态模型获批后用最终骨架重做同一时刻并排对照。', '',
        '## 证据与时间定义', '',
        '- 来源：[Arch-Illager 图库](https://minecraft.wiki/w/Dungeons:Arch-Illager/Gallery)、[行为说明](https://minecraft.wiki/w/Dungeons:Arch-Illager)。文件实际来源、校验值见上级 `SOURCES.md`、`source_manifest.json`。',
        '- `source_time_seconds` 从 GIF 第 0 帧起，逐帧累加真实 `duration`。GIF 编码长度不等于动画动作长度；尾帧停留、重复帧、透明尾段都单独说明。',
        '- `proposed_clip_time_seconds` 是待批准的本项目 clip 时间，按 0.05 秒烘焙格点给出候选；不是已经写进动画的值。',
        '- 原始帧号从 0 开始。PNG 保持原画布、颜色和透明度；联系表只为展示增加灰色衬底、标签和缩略。`*_detail.jpg` 对所有帧使用同一透明包围盒裁切，位移关系仍保留。',
        '- GIF 没有游戏事件轨道，attack / summon / cast 的“出手”仅指可见姿态候选。没有从画面凭空制造三连发事件，也没有借行为页的延时参数冒充动画关键帧。',
        '- 各 GIF 自带旋转/变色的杖顶。旋转可由独立发光骨骼实现；变色没有现成材质动画证据，本阶段不承诺实现。', '',
        '## 素材编码校验', '',
        f'共 {len(meta)} 个 GIF，{sum(v["frame_count"] for v in meta.values())} 帧；全部帧已解码为 PNG，并记录在 `gif_timing.json`。除 Run 每帧 30ms 外，本组其余文件每帧均为 40ms。', '',
        '| 来源代号 | 原文件 | 分辨率 | 帧数 | 编码时长（秒） | 首末像素相同 |',
        '|---|---|---|---:|---:|---|']
    for key,m in meta.items():
        lines.append(f'| {key} | `{m["file"]}` | {m["width"]}×{m["height"]} | {m["frame_count"]} | {m["duration_seconds"]:.2f} | {"是" if m["endpoint_pixels_equal"] else "否"} |')
    lines += ['', '## 持杖手与结构证据', '',
        '**权杖由角色左手持有。** `idle_front` 正面帧 0 / 25 / 50 / 75 / 100，权杖始终位于画面右侧；普通 idle 与 attack 的连续运动一致。骨骼必须按角色身体左右命名，不能把画面右侧误写成 `right_hand`。本项目 Java 坐标约定中，角色左侧为 -X。', '',
        '![正面持杖证据](idle_front_contact.jpg)', '',
        'whirlwind_game 第 84 帧（3.36 秒）能直接看见皇冠与头部之间的空隙；权杖早在第 3 帧（0.12 秒）已和持握手分离。皇冠、权杖必须能独立于头/左手运动。', '',
        '[查看 3.36 秒原始掉冠帧](frames/whirlwind_game/0084.png)', '',
        '## 9 段接口与时长建议（未锁定）', '',
        '| ID | clip | 循环 | 证据 | GIF 编码长度（秒） | 建议 clip（秒） | 候选出手（clip 秒） |',
        '|---:|---|---|---|---:|---:|---|']
    for c in spec['clips']:
        release='、'.join(f'{r["proposed_clip_time_seconds"]:.2f}' for r in c.get('release_candidates',[])) or '—'
        lines.append(f'| {c["id"]} | `{c["name"]}` | {"是" if c["loop"] else "否"} | {c["evidence"]} | {c["source_gif_duration_seconds"]:.2f} | {c["proposed_clip_duration_seconds"]:.2f} | {release}（候选） |')
    lines += ['', '## 关键姿态表', '']
    for c in spec['clips']:
        lines += [f'### {c["id"]} / {c["name"]}', '',f'**证据：{c["evidence"]}。** {c["note"]}', '',
            f'源片段：{c["source_range_seconds"][0]:.2f}–{c["source_range_seconds"][1]:.2f} 秒；建议 clip 长度：{c["proposed_clip_duration_seconds"]:.2f} 秒。', '',
            '| 原 GIF 帧 | 原 GIF 秒 | 建议 clip 秒 | 观察到的姿态 / 推断 |', '|---:|---:|---:|---|']
        for p in c['key_poses']:
            frame='—' if p['source_frame'] is None else str(p['source_frame'])
            source='—' if p['source_time_seconds'] is None else f'{p["source_time_seconds"]:.2f}'
            lines.append(f'| {frame} | {source} | {p["proposed_clip_time_seconds"]:.2f} | {p["pose"]} |')
        for r in c.get('release_candidates',[]):
            lines += ['',f'出手候选：原 GIF {r["source_time_seconds"]:.2f} 秒 → clip {r["proposed_clip_time_seconds"]:.2f} 秒。**{r["status"]}。**']
        lines += ['',f'![{c["name"]} 原作关键姿态]({c["name"]}_keyposes.jpg)', '']
    lines += ['## 必须在后续阶段明确的差异', '',
        '1. **登场剪裁。** Appear 的 9.96 秒文件并非只包含入场：可见内容结束于帧166（6.64秒），167–248全透明；中间还有举杖、前压和离场。建议只取0–1.80秒落定，不能直接把整个文件当登场 clip。',
        '2. **瞬移来源与时长。** Teleport GIF 本身包含进入和离开，不必无证据地倒放进入。建议入场源0–1.20秒压到0.90秒，离场源1.20–2.12秒压到0.90秒。帧52（2.08秒）仍有少量像素，53–134全透明。图库说明“appear缩短版”和行为页“in/out各0.9秒”只支持动作来源与目标时长，不提供精确切点，以上切点属于适配推断。',
        '3. **瞬移的视觉大小与隐藏。** 源图出现由小到大、离场由大到小的变化。仅从截图不能证明这是原作scale轨道、深度运动或渲染机制造成；现有模型通道仅rotation/position，不能声称实现了同样的缩放或完全透明。不得暗中加入scale/Molang、半透明效果。',
        '4. **whirlwind结尾。** game末帧6.40秒和full末帧7.96秒的人物都仍可见，未观测到所有部件缩成一个点。建议game段之后0.60秒收拢是为项目交接补作，必须标“推断”。刚性部件中心重叠不会使体积消失，尤其整根权杖仍有长度；末帧交接/移除的实现边界需和玩法方约定，本任务不写玩法。',
        '5. **首尾过渡。** 非循环动作当前共享管线会回idle。teleport_out / whirlwind不能仅靠最后一帧当作永久隐藏或姿态保持，M4需验证约定的结束交接，不能用“构建通过”替代验证。',
        '6. **未验证项。** 未制作实际模型、未做模型与原作并排、未在Blockbench摆动画、未测sockets、未在真实游戏内看过。M1图只支持关键姿态和来源分析。', '',
        '## 可复现命令', '', '```powershell', 'python _tools/pope_motion_study.py', '```', '',
        '`clips.json` 是本阶段人工观察记录；脚本读取它生成关键姿态联系表和本报告。所有真实动画以后以 `pope.bbmodel` 为事实来源，本JSON不得冒充最终动画数据。', '']
    (OUT/'MOTION_STUDY.md').write_text('\n'.join(lines),encoding='utf-8')

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    result={}
    for key, name in SOURCES.items():
        p=ROOT/name
        if not p.exists():
            print('缺少 '+name)
            continue
        im=Image.open(p)
        frames=[]; rows=[]; times=[]; t=0
        out=OUT/'frames'/key
        out.mkdir(parents=True,exist_ok=True)
        for i in range(im.n_frames):
            im.seek(i)
            duration=im.info.get('duration')
            if duration is None: raise ValueError(f'{name} 帧 {i} 没有 duration，禁止猜测')
            frame=im.convert('RGBA').copy()
            frame.save(out/f'{i:04d}.png')
            frames.append(frame);times.append(t/1000)
            rows.append({'frame':i,'start_ms':t,'duration_ms':duration,'end_ms':t+duration,'path':str((out/f'{i:04d}.png').relative_to(ROOT)).replace('\\','/')})
            t+=duration
        selected=sorted(set(round(j*(len(frames)-1)/19) for j in range(20)))
        contact=board(key,frames,times,selected)
        boxes=[f.getbbox() for f in frames if f.getbbox()]
        bounds=[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)]
        visible=[i for i,f in enumerate(frames) if f.getbbox()]
        result[key]={'file':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'width':im.width,'height':im.height,'frame_count':len(frames),'duration_ms':t,'duration_seconds':t/1000,'loop':im.info.get('loop'),'contact_sheet':contact,'contact_frames':selected,'visible_frame_range':[visible[0],visible[-1]],'alpha_union_box':bounds,'endpoint_pixels_equal':frames[0].tobytes()==frames[-1].tobytes(),'frames':rows}
        if key in ('teleport','appear'):
            board(key,frames,times,list(range(0,55,3)),'detail',bounds)
        elif key=='cast':
            board(key,frames,times,list(range(0,63,3)),'detail',bounds)
        elif key.startswith('whirlwind'):
            board(key,frames,times,selected,'detail',bounds)
        authored=OUT/'clips.json'
        if authored.exists():
            for clip in json.loads(authored.read_text(encoding='utf-8'))['clips']:
                if clip['source_key']==key:
                    indices=[p['source_frame'] for p in clip['key_poses'] if p.get('source_frame') is not None]
                    board(clip['name'],frames,times,indices,'keyposes',bounds)
        print(key,len(frames),t/1000,'秒')
    (OUT/'gif_timing.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    write_report(result)

if __name__=='__main__': main()
