"""用保存的 M3 .bbmodel 在 Blockbench 原生动画时间轴渲染；不后期补光。

请求 JSON: {views:{id:{position,target,height,width?,height_px?,isolate_inner?,ground_y?}},
frames:[{id,clip,time,view}]}。所有输出限制在任务素材目录。
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import display_mob as dm
from heart_of_ender_blockbench import BlockbenchMCP, REF

def value(result):
    return json.loads(next(x["text"] for x in result["content"] if x["type"] == "text"))

def render(request_file, output, port=52907, model=None):
    output = output.resolve()
    if not output.is_relative_to(REF.resolve()):
        raise ValueError("输出必须在任务素材目录内")
    output.mkdir(parents=True, exist_ok=True)
    path = (model or REF / "heart_of_ender.bbmodel").resolve()
    if not path.is_relative_to(REF.resolve()):
        raise ValueError("输入模型必须在任务素材目录内")
    doc = json.loads(path.read_text(encoding="utf-8"))
    req = json.loads(request_file.read_text(encoding="utf-8"))
    client = BlockbenchMCP(port)
    client.tool("create_project", {"name": "heart_of_ender_m3_review", "format": "bedrock"})
    serialized = json.dumps(doc).replace("/", r"\u002f")
    info = value(client.evaluate("(function(){Codecs.project.parse("+serialized+");Modes.options.animate.select();return {uuid:Project.uuid,animations:Animation.all.map(a=>a.name),elements:Cube.all.length};})()"))
    client.evaluate("(function(){Project.save_path="+json.dumps(str(path))+";Project.saved=true;return true;})()")
    state = value(client.evaluate("({loaded:Texture.all.every(t=>t.img.complete && t.img.naturalWidth>0)})"))
    if not state["loaded"]:
        raise RuntimeError("贴图尚未解码，请重跑预览")
    mob = SimpleNamespace(bbmodel=path, anim_from=None, key="heart_of_ender")
    bones, _, _ = dm.load_bbmodel(mob)
    clips = dm.load_animations(mob)
    evidence = {"engine": "Blockbench native WebGL + native animation timeline", "project": info,
        "bbmodel_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "fullbright": "cloned source ShaderMaterial with same map, SHADE=false; all model cubes",
        "postprocessing": "none; no bloom, no recoloring of rendered pixels", "views": req["views"], "frames": []}
    profile = req.get("material_profile", "blockbench")
    if profile not in ("blockbench", "minecraft_item_alpha"):
        raise ValueError("未知的材质预览配置")
    evidence["material_profile"] = profile
    if profile == "minecraft_item_alpha":
        evidence["profile_limit"] = "Offline alpha/cull/blend approximation: cutoff 0.1, front faces, normal alpha blend, depth write. Not the Minecraft renderer; face sorting and directional light are not reproduced."
    for start in range(0, len(req["frames"]), 8):
        batch = req["frames"][start:start+8]
        code = """(function(){
          const frames=FRAMES,views=VIEWS,profile=PROFILE;
          Animator.showDefaultPose();Canvas.scene.updateMatrixWorld(true);
          const restMatrices=Object.fromEntries(Group.all.map(g=>[g.name,g.mesh.matrixWorld.clone()]));
          const originals=[];
          for(const cube of Cube.all){
            const original=cube.mesh.material,fullbright=original.clone();
            fullbright.uniforms.map.value=original.uniforms.map.value;
            fullbright.map=original.map;fullbright.uniforms.SHADE.value=false;
            if(profile==='minecraft_item_alpha'){
              fullbright.fragmentShader=fullbright.fragmentShader.replace('color.a<0.01','color.a<0.1');
              fullbright.side=THREE.FrontSide;fullbright.transparent=true;fullbright.depthWrite=true;
              fullbright.blending=THREE.NormalBlending;fullbright.needsUpdate=true;
            }
            cube.mesh.material=fullbright;originals.push([cube,original,fullbright,cube.mesh.visible]);
          }
          const p=new Preview({id:'heart_of_ender_m3_offscreen',offscreen:true,antialias:false});
          p.setProjectionMode(true);const result=[];
          for(const f of frames){
            const a=Animation.all.find(a=>a.name==='animation.'+f.clip);
            if(!a)throw new Error('missing animation '+f.clip);
            a.select();Timeline.setTime(f.time);Animator.preview();
            const v=views[f.view],w=v.width||500,h=v.height_px||500;
            for(const [cube] of originals)cube.mesh.visible=!v.isolate_inner||cube.parent.name.startsWith('inner_');
            p.resize(w,h);p.renderer.setPixelRatio(1);
            p.camOrtho.position.set(...v.position);p.controls.target.set(...v.target);p.camOrtho.up.set(0,1,0);
            if(v.follow_bone){
              Canvas.scene.updateMatrixWorld(true);
              const g=Group.all.find(g=>g.name===v.follow_bone);
              const delta=g.mesh.matrixWorld.clone().multiply(restMatrices[v.follow_bone].clone().invert());
              p.camOrtho.position.applyMatrix4(delta);p.controls.target.applyMatrix4(delta);p.camOrtho.up.transformDirection(delta);
            }
            p.camOrtho.lookAt(p.controls.target);p.camOrtho.zoom=(h/40)/v.height;p.camOrtho.updateProjectionMatrix();p.controls.update();
            let floor;
            if(v.ground_y!==undefined){
              floor=new THREE.Mesh(new THREE.BoxGeometry(400,200,400),new THREE.MeshBasicMaterial({color:0x373c46}));
              floor.position.y=v.ground_y-100;Canvas.scene.add(floor);
            }
            Canvas.scene.updateMatrixWorld(true);
            const matrices=Group.all.map(g=>({name:g.name,matrix:g.mesh.matrixWorld.toArray()}));
            let data;Canvas.withoutGizmos(()=>{p.render();data=p.canvas.toDataURL('image/png');});
            result.push({id:f.id,time:Timeline.time,data,matrices,camera:{position:p.camOrtho.position.toArray(),target:p.controls.target.toArray(),up:p.camOrtho.up.toArray()}});
            if(floor){Canvas.scene.remove(floor);floor.geometry.dispose();floor.material.dispose();}
          }
          for(const [cube,original,fullbright,visible] of originals){cube.mesh.material=original;cube.mesh.visible=visible;fullbright.dispose();}
          p.renderer.dispose();return result;
        })()""".replace("FRAMES", json.dumps(batch)).replace("VIEWS", json.dumps(req["views"])).replace("PROFILE", json.dumps(profile))
        rendered = value(client.evaluate(code))
        for expected, got in zip(batch, rendered):
            rel = Path(expected["id"]+".png")
            target = (output / rel).resolve()
            if not target.is_relative_to(output):
                raise ValueError("帧路径越界")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(base64.b64decode(got["data"].split(",", 1)[1]))
            maxerr, worst = 0, None
            for native in got["matrices"]:
                bone = native["name"]
                predicted = dm.mat_mul(dm.posed_matrix(bones, bone, clips[expected["clip"]], expected["time"]), dm.translate(*bones[bone]["pivot"]))
                error = max(abs(predicted[r][c]-native["matrix"][c*4+r]) for r in range(4) for c in range(4))
                if error > maxerr:
                    maxerr, worst = error, bone
            evidence["frames"].append({**expected, "path": str(rel).replace("\\", "/"),
                "native_timeline_time": got["time"], "matrix_max_error_vs_pipeline": maxerr, "matrix_worst_bone": worst,
                "actual_camera":got["camera"],
                "sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
        print(f"Blockbench 渲染 {min(start+8,len(req['frames']))}/{len(req['frames'])}", flush=True)
    errors = [x["matrix_max_error_vs_pipeline"] for x in evidence["frames"]]
    evidence["matrix_max_error_vs_pipeline"] = max(errors, default=0)
    (output / "render_evidence.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("native/pipeline matrix max error", evidence["matrix_max_error_vs_pipeline"])
    return evidence

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("requests", type=Path)
    ap.add_argument("--output", type=Path, default=REF / "m3_preview")
    ap.add_argument("--port", type=int, default=52907)
    ap.add_argument("--model",type=Path,help="可选研究副本；默认正式主文件")
    args = ap.parse_args()
    render(args.requests, args.output, args.port,args.model)

if __name__ == "__main__":
    main()
