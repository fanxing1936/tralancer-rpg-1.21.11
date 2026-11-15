"""M2 静态模型的可重复制作入口（不被 build.sh 自动调用）。

几何测量 + 明确来源图集 -> Blockbench MCP -> .bbmodel。
最终 .bbmodel 是后续动画和资源构建的事实来源；重新执行本脚本会重建静态稿，
因此已有动作或手改时必须显式另存，不能在运行时构建中调用本脚本。
"""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import math
import uuid
from pathlib import Path

from PIL import Image
from heart_of_ender_blockbench import BlockbenchMCP, REF

FACES = ("north", "east", "south", "west", "up", "down")
SPACE = uuid.UUID("2935075e-0b02-4f4e-a859-50109e67c061")


def uid(name):
    return str(uuid.uuid5(SPACE, name))


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def verify_export(expected, actual):
    """确保导出没有悄悄改坐标、UV、骨旋转或层级。"""
    checks=[]
    numeric_errors=[]
    def same(name,a,b):
        if a != b:
            if isinstance(a,list) and isinstance(b,list) and len(a)==len(b) and all(isinstance(x,(int,float)) for x in a+b):
                error=max(abs(x-y) for x,y in zip(a,b))
                if error>0.00000501: raise RuntimeError(f"Blockbench 导出改变了 {name}: {a!r} != {b!r}")
                numeric_errors.append(error)
            else: raise RuntimeError(f"Blockbench 导出改变了 {name}: {a!r} != {b!r}")
        checks.append(name)
    for field, keys in [("elements",("name","from","to")), ("groups",("name","origin","rotation"))]:
        before={x["uuid"]:x for x in expected[field]}
        after={x["uuid"]:x for x in actual[field]}
        same(field+" UUID",set(before),set(after))
        for key,a in before.items():
            b=after[key]
            for prop in keys: same(a["name"]+"/"+prop,a[prop],b[prop])
            if field=="elements":
                for face in FACES:
                    same(a["name"]+"/"+face+"/UV",a["faces"][face]["uv"],b["faces"][face]["uv"])
                    same(a["name"]+"/"+face+"/enabled",a["faces"][face]["texture"] is not None,b["faces"][face]["texture"] is not None)
    def hierarchy(outliner):
        parents={}
        def walk(nodes,parent):
            for node in nodes:
                if isinstance(node,str): parents[node]=parent
                else:
                    parents[node["uuid"]]=parent
                    walk(node.get("children",[]),node["uuid"])
        walk(outliner,None)
        return parents
    same("outliner parent membership",hierarchy(expected["outliner"]),hierarchy(actual["outliner"]))
    same("resolution",expected["resolution"],actual["resolution"])
    return {"passed":True,"checked_fields":len(checks),"method":"by UUID; exact nonnumeric equality, numeric tolerance for Blockbench 5-decimal export",
            "numeric_tolerance":0.00000501,"max_numeric_difference":max(numeric_errors,default=0)}


def write_sockets(target):
    """只记录未来特效锚点候选；不生成实体或特效。"""
    from types import SimpleNamespace
    import display_mob
    bones,_,_=display_mob.load_bbmodel(SimpleNamespace(bbmodel=target))
    document=read(target)
    torso=next(c for c in document["elements"] if c["name"]=="inner_torso")
    lo,hi=torso["from"],torso["to"]
    middle=[(a+b)/2 for a,b in zip(lo,hi)]
    points=[("mouth_center","shell_head",[0,26,-10.808],"闭嘴缝中心候选；未制作特效"),
            ("cross_beam_center","inner_body",middle,"小人躯干中心候选；准确发射姿态与帧待M3")]
    for name,axis,sign in [("cross_north",2,-1),("cross_east",0,1),("cross_south",2,1),("cross_west",0,-1)]:
        point=middle.copy();point[axis]=lo[axis] if sign<0 else hi[axis]
        points.append((name,"inner_body",point,"躯干表面接口候选；不是原作骨骼数据"))
    report={"bbmodel_sha256":hashlib.sha256(target.read_bytes()).hexdigest(),
            "coordinate_system":"+y up, facing -z; unscaled model units, not blocks", "model_scale":None,"seat":None,"sockets":[]}
    for name,bone,point,note in points:
        matrix=display_mob.bone_matrix(bones,bone)
        world=[sum(matrix[i][j]*point[j] for j in range(3))+matrix[i][3] for i in range(3)]
        report["sockets"].append({"name":name,"bone":bone,"bbmodel_unrotated_point":point,
                                  "offset_from_bone_pivot":[round(point[i]-bones[bone]["pivot"][i],6) for i in range(3)],
                                  "rest_model_point":[round(v,6) for v in world],"status":note})
    write(REF/"m2_sockets.json",report)


def subdivide(cube,density):
    """只分割长方体，不改变外轮廓；每面均落在128源像素星窗内。"""
    sizes = [b-a for a, b in zip(cube["from"], cube["to"])]
    axis = max(range(3), key=sizes.__getitem__)
    count = max(1, math.ceil(sizes[axis] / (128/density)))
    if count == 1:
        return [cube]
    result = []
    for i in range(count):
        part = copy.deepcopy(cube)
        part["name"] += f"_uvsegment_{i+1}"
        part["from"][axis] = cube["from"][axis] + sizes[axis]*i/count
        part["to"][axis] = cube["from"][axis] + sizes[axis]*(i+1)/count
        result.append(part)
    return result


def generate():
    spec = read(REF / "m2_geometry/geometry_spec.json")
    atlas_doc = read(REF / "m2_atlas/atlas_regions.json")
    arch_doc = read(REF / "m2_atlas/arch_uv_regions.json")
    regions = {r["name"]: r for r in atlas_doc["regions"]}
    atlas_path = REF / atlas_doc["atlas_file"]
    atlas = Image.open(atlas_path).convert("RGBA")
    elements, groups, parent_of, children = [], [], {}, {}
    mappings = []
    for bone in spec["bones"]:
        name = bone["name"]
        groups.append({"name": name, "uuid": uid("bone/"+name), "origin": bone["pivot"],
                       "rotation": bone["rest_rotation"], "children": [], "export": True,
                       "visibility": True, "shade": True, "reset": False,
                       "mirror_uv": False, "autouv": 0, "color": 0})
        parent_of[name] = bone["parent"]
        children[name] = []

    def cube_element(cube, uv_faces, region_names):
        element = {"name": cube["name"], "uuid": uid("cube/"+cube["name"]), "type": "cube",
                   "from": cube["from"], "to": cube["to"], "origin": [0,0,0],
                   "box_uv": False, "autouv": 0, "export": True,
                   "faces": {f: {"uv": uv_faces.get(f,[0,0,0,0]), "texture": 0 if f in uv_faces else None} for f in FACES}}
        elements.append(element)
        children[cube["bone"]].append(element["uuid"])
        for face, uv in uv_faces.items():
            region = regions[region_names[face]]
            entry = {"element": cube["name"], "bone": cube["bone"], "face": face,
                     "atlas_uv": uv, "region": region["name"], "source_file": region["source_file"]}
            if region["kind"] == "source_copy":
                ax,ay,_,_ = region["atlas_rect"]
                sx,sy,_,_ = region["source_rect"]
                entry["source_uv"] = [round(uv[0]-ax+sx,6),round(uv[1]-ay+sy,6),round(uv[2]-ax+sx,6),round(uv[3]-ay+sy,6)]
            else:
                entry["source_sampling"] = "见 atlas_regions.json 中该区单应矩阵与逐像素源坐标"
            mappings.append(entry)

    arch_map = arch_doc.get("face_mappings", arch_doc)
    def arch_semantic(name):
        if "upper_strip" in name: return "crown"
        if "nose" in name: return "nose"
        if "head" in name: return "head"
        if "torso" in name: return "torso"
        if "arm" in name: return "arm"
        if "foot" in name: return "foot"
        return "leg"

    for original in spec["cubes"]:
        if original["bone"].startswith("inner_"):
            mapping = arch_map[arch_semantic(original["name"])]
            faces = mapping["faces"] if "faces" in mapping else mapping
            uv = {f:[v[0]+432,v[1]+8,v[2]+432,v[3]+8] for f,v in faces.items() if v is not None}
            cube_element(original, uv, {f:"arch_undressed" for f in uv})
            continue
        density=4.5 if original["bone"] in ("shell_head","shell_jaw") else 13
        for cube in subdivide(original,density):
            size = [b-a for a,b in zip(cube["from"],cube["to"])]
            face_size = {"north":(size[0],size[1]), "south":(size[0],size[1]),
                         "east":(size[2],size[1]), "west":(size[2],size[1]),
                         "up":(size[0],size[2]), "down":(size[0],size[2])}
            uv, names = {}, {}
            for f in FACES:
                seed = int(hashlib.sha256((cube["name"]+"/"+f).encode()).hexdigest()[:8],16)
                name = "stars_"+"ABCDEF"[seed%6]
                ax,ay,_,_ = regions[name]["atlas_rect"]
                w,h = [round(v*density,6) for v in face_size[f]]
                if max(w,h)>128.00001: raise ValueError((cube["name"],f,w,h))
                dx,dy = (seed//6)%max(1,int(128-w)+1), (seed//997)%max(1,int(128-h)+1)
                uv[f] = [ax+dx,ay+dy,round(ax+dx+w,6),round(ay+dy+h,6)]
                names[f] = name
            cube_element(cube,uv,names)

    # 单独发光骨：从整面提取图裁取非透明包围盒；不补画、不改变像素。
    fit = spec["head_fit"]
    skull = next(c for c in spec["cubes"] if c["name"] == "shell_skull")
    x0,x1 = skull["from"][0],skull["to"][0]
    top = skull["to"][1]
    front,back = skull["from"][2],skull["to"][2]
    for name,bone,face in [("front_eyes","shell_eyes_glow","north"),
                           ("front_teeth","shell_teeth_front_glow","north"),
                           ("side_teeth","shell_teeth_side_glow","west")]:
        region=regions[name]; ax,ay,bx,by=region["atlas_rect"]
        crop=atlas.crop((ax,ay,bx,by)); box=crop.getchannel("A").getbbox()
        l,t,r,b=box; w,h=crop.size
        yy0=top-fit["total_closed_height"]*b/h
        yy1=top-fit["total_closed_height"]*t/h
        if face=="north":
            # 面向 -Z 时 north 面的 UV 左端位于 +X；不是世界坐标的 x 最小端。
            lo=[x1-(x1-x0)*r/w,yy0,front-0.008]
            hi=[x1-(x1-x0)*l/w,yy1,front-0.008]
        else:
            lo=[x0-0.008,yy0,front+(back-front)*l/w]
            hi=[x0-0.008,yy1,front+(back-front)*r/w]
        cube_element({"name":name+"_surface","bone":bone,"from":lo,"to":hi},
                     {face:[ax+l,ay+t,ax+r,ay+b]},{face:name})

    def branch(name):
        return {"uuid":uid("bone/"+name), "isOpen":False,
                "children":children[name]+[branch(n) for n,p in parent_of.items() if p==name]}
    document={"meta":{"format_version":"5.0","model_format":"bedrock","box_uv":False},
              "name":"heart_of_ender", "model_identifier":"geometry.heart_of_ender",
              "visible_box":[8,8,3], "resolution":{"width":512,"height":512},
              "unhandled_root_fields":{"heart_of_ender_stage":"M2 static only", "glow_mask":{
                  "source":"MCD_Heart_of_Ender_(glow_effect_texture).png", "atlas_rect":regions["glow_mask_raw"]["atlas_rect"],
                  "rgba":"unchanged", "binding":"preserved material source; runtime mask compositing not implemented"}},
              "elements":elements,"groups":groups,"outliner":[branch(n) for n,p in parent_of.items() if p is None],
              "textures":[{"name":"heart_of_ender_atlas.png", "id":"0", "uuid":uid("atlas"),
                           "width":512,"height":512,"uv_width":512,"uv_height":512,"internal":True,
                           "render_mode":"default","render_sides":"auto","pbr_channel":"color",
                           "source":"data:image/png;base64,"+base64.b64encode(atlas_path.read_bytes()).decode()}],
              "animations":[]}
    write(REF/"m2_face_uv.json", {"source":"heart_of_ender_geo.py", "pixels_per_model_unit_stars":{"head_and_jaw":4.5,"body_and_limbs":13},
                                "game_model_scale":"not decided", "faces":mappings})
    return document


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port",type=int,default=52907)
    parser.add_argument("--replace-static",action="store_true",help="明确允许重建本任务的无动画M2稿")
    args=parser.parse_args()
    target=REF/"heart_of_ender.bbmodel"
    if target.exists():
        if read(target).get("animations"):
            raise RuntimeError("已有动画；拒绝用M2脚本覆盖事实来源")
        if not args.replace_static:
            raise RuntimeError("已有静态稿；核对无手改后使用 --replace-static")
    document=generate()
    client=BlockbenchMCP(args.port)
    client.tool("create_project",{"name":"heart_of_ender","format":"bedrock"})
    # 插件的简单注释检查也会匹配base64里的连续斜线；合法JSON Unicode转义保留同一字节内容。
    serialized=json.dumps(document).replace("/",r"\u002f")
    result=client.evaluate("(function(){Codecs.project.parse("+serialized+");return {elements:Cube.all.length,groups:Group.all.length,textures:Texture.all.length};})()")
    print(result)
    exported=client.tool("export_model",{"codec_id":"project","options":{"raw":False},"max_content_length":2000000})
    payload=json.loads(next(b["text"] for b in exported["content"] if b["type"]=="text"))
    if payload["truncated"]: raise RuntimeError("Blockbench 导出被截断，拒绝保存")
    content=payload["content"]
    parsed=json.loads(content)
    if parsed.get("animations"): raise RuntimeError("M2不应生成动作")
    audit=verify_export(document,parsed)
    target.write_text(content,encoding="utf-8")
    digest=hashlib.sha256(target.read_bytes()).hexdigest()
    audit["bbmodel_sha256"]=digest
    write(REF/"m2_authoring_audit.json",audit)
    mapping=read(REF/"m2_face_uv.json")
    actual_elements={e["name"]:e for e in parsed["elements"]}
    atlas_regions={r["name"]:r for r in read(REF/"m2_atlas/atlas_regions.json")["regions"]}
    for face in mapping["faces"]:
        uv=actual_elements[face["element"]]["faces"][face["face"]]["uv"]
        face["atlas_uv"]=uv
        region=atlas_regions[face["region"]]
        if region["kind"]=="source_copy":
            ax,ay,_,_=region["atlas_rect"];sx,sy,_,_=region["source_rect"]
            face["source_uv"]=[round(uv[0]-ax+sx,6),round(uv[1]-ay+sy,6),round(uv[2]-ax+sx,6),round(uv[3]-ay+sy,6)]
    mapping["bbmodel_sha256"]=digest
    mapping["verified_against_blockbench_export"]=True
    write(REF/"m2_face_uv.json",mapping)
    write_sockets(target)
    client.evaluate("(function(){Project.save_path="+json.dumps(str(target))+";Project.saved=true;return {saved:Project.saved};})()")
    print(f"已由Blockbench导出 {target} ({target.stat().st_size} bytes)")


if __name__=="__main__":
    main()
