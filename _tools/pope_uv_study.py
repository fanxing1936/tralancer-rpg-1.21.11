#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""教皇 M1：只分析原像素与 UV 候选，不生成模型/图集/动画。

输出限于 pope_ref/m1/uv；绝不写 heart_of_ender_ref。
"""
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REF = HERE / 'pope_ref'
OUT = REF / 'm1' / 'uv'
ARCH = HERE / 'heart_of_ender_ref' / 'MCD_Arch-Illager_(texture).png'
SHADOW = HERE / 'heart_of_ender_ref' / 'MCD_Arch-Illager_(shadow_texture).png'
FONT = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 18)
SMALL = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 14)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def stats(im):
    a = np.array(im.convert('RGBA'))
    colors, counts = np.unique(a.reshape(-1, 4), axis=0, return_counts=True)
    ids = np.argsort(counts)[::-1][:8]
    return {'size': list(im.size), 'rgba_sha256': sha(a.tobytes()),
            'alpha_values': np.unique(a[:, :, 3]).tolist(),
            'opaque_pixels': int((a[:, :, 3] == 255).sum()),
            'transparent_pixels': int((a[:, :, 3] == 0).sum()),
            'partial_alpha_pixels': int(((a[:, :, 3] > 0) & (a[:, :, 3] < 255)).sum()),
            'top_rgba': [{'rgba': colors[i].tolist(), 'count': int(counts[i])} for i in ids]}


def checker(size, cell=4):
    out = Image.new('RGBA', size, '#3f4651')
    d = ImageDraw.Draw(out)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x//cell + y//cell) % 2:
                d.rectangle((x, y, x+cell-1, y+cell-1), fill='#59616e')
    return out


def preview(im, factor):
    bg = checker(im.size)
    bg.alpha_composite(im.convert('RGBA'))
    return bg.resize((im.width*factor, im.height*factor), Image.Resampling.NEAREST).convert('RGB')


def region(key, label, rect, evidence, note):
    return {'id': key, 'label': label, 'rect': rect, 'evidence': evidence, 'note': note}


def candidate(key, label, faces, dims, proof, cautions):
    return {'id': key, 'label': label, 'candidate_dimensions_whd': dims,
            'source': 'arch', 'faces': faces, 'official_uv_recovered': False,
            'evidence': proof, 'cautions': cautions}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sources = {'arch': ARCH, 'shadow': SHADOW,
               'staff': REF/'T_SuperStaff.png', 'cube': REF/'T_SuperCube.png'}
    images = {k: Image.open(p).convert('RGBA') for k, p in sources.items()}
    source_data = {}
    for key, path in sources.items():
        source_data[key] = {'path_relative_to_tools': path.relative_to(HERE).as_posix(),
                            'file_sha256': sha(path.read_bytes()), **stats(images[key])}
    # 仅将人工判断写成显式候选；原像素统计由代码独立计算。
    regions = [
        region('A01', '眼/眉图样候选', [0, 0, 6, 6], '语义推断', '可见暗灰阶梯、灰皮和1个白像素；不能据此认定矩形整体就是一只眼。'),
        region('A02', '灰头上方区域', [6, 0, 36, 6], '像素确认；面名推断', '30×6灰色块；标准12×7×6盒网只需要其中两个12×6端面，额外6×6尚未分配。'),
        region('A03', '灰头侧带候选', [0, 6, 36, 13], '像素确认；语义高置信推断', '36×7灰带；6+12+6+12可闭合盒网，但不含主渲染中的黑白眼纹。'),
        region('A04', '白色小片', [2, 13, 4, 14], '像素确认；语义未定', '2×1纯白；可能与鼻上表面/眼睛有关，不当作任意白材质池。'),
        region('A05', '小灰侧带候选', [0, 14, 8, 18], '像素确认；语义未定', '8×4灰带，可分四块2×4；与鼻2×4×2相容但端面没有独立、无歧义的完整盒网。'),
        region('A06', '连续灰细条', [6, 13, 10, 21], '像素确认；臂语义中置信推断', '4×8灰条；主渲染细灰臂相容。与A05局部重叠，必须注明共享，不能当两个独立岛。'),
        region('A07', '暗青十字网', [10, 13, 22, 22], '像素确认；语义未定', '六块3×3组成十字；可能躯干下方/小部件。主渲染脚是灰白末端与红尖，不宜直接命名蓝鞋。'),
        region('A08', '金红小片', [0, 18, 5, 22], '像素确认；语义未定', '金、红、灰交界，不能因为有红像素就确定为脚尖。'),
        region('A09', '红宝石/金属饰品候选', [17, 19, 22, 23], '语义中高置信推断', '红色2×2核心及金色外圈与项链吊坠相容，原几何前后/侧面UV未取得。'),
        region('A10', '金属环/饰品候选', [22, 16, 25, 20], '语义中置信推断', '3×4金色矩形有透明孔；与金属项链相容，不能填孔。'),
        region('A11', '内衣上片', [5, 22, 14, 27], '像素确认；语义中置信推断', '9×5绿片，和下方侧带相接。'),
        region('A12', '躯干服装侧带', [0, 27, 27, 36], '像素确认；语义中高置信推断', '27×9蓝金绿侧带；胸前绿色夹金边支持front候选，后蓝面没有唯一左右分界。'),
        region('A13', '内衣下片', [5, 36, 14, 40], '像素确认；语义中置信推断', '9×4绿片；与A11深度不相等，不能声称标准9×9×5盒网。'),
        region('A14', '高金冠', [36, 4, 52, 15], '像素确认；语义高置信推断', '四块4×11侧面；含红/蓝宝石的一块[36,4,40,15]对应主渲染冠正面。'),
        region('A15', '金冠顶环', [40, 0, 44, 4], '像素确认；语义高置信推断', '4×4金环，中心2×2透明；是空心冠口，不能补实。'),
        region('A16', '蓝金细长饰片', [52, 0, 60, 15], '像素确认；语义未定', '每4列为3蓝+1金，连续15行；可能袖口/袍边折片，不能用UV15高认定手臂15长。'),
        region('A17', '蓝袍左片', [32, 15, 38, 29], '像素确认；语义中置信推断', '蓝金长片带灰白上下边；右缘部分透明，不能画成实心长方体。'),
        region('A18', '蓝袍大片', [42, 15, 59, 29], '像素确认；语义中置信推断', '蓝金/白边与不规则透明区，可能含前片、侧片与背片，不能整体命名背面。'),
        region('A19', '袍区透明缺口', [38, 16, 42, 29], '像素确认', '全透明4×13；接邻的1px边缘并不全透明；不能用这块填内衬。'),
    ]
    candidates = [
        candidate('head_shell', '灰头外壳（不含独立眼眉）',
                  {'north':[6,6,18,13], 'east':[18,6,24,13], 'south':[24,6,36,13],
                   'west':[0,6,6,13], 'up':[6,0,18,6], 'down':[18,0,30,6]}, [12,7,6],
                  '六个矩形的尺寸满足12×7×6盒网；主渲染为宽头、短面高。',
                  ['灰侧带纹样不能唯一证明前后/左右；候选方向不是官方恢复。',
                   '不能漏掉眼眉；A01如何拆到眼眉几何需M2两个方案比较。']),
        candidate('crown', '高金冠四壁与顶环',
                  {'north':[36,4,40,15], 'east':[40,4,44,15], 'south':[44,4,48,15],
                   'west':[48,4,52,15], 'up':[40,0,44,4], 'down':None}, [4,11,4],
                  '16×11侧带分四个4×11，4×4空心顶环；主渲染红/蓝宝石列位于冠正面。',
                  ['正面归属有纹样证据；左右/背顺序和各面转向仍是候选。',
                   '底面无可证明原岛，先texture=null；透明口保留，不添加半透明。']),
        candidate('nose_sides', '鼻部四侧候选',
                  {'north':[2,14,4,18], 'east':[4,14,6,18], 'south':[6,14,8,18],
                   'west':[0,14,2,18], 'up':None, 'down':None}, [2,4,2],
                  '8×4灰矩形可形成四个2×4面；主渲染鼻为前突灰色长方体。',
                  ['上下端面未定，不能借相邻红金像素封面。', 'A04可能是上端面但只有2×1，不能擅称2×2。']),
        candidate('thin_arm_sides', '细灰臂四侧候选（左右有意共享）',
                  {'north':[7,13,8,21], 'east':[8,13,9,21], 'south':[9,13,10,21],
                   'west':[6,13,7,21], 'up':None, 'down':None}, [1,8,1],
                  '4×8连续灰条可分四个1×8；主渲染可见细灰手臂。',
                  ['无独立端面证据；若M2复用条端1px必须记录为明确复用。',
                   '1×8 UV不强制几何长度；手的朝向由原图/动图约束，不由贴图猜。']),
        candidate('dark_teal_box', '暗青3×3×3盒网（部位未定）',
                  {'north':[13,16,16,19], 'east':[16,16,19,19], 'south':[19,16,22,19],
                   'west':[10,16,13,19], 'up':[13,13,16,16], 'down':[13,19,16,22]}, [3,3,3],
                  '六块3×3构成完整十字网，尺寸关系可复核。',
                  ['完整盒网不等于鞋；主渲染鞋末端灰白+红，暂不分配给鞋。']),
        candidate('torso_candidate', '内衣/躯干六面工作候选',
                  {'north':[5,27,14,36], 'east':[14,27,19,36], 'south':[19,27,27,36],
                   'west':[0,27,5,36], 'up':[5,22,14,27], 'down':[5,36,14,40]}, None,
                  '前候选含绿色中心和金边，与参考开襟区域相容；所有采样坐标可复查。',
                  ['前宽9、后宽8、上下深5/4，不是严格标准盒网。',
                   '侧面方向和裁切边界仍需M2前后视图比较；不能称全部恢复。']),
    ]
    staff = {
        'id':'staff', 'source':'staff', 'official_uv_recovered':False,
        'rod': {'candidate_dimensions_whd':[1,18,1],
                'faces':{'north':[0,0,1,18], 'east':[1,0,2,18], 'south':[2,0,3,18],
                         'west':[3,0,4,18], 'down':[0,18,1,19], 'up':None},
                'evidence':'四条1×18像素列；灰5行、红7行、灰5行、金1行；唯一额外金色1×1在[0,18,1,19]。',
                'caution':'四条侧面的循环起点未证实；顶端被托盘遮挡，无独立顶端岛，不任意补色。'},
        'collar': {'candidate_dimensions_whd':[3,1,3],
                   'faces':{'up':[5,1,8,4], 'north':[5,0,8,1], 'south':[5,4,8,5],
                            'west':[4,1,5,4], 'east':[8,1,9,4], 'down':[9,1,12,4]},
                   'evidence':'透明背景勾出精确3×3中心、四条3×1边和第二3×3端面；面积30=2×9+4×3。',
                   'caution':'up/down可交换，第二3×3面含中心深灰像素，可能为接杆凹点。左右边UV为1×3，转到Java矩形面时要旋转90°；最终方向须M2核验。'},
    }
    cube = {'id':'staff_cube', 'source':'cube', 'official_uv_recovered':False,
            'source_rect':[0,0,32,32], 'candidate_faces':{f:[0,0,32,32] for f in ('north','east','south','west','up','down')},
            'evidence':'T_SuperCube是32×32全不透明彩色橙黄渐变；无六面独立岛。图库称The texture of the cube，权杖渲染顶部可见斜放方块。',
            'status':'顶部方块材质的高置信候选；全图六面复用是工作映射，不是原UV证明。',
            'cautions':['不是黑白发光遮罩，不能将其整图当半透明光晕。',
                        '无发光参考渲染颜色受光照影响；原RGBA不能重着色追黄绿。',
                        '发光骨骼可预留，但发光强度/哪些面发光没有仅凭此贴图证明。']}
    for r in regions:
        r['pixel_stats'] = stats(images['arch'].crop(tuple(r['rect'])))
    for c in candidates:
        c['face_pixel_stats'] = {f: stats(images[c['source']].crop(tuple(rect)))
                                 for f,rect in c['faces'].items() if rect is not None}
    for part in ('rod','collar'):
        staff[part]['face_pixel_stats'] = {f:stats(images['staff'].crop(tuple(rect)))
                                         for f,rect in staff[part]['faces'].items() if rect is not None}
    eye_pieces = [
        {'id':'brow_vertical', 'label':'眉竖块', 'rect':[4,2,6,4],
         'pixel_fact':'2×2，4个像素均为(57,57,57,255)'},
        {'id':'brow_horizontal', 'label':'眉横块', 'rect':[2,4,6,5],
         'pixel_fact':'4×1，4个像素均为(57,57,57,255)'},
        {'id':'eye_strip', 'label':'眼横条', 'rect':[3,5,6,6],
         'pixel_fact':'3×1，左到右为(37,37,37,255)、(37,37,37,255)、(255,255,255,255)'},
    ]
    for p in eye_pieces:
        p['pixel_stats']=stats(images['arch'].crop(tuple(p['rect'])))
    eye_candidate = {'source':'arch', 'outer_rect':[0,0,6,6],
        'official_uv_recovered':False, 'status':'M1二维裁片候选，未做眼眉几何、UV朝向或3D模型',
        'pieces':eye_pieces, 'retained_pixel_count':11, 'excluded_background_pixel_count':25,
        'evidence':'原像素确认三块共11px；外侧竖眉接向内横眉、黑眼横条带一白端，可与主渲染眼眉外形作比较。',
        'candidate_options':['A：三块各自保留原UV，在几何中分别定位；两眼镜像几何或UV端点，须M2核验白眼端方向。',
                             'B：三块使用相同原像素，但镜像另一侧方向，作为M2眼睛左右朝向对照；未提前决定。'],
        'cautions':['整块A01有25px不透明(43,43,43,255)背景，直接贴6×6会出现深灰矩形，不能视作透明眼片。',
                    '小图的透明区域仅为展示未选像素；未来本体图集仍保存完整原64×64，不修改源alpha。',
                    '三块是否原作独立mesh、厚度、眉角和实际旋转尚未取得，不声称官方拓扑。']}
    data = {'schema_version':1, 'stage':'M1：可追溯UV研究，不是最终映射',
            'coordinate_convention':'原PNG像素，左上为(0,0)，矩形[u0,v0,u1,v1)右下界不含；Java north=-Z/east=+X/south=+Z/west=-X/up=+Y/down=-Y。候选面方向非官方事实。',
            'sources':source_data, 'regions':regions, 'box_candidates':candidates,
            'staff':staff, 'cube':cube, 'eye_candidate':eye_candidate,
            'unresolved':['眼眉几何与A01的面裁切/镜像', '鼻上下端面', '左右手末端面与朝向',
                          '袍A17/A18的前后侧拆分与袖口A16语义', '腿、白鞋、红脚尖逐面绑定',
                          '项链环、吊坠六面与厚度', '托盘上下方向', '方块全图六面复用/方向及发光'],
            'atlas_plan':{'size':[128,64], 'rects':{'arch':[0,0,64,64], 'staff':[64,0,96,32], 'cube':[96,0,128,32]},
                          'status':'仅布局计划，M1不生成图集或模型。全原图1:1复制，无重采样/重着色；shadow只归档不默认作为发光层。'},
            'no_model_or_animation_generated':True}
    (OUT/'uv_map.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    # 像素网格：源像素在放大图中原样保留，只叠网格和坐标。
    for key in ('arch','staff','cube'):
        im=images[key]; fac=16 if key=='arch' else 24
        margin=44
        canvas=Image.new('RGB',(im.width*fac+margin,im.height*fac+margin),(27,31,39))
        canvas.paste(preview(im,fac),(margin,margin)); d=ImageDraw.Draw(canvas)
        for x in range(im.width+1):
            px=margin+x*fac
            d.line((px,margin,px,margin+im.height*fac),fill=(80,85,95),width=1)
            if x%2==0 and x<im.width:d.text((px+1,8),str(x),font=SMALL,fill='white')
        for y in range(im.height+1):
            py=margin+y*fac
            d.line((margin,py,margin+im.width*fac,py),fill=(80,85,95),width=1)
            if y%2==0 and y<im.height:d.text((8,py+1),str(y),font=SMALL,fill='white')
        canvas.save(OUT/(key+'_pixel_grid.png'))
    # 在不重复存源图的前提下，输出来源分析注释图。
    panel=Image.new('RGB',(1650,1130),(27,31,39)); panel.paste(preview(images['arch'],16),(20,65));d=ImageDraw.Draw(panel)
    d.text((20,16),'原64×64像素区域核对｜框只表示来源范围，不表示官方UV已恢复',font=FONT,fill='white')
    colors=['#ffad75','#83d9ff','#e3e379','#ac9cff','#83efaa','#ffa0d0']
    for i,r in enumerate(regions):
        col=colors[i%len(colors)]; x0,y0,x1,y1=r['rect']
        d.rectangle((20+x0*16,65+y0*16,20+x1*16-1,65+y1*16-1),outline=col,width=2)
        d.text((1070,55+i*53),r['id']+' '+r['label'],font=FONT,fill=col)
        d.text((1070,79+i*53),str(r['rect'])+'  '+r['evidence'],font=SMALL,fill='#c8d2e0')
    d.text((25,1065),'深灰 #2b2b2b 是原图不透明像素，不是自动许可使用的内衬；棋盘仅表示alpha=0。',font=FONT,fill='white')
    panel.save(OUT/'arch_regions_annotated.png')
    # 眼眉最小采样证据图：裁片的位置和颜色均来自原图；不是模型贴图。
    eye_sheet=Image.new('RGB',(1280,640),(27,31,39));d=ImageDraw.Draw(eye_sheet)
    d.text((20,16),'A01眼眉拆分候选｜只展示原像素，不是已确认UV或3D模型',font=FONT,fill='white')
    d.text((20,58),'完整A01 [0,0,6,6]：36px全部不透明',font=SMALL,fill='#ffce70')
    eye_sheet.paste(preview(images['arch'].crop((0,0,6,6)),48),(20,95))
    d.text((20,402),'其中25px是#2b2b2b背景。',font=FONT,fill='#ffaaaa')
    d.text((20,431),'整块贴出会产生深灰矩形。',font=FONT,fill='#ffaaaa')
    for i,p in enumerate(eye_pieces):
        yy=68+i*124;crop=images['arch'].crop(tuple(p['rect']))
        d.text((350,yy),p['label']+' '+str(p['rect']),font=FONT,fill='#a9dfff')
        eye_sheet.paste(preview(crop,28),(350,yy+30))
        d.text((490,yy+40),'#393939 ×4' if i<2 else '#252525 ×2 + #ffffff ×1',font=SMALL,fill='white')
    cut=Image.new('RGBA',(6,6),(0,0,0,0))
    for p in eye_pieces:
        x0,y0,x1,y1=p['rect'];cut.paste(images['arch'].crop((x0,y0,x1,y1)),(x0,y0))
    d.text((820,58),'只保留三块，仍在源图位置（11px）',font=SMALL,fill='#a9efbe')
    eye_sheet.paste(preview(cut,48),(820,95))
    d.text((820,402),'棋盘=未选择的像素，非新贴图。',font=FONT,fill='#a9efbe')
    d.text((20,504),'M2可比较左右镜像方案；白眼端朝向、眉角、厚度与几何仍待确认。',font=FONT,fill='white')
    d.text((20,536),'未来atlas保留完整原图RGBA；模型的三个面分别引用源矩形，不能把背景改透明来冒充原贴图。',font=FONT,fill='white')
    d.text((20,584),'这张图只建立可审核的11px裁片候选，不证明原作使用三块独立mesh。',font=SMALL,fill='#b8c5d8')
    eye_sheet.save(OUT/'eye_candidates.png')
    allparts=[(c['label'],c['faces'],images[c['source']]) for c in candidates]
    allparts += [('权杖杆身',staff['rod']['faces'],images['staff']),('权杖托盘',staff['collar']['faces'],images['staff'])]
    sheet=Image.new('RGB',(1540,180*len(allparts)+80),(27,31,39));d=ImageDraw.Draw(sheet)
    d.text((15,10),'六面采样候选｜每一格来自列出的原图矩形；空白=未定，不擅自填色',font=FONT,fill='white')
    order=['north','east','south','west','up','down']
    for i,(label,faces,im) in enumerate(allparts):
        y=60+i*180;d.text((10,y),label,font=SMALL,fill='white')
        for j,f in enumerate(order):
            x=285+j*205;rect=faces[f];d.text((x,y),f,font=SMALL,fill='#ffce70')
            if rect:
                crop=im.crop(tuple(rect));fac=max(1,min(160//crop.width,108//crop.height))
                pic=preview(crop,fac);sheet.paste(pic,(x,y+25));d.text((x,y+143),str(rect),font=SMALL,fill='white')
            else:d.text((x,y+50),'未定 / texture=null候选',font=SMALL,fill='#ff9a9a')
    sheet.save(OUT/'face_candidates.png')
    rows=['| ID | 原图矩形 `[u0,v0,u1,v1)` | 可观察事实与限制 |','|---|---|---|']
    rows += ['| '+r['id']+' '+r['label']+' | `'+str(r['rect'])+'` | '+r['note']+' |' for r in regions]
    face_rows=['| 部件候选 | north（-Z） | east（+X） | south（+Z） | west（-X） | up | down |','|---|---|---|---|---|---|---|']
    for label,faces,_ in allparts:
        face_rows.append('| '+label+' | '+' | '.join('`'+str(faces[f])+'`' if faces[f] else '**未定**' for f in order)+' |')
    notes='''# 教皇 M1：原贴图 UV 研究与证据边界

本报告给出原像素坐标、可复核盒网关系、各候选面的采样位置和未定项。**尚未恢复官方逐面UV，不能将候选直接冒充事实来源。** 未取得原始 geometry；64×64颜色图片可以精确定位像素，却不能唯一确定任意三维面的朝向、旋转、镜像或部位归属。M1没有生成 `.bbmodel`、最终图集或动作。

本次使用的是 `../../../heart_of_ender_ref/MCD_Arch-Illager_(texture).png`，不是 `T_ArchIllagerUndressed.png`。已有 `arch_uv_regions.json` 是无外袍版本的工作推断，并明确标注没有原geometry；这里只把它当候选线索，再逐像素核对本次指定原图。没有修改或重复存放共享贴图。

外形证据来自本次指定 `MCD_Arch-Illager.png` 与正面待机动图。主渲染文件页标记有“Fix Z-fighting in arm”：贴近权杖的手臂杂纹是已知重叠问题，不把这处条纹抄进新贴图或认为属于衣料。正面动图里权杖位于画面右，即角色左手（Java `-X`）；M2结构应从 `left_hand` 连接权杖，不能以画面右就误判成角色右手。

## 坐标与复核办法

所有矩形是原PNG像素 `[u0,v0,u1,v1)`，左上原点、右下界不含；UV矩形的宽高等于像素列数、行数。Java面向 `-Z`，north为正脸候选，east为`+X`，west为`-X`。**这些面名是工作分配，不代表原作者的UV命名。** `uv_map.json` 保存每个采样区的RGBA哈希、透明度和颜色统计；`face_candidates.png` 显示每一面的原裁片。图中棋盘只供透明预览，不写入任何材质。

原Arch贴图有2427个不透明 `(43,43,43,255)` 深灰像素；它们不能当作透明空白，也不能任意充作内衬。原图alpha只有0/255，没有半透明。本体贴图必须整张1:1进入未来图集。`shadow_texture`仅核验/归档，不因文件名就当发光图或改变本体颜色。

## 64×64区域表

'''+ '\n'.join(rows)+'''

## 六面候选表

表内每个数都能回到源图。**有坐标只证明采样位置，不自动证明语义和朝向。** 空白项明确未定；不得从被其他部件占用的区域找近似颜色补面。

'''+ '\n'.join(face_rows)+'''

- 灰头可用 `6+12+6+12=36` 的侧带和两个12×6端面构成12×7×6盒网；主渲染支持宽头、短面高。但此侧带没有黑白眼纹，所以必须单独研究A01眼眉，而不能把无眼灰盒称为完成。
- 金冠四个4×11侧面和4×4顶环关系严格成立。A14首面可看见上红下蓝宝石列，与主渲染正面对应，正面语义较强；左右背顺序仍待M2比较。顶环中央2×2透明和齿口透明必须保留。底面未找到独立原岛，暂不封实。
- A05鼻侧带和A06细臂条局部重叠，若两者采用便是**有意共享**，不能宣称独立官方岛。鼻上下端面未定；A04只2×1，不能把它说成2×2。手/臂端面也未定，若M2用端部1px复用，应逐面记录复用来源。
- A07是数学上完整3³十字网，但没有证据证明是鞋。主渲染的脚末端是灰白和红尖，禁止直接套成蓝色大鞋。
- 躯干工作候选的前/后宽9/8、上/下深5/4，不满足单一长方体标准盒网。必须保留这个差异，不能用圆整尺寸掩盖。
- A17/A18蓝袍区域包含透明缺口、白边和金边；各片前后/左右关系尚未唯一确定，不能默认大片就是背面。侧面与背面在M2必须同时检查。

## 眼眉的具体裁片候选

原像素独立复核后，A01可以进一步拆出三块，而不是把整个6×6方块直接贴脸：

| 裁片 | 原图矩形 | 精确RGBA事实 |
|---|---|---|
| 眉竖块 | `[4,2,6,4]` | 2×2，四个像素全部 `(57,57,57,255)` |
| 眉横块 | `[2,4,6,5]` | 4×1，四个像素全部 `(57,57,57,255)` |
| 眼横条 | `[3,5,6,6]` | 3×1，从左到右为两个 `(37,37,37,255)` 和一个 `(255,255,255,255)` |

三块合计11px，构成可检查的弯眉和黑白眼条；A01剩余25px全部是不透明 `(43,43,43,255)` 深灰背景，**直接贴整块6×6会出现深灰底板**。[眼眉裁片小对照](eye_candidates.png) 左侧显示完整A01，中间显示三个原裁片，右侧仅为11px位置示意；棋盘表示未选择像素，不是修改后的模型材质。

此候选可让M2用三个小面分别引用原UV，按参考眼眉轮廓定位。两眼可比较镜像几何/镜像UV端点的两个方向方案，再核对白眼端、外侧竖眉与向鼻侧横眉。**原作是否确实为三块mesh、厚度、旋转与眉角仍未知；没有做模型，也没有认定哪种镜像方案正确。** 未来图集仍保留原64×64完整RGBA，不把背景改透明或重画眼睛。

另有两项外形交叉核对：A07暗青盒网可以优先与主渲染躯干下方的深青下装比较，比“蓝鞋”更合理，但部位和尺寸仍属候选；A17/A18的白边在主渲染金边袖口/袍襟上没有直接对应，因此不能未经侧背核验就全部作为主外袍。

## 权杖32×32贴图

`T_SuperStaff.png` alpha精确勾出两组互不混淆的网：杆身 `[0,0,4,18]` 分四个1×18侧面，顺序为灰5行、红7行、灰5行、金1行；`[0,18,1,19]` 是额外金端面。杆顶端面没有独立岛，可由托盘遮住，不借别处补色。

托盘中心 `[5,1,8,4]` 为3×3；四条边 `[5,0,8,1]`、`[5,4,8,5]`、`[4,1,5,4]`、`[8,1,9,4]`；第二3×3端面 `[9,1,12,4]`。总面积 `2×9+4×3=30`，与3×1×3薄板六面严格一致。第二端面含深灰中心，可能是接杆处；上下两面仍需参考几何验证，不装作已知。左右UV矩形是1×3，最终映射到薄板边面必须核对90°旋转。

`T_SuperCube.png` 是**全不透明彩色橙黄渐变**32×32，并非黑白发光遮罩，也没有六面独立岛。图库说明仅为“The texture of the cube”；无发光权杖渲染顶部确有斜置方块，因此把它作为顶部方块材质是高置信候选。六面复用全图 `[0,0,32,32]` 只是待比较工作方案，原UV平铺、面方向和发光强度未知。原RGBA不重着色去迎合带光照的黄绿色渲染，也不额外做半透明光晕。发光骨骼先保留结构，不能据此声称发光已复刻。

## 未来单图集布局计划（M1未生成）

计划128×64：本体原图 `[0,0,64,64]`，权杖原图 `[64,0,96,32]`，方块原图 `[96,0,128,32]`。全图1:1原RGBA复制，像素无缩放、无滤波、无调色。模型统一从 `textures[0]` 的base64读取；每个面的图集UV等于本表原UV加对应偏移。shadow仅存档，不默认插入材质或标成emissive。

## M2开始前保留的比较项

1. 眼眉：只用A01能明确定位图样，但裁切、镜像和眉几何未定。M2可摆两种局部方案，与原正面/四分之三逐块比较；不凭连续猜测反复换贴图。
2. 袍/袖/腿：A16–A18的拓扑、白色末端与红脚尖面来源仍未唯一确定。先把能从动图看到的正/侧/背轮廓标清，再做2–3方案；未识别的面不得伪称官方。
3. 鼻/手的端面、项链厚度六面、托盘上下和方块UV方向：先保留未定，最终每个面都必须补上明确矩形和理由，不能用“不明显”跳过。

这份报告不宣称“UV全部解决”。它把精确的像素证据与需要用户确认的重建方案分开，防止重复过去的目测贴图问题。

## 产物与复现

- [区域注释图](arch_regions_annotated.png)
- [原像素网格](arch_pixel_grid.png)
- [六面裁片对照](face_candidates.png)
- [眼眉11px裁片小对照](eye_candidates.png)
- [权杖网格](staff_pixel_grid.png)
- [方块材质网格](cube_pixel_grid.png)
- [机器可读表](uv_map.json)

仓库根目录运行 `python _tools/pope_uv_study.py`。本脚本只写 `_tools/pope_ref/m1/uv/`。原素材版权属于 Mojang；本项目非商业，与 Mojang 无关联。
'''
    (OUT/'UV_MAP.md').write_text(notes,encoding='utf-8')
    # 矩形边界及声明校验；不是语义/视觉还原度测试。
    for c in candidates:
        for rect in c['faces'].values():
            if rect is not None:
                assert 0<=rect[0]<rect[2]<=64 and 0<=rect[1]<rect[3]<=64
    assert source_data['arch']['partial_alpha_pixels']==0
    assert source_data['cube']['opaque_pixels']==1024
    assert regions[-1]['pixel_stats']['transparent_pixels']==52
    print('M1 UV source study: %d regions, %d body candidates, 2 staff nets; unresolved assignments explicitly retained.'%(len(regions),len(candidates)))


if __name__=='__main__':
    main()
