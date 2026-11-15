"""Checkpoint A: deterministic textured, orthographic software preview.

Reads the authoritative bbmodel/config, and the existing spear asset with the
third-person transform recorded by validate_static.py. No animation is sampled,
and no weapon model or runtime function is created. Alpha is cut out at 128.

python _tools/lucifer_ref/render_static.py
python _tools/lucifer_ref/render_static.py --model ../sunken_skeleton_ref/sunken_skeleton.bbmodel --out previews/sunken_test
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
from pathlib import Path
import sys
from types import SimpleNamespace

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import display_mob as dm

NORMALS = {"north": [0, 0, -1], "south": [0, 0, 1],
           "east": [1, 0, 0], "west": [-1, 0, 0],
           "up": [0, 1, 0], "down": [0, -1, 0]}
VIEWS = {
    "front": ([0, 0, -1], "正面 · 朝 -Z"),
    "right_side": ([1, 0, 0], "右侧面 · 持矛侧"),
    "back": ([0, 0, 1], "背面 · 朝 +Z"),
    "three_quarter": ([1.1, 0.65, -2], "四分之三 · 持矛侧"),
}


def font(size):
    path = Path(r"C:\Windows\Fonts\msyh.ttc")
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default()


def point_transform(matrix, points):
    array = np.asarray(points, dtype=float)
    return (np.c_[array, np.ones(len(array))] @ np.asarray(matrix).T)[:, :3]


def cube_face_vertices(lo, hi):
    x0, y0, z0 = lo
    x1, y1, z1 = hi
    # TL, TR, BR, BL when seen from outside; UV reversals remain in face data.
    return {
        "north": [[x1,y1,z0],[x0,y1,z0],[x0,y0,z0],[x1,y0,z0]],
        "south": [[x0,y1,z1],[x1,y1,z1],[x1,y0,z1],[x0,y0,z1]],
        "east": [[x1,y1,z1],[x1,y1,z0],[x1,y0,z0],[x1,y0,z1]],
        "west": [[x0,y1,z0],[x0,y1,z1],[x0,y0,z1],[x0,y0,z0]],
        "up": [[x0,y1,z0],[x1,y1,z0],[x1,y1,z1],[x0,y1,z1]],
        "down": [[x0,y0,z1],[x1,y0,z1],[x1,y0,z0],[x0,y0,z0]],
    }


def append_box(output, lo, hi, faces, matrix, texture, glow=False, source="body"):
    vertices = cube_face_vertices(lo, hi)
    for face, spec in faces.items():
        if spec.get("texture") is None:
            continue
        u0, v0, u1, v1 = spec["uv"]
        uv = np.array([[u0,v0],[u1,v0],[u1,v1],[u0,v1]], dtype=float)
        normal = np.asarray(matrix)[:3,:3] @ np.asarray(NORMALS[face], dtype=float)
        normal /= np.linalg.norm(normal)
        output.append({"vertices": point_transform(matrix, vertices[face]),
                       "uv": uv, "texture": texture, "normal": normal,
                       "glow": glow, "source": source})


def build_scene(model_path, config, weapon_path, rest_override=None):
    doc = json.loads(model_path.read_text(encoding="utf-8"))
    bones, png, resolution = dm.load_bbmodel(SimpleNamespace(bbmodel=str(model_path)))
    if rest_override is not None:
        bones["right_arm"]["rotation"] = [float(rest_override), 0, 0]
    texture = np.array(Image.open(io.BytesIO(png)).convert("RGBA"))
    assert texture.shape[1] == resolution["width"] and texture.shape[0] == resolution["height"]
    scaling = float(config.get("model_scale", 1))
    glow = set(config.get("glow", []))
    scene = []
    included = set()
    parts = config.get("parts")
    if parts:
        for name, members in (parts.items() if isinstance(parts, dict) else parts):
            if name != config.get("held", "weapon"):
                included.update(members)
    else:
        included.update(bones)
    for name in bones:
        if name not in included:
            continue
        matrix = np.asarray(dm.scale(scaling)) @ np.asarray(dm.bone_matrix(bones, name))
        for cube in bones[name]["cubes"]:
            if any(cube.get("rotation", [0, 0, 0])):
                raise ValueError("Element rotation is not exported by display_mob: " + cube["name"])
            inflate = cube.get("inflate", 0)
            append_box(scene, np.array(cube["from"]) - inflate,
                       np.array(cube["to"]) + inflate, cube["faces"],
                       matrix, texture, name in glow, name)
    reference = json.loads(weapon_path.read_text(encoding="utf-8"))
    spear_path = Path(reference["texture_path"])
    spear = np.array(Image.open(spear_path).convert("RGBA"))
    assert hashlib.sha256(spear_path.read_bytes()).hexdigest() == reference["texture_sha256"], "Spear changed since reference capture"
    matrix = np.asarray(dm.scale(scaling)) @ np.asarray(dm.bone_matrix(bones, "right_arm"))
    matrix = matrix @ np.asarray(dm.translate(*bones["right_arm"]["pivot"]))
    for key in ("vanilla_axis_matrix", "hold_matrix", "thirdperson_matrix", "generated_model_center_matrix"):
        matrix = matrix @ np.asarray(reference[key])
    height, width = spear.shape[:2]
    # Standard item/generated: the PNG is read unchanged. Opposite-facing north
    # has the vanilla reversed UV; this is not an additional image mirroring.
    append_box(scene, [0,0,7.5], [16,16,8.5], {
        "north": {"texture": 0, "uv": [width,0,0,height]},
        "south": {"texture": 0, "uv": [0,0,width,height]},
    }, matrix, spear, False, "existing_spear_generated")
    opaque = spear[:,:,3] >= 128
    # In-memory alpha boundary extrusion matching generated item thickness.
    # No replacement weapon geometry is serialized to the resource pack.
    for y, x in zip(*np.nonzero(opaque)):
        edge_faces = {}
        for name, dx, dy in (("east",1,0),("west",-1,0),("up",0,-1),("down",0,1)):
            xx, yy = x+dx, y+dy
            if xx < 0 or xx >= width or yy < 0 or yy >= height or not opaque[yy,xx]:
                edge_faces[name] = {"texture": 0, "uv": [x+.1,y+.1,x+.9,y+.9]}
        if edge_faces:
            append_box(scene, [x*16/width,16-(y+1)*16/height,7.5],
                       [(x+1)*16/width,16-y*16/height,8.5],edge_faces,matrix,spear,
                       False,"existing_spear_generated_edge")
    metadata = {
        "model_sha256": hashlib.sha256(model_path.read_bytes()).hexdigest(),
        "atlas_sha256": hashlib.sha256(png).hexdigest(),
        "model_scale": scaling, "quads": len(scene),
        "held_java_rig_matrix": matrix.tolist(),
        "weapon_texture_sha256": reference["texture_sha256"],
        "weapon_preview": "Existing PNG unchanged; in-memory vanilla generated slab, existing thirdperson_righthand matrix.",
        "animation_count": len(doc.get("animations", [])),
        "right_arm_rest_override_for_preview_only": rest_override,
    }
    return scene, metadata


def camera_basis(direction):
    toward = np.array(direction, dtype=float)
    toward /= np.linalg.norm(toward)
    right = np.cross([0,1,0], toward)
    right /= np.linalg.norm(right)
    up = np.cross(toward, right)
    return np.array([right, up, toward])


def triangle(rgb, zbuffer, screen, uv, texture, shade):
    height, width = zbuffer.shape
    x0 = max(0, int(math.floor(screen[:,0].min())))
    x1 = min(width-1, int(math.ceil(screen[:,0].max())))
    y0 = max(0, int(math.floor(screen[:,1].min())))
    y1 = min(height-1, int(math.ceil(screen[:,1].max())))
    if x0>x1 or y0>y1:
        return
    x, y = np.meshgrid(np.arange(x0,x1+1)+.5, np.arange(y0,y1+1)+.5)
    a,b,c = screen
    den = (b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
    if abs(den)<1e-9:
        return
    p = ((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(y-c[1]))/den
    q = ((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(y-c[1]))/den
    r = 1-p-q
    depth = p*a[2]+q*b[2]+r*c[2]
    target = zbuffer[y0:y1+1,x0:x1+1]
    mask = (p>=-1e-8)&(q>=-1e-8)&(r>=-1e-8)&(depth>target)
    if not mask.any():
        return
    u = p*uv[0,0]+q*uv[1,0]+r*uv[2,0]
    v = p*uv[0,1]+q*uv[1,1]+r*uv[2,1]
    sampled = texture[np.clip(np.floor(v).astype(int),0,texture.shape[0]-1),
                      np.clip(np.floor(u).astype(int),0,texture.shape[1]-1)]
    mask &= sampled[:,:,3]>=128
    target[mask] = depth[mask]
    color = np.clip(sampled[:,:,:3].astype(float)*shade,0,255).astype(np.uint8)
    rgb[y0:y1+1,x0:x1+1][mask] = color[mask]


def render(scene, direction, title, scale, center, size):
    width,height=size
    rgb=np.zeros((height,width,3),dtype=np.uint8)
    rgb[:]=[28,34,32]
    zbuffer=np.full((height,width),-np.inf,dtype=float)
    basis=camera_basis(direction)
    light=np.array([-0.45,0.8,-0.55]);light/=np.linalg.norm(light)
    for face in scene:
        if np.dot(face["normal"],basis[2]) < 1e-8:
            continue
        projected=(face["vertices"]-center) @ basis.T
        projected[:,0]=width/2+projected[:,0]*scale
        projected[:,1]=height/2-projected[:,1]*scale
        shade=1.0 if face["glow"] else .68+.32*max(0,float(np.dot(face["normal"],light)))
        for indices in ((0,1,2),(0,2,3)):
            ids=list(indices)
            triangle(rgb,zbuffer,projected[ids],face["uv"][ids],face["texture"],shade)
    image=Image.fromarray(rgb)
    draw=ImageDraw.Draw(image)
    draw.text((28,22),title,fill=(225,232,218),font=font(30))
    draw.text((28,height-49),"静态软件预览 · 非游戏截图",fill=(165,181,166),font=font(20))
    return image


def place_reference(board, path, box):
    image=Image.open(path).convert("RGBA")
    alpha=image.getchannel("A")
    bbox=alpha.getbbox()
    if bbox:
        image=image.crop(bbox)
    x,y,w,h=box
    ratio=min(w/image.width,h/image.height)
    image=image.resize((max(1,round(image.width*ratio)),max(1,round(image.height*ratio))),Image.Resampling.NEAREST)
    board.alpha_composite(image,(x+(w-image.width)//2,y+(h-image.height)//2))


def comparison(rendered, label, out_path):
    board=Image.new("RGBA",(1800,1200),(235,237,226,255))
    draw=ImageDraw.Draw(board)
    draw.text((36,24),"路西法第一阶段 · "+label,fill=(33,44,35),font=font(35))
    preview=rendered.copy();preview.thumbnail((900,1010),Image.Resampling.LANCZOS)
    board.alpha_composite(preview.convert("RGBA"),(25,95))
    draw.text((975,95),"原作盔甲 · 固定四分之三视图",fill=(33,44,35),font=font(23))
    place_reference(board,HERE/"MCD_Root_Rot_Armor.png",(960,140,405,870))
    draw.text((1390,95),"原作身体 · 固定四分之三视图",fill=(33,44,35),font=font(20))
    place_reference(board,HERE/"MCD_Mossy_Skeleton.png",(1380,140,380,870))
    draw.text((36,1130),"原作未提供同角度正/侧/背视图；右侧固定参考仅用于辨认轮廓、材质和特征，不能作为原作背面证据。",fill=(71,83,66),font=font(21))
    board.convert("RGB").save(out_path)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--model",type=Path,default=HERE/"lucifer.bbmodel")
    parser.add_argument("--config",type=Path,default=HERE/"static_config.json")
    parser.add_argument("--weapon",type=Path,default=HERE/"validation/weapon_reference.json")
    parser.add_argument("--out",type=Path,default=HERE/"previews")
    parser.add_argument("--test-sunken",action="store_true")
    parser.add_argument("--right-arm-rest",type=float,default=None)
    args=parser.parse_args()
    config=json.loads(args.config.read_text(encoding="utf-8")) if args.config.exists() else {}
    if args.test_sunken:
        args.model=HERE.parent/"sunken_skeleton_ref/sunken_skeleton.bbmodel"
        config={"model_scale":1.0,"held":"weapon","glow":[]}
    scene,metadata=build_scene(args.model.resolve(),config,args.weapon,args.right_arm_rest)
    args.out.mkdir(parents=True,exist_ok=True)
    allvertices=np.concatenate([face["vertices"] for face in scene])
    bodyvertices=np.concatenate([face["vertices"] for face in scene if not face["source"].startswith("existing_spear")])
    center=(bodyvertices.min(axis=0)+bodyvertices.max(axis=0))/2
    size=(900,1100)
    fits=[]
    for direction,_ in VIEWS.values():
        projected=(allvertices-center) @ camera_basis(direction).T
        fits.append(min((size[0]-120)/(2*np.abs(projected[:,0]).max()),(size[1]-160)/(2*np.abs(projected[:,1]).max())))
    scale=min(fits)
    metadata["views"]={}
    images=[]
    for key,(direction,label) in VIEWS.items():
        preview=render(scene,direction,label,scale,center,size)
        preview.save(args.out/(key+".png"))
        comparison(preview,label,args.out/(key+"_comparison.png"))
        images.append(preview)
        metadata["views"][key]={"camera_toward":direction,"pixels_per_scaled_model_unit":scale,"center":center.tolist()}
    board=Image.new("RGB",(1800,2200))
    for i,img in enumerate(images):board.paste(img,((i%2)*900,(i//2)*1100))
    board.save(args.out/"four_views.png")
    metadata["limitations"]=["Software preview, not a real Minecraft screenshot", "Fixed original 3q references, no invented original rear view", "Item generated alpha edges approximated as separate texel boundary quads"]
    (args.out/"render_metadata.json").write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"out":str(args.out),"quads":len(scene),"views":list(VIEWS),"model_sha256":metadata["model_sha256"]}))


if __name__=="__main__":main()
