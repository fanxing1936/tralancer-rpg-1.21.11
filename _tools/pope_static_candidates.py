"""在同一个教皇工程临时渲染握杖局部 A/B；finally恢复，不写bbmodel。"""
import base64,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from pope_blockbench import BlockbenchMCP
REF=Path(__file__).resolve().parent/'pope_ref'
OUT=REF/'m2/candidates'

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    spec=json.loads((REF/'m2/model_spec.json').read_text(encoding='utf-8'));pid=spec['blockbench_project']['uuid'];c=BlockbenchMCP()
    js="""(function(){const project=ModelProject.all.find(p=>p.uuid===PID);if(!project||project.name!=='pope_m2_static')throw Error('工程隔离');project.select();
    const hand=Cube.all.find(e=>e.name==='left_hand'),arm=Cube.all.find(e=>e.name==='left_forearm');
    const old=[hand,arm].map(e=>({from:e.from.slice(),to:e.to.slice()}));
    const p=new Preview({id:'pope_hand_candidates',offscreen:true,antialias:false});p.setProjectionMode(true);p.resize(750,600);p.renderer.setPixelRatio(1);
    const target=new THREE.Vector3(-9.5,11,0);p.camOrtho.position.set(-19,17,-25);p.controls.target.copy(target);p.camOrtho.up.set(0,1,0);p.camOrtho.lookAt(target);p.camOrtho.zoom=(600/40)/7;p.camOrtho.updateProjectionMatrix();p.controls.update();
    const result={};try{for(const id of ['A','B']){if(id==='B'){hand.from.splice(0,3,-10.5,10.5,-.5);hand.to.splice(0,3,-9.5,11.5,.5);arm.from[0]=-9.5;}Canvas.updateAll();Canvas.withoutGizmos(()=>{p.render();result[id]=p.canvas.toDataURL('image/png')});}}
    finally{[hand,arm].forEach((e,i)=>{e.from.splice(0,3,...old[i].from);e.to.splice(0,3,...old[i].to)});Canvas.updateAll();p.renderer.dispose();}
    result.restored=[hand,arm].every((e,i)=>JSON.stringify(e.from)===JSON.stringify(old[i].from)&&JSON.stringify(e.to)===JSON.stringify(old[i].to));return result;})()""".replace('PID',json.dumps(pid))
    results=c.evaluate(js)
    if not results['restored']:raise RuntimeError('候选渲染恢复失败')
    for k in ['A','B']:(OUT/('grip_'+k+'.png')).write_bytes(base64.b64decode(results[k].split(',')[1]))
    image=Image.new('RGBA',(2250,760),(55,60,70,255));font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',26);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',21);d=ImageDraw.Draw(image)
    source=Image.open(REF/'MCD_Arch-Illager.png').convert('RGBA').crop((365,590,530,755));source=source.resize((600,600),Image.Resampling.NEAREST);image.alpha_composite(source,(75,90))
    labels=['原作局部 / 原文件有手臂 Z-fighting','A：细握块包住杖杆（当前模型）','B：灰臂平接杖杆（握姿推断）']
    notes=['条纹是参考缺陷；不按它建立重叠面','手块四侧外扩 0.05，遮住共面红杖','缩短臂末端，手和杖杆相接，无叠面']
    for idx in range(3):
        x=idx*750;d.text((x+18,18),labels[idx],font=font,fill='white');d.text((x+18,715),notes[idx],font=small,fill='#d6dce4')
        if idx:image.alpha_composite(Image.open(OUT/('grip_'+['A','B'][idx-1]+'.png')).convert('RGBA'),(x,90))
    image.convert('RGB').save(OUT/'grip_choices.jpg',quality=94)
    (OUT/'grip_choices.json').write_text(json.dumps(dict(engine='Blockbench native WebGL',source_bbmodel_sha256=hashlib.sha256((REF/'pope.bbmodel').read_bytes()).hexdigest(),candidates=dict(A='source geometry; hand expands 0.05 in XYZ to prevent coplanar staff faces',B='temporary hand from[-10.5,10.5,-.5] to[-9.5,11.5,.5]; forearm minX=-9.5'),restored=results['restored'],no_file_model_edits=True),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('已渲染握杖A/B；原工程几何恢复。')

if __name__=='__main__':main()
