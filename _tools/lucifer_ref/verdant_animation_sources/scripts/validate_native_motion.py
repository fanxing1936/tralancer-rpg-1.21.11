"""Compare every authored pose to the running native Blockbench scene matrices."""
from pathlib import Path
import json,sys,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'lucifer_original'))
from native_import import checked,js_literal,REF
from build_animations import BONES,world

def main():
    poses=np.load(HERE/'animation_pose_reference.npz')
    payload=json.loads((HERE/'animation_payload.json').read_text(encoding='utf-8'))
    reports=[]
    for a in payload:
        name=a['name'].split('.')[-1];times=poses[name+'__times'];rot=poses[name+'__lr'];pos=poses[name+'__lp']
        frames=[]
        for f,t in enumerate(times):
            wr,wp=world(rot[f],pos[f]);m=np.zeros((len(BONES),4,4));m[:,:3,:3]=wr;m[:,:3,3]=wp;m[:,3,3]=1
            frames.append({'time':float(t),'matrices':m.transpose(0,2,1).reshape(len(BONES),16).tolist()})
        clip=[]
        for offset in range(0,len(frames),20):
            code='(()=>{ModelProject.all.find(p=>p.name==="lucifer_verdant").select();Modes.options.animate.select();Animation.all.forEach(a=>a.playing=false);const a=Animation.all.find(a=>a.name==='+js_literal(a['name'])+');a.select();a.playing=true;const names='+js_literal([b['name'] for b in BONES])+';const bones=names.map(n=>Outliner.elements.find(e=>e.type==="armature_bone"&&e.name===n));const frames='+js_literal(frames[offset:offset+20])+';return frames.map(f=>{Timeline.time=f.time;Animator.preview();let r=0,p=0,bone="";bones.forEach((b,i)=>{const actual=b.mesh.matrixWorld.toArray();for(let k=0;k<16;k++){const d=Math.abs(actual[k]-f.matrices[i][k]);if(k>=12&&k<=14){p=Math.max(p,d);}else if(d>r){r=d;bone=b.name;}}});return {time:Timeline.time,rotation_error:r,position_error_px:p,worst_rotation_bone:bone};});})()'
            result=checked('risky_eval',{'code':code})
            if not isinstance(result,list):raise RuntimeError(result)
            clip.extend(result)
        report={'clip':name,'poses':len(clip),'max_rotation_matrix_error':max(x['rotation_error'] for x in clip),'max_position_error_px':max(x['position_error_px'] for x in clip),'frames':clip}
        reports.append(report);print({k:v for k,v in report.items() if k!='frames'},flush=True)
    maxr=max(r['max_rotation_matrix_error'] for r in reports);maxp=max(r['max_position_error_px'] for r in reports)
    out={'status':'PASS' if maxr<1e-9 and maxp<1e-8 else 'FAIL','project':'lucifer_verdant','native':'Blockbench 5.2.2','scope':'Every authored source/adapted key pose against actual native armature world matrices, after native interpolation and Molang numeric parsing. Does not validate Minecraft rendering.',
        'decimal_serialization':'Native addKeyframe generates scientific notation for tiny nonzero channels; explicit fixed decimal numeric strings prevent Molang exponent parsing as subtraction. No expressions or scale tracks.',
        'payload_sha256':hashlib.sha256((HERE/'animation_payload.json').read_bytes()).hexdigest(),'reference_sha256':hashlib.sha256((HERE/'animation_pose_reference.npz').read_bytes()).hexdigest(),'max_rotation_error':maxr,'max_position_error_px':maxp,'clips':reports}
    (REF/'separate/verdant_native_animation_validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print('STATUS',out['status'])
    if out['status']!='PASS':raise SystemExit(1)

if __name__=='__main__':main()
