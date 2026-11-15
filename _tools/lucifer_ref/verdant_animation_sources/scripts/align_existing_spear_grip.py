"""Apply the approved rigid bind-space grip translation once through native BB.

No weapon geometry is rebuilt and no project file is saved by this script.
The immutable weapon_native_input.json is the pre-alignment source adapter.
"""
from pathlib import Path
import hashlib
import itertools
import json
import sys

import numpy as np
from PIL import Image

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'lucifer_original'))
from native_import import checked, js_literal


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source_path = HERE / 'weapon_native_input.json'
    input_path = HERE / 'lucifer_verdant_input.json'
    source = json.loads(source_path.read_text(encoding='utf-8'))
    before_hash = sha(input_path)
    source_vertices = source['parts'][0]['vertices']
    world = np.array(source['binding']['world_matrix_from_generated_pixels'])
    socket = np.array(source['binding']['native_bind_world'])
    source_grip = np.array([9.25, 6.25, 8.0, 1.0])
    grip_before = world @ source_grip
    delta = socket[:3, 3] - grip_before[:3]
    expected = np.array([8.881784197001252e-16, -1.3989585340023023, -1.6062441766262074])
    assert np.max(np.abs(delta - expected)) == 0
    shift = np.eye(4)
    shift[:3, 3] = delta
    aligned_world = shift @ world
    aligned = {k: [v[i] + float(delta[i]) for i in range(3)] for k, v in source_vertices.items()}
    payload = {'project': 'lucifer_verdant', 'mesh': 'weapon__LuciferSerpentSpear',
               'before': source_vertices, 'after': aligned, 'delta': delta.tolist()}
    code = '(()=>{const d=' + js_literal(payload) + ';' + r'''
      const candidates=ModelProject.all.filter(p=>p.name===d.project);
      if(candidates.length!==1)throw new Error('Expected one lucifer_verdant project');
      candidates[0].select();
      if(Project.name!==d.project)throw new Error('Project selection mismatch');
      const mesh=Mesh.all.find(m=>m.name===d.mesh);
      if(!mesh)throw new Error('Weapon mesh missing');
      const keys=Object.keys(d.before);
      if(Object.keys(mesh.vertices).length!==keys.length || keys.some(k=>!mesh.vertices[k]))throw new Error('Vertex keys differ');
      function err(expected){let e=0;for(const k of keys)for(let i=0;i<3;i++)e=Math.max(e,Math.abs(mesh.vertices[k][i]-expected[k][i]));return e;}
      const beforeError=err(d.before), afterError=err(d.after);
      if(beforeError>1e-10 && afterError>1e-10)throw new Error('Neither original nor aligned coordinates; refusing repeat/unknown edit');
      const snapshot=()=>JSON.stringify({
        faces:Object.fromEntries(Object.entries(mesh.faces).map(([k,f])=>[k,f.getSaveCopy()])),
        origin:mesh.origin,rotation:mesh.rotation,parent:mesh.parent.uuid,
        bones:ArmatureBone.all.map(b=>b.getSaveCopy()),
        others:Mesh.all.filter(m=>m!==mesh).map(m=>m.getSaveCopy())
      });
      const fixedBefore=snapshot();
      let applied=false;
      if(beforeError<=1e-10){
        Undo.initEdit({elements:[mesh]});
        for(const k of keys)mesh.vertices[k]=d.after[k].slice();
        mesh.preview_controller.updateGeometry(mesh);
        Canvas.updateAll();
        Undo.finishEdit('Align existing spear shaft to original hand socket');
        applied=true;
      }
      if(fixedBefore!==snapshot())throw new Error('Unexpected change outside weapon vertices');
      const finalError=err(d.after);
      if(finalError!==0)throw new Error('Alignment mismatch '+finalError);
      return {project:Project.name,mesh:mesh.name,vertices:keys.length,applied,
        already_aligned:!applied,before_error:beforeError,after_error:finalError,
        nonvertex_fields_unchanged:true,saved_final:false};
    })()'''
    native = checked('risky_eval', {'code': code})
    if not isinstance(native, dict) or native.get('after_error') != 0:
        raise RuntimeError(native)
    # Re-read after RPC so changes made concurrently to other input fields survive.
    data = json.loads(input_path.read_text(encoding='utf-8'))
    parts = [p for p in data['parts'] if p['name'] == payload['mesh']]
    assert len(parts) == 1
    part = parts[0]
    assert set(part['vertices']) == set(aligned)
    input_old_error = max(abs(part['vertices'][k][i] - source_vertices[k][i]) for k in aligned for i in range(3))
    input_new_error = max(abs(part['vertices'][k][i] - aligned[k][i]) for k in aligned for i in range(3))
    assert min(input_old_error, input_new_error) <= 1e-10, 'Unexpected input weapon edit'
    part['vertices'] = aligned
    input_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    arm = next(p for p in data['parts'] if p['name'] == 'body__R_Arm')
    arm_vertices = np.array(list(arm['vertices'].values()))
    arm_min, arm_max = arm_vertices.min(axis=0), arm_vertices.max(axis=0)
    source_corners = np.array([[x,y,z,1] for x,y,z in itertools.product([9,9.5],[6,6.5],[7.5,8.5])])
    world_corners = (aligned_world @ source_corners.T).T[:,:3]
    inside = np.logical_and(world_corners >= arm_min, world_corners <= arm_max).all()
    assert inside
    points = {'grip': source_grip, 'tip': np.array([1.25,15.25,8,1]),
              'base': np.array([14.25,.75,8,1])}
    world_points = {name: (aligned_world @ p)[:3].tolist() for name,p in points.items()}
    direction = np.array(world_points['tip']) - np.array(world_points['base'])
    direction /= np.linalg.norm(direction)
    texture = Path(source['texture_path'])
    report = {
        'scope':'Approved rigid translation of original existing spear only; not a source Dungeons weapon pose.',
        'native_result':native,
        'immutable_adapter_input':str(source_path),'immutable_adapter_sha256':sha(source_path),
        'combined_input':str(input_path),'combined_input_sha256_before':before_hash,
        'combined_input_sha256_after':sha(input_path),
        'source_png':str(texture),'source_png_sha256':sha(texture),
        'grip_pixel_xy':[18,19],'grip_pixel_rgba':list(Image.open(texture).convert('RGBA').getpixel((18,19))),
        'grip_uv_pixel_center':[18.5,19.5],'grip_source_model_xyz':source_grip[:3].tolist(),
        'translation_global_bind':delta.tolist(),
        'translation_socket_local':(np.linalg.inv(socket)[:3,:3] @ delta).tolist(),
        'translation_matrix_global_bind':shift.tolist(),
        'world_matrix_before':world.tolist(),'world_matrix_after':aligned_world.tolist(),
        'socket_local_matrix_after':(np.linalg.inv(socket) @ aligned_world).tolist(),
        'grip_world_before':grip_before[:3].tolist(),'semantic_points_world_after':world_points,
        'base_to_tip_unit_direction_after':direction.tolist(),
        'grip_eight_corners_world_after':world_corners.tolist(),
        'right_arm_bind_aabb':[arm_min.tolist(),arm_max.tolist()],
        'all_grip_corners_inside_right_arm_bind_volume':bool(inside),
        'minimum_bind_clearance':float(min((world_corners-arm_min).min(),(arm_max-world_corners).min())),
        'requirements':['Geometry shape, UV, topology, texture and bone weights remain unchanged.',
          'Animation J_R_Weapon and J_L_Weapon position channels must be zero to retain hand socket location.',
          'Dynamic grip retention requires independent animation validation; this result proves bind alignment only.'],
        'final_project_saved_by_this_script':False
    }
    (HERE/'weapon_grip_alignment.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'native':native,'delta':delta.tolist(),'inside':bool(inside),
                      'report':str(HERE/'weapon_grip_alignment.json')},ensure_ascii=False))


if __name__ == '__main__':
    main()
