"""Latest-material M3 review: render all registered poses from bbmodel, never recolor old PNGs.

Only writes heart_of_ender_ref/m3_material_v3/motion_review. Reuses the read-only
CPU rasterizer; local extensions are camera following, inner isolation, and an
opaque ground volume. No Blockbench connection, game operation or model edits.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import html
import json
import math
from pathlib import Path
import re
from types import SimpleNamespace

import numpy as np
from PIL import Image, ImageDraw

import display_mob as dm
import heart_of_ender_material_preview as cpu

REF = Path(__file__).resolve().parent / 'heart_of_ender_ref'
OUT = REF / 'm3_material_v3/motion_review'
MODEL = REF / 'm3_material_v3/heart_of_ender_material_v3.bbmodel'
EXPECTED = 'af9f3fead3a0a57784288359a38b34fcc03ee6c22e78b7aef08b88d00858328d'
GENERATOR = Path(__file__).name
BG = tuple(cpu.BG)
CLIPS = ('idle', 'walk', 'mortar', 'cross_beam', 'sink', 'rise', 'death')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode('utf-8')


class Output:
    """Checkpoint ownership after each write so interrupted runs can resume safely."""
    def __init__(self):
        self.root = OUT.resolve()
        self.marker = self.root/'review_ownership.json'
        self.state = read(self.marker) if self.marker.exists() else {'generator': GENERATOR, 'files': {}}
        if self.state['generator'] != GENERATOR:
            raise ValueError('Another generator owns the output directory')
        self.root.mkdir(parents=True, exist_ok=True)
        self.marker.write_bytes(encoded(self.state))

    def write(self, name, data):
        path = (self.root/name).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError('Output path escaped exclusive directory')
        key = path.relative_to(self.root).as_posix()
        if path.exists() and sha(path) not in (self.state['files'].get(key), hashlib.sha256(data).hexdigest()):
            raise ValueError(f'Refusing to overwrite unrelated or manually edited file: {path}')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        self.state['files'][key] = hashlib.sha256(data).hexdigest()
        self.marker.write_bytes(encoded(self.state))


def add_ground(model, ground_y):
    # Appending a temporary opaque texel row while extending UV resolution equally
    # leaves every original atlas texel and its UV lookup unchanged.
    h, w = model.atlas.shape[:2]
    if not np.array_equal(model.resolution, [w, h]):
        raise ValueError('Ground extension requires 1:1 atlas/UV resolution')
    row = np.broadcast_to(np.array([*BG, 255], np.uint8), (1, w, 4))
    atlas = np.concatenate((model.atlas, row), axis=0)
    faces = list(model.faces)
    for name in cpu.FACE_NAMES:
        faces.append(cpu.Face(cpu.face_corners([-200, ground_y-200, -200], [200, ground_y, 200], name),
                              np.array([0, h, 1, h+1], float), 'preview_ground/'+name))
    return cpu.Model(faces, atlas, np.array([w, h+1], float), model.evidence)


def filter_inner(model):
    return cpu.Model([f for f in model.faces if f.name.startswith('inner_')], model.atlas,
                     model.resolution, model.evidence)


def actual_camera(view, bones, clip, time):
    position = np.asarray(view['position'], float)
    target = np.asarray(view['target'], float)
    up = np.array([0., 1., 0.])
    follow = view.get('follow_bone')
    if follow:
        # Native Group matrix = dm_matrix * translate(pivot). The pivot translations
        # cancel in posedGroup * inverse(restGroup), so this is the same rigid delta.
        delta = np.asarray(dm.posed_matrix(bones, follow, clip, time)) @ np.linalg.inv(dm.bone_matrix(bones, follow))
        position = (delta @ np.r_[position, 1])[:3]
        target = (delta @ np.r_[target, 1])[:3]
        up = cpu.normalized(delta[:3, :3] @ up)
    if view.get('width', 500) != view.get('height_px', 500):
        raise ValueError('Registered review uses square frames')
    cam = cpu.camera(position-target, target, view['height'], view.get('width', 500), up)
    return cam, {'position': position.tolist(), 'target': target.tolist(), 'up': up.tolist()}


def visible_pixels(pixels):
    mask = np.any(pixels != np.array(BG), axis=2)
    ys, xs = np.where(mask)
    return {'visible_colored_pixels': int(mask.sum()),
            'visible_bbox_xyxy': [int(xs.min()), int(ys.min()), int(xs.max()+1), int(ys.max()+1)] if len(xs) else None,
            'touches_border': bool(mask[0].any() or mask[-1].any() or mask[:, 0].any() or mask[:, -1].any())}


def fit(im, size):
    im = im.convert('RGBA')
    ratio = min(size[0]/im.width, size[1]/im.height)
    im = im.resize((round(im.width*ratio), round(im.height*ratio)), Image.Resampling.NEAREST)
    out = Image.new('RGBA', size, (*BG, 255))
    out.alpha_composite(im, ((size[0]-im.width)//2, (size[1]-im.height)//2))
    return out.convert('RGB')


def mapped_image(path, generated):
    if path.startswith('m3_preview/'):
        relative = path.removeprefix('m3_preview/')
        if relative not in generated:
            raise ValueError(f'Review index references a model image not regenerated: {path}')
        return OUT/'frames'/relative, 'new_model'
    result = (REF/path).resolve()
    if not result.is_relative_to(REF.resolve()) or not result.exists():
        raise ValueError(f'Missing or unsafe original source: {path}')
    return result, 'original_reference'


def board_index(original, generated, output):
    written, source_files, review = [], {}, {'model_sha256': EXPECTED, 'sections': []}
    for section in original['sections']:
        title = section['title']
        is_views = section['id'].endswith('_views')
        subtitle = '全部为最新模型 · 固定相机正侧背 · 离线CPU，非BB、非游戏' if is_views else '左：原素材；右：最新模型 · 同刻或依据截图见标签 · 离线CPU，非BB、非游戏'
        normalized_rows = []
        for row in section['pairs']:
            normalized = dict(row)
            for key in ('source', 'model'):
                path, kind = mapped_image(row[key], generated)
                normalized[key] = path.relative_to(REF).as_posix()
                normalized[key+'_kind'] = kind
                if kind == 'original_reference':
                    source_files[path.relative_to(REF).as_posix()] = sha(path)
                label = row.get(key+'_label', '原素材' if kind == 'original_reference' else '离线CPU')
                if kind == 'new_model':
                    for previous in ('Blockbench', '原生模型', '保存模型', '模型'):
                        label = label.replace(previous, '离线CPU')
                normalized[key+'_label'] = label
            normalized_rows.append(normalized)
        review['sections'].append({'id': section['id'], 'title': title, 'subtitle': subtitle, 'pairs': normalized_rows})
        for page, start in enumerate(range(0, len(normalized_rows), 6), 1):
            chunk = normalized_rows[start:start+6]
            canvas = Image.new('RGB', (1040, 100+math.ceil(len(chunk)/2)*336), BG)
            draw = ImageDraw.Draw(canvas)
            draw.text((16, 8), title+f'  {page}/{math.ceil(len(normalized_rows)/6)}', font=cpu.font(24), fill='white')
            draw.text((16, 48), subtitle, font=cpu.font(17), fill=(214, 218, 226))
            for i, row in enumerate(chunk):
                x, y = 8+(i % 2)*516, 100+(i//2)*336
                draw.text((x+4, y), row['label'], font=cpu.font(17), fill='white')
                for col, key in enumerate(('source', 'model')):
                    draw.text((x+4+col*256, y+28), row[key+'_label'], font=cpu.font(14), fill=(205, 210, 220))
                    im = Image.open(REF/row[key])
                    if row.get(key+'_crop'):
                        im = im.crop(row[key+'_crop'])
                    canvas.paste(fit(im, (250, 250)), (x+col*256, y+55))
                if row.get('note'):
                    draw.text((x+4, y+307), row['note'], font=cpu.font(14), fill=(235, 193, 145))
            name = f'boards/{section["id"]}_{page:02d}.png'
            output.write(name, cpu.png_bytes(canvas))
            written.append({'section': section['id'], 'title': title, 'file': name})
    output.write('review_index.json', encoded(review))
    output.write('source_images.json', encoded(source_files))
    output.write('boards/index.json', encoded(written))
    return written, source_files


def overview(output):
    rows = [
        ('idle 待机 · 外壳有动图', 'frames/MCD_Heart_of_Ender_Idle/frame_0065.png', 'idle/idle_f000.png', 'idle/idle_f065.png', '0.00s', '2.60s'),
        ('walk 爬行 · 外壳推断', 'Heart_of_ender_crawling_with_decal_trail.png', 'walk/walk_00.00.png', 'walk/walk_01.00.png', '0.00s', '1.00s'),
        ('mortar 后仰吐息 · 推断', 'Minecraft-dungeons-heart-of-ender.jpg', 'mortar/mortar_00.40.png', 'mortar/mortar_01.20.png', '0.40s', '1.20s'),
        ('cross_beam 抬身 · 外壳推断', 'Heart_of_Ender_prepare_to_shoot_beams.png', 'cross_beam/cross_beam_00.50.png', 'cross_beam/cross_near_front.png', '0.50s', '2.00s（近正面）'),
        ('sink 沉地 · 推断', 'Heart_of_Ender_in_game.png', 'sink/sink_00.40.png', 'sink/sink_01.70.png', '0.40s', '1.70s'),
        ('rise 升起 · 推断', 'Heart_of_Ender_in_game.png', 'rise/rise_00.20.png', 'rise/rise_01.90.png', '0.20s', '1.90s'),
        ('death 死亡 · 推断', 'Hero_kills_Heart_of_Ender_Arch-Illager_disappear.jpg', 'death/death_00.00.png', 'death/death_03.80.png', '0.00s', '3.80s'),
    ]
    canvas = Image.new('RGB', (900, 95+len(rows)*340), BG)
    draw = ImageDraw.Draw(canvas)
    draw.text((15, 10), '动作关键姿态总览 · '+EXPECTED[:8], font=cpu.font(27), fill='white')
    draw.text((15, 48), '离线CPU重新渲染 · 非Blockbench、非游戏 · 无bloom', font=cpu.font(18), fill=(220, 220, 230))
    for i, (label, source, a, b, ta, tb) in enumerate(rows):
        y = 95+i*340
        draw.text((12, y+4), label, font=cpu.font(18), fill='white')
        for col, (path, caption) in enumerate(((REF/source, '依据素材'), (OUT/'frames'/a, '模型 '+ta), (OUT/'frames'/b, '模型 '+tb))):
            canvas.paste(fit(Image.open(path), (290, 280)), (5+col*300, y+32))
            draw.text((12+col*300, y+312), caption, font=cpu.font(18), fill='white')
    output.write('overview.png', cpu.png_bytes(canvas))


def html_index(boards, evidence, output):
    nav, figures, seen = [], [], set()
    for b in boards:
        anchor = ''
        if b['section'] not in seen:
            seen.add(b['section'])
            anchor = f' id="{b["section"]}"'
            nav.append(f'<a href="#{b["section"]}">{html.escape(b["title"])}</a>')
        figures.append(f'<figure{anchor}><figcaption>{html.escape(b["title"])}</figcaption><a href="{b["file"]}"><img loading="lazy" src="{b["file"]}"></a></figure>')
    frame_links = ''.join(f'<li><a href="{f["path"]}">{html.escape(f["id"])} · {f["time"]:g}s · {f["view"]}</a></li>' for f in evidence['frames'])
    page = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>M3 最新材质动作对照</title>
<style>body{background:#20242a;color:#eee;font:17px system-ui;max-width:1120px;margin:28px auto;padding:0 20px;line-height:1.6}a{color:#dab8ff}img{max-width:100%;display:block;margin:12px 0}figure{margin:34px 0}nav a{display:inline-block;margin:5px 10px 5px 0}code{word-break:break-all}</style>
<h1>Heart of Ender · M3 最新材质动作对照</h1>
<p>全部模型图从最新 af9f3fea… 模型重新计算姿态与采样图集，没有给旧PNG改色。离线 CPU 渲染，非 Blockbench 原生图、非游戏截图，没有 bloom；不证明 Java 透明排序或实际方向光。</p>
<p>有动图的片段对照原GIF选帧；推断动作对照依据截图，不冒充同帧原作动画。原来的动作残差没有因为换材质而消失。</p>
<p><a href="MOTION_REVIEW_REPORT.md">报告与局限</a> · <a href="../heart_of_ender_material_v3.bbmodel">本次模型</a> · <a href="render_evidence.json">逐帧版本、相机与哈希</a> · <a href="review_index.json">对照索引</a></p>
<a href="overview.png"><img src="overview.png" alt="七动作关键姿态总览"></a>
<h2>逐关键姿态与正侧背</h2><nav>'''+''.join(nav)+'</nav>'+''.join(figures)+'<details><summary>254 张原始模型帧（500×500）</summary><ul>'+frame_links+'</ul></details></html>'
    output.write('index.html', page.encode('utf-8'))


def report(evidence, boards, output):
    counts = Counter(f['clip'] for f in evidence['frames'])
    table = '\n'.join(f'| `{clip}` | {counts[clip]} |' for clip in CLIPS)
    text = f'''# M3 最新材质关键姿态审阅

本组把现有 M3 动作按最新材质重新渲染，供用户视觉审阅；没有改模型、动作或进入 M4/M5。模型 SHA-256：`{EXPECTED}`。仍为21个展示部件、7段动作、3401个关键帧。

## 入口与覆盖

[打开完整审阅页](index.html) · [七动作总览](overview.png) · [逐帧证据](render_evidence.json) · [原素材哈希](source_images.json)

完成原 `m3_motion/review_requests.json` 的全部 **254个请求、{len(boards)}页并排图**。81张外壳Idle帧覆盖完整16秒；77张小人近景包含Docile 12姿态、Anxious 15姿态、Fourside全部50源帧。每段动作另有固定正面、侧面、背面及四分之三视角。没有删掉难画的转折，也没有给旧PNG换色。

| 模型 clip | 请求帧数（含近景与各视角） |
|---|---:|
{table}

## 来源标签与时间

- `idle` 外壳有16秒动图；体内Docile有4.8秒动图，16秒嵌入3周期，每周期16/3秒，速度为原片90%，`t=k×16/3+u/0.9`。
- `walk` 外壳根据爬行截图与页面攻击间隙爬行文字推断；小人Anxious有8秒动图，1:1嵌入。
- `cross_beam` 外壳依据抬身截图/页面文字推断；小人Fourside有动图，全部50帧按`t=1+f/25`放入1–3秒。没有把快变帧平滑成匀速旋转，也没有制作光束。
- `mortar`、`sink`、`rise`、`death`均为推断，并排左列明确使用依据截图，不能当作同帧原作视频。

每格源文件和模型时间见 [review_index.json](review_index.json)。完整动作证据与既有局限仍见 [历史M3报告](../../M3_REPORT.md)；该报告旧PNG不作为本组新材质图片。

## 渲染方式与相机

全部图由只读复用的 Python/NumPy CPU 正交光栅器，从当前bbmodel的骨骼轨道、元素、UV及内嵌图集重新生成。最近邻取样、alpha 0.1阈值、背面剔除、普通alpha混合和深度写入；全亮原RGB、没有bloom或后期补画。

这是**离线模拟，非Blockbench原生渲染，非Minecraft截图**。面中心排序仅为单缓冲近似，不覆盖Java实际实体分批、方向光、雾、mipmap和所有透明穿插。91项正式模型校验仍见 [validation.json](../validation.json)，不能与本组图片合并宣称游戏效果已通过。

沿用原请求的固定相机与原参考拟合，不对每帧重新居中/缩放。cross_beam全景和正侧背沿用高度96的固定镜头。小人近景只跟随`shell_root`相对rest的整体变换，剥离外壳整体动作，**不追随inner_root、不抵消小人自身运动**。相机数值与历史原生记录的最大差为 `{evidence['historical_camera_max_error']:.9g}`；这项只核相机约定，不是本次原生渲染验证。

有地面的视角使用顶面 `y=-4.66381`、向下200单位的实心地块，避免零厚度平面在正侧背视图漏出地下小人。地块只存在于预览，不改模型或世界。沉地/升起及死亡末段的遮挡核对见证据中的`ground_visibility_checks`。

## 已知视觉差距

材质变化不修改已确认的R2几何和既有动作。Idle源f015的B肢仍保留端点优先方案，方向与端点的二维证据有冲突；Fourside源45仍暂用E1后收肢方案，隐藏深度是推断。历史同帧审阅记录的冠根最大44.38px残差、45帧底部低21px、小人脸纹缺失及单骨肢体轮廓差距仍须保留；本轮没有重新拟合这些残差，更不能因为重新渲染而称它们消失。

cross_beam保持C1固定肢根、抬肢开放小人的推断；上层末端可能比参考偏高。walk循环首尾矩阵相等不等于步态已还原。death是低头、肢体内蜷、小人最后沉地；外壳不整体沉地。

本组只补齐最新材质的关键姿态视觉证据，等待用户审阅，不宣称动作全部精确还原。v2曾由用户实测接受，不能因此把这组CPU图标成v3真实游戏验证；独立探针状态由根任务另行记录。没有新增 gameplay、M4模型或M5正式接入。

原素材版权属于Mojang Studios；本项目非商业，与Mojang无关联。原始来源见 [SOURCES.md](../../SOURCES.md)。
'''
    output.write('MOTION_REVIEW_REPORT.md', text.encode('utf-8'))


def assemble(req, index, evidence, output):
    generated = {f['id']+'.png' for f in req['frames']}
    boards, sources = board_index(index, generated, output)
    overview(output)
    html_index(boards, evidence, output)
    report(evidence, boards, output)
    missing_links = []
    for filename in ('index.html', 'MOTION_REVIEW_REPORT.md'):
        content = (OUT/filename).read_text(encoding='utf-8')
        links = re.findall(r'(?:href|src)="([^"]+)"', content) if filename.endswith('.html') else re.findall(r'\]\(([^)]+)\)', content)
        for target in links:
            if not target.startswith(('#', 'http:', 'https:')) and not (OUT/target).exists():
                missing_links.append([filename, target])
    assert not missing_links, missing_links
    review = read(OUT/'review_index.json')
    model_prefix = OUT.relative_to(REF).as_posix()+'/frames/'
    used = {row[key].removeprefix(model_prefix) for section in review['sections'] for row in section['pairs']
            for key in ('source', 'model') if row[key].startswith(model_prefix)}
    assert used == generated, 'Some registered frames are missing from comparison boards'
    coverage = {'model_sha256':EXPECTED, 'requested':254, 'rendered':len(evidence['frames']),
                'board_pages':len(boards),'source_files':len(sources),
                'all_frame_hashes_match':all(sha(OUT/f['path'])==f['sha256'] for f in evidence['frames']),
                'original_sources_unchanged':all(sha(REF/k)==v for k,v in sources.items()),
                'model_unchanged':sha(MODEL)==EXPECTED,
                'all_254_frames_used_in_boards':used==generated,
                'local_links_missing':missing_links,
                'rendered_frames_touching_image_border':sum(f['render_stats']['touches_border'] for f in evidence['frames']),
                'camera_max_error_vs_historical_native':evidence['historical_camera_max_error'],
                'ground_visibility_checks':evidence['ground_visibility_checks']}
    output.write('delivery_check.json',encoded(coverage))
    print(json.dumps(coverage, ensure_ascii=False), flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--render-only', action='store_true', help='Only render registered frames and evidence')
    ap.add_argument('--assemble-only', action='store_true', help='Rebuild only labels/index after validating existing current-model frame hashes')
    args = ap.parse_args()
    if sha(MODEL) != EXPECTED:
        raise ValueError('Source model differs from the explicitly selected latest material')
    request_path, index_path = REF/'m3_motion/review_requests.json', REF/'m3_motion/review_index.json'
    req, index = read(request_path), read(index_path)
    assert len(req['frames']) == 254
    assert len({r['id'] for r in req['frames']}) == 254
    if args.assemble_only:
        evidence = read(OUT/'render_evidence.json')
        assert evidence['bbmodel_sha256'] == EXPECTED
        assert evidence['requests_sha256'] == sha(request_path)
        assert len(evidence['frames']) == 254
        assert all(sha(OUT/f['path']) == f['sha256'] for f in evidence['frames'])
        evidence['assembly_generator_sha256'] = sha(Path(__file__))
        output = Output()
        output.write('render_evidence.json', encoded(evidence))
        assemble(req, index, evidence, output)
        return
    checks = cpu.self_checks()
    mob = SimpleNamespace(bbmodel=MODEL, anim_from=None, key='heart_of_ender_m3_review')
    bones, _, _ = dm.load_bbmodel(mob)
    clips = dm.load_animations(mob)
    historic = read(REF/'m3_preview/render_evidence.json')
    native_frames = {f['id']:f for f in historic['frames']}
    output = Output()
    evidence = {'engine': 'Python/NumPy CPU rasterizer; reused heart_of_ender_material_preview.py read-only',
                'status': 'OFFLINE ONLY; NOT BLOCKBENCH; NOT MINECRAFT; no recoloring old renders; no bloom',
                'bbmodel_sha256': EXPECTED, 'generator_sha256': sha(Path(__file__)),
                'renderer_sha256': sha(Path(cpu.__file__)), 'requests_sha256': sha(request_path),
                'source_index_sha256': sha(index_path), 'views': req['views'], 'self_checks': checks,
                'historic_camera_evidence_sha256': sha(REF/'m3_preview/render_evidence.json'),
                'historic_camera_model_sha256': historic['bbmodel_sha256'],
                'frames': [], 'ground_visibility_checks': [], 'historical_camera_max_error': 0.0,
                'rendering': {'alpha_cutoff':0.1,'nearest_neighbor':True,'depth_write':True,
                              'sorting':'one global quad-center far-to-near list',
                              'lighting':'raw fullbright RGB; no directional shader lighting or bloom',
                              'ground':'temporary opaque 400x200x400 box, top at registered ground_y',
                              'inner_camera':'posed(shell_root) * inverse(rest(shell_root)); never follows inner_root'}}
    @lru_cache(maxsize=12)
    def pose(clip, time):
        return cpu.load_model(MODEL, clip, time)
    for number, f in enumerate(req['frames'], 1):
        v = req['views'][f['view']]
        raw = pose(f['clip'], f['time'])
        model = filter_inner(raw) if v.get('isolate_inner') else raw
        cam, actual = actual_camera(v, bones, clips[f['clip']], f['time'])
        old = native_frames.get(f['id'])
        err = 0.0
        if old:
            err = max(float(np.max(np.abs(np.array(actual[k])-np.array(old['actual_camera'][k])))) for k in ('position','target','up'))
            evidence['historical_camera_max_error'] = max(evidence['historical_camera_max_error'], err)
        if 'ground_y' in v:
            model = add_ground(model, v['ground_y'])
        pixels, stats = cpu.render(model, cam)
        stats.update(visible_pixels(pixels))
        name = 'frames/'+f['id']+'.png'
        data = cpu.png_bytes(Image.fromarray(pixels))
        output.write(name, data)
        evidence['frames'].append({**f, 'path':name, 'bbmodel_sha256':EXPECTED,
            'sha256':hashlib.sha256(data).hexdigest(), 'geometry_sha256':raw.evidence['posed_geometry_sha256'],
            'embedded_png_sha256':raw.evidence['embedded_png_sha256'], 'camera':cam,'actual_camera':actual,
            'camera_error_vs_historical_native':err,'render_stats':stats,'isolated_inner':bool(v.get('isolate_inner'))})
        if 'ground_y' in v and ((f['clip']=='sink' and f['time']>=1.7) or (f['clip']=='rise' and f['time']==0)):
            check={'id':f['id'],'purpose':'fully sunk shell occluded by ground volume','visible_pixels':stats['visible_colored_pixels']}
            assert check['visible_pixels']==0, check
            evidence['ground_visibility_checks'].append(check)
        if 'ground_y' in v and f['clip']=='death' and f['time']>=3.8:
            inner, _ = cpu.render(add_ground(filter_inner(raw),v['ground_y']),cam)
            check={'id':f['id'],'purpose':'final inner figure hidden by ground, outer shell retained',
                   'visible_inner_pixels':visible_pixels(inner)['visible_colored_pixels']}
            assert check['visible_inner_pixels']==0, check
            evidence['ground_visibility_checks'].append(check)
        if number % 8 == 0 or number == len(req['frames']):
            print(f'CPU key poses {number}/{len(req["frames"])} | {f["id"]}', flush=True)
    assert evidence['historical_camera_max_error'] < 1e-4, 'Camera following differs from the recorded reference convention'
    assert sha(MODEL) == EXPECTED, 'Source model changed while rendering'
    evidence['counts']={'frames':len(evidence['frames']), 'by_clip':dict(Counter(f['clip'] for f in req['frames'])),
                        'by_view':dict(Counter(f['view'] for f in req['frames']))}
    output.write('render_evidence.json', encoded(evidence))
    if args.render_only:
        return
    assemble(req, index, evidence, output)


if __name__ == '__main__':
    main()
