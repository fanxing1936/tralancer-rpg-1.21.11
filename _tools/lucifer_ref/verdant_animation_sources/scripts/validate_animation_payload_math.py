"""Read-only source_clip/payload audit; no native UI calls or writes to inputs.

The default source mapping describes the current original-source clips. Any later
retimed/adapted clip requires explicit per-frame source-time/adapted-bone metadata;
do not silently label those frames source-exact.
"""
from pathlib import Path
import importlib.util, hashlib, json, math
import numpy as np
from audit_animation_source import reference_frame, sha, FROZEN_SHA256, SOURCE

ROOT=Path(__file__).resolve().parent

def euler_zyx(v):
    x,y,z=np.radians(v)
    rx=np.array([[1,0,0],[0,math.cos(x),-math.sin(x)],[0,math.sin(x),math.cos(x)]])
    ry=np.array([[math.cos(y),0,math.sin(y)],[0,1,0],[-math.sin(y),0,math.cos(y)]])
    rz=np.array([[math.cos(z),-math.sin(z),0],[math.sin(z),math.cos(z),0],[0,0,1]])
    return rz@ry@rx

def main():
    assert sha(SOURCE)==FROZEN_SHA256
    source=json.loads(SOURCE.read_text(encoding='utf-8'))
    builder=ROOT/'build_animations.py'
    before=sha(builder)
    spec=importlib.util.spec_from_file_location('read_only_animation_builder',builder)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    results=[]
    for a in source['animations']:
        c=mod.source_clip(a['short_name'])
        max_local_r=max_local_p=max_world_r=max_world_p=0.
        for f,t in enumerate(c['times']):
            expected=reference_frame(source,a['short_name'],float(t))
            wr,wp=mod.world(c['lr'][f],c['lp'][f])
            for i,(local,world) in enumerate(zip(expected['target_local'],expected['target_world'])):
                max_local_r=max(max_local_r,float(np.max(np.abs(local[:3,:3]-c['lr'][f,i]))))
                max_local_p=max(max_local_p,float(np.max(np.abs(local[:3,3]-c['lp'][f,i]))))
                max_world_r=max(max_world_r,float(np.max(np.abs(world[:3,:3]-wr[i]))))
                max_world_p=max(max_world_p,float(np.max(np.abs(world[:3,3]-wp[i]))))
        results.append({'source':a['short_name'],'frames':len(c['times']),
                        'local_rotation_matrix_max_error':max_local_r,'local_position_max_error_px':max_local_p,
                        'world_rotation_matrix_max_error':max_world_r,'world_position_max_error_px':max_world_p})
    payload_path=ROOT/'animation_payload.json';npz_path=ROOT/'animation_pose_reference.npz'
    payload_results=[]
    if payload_path.exists() and npz_path.exists():
        payload=json.loads(payload_path.read_text(encoding='utf-8'));ref=np.load(npz_path)
        for a in payload:
            name=a['name'].removeprefix('animation.');times=ref[name+'__times'];lr=ref[name+'__lr'];lp=ref[name+'__lp']
            tracks={t['bone']:t['keyframes'] for t in a['tracks']}
            mr=mp=0.
            for bi,b in enumerate(mod.BONES):
                bone_keys=tracks.get(b['name'],[])
                for channel,base in [('rotation',mod.REST_E[bi]),('position',mod.REST_P[bi])]:
                    keys=sorted([k for k in bone_keys if k['channel']==channel],key=lambda k:k['time'])
                    values={float(k['time']):np.array([float(k['data_points'][0][axis]) for axis in 'xyz']) for k in keys}
                    for fi,t in enumerate(times):
                        if not values:v=np.zeros(3)
                        elif len(values)==1:v=next(iter(values.values()))
                        else:
                            assert float(t) in values, 'reference sample missing exact native payload key'
                            v=values[float(t)]
                        if channel=='rotation':mr=max(mr,float(np.max(np.abs(euler_zyx(base+v)-lr[fi,bi]))))
                        else:mp=max(mp,float(np.max(np.abs(base+v-lp[fi,bi]))))
            payload_results.append({'clip':name,'frames':len(times),'ZYX_rest_plus_channel_to_reference_matrix_max_error':mr,'rest_plus_position_to_reference_max_error_px':mp})
    unchanged=sha(builder)==before
    passed=all(max(r[k] for k in r if k.endswith('_error') or k.endswith('_error_px'))<1e-9 for r in results)
    passed=passed and all(r['ZYX_rest_plus_channel_to_reference_matrix_max_error']<1e-9 and r['rest_plus_position_to_reference_max_error_px']<1e-9 for r in payload_results)
    result={'status':'PASS' if passed and unchanged else 'FAIL_OR_INPUT_CHANGED',
            'scope':'Independent matrix implementation vs builder source_clip, plus payload Euler+rest reconstruction vs NPZ. Does not inspect current native Blockbench serialization or game playback.',
            'source_sha256':sha(SOURCE),'builder_sha256':before,'builder_unchanged_during_audit':unchanged,
            'source_clip_results':results,'payload_results':payload_results,
            'payload_sha256':sha(payload_path) if payload_results else None,'npz_sha256':sha(npz_path) if payload_results else None,
            'weapon_adaptation':'If payload uses target-rest weapon position, that is an explicit staff-to-spear adaptation; source_clip comparison remains pre-adaptation.'}
    (ROOT/'animation_payload_math_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    assert passed and unchanged

if __name__=='__main__':main()
