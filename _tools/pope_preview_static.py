"""M2 Blockbench 原生渲染与参考并排；Pillow仅做排版，不修改模型渲染。"""
import argparse,base64,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from pope_blockbench import BlockbenchMCP

REF=Path(__file__).resolve().parent/'pope_ref'
OUT=REF/'m2'/'preview'
FONT='C:/Windows/Fonts/msyh.ttc'
BG=(55,60,70,255)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',default='preview');args=p.parse_args()
    out=REF/'m2'/args.output
    if not out.resolve().is_relative_to((REF/'m2').resolve()):raise ValueError('仅写m2目录')
    out.mkdir(parents=True,exist_ok=True)
    client=BlockbenchMCP();spec=json.loads((REF/'m2/model_spec.json').read_text(encoding='utf-8'));pid=spec['blockbench_project']['uuid']
    prefix="const project=ModelProject.all.find(p=>p.uuid==="+json.dumps(pid)+");if(!project||project.name!=='pope_m2_static')throw Error('项目隔离');project.select();"
    ready=client.evaluate('(function(){'+prefix+'return {ready:Texture.all.every(t=>t.img.complete&&t.img.naturalWidth>0),name:Project.name,elements:Cube.all.length,animations:Animation.all.length};})()')
    if not ready['ready']:raise RuntimeError('贴图未解码')
    views=[dict(name='front',direction=[0,0,-1]),dict(name='side',direction=[-1,0,0]),dict(name='right_side',direction=[1,0,0]),dict(name='back',direction=[0,0,1]),dict(name='three_quarter',direction=[-.62,.39,-.69]),dict(name='front_reference',direction=[0,.12,-1]),dict(name='side_reference',direction=[-1,.58,.08]),dict(name='back_reference',direction=[.06,.6,1])]
    code="""(function(){PREFIX
      const defs=DEFS;const p=new Preview({id:'pope_m2_offscreen',offscreen:true,antialias:false});
      p.setProjectionMode(true);p.resize(900,1000);p.renderer.setPixelRatio(1);
      const box=new THREE.Box3();Cube.all.forEach(c=>box.expandByObject(c.mesh));const center=box.getCenter(new THREE.Vector3());
      const result={bounds:[box.min.toArray(),box.max.toArray()],views:{}};
      for(const v of defs){const target=center.clone();const pos=target.clone().addScaledVector(new THREE.Vector3(...v.direction).normalize(),100);
       p.camOrtho.position.copy(pos);p.controls.target.copy(target);p.camOrtho.up.set(0,1,0);p.camOrtho.lookAt(target);p.camOrtho.zoom=(1000/40)/38;p.camOrtho.updateProjectionMatrix();p.controls.update();
       let data;Canvas.withoutGizmos(()=>{p.render();data=p.canvas.toDataURL('image/png')});result.views[v.name]={data,position:pos.toArray(),target:target.toArray(),height:38};
      }p.renderer.dispose();return result;})()""".replace('PREFIX',prefix).replace('DEFS',json.dumps(views))
    result=client.evaluate(code)
    for name,v in result['views'].items():(out/(name+'.png')).write_bytes(base64.b64decode(v.pop('data').split(',')[1]))
    result.update(engine='Blockbench 5.2.2 native WebGL Preview',model_sha256=hashlib.sha256((REF/'pope.bbmodel').read_bytes()).hexdigest(),opened=ready,stage='static; no animation; no bloom; no recolor; not Minecraft runtime')
    (out/'render_evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    font=ImageFont.truetype(FONT,26);small=ImageFont.truetype(FONT,20)
    def fitted(path,size):
        im=Image.open(path).convert('RGBA');bbox=im.getbbox();im=im.crop(bbox) if bbox else im;scale=min(size[0]/im.width,size[1]/im.height);return im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
    def panel(path,label,note='',width=900,height=1100):
        pane=Image.new('RGBA',(width,height),BG);im=fitted(path,(width-80,height-150));pane.alpha_composite(im,((width-im.width)//2,90+(height-150-im.height)//2));d=ImageDraw.Draw(pane);d.text((20,16),label,font=font,fill='white');d.text((20,height-45),note,font=small,fill='#d7dbe1');return pane
    reference=REF/'m2/reference'
    pairs=[('front','front_reference','front_source_crop.png','正面：坐姿参考，核对头脸/衣领','已选王座宽眼白；原作坐姿，模型站姿'),('side','side_reference','side_source_crop.png','侧面：动态图转身帧','原作动作姿态；此处核对前后结构与连接'),('back','back_reference','back_source_crop.png','背面：瞬移动图背帧','原作飞起姿态；核对蓝背布和白下缘'),('three_quarter','three_quarter','three_quarter_source_crop.png','四分之三：原作主渲染','原图窄白；模型按用户选择采用王座宽白')]
    board=Image.new('RGBA',(1800,4400),BG)
    for idx,(name,render,src,title,note) in enumerate(pairs):
        srcpath=reference/src
        if not srcpath.exists():
            print('缺参考裁片',srcpath);continue
        pair=Image.new('RGBA',(1800,1100),BG);pair.alpha_composite(panel(srcpath,'原作 / Mojang · '+title,note),(0,0));pair.alpha_composite(panel(out/(render+'.png'),'M2 / Blockbench 原生渲染',note),(900,0));pair.convert('RGB').save(out/(name+'_comparison.jpg'),quality=94);board.alpha_composite(pair,(0,idx*1100))
    board.convert('RGB').save(out/'four_views_comparison.jpg',quality=94)
    grid=Image.new('RGBA',(1800,2200),BG)
    for name,label,pos in [('front','正面',(0,0)),('side','左侧（持杖侧）',(900,0)),('back','背面',(0,1100)),('three_quarter','四分之三',(900,1100))]:grid.alpha_composite(panel(out/(name+'.png'),label),(pos))
    grid.convert('RGB').save(out/'four_views_model.jpg',quality=94)
    print(json.dumps(dict(out=str(out),views=len(views),bounds=result['bounds']),ensure_ascii=False))

if __name__=='__main__':main()
