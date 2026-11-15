from pathlib import Path
import json,sys,base64
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'lucifer_original'))
from native_import import checked,js_literal,REF

def capture(clip,t,label=None,position=None,target=None,height=64,output_dir=None):
    target=target or [0,23,0];position=position or [70,44,-100]
    code='(()=>{ModelProject.all.find(p=>p.name==="lucifer_verdant").select();Modes.options.animate.select();unselectAll();Animation.all.forEach(a=>a.playing=false);const a=Animation.all.find(a=>a.name==='+js_literal('animation.'+clip)+');a.select();a.playing=true;Timeline.time='+str(t)+';Animator.preview();const v=Preview.selected;v.loadAnglePreset({position:'+js_literal(position)+',target:'+js_literal(target)+',projection:"orthographic"});v.camOrtho.zoom=(v.camOrtho.top-v.camOrtho.bottom)/'+str(height)+';v.camOrtho.updateProjectionMatrix();v.camera.lookAt(v.controls.target);let picture;Screencam.screenshotPreview(v,{crop:false},url=>picture=url);return {project:Project.name,clip:a.name,time:Timeline.time,picture};})()'
    result=checked('risky_eval',{'code':code})
    if isinstance(result,str):raise RuntimeError(result)
    assert result['project']=='lucifer_verdant' and result['clip']=='animation.'+clip
    path=(output_dir or REF/'native')/(label or f'lucifer_verdant_{clip}_{t:.3f}.png')
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(base64.b64decode(result.pop('picture').split(',')[1]))
    return dict(result,path=str(path))

if __name__=='__main__':
    clip=sys.argv[1] if len(sys.argv)>1 else 'idle';t=float(sys.argv[2]) if len(sys.argv)>2 else 0
    print(capture(clip,t))
