#!/usr/bin/env python3
"""教皇 M2 静态参考取景与像素测量。只写 pope_ref/m2/reference，不生成模型或动作。"""
import hashlib
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REF=Path(__file__).resolve().parent/'pope_ref'
OUT=REF/'m2'/'reference'
BG='#34424f'

def font(n):
    return ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',n)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def composite(im):
    out=Image.new('RGBA',im.size,BG)
    out.alpha_composite(im.convert('RGBA'))
    return out.convert('RGB')

VIEWS=[
 {'id':'front','label':'正面 / 王座坐姿','source_file':'Arch-Illager_sit_in_his_throne_room_front_view.jpg','source_frame':None,'source_time_seconds':None,'crop_bbox':[710,145,1175,770],'character_bbox_estimate':[712,150,1163,765],
  'candidate_camera':{'yaw_degrees':0,'yaw_error_degrees':10,'pitch_down_degrees':5,'pitch_error_degrees':10,'projection':'透视截图；非严格正交'},
  'pose':'坐姿，双臂较高，腿朝前；不能直接用于站姿腿角度验收','evidence':'高分辨率眉眼、鼻、冠正面红蓝宝石与项链；权杖在画面右=角色左手','occlusion':'王座与持杖手遮挡身体边界，头画面右缘受杖杆遮挡，不能把可见宽度当完整头宽'},
 {'id':'side','label':'侧面 / 转身动态','source_file':'MCD_Arch-Illager_Summon_Circle.gif','decoded_frame':'m1/motion/frames/summon/0013.png','source_frame':13,'source_time_seconds':0.52,'crop_bbox':[198,123,376,373],
  'candidate_camera':{'yaw_degrees':90,'yaw_error_degrees':15,'pitch_down_degrees':25,'pitch_error_degrees':15,'projection':'渲染图近侧视，身体自身在转动/前倾，不能唯一分离相机角与姿态角'},
  'pose':'施法转身，躯干前倾、披摆后扬，非静态正交侧面','evidence':'头深度、鼻凸出方向、后布与白下缘、细金腿和红尖分离','occlusion':'权杖和手臂存在重叠，背布掀起使自然下垂长度不可直接量取'},
 {'id':'back','label':'背面 / 瞬移动态','source_file':'MCD_Arch-Illager_Teleport_(Appear_Short).gif','decoded_frame':'m1/motion/frames/teleport/0038.png','source_frame':38,'source_time_seconds':1.52,'crop_bbox':[129,201,316,409],
  'candidate_camera':{'yaw_degrees':180,'yaw_error_degrees':15,'pitch_down_degrees':20,'pitch_error_degrees':15,'projection':'近背视，动态旋转/俯仰，非严格正交'},
  'pose':'瞬移离场转身，后布掀起、双脚弯曲，非站姿','evidence':'背头没有正脸眼眉；皇冠背壁无红蓝宝石列；蓝背布和白下缘清楚','occlusion':'腿部分遮挡；原帧主体仅约167×188像素，不宜从放大图补造细节'},
 {'id':'three_quarter','label':'四分之三 / 主外形','source_file':'MCD_Arch-Illager.png','source_frame':None,'source_time_seconds':0.0,'crop_bbox':[53,0,625,999],
  'candidate_camera':{'yaw_degrees':42,'yaw_error_degrees':7,'pitch_down_degrees':23,'pitch_error_degrees':7,'projection':'由头盒边投影反推的正交近似；不是官方相机参数','head_crown_screen_lean_degrees':8,'note':'头/冠竖线倾斜，杖杆近竖直；别把相机或整个模型连杖一起倾斜'},
  'pose':'站立，头与冠轻侧倾；左手持杖，空手自然垂出','evidence':'主要站姿、肩颈紧凑性、冠/头/身体比例和权杖相对尺寸','occlusion':'杖顶遮住一部分头盒后角；金属项链局部藏在下颌下'},
 {'id':'front_gif_support','label':'正面 GIF 辅证','source_file':'MCD_Arch-Illager_Idle_Highblock_Halls_(front_view).gif','decoded_frame':'m1/motion/frames/idle_front/0000.png','source_frame':0,'source_time_seconds':0.0,'crop_bbox':[116,36,364,452],
  'candidate_camera':{'yaw_degrees':0,'yaw_error_degrees':10,'pitch_down_degrees':10,'pitch_error_degrees':10,'projection':'近正面渲染，不是严格正交站姿'},'pose':'王座坐姿','evidence':'再次确认持杖手与眼眉方向','occlusion':'王座遮挡'},
 {'id':'back_three_quarter_support','label':'背侧辅证 / 转身动态','source_file':'MCD_Arch-Illager_Summon_Circle.gif','decoded_frame':'m1/motion/frames/summon/0012.png','source_frame':12,'source_time_seconds':0.48,'crop_bbox':[100,105,400,400],
  'candidate_camera':{'yaw_degrees':145,'yaw_error_degrees':20,'pitch_down_degrees':25,'pitch_error_degrees':15,'projection':'动态背侧渲染，角度只作试拍起点'},'pose':'身体向前、后布后扬','evidence':'背布白下缘与腿相互独立','occlusion':'手臂与头侧部分重叠'},
 {'id':'staff','label':'权杖 / 无发光单独渲染','source_file':'MCD_Arch-Illagers_Staff.png','source_frame':None,'source_time_seconds':None,'crop_bbox':[0,0,342,956],
  'candidate_camera':{'yaw_degrees':45,'yaw_error_degrees':10,'pitch_down_degrees':25,'pitch_error_degrees':10,'projection':'近等轴渲染，方块自身另有旋转'},'pose':'杖杆竖直、托盘水平、顶块斜置','evidence':'托盘与杆粗细，顶块明显大于托盘；不根据光照重绘原色','occlusion':'顶块遮住托盘部分上表面'}
]

SEGMENTS=[
 {'id':'H1','label':'头正面上缘','points':[[95,296],[360,427]],'status':'可见边端点，人工定位约±4px'},
 {'id':'H2','label':'头正面右竖边','points':[[360,427],[334,625]],'status':'可见边端点，人工定位约±3px'},
 {'id':'H3','label':'头顶深度边','points':[[95,296],[228,261]],'status':'后端部分近冠遮挡，约±6px'},
 {'id':'C1','label':'冠正面上缘','points':[[249,45],[335,88]],'status':'前壁可见边，不含上方冠齿，约±4px'},
 {'id':'C2','label':'冠正面右竖边','points':[[335,88],[296,377]],'status':'11高侧壁候选，约±4px'},
 {'id':'N1','label':'鼻前面长边','points':[[212,491],[195,603]],'status':'可见鼻前面边，约±4px'},
 {'id':'S1','label':'杖杆竖直参考','points':[[494,519],[494,995]],'status':'托盘下至杆底，约±4px；不能用图片底差判断穿地'},
 {'id':'S2','label':'托盘投影宽','points':[[430,474],[562,474]],'status':'包围盒横向宽，非同一条几何边，约±3px'},
 {'id':'S3','label':'顶部方块投影宽','points':[[390,360],[615,360]],'status':'包围盒横向宽，非立方体边长，约±3px'}
]

REGIONS=[
 {'id':'R1','name':'高冠外框','bbox':[207,1,423,378],'status':'可见金冠及冠齿，边界约±3px'},
 {'id':'R2','name':'头盒外框','bbox':[68,260,494,626],'status':'被皇冠/权杖遮挡的后角有推定；不是分割mask'},
 {'id':'R3','name':'鼻部','bbox':[152,464,233,605],'status':'可见鼻轮廓，约±3px'},
 {'id':'R4','name':'左持杖臂','bbox':[388,620,496,701],'status':'袖内灰臂至握点，局部遮挡/旧渲染Z-fighting'},
 {'id':'R5','name':'右空手末段','bbox':[63,568,129,650],'status':'灰细臂露出部分，不代表完整臂长'},
 {'id':'R6','name':'项链红宝石','bbox':[179,628,266,714],'status':'含金色镶边的投影外框，非完整项链'},
 {'id':'R7','name':'蓝袍/白下缘区域','bbox':[154,580,374,906],'status':'粗分组边界，含遮挡，禁止当腿/靴的语义分割'},
 {'id':'R8','name':'右侧图中红脚尖','bbox':[251,889,294,917],'status':'可见脚尖像素，约±3px'},
 {'id':'R9','name':'左侧图中红脚尖','bbox':[170,848,235,880],'status':'可见脚尖像素，约±3px'}
]

def source_for(v): return REF/v.get('decoded_frame',v['source_file'])

def main_measures():
    src=Image.open(REF/'MCD_Arch-Illager.png').convert('RGBA')
    im=Image.new('RGB',(1226,1090),'#ede9df');im.paste(composite(src),(0,48))
    d=ImageDraw.Draw(im);d.text((18,8),'主渲染像素测量：原图坐标，不是三维尺寸',font=font(23),fill='#182734')
    colors=['#fc8574','#73d4eb','#c8ec79','#ffc96e','#b7a1f0','#f4a8dc','#9ed9b2','#f9eb8c','#b7d9f4']
    for j,s in enumerate(SEGMENTS):
        xy=[(p[0],p[1]+48) for p in s['points']];d.line(xy,fill=colors[j],width=3)
        for x,y in xy:d.ellipse((x-4,y-4,x+4,y+4),fill=colors[j])
        x,y=xy[0];d.text((x+6,y-24),s['id'],font=font(18),fill=colors[j])
        y=70+j*77;a,b=s['points'];length=math.dist(a,b)
        d.text((682,y),s['id']+' '+s['label'],font=font(20),fill='#182734')
        d.text((682,y+27),f'{a} → {b}',font=font(17),fill='#31485c')
        d.text((682,y+50),f'投影线段 {length:.1f}px',font=font(16),fill='#31485c')
    notes=['头前缘 / 冠前缘 ≈ 3.1','托盘横宽 / 杖顶横宽 = 132 / 225','头冠竖线有侧倾，杖杆几乎竖直','原图冠顶 y≈1，最低脚尖 y≈917','杆底 y≈995；地面深度会改变投影位置','所有人工定位含误差；遮挡后角不能视作实测']
    for i,n in enumerate(notes):d.text((682,790+i*35),n,font=font(17),fill='#182734')
    d.text((15,1055),'原作图像版权属于 Mojang；测量线/标签为本项目分析。没有旋转、拉伸或补画原图。',font=font(18),fill='#182734')
    im.save(OUT/'main_measures.png')
    grid=composite(src);gd=ImageDraw.Draw(grid)
    for x in range(0,666,50):gd.line((x,0,x,999),fill='#8f9ba6');gd.text((x+2,225),str(x),font=font(10),fill='white')
    for y in range(0,999,50):gd.line((0,y,666,y),fill='#8f9ba6');gd.text((2,y+2),str(y),font=font(10),fill='white')
    grid.save(OUT/'main_pixel_grid.jpg',quality=96)

def view_board(views):
    board=Image.new('RGB',(1800,790),'#ede9df');d=ImageDraw.Draw(board)
    d.text((20,12),'M2 四视角原作证据（动态/坐姿参考已标注，非四张正交静态图）',font=font(26),fill='#182734')
    for j,v in enumerate(views[:4]):
        src=Image.open(source_for(v)).convert('RGBA');crop=src.crop(v['crop_bbox'])
        crop.save(OUT/(v['id']+'_source_crop.png'))
        tile=composite(crop);factor=min(420/tile.width,550/tile.height);tile=tile.resize((round(tile.width*factor),round(tile.height*factor)),Image.Resampling.NEAREST)
        x=15+j*450;y=60
        d.rectangle((x,y,x+420,y+550),fill=BG);board.paste(tile,(x+(420-tile.width)//2,y+(550-tile.height)//2))
        d.text((x,y+563),v['label'],font=font(22),fill='#182734')
        line='静态原渲染' if v['source_frame'] is None else f'帧 {v["source_frame"]} / GIF {v["source_time_seconds"]:.2f}s'
        if v['id']=='front': line='原截图；坐姿，不用于腿角度验收'
        d.text((x,y+598),line,font=font(18),fill='#31485c')
        d.text((x,y+630),'原图裁切、等比放大；未旋转',font=font(17),fill='#31485c')
    board.save(OUT/'four_views_source.jpg',quality=95)

def candidates():
    entries=[('summon',i) for i in range(8,18)]+[('teleport',i) for i in range(33,41)]
    im=Image.new('RGB',(1500,1390),'#ede9df');d=ImageDraw.Draw(im)
    d.text((15,15),'M2 侧/背候选：逐格裁边等比放大，未旋转；动态姿态，不是正交静态图',font=font(20),fill='#182734')
    for j,(key,i) in enumerate(entries):
        frame=Image.open(REF/f'm1/motion/frames/{key}/{i:04d}.png').convert('RGBA');frame=frame.crop(frame.getbbox());factor=min(280/frame.width,270/frame.height);frame=frame.resize((round(frame.width*factor),round(frame.height*factor)),Image.Resampling.NEAREST)
        x=(j%5)*300;y=70+(j//5)*330
        tile=Image.new('RGBA',(290,280),BG);tile.alpha_composite(frame,((290-frame.width)//2,(280-frame.height)//2));im.paste(tile.convert('RGB'),(x,y))
        d.text((x+8,y+286),f'{key} 帧{i} / {i*.04:.2f}秒',font=font(18),fill='#182734')
    im.save(OUT/'candidate_side_back.jpg',quality=95)

def front_measures():
    view=VIEWS[0];src=Image.open(REF/view['source_file']).convert('RGBA');bb=view['crop_bbox'];pic=composite(src.crop(bb));im=Image.new('RGB',(pic.width+300,pic.height),'#ede9df');im.paste(pic,(0,0));d=ImageDraw.Draw(im)
    marks=[('冠口',(946,205)),('冠底',(949,422)),('眉',(1014,478)),('鼻端',(948,591)),('吊坠',(941,638)),('角色左握点',(1056,603)),('红脚底',(857,712)),('金色杖底',(1048,757))]
    d.text((pic.width+15,12),'原截图坐标地标',font=font(22),fill='#182734')
    for i,(label,(x,y)) in enumerate(marks):
        xx=x-bb[0];yy=y-bb[1];d.ellipse((xx-3,yy-3,xx+3,yy+3),fill='#ff5555');d.text((xx+5,yy-16),str(i+1),font=font(16),fill='#fff0a0')
        d.text((pic.width+15,60+i*60),f'{i+1}. {label}',font=font(18),fill='#182734');d.text((pic.width+15,85+i*60),f'({x}, {y})',font=font(16),fill='#31485c')
    d.text((pic.width+15,565),'约±5px；不是骨骼锚点',font=font(16),fill='#31485c')
    im.save(OUT/'front_landmarks.png')
    return [{'name':n,'pixel':[x,y],'status':'人工可见特征定位，约±5px；非骨骼pivot'} for n,(x,y) in marks]

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    views=[]
    for raw in VIEWS:
        v=dict(raw);p=source_for(v);im=Image.open(p).convert('RGBA')
        v['source_sha256']=sha(REF/v['source_file']);v['decoded_image_sha256']=sha(p);v['source_canvas']=[im.width,im.height]
        v['alpha_bbox']=list(im.getbbox()) if im.getbbox() else None
        v['bbox_note']='bbox采用[x0,y0,x1,y1)；JPEG alpha_bbox只代表整画布，不代表主体'
        views.append(v)
    for s in SEGMENTS:s['projected_length_pixels']=round(math.dist(*s['points']),3)
    landmarks=front_measures()
    dims=[
        {'part':'head','candidate_xyz_units':[12,7,6],'basis':'M1灰侧带6+12+6+12与主图头/冠前缘比例约3.1','confidence':'重建候选，非官方geometry'},
        {'part':'crown','candidate_xyz_units':[4,11,4],'basis':'M1四个4×11侧面和4×4空心顶环；主图形状相符','confidence':'相对较强，冠齿和底部连接另核'},
        {'part':'nose','candidate_xyz_units':[2,4,2],'basis':'M1侧带2×4与主图细长鼻，端面UV未唯一确定','confidence':'重建候选'},
        {'part':'torso','candidate_xyz_units':[9,9,5],'basis':'图中窄于头，肩下紧接躯干；M1衣料拓扑不满足单一盒网','confidence':'低至中；仅布局起点，不是已证明立方体'},
        {'part':'thin_arm','candidate_xyz_units':[1,8,1],'basis':'M1细灰条与原图细臂；姿态遮挡/透视使完整长度未能直接量取','confidence':'长度待模型并排确认，禁止从可见短段直接定总长'},
        {'part':'staff_shaft','candidate_xyz_units':[1,18,1],'basis':'T_SuperStaff四个1×18侧面及主图杆宽','confidence':'相对较强'},
        {'part':'staff_tray','candidate_xyz_units':[3,1,3],'basis':'T_SuperStaff完整薄板盒网；主图投影宽132px','confidence':'相对较强'},
        {'part':'staff_cube','candidate_xyz_units':[5,5,5],'basis':'主图顶块投影宽225px/托盘132px≈1.70；单杖图342px/171px≈2.0；角度不同，不能直接按比值放大三维尺寸','confidence':'试模尺寸，必须与两个视角比较'},
        {'part':'full_character','candidate_height_units':29,'candidate_model_scale':round(2.6*16/29,6),'basis':'站姿布局假设：脚段约2+躯干约9+头7+冠11；以最后bbmodel冠顶到脚底真实包围盒重新计算','confidence':'布局建议，不能当最终比例验收值'}
    ]
    data={'stage':'M2 静态参考分析，无动画制作','image_coordinate_system':'原图片左上原点，+x向右、+y向下，bbox右下界不含；未旋转原始图片','model_coordinate_system':'Java +Y向上，正脸-Z；角色左手位于-X','camera_note':'所有相机角是试拍起点。动态图自身俯仰/旋转与相机无法唯一分离，不是官方相机参数。',
          'views':views,'main_render_segments':SEGMENTS,'main_render_regions':REGIONS,'front_landmarks':landmarks,'dimension_candidates':dims,
          'ratios':{'head_front_edge_over_crown_front_edge':round(SEGMENTS[0]['projected_length_pixels']/SEGMENTS[3]['projected_length_pixels'],3),'main_cube_bbox_width_over_tray_bbox_width':225/132,'staff_render_cube_bbox_width_over_tray_bbox_width':342/171,'projected_crown_to_red_toe_height_pixels':916},
          'critical_findings':['左手持杖，不以画面右侧误名right_hand','头下沿与肩/项链几乎贴合，不留明显颈间隙','主图头冠有约8度画面侧倾，杖杆近竖直；不把整个模型一起倾斜','连续侧背帧显示白下缘随蓝布后摆，不能直接建成白靴；金细腿/红脚尖独立在其下','没有严格正交静态侧背素材；M2渲染需要四视图，但原参考中只能有条件核验轮廓、材质和部件朝向','杖底与脚底在投影图不同高度不直接证明穿地，深度投影与相机必须先匹配']}
    (OUT/'reference_views.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    main_measures();view_board(views);candidates()
    text='''# 教皇 M2：静态参考取景与比例证据

本目录只整理原作证据，没有修改或生成模型、动画，也没有操作 Blockbench。

![四视角证据](four_views_source.jpg)

## 视角限制

正面采用1920×992王座原截图，冠、脸、项链与左手握杖较清楚，但它是坐姿、轻俯视透视；不能把膝脚角度当站姿要求。正面GIF第0帧作为辅助。

侧面取 Summon_Circle 第13帧（0.52秒）；背面取 Teleport 第38帧（1.52秒）。二者都是转身时刻，衣摆被扬起且腿屈曲。它们支持侧背材质和部件朝向检查，不是正交静态三视图。没有旋转图片来冒充其他视角。所有裁片仅裁切、等比显示，原坐标与裁框写入 `reference_views.json`。

四分之三使用主渲染 MCD_Arch-Illager.png；建议原生Blockbench相机先试 yaw约42°（±7°）、向下俯视约23°（±7°），再匹配头盒可见边。此角度来自投影估计，不是官方参数。主图头/皇冠竖边在画面中侧倾约8°，杖杆基本竖直，不能为贴合头冠而把整个模型或相机连权杖一起斜。

## 比例与布局起点

![主图坐标测量](main_measures.png)

主图头前缘与冠前缘投影长度约297:96≈3.1，支持头宽12、冠宽4的起点。头12×7×6、冠4×11×4、鼻2×4×2来自贴图盒网候选加图像交叉核对，仍不是官方geometry。身体可先按约9宽、9高、5深布局，细灰臂约1截面、8长；这些弱证据项必须看模型并排后再定。

按脚段约2、躯干约9、头7、冠11估计人物高约29模型单位，暂用 `model_scale = 2.6 * 16 / 29 ≈ 1.434483`。最终必须从bbmodel最高冠齿到最低脚端重新量包围盒，不能照抄这个试模值。

杖杆1×18×1、托盘3×1×3与原权杖UV较一致；主图顶部块的投影宽约225px，托盘约132px，比约1.70。单杖图顶块/托盘投影宽约342/171=2.0，差异来自方块自身朝向与视角。顶块可先试边长5，再同时核对两个渲染；投影包围盒比值不能直接当三维边长比。

## 骨架与衣摆

- 角色左手持杖（Java -X）；图中右侧不是角色右手。
- 头、肩、项链相接很紧，不能做长脖颈或把肩远离头下沿。主图持杖灰臂从约(390,625)直接连向约(494,682)握点；这些是图像地标，不是骨骼pivot。
- Summon_Circle帧11–13和Teleport帧36–38连续显示：白色下缘随蓝色后布一起摆动；细金腿与红脚尖独立露在下方。因此不要把主图所有灰白下端直接当白靴，先把白边和袍/背布一起核验。这是连续帧支持的结构推断，不声称已取得原拓扑。
- 背面冠壁无正面的红蓝宝石列，背头无眼眉。背布朝身体后方，白下缘向下；侧背图必须一同检查，避免正反装错。
- 杖底在主图比脚尖投影低约80px；深度投影会改变同一地平面的画面高度，不能由这点直接把模型杖杆埋入地面。

## 机器可读产物

`reference_views.json` 包含原文件哈希、帧号、源时间、原画布、alpha边界、取景框、相机候选与误差、姿态/遮挡说明、像素线段、比例和尺寸建议。图中坐标全部以未裁切原图为准。`front_landmarks.png` 标出正面头冠/鼻/吊坠等地标，但它们不是骨骼锚点。

运行：`python _tools/pope_m2_reference.py`。只写本目录；原作图像版权归 Mojang，本项目非商业，与 Mojang 无关联。
'''
    (OUT/'REFERENCE_README.md').write_text(text,encoding='utf-8')
    print('已生成四视角证据、像素测量、reference_views.json；未操作模型和动画。')

if __name__=='__main__':main()
