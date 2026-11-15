#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M2衣袍/袖筒/腿脚的可执行UV候选；不生成最终bbmodel。"""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
REF=HERE/'pope_ref'
OUT=REF/'m2'/'uv_study'
SOURCE=HERE/'heart_of_ender_ref'/'MCD_Arch-Illager_(texture).png'
F=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',19)
S=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',15)

def face(surface, rect, notes, flip_u=False, flip_v=False):
    x0,y0,x1,y1=rect
    return {'surface':surface,'source_rect':rect,
            'bb_uv':[x1 if flip_u else x0,y1 if flip_v else y0,
                     x0 if flip_u else x1,y0 if flip_v else y1],
            'rotation':0,'texture':0,'notes':notes}

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    im=Image.open(SOURCE).convert('RGBA')
    sleeves=[]
    for name,u,sign in [('right_arm',52,1),('left_arm',56,-1)]:
        # CubeFace默认：north U沿-X，south/up/down U沿+X；只翻UV端点。
        faces={
            'up':face('袖筒外顶',[u,3,u+4,6],'源U末1列金边必须在远离躯干的一端；V横跨袖筒。',sign<0),
            'north':face('袖筒外前',[u,6,u+4,9],'同上；north默认U沿-X，因此角色右袖翻U。',sign>0),
            'down':face('袖筒外底',[u,9,u+4,12],'此块暗蓝/暗金与朝下表面相容，面分配仍为重建候选。',sign<0),
            'south':face('袖筒外后',[u,12,u+4,15],'源U末列在外袖口；原作绕轴面序未取得。',sign<0),
            ('west' if sign>0 else 'east'):face('靠肩封帽',[u,0,u+3,3],'3×3蓝色帽，靠躯干一侧，可被身体遮挡。'),
            ('east' if sign>0 else 'west'):{'surface':'袖口中央','source_rect':None,'bb_uv':None,'rotation':0,'texture':None,'notes':'必须开孔，不能贴金色实心方块。'},
        }
        rim={k:face('袖口金色截面-'+k,[u+3,v,u+4,v+1],'明确复用本侧金边中的1px；四根薄壁构成环，中间空。')
             for k,v in [('up',4),('north',7),('down',10),('south',13)]}
        sleeves.append({'bone':name,'source_u':u,'axis':[sign,0,0],
                        'shoulder_point':[sign*3.1,10.8,0], 'cuff_point':[sign*5.8,10.8,0],
                        'outer_cross_section_yz':[3,3],'wall_thickness':0.18,
                        'faces':faces,'cuff_rim_faces':rim,
                        'inner_wall_rule':'内壁明确复用对应外壁裁片，翻转U端点使金列仍在袖口。内壁面向空腔，不增加显示实体。',
                        'evidence':'每套3×3帽+四块4×3壁，共57px；第4列顶部3px是背景、下12px是金边，支持单端开放袖筒。',
                        'status':'候选；外截面与长度按原图紧凑比例，非官方几何。'})
    shorts={f:face('深青短裤-'+f,r,'同一3³盒网被左右两条短裤腿有意共享；summon13可见两块深青裤腿。')
            for f,r in {'north':[13,16,16,19],'east':[16,16,19,19],'south':[19,16,22,19],
                         'west':[10,16,13,19],'up':[13,13,16,16],'down':[13,19,16,22]}.items()}
    leg={f:face('金腿-'+f,r,'四个1×3金色侧面；行19暗金、20–21金色；同网两腿共享。')
         for f,r in {'north':[1,19,2,22],'east':[2,19,3,22],'south':[3,19,4,22],
                     'west':[0,19,1,22],'up':[2,18,3,19],'down':[1,18,2,19]}.items()}
    leg['up']['notes']='1×1灰色(182,182,182)，连接裤内；推断为上端，不把它挪作鞋。'
    leg['down']['notes']='1×1纯红(255,0,0)，与脚板相接；推断为下端。'
    foot={f:face('红脚板-'+f,r,'原图独立1×3纯红条；顶部/底部整条复用，窄侧明确复用条边，不重画红色。')
          for f,r in {'up':[4,18,5,21],'down':[4,18,5,21], 'north':[4,18,5,19],
                      'south':[4,20,5,21], 'east':[4,18,5,21],'west':[4,18,5,21]}.items()}
    robe={f:face('外袍-'+f,r,'从带白领/白下摆的蓝袍区取样；不是鞋。')
          for f,r in {'north':[36,15,44,29], 'west':[32,15,36,29],
                      'east':[43,15,47,29], 'south':[47,15,55,29]}.items()}
    robe['north']['notes']='上段开口4px、下段开口6px，金边随开口变窄；原alpha=0/255完整保留。'
    robe['east']['notes']='与front有意共享u43金缝列；是工作映射，不伪称严格24px无重叠盒网。'
    robe['south']['notes']='8×14，顶有短白领图样、底有2px完整白边；不取u55..59另一个白条。'
    for f in ('up','down'):
        robe[f]={'surface':'外袍-'+f,'source_rect':None,'bb_uv':None,'texture':None,'rotation':0,
                 'notes':'外袍为空心薄片，不用完整上下盖堵住脖子或裤腿。薄片厚度边可明确复用本片最外1px，不跨未知区。'}
    torso={f:face('内衣上身-'+f,r,'A11–A13工作六面；source宽高含不一致边界，几何以参考体型为准。')
           for f,r in {'north':[5,27,14,36], 'east':[14,27,19,36], 'south':[19,27,27,36],
                       'west':[0,27,5,36], 'up':[5,22,14,27], 'down':[5,36,14,40]}.items()}
    nose={f:face('鼻-'+f,r,'M2原生渲染复核后修正：2×4×1完整28px盒网；6..10灰条属于手臂，不混入鼻。')
          for f,r in {'north':[2,14,4,18], 'south':[0,14,2,18],
                      'east':[4,14,5,18], 'west':[5,14,6,18],
                      'up':[2,13,4,14], 'down':[2,18,4,19]}.items()}
    pendant={f:face('吊坠-'+f,r,'2×2×1完整16px盒网；正面只贴红白2×2宝石，金为实体侧/顶/背，不取43灰背景角。')
             for f,r in {'north':[18,20,20,22], 'west':[17,20,18,22],
                         'east':[20,20,21,22], 'up':[18,19,20,20],
                         'down':[18,22,20,23], 'south':[21,20,23,22]}.items()}
    data={'schema_version':1,'stage':'M2局部重建候选，不是最终bbmodel',
          'source_file':SOURCE.relative_to(HERE).as_posix(),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
          'coordinate_system':'+Y上，面向-Z；right_arm在+X，left_arm在-X；地面Y=0。source_rect为原64×64像素半开矩形。',
          'uv_rule':'bb_uv已包括端点翻转，rotation始终0。display_mob.py忽略face.rotation，不可依赖90度UV字段。所有rect需加图集偏移，本体建议offset=(0,0)。',
          'sleeves':sleeves, 'shorts_faces':shorts, 'leg_faces':leg,'foot_faces':foot,
          'robe_faces':robe,'torso_faces':torso,'nose_faces':nose,'pendant_faces':pendant,
          'native_review_corrections':{
              'nose_geometry_whd':[2,4,1], 'nose_evidence':'2×8+2×4+2×2=28px；正面165灰，背57灰，两侧182灰，上230白，下182灰。图中黑鼻侧来自把背面57灰误贴侧面。',
              'pendant_geometry_whd':[2,2,1], 'pendant_evidence':'2×4+4×2=16px；不透明43背景只在网外角，整5×4上脸产生黑角。',
              'sleeve_note':'首版金边方向正确但0.15壁厚像线框；可在0.3~0.4中取0.35试贴近参考，不改原纹理。',
              'hand_staff_note':'首版left_hand与staff_rod的X/Z边界完全一致，四侧共面导致Z-fighting；灰握块X/Z向外各扩0.04~0.06或裁掉相交面，不能复制原参考已知缺陷。'},
          'geometry_recommendation':{
              'torso':{'from':[-3.1,6,-1.75],'to':[3.1,12,1.75]},
              'robe':{'outer_from':[-4,1.6,-2.02],'outer_to':[4,12,2.02], 'thickness':0.16,
                      'split':'body拥有front/side薄片；cape拥有back薄片；正面透明开口不能被其它填充面挡住。'},
              'legs':[{'side':side,'center_x':sign*1.7,
                       'shorts_from':[sign*1.7-1.5,3.08,-1.5],'shorts_to':[sign*1.7+1.5,6.08,1.5],
                       'leg_from':[sign*1.7-.5,.08,-.5],'leg_to':[sign*1.7+.5,3.08,.5],
                       'foot_from':[sign*1.7-.5,0,-2.5],'foot_to':[sign*1.7+.5,.08,.5]}
                      for side,sign in [('right',1),('left',-1)]],
              'head_interface':'建议头底Y=12、12×7×6头至Y=19，冠11高至Y≈30；整体model_scale≈2.6*16/30=1.3867，最终须依bbmodel实测总高。',
              'status':'坐标为开始建模的紧凑工作尺寸，非原模型恢复；须由原图并排渲染修正。'},
          'alternatives':[
              {'id':'A','label':'首选：金腿+薄红脚板、空心袖、环绕蓝白外袍',
               'details':'使用以上所有精确rect；外袍前面透空，背面白领/白边由summon11支持。'},
              {'id':'B','label':'仅用于背袍UV宽度歧义的比较',
               'overrides':{'robe_south_source_rect':[46,15,55,29]},
               'details':'背UV用9×14而非8×14，几何宽保持8；移动白领横向比例而不改变原像素。只比较背面，不连带改腿脚或换色。',
               'reason':'此段非完美标准盒网，back起点46或47不能仅靠纯蓝连续纹样唯一确定；A更符合8宽主体与居中短白领。'}],
          'evidence_frames':[{'clip':'summon','frame':11,'time':.44,'features':'背袍白领、蓝背、整条白下摆'},
                             {'clip':'summon','frame':13,'time':.52,'features':'两条深青短裤、金腿、红色前伸薄脚板'},
                             {'clip':'summon','frame':24,'time':.96,'features':'背袍侧厚与袖筒开口、金色袖边'}],
          'not_generated':['最终bbmodel','动画','接入文件','新材质色彩']}
    for group in [shorts,leg,foot,robe,torso,nose,pendant]+[s['faces'] for s in sleeves]+[s['cuff_rim_faces'] for s in sleeves]:
        for record in group.values():
            if record['source_rect'] is not None:
                crop=im.crop(tuple(record['source_rect']))
                record['rgba_sha256']=hashlib.sha256(crop.tobytes()).hexdigest()
    (OUT/'geometry_uv_candidates.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    # 关键局部图按原像素放大，用于用户核对。
    sheet=Image.new('RGB',(1360,1040),'#1e242d');d=ImageDraw.Draw(sheet)
    d.text((20,15),'M2 衣袍 / 袖筒 / 腿脚：原像素展开与转身证据',font=F,fill='white')
    for name,rect,xy,factor in [
        ('双袖：3×3帽 + 四块4×3壁',[52,0,60,15],(25,95),21),
        ('腿1×3×1 + 红脚板1×3',[0,18,5,22],(25,490),38),
        ('外袍：前开口 / 金边 / 白领白下摆',[32,15,55,29],(240,95),20),
        ('深青裤腿：3³盒网',[10,13,22,22],(250,490),23),
    ]:
        crop=im.crop(tuple(rect));bg=Image.new('RGBA',crop.size,'#515a68');bg.alpha_composite(crop)
        sheet.paste(bg.resize((crop.width*factor,crop.height*factor),Image.Resampling.NEAREST).convert('RGB'),xy)
        d.text((xy[0],xy[1]-50),name,font=S,fill='#f7cf78');d.text((xy[0],xy[1]-28),str(rect),font=S,fill='white')
    for i,n in enumerate([11,13]):
        frame=Image.open(REF/'m1'/'motion'/'frames'/'summon'/f'{n:04}.png').convert('RGBA')
        box=frame.getbbox();crop=frame.crop(box);bg=Image.new('RGBA',crop.size,'#37414c');bg.alpha_composite(crop)
        ratio=min(610/crop.width,410/crop.height);pic=bg.resize((int(crop.width*ratio),int(crop.height*ratio)),Image.Resampling.NEAREST).convert('RGB')
        x,y=730,70+i*480;sheet.paste(pic,(x,y));d.text((x,y+415),f'summon {n:03d} / {n*.04:.2f}s 原帧',font=F,fill='white')
    d.text((20,760),'结论：灰白“靴子”实际是袍边；腿为金色细杆，脚为前伸红薄板。',font=F,fill='white')
    d.text((20,795),'袖口为开放方筒，金边应始终在远离身体的外端。',font=F,fill='white')
    d.text((20,830),'蓝白区域在转身背面直接可见：不能继续标成完全未知。',font=F,fill='white')
    d.text((20,865),'几何尺寸/六面循环次序仍属重建候选，最终靠四视角对照。',font=F,fill='white')
    d.text((20,945),'没有修改原贴图、M1或最终模型；只交原像素证据和可读取候选JSON。',font=S,fill='#bfcce0')
    sheet.save(OUT/'clothes_uv_evidence.png')
    notes='''# M2 衣袍、袖筒与腿脚 UV 反推

本阶段新增证据来自召唤转身原GIF：第11帧0.44秒是背袍，第13帧0.52秒可见两条短裤、金腿和红脚板，第24帧0.96秒可见袍侧和袖口。M1没有确认的若干部位现在获得较强视觉支持；没有修改M1历史报告。

可直接给主模型读取：[geometry_uv_candidates.json](geometry_uv_candidates.json)。每个面包含 `surface`、`source_rect`、`bb_uv`、`rotation`、`texture`、`notes` 及源裁片RGBA哈希。`source_rect` 永远是规范原图范围，`bb_uv` 可以反向，用于镜像端点；两者不是同一概念。

## 先纠正形态

主静态渲染下方两块灰白“鞋”其实是长外袍两侧的白下摆。转身帧13露出真正的两条深青短裤、金色细腿、向前伸出的红色薄脚板。帧11蓝背袍顶端有短白领，底端有整条白边，直接支持A17/A18属于外袍，而不是把白区任意解释成手套或鞋。图见 [原像素与转身证据](clothes_uv_evidence.png)。

## 袖筒（较强展开证据）

左右两组完全对应。第一组u=52，第二组u=56：肩封帽 `[u,0,u+3,3]`；四壁依次 `[u,3,u+4,6]`、`[u,6,u+4,9]`、`[u,9,u+4,12]`、`[u,12,u+4,15]`。每壁4×3，末1列为金边；帽旁第4列是背景。面积9+4×12=57px，支持3×3截面的单端开放方筒，不支持把整块4×15当一条15长手臂。

工作几何截面3×3、轴长2.7（纹理轴长4不强迫几何4长），壁厚0.18；肩点x=±3.1、袖口x=±5.8，y=10.8。金口必须是环，中央可看见灰细臂。四个金色截面各明确复用该侧金边中的1px；内壁复用对应侧壁，不另找未知内衬材质。

**管线只读face.uv，不输出face.rotation。** 因此袖筒原生沿±X建模，四壁U均沿袖轴；角色右袖(+X) north翻U，south/up/down不翻；角色左袖(-X) north不翻，south/up/down翻U。肩帽在右袖west/左袖east，袖口开放面相反。JSON已写端点方向，rotation全部0。面绕轴次序仍是重建候选，暗蓝片优先朝下。若原生沿Y建袖，不能仅设90°UV旋转；须重新组织源像素图集并登记映射。

## 腿脚（较强展开与形态证据）

金腿四侧为 `[0,19,1,22]`、`[1,19,2,22]`、`[2,19,3,22]`、`[3,19,4,22]`；上端候选 `[2,18,3,19]` 灰色182，下端 `[1,18,2,19]` 纯红。旁边独立 `[4,18,5,21]` 是纯红1×3，和转身中的前伸脚板相符。几何建议腿1×3×1，脚板1×0.08×3；腿占后1深度，前2沿-Z伸出。两腿有意共享同网。窄脚侧面明确复用红条边缘，不新画红色。

深青十字网是六块3×3，放到左右各一块3×3×3短裤。两块短裤独立跟随两腿，不合成一个跨裆大盒子。

## 外袍（有明确语义，分界仍有候选）

首选A：west `[32,15,36,29]`，front `[36,15,44,29]`，east `[43,15,47,29]`，back `[47,15,55,29]`。front上段透明开口4px、下段6px，金边随开口变窄；east与front明确共享u43金缝列。back含白领和2px白下摆。不要把u55..59独立白片并到背面。source14高不直接等于模型14高；工作几何宽8、深4.04、长10.4，底Y=1.6、肩Y=12，身体更紧凑。

方案B只把背UV起点改46（9×14），几何宽保持8；用于比较白领宽度与居中位置。纯蓝连续区无法唯一证明back起点46或47，A更符合8宽主体。其他部位不跟着改，避免多个变量同时猜。

上身内衣仍用A11–A13六面候选，工作宽6.2、深3.5、高6，Y=6..12；前面绿色和金边。该网前后9/8、上下5/4差异仍记录，不假装严格标准盒网。外袍是空心薄片，顶底没有完整盖，避免堵住颈/裤腿；front/side可归body，back归cape；透明正面必须真正露出内衣。

头接口推荐底Y=12、头12×7×6至Y=19、冠11至约30。理论model_scale约1.3867使30模型单位≈2.6格；最终应按主模型实际最高/最低点重算。这是供开始建模的坐标，非官方mesh精确尺寸。

原RGBA没有重画或调色；版权属于Mojang，本项目非商业、与Mojang无关联。复现：`python _tools/pope_m2_uv.py`，只写当前研究目录。未生成最终bbmodel或动作。

## 原生首版审查追加：鼻与吊坠完整盒网

首版对照中的黑色鼻侧来自把57灰误放在可见侧面。进一步检查原像素可得到完整 **2×4×1鼻盒网**：north `[2,14,4,18]` 为165灰2×4；south `[0,14,2,18]` 为57灰2×4，应藏于脸内；east `[4,14,5,18]`、west `[5,14,6,18]` 各182灰1×4；up `[2,13,4,14]` 为230白2×1；down `[2,18,4,19]` 为182灰2×1。面积 `2×8+2×4+2×2=28px` 精确闭合。鼻深应为1，不再用2；u6..10连续灰条留给手臂。

吊坠是 **2×2×1小盒**，不能用 `[17,19,22,23]` 整个5×4平面：north `[18,20,20,22]` 为白/红/红/暗红2×2；west `[17,20,18,22]` 与east `[20,20,21,22]` 为金1×2；up `[18,19,20,20]` 与down `[18,22,20,23]` 为金2×1；south `[21,20,23,22]` 为暗金2×2。面积16px，正好是 `2×(2×2+2×1+2×1)`。没有任何43灰背景像素；原参考的金色主要在实体侧/顶面，不额外做黑角或平面金框。精确面定义见JSON `nose_faces`、`pendant_faces`。

袖口首版金边朝外正确；0.15壁厚在原生图像线框，建议先试0.35厚度。持杖手首版与杆在X/Z四侧完全共面：`left_hand [-11.5,10.5,-0.5]..[-10.5,11.5,0.5]`，`staff_rod [-11.5,0,-0.5]..[-10.5,18,0.5]`。渲染出现条纹，不是材质图样；可将灰握块X/Z外扩0.04–0.06或裁掉相交面。这些仅为审查建议，研究脚本没有修改最终模型。
'''
    (OUT/'CLOTHES_UV.md').write_text(notes,encoding='utf-8')
    print(OUT/'geometry_uv_candidates.json')

if __name__=='__main__':main()
