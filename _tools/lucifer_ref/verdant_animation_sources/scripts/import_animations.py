from pathlib import Path
import json,sys,hashlib
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'lucifer_original'))
from native_import import checked,js_literal,REF
SELECT='ModelProject.all.find(p=>p.name==="lucifer_verdant").select();'

def native(code):return checked('risky_eval',{'code':SELECT+code})

def save_large():
    info=native('(()=>{globalThis.luciferNativeSave=Codecs.project.compile();return {size:luciferNativeSave.length,name:Project.name,precision:Codecs.project.compile.toString().includes("source_precision")};})()')
    assert info['precision'] and info['name']=='lucifer_verdant'
    chunks=[]
    for start in range(0,info['size'],400000):chunks.append(native('luciferNativeSave.slice('+str(start)+','+str(start+400000)+')'))
    path=REF/'separate/lucifer_verdant.bbmodel';path.write_text(''.join(chunks),encoding='utf-8',newline='\n')
    native('Project.save_path='+js_literal(str(path))+';Project.saved=true;true')
    print({'path':str(path),'size':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})

def main():
    payload=json.loads((HERE/'animation_payload.json').read_text(encoding='utf-8'))
    native('while(Animation.all.length)Animation.all[0].remove();true')
    for a in payload:
        code='(()=>{const d='+js_literal(a)+';const a=new Animation({name:d.name,loop:d.loop,length:d.length,snapping:d.snapping}).add();const report=[];for(const tr of d.tracks){const b=Outliner.elements.find(x=>x.type==="armature_bone"&&x.name===tr.bone);if(!b)throw Error(tr.bone);const an=a.getBoneAnimator(b);for(const k of tr.keyframes){const key=an.addKeyframe(k);for(const axis of ["x","y","z"])key.data_points[0][axis]=k.data_points[0][axis].toFixed(15);}report.push({bone:b.name,keys:tr.keyframes.length});}return {name:a.name,length:a.length,tracks:report.length};})()'
        print(native(code),flush=True)
    native('Modes.options.animate.select();Animation.all.forEach(a=>a.playing=false);Animation.all[0].select();Animation.all[0].playing=true;Timeline.time=0;Animator.preview();true')
    save_large()

if __name__=='__main__':main()
