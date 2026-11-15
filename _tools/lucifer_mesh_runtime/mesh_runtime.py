"""Lucifer-only Generic Mesh/Cube/Armature adapter. Writes are confined to the explicit RP and DP output roots.

No editing of display_mob, existing weapon assets, other mobs or combat functions.
Source mesh triangles remain evidence; Java draws exact-plane fragment proxies.
"""
from pathlib import Path
from zipfile import ZipFile
from decimal import Decimal
import base64, hashlib, io, json, math, re, struct, sys, uuid, warnings
import numpy as np
from scipy.spatial.transform import Rotation
from PIL import Image
import shader_helpers as prototype
from shader_io import VanillaArchive, phase2_sources, guarded_write_shader, mark_block

HERE=Path(__file__).resolve().parent
REPO=next(p for p in HERE.parents if (p/'_tools/display_mob.py').is_file())
sys.path.insert(0,str(REPO/'_tools'))
import display_mob as dm

KEY='lucifer_lord'; TAG='rpg.lu'; SCORE='rpg_lu'; SEAT=2.0
ORDER=['idle','walk','attack','strong','cast','laugh','stun','rise']
SKILLS={'sk1_1':'attack','sk1_2':'attack','sk1_3':'cast','sk1_4':'strong','sk1_5':'strong','ult1_warn':'laugh','ult1':'strong'}
DECIMAL=re.compile(r'^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$')
JAR=None
BASE_BONE_NAMES={'J_Root','J_L_Hip','J_R_Leg','J_R_Foot','R_Leg','J_L_Leg','J_L_Foot','L_Leg','J_L_Spine','J_Shoulders','J_L_Arm','J_L_Hand','J_L_Weapon','L_Arm','J_R_Arm','J_R_Hand','J_R_Weapon','R_Arm','J_Neck','J_Head','Head','Body'}
# Blockbench's Cube BufferGeometry.setShape order. Each rectangular face uses
# local indices [0,2,1], [2,3,1]; these are outward-facing, including up/down.
CUBE_FACE_CORNERS={
    'east':(0,1,2,3),'west':(4,5,6,7),'up':(4,1,5,0),
    'down':(7,2,6,3),'south':(5,0,7,2),'north':(1,4,3,6),
}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def material_mode():
    import os
    return os.environ.get('LUCIFER_MATERIAL','plain').lower()
OUTPUT_ROOTS=()
def set_output_roots(rp,dp):
    global OUTPUT_ROOTS
    OUTPUT_ROOTS=(Path(rp).resolve(),Path(dp).resolve())
def write(p,s):
    p=Path(p).resolve()
    if not OUTPUT_ROOTS or not any(p.is_relative_to(root)for root in OUTPUT_ROOTS):raise ValueError('Write outside explicit RP/DP roots: '+str(p))
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def js(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def euler(v):return Rotation.from_euler('ZYX',np.asarray(v)[::-1],degrees=True).as_matrix()
def trs(p,r):
    m=np.eye(4);m[:3,:3]=r;m[:3,3]=p;return m
def scale(v):return np.diag([v,v,v,1.])
def trans(v):return trs(v,np.eye(3))
R180=np.diag([-1.,1.,-1.,1.])

def numeric(value):
    if isinstance(value,str) and not DECIMAL.fullmatch(value):raise ValueError('Molang/scientific-string key not allowed: '+repr(value))
    value=float(value)
    if not math.isfinite(value):raise ValueError('nonfinite key')
    return value

class NativeRig:
    def __init__(self,path):
        self.path=Path(path);self.raw=self.path.read_bytes();self.sha=hashlib.sha256(self.raw).hexdigest();self.doc=json.loads(self.raw)
        self.elements={e['uuid']:e for e in self.doc['elements']};self.parents={};self.order=[]
        def visit(node,parent):
            uid=node if isinstance(node,str) else node['uuid'];self.parents[uid]=parent
            if self.elements[uid]['type']=='armature_bone':self.order.append(uid)
            if not isinstance(node,str):
                for child in node.get('children',[]):visit(child,uid)
        for n in self.doc['outliner']:visit(n,None)
        self.bones={u:self.elements[u] for u in self.order};self.byname={b['name']:u for u,b in self.bones.items()}
        if len(self.byname)!=len(self.order) or not BASE_BONE_NAMES.issubset(self.byname):raise ValueError('original22bone names must remain unique and present')
        extra_bones={uid for uid in self.order if self.bones[uid]['name'] not in BASE_BONE_NAMES}
        if len(self.order)not in [22,28] or any(self.parents[uid]!=self.byname['J_L_Spine'] or not self.bones[uid]['name'].startswith('J_Wing_')for uid in extra_bones):raise ValueError('only optional six wing hinges parented to existing J_L_Spine are supported')
        self.bind=self.world();self.invbind={u:np.linalg.inv(m)for u,m in self.bind.items()}
        self.meshes=[e for e in self.doc['elements'] if e['type']=='mesh' and e.get('export',True)]
        self.cubes=[e for e in self.doc['elements'] if e['type']=='cube' and e.get('export',True)]
        wings=[m for m in self.meshes if m['name'].startswith('wings__')]
        if self.cubes:
            if wings or len(self.meshes)!=11 or len(self.order)!=28:raise ValueError('native Cube wings require original11meshes, six added hinges and no wing Mesh elements')
        elif (len(self.order),len(wings))not in [(22,0),(22,1),(28,7)] or len(self.meshes)!=11+len(wings):raise ValueError('expected original11meshes plus optional static1 or articulated7 wing meshes')
        self.wings=bool(wings or self.cubes);self.extra_wing_bones=extra_bones
        self.binding={}
        prefixes={m['uuid'][:6]:m['uuid']for m in self.meshes}
        if len(prefixes)!=len(self.meshes):raise ValueError('ambiguous native mesh weight prefix')
        weights={m['uuid']:{k:[]for k in m['vertices']}for m in self.meshes}
        for uid,b in self.bones.items():
            for token,w in b.get('vertex_weights',{}).items():
                prefix,vertex=token.split(':',1)
                if prefix in prefixes:weights[prefixes[prefix]][vertex].append((uid,float(w)))
        for m in self.meshes:
            if any(float(x)!=0 for x in m.get('origin',[0,0,0])+m.get('rotation',[0,0,0])):raise ValueError('nonidentity mesh-local transform needs explicit adaptation')
            assigned=set()
            for vertex,ws in weights[m['uuid']].items():
                if len(ws)!=1 or ws[0][1]!=1:raise ValueError('source vertex is not rigid weight1: '+m['name']+':'+vertex)
                assigned.add(ws[0][0])
            if len(assigned)!=1:raise ValueError('one mesh spans moving bones; cannot silently merge')
            self.binding[m['uuid']]=assigned.pop()
            if m['name'].startswith('wings__') and self.binding[m['uuid']]not in extra_bones|{self.byname['J_L_Spine']}:raise ValueError('wing mesh bound outside Spine/optional wing hinge family')
        if self.cubes:
            wings=self.cube_geometry()
            self.meshes=self.meshes+wings
        if extra_bones and (({self.binding[mesh['uuid']]for mesh in wings}-{self.byname['J_L_Spine']})!=extra_bones or sum(self.binding[mesh['uuid']]==self.byname['J_L_Spine']for mesh in wings)!=1):raise ValueError('articulated wings require one Spine-owned inner mesh and one outer mesh per added hinge')
        self.clips={}
        native_order=[a['name'].removeprefix('animation.')for a in self.doc['animations']]
        if native_order not in [ORDER[:8],ORDER[:8]+['slash']]:raise ValueError('unexpected clip order')
        ORDER[:]=native_order
        for a in self.doc['animations']:
            name=a['name'].removeprefix('animation.');tracks={}
            if (a['loop']=='loop')!=(name in ['idle','walk']):raise ValueError('clip loop mismatch')
            for uid,animator in a['animators'].items():
                if uid not in self.bones or animator.get('type')!='armature_bone':raise ValueError('unsupported animator')
                if animator.get('rotation_global')or animator.get('quaternion_interpolation'):raise ValueError('unsupported rotation sampling mode')
                for k in animator.get('keyframes',[]):
                    c=k['channel'];mode=k['interpolation']
                    if c not in ['rotation','position']or mode not in ['linear','catmullrom','step']:raise ValueError('unsupported channel/interpolation')
                    if len(k['data_points'])!=1:raise ValueError('split key is not supported without an explicit interpolation adapter')
                    dp=k['data_points'][0];tracks.setdefault((uid,c),[]).append((numeric(k['time']),[numeric(dp[axis])for axis in 'xyz'],mode))
            self.clips[name]={'length':numeric(a['length']),'loop':name in ['idle','walk'],'tracks':{k:sorted(v)for k,v in tracks.items()}}
        self.images=[]
        for texture in self.doc['textures']:
            data=base64.b64decode(texture['source'].split(',',1)[1]);im=Image.open(io.BytesIO(data)).convert('RGBA')
            eye_config=self.doc.get('lucifer_eye_emission',{})
            expected=eye_config.get('emissive_layer_size_pixels') if texture['uuid']==eye_config.get('emissive_layer_uuid') else [texture['uv_width'],texture['uv_height']]
            if list(im.size)!=expected:raise ValueError('texture pixel dimensions differ from source contract')
            self.images.append((data,im))
        # Keep original material/metadata pixel coordinates; expand the derived
        # atlas, never the source PNGs or mesh/proxy geometry. Square sprites also
        # avoid ambiguity with image-frame metadata in resource-pack loaders.
        self.metadata_end_y=64+8*math.ceil(sum(len([f for f in mesh['faces'].values()if f.get('texture')is not None])for mesh in self.meshes if not mesh['name'].startswith('weapon__'))/16)
        self.wing_rect=None
        if self.wings:
            if len(self.images)<6:raise ValueError('wing family requires texture index5')
            width,height=self.images[5][1].size
            if width<=0 or height<=0 or max(width,height)>2048:raise ValueError('wing source atlas must have positive dimensions at most2048')
            # Metadata occupies x[0,128), eye occupies x[256,512),y[0,128).
            self.wing_rect=(128 if width<=384 else 512,128,width,height)
        needed=max(512 if self.wings or self.doc.get('lucifer_eye_emission',{}).get('emissive_layer_uuid') else 256,self.metadata_end_y)
        if self.wing_rect:needed=max(needed,self.wing_rect[0]+self.wing_rect[2],self.wing_rect[1]+self.wing_rect[3])
        side=1<<(int(needed)-1).bit_length()
        if side>4096:raise ValueError('derived metadata/material atlas exceeds4096; explicit layout review required')
        self.atlas_size=(side,side)

    def cube_geometry(self):
        """Derive rigid render geometry without converting native Cube elements.

        Cube from/to/origin/rotation are local to their directly owning armature
        bone. Bake the cube transform into bind-world vertices, then reuse the
        existing world(t) @ inverse(bind) rigid animation path for that owner.
        The source document, original meshes and bone weights remain untouched.
        """
        spine=self.byname['J_L_Spine'];owners=[spine]+[u for u in self.order if u in self.extra_wing_bones]
        expected_names={f'J_Wing_pair{pair}_{side}'for pair in range(3)for side in ['L','R']}
        if {self.bones[u]['name']for u in self.extra_wing_bones}!=expected_names:raise ValueError('native Cube wings require the six named pair0/1/2 L/R hinges')
        groups={u:[]for u in owners}
        for cube in self.cubes:
            owner=self.parents.get(cube['uuid'])
            if not cube['name'].startswith('wings__') or owner not in groups:raise ValueError('exported Cube must be wings__ and directly owned by Spine or a wing hinge')
            groups[owner].append(cube)
        if any(not cubes for cubes in groups.values()):raise ValueError('native Cube wings require one nonempty render group for Spine and each of six hinges')
        result=[]
        for owner,cubes in groups.items():
            name='wings__inner'if owner==spine else 'wings__outer_'+self.bones[owner]['name'].removeprefix('J_Wing_')
            mesh={'name':name,'uuid':str(uuid.uuid5(uuid.NAMESPACE_URL,'lucifer-native-cube-owner:'+owner)),
                  'type':'mesh','origin':[0,0,0],'rotation':[0,0,0],'render_sides':'front','vertices':{},'faces':{},
                  'source_element_type':'cube','source_cube_uuids':[c['uuid']for c in cubes]}
            for cube in cubes:
                if cube.get('box_uv',self.doc.get('meta',{}).get('box_uv',False)) or cube.get('rescale',False):raise ValueError('native Cube adapter requires explicit per-face UV and no Java rescale')
                stretch=np.array([numeric(x)for x in cube.get('stretch',[1,1,1])],float)
                if numeric(cube.get('inflate',0))!=0 or stretch.shape!=(3,) or np.any(stretch!=1):raise ValueError('native Cube adapter requires uninflated, unstretched source cuboids')
                vectors=[np.array([numeric(x)for x in cube.get(field,[0,0,0])],float)for field in ['from','to','origin','rotation']]
                if any(v.shape!=(3,)for v in vectors):raise ValueError('native Cube vector must have three finite components')
                lower,upper,origin,rotation=vectors
                if np.any(upper<=lower):raise ValueError('native wing Cube must have positive extent on every axis')
                x0,y0,z0=lower;x1,y1,z1=upper
                corners=np.array([[x1,y1,z1],[x1,y1,z0],[x1,y0,z1],[x1,y0,z0],[x0,y1,z0],[x0,y1,z1],[x0,y0,z0],[x0,y0,z1]])
                local=(corners-origin)@euler(rotation).T+origin
                world=local@self.bind[owner][:3,:3].T+self.bind[owner][:3,3]
                keys=[cube['uuid']+':v'+str(i)for i in range(8)]
                mesh['vertices'].update({key:point.tolist()for key,point in zip(keys,world)})
                if set(cube.get('faces',{}))!=set(CUBE_FACE_CORNERS):raise ValueError('native wing Cube requires all six rectangular faces')
                for direction,indices in CUBE_FACE_CORNERS.items():
                    face=cube['faces'][direction]
                    texture=face.get('texture')
                    if isinstance(texture,str):texture=next((i for i,t in enumerate(self.doc['textures'])if t['uuid']==texture),texture)
                    if texture!=5 or isinstance(texture,bool) or not face.get('enabled',True):raise ValueError('native wing Cube faces must be enabled and assigned to texture5')
                    rect=[numeric(x)for x in face.get('uv',[])]
                    rotation_uv=numeric(face.get('rotation',0))
                    if len(rect)!=4 or rect[0]==rect[2] or rect[1]==rect[3] or rotation_uv not in [0,90,180,270]:raise ValueError('native Cube face requires nondegenerate rectangular UV and quarter-turn rotation')
                    u0,v0,u1,v1=rect;uv=[[u0,v0],[u1,v0],[u0,v1],[u1,v1]]
                    for _ in range(int(rotation_uv)//90):uv=[uv[2],uv[0],uv[3],uv[1]]
                    for triangle,order in enumerate([(0,2,1),(2,3,1)]):
                        vertex_keys=[keys[indices[i]]for i in order];fid=cube['uuid']+':'+direction+':'+str(triangle)
                        mesh['faces'][fid]={'vertices':vertex_keys,'uv':{key:uv[i]for key,i in zip(vertex_keys,order)},'texture':5}
            self.binding[mesh['uuid']]=owner;result.append(mesh)
        return result

    def world(self,clip=None,t=0):
        result={};a=self.clips[clip] if clip is not None else None
        for uid in self.order:
            b=self.bones[uid];p=np.array(b['origin'],float);r=np.array(b['rotation'],float)
            if a:
                for channel,target in [('position',p),('rotation',r)]:
                    keys=a['tracks'].get((uid,channel))
                    if keys:target+=dm.track_value(keys,t,a['loop'])
            local=trs(p,euler(r));parent=self.parents[uid]
            result[uid]=(result[parent] if parent in result else np.eye(4))@local
        return result

    def source_geometry(self):
        result=[]
        for m in self.meshes:
            if m['name'].startswith('weapon__'):continue
            faces=[]
            for fid,f in m['faces'].items():
                if f.get('texture')is None:continue
                if len(f['vertices'])!=3:raise ValueError('source body/armor is not triangular')
                faces.append({'source_face_id':fid,'vertices':f['vertices'],'uv':f['uv'],'texture':f['texture']})
            textures={f['texture']for f in faces}
            expected={5} if m['name'].startswith('wings__') else {0,1}
            if len(textures)!=1 or next(iter(textures))not in expected:raise ValueError('unexpected source material assignment')
            result.append({'name':m['name'].lower().replace('__','_'),'source_name':m['name'],'vertices':m['vertices'],'faces':faces,
                           'texture':textures.pop(),'bone':self.binding[m['uuid']],'mesh_uuid':m['uuid']}|({'render_sides':m.get('render_sides','front')}if m['name'].startswith('wings__')else {})|
                          ({'source_element_type':'cube','source_cube_uuids':m['source_cube_uuids']}if m.get('source_element_type')=='cube'else {}))
        return result

def weapon_calibration(rig,reference,resourcepack):
    d=json.loads(Path(reference).read_text(encoding='utf-8'));m=next(m for m in rig.meshes if m['name'].startswith('weapon__'))
    q=d['source_generated_vertices'];keys=list(m['vertices'])
    A=np.array([q[k]+[1]for k in keys]);B=np.array([m['vertices'][k]for k in keys]);fit=np.linalg.lstsq(A,B,rcond=None)[0]
    residual=float(np.abs(A@fit-B).max())
    if residual>1e-8:raise ValueError('held mesh is not the unchanged existing Java model under one affine adapter')
    for f in m['faces'].values():
        for k,uv in f['uv'].items():
            if uv!=d['source_generated_uv_pixels'][k]:raise ValueError('held weapon UV differs from existing item model')
    for p,expected in d['source_manifest']['files_sha256'].items():
        if 'resourcepack' in p:
            target=Path(resourcepack)/Path(p).relative_to('resourcepack')
            if not target.exists() or sha(target)!=expected:raise ValueError('Target weapon dependency missing/changed; run add_lucifer.py before mesh adapter: '+str(target))
    dispatch_path=Path(resourcepack)/'assets/minecraft/items/netherite_spear.json'
    dispatch=json.loads(dispatch_path.read_text(encoding='utf-8'))
    entries=[entry for entry in dispatch['model']['entries'] if entry.get('threshold')==1110014]
    if entries!=d['source_manifest']['netherite_spear_dispatch']['lucifer_entries']:raise ValueError('Target CMD1110014 dispatch differs from held native calibration')
    matrix=np.eye(4);matrix[:3]=fit.T
    engine=R180@np.array(d['binding']['item_transform_from_model_pixels'])
    return {'bone':rig.binding[m['uuid']],'native_bind_from_generated_pixels':matrix,'engine_from_generated_pixels':engine,
            'fit_error_px':residual,'source_path':str(reference),'source_sha256':sha(reference)}

def export_geometry(rig,rp):
    eye=rig.doc.get('lucifer_eye_emission',{});layer_uuid=eye.get('emissive_layer_uuid');layer_index=next((i for i,t in enumerate(rig.doc['textures'])if t['uuid']==layer_uuid),None) if layer_uuid else None
    atlas=np.zeros((rig.atlas_size[1],rig.atlas_size[0],4),np.uint8)
    if rig.wings:
        wing_image=rig.images[5][1]
        wx,wy,ww,wh=rig.wing_rect
        atlas[wy:wy+wh,wx:wx+ww]=np.array(wing_image)
    if layer_index is not None:
        layer=rig.images[layer_index][1]
        if list(layer.size)!=eye['emissive_layer_size_pixels'] or layer.size!=(256,128):raise ValueError('unsupported eye layer size')
        atlas[:128,256:512]=np.array(layer)
    for (_,im),x in zip(rig.images[:3],[0,64,128]):atlas[:im.height,x:x+im.width]=np.array(im)
    parts=[];records=[];maxerr=0.
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        for part in rig.source_geometry():
            v=np.array(list(part['vertices'].values()));K=(v.min(0)+v.max(0))/2-8;els=[];proxy_scale=1.0
            if part['texture']==5:
                # Exact inverse display compensation lets a wide single wing mesh
                # fit Java element coordinates without changing native geometry/UV.
                max_proxy_extent=24.0
                for face in part['faces']:
                    tri=np.array([part['vertices'][key]for key in face['vertices']],dtype=float);xx=tri[1]-tri[0];xx/=np.linalg.norm(xx);zz=np.cross(tri[1]-tri[0],tri[2]-tri[0]);zz/=np.linalg.norm(zz);basis_fit=np.array([xx,np.cross(zz,xx),zz]).T
                    qq=(tri-tri[0])@basis_fit;lo_fit=qq[:,:2].min(0);hi_fit=qq[:,:2].max(0);center_fit=tri[0]+basis_fit[:,:2]@((lo_fit+hi_fit)/2)-K-8;radius_fit=np.r_[(hi_fit-lo_fit)/2,0]
                    max_proxy_extent=max(max_proxy_extent,float(np.max(abs(center_fit-radius_fit))),float(np.max(abs(center_fit+radius_fit))))
                proxy_scale=max_proxy_extent/24*(1+1e-12) if max_proxy_extent>24 else 1.0
            for f in part['faces']:
                p=np.array([part['vertices'][k]for k in f['vertices']],dtype=float);uv=np.array([f['uv'][k]for k in f['vertices']],dtype=float);x=p[1]-p[0];x/=np.linalg.norm(x)
                z=np.cross(p[1]-p[0],p[2]-p[0]);z/=np.linalg.norm(z);y=np.cross(z,x);basis=np.array([x,y,z]).T
                q=(p-p[0])@basis;lo=q[:,:2].min(0);hi=q[:,:2].max(0);span=hi-lo;st=(q[:,:2]-lo)/span;bc=np.linalg.inv(np.vstack([st.T,np.ones(3)]))
                i=len(records);base=np.array([i%16*8,64+i//16*8]);material=part['texture'];render_kind=2 if material==5 else material
                if base[1]+7>=atlas.shape[0] or base[0]+7>=atlas.shape[1]:raise ValueError('triangle metadata exceeds atlas capacity')
                if rig.wing_rect:
                    wx,wy,ww,wh=rig.wing_rect
                    if base[0]<wx+ww and base[0]+8>wx and base[1]<wy+wh and base[1]+8>wy:raise ValueError('triangle metadata overlaps wing tile rectangle')
                for a in range(2):
                    for b in range(2):atlas[base[1]+b,base[0]+a]=[17,149,83,240+a+2*b]
                atlas[base[1],base[0]+2]=[211,57,193,71];atlas[base[1],base[0]+3]=[65,27,219,156]
                values=[*base,render_kind,*bc[:2].flatten(),*uv.flatten()]
                for j,value in enumerate(values):atlas[base[1]+2+j//8,base[0]+j%8]=list(struct.pack('<f',float(value)))
                center=p[0]+basis[:,:2]@((lo+hi)/2)-K
                if proxy_scale!=1.0:center=(center-8)/proxy_scale+8
                rot=Rotation.from_matrix(basis).as_euler('ZYX',degrees=True)[::-1]
                lower=center-np.array([span[0]/2,span[1]/2,0])/proxy_scale;upper=center+np.array([span[0]/2,span[1]/2,0])/proxy_scale
                if min(*lower,*upper)<-16 or max(*lower,*upper)>32:raise ValueError('Java proxy bounds exceed -16..32')
                # Java face UV uses16 units over the entire sprite, not pixel/16.
                uv_scale=np.array([16/atlas.shape[1],16/atlas.shape[0]])
                u0,v0=(base+.5)*uv_scale;u1,v1=(base+1.5)*uv_scale
                faces={'south':{'uv':[u0,v0,u1,v1],'texture':'#0','tintindex':0}}
                if part.get('render_sides',rig.doc['textures'][material].get('render_sides'))=='double':faces['north']={'uv':[u1,v0,u0,v1],'texture':'#0','tintindex':0}
                els.append({'from':lower.tolist(),'to':upper.tolist(),'rotation':{'origin':center.tolist(),**dict(zip('xyz',map(float,rot)))},'faces':faces,'shade':False})
                weights=np.array([[.2,.3,.5],[1/3]*3,[.1,.8,.1]]);sample=weights@st;rb=np.column_stack([sample,np.ones(3)])@np.float32(bc[:2]).T;rb=np.column_stack([rb,1-rb.sum(1)])
                error=float(np.abs(rb@uv-weights@uv).max());maxerr=max(maxerr,error)
                records.append({'id':i,'part':part['name'],'source_face_id':f['source_face_id'],'material_index':material,'render_kind':render_kind,'source_vertices':p.tolist(),'source_UV_px':uv.tolist(),'metadata_base_px':base.tolist(),
                                'metadata_float32_values':np.float32(values).astype(float).tolist(),'barycentric_from_proxy_st':bc.tolist(),'plane_basis':basis.tolist(),'float32_uv_error_px':error})
            model={'textures':{'0':f'rpg:item/{KEY}/atlas','particle':f'rpg:item/{KEY}/atlas'},'elements':els}
            js(rp/f'assets/rpg/models/{KEY}/{part["name"]}.json',model)
            js(rp/f'assets/rpg/items/{KEY}/{part["name"]}.json',{'model':{'type':'minecraft:model','model':f'rpg:{KEY}/{part["name"]}','tints':[{'type':'minecraft:custom_model_data','index':0,'default':16777215}]}})
            parts.append({k:part[k]for k in ['name','source_name','bone','mesh_uuid']}|{'K':K.tolist(),'triangles':len(els),'quads':sum(len(e['faces'])for e in els)}|({'proxy_scale':proxy_scale}if part['texture']==5 else {})|
                         ({'source_element_type':'cube','source_cube_uuids':part['source_cube_uuids']}if part.get('source_element_type')=='cube'else {}))
    path=rp/f'assets/rpg/textures/item/{KEY}/atlas.png';path.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(atlas).save(path)
    return parts,records,{'metadata_last_y':max(r['metadata_base_px'][1]+7 for r in records),'atlas_size_pixels':rig.atlas_size,'metadata_y_limit':atlas.shape[0],'max_uv_float32_error_px':maxerr,'png_regions_rgba_equal':all(np.array_equal(np.array(im),atlas[:im.height,x:x+im.width])for (_,im),x in zip(rig.images[:3],[0,64,128])),
                         'eye_layer_rgba_equal':None if layer_index is None else bool(np.array_equal(np.array(rig.images[layer_index][1]),atlas[:128,256:512])),'eye_layer_source_png_sha256':None if layer_index is None else hashlib.sha256(rig.images[layer_index][0]).hexdigest(),'eye_layer_atlas_rect':None if layer_index is None else [256,0,256,128],'wing_rgba_equal':None if not rig.wings else bool(np.array_equal(np.array(rig.images[5][1]),atlas[rig.wing_rect[1]:rig.wing_rect[1]+rig.wing_rect[3],rig.wing_rect[0]:rig.wing_rect[0]+rig.wing_rect[2]])),'wing_source_png_sha256':None if not rig.wings else hashlib.sha256(rig.images[5][0]).hexdigest(),'wing_atlas_rect':rig.wing_rect,'source_png_sha256':[hashlib.sha256(b).hexdigest()for b,_ in rig.images[:3]]}

def export_shaders(rig,rp,evidence):
    material=rig.doc['dungeons_material_source'];p=material['parameters'];tint=material.get('palette_tint_linear',[1,1,1])
    common=prototype.FRAGMENT_HELPER.split('vec4 luFragment()')[0]
    sample='''vec2 luSourceUV;
vec4 luSample(out ivec2 uv) {
    vec3 p=vec3(luPlane,1.0);
    vec3 b=vec3(dot(luBary0,p),dot(luBary1,p),0); b.z=1.0-b.x-b.y;
    if(any(lessThan(b,vec3(0)))) discard;
    luSourceUV=b.x*luUV0+b.y*luUV1+b.z*luUV2;
    uv=ivec2(floor(luSourceUV));
    ivec2 limit=luMode==3?WING_LIMIT:(luMode==1?ivec2(63,31):ivec2(63));
    ivec2 offset=luMode==3?WING_OFFSET:(luMode==1?ivec2(0):ivec2(64,0));
    uv=clamp(uv,ivec2(0),limit);
    vec4 a=texelFetch(Sampler0,luAtlasOrigin+offset+uv,0);
    if(a.a < (luMode==2?CLIP:0.1)) discard;
    return a;
}
'''.replace('CLIP',repr(float(p['OpacityMaskClipValue'])))
    wing_rect=rig.wing_rect or (0,320,192,64)
    sample=sample.replace('WING_LIMIT',f'ivec2({wing_rect[2]-1},{wing_rect[3]-1})').replace('WING_OFFSET',f'ivec2({wing_rect[0]},{wing_rect[1]})')
    core=common+sample+'''in vec4 luTint; in vec4 luLight;
vec4 luFragment() {
    ivec2 uv; vec4 a=luSample(uv);
    vec3 n=normalize(cross(dFdx(luWorldPosition),dFdy(luWorldPosition)));
    n *= gl_FrontFacing?1.0:-1.0;
    vec4 light=minecraft_mix_light(Light0_Direction,Light1_Direction,n,luTint)*luLight;
    vec4 color=a*light*ColorModulator;
    if(luMode==2) {
        vec3 albedo=luLinear(luRemap(a.rgb))*TINT;
        vec3 aux=luLinear(texelFetch(Sampler0,luAtlasOrigin+ivec2(128,0)+uv,0).rgb);
        vec3 E=max((aux.b*EMISSIVE*POWER+albedo*NATURAL)*DEATH,vec3(0));
        color.rgb=luSRGB(albedo*light.rgb*ColorModulator.rgb+E);
    }
    return apply_fog(color,sphericalVertexDistance,cylindricalVertexDistance,FogEnvironmentalStart,FogEnvironmentalEnd,FogRenderDistanceStart,FogRenderDistanceEnd,FogColor);
}
'''
    remap='vec3 luRemap(vec3 s) { ivec3 c=ivec3(floor(s*255.0+0.5));\n'
    for entry in material.get('palette_remap_srgb8',[]):
        source=','.join(map(str,entry['from']));target=','.join(str(float(x)/255) for x in entry['to'])
        remap+=f'if(all(equal(c,ivec3({source})))) return vec3({target});\n'
    remap+='return s; }\n'
    core=remap+core
    eye=rig.doc.get('lucifer_eye_emission')
    if eye:
        if eye.get('schema')!='lucifer-eye-emission-v1' or eye.get('texture_size_pixels')!=[64,32]:raise ValueError('unsupported eye emission schema')
        mask=' || '.join('all(equal(uv,ivec2('+','.join(map(str,pixel))+')))' for pixel in eye['texels']) or 'false'
        E='vec3('+','.join(map(str,eye['emission_linear']))+')'
        eye_output=('vec3('+','.join(str(float(c)/255)for c in eye['preview_output_srgb8'])+')') if 'preview_output_srgb8' in eye else 'luSRGB('+E+')'
        if eye.get('emissive_layer_uuid'):
            strength=float(eye.get('halo_strength',.18))
            halo=f'    if(luMode==1) {{ vec2 eyePixel=clamp(luSourceUV*4.0,vec2(0.5),vec2(255.5,127.5)); vec4 layer=textureLod(Sampler0,(vec2(luAtlasOrigin)+vec2(256,0)+eyePixel)/vec2(textureSize(Sampler0,0)),0.0); color.rgb=1.0-(1.0-color.rgb)*(1.0-layer.rgb*layer.a*{strength}); }}\n'
            core=core.replace('    return apply_fog(color,',halo+'    return apply_fog(color,')
        # Core remains pure static purple, halo uses the actual independent RGBA PNG.
        core=core.replace('    return apply_fog(color,',f'    if(luMode==1 && ({mask})) {{ color.rgb={eye_output}; }}\n    return apply_fog(color,')
    for token,value in {'TINT' :'vec3('+','.join(map(str,tint))+')','EMISSIVE':'vec3('+','.join(str(float(x))for x in p['Emissive'])+')','POWER':str(float(p['EmissivePower'])),'NATURAL':str(float(p['NaturalEmissive'])),'DEATH':str(float(p['DeathEmissive']))}.items():core=core.replace(token,value)
    fallback=[]
    with VanillaArchive(HERE/"vanilla_1_21_11") as jar:
        def preprocess(s):
            s=re.sub(r'^#version[^\n]*\n','',s,flags=re.M)
            return re.sub(r'#moj_import <minecraft:([^>]+)>',lambda m:preprocess(jar.read('assets/minecraft/shaders/include/'+m[1]).decode()),s)
        for kind in ['rendertype_item_entity_translucent_cull','rendertype_outline']:
            base='assets/minecraft/shaders/core/'+kind;v0=jar.read(base+'.vsh').decode();f0=jar.read(base+'.fsh').decode()
            p2_hash=None
            if 'item_' in kind:
                from dungeons_conversion import materials as p2material
                p2_hash=sha(Path(p2material.__file__))
                p2sources=phase2_sources(REPO,p2material,jar)
                v0=p2sources['vsh'];f0=p2sources['fsh']
            vh=prototype.VERTEX_HELPER;start='    luDecode();\n'
            if 'item_'in kind:
                vh+='out vec4 luTint; out vec4 luLight;\n';start+='    luTint=Color; luLight=texelFetch(Sampler2,UV2/16,0);\n'
                fh='#moj_import <minecraft:light.glsl>\n'+core;branch='    if(luMode!=0) { fragColor=luFragment(); return; }\n'
            else:
                fh=common+sample;branch='    if(luMode!=0) { ivec2 uv; vec4 source=luSample(uv); fragColor=vec4(ColorModulator.rgb*vertexColor.rgb,ColorModulator.a); return; }\n'
            vh=mark_block('DECL',vh);start=mark_block('MAIN',start)
            fh=mark_block('DECL',fh);branch=mark_block('MAIN',branch)
            vs=v0.replace('void main() {',vh+'\nvoid main() {\n'+start,1)
            fs=f0.replace('void main() {',fh+'\nvoid main() {\n'+branch,1)
            for ext,text in [('vsh',vs),('fsh',fs)]:
                path=rp/(base+'.'+ext)
                guarded_write_shader(path,text,jar.read(base+'.'+ext).decode(), {'vsh':v0,'fsh':f0}[ext])
                if evidence is not None:write(evidence/f'{kind}.{ext}','#version 330\n'+preprocess(text))
            fallback.append({'pipeline':kind,'phase2_material_module_sha256':p2_hash,'prior_vertex_body_retained':vs.replace(vh+'\nvoid main() {\n'+start,'void main() {',1)==v0,
                             'prior_fragment_body_retained':fs.replace(fh+'\nvoid main() {\n'+branch,'void main() {',1)==f0})
    return {'parameters':p,'palette_tint_linear':tint,'wing_material':None if not rig.wings else {'source_texture_index':5,'render_kind':2,'shader_mode':3,'atlas_rect':rig.wing_rect,'alpha_clip':0.1,'robe_palette_remap_applied':False,'emission_applied':False},'fallback':fallback,'full_source_specular_scene_lighting':False,
            'normal_policy':'flat native mesh geometric normal from screen derivatives; no claim of original Unreal smooth normals',
            'hdr_policy':'float static E preserved until target framebuffer; actual Minecraft HDR clipping/tone mapping not tested',
            'eye':rig.doc.get('lucifer_eye_emission'),'palette_remap_srgb8':material.get('palette_remap_srgb8',[]),'eye_output_policy':'Exact preview_output_srgb8 unlit static color, native alpha, then target vanilla fog; not original Unreal HDR.','outline_policy':'same barycentric and material alpha clipping as main shader; vanilla outline color path preserved'}

def float_snbt(v):
    f=np.float32(v)
    if not np.isfinite(f):raise ValueError('not finite float32')
    s=format(Decimal(str(f)),'f')
    if s in ['-0.0','-0']:s='0'
    assert np.float32(float(s))==f
    return s+'f'
def vector(v):return '['+','.join(float_snbt(x)for x in v)+']'
def components(matrix,previous=None):
    # A rigid native bone multiplies a constant affine mesh adapter. Preserve
    # its right singular frame instead of re-SVDing nearly degenerate scales.
    if previous is not None and len(previous)==4 and min(abs(x)for x in previous[2])>1e-10:
        right=Rotation.from_quat(previous[3]).as_matrix()
        left=matrix[:3,:3]@right.T@np.diag(1/np.array(previous[2]))
        if np.linalg.det(left)>0 and np.max(abs(left.T@left-np.eye(3)))<1e-7:
            q=Rotation.from_matrix(left).as_quat()
            if np.dot(q,previous[1])<0:q=-q
            return matrix[:3,3].tolist(),q.tolist(),previous[2],previous[3]
    c=dm.affine_components(matrix.tolist(),previous)
    if len(c)==2:
        uniform=float(np.linalg.norm(matrix[:3,:3])/math.sqrt(3));c=(*c,[uniform]*3,[0,0,0,1])
    return c
def snbt(c):return '{translation:'+vector(c[0])+',left_rotation:'+vector(c[1])+',scale:'+vector(c[2])+',right_rotation:'+vector(c[3])+'}'

def bake(rig,parts,weapon,model_scale):
    G=trans([0,-SEAT,0])@R180@scale(model_scale/16);output={};references={}
    for name in ORDER:
        a=rig.clips[name];ticks=round(a['length']*20);times=list(range(ticks if a['loop'] else ticks+1));frames=[];previous={};mats=[]
        for tick in times:
            world=rig.world(name,tick/20);frame={};matframe=[]
            for part in parts:
                D=world[part['bone']]@rig.invbind[part['bone']]
                F=scale(1/16)@R180@scale(1/part.get('proxy_scale',1.0))@trans(-np.array(part['K'])-8)
                M=G@D@np.linalg.inv(F);c=components(M,previous.get(part['name']));frame[part['name']]=c;previous[part['name']]=c;matframe.append(M)
            D=world[weapon['bone']]@rig.invbind[weapon['bone']]
            M=G@D@weapon['native_bind_from_generated_pixels']@np.linalg.inv(weapon['engine_from_generated_pixels'])
            c=components(M,previous.get('weapon'));frame['weapon']=c;previous['weapon']=c;matframe.append(M)
            frames.append((tick,frame));mats.append(matframe)
        output[name]={'ticks':ticks,'step':1,'loop':a['loop'],'frames':frames};references[name]=np.array(mats)
    return output,references

def export_runtime(rig,rp,dp,parts,weapon,model_scale):
    baked,refs=bake(rig,parts,weapon,model_scale)
    names=[p['name']for p in parts]+['weapon'];base=dp/f'data/rpg/function/{KEY}'
    for ci,name in enumerate(ORDER):
        clip=baked[name];leaves=[]
        for tick,frame in clip['frames']:
            lines=[f'# Lucifer native Generic frame {tick}; derived from {rig.sha}']
            duration=0 if name=='laugh' else 1
            for part in names:lines.append(f'execute on passengers if entity @s[tag={TAG}.p.{part}] run data merge entity @s {{start_interpolation:0,interpolation_duration:{duration},transformation:{snbt(frame[part])}}}')
            write(base/f'anim/{name}/f{tick}.mcfunction','\n'.join(lines)+'\n');leaves.append((tick+1,f'rpg:{KEY}/anim/{name}/f{tick}'))
        proxy=type('Writer',(),{'t_score':SCORE+'_t'})();dm.dispatch_tree(proxy,str(base/f'anim/{name}/at'),f'rpg:{KEY}/anim/{name}/at',leaves)
        end=(f'execute if score @s {SCORE}_t matches {clip["ticks"]}.. run scoreboard players set @s {SCORE}_t 0'if clip['loop']else f'execute if score @s {SCORE}_t matches {clip["ticks"]+1}.. run return run function rpg:{KEY}/anim/enter/idle')
        write(base/f'anim/{name}/tick.mcfunction',end+f'\nscoreboard players add @s {SCORE}_t 1\nfunction rpg:{KEY}/anim/{name}/at\n')
        write(base/f'anim/enter/{name}.mcfunction',f'scoreboard players set @s {SCORE}_anim {ci}\nscoreboard players set @s {SCORE}_t 0\nreturn run function rpg:{KEY}/anim/{name}/tick\n')
        write(base/f'debug/anim/{name}.mcfunction',f'execute as @e[tag={TAG}.candidate] run function rpg:{KEY}/anim/enter/{name}\n')
    write(base/'anim/tick.mcfunction','\n'.join(f'execute if score @s {SCORE}_anim matches {i} run return run function rpg:{KEY}/anim/{name}/tick'for i,name in enumerate(ORDER))+'\n')
    write(base/'load.mcfunction',f'scoreboard objectives add {SCORE}_anim dummy\nscoreboard objectives add {SCORE}_t dummy\n')
    write(base/'tick.mcfunction',f'execute as @e[tag={TAG}.candidate] at @s run function rpg:{KEY}/follow\nexecute as @e[type=minecraft:item_display,tag={TAG}.candidate.part] unless predicate rpg:{KEY}/riding run kill @s\n')
    write(base/'follow.mcfunction',f'execute on passengers run rotate @s ~ 0\nfunction rpg:{KEY}/anim/tick\n')
    js(dp/f'data/rpg/predicate/{KEY}/riding.json',{'condition':'minecraft:entity_properties','entity':'this','predicate':{'vehicle':{}}})
    merge_tag(dp,'load',f'rpg:{KEY}/load');merge_tag(dp,'tick',f'rpg:{KEY}/tick')
    first=baked['idle']['frames'][0][1];passengers=[]
    for name in names:
        item='{id:"minecraft:netherite_spear",count:1,components:{"minecraft:custom_model_data":{floats:[1110014.0f]}}}'if name=='weapon'else'{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:'+KEY+'/'+name+'"}}'
        context='thirdperson_righthand'if name=='weapon'else'none'
        passengers.append('{id:"minecraft:item_display",Tags:["'+TAG+'.part","'+TAG+'.candidate.part","'+TAG+'.p.'+name+'"],item:'+item+',item_display:"'+context+'",teleport_duration:2,interpolation_duration:1,view_range:1.5f,transformation:'+snbt(first[name])+'}')
    # Isolated debug carrier only; no taint/lord1 or other combat function is touched.
    write(base/'debug/summon.mcfunction','summon minecraft:vindicator ~ ~ ~ {Tags:["'+TAG+'","'+TAG+'.candidate"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,active_effects:[{id:"minecraft:invisibility",amplifier:0b,duration:-1,show_particles:0b}],Passengers:['+','.join(passengers)+']}\n'+f'execute as @e[tag={TAG}.candidate,distance=..2,sort=nearest,limit=1] run function rpg:{KEY}/anim/enter/idle\n')
    write(base/'debug/cleanup.mcfunction',f'execute as @e[tag={TAG}.candidate] on passengers run kill @s\nkill @e[tag={TAG}.candidate]\nkill @e[tag={TAG}.candidate.part]\n')
    write(base/'debug/outline.mcfunction',f'execute as @e[tag={TAG}.candidate] on passengers run data merge entity @s {{Glowing:1b}}\n')
    for hook,clip in SKILLS.items():write(base/f'hooks/{hook}.mcfunction',f'# Candidate callable hook only; no taint function edited.\nfunction rpg:{KEY}/anim/enter/{clip}\n')
    return baked,refs

def merge_tag(dp,tag,value):
    path=dp/f'data/minecraft/tags/function/{tag}.json'
    doc=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'values':[]}
    if value not in doc['values']:doc['values'].append(value)
    js(path,doc)

def build(model,rp,dp,weapon_source=None,model_scale=None,defer_shaders=False):
    rp=Path(rp).resolve();dp=Path(dp).resolve();set_output_roots(rp,dp)
    if rp==dp:raise ValueError('RP and DP roots must differ')
    rig=NativeRig(model);weapon_source=Path(weapon_source or HERE/'weapon_calibration.json')
    geo=rig.source_geometry();vertices=np.array([v for p in geo if p['texture']!=5 for v in p['vertices'].values()]);height=float(np.ptp(vertices[:,1]));model_scale=float(model_scale or 2.4*16/height)
    # LUCIFER_MATERIAL=shader keeps the metadata-atlas + core-shader material; the default 'plain'
    # bakes real texels per triangle so the look survives Iris / shader packs (plain_material.py)
    plain=material_mode()=='plain'
    if plain:
        import plain_material
        parts,records,geometry=plain_material.export_geometry_plain(rig,rp,KEY)
    else:parts,records,geometry=export_geometry(rig,rp)
    weapon=weapon_calibration(rig,weapon_source,rp)
    baked,refs=export_runtime(rig,rp,dp,parts,weapon,model_scale)
    import production
    dependencies=production.dependencies(sys.modules[__name__],rp)
    calibration=json.loads(weapon_source.read_text(encoding='utf-8'))
    for relative,expected in calibration['source_manifest']['files_sha256'].items():
        target=rp/Path(relative).relative_to('resourcepack')
        if sha(target)!=expected:raise ValueError('Target held-weapon dependency differs from native calibration: '+str(target))
    runtime=production.runtime(sys.modules[__name__],rig,rp,dp,baked,parts)
    from shader_io import prepare_deferred_shaders
    if plain:material={'plain':True}
    elif defer_shaders:
        prepare_deferred_shaders(rp,REPO,HERE/'vanilla_1_21_11');material={'deferred':True}
    else:material=export_shaders(rig,rp,None)
    if not (rp/'pack.mcmeta').exists():js(rp/'pack.mcmeta',{'pack':{'description':'Lucifer mesh runtime','min_format':[75,0],'max_format':75,'pack_format':75}})
    if not (dp/'pack.mcmeta').exists():js(dp/'pack.mcmeta',{'pack':{'description':'Lucifer mesh runtime','min_format':[94,1],'max_format':[94,1],'pack_format':94}})
    if sha(model)!=rig.sha:raise ValueError('native model changed during export; rerun')
    for entry in material.get('fallback',[]):
        h=entry.get('phase2_material_module_sha256')
        if h and sha(REPO/'_tools/dungeons_conversion/materials.py')!=h:raise ValueError('phase2 source changed during export')
    return {'model_sha256':rig.sha,'display_parts':len(parts)+1,'source_triangles':len(records),'proxy_quads':sum(p['quads']for p in parts),'clips':ORDER,'geometry':geometry,'material':material,'runtime':runtime,'dependencies':dependencies,'model_scale':model_scale}
