"""原生渲染A/B原作表情；用户已选B，临时对照结束后恢复保存模型的几何。"""
import base64,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from pope_blockbench import BlockbenchMCP
REF=Path(__file__).resolve().parent/'pope_ref'
OUT=REF/'m2/eye_fix'

def render(c,pid):
    code="""(function(){const p=ModelProject.all.find(p=>p.uuid===PID);if(!p||p.name!=='pope_m2_static')throw Error('工程隔离');p.select();
    const head=Group.all.find(g=>g.name==='head');const previousAngle=head.rotation.slice();
    const white=['right','left'].map(s=>Cube.all.find(c=>c.name===s+'_eye'));const pupils=['right','left'].map(s=>Cube.all.find(c=>c.name===s+'_pupil'));
    const items=[...white,...pupils];const original=items.map(e=>({from:e.from.slice(),to:e.to.slice()}));const visibility=Cube.all.map(e=>[e,e.visibility]);
    const v=new Preview({id:'pope_eye_review',offscreen:true,antialias:false});v.setProjectionMode(true);v.resize(840,600);v.renderer.setPixelRatio(1);
    const output={};try{head.rotation[2]=0;for(const [e] of visibility)e.visibility=(e.parent===head||e.parent.name.endsWith('_brow'));Canvas.updateAll();
    for(const expression of ['A','B']){for(let i=0;i<2;i++){const sign=i===0?1:-1;if(expression==='A'){white[i].from.splice(0,3,Math.min(3*sign,4*sign),14.5,-3.02);white[i].to.splice(0,3,Math.max(3*sign,4*sign),15.5,-3.02);pupils[i].from.splice(0,3,Math.min(sign,3*sign),14.5,-3.02);pupils[i].to.splice(0,3,Math.max(sign,3*sign),15.5,-3.02);}else{white[i].from.splice(0,3,Math.min(sign,4*sign),14.5,-3.02);white[i].to.splice(0,3,Math.max(sign,4*sign),15.5,-3.02);pupils[i].from.splice(0,3,Math.min(1.3*sign,2.4*sign),15,-3.04);pupils[i].to.splice(0,3,Math.max(1.3*sign,2.4*sign),15.5,-3.04);}}
    Canvas.updateAll();const target=new THREE.Vector3(0,15.55,-2.8);v.camOrtho.position.copy(target).add(new THREE.Vector3(0,0,-100));v.controls.target.copy(target);v.camOrtho.up.set(0,1,0);v.camOrtho.lookAt(target);v.camOrtho.zoom=(600/40)/9;v.camOrtho.updateProjectionMatrix();v.controls.update();Canvas.withoutGizmos(()=>{v.render();output[expression]=v.canvas.toDataURL('image/png')});}}
    finally{head.rotation.splice(0,3,...previousAngle);items.forEach((e,i)=>{e.from.splice(0,3,...original[i].from);e.to.splice(0,3,...original[i].to)});for(const [e,visible] of visibility)e.visibility=visible;Canvas.updateAll();v.renderer.dispose();}
    output.restored=items.every((e,i)=>JSON.stringify(e.from)===JSON.stringify(original[i].from)&&JSON.stringify(e.to)===JSON.stringify(original[i].to))&&JSON.stringify(head.rotation)===JSON.stringify(previousAngle);return output;})()""".replace('PID',json.dumps(pid))
    return c.evaluate(code)

def main():
    OUT.mkdir(parents=True,exist_ok=True);c=BlockbenchMCP();spec=json.loads((REF/'m2/model_spec.json').read_text(encoding='utf-8'));result=render(c,spec['blockbench_project']['uuid']);assert result['restored']
    for name in ['A','B']:(OUT/('expression_'+name+'.png')).write_bytes(base64.b64decode(result[name].split(',')[1]))
    font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',28);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',21);bg=(55,60,70,255)
    board=Image.new('RGBA',(1680,1440),bg);draw=ImageDraw.Draw(board)
    refs=[('主渲染：窄白、大瞳（透视校正分析图）','main_face_rectified.png','A：主渲染 / 普通 Idle 表情对照'),('王座正面：宽白、小瞳（原图裁片）','source_front.png','B：王座 / 正面 Idle（用户选定）')]
    for i,(title,path,label) in enumerate(refs):
        y=i*720;draw.text((20,y+18),title,font=font,fill='white');draw.text((860,y+18),label,font=font,fill='white')
        im=Image.open(OUT/path).convert('RGBA');scale=min(790/im.width,580/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);board.alpha_composite(im,((840-im.width)//2,y+82+(580-im.height)//2));board.alpha_composite(Image.open(OUT/('expression_'+['A','B'][i]+'.png')).convert('RGBA'),(840,y+72))
        draw.text((20,y+680),'两种原作表情不同；校正图只用于测量，非新增素材。',font=small,fill='#d7dce4');draw.text((860,y+680),'两版眼位一致；头归正用于局部审阅，不是动画。',font=small,fill='#d7dce4')
    board.convert('RGB').save(OUT/'eye_choices.jpg',quality=95)
    board.crop((0,720,1680,1440)).convert('RGB').save(OUT/'eye_B_selected.jpg',quality=95)
    # Before/after keep the same camera, frame and whole-model scale.
    before=Image.open(OUT/'before/three_quarter_comparison.jpg').crop((900,0,1800,1100));after=Image.open(REF/'m2/preview/three_quarter_comparison.jpg').crop((900,0,1800,1100))
    diff=Image.new('RGB',(1800,1160),(55,60,70));diff.paste(before,(0,60));diff.paste(after,(900,60));d=ImageDraw.Draw(diff);d.text((20,12),'修正前：眼睛与眉毛偏外',font=font,fill='white');d.text((920,12),'已选 B：眼位内收，宽白、小瞳',font=font,fill='white');diff.save(OUT/'before_after.jpg',quality=95)
    old=json.loads((OUT/'before/model.json').read_text(encoding='utf-8'));now=json.loads((REF/'pope.bbmodel').read_text(encoding='utf-8'));eye_names={s+'_'+n for s in ['left','right'] for n in ['eye','pupil','brow_vertical','brow_horizontal']}
    original_other={e['name']:e for e in old['elements'] if e['name'] not in eye_names};current_other={e['name']:e for e in now['elements'] if e['name'] not in eye_names};assert original_other==current_other
    original_groups={g['name']:g for g in old['groups']};current_groups={g['name']:g for g in now['groups'] if not g['name'].endswith('_brow')};assert original_groups==current_groups
    evidence=dict(engine='Blockbench native WebGL',model_sha256=hashlib.sha256((REF/'pope.bbmodel').read_bytes()).hexdigest(),before_sha256=hashlib.sha256((OUT/'before/model.json').read_bytes()).hexdigest(),selected_expression='B',selected_by_user=True,temporary_candidate_restored=result['restored'],non_eye_elements_unchanged=len(original_other),existing_groups_unchanged=len(original_groups),head_normalized_for_review_only=True,expressions={'A':'primary render / ordinary Idle: outer white1x1, inner pupil2x1','B':'throne / front Idle: white3x1, inner pupil1.1x0.5 with0.3 inner margin'},eye_span=[1,4],brow_rest_degrees=[8,-8])
    (OUT/'eye_fix_validation.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(evidence,ensure_ascii=False))

if __name__=='__main__':main()
