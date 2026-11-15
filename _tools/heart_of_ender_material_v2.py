"""M3 材质修订：独立 UV 渐隐与来源像素紫光；不改动画或公共管线。"""
from __future__ import annotations
import argparse,base64,copy,hashlib,json,math
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt
from heart_of_ender_blockbench import REF,BlockbenchMCP
from heart_of_ender_geo import uid,verify_export
from heart_of_ender_atlas import homography,FRONT_QUAD,SIDE_QUAD

OUT=REF/'m3_material_v2'
def read(p):return json.loads(p.read_text('utf8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

class Atlas:
    def __init__(self,base):
        self.image=Image.new('RGBA',(1024,1024));self.image.paste(base,(0,0))
        self.zones=[(520,0,1024,512),(0,520,1024,1024)];self.zone=0
        self.x,self.y=520,0;self.row=0;self.records=[]
    def put(self,name,patch,record):
        w,h=patch.size
        while True:
            x0,y0,x1,y1=self.zones[self.zone]
            if self.x+w+2>x1:self.x=x0;self.y+=self.row;self.row=0
            if self.y+h+2<=y1:break
            self.zone+=1
            if self.zone>=len(self.zones):raise ValueError('图集容量不足')
            self.x,self.y=self.zones[self.zone][:2];self.row=0
        x,y=self.x+1,self.y+1
        arr=np.array(patch);self.image.paste(Image.fromarray(np.pad(arr,((1,1),(1,1),(0,0)),mode='edge')),(x-1,y-1))
        self.records.append({'name':name,'atlas_rect':[x,y,x+w,y+h],**record})
        self.x+=w+2;self.row=max(self.row,h+2)
        return [x,y,x+w,y+h]

def line_alpha(src,start,end,count=1024,radius=3):
    a,b=np.array(start,float),np.array(end,float);v=b-a;n=np.array([-v[1],v[0]])/np.linalg.norm(v)
    points=a[None,:]+np.linspace(0,1,count)[:,None]*v
    samples=[]
    for offset in range(-radius,radius+1):
        xy=np.floor(points+offset*n+.5).astype(int)
        samples.append(src[xy[:,1],xy[:,0],3])
    raw=np.median(samples,axis=0)
    # A measured noisy line is not a useful repeated horizontal stripe texture.
    # Fit eleven local averages, retain endpoint opacities, and interpolate a monotone envelope.
    points=np.linspace(0,count-1,11);values=[]
    for pt in points:
        i=int(round(pt));values.append(float(np.mean(raw[max(0,i-40):min(count,i+41)])))
    values[0]=float(raw[0]);values[-1]=float(raw[-1])
    values=np.maximum.accumulate(values) if values[-1]>=values[0] else np.minimum.accumulate(values)
    return np.interp(np.arange(count),points,values)

def rectified(src,quad,pad=32):
    yy,xx=np.indices((160+pad*2,128+pad*2))
    uv=np.stack(((xx-pad+.5)/128,(yy-pad+.5)/160,np.ones_like(xx))).reshape(3,-1)
    m=homography(quad)@uv;x=np.floor(m[0]/m[2]+.5).astype(int);y=np.floor(m[1]/m[2]+.5).astype(int)
    valid=(x>=0)&(x<src.shape[1])&(y>=0)&(y<src.shape[0]);rgba=np.zeros((x.size,4),np.uint8)
    rgba[valid]=src[y[valid],x[valid]]
    return rgba.reshape(yy.shape+(4,)),x.reshape(yy.shape),y.reshape(yy.shape)

def wrap_eye_glow(src,old,regions,spec,atlas):
    """Reference-projected light field with shared edges, retaining only original eye cores."""
    size=144;yy,xx=np.indices((size,size));u=(xx+.5)/size;v=(yy+.5)/size
    sy_ratio=12/spec['total_closed_height'];fields={};provenance={}
    def project(quad,uu,vv):
        q=homography(quad)@np.stack((uu,vv,np.ones_like(uu))).reshape(3,-1)
        sx=np.rint(q[0]/q[2]).astype(int).reshape(uu.shape);sy=np.rint(q[1]/q[2]).astype(int).reshape(uu.shape)
        rgba=src[sy,sx].copy();rgb=rgba[:,:,:3].astype(float);value=rgb.max(2)
        # Keep the original eye/teeth core planes as the only bright glyphs.
        # Exclude stars from this layer, so it does not introduce a second star pattern.
        bright=(rgb[:,:,0]>=230)&(rgb[:,:,1]>=180)&(rgb[:,:,2]>=230)
        stars=(value>70)&(rgb[:,:,1]<rgb[:,:,0]*.17)
        invalid=bright|stars
        nearest=distance_transform_edt(invalid,return_distances=False,return_indices=True)
        clean=rgba[nearest[0],nearest[1]]
        return clean,sx[nearest[0],nearest[1]],sy[nearest[0],nearest[1]],invalid
    for face,quad,uu,vv in [
        ('north',FRONT_QUAD,u,v*sy_ratio),
        ('west',SIDE_QUAD,u,v*sy_ratio),
        ('up',[[348,262],[218,211],[346,103],[476,154]],u,v)]:
        rgba,sx,sy,removed=project(quad,uu,vv);fields[face]=rgba.astype(float)
        provenance[face]={'source_quad':quad,'removed_core_or_star_texels':int(removed.sum())}
        np.savez_compressed(OUT/('eye_wrap_'+face+'.npz'),source_x=sx,source_y=sy,excluded_core_or_star=removed)
    # Hidden east face is the measured west falloff, matched to the actual left front edge.
    # The front-facing edge is east-u1, west-u0, exactly as CubeFace.UVToLocal defines.
    east=fields['west'][:,::-1].copy()
    edge_delta=fields['north'][:,0,:3]-fields['west'][:,0,:3]
    depth=(1-u)*spec['depth'];east[:,:,:3]+=edge_delta[:,None,:]*np.exp(-depth[:,:,None]/3)
    fields['east']=np.clip(east,0,255)
    # The unseen back receives only the weak side tail, continuously joined to both side edges.
    back=fields['west'][:,-1,:][:,None,:]*(1-u[:,:,None])+fields['east'][:,0,:][:,None,:]*u[:,:,None]
    fields['south']=back
    faces={}
    for face in ('north','east','south','west','up','down'):
        if face=='down':faces[face]={'uv':[0,0,0,0],'texture':None};continue
        rgba=fields[face];rgb=rgba[:,:,:3];value=rgb.max(2)
        a=rgba[:,:,3]*value/255;stored_a=np.where(a>0,np.maximum(a,26),0)
        color=np.zeros(rgba.shape,np.uint8)
        color[:,:,:3]=np.rint(rgb*255/np.maximum(value[:,:,None],1)*(a/np.maximum(stored_a,1))[:,:,None]).clip(0,255).astype('uint8')
        color[:,:,3]=np.rint(stored_a).clip(0,255).astype('uint8')
        rect=atlas.put('eyes_wrapped_'+face,Image.fromarray(color),{
            'kind':'reference_projected_eye_glow','source':'MCD_Heart_of_Ender.png','face':face,
            'sampling':'nearest original source RGBA; nearest valid source pixel replaces white cores and stars, original core geometry retained',
            'visible_source':provenance.get(face),
            'hidden_side_assumption':None if face in provenance else 'east mirrors measured west with front-edge RGB matching fading over 3 model units; back interpolates weak side tails',
            'not_bloom':'surface emission approximation; no screen-space blur, no invented distance-ring eye shape'})
        faces[face]={'uv':rect,'texture':0}
    write(OUT/'eye_wrap_source.json',{'method':'actual source light field projected onto front/west/top, nearest source sampling; no dilation of the eye glyph',
        'visible_faces':provenance,'hidden_faces':['east','south'],
        'edge_matching':'front-west share identical source edge; hidden east joins the left front RGB and decays into the measured side field',
        'shape_preserved':'original eye cores remain untouched; no added thick white/pink distance contour',
        'limits':'original camera/UV fit remains approximate; hidden-side field and inverse-alpha composition are inferred'})
    return {'name':'eyes_source_wrapped_purple_halo','uuid':uid('M3_material_v2/front_eyes'),'type':'cube',
        'from':[-6.004,25.996,-10.804],'to':[6.004,38.004,1.61451],'origin':[0,0,0],
        'box_uv':False,'autouv':0,'export':True,'faces':faces}

def build():
    OUT.mkdir(exist_ok=True);baseline=OUT/'baseline.bbmodel'
    if not baseline.exists():baseline.write_bytes((REF/'heart_of_ender.bbmodel').read_bytes())
    base=read(baseline);doc=copy.deepcopy(base)
    old=Image.open(REF/'m3_material/atlas.png').convert('RGBA');atlas=Atlas(old)
    src=np.array(Image.open(REF/'MCD_Heart_of_Ender.png').convert('RGBA'))
    roots=line_alpha(src,[246,394],[120,433]) # local +Y root -> local -Y opaque limb
    body=line_alpha(src,[432,543],[455,715]) # body opaque top -> fading lower edge
    root_record={'source':'MCD_Heart_of_Ender.png','line_root_to_opaque':[[246,394],[120,433]],'perpendicular_median_radius_px':3,
        'mapping':'原 B 肢可见条带迁移到六肢近根半段；其余五根与三维衰减宽度为推断',
        'alpha_fit':'11 local-average controls, endpoint opacities retained, monotone envelope, linear interpolation'}
    body_record={'source':'MCD_Heart_of_Ender.png','line_top_to_bottom':[[432,543],[455,715]],'perpendicular_median_radius_px':3,
        'mapping':'源身体下缘 alpha 剖面迁移到局部 y=10..-1.5；侧背隐藏深度为推断',
        'alpha_fit':'11 local-average controls, endpoint opacities retained, monotone envelope, linear interpolation'}
    changes=[]
    for cube in doc['elements']:
        root=cube['name'].startswith('limb_') and '_proximal_cube_uvsegment_2' in cube['name']
        lower=cube['name'].startswith('shell_body_lower')
        if not(root or lower):continue
        for face,f in cube['faces'].items():
            if f.get('texture') is None or (root and face=='down'):continue
            uv=f['uv'];box=[math.floor(min(uv[0],uv[2])),math.floor(min(uv[1],uv[3])),math.ceil(max(uv[0],uv[2])),math.ceil(max(uv[1],uv[3]))]
            patch=np.array(old.crop(box));yy,xx=np.indices(patch.shape[:2]);v=(yy+box[1]+.5-uv[1])/(uv[3]-uv[1])
            y=cube['to'][1]-v*(cube['to'][1]-cube['from'][1])
            if face=='up':y=np.full_like(y,cube['to'][1])
            if face=='down':y=np.full_like(y,cube['from'][1])
            if root:
                t=(cube['to'][1]-y)/(cube['to'][1]-cube['from'][1]);profile=roots;rec=root_record
            else:
                fade_height=7 if '_rim' in cube['name'] else 11.5
                t=(10-y)/fade_height;profile=body
                rec={**body_record,'local_y_opaque_to_clear':[10,10-fade_height]}
            idx=np.rint(np.clip(t,0,1)*(len(profile)-1)).astype(int)
            patch[:,:,3]=np.rint(patch[:,:,3].astype(float)*profile[idx]/255).astype('uint8')
            rect=atlas.put(cube['name']+'/'+face,Image.fromarray(patch),{'kind':'independent_uv_alpha_profile','old_atlas_box':box,'old_uv':uv,**rec})
            f['uv']=[uv[0]-box[0]+rect[0],uv[1]-box[1]+rect[1],uv[2]-box[0]+rect[0],uv[3]-box[1]+rect[1]]
            changes.append({'element':cube['name'],'face':face,'old_uv':uv,'new_uv':f['uv']})
    regions={r['name']:r for r in read(REF/'m3_material/atlas_regions.json')['regions']}
    spec=read(REF/'m2_geometry/geometry_spec.json')['head_fit'];added=[]
    def append_glow(element,bone):
        doc['elements'].append(element);added.append(element['uuid'])
        gid=next(g['uuid'] for g in doc['groups'] if g['name']==bone)
        def attach(node):
            if isinstance(node,dict):
                if node['uuid']==gid:node['children'].append(element['uuid']);return
                for n in node.get('children',[]):attach(n)
        for node in doc['outliner']:attach(node)
    for name,bone,face,quad in [('front_eyes','shell_eyes_glow','north',FRONT_QUAD),('front_teeth','shell_teeth_front_glow','north',FRONT_QUAD),('side_teeth','shell_teeth_side_glow','west',SIDE_QUAD)]:
        if name=='front_eyes':
            append_glow(wrap_eye_glow(src,old,regions,spec,atlas),bone)
            continue
        rgba,sx,sy=rectified(src,quad);rgb=rgba[:,:,:3].astype(float);value=rgb.max(2)
        seed=np.zeros(rgba.shape[:2],bool);seed[32:192,32:160]=np.array(old.crop(regions[name]['atlas_rect']))[:,:,3]>0
        distance=distance_transform_edt(~seed)
        # Raw reference RGB is already a glow over black. Re-express it as a normal-alpha layer.
        # This inversion is an implementation assumption, not a recovered original emissive shader.
        allowed=(distance<=38)&(value>0)
        # Reject saturated star cores: retain the original star-window pattern below the layer.
        allowed &= ~((rgb[:,:,1]<rgb[:,:,0]*.1)&(value>60))
        alpha=np.where(allowed,rgba[:,:,3].astype(float)*value/255,0)
        # A broad low tail from the source meets zero outside the bounded face study.
        alpha*=np.clip((38-distance)/8,0,1)
        gy,gx=np.indices(alpha.shape);face_x=gx-32;face_y=gy-32
        # Keep the glow on the corresponding solid surface. A free floating screen halo is not bloom.
        upper=0 if name=='front_eyes' else 120
        lower=130 if name=='front_eyes' else 160
        alpha*=((face_x>=0)&(face_x<128)&(face_y>=upper)&(face_y<lower))
        edge=np.minimum.reduce([face_x+.5,127.5-face_x,face_y-upper+.5,lower-.5-face_y])
        alpha*=np.clip(edge/8,0,1)
        # Preserve the premultiplied source glow while keeping its faint surface tail above
        # Java's 0.1 discard. This is not used on the body/root transparency gradients.
        stored_alpha=np.where(alpha>0,np.maximum(alpha,26),0)
        color=np.zeros_like(rgba)
        color[:,:,:3]=np.rint(rgb*255/np.maximum(value[:,:,None],1)*
            (alpha/np.maximum(stored_alpha,1))[:,:,None]).clip(0,255).astype('uint8')
        color[:,:,3]=np.rint(stored_alpha).clip(0,255).astype('uint8')
        box=Image.fromarray(color).getbbox();l,t,r,b=box;patch=Image.fromarray(color).crop(box)
        rect=atlas.put(name+'_purple_halo',patch,{'kind':'source_projected_glow','source':'MCD_Heart_of_Ender.png',
            'quad':quad,'base_grid':[128,160],'padding':32,'crop':list(box),'nearest':'floor(coord+.5)',
            'formula':'a=source_alpha*source_value/255*bounded_tail; stored_a=max(a,26) for a>0; rgb_out=source_rgb/source_value*255*a/stored_a; premultiplied glow retained',
            'assumption':'从黑底发光反解普通alpha层；非官方独立mask材质，非屏幕bloom'})
        np.savez_compressed(OUT/(name+'_halo_sampling.npz'),source_x=sx[t:b,l:r],source_y=sy[t:b,l:r])
        yy0=38-spec['total_closed_height']*(b-32)/160;yy1=38-spec['total_closed_height']*(t-32)/160
        if face=='north':
            lo=[6-12*(r-32)/128,yy0,-10.804];hi=[6-12*(l-32)/128,yy1,-10.804]
        else:
            lo=[-6.004,yy0,-10.8+spec['depth']*(l-32)/128];hi=[-6.004,yy1,-10.8+spec['depth']*(r-32)/128]
        element={'name':name+'_purple_halo_surface','uuid':uid('M3_material_v2/'+name),'type':'cube','from':lo,'to':hi,
            'origin':[0,0,0],'box_uv':False,'autouv':0,'export':True,
            'faces':{f:{'uv':rect if f==face else [0,0,0,0],'texture':0 if f==face else None} for f in ('north','east','south','west','up','down')}}
        append_glow(element,bone)
    # Mouth interior is added below from a separately recorded open-mouth source sampling.
    mouth_spec=OUT/'mouth_interior_source.json'
    if mouth_spec.exists():
        m=read(mouth_spec);img=np.array(Image.open(REF/m['source']).convert('RGBA'))
        projected,_,_=rectified(img,m['quad'],0)
        floor_patch=Image.fromarray(projected).resize((128,128),Image.Resampling.NEAREST)
        ceiling_patch=floor_patch.copy()
        for element_name,face,patch,record in [
            ('shell_lower_jaw','up',floor_patch,{'kind':'source_projected_opening','quad':m['quad'],'resampling':'nearest projected source RGBA; original irregular white shape retained'}),
            ('shell_skull','down',ceiling_patch,{'kind':'whole_cavity_emission_requested_by_user','quad':m['quad'],
                'resampling':'same original luminous opening throughout upper and lower inner surface; hidden ceiling mapping inferred; no radial spot'})]:
            rect=atlas.put('mouth_interior_'+face,patch,{**m,**record})
            e=next(e for e in doc['elements'] if e['name']==element_name);old_uv=e['faces'][face]['uv'];e['faces'][face]['uv']=rect
            changes.append({'element':element_name,'face':face,'old_uv':old_uv,'new_uv':rect,'kind':'mouth_interior'})
    atlas_path=OUT/'atlas.png';atlas.image.save(atlas_path)
    doc['resolution']={'width':1024,'height':1024};tex=doc['textures'][0]
    tex.update({'name':'heart_of_ender_material_v2.png','width':1024,'height':1024,'uv_width':1024,'uv_height':1024,
        'source':'data:image/png;base64,'+base64.b64encode(atlas_path.read_bytes()).decode()})
    doc.setdefault('unhandled_root_fields',{})['material_status']={'version':'M3 material v2','alpha':'reference-derived root/lower-body fade',
        'glow':'reference-sampled purple normal-alpha overlays; no screen bloom','raw44':'original RGBA preserved at [432,88,476,132]; no independent mask shader',
        'runtime':'offline alpha approximation only; real game unverified'}
    write(OUT/'atlas_regions.json',{'atlas_size':[1024,1024],'baseline_atlas_unchanged_rect':[0,0,512,512],'regions':atlas.records})
    write(OUT/'material_changes.json',{'base_sha256':sha(baseline),'uv_changes':changes,'added_overlay_uuids':added,
        'original_core_glow_geometry_unchanged':True,'animations_unchanged':doc['animations']==base['animations'],
        'raw44_preserved':np.array_equal(np.array(atlas.image.crop((432,88,476,132))),np.array(old.crop((432,88,476,132)))),
        'root_alpha_profile':roots.tolist(),'body_alpha_profile':body.tolist(),'mouth_interior_included':mouth_spec.exists()})
    return doc

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--promote',action='store_true',help='核对主稿未被外部改动后，将此材质修订写入主bbmodel')
    parser.add_argument('--python-export',action='store_true',help='编辑器服务不可用时直接保存同格式JSON；报告明确未经过本轮原生导出')
    args=parser.parse_args()
    doc=build()
    if args.python_export:
        data={'content':json.dumps(doc,ensure_ascii=False,indent=2)+'\n'};got=json.loads(data['content'])
        audit={'export_mode':'Python structured JSON using the accepted Blockbench schema','native_export_verified':False,
            'reason':'Blockbench renderer became blank and its local MCP endpoint disconnected; no unsaved app state was killed'}
    else:
        client=BlockbenchMCP();client.tool('create_project',{'name':'heart_of_ender_material_v2','format':'bedrock'})
        client.evaluate('(function(){Codecs.project.parse('+json.dumps(doc).replace('/',r'\u002f')+');return true;})()')
        r=client.tool('export_model',{'codec_id':'project','options':{'raw':False},'max_content_length':2000000})
        data=json.loads(next(x['text'] for x in r['content'] if x['type']=='text'))
        if data['truncated']:raise ValueError('Blockbench export truncated')
        got=json.loads(data['content']);audit=verify_export(doc,got)
    assert got['animations']==doc['animations'],'必须保留原动画逐值不变'
    target=OUT/'heart_of_ender_material_v2.bbmodel';target.write_text(data['content'],'utf8')
    audit.update({'bbmodel_sha256':sha(target),'base_sha256':sha(OUT/'baseline.bbmodel'),'atlas_sha256':sha(OUT/'atlas.png')})
    write(OUT/'authoring_audit.json',audit)
    if args.promote:
        main_model=REF/'heart_of_ender.bbmodel';active=OUT/'active_material.json'
        allowed={sha(OUT/'baseline.bbmodel')}
        if active.exists():allowed.add(read(active)['bbmodel_sha256'])
        if sha(main_model) not in allowed:raise ValueError('主模型存在未登记修改；拒绝覆盖')
        main_model.write_bytes(target.read_bytes())
        write(active,{'bbmodel_sha256':sha(main_model),'variant':'M3 material v2','source_model':'m3_material_v2/heart_of_ender_material_v2.bbmodel',
            'baseline':'m3_material_v2/baseline.bbmodel','runtime_verified':False})
    print(json.dumps({'model':str(target),'sha256':sha(target),'cubes':len(got['elements']),'clips':len(got['animations'])}))

if __name__=='__main__':main()
