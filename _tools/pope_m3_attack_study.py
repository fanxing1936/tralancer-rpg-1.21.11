"""M3 三个战斗 clip 的原图测量与姿态建议；不修改模型或动画。"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import label
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation

HERE = Path(__file__).resolve().parent
REF = HERE / 'pope_ref'
OUT = REF / 'm3' / 'motion_attack_cast'
FRAMES = REF / 'm1' / 'motion' / 'frames'
KEYS = {
    'attack': [0, 5, 7, 10, 11, 13, 18, 23, 27, 31],
    'summon': [0, 5, 8, 9, 10, 11, 12, 13, 14, 16, 18, 21, 25, 29, 33, 37, 43, 50],
    'cast': [0, 3, 6, 10, 15, 23, 30, 36, 45, 51, 57, 62],
}


def font(size=15):
    for path in ('C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/arial.ttf'):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def components(mask):
    lab, n = label(mask)
    result = []
    for i in range(1, n + 1):
        yy, xx = np.where(lab == i)
        if len(xx) < 5:
            continue
        pts = np.column_stack([xx, yy])
        result.append(dict(area=len(xx), bbox=[int(xx.min()), int(yy.min()), int(xx.max()+1), int(yy.max()+1)],
                           center=np.mean(pts, axis=0).round(3).tolist(), points=pts))
    return sorted(result, key=lambda x: x['area'], reverse=True)


def auto_measure(im):
    a = np.array(im.convert('RGBA')).astype(float)
    r, g, b, alpha = a.transpose(2, 0, 1)
    red = components((alpha > 128) & (r > 120) & (g < 100) & (b < 120) & (r > g * 1.5))
    # 红缠带连通面积大于冠宝石和脚尖，但算法结果仍需在关键帧人工核对。
    shaft = red[0]
    pts = shaft['points']
    cov = np.cov(pts.T)
    vals, vecs = np.linalg.eigh(cov)
    axis = vecs[:, np.argmax(vals)]
    if axis[1] < 0:
        axis = -axis
    pos = pts @ axis
    lo, hi = np.percentile(pos, [1, 99])
    center = np.mean(pts, axis=0)
    ends = [center + axis * (lo-center@axis), center + axis * (hi-center@axis)]
    bright = components((alpha > 128) & (r >= 180) & (g >= 90) & (b >= 125) & (b > .58*r))
    core = bright[0] if bright else None
    return dict(red_band_center=shaft['center'], red_band_bbox=shaft['bbox'],
                red_band_area=shaft['area'], red_band_axis_undirected=axis.round(5).tolist(),
                red_band_axis_endpoints=[p.round(3).tolist() for p in ends],
                staff_core_bright_center=core['center'] if core else None,
                staff_core_bright_bbox=core['bbox'] if core else None,
                status='自动颜色区域测量，中心是可见像素质心，不等同三维骨骼枢轴；关键帧另作人工核对')


def study_sheets():
    OUT.mkdir(parents=True, exist_ok=True)
    all_data = {}
    for clip, keys in KEYS.items():
        entries = []
        for f in range({'attack':32,'summon':51,'cast':63}[clip]):
            im = Image.open(FRAMES / clip / f'{f:04}.png').convert('RGBA')
            m = auto_measure(im)
            m.update(source_frame=f, source_time_seconds=round(f*.04, 3), alpha_bbox=list(im.getbbox()))
            entries.append(m)
        all_data[clip] = entries
        for page in range((len(keys)+5)//6):
            subset=keys[page*6:(page+1)*6]
            sheet=Image.new('RGB',(1500,1060),(32,40,48));draw=ImageDraw.Draw(sheet)
            for j,f in enumerate(subset):
                x0=(j%3)*500;y0=(j//3)*530
                im=Image.open(FRAMES/clip/f'{f:04}.png').convert('RGBA')
                bg=Image.new('RGBA',im.size,(45,54,63,255));bg.alpha_composite(im)
                d=ImageDraw.Draw(bg)
                for x in range(50,500,25):
                    d.line((x,60,x,499),fill=(94,110,119,70),width=1)
                    d.text((x,42),str(x),font=font(11),fill='white')
                for y in range(75,500,25):
                    d.line((45,y,499,y),fill=(94,110,119,70),width=1)
                    d.text((16,y-6),str(y),font=font(11),fill='white')
                m=entries[f]
                for k,col in [('red_band_center','#ffcc00'),('staff_core_bright_center','#66ffcc')]:
                    if m[k] is not None:
                        x,y=m[k];d.ellipse((x-3,y-3,x+3,y+3),outline=col,width=2)
                sheet.paste(bg.convert('RGB'),(x0,y0+30))
                draw.text((x0+10,y0+5),f'{clip}  f{f:03d}  {f*.04:.2f}s  原图坐标',font=font(18),fill='white')
            sheet.save(OUT/f'{clip}_grid_{page+1}.jpg',quality=94)
    write_json(OUT/'pixel_tracks_auto.json',all_data)


def candidate_poses():
    # f, bodyX, bodyYaw(展开), head世界X, head世界Z, crown世界Z,
    # leftArmY/Z, rightArm绝对Z, rightLeg绝对X, leftLeg绝对X,
    # cape局部X, staff局部Y换握, core额外Y, staff世界X/Y/Z
    # 这些是原帧约束下的可执行起始解；不是从原游戏骨架导出的曲线。
    values = {
        'attack': [
            [0,0,0,0,8,8,0,0,-48,0,0,0,0,0,0,0,0],
            [5,6,0,0,1,1,10,-25,0,65,0,-12,6.5,0,35,0,8],
            [7,8,0,0,0,0,10,-25,0,70,0,-15,7,0,40,0,10],
            [10,-8,0,-5,8,8,-80,-5,-35,25,0,-24,5,0,28,0,0],
            [11,-65,0,-28,-4,-4,-85,0,-15,10,-15,-10,1,0,-80,0,-5],
            [13,-75,0,-32,-5,-3,-85,3,-15,10,-12,-8,0,0,-103,0,-15],
            [18,-75,0,-8,-8,-8,-85,3,-15,8,-15,-5,0,0,-117,0,-15],
            [23,-25,0,-3,0,0,-95,0,-35,8,-5,-25,0,0,-60,0,40],
            [27,-3,0,0,8,8,-12,0,-48,0,0,-8,0,0,0,0,-3],
            [31,0,0,0,8,8,0,0,-48,0,0,0,0,0,0,0,0],
        ],
        'summon': [
            [0,0,0,0,8,8,0,0,-48,0,0,0,0,0,0,0,0],
            [5,6,0,0,0,0,10,-25,0,65,0,-12,7,0,40,0,10],
            [8,0,0,-3,16,16,5,-5,-35,20,0,-18,5,0,35,0,-38],
            [9,-10,-25,-8,18,18,0,0,-20,10,-5,-25,3,0,10,-25,-75],
            [10,-25,-80,-15,10,10,0,0,-5,20,-10,-32,1,0,-60,-80,-30],
            [11,-35,-130,-15,5,5,-10,0,10,25,-15,-40,0,0,-80,-130,0],
            [12,-35,-185,-12,-8,-8,-15,0,5,25,-15,-45,0,0,-80,-185,0],
            [13,-40,-235,-15,-8,-8,-35,0,0,20,-10,-45,0,0,-80,-235,0],
            [14,-50,-275,-20,-6,-6,-55,0,-5,15,-5,-35,0,0,-85,-275,0],
            [16,-60,-315,-22,-3,-3,-80,0,-5,12,-10,-20,0,0,-90,-315,0],
            [18,-70,-340,-25,-3,-3,-85,0,-5,10,-10,-15,0,0,-95,-340,-4],
            [21,-75,-360,-30,-5,-3,-85,0,-5,10,-10,-8,0,0,-100,-360,-8],
            [25,-75,-390,-18,-7,-5,-85,0,-5,12,-8,-10,0,0,-92,-390,-8],
            [29,-65,-415,-10,-6,-6,-90,0,-5,12,-10,-15,0,0,-75,-415,0],
            [33,-45,-405,-6,-2,-2,-95,0,-10,10,-8,-25,0,0,-70,-405,25],
            [37,-15,-375,-2,8,8,-80,0,-35,8,-4,-20,0,0,-35,-375,35],
            [43,-2,-360,0,8,8,-10,0,-48,0,0,-5,0,0,0,-360,0],
            [50,0,-360,0,8,8,0,0,-48,0,0,0,0,0,0,-360,0],
        ],
        'cast': [
            [0,0,0,0,8,8,0,0,-48,0,0,0,0,0,0,0,0],
            [3,2,0,0,12,12,-90,0,-48,5,0,-10,1,0,-45,0,30],
            [6,4,0,0,14,14,-85,0,-48,8,0,-20,3,0,0,0,0],
            [10,6,0,0,16,16,-85,0,-48,10,0,-30,3,2,0,0,0],
            [15,8,0,1,17,17,-85,0,-48,10,0,-42,3,4,0,0,2],
            [23,9,0,2,17,17,-85,0,-48,10,0,-50,3,8,0,0,6],
            [30,9,0,2,18,18,-85,0,-48,10,0,-48,3,8.7,0,0,10],
            [36,9,0,2,18,18,-85,0,-48,10,0,-45,3,8,0,0,12],
            [45,8,0,1,16,16,-85,0,-48,8,0,-55,3,7.5,0,0,15],
            [51,6,0,0,13,13,-85,0,-48,7,0,-38,2,5.5,0,0,18],
            [57,3,0,0,10,10,-85,0,-48,4,0,-18,1,5.2,0,0,20],
            [62,0,0,0,8,8,0,0,-48,0,0,0,0,0,0,0,0],
        ],
    }
    out={}
    for clip,rows in values.items():
        out[clip]=[]
        for v in rows:
            f,bx,by,hx,hz,cz,lay,laz,raz,rl,ll,cap,slide,lift,sx,sy,sz=v
            t=round(f*.04/({'attack':1.24,'summon':2,'cast':2.48}[clip])*{'attack':1.25,'summon':2,'cast':2.5}[clip],6)
            pose={
                'body':{'rotation':[bx,by,0],'position':[0,0,0]},
                'head':{'world_rotation':[hx,by,hz]},
                'crown':{'world_rotation':[0,by,cz]},
                'right_arm':{'rotation':[0,0,raz+48]},
                'right_hand':{'rotation':[0,0,0]},
                'left_arm':{'rotation':[0,lay,laz]},
                'left_hand':{'world_rotation':[sx,sy,sz]},
                'right_leg':{'rotation':[rl-bx,0,0]},
                'left_leg':{'rotation':[ll-bx,0,0]},
                'cape':{'rotation':[cap,0,0]},
                'staff':{'position':[0,slide,0]},
                'staff_glow':{'position':[0,lift,0],'rotation':[0,90*t,0]},
            }
            out[clip].append(dict(time=t,source_frame=f,source_time_seconds=round(f*.04,3),pose=pose,
                                  evidence='有动图；3D欧拉、深度、幅度为需原生并排验收的数值起始解'))
    write_json(OUT/'action_poses_candidates.json',out)
    return out


def calibrate_cameras():
    p=np.array([[6,19.5,-3],[-6,19.5,-3],[6,12.5,-3],[-6,12.5,-3],[6,19.5,3],[-6,19.5,3]],float)
    pivot=np.array([0,12.5,0]);p=(p-pivot)@Rotation.from_euler('z',8,degrees=True).as_matrix().T+pivot
    corners={
        'attack':[[198,198],[270,235],[189,255],[261,291],[229,190],[301,227]],
        'summon':[[223,202],[292,237],[215,254],[284,289],[253,193],[322,228]],
        'cast':[[187,206],[292,260],[175,287],[280,339],[233,195],[339,247]],
    }
    results={}
    for clip,q in corners.items():
        def proj(v):
            yaw,pitch=np.radians(v[:2]);s,tx,ty=v[2:]
            mat=np.array([[-np.cos(yaw),0,np.sin(yaw)],[-np.sin(pitch)*np.sin(yaw),-np.cos(pitch),-np.sin(pitch)*np.cos(yaw)]])
            return p@mat.T*s+[tx,ty]
        fit=least_squares(lambda v:(proj(v)-q).ravel(),[44,20,9,240,400])
        yaw,pitch,s,tx,ty=fit.x
        results[clip]=dict(source_frame=0,source_time_seconds=0,source_head_six_corners=q,
                           head_model_corners_before_rest=[[6,19.5,-3],[-6,19.5,-3],[6,12.5,-3],[-6,12.5,-3],[6,19.5,3],[-6,19.5,3]],
                           head_rest_rotation=[0,0,8],camera_yaw_degrees=round(yaw,5),camera_pitch_down_degrees=round(pitch,5),
                           pixels_per_model_unit=round(s,6),world_origin_pixel=[round(tx,5),round(ty,5)],
                           pixel_rmse=round(float(np.sqrt(np.mean(fit.fun**2))),5),
                           predicted_corners=proj(fit.x).round(3).tolist(),
                           status='最终模型头盒比例与源首帧近静息姿态假设下的正交拟合；不是官方相机参数')
    results['walk_advisory']=dict(source_frame=0,camera_yaw_degrees=43,camera_pitch_down_degrees=19,pixels_per_model_unit=10.6,
        status='低置信试拍值；f0头有动作且杖遮住两个前上角，不能应用静息6角假设；未提供虚构RMSE')
    write_json(OUT/'camera_calibration.json',dict(projection='uv = scale * P * world + origin; P=[[-cos(yaw),0,sin(yaw)],[-sin(pitch)*sin(yaw),-cos(pitch),-sin(pitch)*cos(yaw)]]',cameras=results))
    return results


def manual_constraints():
    # 原画布像素；不明确或被头/身体挡住的杆底/手点写 null，不用外推代替观测。
    # 每项: 帧, 头盒可见轮廓中心代理, 杆底, 托盘/杆上端, 左手握点, 右手端点。
    raw={
        'attack':[
            [0,[248,242],[306,390],[307,255],[306,303],[192,291]],
            [5,[256,245],[314,312],[389,190],[328,282],[161,265]],
            [7,[257,245],[309,306],[393,179],[330,274],[163,263]],
            [10,[218,261],[232,295],[287,167],[236,291],[170,288]],
            [11,[210,292],None,[139,338],[222,328],None],
            [13,[206,300],None,[119,399],[217,340],None],
            [18,[203,305],None,[122,431],[222,351],None],
            [23,[217,265],[308,352],[262,329],[271,333],None],
            [27,[244,246],[312,382],[301,255],[300,318],[190,287]],
            [31,[248,242],[306,390],[307,255],[306,303],[192,291]],
        ],
        'summon':[
            [0,[273,244],[329,385],[328,260],[328,303],[221,288]],
            [5,[282,249],[333,299],[407,171],[345,275],[192,260]],
            [8,[262,260],None,[419,237],None,[204,286]],
            [9,[237,258],[240,313],[381,308],None,None],
            [10,[220,271],None,None,None,None],
            [11,[245,251],None,[106,282],[168,282],None],
            [12,[280,255],None,[154,204],None,None],
            [13,[328,282],[354,310],None,None,None],
            [14,[328,308],[360,337],[434,236],None,None],
            [16,[298,289],[295,357],None,None,None],
            [18,[269,300],None,None,None,None],
            [21,[233,303],None,[145,383],[215,351],[304,249]],
            [25,[217,299],None,[69,341],None,None],
            [29,[206,303],None,[132,294],None,[284,246]],
            [33,[232,298],[262,364],[118,321],None,None],
            [37,[255,273],[319,377],None,None,[216,287]],
            [43,[273,244],[330,387],[330,258],[330,302],[220,289]],
            [50,[273,244],[329,385],[328,260],[328,303],[221,288]],
        ],
        'cast':[
            [0,[263,269],[346,485],[346,289],[345,356],[181,341]],
            [3,[266,264],[259,429],[179,328],[227,377],None],
            [6,[262,266],[230,395],[226,221],None,None],
            [10,[263,265],[225,403],[225,216],None,None],
            [15,[263,262],[223,408],[229,212],[229,320],None],
            [23,[263,266],[213,417],[231,220],[228,320],None],
            [30,[263,268],[207,421],[236,229],[224,337],None],
            [36,[263,270],[200,433],[233,226],[221,340],None],
            [45,[263,271],[190,444],[241,230],[219,342],None],
            [51,[263,271],[181,447],[240,257],[216,344],None],
            [57,[263,271],[180,444],[245,274],[218,343],None],
            [62,[263,269],[346,485],[346,289],[345,356],[181,341]],
        ],
    }
    # 仅保留已在原帧上确认是灰色手端的点；袖口/脚/遮挡推断全部撤销。
    hand_verified={'attack':{0,5,7,13,31},'summon':{0,5,11,50},'cast':{0,23,62}}
    right_verified={'attack':{0,5,7,31},'summon':{0,5,29,50},'cast':{0,62}}
    for clip,rows in raw.items():
        for row in rows:
            if row[0] not in hand_verified[clip]:row[4]=None
            if row[0] not in right_verified[clip]:row[5]=None
    auto=json.loads((OUT/'pixel_tracks_auto.json').read_text(encoding='utf-8'))
    output={}
    for clip,rows in raw.items():
        output[clip]=[]
        first_b=np.array(rows[0][2]);first_t=np.array(rows[0][3]);first_g=np.array(rows[0][4]);first_d=first_t-first_b
        base_grip=float((first_g-first_b)@first_d/(first_d@first_d))
        first_core=np.array(auto[clip][0]['staff_core_bright_center'])
        base_float=float((first_core-first_t)@first_d/(first_d@first_d)*17)
        for f,h,b,t,g,r in rows:
            a=auto[clip][f]
            item=dict(source_frame=f,source_time_seconds=round(f*.04,3),head_visible_box_center_proxy=h,
                      staff_rod_bottom=b,staff_tray_center=t,left_hand_grip=g,right_hand_endpoint=r,
                      staff_core_visible_pixel_centroid=a['staff_core_bright_center'],
                      staff_core_bbox=a['staff_core_bright_bbox'],manual_point_error_pixels=[3,5],
                      point_review='第二次原帧复核；关键f13/f11/f23以4倍网格裁片检查，未验证的手点一律null',
                      head_proxy_error_pixels=[4,7],
                      note='头点是可见灰盒轮廓中心代理，不是骨骼pivot；手点是可见握杆/末端，遮挡处null；不能仅由二维点唯一恢复深度')
            if b is not None and t is not None:
                bb=np.array(b);tt=np.array(t);dd=tt-bb;norm=float(dd@dd)
                item['staff_axis_pixel_vector']=(tt-bb).tolist()
                if g is not None:
                    grip=float((np.array(g)-bb)@dd/norm)
                    item['grip_fraction_bottom_to_tray']=round(grip,4)
                    item['suggested_staff_slide_y_from_ratio']=round((base_grip-grip)*17,3)
                core=np.array(item['staff_core_visible_pixel_centroid'])
                float_y=float((core-tt)@dd/norm*17)
                item['core_extra_lift_y_from_axis_projection']=round(float_y-base_float,3)
                item['core_lift_caveat']='以17单位杆和本clip首姿归零，沿可见杆轴投影估计；杆强烈缩短投影时误差放大，仍须三维并排核对'
            output[clip].append(item)
        for page in range((len(rows)+5)//6):
            subset=output[clip][page*6:(page+1)*6]
            sheet=Image.new('RGB',(1500,1060),(31,39,47));draw=ImageDraw.Draw(sheet)
            for j,item in enumerate(subset):
                f=item['source_frame'];x0=(j%3)*500;y0=(j//3)*530
                im=Image.open(FRAMES/clip/f'{f:04}.png').convert('RGBA');bg=Image.new('RGBA',im.size,(45,54,63,255));bg.alpha_composite(im);d=ImageDraw.Draw(bg)
                marks=[('H','head_visible_box_center_proxy','#eeeeee'),('B','staff_rod_bottom','#ffaa00'),('T','staff_tray_center','#ffdd00'),('L','left_hand_grip','#ff6688'),('R','right_hand_endpoint','#66ccff'),('C','staff_core_visible_pixel_centroid','#66ffcc')]
                for letter,key,col in marks:
                    val=item.get(key)
                    if val is None:continue
                    x,y=val;d.line((x-5,y,x+5,y),fill=col,width=2);d.line((x,y-5,x,y+5),fill=col,width=2)
                    d.text((x+6,y-15),f'{letter} {round(x)},{round(y)}',font=font(12),fill=col,stroke_width=1,stroke_fill='#17222b')
                if item['staff_rod_bottom'] is not None and item['staff_tray_center'] is not None:
                    d.line(tuple(item['staff_rod_bottom']+item['staff_tray_center']),fill='#ffdd00',width=1)
                sheet.paste(bg.convert('RGB'),(x0,y0+30));draw.text((x0+10,y0+5),f'{clip} f{f:03d} {f*.04:.2f}s | 原图观测点',font=font(18),fill='white')
            sheet.save(OUT/f'{clip}_landmarks_{page+1}.jpg',quality=95)
    write_json(OUT/'manual_landmarks.json',dict(revision=2,review_status='人工点复核完成；保持遮挡/null',
        model_anchors=dict(staff_rod_bottom=[-11,0,0],staff_tray_center=[-11,17.5,0],left_hand_grip=[-11,11,0],staff_core=[-11,22.2645298841,0]),
        coordinates='原始500×500画布左上原点，x右y下；没有裁剪缩放后坐标',clips=output))
    return output


def write_report(observations):
    lines=['# M3：attack / summon / cast 原帧与数值姿态研究','',
      '本目录是动作制作的输入与证据，不是最终动画事实来源。最终动画以 `../../pope.bbmodel` 为准；本脚本没有修改它，也没有操作 Blockbench。所有欧拉、深度与幅度都是由二维图像约束重建的起始解，必须经原生模型同帧并排校正，不能称为原游戏骨骼曲线。','',
      '## 坐标、骨架与相机','',
      '- Java +Y向上，正脸−Z；角色左侧−X，左手持杖。最终层级为 body→left_arm→left_hand→staff→staff_glow。','- right_arm rest Z=−48°，head rest Z=8°。`rotation`是增量，`world_rotation`是作者阶段的世界欧拉约束；运行时仍应解算为纯数字局部rotation/position。','- crown必须反向补偿head俯仰。attack f13头盒下俯而冠轴近竖直，不可锁定crown相对head不动。','- cape上端pivot为(0,12,2.2)，下摆向−Y。负X旋转使下摆甩向背后+Z；正X使它卷向身体前方。','- 三GIF均500×500，但人物缩放不同。相机拟合见camera_calibration.json。6个头角采用最终12×7×6头盒与rest Z=8°，测量误差与原作比例差异仍可能混入相机参数。','',
      '| clip | yaw | 俯视 | px/单位 | 6角RMSE |','|---|---:|---:|---:|---:|','| attack | 43.569° | 18.519° | 8.405906 | 1.706px |','| summon | 42.978° | 19.424° | 7.948490 | 1.179px |','| cast | 43.300° | 18.536° | 12.163688 | 1.979px |','',
      'walk f0有额外头动作且杖遮住两个前上角，未套用静息6角假设。camera_calibration.json中的walk值仅为试拍建议，无伪造拟合RMSE。','',
      '## 时长与出手候选','',
      '| clip | 原GIF编码时长 | 末姿时间 | 建议clip时长 | 建议出手 | 证据 |','|---|---:|---:|---:|---:|---|','| attack | 1.28s | 1.24s / f31 | 1.25s | 0.50s | 有动图；出手事件为推断 |','| summon | 2.04s | 2.00s / f50 | 2.00s | 0.65s | 有动图；出手事件为推断 |','| cast | 2.52s | 2.48s / f62 | 2.50s | 0.90s | 有动图；出手事件为推断 |','',
      'attack/cast以末姿时间线性映射建议长度，summon保持源时间。JSON逐帧同时保存source_time_seconds和建议time；它们不能混称原作时刻。clip出手0.50/0.65/0.90s分别是前压到位、环扫到正面、高悬方块到稳定段的玩法同步候选。GIF无弹体发射、召唤实体或事件轨道，未证明这些是原作事件时间。','',
      '## 关键观察','',
      '### attack：一次前压，前10→11帧变化极快','',
      '- f0→f7（0–0.28s）：左手举杖向后上，右臂横伸，角色右腿向前踢。','- f10→f11（0.40–0.44s）：杆轴从近竖直迅速变为向前横压。不能用全段平滑缓入抹掉这40ms的突变；20TPS无法逐帧等时复现，必须在0.40/0.45s附近保留姿态。','- f13–18（0.52–0.72s）：躯干强烈前压，杖端向前下，冠轴仍近竖直。f23起收回，f31回首姿。','- 原图只有一遍准备→伸杖→回收，不能做三次挥杖来假装三连弹。','',
      '握点变化有明确像素证据：f0杆底(306,390)、托盘(307,255)、握点(306,303)，握点位于杆底→托盘约64.4%；f7为(309,306)→(393,179)，握点(330,274)，约25.1%。同一17单位杆对应向上窜约6.7单位。允许staff局部Y约+7，表示手仍贴杆但换握，而不是把手与杆拆开。','',
      '### summon：负向完整旋转及过冲','',
      '| 帧/源时间 | 观察 | 建议累计Java yaw |','|---|---|---:|','| f8 / 0.32 | 正脸3/4，开始横扫 | 0° |','| f9 / 0.36 | 正脸明显变窄 | −25° |','| f10 / 0.40 | 侧面 | −80° |','| f11 / 0.44 | 背部出现 | −130° |','| f12 / 0.48 | 背面3/4 | −185° |','| f13 / 0.52 | 另一侧 | −235° |','| f14 / 0.56 | 正脸重新出现 | −275° |','| f16 / 0.64 | 近正面 | −315° |','| f21 / 0.84 | 接近最初3/4方向 | −360° |','| f29 / 1.16 | 同方向过冲，正脸再次变窄 | −415° |','| f50 / 2.00 | 回到起始朝向 | −360° |','',
      '方向证据来自前脸眉眼/冠宝石与后脑灰点/蓝后布的连续顺序；角度值是重建建议，非原骨骼读数。不要把−360端点替换为0并做最短角插值，否则完整旋转会变成反向摆动。杆端贯穿整个圆扫，躯干同时前压，不可只抬双臂。','',
      '### cast：方块离开托盘升高，整杖没有同幅度上升','',
      '- f0→f6（0–0.24s）：把杆从身侧带到脸前；杆托盘停在前额/头顶下缘附近。','- f6→f23（0.24–0.92s）：发光立方单独浮起，身体小幅后仰，头冠向画面右倾，后布抬向背后。','- f23–45（0.92–1.80s）：方块在皇冠上方悬停，杆仍在脸前；f51→57方块下降，f62归位。','- f23放大证据见cast23_enlarged.png：灰托盘约(231,220)，方块亮像素质心约(241,88)，其间确有透明空隙。静息托盘约(346,289)，方块质心约(344,250)。轴向估算比首姿额外浮起约8单位。因此staff_glow独立position Y约+8，不能将整根杆上移8单位代替。','',
      '## 文件与误差','',
      '- action_poses_candidates.json：40个可执行姿态起始解，所有骨骼都有明确数值。body position当前为零；侧向/纵向根位移尚未由二维点解深度，需要根制作者统一IK后调整。','- manual_landmarks.json：人工原像素点、遮挡null、杆轴/换握/悬浮量估计；点误差约3–5px，头盒中心代理误差约4–7px。头中心不是骨骼pivot。','- pixel_tracks_auto.json：146帧颜色区域质心/杆红带PCA；普通红带选择可能误选冠宝石（summon f37就是已知例子），不能把未人工检查的所有自动点直接作为IK约束。','- *_landmarks_*.jpg：原画布测量联系表。H=灰头可见轮廓中心代理、B=杆底、T=托盘、L/R=左握点/右手端、C=亮立方像素质心。没有旋转源图或用渲染图替代原图。','- *_grid_*.jpg：25px网格原帧联系表；*_landmarks_*优先于自动颜色圈。','',
      '尚未做：未原生渲染这份起始解、未在真实游戏内看过、未证明最终视觉还原度、未烘焙/集成玩法或音效。root接手原生并排后应以数值像素误差和视觉朝向共同判定，不能因JSON合法就声称动作完成。','']
    (OUT/'MOTION_ATTACK_CAST.md').write_text('\n'.join(lines),encoding='utf-8')


def audit_crops():
    cases=[
        ('attack',13,(90,300,260,430),4,'attack_critical_detail.png'),
        ('summon',11,(70,240,235,325),4,'summon_critical_detail.png'),
        ('cast',23,(190,190,260,430),4,'cast_critical_detail.png'),
        ('cast',6,(195,210,260,450),3,'cast6_point_audit.png'),
        ('cast',10,(195,210,260,450),3,'cast10_point_audit.png'),
        ('summon',13,(320,220,380,370),3,'summon13_point_audit.png'),
        ('summon',14,(340,220,460,380),3,'summon14_point_audit.png'),
    ]
    for clip,f,box,mult,name in cases:
        im=Image.open(FRAMES/clip/f'{f:04}.png').convert('RGBA')
        bg=Image.new('RGBA',im.size,(45,54,63,255));bg.alpha_composite(im)
        tile=bg.crop(box).resize(((box[2]-box[0])*mult,(box[3]-box[1])*mult))
        d=ImageDraw.Draw(tile)
        for x in range(box[0],box[2],10):
            xx=(x-box[0])*mult;d.line((xx,0,xx,tile.height),fill='#465464');d.text((xx+1,1),str(x),font=font(13),fill='white')
        for y in range(box[1],box[3],10):
            yy=(y-box[1])*mult;d.line((0,yy,tile.width,yy),fill='#465464');d.text((1,yy+1),str(y),font=font(13),fill='white')
        tile.save(OUT/name)
    im=Image.open(FRAMES/'cast'/'0023.png').convert('RGBA')
    bg=Image.new('RGBA',im.size,(42,53,63,255));bg.alpha_composite(im)
    bg.crop((160,0,370,430)).resize((420,860)).save(OUT/'cast23_enlarged.png')


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    candidate_poses()
    calibrate_cameras()
    study_sheets()
    write_report(manual_constraints())
    audit_crops()
