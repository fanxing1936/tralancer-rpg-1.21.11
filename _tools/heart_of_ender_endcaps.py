"""渲染三个静态端盖方案供用户选择；不会替换主 .bbmodel。"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from heart_of_ender_blockbench import BlockbenchMCP, REF
from heart_of_ender_geo import verify_export


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port",type=int,default=52907)
    args=parser.parse_args()
    out=REF/"m2_endcaps"
    out.mkdir(exist_ok=True)
    source=REF/"heart_of_ender.bbmodel"
    source_bytes=source.read_bytes()
    model=json.loads(source_bytes)
    options=json.loads((REF/"m2_geometry/endcap_options.json").read_text(encoding="utf-8"))["options"]
    client=BlockbenchMCP(args.port)
    evidence={"source_bbmodel_sha256":hashlib.sha256(source_bytes).hexdigest(),"options":[]}
    for option in options:
        ident=option["id"]
        if ident=="R0":
            evidence["options"].append({"id":ident,"model":"../heart_of_ender.bbmodel","render":"../m2_preview/reference_three_quarter.png"})
            continue
        doc=copy.deepcopy(model)
        doc["name"]="heart_of_ender_"+ident
        for group in doc["groups"]:
            if group["name"] in option["bone_rest_replacements"]:
                group["rotation"]=option["bone_rest_replacements"][group["name"]]
        doc.setdefault("unhandled_root_fields",{})["endcap_candidate"]=ident
        client.tool("create_project",{"name":doc["name"],"format":"bedrock"})
        encoded=json.dumps(doc).replace("/",r"\u002f")
        client.evaluate("(function(){Codecs.project.parse("+encoded+");return true;})()")
        result=client.tool("export_model",{"codec_id":"project","max_content_length":2000000})
        data=json.loads(next(b["text"] for b in result["content"] if b["type"]=="text"))
        if data["truncated"]:raise RuntimeError("导出被截断")
        actual=json.loads(data["content"])
        audit=verify_export(doc,actual)
        target=out/(ident+".bbmodel")
        target.write_text(data["content"],encoding="utf-8")
        subprocess.run([sys.executable,str(Path(__file__).with_name("heart_of_ender_preview.py")),"--port",str(args.port),"--model",str(target),"--output",str(out/ident)],check=True)
        evidence["options"].append({"id":ident,"model":target.name,"model_sha256":hashlib.sha256(target.read_bytes()).hexdigest(),"export_audit":audit,"render":ident+"/reference_three_quarter.png"})
    if source.read_bytes()!=source_bytes:raise RuntimeError("主模型被改变")
    evidence["main_model_unchanged"]=True
    (out/"evidence.json").write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    images=[Image.open(REF/"MCD_Heart_of_Ender.png"),Image.open(REF/"m2_preview/reference_three_quarter.png"),Image.open(out/"R1/reference_three_quarter.png"),Image.open(out/"R2/reference_three_quarter.png")]
    font=ImageFont.truetype("C:/Windows/Fonts/msyh.ttc",22)
    small=ImageFont.truetype("C:/Windows/Fonts/msyh.ttc",18)
    board=Image.new("RGBA",(1440,1220),(55,60,70,255))
    draw=ImageDraw.Draw(board)
    headers=["原始渲染（Mojang）","R0：当前主模型","R1：较小角度调整","R2：按可见边线拟合"]
    for col,label in enumerate(headers): draw.text((col*360+12,18),label,font=font,fill="white")
    crops=[("A：画面左上端",(20,0,200,180)),("B：画面左中端",(0,350,180,530)),("E：画面右前下端",(545,660,725,840))]
    for row,(label,box) in enumerate(crops):
        y=64+row*370
        for col,im in enumerate(images):
            panel=Image.new("RGBA",(360,360),(55,60,70,255))
            panel.alpha_composite(im.convert("RGBA").crop(box).resize((360,360),Image.Resampling.NEAREST))
            board.alpha_composite(panel,(col*360,y))
        draw.text((10,y+5),label,font=small,fill=(255,221,117))
    draw.text((12,1180),"只调整远段绕轴滚转，中心线不变。R2 的 E 斜率更近，但底沿仍偏低约 10 像素；不是精确原骨架。",font=small,fill="white")
    board.convert("RGB").save(out/"endcap_comparison.png")
    print(out/"endcap_comparison.png")


if __name__=="__main__":main()
