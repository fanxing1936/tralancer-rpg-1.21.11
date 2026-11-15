#!/usr/bin/env python3
"""M1 source-image measurements only; does not create a model or animation.

Coordinates are original-image pixels (origin at upper left). Overlay lines
are manual observations, not recovered 3D joints. No source pixels are
repainted: only alpha compositing onto gray, nearest-neighbour crops, labels,
and measurement guides are used. Run from any working directory.
"""
from pathlib import Path
import json
import math
from PIL import Image, ImageDraw, ImageFont

REF = Path(__file__).resolve().parent / "heart_of_ender_ref"
OUT = REF / "analysis_structure"
BG = (55, 60, 70)
COLORS = [(255, 201, 77), (89, 221, 230), (142, 239, 154),
          (255, 140, 197), (178, 166, 255), (255, 151, 105)]


def font(size=20):
    for path in ("C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/arial.ttf"):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def flatten(im):
    im = im.convert("RGBA")
    base = Image.new("RGBA", im.size, BG + (255,))
    base.alpha_composite(im)
    return base.convert("RGB")


def load(name, frame=None):
    im = Image.open(REF / name)
    if frame is not None:
        im.seek(frame)
    return flatten(im)


def label(draw, xy, text, fill, size=20):
    f = font(size)
    box = draw.textbbox(xy, text, font=f)
    draw.rectangle((box[0]-3, box[1]-2, box[2]+3, box[3]+2), fill=(15,20,28))
    draw.text(xy, text, font=f, fill=fill)


def point(draw, xy, name, fill, offset=(10, -25), radius=5, size=20):
    x, y = xy
    draw.ellipse((x-radius,y-radius,x+radius,y+radius), outline=fill, width=2)
    label(draw, (x+offset[0], y+offset[1]), name, fill, size)


def dashed(draw, start, end, fill, width=2):
    length = math.dist(start, end)
    if not length:
        return
    for s in range(0, int(length), 14):
        a, b = s/length, min(s+7, length)/length
        draw.line(tuple(start[k]+(end[k]-start[k])*t for t in (a,b) for k in (0,1)), fill=fill, width=width)


MEASUREMENTS = {
    "coordinate_system": "Original image pixels: x right, y down. NOT Java model coordinates.",
    "date": "2026-11-04",
    "limb_ids": "A-F name the visible terminal positions in Idle frame 0; no anatomical left/right mapping is asserted.",
    "render": {
        "file": "MCD_Heart_of_Ender.png", "size": [1000, 840],
        "head_bbox": [218, 103, 565, 422], "head_bbox_uncertainty_px": 8,
        "visible_trunk_bbox": [357, 396, 640, 690], "trunk_boundary_uncertainty_px": 25,
        "model_outline_bbox": [26, 20, 979, 802], "outline_uncertainty_px": 6,
        "inner_illager_glowing_silhouette_bbox": [487, 555, 575, 731],
        "mouth_emission_bbox": [276, 351, 441, 417],
        "terminal_centers": {"A":[86,54], "B":[49,452], "C":[47,674], "D":[966,487], "E":[626,778], "F":[668,627]},
    },
    "idle_frame_0": {
        "file":"MCD_Heart_of_Ender_Idle.gif", "frame":0, "time_s":0,
        "head_bbox":[108,109,282,269], "head_bbox_uncertainty_px":4,
        "visible_trunk_bbox":[174,254,318,376], "trunk_boundary_uncertainty_px":12,
        "model_outline_bbox":[14,65,490,457],
        "terminal_centers":{"A":[50,80],"B":[26,282],"C":[30,390],"D":[481,300],"E":[317,446],"F":[334,371]},
    },
    "raised_front_three_quarter": {
        "file":"Heart_of_Ender_prepare_to_shoot_beams.png", "size":[1622,817],
        "upper_skull_bbox":[998,63,1205,230], "head_and_open_jaw_bbox":[998,63,1205,294],
        "visible_trunk_bbox":[1039,290,1190,538],
        "terminal_centers":{"P1":[804,55],"P2":[782,278],"P3":[779,365],"P4":[1391,98],"P5":[1399,222],"P6":[1452,376]},
        "root_proxy_pairs":[[[1040,335],[1161,337]],[[1045,427],[1175,422]],[[1046,508],[1160,513]]],
        "root_proxy_uncertainty_px":25,
        "note":"P1-P6 are local screenshot IDs; pair centers are silhouette attachment zones, not recovered skeleton pivots; brightness/overlap hides boundaries.",
    },
    "d_limb_bend": {
        "file":"MCD_Heart_of_Ender_Idle.gif", "frame":62, "time_s":2.48,
        "proximal_visible_center":[300,332],"bend_center":[363,366],"terminal_center":[450,356],
        "uncertainty_px":6,
        "note":"Two straight directions are directly visible in D. Does not prove identical joint structure for all six limbs.",
    },
}


def count_diagram():
    a = load("MCD_Heart_of_Ender.png")
    b = a.copy(); d=ImageDraw.Draw(b)
    for i, (name, xy) in enumerate(MEASUREMENTS["render"]["terminal_centers"].items()):
        off = (-55,-35) if name=="D" else (12,-25)
        point(d, xy, name, COLORS[i], off, radius=8, size=30)
    for key, color in (("head_bbox",(230,230,230)),("visible_trunk_bbox",(120,200,255))):
        d.rectangle(MEASUREMENTS["render"][key],outline=color,width=2)
    d.line((225,434,551,434),fill=(230,230,230),width=2)
    label(d,(270,435),"H = 347 px（投影包围宽）",(230,230,230),17)
    panel=Image.new("RGB",(2000,910),BG);panel.paste(a,(0,70));panel.paste(b,(1000,70))
    dd=ImageDraw.Draw(panel)
    label(dd,(20,12),"原始渲染图（仅合成灰底）",(255,255,255),26)
    label(dd,(1020,12),"6 个末端编号；白框=头；蓝框=可见躯干范围",(255,255,255),24)
    panel.save(OUT/"01_render_count_measurements.png")


def raised_diagram():
    a=load("Heart_of_Ender_prepare_to_shoot_beams.png");b=a.copy();d=ImageDraw.Draw(b)
    m=MEASUREMENTS["raised_front_three_quarter"]
    for i,(name,xy) in enumerate(m["terminal_centers"].items()):
        point(d,xy,name,COLORS[i],offset=(-32,15),radius=9,size=28)
    for i,pair in enumerate(m["root_proxy_pairs"]):
        for xy in pair:
            x,y=xy;d.rectangle((x-25,y-25,x+25,y+25),outline=COLORS[i],width=2)
        dashed(d,pair[0],pair[1],COLORS[i])
        label(d,(1210,pair[1][1]-14),f"连接带 {i+1}（约 ±25px）",COLORS[i],20)
    d.rectangle(m["head_and_open_jaw_bbox"],outline=(240,240,240),width=3)
    d.rectangle(m["visible_trunk_bbox"],outline=(120,200,255),width=3)
    b.save(OUT/"02_raised_six_ends_and_root_zones.png")
    # Comparison retains aspect ratios, uses only nearest neighbour scaling.
    p=Image.new("RGB",(1622,880),BG);d=ImageDraw.Draw(p)
    for n,img in enumerate([a,b]):
        img=img.crop((730,10,1500,590))
        p.paste(img,(n*811+15,65))
    label(d,(20,10),"原图局部",(255,255,255),25)
    label(d,(831,10),"原图局部 + 量测；框不是已知骨架关节",(255,255,255),23)
    label(d,(25,675),"这是不同观察角度的独立编号 P1–P6；不把它强配为 A–F 的解剖左右。",(255,255,255),24)
    label(d,(25,725),"六末端可直接数出；连接带被半透明材质、交叠和高光遮挡，坐标只给范围。",(255,255,255),23)
    p.save(OUT/"02b_raised_comparison.png")


def bend_diagram():
    panel=Image.new("RGB",(1500,780),BG);d=ImageDraw.Draw(panel)
    for n,f in enumerate([0,62,75]):
        im=load("MCD_Heart_of_Ender_Idle.gif",f)
        if f==62:
            dd=ImageDraw.Draw(im);m=MEASUREMENTS["d_limb_bend"]
            pts=[m["proximal_visible_center"],m["bend_center"],m["terminal_center"]]
            dd.line(pts,fill=COLORS[3],width=2)
            for j,xy in enumerate(pts):point(dd,xy,["近端可见段","折点","末端 D"][j],COLORS[3],offset=(-45,12),size=13)
        panel.paste(im,(n*500,40))
        crop=load("MCD_Heart_of_Ender_Idle.gif",f).crop((280,310,490,450)).resize((420,280),Image.Resampling.NEAREST)
        panel.paste(crop,(n*500+40,500))
        label(d,(n*500+12,7),f"Idle f{f:04d} / {f/25:.2f} s",(255,255,255),20)
    panel.save(OUT/"03_d_limb_two_direction_evidence.png")


def video_crops():
    panel=Image.new("RGB",(1600,1300),BG);d=ImageDraw.Draw(panel)
    for i,f in enumerate([0,4,8,12]):
        p=REF/"frames/Heart_of_Ender_idle_video"/f"frame_{f:04d}.png"
        if not p.exists():
            continue
        im=flatten(Image.open(p)).crop((480,200,1400,850))
        im.thumbnail((780,590),Image.Resampling.NEAREST)
        panel.paste(im,(i%2*800+10,i//2*650+45))
        label(d,(i%2*800+10,i//2*650+10),f"游戏视频样本 {f}（实际 pts 见 frames.csv）",(255,255,255),20)
    panel.save(OUT/"04_video_bends_front_view_only.png")


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"measurements.json").write_text(json.dumps(MEASUREMENTS,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    count_diagram();raised_diagram();bend_diagram();video_crops()
    print("M1 structure diagrams and measurements written to",OUT)


if __name__=="__main__":
    main()
