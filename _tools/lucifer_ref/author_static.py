"""检查点 A 候选重建。原图/原骨架不修改；每个输出面均记录来源与推断。

lucifer.bbmodel 是后续编辑和导出的事实来源；本脚本只用于复现本次初始静态候选。
禁止在后续 Blockbench 编辑后无条件重跑覆盖工程。
"""
from pathlib import Path
import base64, copy, io, json, math, sys, uuid
from PIL import Image
import numpy as np

HERE=Path(__file__).resolve().parent
TOOLS=HERE.parent
sys.path.insert(0,str(TOOLS))
import display_mob as dm

def ident(name): return str(uuid.uuid5(uuid.NAMESPACE_URL,'tralancer/lucifer_lord/static/'+name))
def write(name,obj): (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

original=json.loads((TOOLS/'sunken_skeleton_ref/sunken_skeleton.bbmodel').read_text(encoding='utf-8'))
body=Image.open(HERE/'T_MossySkeleton.png').convert('RGBA')
armor=Image.open(HERE/'Root_Rot_Armor_texture.png').convert('RGBA')
shadow=Image.open(HERE/'RootRotArmor_ShadowTexture_(MCD).png').convert('RGB')
atlas=Image.new('RGBA',(128,128))
body_arr=np.array(body)
body_arr[:,:,3]=np.where(body_arr[:,:,3]>=128,255,0)
atlas.paste(Image.fromarray(body_arr),(0,0))
atlas.paste(armor,(64,0))
# 原版 Unreal 材质缺失：仅为原图绿色亮部做可追溯的外观补偿，非证明材质公式。
# ShadowTexture 的青色区域 + diffuse -> 淡绿端部；洋红/黄色通道完全不处理。
derived=np.array(armor).copy()
mask=np.array(shadow)
energy=np.minimum(mask[:,:,1],mask[:,:,2]).astype(float)
energy=np.where((mask[:,:,0]<32)&(energy>=64),energy,0)
for c,gain in enumerate((0.75,1.0,0.60)):
    derived[:,:,c]=np.minimum(255,derived[:,:,c].astype(float)+energy*gain).astype(np.uint8)
atlas.paste(Image.fromarray(derived),(64,64))
# 内衬只复制已核对的独立单像素，不借用其他装备/贴图岛。
atlas.putpixel((0,33),armor.getpixel((12,1)))
atlas.save(HERE/'lucifer_atlas.png')

doc=copy.deepcopy(original)
doc.update(name='路西法 · 第一阶段 · 静态候选 A',model_identifier='lucifer_lord',
           resolution={'width':128,'height':128},animations=[],elements=[],groups=[],outliner=[])
doc['meta']['box_uv']=False
doc['meta']['model_format']='bedrock'
doc['animation_variable_placeholders']=''
groups={}; nodes={}; rows=[]
base_groups={g['name']:g for g in original['groups']}

def group(name,parent=None,origin=None,rotation=None):
    if name in base_groups:
        g=copy.deepcopy(base_groups[name]); g['uuid']=ident('bone/'+name)
    else:
        g={'name':name,'uuid':ident('bone/'+name),'export':True,'visibility':True,'children':[],
           'origin':origin or [0,0,0],'rotation':rotation or [0,0,0],'color':0,'shade':True,'autouv':0}
    if origin is not None:g['origin']=origin
    if rotation is not None:g['rotation']=rotation
    groups[name]=g;doc['groups'].append(g)
    n={'uuid':g['uuid'],'isOpen':False,'children':[]}; nodes[name]=n
    (nodes[parent]['children'] if parent else doc['outliner']).append(n)

group('root');group('body','root');group('head','body')
group('right_arm','body');group('left_arm','body')
group('right_leg','root');group('left_leg','root')
group('eyes_glow','head',[0,24,0])
group('sprout_left','head',[-2.6,32.75,0], [0,0,-10])
group('sprout_right','head',[2.6,32.75,0], [0,0,10])

def spec(uv,source='armor',basis='候选重建：展开尺寸与图案支持，未由原作网格确认',derived=False):
    return {'uv':list(uv),'source':source,'basis':basis,'derived':derived}

def cube(name,bone,frm,to,faces):
    e={'name':name,'uuid':ident('cube/'+name),'type':'cube','box_uv':False,'from':list(frm),'to':list(to),
       'origin':[0,0,0],'rotation':[0,0,0],'export':True,'visibility':True,'autouv':0,'faces':{}}
    for face,s in faces.items():
        u0,v0,u1,v1=s['uv']; src=s['source']
        if src=='body': off=(0,0); fn='T_MossySkeleton.png'
        elif src=='lining': off=(0,0); fn='Root_Rot_Armor_texture.png'
        else: off=(64,64 if s['derived'] else 0); fn='Root_Rot_Armor_texture.png'
        uv=[u0+off[0],v0+off[1],u1+off[0],v1+off[1]]
        if src=='lining':uv=[0,33,1,34]
        e['faces'][face]={'uv':uv,'texture':0}
        rows.append({'element':name,'bone':bone,'face':face,'source_file':fn,'source_uv':s['uv'],
                     'atlas_uv':uv,'evidence':s['basis'],
                     'processing':('独立复制原像素，无改色' if src=='lining' else
                        'ShadowTexture青色区域的候选绿色亮部补偿；非原版材质还原' if s['derived'] else
                        'alpha>=128二值化；RGB不改' if src=='body' else '原像素不改'),
                     'source_geometry':'Sunken骨架裁切' if src=='body' else '用户已允许的候选重建'})
    doc['elements'].append(e);nodes[bone]['children'].append(e['uuid'])
    return e

def boxfaces(front,side1,back,side2,top,bottom,**kw):
    return {f:spec(uv,**kw) for f,uv in zip(['north','east','south','west','up','down'],
                  [front,side1,back,side2,top,bottom])}

# 被兜帽/衣身完整遮挡的原头、原身体不输出。手与腿只留外露段。
removed=[]
for e in original['elements']:
    n=e['name']
    if n in ('head','body','coral','sprig'):
        removed.append({'element':n,'reason':'兜帽/衣身遮挡' if n in ('head','body') else 'Sunken独有附属物不属于Mossy'})
        continue
    if n not in ('right_arm','left_arm','right_leg','left_leg'):continue
    frm=e['from'].copy();to=e['to'].copy()
    if 'arm' in n:to[1]=14
    else:frm[1]=6.5
    faces={}
    for face,data in e['faces'].items():
        if face in ('up','down'):continue # 与袖/靴相交的端面不保留
        u0,v0,u1,v1=data['uv'];oldh=e['to'][1]-e['from'][1]
        nv0=v0+(e['to'][1]-to[1])/oldh*(v1-v0)
        nv1=v0+(e['to'][1]-frm[1])/oldh*(v1-v0)
        faces[face]=spec([u0,nv0,u1,nv1],'body','继承Sunken原逐面UV，仅按露出长度裁切；见UV_BODY_ANALYSIS.md')
    cube('mossy_'+n+'_exposed',n,frm,to,faces)

# 兜帽 10x10x9.75，前框最前缘为z=-5；骷髅头每侧外扩0.75~1px。
hood=boxfaces([0,18,10,28],[0,8,10,18],[20,8,30,18],[10,8,20,18],[10,0,20,8],[12,1,13,2])
hood['north']['basis']='暗脸/双眼图案像素定位；平面与外框厚度为候选'
hood['up']['basis']='候选顶面：10x8源区映射10x10面，V拉伸1.25；原网格未确认'
hood['down']=spec([12,1,13,2],'lining','已数值核对#14250D；内衬几何为候选')
cube('root_rot_hood','head',[-5,23,-4.75],[5,33,5],hood)
# 帽檐在暗脸外沿，不把双眼当成裸露骷髅面。
rim_regions={'north':spec([10,8,20,10]),'south':spec([12,1,13,2],'lining'),
             'up':spec([10,0,20,1]),'down':spec([12,1,13,2],'lining'),
             'east':spec([10,8,11,10]),'west':spec([19,8,20,10])}
cube('hood_brow','head',[-5,31,-5],[5,33,-4.75],rim_regions)
for side,x0,x1,u in [('right',4,5,10),('left',-5,-4,19)]:
    faces={f:spec([u,10,u+1,18]) for f in ('north','east','west')}
    faces.update({f:spec([12,1,13,2],'lining') for f in ('up','down','south')})
    cube('hood_rim_'+side,'head',[x0,23,-5],[x1,31,-4.75],faces)

# 原作帽檐可见的下垂苔条：按已定位苔区裁片，深度不超头部外扩1px。
for i,(x0,x1,bottom,u) in enumerate([(2.5,3.5,29,10),(-.5,.5,28.5,14),(-3.5,-2.5,30,18)]):
    faces={f:spec([u,10,u+1,14],basis='帽檐苔区精确裁片；条长与分布为轮廓重建推断')
           for f in ('north','east','west')}
    faces.update({f:spec([12,1,13,2],'lining') for f in ('south','up','down')})
    cube('hood_moss_drop_'+str(i),'head',[x0,bottom,-5],[x1,32,-4.75],faces)

for side,x0,x1,uv in [('right',1,3,[2,24,4,25]),('left',-3,-1,[6,24,8,25])]:
    cube('green_eye_'+side,'eyes_glow',[x0,26,-4.80],[x1,27,-4.77],
         {'north':spec(uv,basis='原暗脸双眼精确区域；绿色材质亮度补偿为候选',derived=True)})

# 保留像素形状的薄体积嫩芽，分别绑定head的子骨骼；不是第二套item_display。
for side,xc,uv in [('left',-2.6,[34,47,39,52]),('right',2.6,[42,48,47,53])]:
    u0,v0,u1,v1=uv
    for v in range(v0,v1):
        for u in range(u0,u1):
            if armor.getpixel((u,v))[3]<128:continue
            x=xc+(u-u0-2.5)*.65;y=32.8+(v1-1-v)*.65
            faces={f:spec([u,v,u+1,v+1],basis='嫩芽连通域精确像素；体积/位置/倾斜为候选',derived=True)
                   for f in ('north','east','south','west','up','down')}
            cube(f'sprout_{side}_{u}_{v}','sprout_'+side,[x,y,-.35],[x+.65,y+.65,.35],faces)

torso=boxfaces([37,10,47,24],[33,10,37,24],[51,10,61,24],[47,10,51,24],
              [37,6,47,10],[12,1,13,2])
torso['down']=spec([12,1,13,2],'lining','内衬专用单像素；不复用衣袖纹理')
cube('root_rot_torso','body',[-5,11,-3],[5,25,3],torso)

for side,x0,x1,du in [('right',3,7,0),('left',-7,-3,14)]:
    # 4x3贴图展开映射4x3外层，原2x2骨臂每侧外扩0.5~1px。
    faces=boxfaces([3+du,31,7+du,41],[du,31,3+du,41],[10+du,31,14+du,41],
                   [7+du,31,10+du,41],[3+du,28,7+du,31],[12,1,13,2])
    faces['down']=spec([12,1,13,2],'lining','袖口内衬专用单像素')
    cube('root_rot_sleeve_'+side,side+'_arm',[x0,14,-1.5],[x1,24.5,1.5],faces)

for side,x0,x1 in [('right',0,4),('left',-4,0)]:
    faces=boxfaces([4,46,8,52],[0,46,4,52],[12,46,16,52],[8,46,12,52],
                   [4,42,8,46],[4,52,8,56])
    cube('root_rot_boot_'+side,side+'_leg',[x0,-.5,-2],[x1,6.5,2],faces)

# 六簇根须若独立运动需要13个display，超过12：全部并回身体/手臂，不制作摆动。
for name,xc,z,rx in [('root_front_right',4,-2.6,18),('root_front_left',-4,-2.6,18),
                     ('root_back_right',4,2.6,-18),('root_back_left',-4,2.6,-18)]:
    group(name,'body',[xc,13,z],[rx,0,0])
    for i,(dx,height) in enumerate([(-.55,7),(.55,5.5)]):
        # 精确使用袍子侧面的绿色根须列；变亮副本仅补偿原图材质亮部。
        column=[38,45][i]
        uv=[column,20,column+1,24]
        faces={f:spec(uv,basis='袍子根须列；细柱长度、厚度和18度外张为候选',derived=True)
               for f in ('north','east','south','west')}
        faces.update({f:spec([column,23,column+1,24],derived=True) for f in ('up','down')})
        cube(name+'_'+str(i),name,[xc+dx-.4,13-height,z-.4],[xc+dx+.4,13,z+.4],faces)

for side,xc,angle in [('right',5,12),('left',-5,-12)]:
    name='cuff_roots_'+side
    group(name,side+'_arm',[xc,15,0],[0,0,angle])
    for i,dx in enumerate([-.7,.7]):
        column=[38,45][i]
        faces={f:spec([column,20,column+1,24],basis='原根须像素复用到袖口；几何为候选',derived=True)
               for f in ('north','east','south','west','up','down')}
        cube(name+'_'+str(i),name,[xc+dx-.22,11.8+i*.5,.7],[xc+dx+.22,15,1.2],faces)

# 只做全模型+0.5px统一落地偏移，补偿靴底外扩；骨骼相对比例/关节间距不变。
for g in doc['groups']:g['origin'][1]+=.5
for e in doc['elements']:
    e['from'][1]+=.5;e['to'][1]+=.5;e['origin'][1]+=.5
buf=io.BytesIO();atlas.save(buf,format='PNG')
tex=copy.deepcopy(original['textures'][0])
tex.update(name='lucifer_atlas.png',path=str(HERE/'lucifer_atlas.png'),width=128,height=128,
           uv_width=128,uv_height=128,source='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode())
doc['textures']=[tex]
doc['lucifer_review']={'checkpoint':'A','status':'候选，待用户确认','animations_authored':False,
                       'unknown_uv_policy':'2026-11-07用户允许候选重建，逐面标明依据与推断',
                       'face_mapping':'FACE_UV_MAP.json'}
write('lucifer.bbmodel',doc)
parts=[['body',['body','root_front_right','root_front_left','root_back_right','root_back_left']],
       ['head',['head','eyes_glow','sprout_left','sprout_right']],
       ['right_arm',['right_arm','cuff_roots_right']],['left_arm',['left_arm','cuff_roots_left']],
       ['weapon',['right_arm']],['right_leg',['right_leg']],['left_leg',['left_leg']]]
mob=dm.Mob(key='lucifer_lord',label='路西法',generator='add_lucifer_model.py',bbmodel=str(HERE/'lucifer.bbmodel'),
           parts=parts,glow={'eyes_glow'},seat=2.0,tag='rpg.lu',score='rpg_lu',clips=[],held='weapon')
bones,_,_=dm.load_bbmodel(mob)
mins=np.array([1e9]*3);maxs=-mins.copy()
for n,b in bones.items():
    M=np.array(dm.bone_matrix(bones,n))
    for c in b['cubes']:
        for k in range(8):
            v=np.array([c['to'][j] if k>>j&1 else c['from'][j] for j in range(3)]+[1])
            p=(M@v)[:3];mins=np.minimum(mins,p);maxs=np.maximum(maxs,p)
model_scale=38.4/float(maxs[1]-mins[1])
write('static_config.json',{'key':'lucifer_lord','label':'路西法','tag':'rpg.lu','score':'rpg_lu',
      'seat':2.0,'held':'weapon','parts':parts,'glow':['eyes_glow'],'model_scale':model_scale,
      'rest_bounds_java_px':{'min':mins.tolist(),'max':maxs.tolist()},
      'rest_height_blocks':2.4,'scale_height_includes':'兜帽/嫩芽/靴，不包含手持矛',
      'stage':'checkpoint_A_candidate','animations':[]})
write('FACE_UV_MAP.json',{'atlas_size':[128,128],'body_offset':[0,0],'armor_offset':[64,0],
      'material_candidate_offset':[64,64],'lining_atlas_uv':[0,33,1,34],
      'material_formula':'E=min(shadow.G,shadow.B) if shadow.R<32 and E>=64 else0; RGB=clamp(diffuse+E*[0.75,1,0.60]); alpha保持',
      'faces':rows,'removed_source_elements':removed})
md=['# 路西法静态候选：逐面UV映射','','所有坐标均为原图像素边界，反向端点保留。最终工程为 lucifer.bbmodel。',
    '用户已允许候选重建；“候选”不代表原版网格已验证。BODY/HOOD/ARMOR分析报告给出证据强度。',
    '图集左上身体(0,0)，右上盔甲(64,0)，右下为绿色材质补偿候选(64,64)，内衬独占[0,33,1,34]。',
    '下表逐面对应JSON；六簇根须合并所在部件，不做独立运动。','','| 元素 | 骨骼 | 面 | 原图 | 原图UV | 图集UV | 依据 | 处理 |',
    '|---|---|---|---|---|---|---|---|']
for r in rows:md.append('| '+' | '.join(str(r[k]).replace('|','/') for k in ['element','bone','face','source_file','source_uv','atlas_uv','evidence','processing'])+' |')
(HERE/'FACE_UV_MAP.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps({'cubes':len(doc['elements']),'faces':len(rows),'bones':len(groups),'parts':len(parts),'scale':model_scale,'height':2.4},ensure_ascii=False))
