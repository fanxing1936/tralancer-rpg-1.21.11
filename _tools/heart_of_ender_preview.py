"""从已保存 .bbmodel 经 Blockbench 原生 WebGL 渲染 M2 静态对照。

不生成/修改贴图，不加辉光，不调整曝光；Pillow 只负责把真实渲染和原参考并排。
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from heart_of_ender_blockbench import BlockbenchMCP, REF

OUT=REF/"m2_preview"
BG=(55,60,70,255)


def value(result):
    return json.loads(next(b["text"] for b in result["content"] if b["type"]=="text"))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port",type=int,default=52907)
    parser.add_argument("--model",type=Path,default=REF/"heart_of_ender.bbmodel")
    parser.add_argument("--output",type=Path,default=OUT)
    parser.add_argument("--fullbright-all",action="store_true",help="M3紫色材质审阅：全模型自发光；不加bloom")
    args=parser.parse_args()
    global_output=args.output.resolve()
    if not global_output.is_relative_to(REF.resolve()) or not args.model.resolve().is_relative_to(REF.resolve()):
        raise ValueError("输入/输出必须在 heart_of_ender_ref 内")
    output=global_output
    output.mkdir(parents=True,exist_ok=True)
    path=args.model
    document=json.loads(path.read_text(encoding="utf-8"))
    spec=json.loads((REF/"m2_geometry/geometry_spec.json").read_text(encoding="utf-8"))
    client=BlockbenchMCP(args.port)
    client.tool("create_project",{"name":"heart_of_ender","format":"bedrock"})
    serialized=json.dumps(document).replace("/",r"\u002f")
    info=value(client.evaluate("(function(){Codecs.project.parse("+serialized+");return {name:Project.name,uuid:Project.uuid,format:Format.id,elements:Cube.all.length,groups:Group.all.length,textures:Texture.all.length,animations:Animation.all.length};})()"))
    client.evaluate("(function(){Project.save_path="+json.dumps(str(path))+";Project.saved=true;return true;})()")
    camera=spec["camera"]
    # 等待纹理解码完成由后续RPC边界和Blockbench返回决定，不以任意固定sleep猜时序。
    state=value(client.evaluate("({loaded:Texture.all.every(t=>t.img.complete && t.img.naturalWidth>0),sizes:Texture.all.map(t=>[t.img.naturalWidth,t.img.naturalHeight])})"))
    if not state["loaded"]: raise RuntimeError("Blockbench贴图尚未完成加载；保留工程后重跑preview")
    views=[{"name":"reference_three_quarter","position":camera["position_at_distance_80"],"target":camera["target"],"height":camera["orthographic_height"]},
           {"name":"front","direction":[0,0,-1]}, {"name":"right_side","direction":[1,0,0]},
           {"name":"back","direction":[0,0,1]}]
    glow_bones=[g["name"] for g in document["groups"]] if args.fullbright_all else spec["glow_bones"]
    code="""(function(){
      const definitions=DEFINITIONS;
      const glowBones=GLOWBONES;
      const originals=[];
      for(const cube of Cube.all){
        if(glowBones.includes(cube.parent.name)){
          const original=cube.mesh.material;
          const fullbright=original.clone();
          fullbright.uniforms.map.value=original.uniforms.map.value;
          fullbright.map=original.map;
          fullbright.uniforms.SHADE.value=false;
          cube.mesh.material=fullbright;
          originals.push([cube,original,fullbright]);
        }
      }
      const p=new Preview({id:'heart_of_ender_m2_offscreen',offscreen:true,antialias:false});
      p.setProjectionMode(true);p.resize(1000,840);p.renderer.setPixelRatio(1);
      const result={};
      const bounds=new THREE.Box3();Cube.all.forEach(c=>bounds.expandByObject(c.mesh));
      const center=bounds.getCenter(new THREE.Vector3());
      const dimensions=bounds.getSize(new THREE.Vector3());
      for(const v of definitions){
        let target=v.target ? new THREE.Vector3(...v.target) : center.clone();
        let position=v.position ? new THREE.Vector3(...v.position) : target.clone().addScaledVector(new THREE.Vector3(...v.direction),100);
        let height=v.height || Math.max(dimensions.y+6,((v.name==='right_side'?dimensions.z:dimensions.x)+6)*840/1000);
        p.camOrtho.position.copy(position);p.controls.target.copy(target);p.camOrtho.up.set(0,1,0);
        p.camOrtho.lookAt(target);p.camOrtho.zoom=(840/40)/height;p.camOrtho.updateProjectionMatrix();
        p.controls.update();
        let data;Canvas.withoutGizmos(()=>{p.render();data=p.canvas.toDataURL('image/png');});
        result[v.name]={data,position:position.toArray(),target:target.toArray(),height};
      }
      for(const [cube,original,fullbright] of originals){cube.mesh.material=original;fullbright.dispose();}
      p.renderer.dispose();return result;
    })()""".replace("DEFINITIONS",json.dumps(views)).replace("GLOWBONES",json.dumps(glow_bones))
    rendered=value(client.evaluate(code))
    evidence={"engine":"Blockbench native WebGL, offscreen Preview", "source_bbmodel_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
              "opened_project":info,"texture_loaded":state,"alpha_note":"Blockbench preview only, not Minecraft alpha sorting evidence",
              "full_bright_preview_from_glow_bones":glow_bones,"full_bright_method":"clone native material and set SHADE=false only on these surfaces; no bloom, recoloring or alpha edit", "views":{}}
    for name,data in rendered.items():
        raw=base64.b64decode(data.pop("data").split(",",1)[1])
        (output/(name+".png")).write_bytes(raw)
        evidence["views"][name]=data
    (output/"render_evidence.json").write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    try: font=ImageFont.truetype("C:/Windows/Fonts/msyh.ttc",26)
    except OSError: font=ImageFont.load_default()
    def panel(image,label):
        result=Image.new("RGBA",(1000,900),BG)
        result.alpha_composite(image.convert("RGBA"),(0,60))
        ImageDraw.Draw(result).text((18,14),label,font=font,fill="white")
        return result
    original=Image.open(REF/"MCD_Heart_of_Ender.png").convert("RGBA")
    native=Image.open(output/"reference_three_quarter.png").convert("RGBA")
    pair=Image.new("RGBA",(2000,900),BG)
    pair.alpha_composite(panel(original,"原始渲染 / Mojang（仅合成灰底）"),(0,0))
    label="Blockbench / 来源紫色图集 / 全模型自发光 / 无辉光" if args.fullbright_all else "Blockbench 静态模型 / 原图集 / 未加辉光"
    pair.alpha_composite(panel(native,label),(1000,0))
    pair.convert("RGB").save(output/"reference_comparison.png")
    board=Image.new("RGBA",(2000,1800),BG)
    labels={"front":"正面：检查六肢、头身与小人", "right_side":"右侧：检查连接与前后方向（隐藏深度推断）",
            "reference_three_quarter":"四分之三：与原图相同相机拟合", "back":"背面：隐藏连接结构推断"}
    for (name,label),(x,y) in zip(labels.items(),[(0,0),(1000,0),(0,900),(1000,900)]):
        board.alpha_composite(panel(Image.open(output/(name+".png")),label),(x,y))
    board.convert("RGB").save(output/"four_views.png")
    print(json.dumps({"project":info,"images":len(rendered),"directory":str(output)},ensure_ascii=False))


if __name__=="__main__":main()
