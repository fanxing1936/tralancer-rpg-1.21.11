#!/usr/bin/env python3
"""M2 单图集：原样星窗/小人/44px遮罩 + 可追溯的眼齿最近邻采样。

不生成几何或动作，不调用共用构建。所有派生输出仅在 m2_atlas/。
"""
from pathlib import Path
import hashlib
import json
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont

REF = Path(__file__).resolve().parent / 'heart_of_ender_ref'
OUT = REF / 'm2_atlas'
SIZE = (512, 512)
STARS = 'MCD_Decal_Puddle_(texture).png'
RENDER = 'MCD_Heart_of_Ender.png'
MASK = 'MCD_Heart_of_Ender_(glow_effect_texture).png'
ARCHIE = 'T_ArchIllagerUndressed.png'
FONT = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 18)
SMALL = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 15)

STAR_WINDOWS = {
    'A': [24, 24, 152, 152], 'B': [260, 32, 388, 160],
    'C': [472, 112, 600, 240], 'D': [72, 440, 200, 568],
    'E': [290, 346, 418, 474], 'F': [498, 478, 626, 606],
}
# 同结构量测统一的二维拟合；包含上颅与闭合下颚的全头矩形。
# 顺序 TL, TR, BR, BL。低对比角点仍为拟合，误差约8–12源像素。
FRONT_QUAD = [[218, 211], [348, 262], [402, 439], [272, 388]]
SIDE_QUAD = [[348, 262], [476, 154], [530, 331], [402, 439]]
LEFT_EYE_QUAD = [[254, 297], [289, 311], [296, 329], [261, 315]]
RIGHT_EYE_QUAD = [[325, 325], [358, 338], [366, 357], [333, 344]]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def rgbahash(im):
    return digest(im.convert('RGBA').tobytes())


def load(name):
    return Image.open(REF / name).convert('RGBA')


def homography(quad):
    """Map destination normalized (u,v,1) to source pixel coordinates."""
    a, b = [], []
    for (u, v), (x, y) in zip(((0, 0), (1, 0), (1, 1), (0, 1)), quad):
        a += [[u, v, 1, 0, 0, 0, -x*u, -x*v], [0, 0, 0, u, v, 1, -y*u, -y*v]]
        b += [x, y]
    h = np.linalg.solve(np.asarray(a, dtype=float), np.asarray(b, dtype=float))
    return np.append(h, 1).reshape(3, 3)


def extract(quad, size, rects, halfplanes=()):
    src = np.array(load(RENDER))
    width, height = size
    yy, xx = np.indices((height, width))
    uv = np.stack(((xx + .5) / width, (yy + .5) / height, np.ones_like(xx)), axis=0).reshape(3, -1)
    h = homography(quad)
    xy = h @ uv
    x = np.floor(xy[0] / xy[2] + .5).astype(int).reshape(height, width)
    y = np.floor(xy[1] / xy[2] + .5).astype(int).reshape(height, width)
    assert x.min() >= 0 and y.min() >= 0 and x.max() < src.shape[1] and y.max() < src.shape[0]
    samples = src[y, x]
    keep = (samples[:, :, 0] >= 230) & (samples[:, :, 1] >= 180) & (samples[:, :, 2] >= 230) & (samples[:, :, 3] >= 1)
    spatial = np.zeros((height, width), dtype=bool)
    for x0, y0, x1, y1 in rects:
        spatial |= (x >= x0) & (x < x1) & (y >= y0) & (y < y1)
    keep &= spatial
    for aa, bb, cc in halfplanes:
        keep &= aa*x + bb*y + cc >= 0
    result = np.zeros_like(samples)
    result[keep] = samples[keep]  # retained RGB AND alpha remain exact source values
    rule = {
        'destination_coordinates': 'u=(pixel_x+0.5)/width; v=(pixel_y+0.5)/height',
        'inverse_homography': h.tolist(),
        'homogeneous_divide': True,
        'nearest': 'floor(source_coordinate + 0.5)',
        'source_mask': {'rgb_min': [230, 180, 230], 'alpha_min': 1, 'union_rects': rects,
                        'halfplanes_ax_by_c_ge_0': [list(p) for p in halfplanes]},
        'retained_rgba': 'copy source[y,x] without recoloring or alpha change',
        'discarded_rgba': [0, 0, 0, 0],
    }
    return Image.fromarray(result, 'RGBA'), rule, x.astype(np.uint16), y.astype(np.uint16), keep


def checker(size, cell=16):
    im = Image.new('RGBA', size, (52, 57, 67, 255))
    d = ImageDraw.Draw(im)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x//cell+y//cell) % 2:
                d.rectangle((x, y, x+cell-1, y+cell-1), fill=(78, 83, 94, 255))
    return im


def arch_uv_study():
    """Record visible UV bounds separately from uncertain anatomical labels."""
    OUT.mkdir(parents=True, exist_ok=True)
    def item(label, faces, dims, confidence, evidence, cautions):
        return {'label': label, 'evidence': 'inferred', 'pixel_boundaries': 'confirmed_by_source_pixels',
                'semantic_confidence': confidence, 'candidate_uv_box_dimensions_whd': dims,
                'faces': faces, 'atlas_faces': {k: [v[0]+432,v[1]+8,v[2]+432,v[3]+8] for k,v in faces.items()},
                'evidence_notes': evidence, 'cautions': cautions}
    data = {
        'schema_version': 1,
        'source_file': ARCHIE, 'source_size': [64,64], 'atlas_offset': [432,8],
        'coordinate_convention': 'UV rects [u0,v0,u1,v1), origin top-left; faces are proposed Java-facing assignments, not recovered original UV orientation',
        'source_png_sha256': digest((REF/ARCHIE).read_bytes()),
        'status': 'M2 provisional UV assignment; source geometry and original face orientation unavailable',
        'head': item('宽灰头候选', {
            'north':[6,6,18,13], 'east':[18,6,24,13], 'south':[24,6,36,13],
            'west':[0,6,6,13], 'up':[6,0,18,6], 'down':[18,0,30,6]},
            [12,7,6], 'high',
            ['灰色横带宽36、高7；两块12×6顶/底候选与12/6/12/6侧带可构成12×7×6盒网。',
             'Docile/Anxious可见宽头、短面高；与普通村民8×10头比例不同。'],
            ['黑灰的面边界部分连续，网络并非源geometry证明。',
             'north/east方向为工作映射；原图没有足够纹样证明所有面的朝向。']),
        'nose': item('鼻部候选', {
            'north':[2,14,4,18], 'east':[4,14,6,18], 'south':[6,14,8,18],
            'west':[0,14,2,18], 'up':[2,12,4,14], 'down':[4,12,6,14]},
            [2,4,2], 'medium',
            ['小灰色块有2×4侧面与2×2端面候选，可拟合2×4×2。',
             'Anxious侧面有脸下突起，但强光下难以拆分鼻与同侧细肢。'],
            ['与宽头末行、灰细条相邻/部分共用灰像素，不主张已识别独立官方鼻UV。',
             '如几何鼻更短，保持几何测量；不得用UV盒候选强行拉长鼻。']),
        'crown': item('顶部长条/高冠候选', {
            'north':[36,4,40,15], 'east':[40,4,44,15], 'south':[44,4,48,15],
            'west':[48,4,52,15], 'up':[40,0,44,4], 'down':[44,0,48,4]},
            [4,11,4], 'high',
            ['金色侧带[36,4,52,15]可分四块4×11；[40,0,44,4]为4×4金色圈，中心2×2透明。',
             'Docile/Anxious顶部竖条宽约主头三分之一，与4:12候选比相容。'],
            ['名称冠是语义推断；更可靠称呼为头顶长条。没有原geometry。',
             '将含红/蓝细点的一面朝north是待核对方案，不能称原作朝向已证实。',
             'down区域原图全透明，可保留透明或texture=null，不能填新颜色封底。']),
        'torso': item('绿中心/蓝金侧衣的躯干候选', {
            'north':[5,27,14,36], 'east':[14,27,19,36], 'south':[19,27,27,36],
            'west':[0,27,5,36], 'up':[5,22,14,27], 'down':[5,36,14,40]},
            None, 'medium_low',
            ['可直接量到9×5上方绿色矩形、约27×9横带、9×4下方绿色矩形。',
             'Docile显示比宽头明显窄的躯干；此岛可作为保守服装来源候选。'],
            ['north宽9、south宽8，up深5、down深4，不能冒称完美9×9×5标准盒网。',
             '像素边界/补边与实际三维尺寸可能不同；几何以Docile轮廓拟合为准。',
             '若映射出与参考不符的金边，需对照渲染选择候选，而非移动到不明UV区补色。']),
        'arm': item('灰细肢皮肤候选', {
            'north':[7,13,8,21], 'east':[8,13,9,21], 'south':[9,13,10,21],
            'west':[6,13,7,21], 'up':[7,13,8,14], 'down':[7,20,8,21]},
            [1,8,1], 'low',
            ['灰色连续条[6,13,10,21]中可取四个1×8细长面，且无杂色条。',
             'Docile侧面细肢与宽头相比很细，Anxious可见细条抬起。'],
            ['这是受源颜色约束的暂定分配，不是已恢复官方arm UV。',
             '端面取条内端部1px，明确复用灰色，未宣称找到独立端面岛。',
             '使用相同纹理的左右臂可共享此区域；实际朝向需几何姿态确认。']),
        'leg': item('灰细肢皮肤候选（与arm有意复用）', {
            'north':[7,13,8,21], 'east':[8,13,9,21], 'south':[9,13,10,21],
            'west':[6,13,7,21], 'up':[7,13,8,14], 'down':[7,20,8,21]},
            None, 'low',
            ['Docile可见两条细腿与两个前伸末端，证明腿要分开；颜色被强光覆盖。',
             '未找到可无歧义绑定腿的独立UV岛，暂时有意复用灰细条。'],
            ['不把8像素UV高当作已确认腿长；可见腿只有较短一段。',
             '不能将蓝金15像素长条直接定为腿并据此拉长模型。']),
        'foot': item('暗蓝十字岛的鞋/末端候选', {
            'north':[13,16,16,19], 'east':[16,16,19,19], 'south':[19,16,22,19],
            'west':[10,16,13,19], 'up':[13,13,16,16], 'down':[13,19,16,22]},
            [3,3,3], 'low',
            ['暗蓝区域确为六块3×3组成的十字候选网。',
             'Docile/Anxious看见脚尖前伸，支持腿末端需要方向，而不支持立方大鞋。'],
            ['该岛的鞋语义未经原geometry证实；可能属于别的小部件。',
             '3×3面是采样区，不要求几何脚为3×3×3；脚的长宽高仍按轮廓。',
             '若这个候选造成明显蓝鞋偏差，可用灰细肢延伸方案对照，不得称其已复刻。']),
        'alternatives': [
            {'id':'A','label':'宽头+窄躯干+灰细肢（建议首轮对照）',
             'torso_dimensions_candidates_whd':[[8,9,4],[9,9,5]],
             'limbs':'几何按Docile可见轮廓，灰条只供表面采样；左右腿独立。',
             'foot':'前伸短段，可用暗蓝3×3面候选，但不做3³鞋块。',
             'basis':'宽头/长顶条/细肢/双脚可见；四肢具体UV语义未证实。'},
            {'id':'B','label':'蓝金衣袖候选（供必要时比较，不是默认事实）',
             'arm_uv_source_rect':[52,0,60,15],
             'dimensions_hypotheses_whd':[[2,15,2],[1,15,1]],
             'basis':'该区域可以解释为四个2×15面，或两个四面1×15细条；仅凭贴图无法确定。',
             'caution':'这些UV尺寸不能直接成为手臂长度；它也可能是衣饰，GIF高亮无法识别蓝金颜色。'},
            {'id':'C','label':'腿与脚同皮肤候选',
             'foot_uv_reuse':'arm/leg灰细条，几何保留脚尖前伸但不使用暗蓝岛。',
             'basis':'保留已经看见的末端朝向，避免给无法辨认的鞋岛过高置信；颜色还原仍未证实。'}],
        'unused_or_unassigned': [
            {'rect':[32,15,55,29], 'note':'蓝金长片，白灰上/下边与中间透明开口；疑似衣片/外袍，不能直接称左右腿。'},
            {'rect':[52,0,60,15], 'note':'蓝金细条；保留为衣袖/衣饰候选，不在默认灰细肢方案中使用。'},
            {'rect':[0,0,6,6], 'note':'小灰/黑/白图形；不能因包含白像素就任意拼成眼睛。'},
            {'rect':[18,16,24,23], 'note':'零散金红区域；未给新模型追加缺乏证据的饰品。'}],
    }
    (OUT/'arch_uv_regions.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')

    source = load(ARCHIE)
    preview = checker(source.size,2);preview.alpha_composite(source)
    preview=preview.resize((1024,1024),Image.Resampling.NEAREST).convert('RGB')
    d=ImageDraw.Draw(preview)
    for k in range(0,65,4):
        d.line((k*16,0,k*16,1023),fill=(110,110,110),width=1)
        d.line((0,k*16,1023,k*16),fill=(110,110,110),width=1)
        if k<64:
            d.text((k*16+2,1),str(k),font=SMALL,fill=(255,170,245),stroke_width=1,stroke_fill='black')
            d.text((1,k*16+2),str(k),font=SMALL,fill=(255,170,245),stroke_width=1,stroke_fill='black')
    preview.save(OUT/'arch_uv_grid.png')
    colors={'head':(255,120,100),'nose':(120,220,255),'crown':(255,220,70),'torso':(100,255,140),'arm':(220,160,255),'foot':(255,170,70)}
    for name,color in colors.items():
        for face,rect in data[name]['faces'].items():
            x0,y0,x1,y1=rect
            d.rectangle((x0*16,y0*16,x1*16-1,y1*16-1),outline=color,width=2)
    for name,x,y in [('head',16,650),('crown',16,690),('torso',16,730),('nose',16,770),('arm',16,810),('foot',16,850)]:
        d.text((x,y),name+'：'+data[name]['label']+' / '+data[name]['semantic_confidence'],font=FONT,fill=colors[name])
    d.text((16,920),'边框是可追溯采样区；语义与朝向均标推断，不是官方UV恢复。',font=FONT,fill='white')
    preview.save(OUT/'arch_uv_islands_annotated.png')

    facesheet=Image.new('RGB',(1200,7*170),(31,34,42));d=ImageDraw.Draw(facesheet)
    for i,name in enumerate(('head','nose','crown','torso','arm','leg','foot')):
        d.text((10,i*170+5),name+' / '+data[name]['semantic_confidence'],font=SMALL,fill='white')
        for j,(face,rect) in enumerate(data[name]['faces'].items()):
            patch=source.crop(tuple(rect));bg=checker(patch.size,2);bg.alpha_composite(patch)
            factor=max(1,min(120//max(1,patch.width),112//max(1,patch.height)))
            view=bg.resize((patch.width*factor,patch.height*factor),Image.Resampling.NEAREST).convert('RGB')
            x=175+j*165;y=i*170+30;facesheet.paste(view,(x,y))
            d.text((x,i*170+7),face,font=SMALL,fill='white')
            d.text((x,i*170+145),str(rect),font=SMALL,fill=(190,200,215))
    facesheet.save(OUT/'arch_uv_faces_comparison.png')
    gif=Image.open(REF/'MCD_Arch-Illager_Docile.gif');gif.seek(0);f=gif.convert('RGBA')
    bg=Image.new('RGBA',f.size,(95,99,111,255));bg.alpha_composite(f)
    bg.resize((1000,1000),Image.Resampling.NEAREST).save(OUT/'arch_docile_reference.png')
    notes='''# M2：体内小人的 UV 岛与证据边界

`arch_uv_regions.json` 按 `head,nose,crown,torso,arm,leg,foot` 提供 `faces.north/east/south/west/up/down`，坐标均为原64×64贴图像素；另给加上图集偏移 `(432,8)` 的 `atlas_faces`。所有材质RGBA均从原贴图原样读取，不重画、不重着色。

**像素边界可确认，不等于部位语义、三维尺寸、朝向已确认。** 原始geometry不在素材内，Docile/Anxious强光又遮掉纹理颜色；所以每个semantic region的 `evidence` 都诚实写为 `inferred`，另分高/中/低置信。没有把普通村民box UV套上后称为事实。

| 候选 | 可观察的UV结构 | 与动图相互支持的部分 | 未能确认 |
|---|---|---|---|
| 宽灰头 | 36×7灰侧带，可分6/12/6/12；12×6上下候选 | 宽头、短脸高，与12×7×6候选相容 | 原face朝向，灰色连续块是否有共享/补边 |
| 顶部长条/高冠 | 四个4×11金色侧面；4×4顶金圈中间2×2透明 | 顶部长条宽约主头三分之一，与4:12吻合 | “冠”语义、红/蓝细点朝向；不得把这个推断包装成官方源模型 |
| 鼻候选 | 小灰块可拼2×4×2 | 侧面有面下突起 | 强光下鼻和细肢部分交叠；此处有共享灰像素 |
| 躯干候选 | 上9×5绿块，侧带约27×9，下9×4绿块 | 躯干明显窄于头 | 不是标准完全一致的盒网；8×9×4与9×9×5均是合理工作候选，不能仅据UV精确断言 |
| 臂/腿灰细条 | 连续4×8灰条，可取四个1×8面 | 细肢、两条独立腿可见 | 尚未找到唯一官方部位对应；caps明确复用条内端部像素，左右肢有意共享，不冒称独立岛 |
| 脚/鞋候选 | 暗蓝六块3×3十字网 | GIF脚尖向前，需要保留末端方向 | 该岛可能属于别的小部件；3×3 UV绝不要求几何是3³大鞋 |

三套可比较的处理方案已写在JSON `alternatives`：A以宽头、窄身、灰细肢作为首轮形态；B保留蓝金细条作为衣袖/衣饰候选，但不用15像素UV高强迫几何手臂变长；C脚部继续使用灰细条，只保留脚尖形状，避免给暗蓝岛鞋的语义过高置信。这里没有提前替用户认定不确定部位已经复刻。

特别保留未分配岛 `[32,15,55,29]`：它有白灰边、中间透明开口和蓝金长片，更像服装/披片，不能凭蓝色把它直接当作双腿。`[52,0,60,15]` 蓝金条可能是一个2×15×2盒或两个1×15×1条；单凭贴图不能唯一判断。

- [原贴图像素网格](arch_uv_grid.png)
- [采样边界标注](arch_uv_islands_annotated.png)
- [各候选六面原像素对照](arch_uv_faces_comparison.png)
- [Docile原始第0帧最近邻放大](arch_docile_reference.png)

这些文件仅为静态UV研究；不写bbmodel，不增加骨骼，不做动作。新模型的尺寸仍须由Docile/渲染轮廓约束。原作素材版权属于Mojang；项目非商业、与Mojang无关联。复现由 `heart_of_ender_atlas.py` 中 `arch_uv_study()` 完成。
'''
    (OUT/'ARCH_UV_NOTES.md').write_text(notes,encoding='utf-8')
    return data


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    atlas = Image.new('RGBA', SIZE, (0, 0, 0, 0))
    regions, arrays, pieces, occupancy = [], {}, {}, np.zeros((SIZE[1], SIZE[0]), dtype=bool)

    def put(name, patch, dest, record):
        x0, y0, x1, y1 = dest
        assert patch.size == (x1-x0, y1-y0)
        assert 0 <= x0 < x1 <= SIZE[0] and 0 <= y0 < y1 <= SIZE[1]
        assert not occupancy[y0:y1, x0:x1].any(), name
        occupancy[y0:y1, x0:x1] = True
        atlas.paste(patch, (x0, y0))  # no alpha compositing: raw RGBA is retained
        pieces[name] = patch
        record.update({'name': name, 'atlas_rect': dest, 'size': list(patch.size),
                       'resampling': 'nearest', 'output_rgba_sha256': rgbahash(patch),
                       'opaque_pixels': int((np.array(patch)[:, :, 3] == 255).sum()),
                       'semitransparent_pixels': int(((np.array(patch)[:, :, 3] > 0) & (np.array(patch)[:, :, 3] < 255)).sum()),
                       'visible_pixels': int((np.array(patch)[:, :, 3] > 0).sum())})
        regions.append(record)

    def copy(name, source, rect, dest, note):
        patch = load(source).crop(tuple(rect))
        put(name, patch, dest, {'kind': 'source_copy', 'source_file': source, 'source_rect': rect,
                             'scale': [1, 1], 'flip': [False, False],
                             'source_rgba_sha256': rgbahash(patch), 'note': note})

    for i, (label, rect) in enumerate(STAR_WINDOWS.items()):
        x, y = 8+(i % 3)*136, 8+(i//3)*136
        assert np.array(load(STARS).crop(tuple(rect)))[:, :, 3].min() == 255, label
        copy('stars_'+label, STARS, rect, [x, y, x+128, y+128],
             '原 RGB/alpha 的128×128窗口；不缩整张711图，不重映射成紫色。')
    copy('arch_undressed', ARCHIE, [0, 0, 64, 64], [432, 8, 496, 72],
         '无外袍小人原贴图；64×64全图1:1；_S仅存档，不作发光。')
    copy('glow_mask_raw', MASK, [0, 0, 44, 44], [432, 88, 476, 132],
         '用户指定44×44效果遮罩原样保留RGBA；不是眼齿图案；半透明游戏渲染尚未验证。')

    extraction_specs = [
        ('front_eyes', FRONT_QUAD, (128, 160), [[248, 292, 301, 334], [322, 321, 372, 364]], [], [8, 288, 136, 448]),
        ('front_teeth', FRONT_QUAD, (128, 160), [[272, 350, 407, 431]], [[-.4, 1, -239.2]], [144, 288, 272, 448]),
        ('side_teeth', SIDE_QUAD, (128, 160), [[389, 350, 447, 420]], [], [280, 288, 408, 448]),
        ('left_eye_local', LEFT_EYE_QUAD, (64, 24), [[248, 292, 301, 334]], [], [432, 160, 496, 184]),
        ('right_eye_local', RIGHT_EYE_QUAD, (64, 24), [[322, 321, 372, 364]], [], [432, 200, 496, 224]),
    ]
    for name, quad, size, rects, halfplanes, dest in extraction_specs:
        patch, rule, sx, sy, keep = extract(quad, size, rects, halfplanes)
        points = np.array(quad)
        source_rect = [math.floor(points[:, 0].min()), math.floor(points[:, 1].min()),
                       math.ceil(points[:, 0].max())+1, math.ceil(points[:, 1].max())+1]
        put(name, patch, dest, {'kind': 'projection_extract', 'source_file': RENDER,
                             'source_rect': source_rect, 'source_quad': quad,
                             'quad_order': ['TL', 'TR', 'BR', 'BL'],
                             'scale': None, 'flip': [False, False], 'sampling_rule': rule,
                             'note': '只提取已有亮形；四角是与结构量测一致的二维拟合，不是原作UV。全头front包括闭合下颚。'})
        arrays[name+'_x'], arrays[name+'_y'], arrays[name+'_keep'] = sx, sy, keep

    atlas_path = OUT/'atlas.png'
    atlas.save(atlas_path)
    np.savez_compressed(OUT/'pixel_source_map.npz', **arrays)
    doc = {
        'schema_version': 1, 'atlas_file': 'm2_atlas/atlas.png', 'atlas_size': list(SIZE),
        'coordinate_convention': 'all rects are [x0,y0,x1,y1), origin top-left; source_file relative to heart_of_ender_ref',
        'pixel_sha256_definition': 'SHA-256 of width*height*4 RGBA bytes in row-major order, not PNG container bytes',
        'atlas_png_sha256': digest(atlas_path.read_bytes()), 'atlas_rgba_sha256': rgbahash(atlas),
        'source_files': {n: {'png_sha256': digest((REF/n).read_bytes()), 'size': list(load(n).size), 'rgba_sha256': rgbahash(load(n))}
                         for n in (STARS, RENDER, MASK, ARCHIE)},
        'regions': regions,
        'no_model_or_animation_generated': True,
    }
    (OUT/'atlas_regions.json').write_text(json.dumps(doc, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

    # Independent local assertions: raw atlas pixels, copy equality, sampled source identity.
    reopened = Image.open(atlas_path).convert('RGBA')
    audit = {'atlas_size': list(reopened.size), 'overlapping_rectangles': False, 'regions': []}
    for r in regions:
        actual = reopened.crop(tuple(r['atlas_rect']))
        assert rgbahash(actual) == r['output_rgba_sha256']
        if r['kind'] == 'source_copy':
            expected = load(r['source_file']).crop(tuple(r['source_rect']))
            assert actual.tobytes() == expected.tobytes(), r['name']
            result = 'RGBA exact source crop'
        else:
            name = r['name']; src = np.array(load(RENDER)); pix = np.array(actual)
            keep = arrays[name+'_keep']; sx = arrays[name+'_x']; sy = arrays[name+'_y']
            assert np.array_equal(pix[keep], src[sy[keep], sx[keep]])
            assert not pix[~keep].any()
            result = 'each retained RGBA pixel equals recorded nearest source coordinate; discarded RGBA zero'
        audit['regions'].append({'name': r['name'], 'result': result, 'visible_pixels': r['visible_pixels']})
    (OUT/'atlas_audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

    # UV atlas labels. Checkerboard is preview-only and never inserted in atlas.png.
    preview = checker(SIZE)
    preview.alpha_composite(atlas)
    preview = preview.resize((1024, 1024), Image.Resampling.NEAREST).convert('RGB')
    d = ImageDraw.Draw(preview)
    for r in regions:
        x0, y0, x1, y1 = r['atlas_rect']
        d.rectangle((2*x0-1, 2*y0-1, 2*x1, 2*y1), outline=(255, 196, 80), width=2)
        d.text((2*x0+4, 2*y0+4), r['name'], font=SMALL, fill=(255, 220, 130), stroke_width=2, stroke_fill=(0, 0, 0))
    preview.save(OUT/'atlas_annotated.png')

    star_src = load(STARS)
    star_preview = checker(star_src.size); star_preview.alpha_composite(star_src)
    d = ImageDraw.Draw(star_preview)
    for label, rect in STAR_WINDOWS.items():
        d.rectangle((rect[0], rect[1], rect[2]-1, rect[3]-1), outline=(255, 196, 80), width=3)
        d.text((rect[0]+5, rect[1]+5), label, font=FONT, fill=(255, 220, 130))
    star_preview.convert('RGB').save(OUT/'star_window_mapping.png')

    rendered = load(RENDER)
    source = Image.new('RGBA', rendered.size, (95, 99, 111, 255)); source.alpha_composite(rendered)
    crop = source.crop((200, 90, 590, 445)).resize((780, 710), Image.Resampling.NEAREST).convert('RGB')
    crop.save(OUT/'source_head_crop.png')
    d = ImageDraw.Draw(crop)
    for quad, color, label in ((FRONT_QUAD, (255, 196, 80), 'front'), (SIDE_QUAD, (80, 205, 255), 'side')):
        local = [(2*(x-200), 2*(y-90)) for x, y in quad]
        d.line(local+[local[0]], fill=color, width=3)
        for i, (x, y) in enumerate(local):
            d.ellipse((x-4, y-4, x+4, y+4), fill=color)
            d.text((x+5, y+3), label+' '+str(i), font=SMALL, fill=color)
    crop.save(OUT/'head_projection_quads.png')

    comp = Image.new('RGB', (1500, 780), (31, 34, 42)); d = ImageDraw.Draw(comp)
    comp.paste(crop, (10, 45))
    d.text((10, 10), '原渲染 + 二维拟合四角（不是原作UV；仅供来源核对）', font=FONT, fill='white')
    for i, name in enumerate(('front_eyes', 'front_teeth', 'side_teeth')):
        part = checker(pieces[name].size); part.alpha_composite(pieces[name])
        part = part.resize((256, 320), Image.Resampling.NEAREST).convert('RGB')
        x = 810+(i % 2)*330; y = 70+(i//2)*360
        comp.paste(part, (x, y)); d.text((x, y-25), name+'：保留源RGB/alpha', font=SMALL, fill='white')
    comp.save(OUT/'emissive_source_comparison.png')

    raw = Image.new('RGB', (1080, 600), (31, 34, 42)); d = ImageDraw.Draw(raw)
    for name, x, factor in (('arch_undressed', 20, 8), ('glow_mask_raw', 570, 10)):
        patch = pieces[name]; display = checker(patch.size, 4); display.alpha_composite(patch)
        raw.paste(display.resize((patch.width*factor, patch.height*factor), Image.Resampling.NEAREST).convert('RGB'), (x, 60))
        d.text((x, 15), name+' 原样RGBA / 预览棋盘不在图集中', font=SMALL, fill='white')
    raw.save(OUT/'raw_materials_comparison.png')

    rows = ['| 名称 | 源文件 / 矩形 | 图集矩形 | 操作 |', '|---|---|---|---|']
    for r in regions:
        method = '原RGBA 1:1裁取' if r['kind']=='source_copy' else '登记四角 → 最近邻 → 亮形剔背景'
        rows.append('| `%s` | `%s` / `%s` | `%s` | %s |' % (r['name'], r['source_file'], r['source_rect'], r['atlas_rect'], method))
    notes = '''# M2：单图集及精确像素来源

本目录只完成材质图集，不生成模型、骨骼或动画。原始素材版权属于 Mojang Studios；本项目非商业，与 Mojang 无关联。原文件地址/哈希见上级 SOURCES.md。

`atlas.png` 是512×512、单张RGBA图集；坐标统一为左上角原点、右下界不含的 `[x0,y0,x1,y1)`。模型应把该PNG原样base64内嵌为 `textures[0]`。`atlas_regions.json` 是机器可读来源表；`pixel_source_map.npz` 为每个透视提取输出像素保存原图x/y及保留标记。

## 已确认的材质规则

- 六个128×128星窗从711×711原图各取不同区域，**没有整图缩小、没有紫色烘焙、没有改变RGB或alpha**。六窗逐像素核验均为255 alpha，避免M1发现的原图中部透明短条。图集采用1:1保存；预览的放大只用最近邻。
- `glow_mask_raw` 是44×44 `MCD_Heart_of_Ender_(glow_effect_texture).png` 原图的完整RGBA拷贝；**不重着色，不改变alpha，不二值化**。它是白色效果遮罩，不能当眼睛/牙齿图案。半透明是否在实际Minecraft渲染路径达到预期，仍须实测，本图集校验不能证明渲染支持。
- `arch_undressed` 是64×64完整无外袍本体贴图原样拷贝。`T_ArchIllagerUndressed_S.png` 继续仅存档，不作为小人发光层。
- 只有眼/牙/嘴亮形进行了用户允许的来源提取。保留像素的RGBA直接来自原渲染，没有补画侧边牙齿、添加图案或编造颜色。未保留区域被置为全透明零RGBA，所以不会把整块紫色辉光矩形贴上模型。
- 原星图为彩色RGB星点，原小人本体是灰/蓝等色；保留原数据意味着它们不会自动变成原渲染的紫色星空或粉紫小人。此差异是明确采用原样材质的结果，不能以调整曝光或报告措辞掩盖。

## 区域表

'''+ '\n'.join(rows)+'''

## 发光形状采样方法

正面（含闭颚）四角为 TL(218,211)、TR(348,262)、BR(402,439)、BL(272,388)；右侧面四角为 TL(348,262)、TR(476,154)、BR(530,331)、BL(402,439)。与结构量测的三轴拟合保持一致；低对比点仍有约8–12源像素不确定性，**并非恢复了原作UV**。

正面 eyes 与 teeth 分别放在独立128×160区域；侧面牙齿单列128×160区域。全头正面拟合包含上颅与闭合下颚，不能把整个参考矩形直接当作一个上颅面。模型可把眼骨与头合并、牙骨与颚合并，或依照登记坐标裁取实际透明子范围。`left_eye_local` / `right_eye_local` 是备用局部64×24提取，使用各眼可见四边形，不应与整面eyes重复显示。

每个目标像素中心取 `u=(x+0.5)/width, v=(y+0.5)/height`，以登记3×3单应矩阵映到原图，齐次除法后以 `floor(coord+0.5)` 最近邻取整。仅保留 `R≥230,G≥180,B≥230,alpha≥1` 且位于该部位登记的源矩形/半平面中的像素；保留像素RGBA不变。这个阈值把白/浅粉的亮形核心与软紫色辉光分开，代价是未保留柔光外缘，不伪称逐像素重现原游戏后处理。具体掩码与四角完整写在JSON，不依赖人工再描线。

眼睛源矩形 `[248,292,301,334)` 与 `[322,321,372,364)`；正面牙齿额外使用 `y−0.4x−239.2≥0` 剔除眼睛末端；侧面牙齿仅取 `[389,350,447,420)`。正/侧面拆开，避免在同一张正面贴图上叠入侧齿。纹理所有RGB采样均来自原始 `MCD_Heart_of_Ender.png`，不是本目录预览图。

## 可视化与验证

- [图集与区域标记](atlas_annotated.png)：棋盘只是透明预览背景，不在atlas中。
- [星窗原位置](star_window_mapping.png)。
- [头部投影四角](head_projection_quads.png)。
- [原渲染与发光形状并排](emissive_source_comparison.png)。
- [64px小人和44px遮罩原样放大](raw_materials_comparison.png)。
- `atlas_audit.json` 记录本脚本的逐RGBA校验。六星窗、遮罩、小人全为原图裁片字节一致；发光采样每个保留像素都与记录的源坐标RGBA一致。

像素哈希是解码后的逐行RGBA字节SHA-256，与PNG容器文件哈希不同；两种在JSON分别记录。区域不重叠，所有UV矩形在512×512内。尚未在Minecraft实测半透明、混合排序、mipmap和发光效果；这些不能由静态图集校验代替。

复现：仓库根目录运行 `python _tools/heart_of_ender_atlas.py`。只重建本目录，不改任何原始素材、其他怪或共用管线。
'''
    (OUT/'TEXTURE_NOTES.md').write_text(notes, encoding='utf-8')
    print('atlas512: %d regions, exact raw copies and retained sampled pixels verified' % len(regions))
    print('visible light pixels:', {r['name']: r['visible_pixels'] for r in regions if r['kind']=='projection_extract'})
    arch_uv_study()


if __name__ == '__main__':
    main()
