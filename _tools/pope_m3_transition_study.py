"""M3 过渡动作原帧量测；不生成/修改模型。Python + Pillow + NumPy + SciPy。"""
from pathlib import Path
import csv
import json
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

ROOT = Path(__file__).resolve().parent
REF = ROOT / "pope_ref"
FRAMES = REF / "m1/motion/frames"
OUT = REF / "m3/motion_transition"
OUT.mkdir(parents=True, exist_ok=True)
TIMING = json.loads((REF / "m1/motion/gif_timing.json").read_text(encoding="utf-8"))

def font(size=18):
    return ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", size)

def component(mask):
    lab, n = ndimage.label(mask)
    if not n:
        return None
    counts = np.bincount(lab.ravel()); counts[0] = 0
    k = int(counts.argmax())
    yy, xx = np.where(lab == k)
    if len(xx) < 3:
        return None
    return {
        "pixel_count": len(xx),
        "bbox": [int(xx.min()), int(yy.min()), int(xx.max()+1), int(yy.max()+1)],
        "centroid": [round(float(xx.mean()), 2), round(float(yy.mean()), 2)],
        "bbox_center": [round(float((xx.min()+xx.max())/2), 2), round(float((yy.min()+yy.max())/2), 2)],
    }

def measure(clip, f):
    a = np.array(Image.open(FRAMES / clip / f"{f:04d}.png").convert("RGBA"))
    r,g,b = a[:,:,:3].astype(float).transpose(2,0,1)
    v = a[:,:,3] > 0
    crown = component(v & (r>125) & (g>80) & (b<150) & (r>b*1.18) & (g>b*1.1))
    head = component(v & (r>50) & (r<210) & (abs(r-g)<12) & (abs(g-b)<12))
    body = component(v & (b>120) & (r<70) & (g<140) & (b>g*1.3))
    by,bx=np.where(v & (b>120) & (r<70) & (g<140) & (b>g*1.3))
    body_union = {"bbox":[int(bx.min()),int(by.min()),int(bx.max()+1),int(by.max()+1)],
                  "bbox_center":[round(float((bx.min()+bx.max())/2),2),round(float((by.min()+by.max())/2),2)],
                  "notes_zh":"全部袍蓝+双袖的联合包围盒中心；躯干目标的辅助代理，仍受手臂姿态影响。"} if len(bx) else None
    row = {"source_clip":clip, "frame":f, "source_seconds":round(f*.04,2),
           "head_gray":head, "crown_gold":crown, "body_blue":body,"body_blue_union":body_union,
           "alpha_bbox":list(Image.fromarray(a).getbbox()) if v.any() else None}
    if head and body:
        h = np.array(head["centroid"]); q = np.array(body["centroid"]); d = h-q
        row["screen_body_axis_degrees"] = round(math.degrees(math.atan2(d[0],-d[1])),2)
    if head and crown:
        d = np.array(crown["centroid"])-head["centroid"]
        row["crown_minus_head_px"] = np.round(d,2).tolist()
    if clip == "whirlwind_game":
        yy,xx = np.indices(v.shape)
        lo,hi = (430,445) if f == 0 else (385,416)
        rod = component(v & (r>70) & (r>g*1.4) & (r>b*1.4) & (xx>lo) & (xx<hi))
        row["staff_red_band"] = rod
        if rod and f not in [0,3]:
            cx = int(round(rod["centroid"][0])); top=rod["bbox"][1]; bot=rod["bbox"][3]-1
            column = v[:,cx-1:cx+2].any(axis=1)
            while top>0 and column[top-1]: top-=1
            while bot+1<len(column) and column[bot+1]: bot+=1
            row["staff_tray_px"] = [cx,rod["bbox"][1]-28]
            row["staff_bottom_px"] = [cx,bot]
            row["staff_measurement"] = "红杆最大连通块定位中心列，杖底沿不透明列向下扫描；托盘取红段首行-28px（按可见托盘/杆结构拟合，约4px误差）。不沿不透明列向上找托盘，以免杖顶方块投影连接造成误判。"
        elif f == 0:
            row.update(staff_tray_px=None,staff_bottom_px=[438,735],staff_measurement="杖底手工读原像素约3px误差；初帧托盘被方块遮住，留空。")
        elif f == 3:
            row.update(staff_tray_px=[396,636],staff_bottom_px=[414,700],staff_measurement="手工读原像素，误差约3px；此时杖斜，中心列法不适用。")
    return row

KEYS = {
 "appear":[0,3,6,9,12,18,27,39,45],
 "teleport_in":[0,3,6,9,15,24,30],
 "teleport_out":[30,33,36,39,42,45,48,51,53],
 "whirlwind":[0,3,8,16,25,34,42,51,59,67,68,71,76,84,93,98,101,109,118,126,135,143,152,160],
}
OBS = {
 "appear":{
  0:"全透明；无法量测。",3:"很小的侧背形体；姿态尚不可精确读。",6:"清楚露背，杖在画面左；冠随头倾。",9:"已正面朝镜头，左臂外举直杖，双腿悬空。",12:"面朝前，头/冠向画面右倾，杖在额前，腿分开。",18:"开始下降，头/冠回近竖直，杖仍高于头侧。",27:"低位，杖头移至躯干侧下方，肩肘回收。",39:"身体抬回站立高度，杖回侧边。",45:"可衔接站立；身形尚有细小变化。"},
 "teleport_in":{
  0:"全透明。",3:"微小侧背形体。",6:"清楚露背，杖在画面左。",9:"正面举杖高点。",15:"悬空下降，腿仍分开，杖在脸前。",24:"到低位，杖头降到胸侧。",30:"低位正面姿态；下一段开始前。"},
 "teleport_out":{
  30:"正面，杖头在画面右下。",33:"仍正面，左手将杖伸向画面右上；开始转身。",36:"清楚露背，杖转到画面左；后袍白边可见。",39:"仍背面但换成另一侧，杖近竖直，双脚内收。",42:"再次正面；视觉体积已减小。",45:"再次背面，杖在画面左；继续旋转。",48:"再次正面，杖在画面右；形体很小。",51:"仅少量像素，不可靠读姿态。",53:"全透明。"},
 "whirlwind":{
  0:"起点已经前倾；冠斜向画面左，杖仍贴近身体。",3:"杖与人物已清楚分离；人飞向右上，身体接近直立。",8:"人物倒置，头在蓝袍下方。",16:"人物再次接近直立，飞到高位右侧。",25:"最右侧大幅远离杖，冠向画面右，人物近横置。",34:"向杖回转，头/冠在躯干左方。",42:"经过杖左侧，人物斜横置；冠向左。",51:"飞到左侧，人物倒置。",59:"向左上抬升，冠朝左上。",67:"在杖左上，头在身体上方，冠明显向右漂偏。",76:"飞到右上，人物横置。",84:"背部朝镜头，皇冠与头之间有可见空隙，冠在头左上。",93:"人物转到杖左下，冠在右侧。",101:"贴近杖左下，双腿在上方。",109:"到杖右下，接近倒置；袍蓝区受遮挡，蓝质心轴不可靠。",118:"绕到杖左侧中高位，冠向左上。",126:"到杖下方，头朝下侧。",135:"杖右下，蓝袍在头左上；头冠投影再靠近。",143:"杖下，人物横置，冠朝右。",152:"杖左下，人物斜横置，冠朝左。",160:"位于杖底下方，身体仍完整；冠与头投影重叠，不是已吸尽。"}
}
OBS["whirlwind"].update({68:"皇冠与头右侧清楚分离；连续帧68–72均有可见空隙，早于M1抽帧84。",71:"皇冠继续在头右侧独立漂浮，长轴转到近横向。",98:"人物倒置，皇冠在头右下，与头有空隙。"})
MANUAL_STAFF = {
 "appear":{3:([247,359],[250,374]),6:([233,205],[221,259]),9:([313,135],[319,225]),12:([271,126],[299,230]),18:([280,214],[306,320]),27:(None,[281,420]),39:([288,352],[281,411]),45:([287,359],[282,419])},
 "teleport":{3:([247,359],[250,374]),6:([233,205],[221,259]),9:([313,135],[319,225]),15:([274,156],[299,263]),24:(None,[293,438]),30:(None,[280,426]),33:([385,300],[283,385]),36:([173,279],[221,382]),39:([229,252],[220,344]),42:([314,292],[281,326]),45:([212,280],[238,313]),48:([269,269],[259,280])}
}

def quantize(x):
    return round(math.floor(x*20+.5)/20,2)

def clip_time(clip,f):
    if clip == "teleport_in": return quantize(f*.04*.75)
    if clip == "teleport_out": return quantize((f*.04-1.2)*.9/.92)
    return quantize(f*.04)

COLORS = {"head_gray":(50,235,235),"crown_gold":(255,202,25),"body_blue":(255,100,220)}
LABELS = {"head_gray":"H", "crown_gold":"C", "body_blue":"B"}

def overlay(row,size=400):
    clip,f=row["source_clip"],row["frame"]
    im=Image.open(FRAMES/clip/f"{f:04d}.png").convert("RGBA")
    bg=Image.new("RGBA",im.size,(48,55,65,255));bg.alpha_composite(im);bg=bg.convert("RGB")
    d=ImageDraw.Draw(bg)
    for key,color in COLORS.items():
        ob=row.get(key)
        if ob:
            x,y=ob["centroid"]
            d.ellipse((x-4,y-4,x+4,y+4),outline=color,width=2)
            d.text((x+5,y-15),LABELS[key],font=font(16),fill=color)
    for key,label in [("staff_tray_px","T"),("staff_bottom_px","S")]:
        if row.get(key):
            x,y=row[key];d.line((x-5,y,x+5,y),fill=(120,255,120),width=2);d.line((x,y-5,x,y+5),fill=(120,255,120),width=2)
            d.text((x+5,y-12),label,font=font(16),fill=(120,255,120))
    return bg.resize((size,size),Image.Resampling.NEAREST)

def contacts(clip,rows):
    w=400; n=4;h=452
    im=Image.new("RGB",(n*w,math.ceil(len(rows)/n)*h+75),(238,236,224));d=ImageDraw.Draw(im)
    d.text((12,9),f"{clip} 原作标点（H头灰 / C皇冠金 / B袍蓝 / T托盘 / S杖底）",font=font(23),fill=(25,30,35))
    d.text((12,40),"保留整张画布、同一比例。点是可见颜色质心或手工观测，不是官方骨骼枢轴。",font=font(19),fill=(50,50,50))
    for i,row in enumerate(rows):
        x=i%n*w;y=i//n*h+75;im.paste(overlay(row,w),(x,y))
        d.text((x+8,y+w+5),f"帧{row['frame']:03d} 源{row['source_seconds']:.2f}s → clip {row['clip_seconds']:.2f}s",font=font(18),fill=(25,30,35))
    im.save(OUT/f"{clip}_landmarks.jpg",quality=94)

def trajectory(rows):
    im=Image.new("RGB",(1100,1060),(238,236,224));d=ImageDraw.Draw(im)
    d.text((25,12),"whirlwind 屏幕轨迹：原800×800坐标，同一画布",font=font(25),fill=(20,25,30))
    ox,oy=90,105
    for q in range(0,801,100):
        d.line((ox+q,oy,ox+q,oy+800),fill=(205,205,195));d.line((ox,oy+q,ox+800,oy+q),fill=(205,205,195))
        d.text((ox+q-13,oy-27),str(q),font=font(15),fill=(30,30,30));d.text((ox-43,oy+q-8),str(q),font=font(15),fill=(30,30,30))
    for key,col in COLORS.items():
        pts=[(ox+r[key]["centroid"][0],oy+r[key]["centroid"][1]) for r in rows if r.get(key)]
        d.line(pts,fill=col,width=3)
        for r in rows:
            if r.get(key):
                x,y=r[key]["centroid"];x+=ox;y+=oy;d.ellipse((x-3,y-3,x+3,y+3),fill=col)
                if key=="head_gray":d.text((x+4,y+3),str(r["frame"]),font=font(14),fill=(20,30,30))
    for key in ["staff_tray_px","staff_bottom_px"]:
        pts=[(ox+r[key][0],oy+r[key][1]) for r in rows if r.get(key)]
        d.line(pts,fill=(50,140,50),width=3)
    d.text((25,940),"青：头灰质心；金：冠金质心；粉：袍蓝质心；绿：托盘/杖底。数字是帧号。",font=font(20),fill=(20,30,30))
    d.text((25,975),"不能直接当作世界XY轨迹：镜头俯视/偏航及Z深度不确定；须由最终模型对照校准。",font=font(19),fill=(20,30,30))
    im.save(OUT/"whirlwind_screen_trajectory.png")

def crown_gap_contacts(all_rows):
    chosen=[68,69,70,71,83,84,85,98,99,100,101,160]
    im=Image.new("RGB",(1800,630),(238,236,224));d=ImageDraw.Draw(im)
    for i,f in enumerate(chosen):
        row=all_rows["whirlwind_game"][f]
        boxes=[row[k]["bbox"] for k in COLORS if row.get(k)]
        box=[min(b[0] for b in boxes)-12,min(b[1] for b in boxes)-12,max(b[2] for b in boxes)+12,max(b[3] for b in boxes)+12]
        raw=Image.open(FRAMES/"whirlwind_game"/f"{f:04d}.png").convert("RGBA").crop(box)
        bg=Image.new("RGBA",raw.size,(48,55,65,255));bg.alpha_composite(raw);bg=bg.convert("RGB")
        scale=min(290/bg.width,260/bg.height);bg=bg.resize((round(bg.width*scale),round(bg.height*scale)),Image.Resampling.NEAREST)
        x=i%6*300;y=i//6*315;im.paste(bg,(x,y+35));d.text((x+5,y+2),f"帧{f} / {f*.04:.2f}s",font=font(21),fill=(20,20,20))
    im.save(OUT/"crown_gap_candidates.jpg",quality=96)

def main():
    all_rows={}
    for clip,end in [("appear",45),("teleport",53),("whirlwind_game",160)]:
        all_rows[clip]=[measure(clip,f) for f in range(end+1)]
    clips={}
    for clip,frames in KEYS.items():
        src="teleport" if clip.startswith("teleport") else ("whirlwind_game" if clip=="whirlwind" else clip)
        rows=[]
        for f in frames:
            row=dict(all_rows[src][f]);row["clip_seconds"]=clip_time(clip,f);row["observation_zh"]=OBS[clip][f]
            if src in MANUAL_STAFF and f in MANUAL_STAFF[src]:
                row["staff_tray_px"],row["staff_bottom_px"]=MANUAL_STAFF[src][f]
                row["staff_measurement"]="人工读取可见像素中心，估计误差4–6px；null表示托盘被杖顶/身体遮挡，未凭空补坐标。"
            if f in (0,3,51,53) and src!="whirlwind_game":
                row["confidence_zh"]="透明/微小阶段，颜色质心可能是错误部位，只支持整体可见性与粗轨迹。"
            elif src=="whirlwind_game" and f in (25,109):
                row["confidence_zh"]="头灰分裂或袍蓝遮挡明显，颜色质心偏离真实骨骼中心；须看原图。"
            else:row["confidence_zh"]="颜色分区及视觉识别；中心是可见表面代理，非三维枢轴。"
            rows.append(row)
        clips[clip]={"duration_seconds":{"appear":1.8,"teleport_in":.9,"teleport_out":.9,"whirlwind":7}[clip],"keyframes":rows}
        contacts(clip,rows)
    trajectory(clips["whirlwind"]["keyframes"])
    crown_gap_contacts(all_rows)
    result={
      "stage":"M3_source_motion_study_only",
      "coordinate_system":"PNG像素：原画布左上(0,0)，x向右，y向下；不是Java模型XYZ",
      "method":"同帧最大连通色块质心；灰=头、金=冠、蓝=袍的可见表面代理。保留bbox/像素数便于审核。mask阈值在脚本。",
      "raw_measurement_caution":"all_frame_measurements是自动分割原数据，未逐帧人工确认：冠被遮住时金色可能误抓腿（如whirlwind44/45），蓝色可能偏向单袖，勿直接当骨骼轨迹。选中的关键帧已配原图供人工审核。",
      "screen_angle":"头灰质心减袍蓝质心的向量相对屏幕向上角度，顺时针正。遮挡/姿态可使该代理偏移；不是Java欧拉。",
      "source_timing":"所有本组源GIF均40ms一帧；clip量化至0.05s。",
      "no_scale":"仅rotation/position。源大小变化/透明阶段不能原样重现。",
      "camera_candidate_not_official":{
        "yaw_degrees":45,"elevation_degrees":30,
        "appear_teleport":{"canvas":[500,500],"pixels_per_model_unit_full_size_range":[7.0,7.5],"ground_anchor_px_candidate":[250,425],"ground_anchor_tolerance_px":10,"notes":"由头前面/侧面约2:1可见宽度、顶边斜率以及最终身高粗估；早期/离场体积变化不应用固定scale解释为已证实镜头缩放。"},
        "whirlwind":{"canvas":[800,800],"pixels_per_model_unit_candidate":5.67,"evidence":"源竖直自由杖托盘到杖底约86px；当前静态模型对应17.5单位，取仰角30度得86/(17.5*cos30)=5.67。依赖当前重建杆长，非官方相机参数。","screen_reference_px":[401,613],"reference_frame":25,"notes":"以上只是固定屏幕基准，不称世界地面。真实世界原点不可从透明单视角唯一确定。"}},
      "orientation_candidates_not_official":{
        "teleport_out":{"clip_seconds":[0,.1,.25,.35,.45,.6,.7,.9],"relative_yaw_magnitude_deg":[0,10,150,240,360,540,720,900],"notes":"正背次序约束的试摆值，不是测得官方欧拉；旋转符号必须由当前模型摄影方向与持杖手轨迹验证。0.7以后太小不能确证最后900度，仅为保持转向的推断；可不再新增一圈。"},
        "appear_teleport_in":{"source_frame":[3,6,9,12,18,27,45],"relative_yaw_magnitude_deg":[90,180,360,360,360,360,360],"notes":"0.24秒露背、0.36秒正面支持前段转身，不能唯一证明恰好整圈。之后主要升降、举杖和回收。"},
        "whirlwind_first_turn":{"source_frame":[0,3,8,16],"screen_body_axis_unwrapped_degrees":[-18.89,22.99,181.85,336.16],"notes":"头灰→袍蓝轴首0.64秒支持近整圈顺时针屏幕翻滚；仅可作相机平面roll目标，不能直接当Java Z动画角。后段投影有反向，需复合yaw/pitch，按原帧目标点解算。"}},
      "whirlwind_final_inference":{"start_seconds":6.4,"end_seconds":7.0,"instruction":"由所有部件现有世界中心，插值至同一交接中心；同时逐渐整理各自姿态。属于项目推断，不是源GIF结局。不能称为体积消失。"},
      "clips":clips}
    (OUT/"transition_keyframes.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (OUT/"all_frame_measurements.json").write_text(json.dumps(all_rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with (OUT/"keyframe_landmarks.csv").open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.writer(f);w.writerow(["clip","frame","source_s","clip_s","head_x","head_y","crown_x","crown_y","body_x","body_y","tray_x","tray_y","staff_bottom_x","staff_bottom_y","axis_cw_deg","observation"])
        for clip,data in clips.items():
            for row in data["keyframes"]:
                nums=[]
                for key in ["head_gray","crown_gold","body_blue"]:nums+=row[key]["centroid"] if row.get(key) else [None,None]
                nums+=row.get("staff_tray_px") or [None,None];nums+=row.get("staff_bottom_px") or [None,None]
                w.writerow([clip,row["frame"],row["source_seconds"],row["clip_seconds"],*nums,row.get("screen_body_axis_degrees"),row["observation_zh"]])
    print(f"已输出 {OUT}")

if __name__ == "__main__":main()
