"""M2：通过本机 Blockbench 原生 Group/Cube/Texture API 建立教皇静态工程。

只写 pope_ref；不接入资源包、不生成动画。所有 UV 来源逐面登记。
"""
from __future__ import annotations
import base64
import hashlib
import io
import json
import uuid
from pathlib import Path
from PIL import Image
from pope_blockbench import BlockbenchMCP

HERE=Path(__file__).resolve().parent
REF=HERE/'pope_ref'
OUT=REF/'m2'
ARCH='_tools/heart_of_ender_ref/MCD_Arch-Illager_(texture).png'
STAFF='_tools/pope_ref/T_SuperStaff.png'
CUBE='_tools/pope_ref/T_SuperCube.png'
FACES=('north','east','south','west','up','down')

def uid(name): return str(uuid.uuid5(uuid.NAMESPACE_URL,'tralancer:pope:m2:'+name))
def write_json(path,obj): path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

class Builder:
    def __init__(self):
        self.groups=[];self.elements=[];self.provenance=[]
        self.atlas=Image.new('RGBA',(128,64),(0,0,0,0))
        self.placements=[];self.extra={};self.next_x=64;self.next_y=32;self.row_h=0
        for source,x,y in [(ARCH,0,0),(STAFF,64,0),(CUBE,96,0)]:
            im=Image.open(HERE.parent/source).convert('RGBA');self.atlas.paste(im,(x,y))
            self.placements.append(dict(source_file=source,source_rect=[0,0,*im.size],atlas_rect=[x,y,x+im.width,y+im.height],transform='identity'))

    def group(self,name,pivot,parent='root',rotation=(0,0,0)):
        self.groups.append(dict(name=name,uuid=uid('bone:'+name),origin=list(pivot),rotation=list(rotation),parent=parent))

    def uv(self,rect,source=ARCH,transform='identity'):
        if transform=='identity':
            ox=0 if source==ARCH else 64 if source==STAFF else 96
            return [rect[0]+ox,rect[1],rect[2]+ox,rect[3]]
        key=(source,tuple(rect),transform)
        if key not in self.extra:
            im=Image.open(HERE.parent/source).convert('RGBA').crop(rect)
            operation={'rotate90_cw':Image.Transpose.ROTATE_270,'rotate270_cw':Image.Transpose.ROTATE_90,'flip_h':Image.Transpose.FLIP_LEFT_RIGHT,'flip_v':Image.Transpose.FLIP_TOP_BOTTOM,'rotate180':Image.Transpose.ROTATE_180}[transform]
            im=im.transpose(operation)
            if self.next_x+im.width>128:self.next_x=64;self.next_y+=self.row_h;self.row_h=0
            if self.next_y+im.height>64:raise ValueError('图集额外裁片区域已满')
            x,y=self.next_x,self.next_y;dest=[x,y,x+im.width,y+im.height]
            self.atlas.paste(im,(x,y));self.placements.append(dict(source_file=source,source_rect=rect,atlas_rect=dest,transform=transform))
            self.extra[key]=dest;self.next_x+=im.width;self.row_h=max(self.row_h,im.height)
        return self.extra[key].copy()

    def cube(self,name,bone,lo,hi,maps,note,status='依据展开与多视角重建'):
        element=dict(name=name,uuid=uid('element:'+name),bone=bone,from_=lo,to=hi,origin=[0,0,0],rotation=[0,0,0],box_uv=False,autouv=0,faces={})
        for face in FACES:
            if face not in maps:
                element['faces'][face]=dict(uv=[0,0,0,0],texture=None);continue
            data=maps[face]
            if isinstance(data,list):data={'rect':data}
            rect=data['rect'];source=data.get('source',ARCH);transform=data.get('transform','identity')
            uv=self.uv(rect,source,transform)
            if data.get('flip_u'):uv=[uv[2],uv[1],uv[0],uv[3]]
            if data.get('flip_v'):uv=[uv[0],uv[3],uv[2],uv[1]]
            element['faces'][face]=dict(uv=uv,texture=0,rotation=0)
            self.provenance.append(dict(element_uuid=element['uuid'],element_name=name,face=face,atlas_uv=uv,source_file=source,source_rect=rect,transform=transform,flip_u=data.get('flip_u',False),flip_v=data.get('flip_v',False),note=note,status=status))
        element['from']=element.pop('from_');self.elements.append(element)

def make_spec():
    b=Builder();b.group('root',[0,0,0],None)
    b.group('body',[0,7,0]);b.group('head',[0,12.5,0],'body',(0,0,8))
    b.group('crown',[0,19.5,0],'head')
    b.group('right_arm',[3.5,11,0],'body',(0,0,-48))
    b.group('right_hand',[10.5,11,0],'right_arm')
    b.group('left_arm',[-3.5,11,0],'body')
    b.group('left_hand',[-10.5,11,0],'left_arm')
    b.group('right_leg',[1.65,6,0],'body');b.group('left_leg',[-1.65,6,0],'body')
    b.group('cape',[0,12,2.2],'body')
    b.group('staff',[-11,11,0],'left_hand')
    b.group('staff_glow',[-11,22.2645298841,0],'staff',(47.24528227,17.71481121,44.80072472))
    b.cube('head_gray','head',[-6,12.5,-3],[6,19.5,3],dict(zip(FACES,[[6,6,18,13],[18,6,24,13],[24,6,36,13],[0,6,6,13],[6,0,18,6],[18,0,30,6]])), '12×7×6 灰头完整盒网；眉眼另外逐像素贴面')
    b.cube('nose','head',[-1,11.5,-4],[1,15.5,-3],dict(zip(FACES,[[2,14,4,18],[4,14,5,18],[0,14,2,18],[5,14,6,18],[2,13,4,14],[2,18,4,19]])), '2×4×1 鼻子完整28像素盒网；深灰背面藏于脸部，182灰为两个1×4侧面')
    for side,s in [('right',1),('left',-1)]:
        b.group(side+'_brow',[s*3,17,-3.015],'head',(0,0,s*8))
        for kind,rect,span in [('brow_vertical',[4,2,6,4],[3,16.5,5,18.5]),('brow_horizontal',[2,4,6,5],[1,15.5,5,16.5])]:
            x0,y0,x1,y1=span
            lo=[min(s*x0,s*x1),y0,-3.015];hi=[max(s*x0,s*x1),y1,-3.015]
            b.cube(side+'_'+kind,side+'_brow',lo,hi,{'north':dict(rect=rect,flip_u=s>0)},'眉毛仅取57灰L形8像素；头面投影测得外缘距头边约1单位，左右各内压8°；不取43灰背景','原作头面投影重建，角度约±2°测量误差')
        # User-selected B: throne/front-idle white base and a small upper pupil.
        b.cube(side+'_eye','head',[min(s,s*4),14.5,-3.02],[max(s,s*4),15.5,-3.02],{'north':[5,5,6,6]},'用户选定眼神B：王座/正面Idle；原眼岛白像素铺满3×1眼底，眼区±[1,4]，外缘距头边2单位')
        b.cube(side+'_pupil','head',[min(s*1.3,s*2.4),15,-3.04],[max(s*1.3,s*2.4),15.5,-3.04],{'north':[3,5,5,6]},'用户选定眼神B：原眼岛37灰两像素映射1.1×0.5上半小瞳；鼻侧留0.3单位白边；瞳面前移0.02避免与白底共面')
    crown_faces=dict(zip(FACES[:4],[[36,5,40,15],[40,5,44,15],[44,5,48,15],[48,5,52,15]]))
    crown_faces['up']=[40,0,44,4]
    b.cube('crown_shaft','crown',[-2,19.5,-2],[2,29.5,2],crown_faces,'高冠侧带去除透明齿行，顶面用独立金环；底部贴头隐藏，不封')
    for name,lo,hi,rect in [('front',[-1,29.5,-2],[1,30.5,-1.7],[37,4,39,5]),('back',[-1,29.5,1.7],[1,30.5,2],[45,4,47,5]),('right',[1.7,29.5,-1],[2,30.5,1],[41,4,43,5]),('left',[-2,29.5,-1],[-1.7,30.5,1],[49,4,51,5])]:
        b.cube('crown_tooth_'+name,'crown',lo,hi,{f:rect for f in FACES if f!='down'},'齿行原始不透明两像素；侧/顶复用同一金色齿像素，几何明确重建')
    b.cube('inner_tunic','body',[-3.5,6,-1.9],[3.5,12.5,1.9],dict(zip(FACES,[[5,27,13,36],[14,27,19,36],[19,27,27,36],[0,27,5,36],[5,22,14,27],[5,36,14,40]])), '绿色内衣与蓝金躯干网；前面居中8像素去掉右侧额外蓝列；隐藏面按几何拉伸，未挪用内衬','分面来源明确；隐藏边界与几何为重建')
    b.cube('robe_open_shell','body',[-4,1.1,-2.1],[4,13.8,2.1],{'north':[36,15,44,29],'east':[43,15,47,29],'west':[32,15,36,29]},'蓝袍前开口和两侧白下缘；前面透明4列保留；u43金缝共享；肩端白领伸入头下避免宽白围领','衣片分割为工作候选')
    b.cube('cape_back','cape',[-4,1.1,2.1],[4,13.8,2.3],{'south':[47,15,55,29],'north':dict(rect=[47,15,55,29],flip_u=True),'east':[54,15,55,29],'west':[47,15,48,29],'down':[47,28,55,29],'up':[47,15,55,16]},'背布蓝色主体、上端白领、整条白下缘；内侧明确复用同片，不使用空白背景','连续帧可见外侧；内侧为推断复用')
    for side,sgn in [('right',1),('left',-1)]:
        def box(x0,x1,y0,y1,z0,z1):return ([min(sgn*x0,sgn*x1),y0,z0],[max(sgn*x0,sgn*x1),y1,z1])
        arm=side+'_arm';hand=side+'_hand';offset=0 if sgn>0 else 4
        # Sleeve walls along X: U follows sleeve axis. No face.rotation.
        x0,x1=3.5,6.5; y0,y1=9.5,12.5; z0,z1=-1.5,1.5
        strip=lambda v,flip=False:dict(rect=[52+offset,v,56+offset,v+3],flip_u=flip)
        # North/south and horizontal faces are assigned explicit quarter turns in atlas where needed.
        walls=[('front',box(x0,x1,y0,y1,z0,z0+.4),{'north':strip(3,sgn>0),'south':strip(3,sgn<0)}),
               ('back',box(x0,x1,y0,y1,z1-.4,z1),{'south':strip(9,sgn<0),'north':strip(9,sgn>0)}),
               ('top',box(x0,x1,y1-.4,y1,z0,z1),{'up':strip(6,sgn<0),'down':strip(6,sgn>0)}),
               ('bottom',box(x0,x1,y0,y0+.4,z0,z1),{'down':strip(12,sgn<0),'up':strip(12,sgn>0)})]
        for name,(lo,hi),maps in walls:
            # Rim end picks gold last column of that wall, caps hidden at shoulder.
            v={'front':3,'top':6,'back':9,'bottom':12}[name]
            maps['east' if sgn>0 else 'west']=[55+offset,v,56+offset,v+3]
            b.cube(side+'_sleeve_'+name,arm,lo,hi,maps,'A16开放袖筒：四张4×3侧壁，末列金色朝外；内侧复用同片，无实心金盖')
        lo,hi=box(x0,x0+.15,y0,y1,z0,z1)
        b.cube(side+'_sleeve_shoulder',arm,lo,hi,{'west' if sgn>0 else 'east':[52+offset,0,55+offset,3]},'A16各套3×3肩端封帽；袖口另一端敞开')
        for kind,a,zlen,target in [('forearm',3.5,7,arm),('hand',10.5,1,hand)]:
            lo,hi=box(a,a+zlen,10.5,11.5,-.5,.5)
            if kind=='hand' and side=='left':
                lo=[v-.05 for v in lo];hi=[v+.05 for v in hi]
            maps={}
            for f,col in [('north',6),('up',7),('south',8),('down',9)]:
                rect=[col,13 if kind=='forearm' else 20,col+1,20 if kind=='forearm' else 21]
                maps[f]=dict(rect=rect,transform='rotate90_cw',flip_u=sgn<0)
            maps['east' if sgn>0 else 'west']=[6,20,7,21]
            b.cube(side+'_'+kind,target,lo,hi,maps,'连续1×8灰臂带旋转90°后1:1入图集；手是末一段独立部件，端面复用灰末像素','手部端面/灰带周向为工作候选')
        center=1.65*sgn
        b.cube(side+'_shorts',side+'_leg',[center-1.5,3,-1.5],[center+1.5,6,1.5],dict(zip(FACES,[[13,16,16,19],[16,16,19,19],[19,16,22,19],[10,16,13,19],[13,13,16,16],[13,19,16,22]])), '3³暗青短裤盒网；两条腿共享')
        b.cube(side+'_gold_leg',side+'_leg',[center-.5,.1,-.5],[center+.5,3.1,.5],dict(zip(FACES,[[1,19,2,22],[2,19,3,22],[3,19,4,22],[0,19,1,22],[2,18,3,19],[1,18,2,19]])), '1×3×1金腿盒网；灰色上端插入短裤，红色下端接脚片')
        b.cube(side+'_red_foot',side+'_leg',[center-.5,0,-2.5],[center+.5,.1,.5],{'up':[4,18,5,21],'down':[4,18,5,21],'north':[4,18,5,19],'south':[4,20,5,21],'east':[4,18,5,21],'west':[4,18,5,21]},'独立1×3纯红脚片；脚尖沿-Z；窄侧明确复用脚片边缘','薄片厚度0.1为刚性管线重建')
    # Necklace: own exact ring island and gemstone island; no unregistered color swatches.
    b.group('chain_right',[1.2,11.3,-2.25],'body',(0,0,-25))
    b.group('chain_left',[-1.2,11.3,-2.25],'body',(0,0,25))
    for side,s in [('right',1),('left',-1)]:
        b.cube('necklace_ring_'+side,'chain_'+side,[s*1.2-.65,8.5,-2.35],[s*1.2+.65,11.5,-2.35],{'north':[22,16,25,20],'south':dict(rect=[22,16,25,20],flip_u=True)},'3×4金环原片透明孔保留；两环单轴25°，合并body')
    b.cube('necklace_ruby','body',[-1,7.2,-3.3],[1,9.2,-2.3],{'north':[18,20,20,22],'south':[21,20,23,22],'west':[17,20,18,22],'east':[20,20,21,22],'up':[18,19,20,20],'down':[18,22,20,23]},'2×2×1 吊坠完整16像素盒网；正面红白占满，金边是实体侧面，排除43底色四角')
    b.cube('staff_rod','staff',[-11.5,0,-.5],[-10.5,17,.5],{f:dict(rect=r,source=STAFF) for f,r in zip(FACES,[[0,0,1,18],[1,0,2,18],[2,0,3,18],[3,0,4,18],[0,0,1,1],[0,18,1,19]])},'T_SuperStaff四条1×18像素杆；几何1×17×1按主图投影比例拟合；灰红灰金纵向布局不重绘','UV网确定；17单位杆长为参考比例重建')
    b.cube('staff_tray','staff',[-12.5,17,-1.5],[-9.5,18,1.5],{f:dict(rect=r,source=STAFF) for f,r in zip(FACES,[[5,0,8,1],[8,1,9,4],[5,4,8,5],[4,1,5,4],[5,1,8,4],[9,1,12,4]])},'3×1×3托盘完整展开；接杆底面深灰中心')
    b.cube('staff_core','staff_glow',[-13.5,19.7645298841,-2.5],[-8.5,24.7645298841,2.5],{f:dict(rect=([7,0,10,32] if f in ['west','east'] else [10,0,13,32]),source=CUBE) for f in FACES},'T_SuperCube原图整数列数值拟合：大面10..12，窄面7..9，V全高；详见M2 UV拟合证据；不改色、不加bloom','可见面颜色高置信拟合；面名/隐藏面对面复用及静息转角为重建')
    parts=[[name,[name]+(['chain_right','chain_left'] if name=='body' else ['right_brow','left_brow'] if name=='head' else [])] for name in ['body','head','crown','right_arm','right_hand','left_arm','left_hand','right_leg','left_leg','cape','staff','staff_glow']]
    return b,parts

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    existing=REF/'pope.bbmodel'
    if existing.exists() and json.loads(existing.read_text(encoding='utf-8')).get('animations'):
        raise RuntimeError('M2静态生成器不能覆盖已含M3动画的事实来源。')
    b,parts=make_spec();buf=io.BytesIO();b.atlas.save(buf,format='PNG');data=buf.getvalue()
    (OUT/'atlas.png').write_bytes(data)
    spec=dict(stage='M2_static',key='pope',label='教皇',tag='rpg.pope',score='rpg_pp',eye_expression='B',eye_expression_selected_by_user=True,parts=parts,glow=['staff_glow'],model_scale=1,atlas_sources=b.placements,height_bones=[g['name'] for g in b.groups if g['name'] not in ['root','staff','staff_glow']],groups=b.groups,elements=b.elements,coordinate_system='+Y up; face -Z; character right +X',construction='Blockbench native Group/Cube/Texture API; no manual unrecorded edits')
    # Native APIs preserve exact face UVs; no Bedrock geometry importer sign flips.
    client=BlockbenchMCP()
    found=client.evaluate("ModelProject.all.filter(p=>p.name==='pope_m2_static').map(p=>p.uuid)")
    if len(found)>1:raise RuntimeError('多个同名工程，需先明确目标')
    if not found:
        client.tool('create_project',dict(name='pope_m2_static',format='bedrock'))
        found=client.evaluate("ModelProject.all.filter(p=>p.name==='pope_m2_static').map(p=>p.uuid)")
    project_uuid=found[0]
    js="""(function(){const p=ModelProject.all.find(p=>p.uuid===PROJECT_ID);if(!p||p.name!=='pope_m2_static')throw Error('项目隔离校验失败');p.select();
    const d=SPEC;
    for(const e of [...Outliner.root])e.remove();for(const t of [...Texture.all])t.remove();
    Project.texture_width=128;Project.texture_height=64;Project.box_uv=false;
    const tex=new Texture({name:'pope_atlas.png',uuid:TEXTURE_ID,uv_width:128,uv_height:64}).fromDataURL(ATLAS);tex.add(false);tex.width=128;tex.height=64;
    const groups={};for(const g of d.groups){const copy={...g};delete copy.parent;const node=new Group(copy,g.uuid);if(g.parent)node.addTo(groups[g.parent]);node.init();groups[g.name]=node;}
    for(const e of d.elements){const copy={...e,faces:{},color:0};delete copy.bone;for(const [f,v] of Object.entries(e.faces))copy.faces[f]={...v,texture:v.texture===null?null:tex.uuid};new Cube(copy,e.uuid).addTo(groups[e.bone]).init();}
    Canvas.updateAll();Project.name='pope_m2_static';return {uuid:Project.uuid,elements:Cube.all.length,groups:Group.all.length,animations:Animation.all.length};})()"""
    for key,value in [('PROJECT_ID',project_uuid),('SPEC',spec),('TEXTURE_ID',uid('atlas')),('ATLAS','data:image/png;base64,'+base64.b64encode(data).decode())]:js=js.replace(key,json.dumps(value,ensure_ascii=False).replace('/',r'\u002f'))
    info=client.evaluate(js);print(json.dumps(info,ensure_ascii=False))
    code="(function(){const p=ModelProject.all.find(p=>p.uuid==="+json.dumps(project_uuid)+");if(!p||p.name!=='pope_m2_static')throw Error('项目隔离');p.select();return Codecs.project.compile({raw:true});})()"
    doc=client.evaluate(code)
    if isinstance(doc,str):doc=json.loads(doc)
    model=REF/'pope.bbmodel';write_json(model,doc)
    # Measure real rest transform, including head lean; scale to 2.6 blocks.
    from types import SimpleNamespace
    import display_mob
    from pope_validate_model import posed_bounds
    bones,_,_=display_mob.load_bbmodel(SimpleNamespace(bbmodel=model))
    lo,hi=posed_bounds(bones,spec['height_bones']);spec['rest_bounds']=[lo,hi];spec['model_scale']=41.6/(hi[1]-lo[1])
    spec['blockbench_project']=info;spec['model_sha256']=hashlib.sha256(model.read_bytes()).hexdigest()
    write_json(OUT/'model_spec.json',spec);write_json(OUT/'face_provenance.json',b.provenance)
    client.evaluate("(function(){const p=ModelProject.all.find(p=>p.uuid==="+json.dumps(project_uuid)+");if(!p||p.name!=='pope_m2_static')throw Error('项目隔离');p.select();p.save_path="+json.dumps(str(model))+";p.saved=true;return true;})()")
    print(json.dumps(dict(model=str(model),faces=len(b.provenance),parts=len(parts),model_scale=spec['model_scale']),ensure_ascii=False))

if __name__=='__main__':main()
