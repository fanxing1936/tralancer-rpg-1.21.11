"""Source-driven Jungle Abomination static cube conversion (checkpoint A).

Ordinary planar source faces retain their original atlas coordinates. Nonrectangular
faces use source-triangle rasterized cutout tiles; their explicit geometric and
sampling bounds are reported. This does not author animation keyframes.
"""
from __future__ import annotations
import argparse, base64, hashlib, io, itertools, json, math, uuid
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
from source_math import load_source, build_bb_skeleton, ue_to_java, transform_points, about, matrix_to_euler_zyx, jsonable

NS=uuid.UUID('89f3032b-1c88-47dd-8fac-6cb40622e34b')
FACES={
 'north':[(1,1,0),(1,0,0),(0,0,0),(0,1,0)],
 'south':[(0,1,1),(0,0,1),(1,0,1),(1,1,1)],
 'east': [(1,1,1),(1,0,1),(1,0,0),(1,1,0)],
 'west': [(0,1,0),(0,0,0),(0,0,1),(0,1,1)],
 'up':   [(0,1,0),(0,1,1),(1,1,1),(1,1,0)],
 'down': [(0,0,1),(0,0,0),(1,0,0),(1,0,1)],
}

def uid(value): return str(uuid.uuid5(NS,value))

def write_json(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(jsonable(data),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def indexed_components(triangles):
    parent=list(range(len(triangles)))
    def find(i):
        while parent[i]!=i: parent[i]=parent[parent[i]];i=parent[i]
        return i
    seen={}
    for i,tri in enumerate(triangles):
        for vertex in tri:
            if int(vertex) in seen: parent[find(i)]=find(seen[int(vertex)])
            else:seen[int(vertex)]=i
    groups=defaultdict(list)
    for i in range(len(triangles)):groups[find(i)].append(i)
    return sorted(groups.values(),key=lambda x:min(x))

def plane_basis(points,triangles):
    normal=np.cross(points[triangles[0,1]]-points[triangles[0,0]],points[triangles[0,2]]-points[triangles[0,0]])
    normal/=np.linalg.norm(normal)
    edges=defaultdict(int)
    for tri in triangles:
        for i in range(3):edges[tuple(sorted((int(tri[i]),int(tri[(i+1)%3]))))]+=1
    candidates=[edge for edge,n in edges.items() if n==1]
    if not candidates:candidates=list(edges)
    a,b=max(candidates,key=lambda ij:np.linalg.norm(points[ij[1]]-points[ij[0]]))
    x=points[b]-points[a];x/=np.linalg.norm(x)
    x-=np.dot(x,normal)*normal;x/=np.linalg.norm(x)
    y=np.cross(normal,x)
    return np.column_stack((x,y,normal))

def canonical_basis(basis,owner_rotation):
    candidates=[]
    for perm in itertools.permutations(range(3)):
        for sign in itertools.product((-1,1),repeat=3):
            b=basis[:,perm]*np.array(sign)
            if np.linalg.det(b)>0:
                relative=owner_rotation.T@b
                candidates.append((np.linalg.norm(relative-np.eye(3)),tuple(np.round(relative,8).ravel()),b))
    return min(candidates,key=lambda v:(v[0],v[1]))[2]

def face_corners(face,lo,hi):
    return np.array([[hi[i] if bit[i] else lo[i] for i in range(3)] for bit in FACES[face]])

def rectangular_uv(uv,tolerance=1e-5):
    # Java FaceBakery: corner i uses UV corner (i+rotation/90)%4.
    for rot in range(4):
        unrotated=np.roll(uv,rot,axis=0)
        u0,v0=unrotated[0];u1,v1=unrotated[2]
        expected=np.array([[u0,v0],[u0,v1],[u1,v1],[u1,v0]])
        if np.max(abs(unrotated-expected))<=tolerance:
            return {'uv':[float(u0),float(v0),float(u1),float(v1)],'rotation':rot*90,'texture':0}
    return None

def bake_tile(points,uv,triangles,axes,lo,hi,texture,model_scale):
    a,b=axes;xy=points[:,axes];dx,dy=hi[a]-lo[a],hi[b]-lo[b]
    th,tw=texture.shape[:2]
    density=np.zeros(2)
    for tri in triangles:
        p=xy[tri];coeff=np.linalg.solve(np.c_[p,np.ones(3)],uv[tri]*[tw,th])
        density=np.maximum(density,np.linalg.norm(coeff[:2],axis=1))
    width=max(8,int(math.ceil(dx*max(density[0]*4,model_scale*8))))
    height=max(8,int(math.ceil(dy*max(density[1]*4,model_scale*8))))
    if width>2048 or height>2048:raise ValueError(f'Cutout exceeds quality tile budget: {width}x{height}')
    x=lo[a]+(np.arange(width)+.5)*dx/width
    y=hi[b]-(np.arange(height)+.5)*dy/height
    xx,yy=np.meshgrid(x,y);sample=np.stack([xx,yy,np.ones_like(xx)],axis=-1)
    result=np.zeros((height,width,4),dtype=np.uint8)
    covered=np.zeros((height,width),dtype=bool)
    for tri in triangles:
        bary=sample@np.linalg.inv(np.c_[xy[tri],np.ones(3)])
        mask=np.all(bary>=-1e-10,axis=-1)
        sampled_uv=bary@uv[tri]
        sx=np.floor(sampled_uv[:,:,0]*tw).astype(int)%tw
        sy=np.floor(sampled_uv[:,:,1]*th).astype(int)%th
        result[mask]=texture[sy[mask],sx[mask]];covered|=mask
    return Image.fromarray(result),{'width':width,'height':height,
        'maximum_cutout_cell_diagonal_visual_pixels':float(math.hypot(dx/width,dy/height)*model_scale),
        'source_texture_sampling':'nearest original RGBA texel, no color interpolation',
        'source_uv_samples_per_texel_minimum':4,'covered_tile_pixels':int(covered.sum())}

def pack_tiles(tiles):
    for size in (1024,2048,4096,8192):
        x=y=2;row=0;placements=[];ok=True
        for tile in tiles:
            w,h=tile.size
            if w+4>size or h+4>size:ok=False;break
            if x+w+2>size:x=2;y+=row+4;row=0
            if y+h+2>size:ok=False;break
            placements.append((x,y));x+=w+4;row=max(row,h)
        if ok:
            atlas=Image.new('RGBA',(size,size))
            for tile,pos in zip(tiles,placements):atlas.paste(tile,pos)
            return atlas,placements
    raise ValueError('Atlas exceeds 8192 pixels')

def convert(mesh,meta,texture_path,out,unit_scale=.0192,model_scale=10.):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    source=load_source(mesh,meta)
    groups,outliner,state=build_bb_skeleton(meta,unit_scale)
    vertices=ue_to_java(source['vertices_ue_cm'],unit_scale)
    triangles=source['triangles'];uv=source['uv']
    owners=source['joint_source_indices'][np.arange(len(vertices)),np.argmax(source['weights'],axis=1)]
    texture_image=Image.open(texture_path).convert('RGBA');texture=np.array(texture_image)
    texture_size=np.array(texture_image.size)
    tiles=[texture_image];tile_records=[{'kind':'original_texture','source':Path(texture_path).name,'original_size':list(texture_image.size)}]
    auxiliary=np.array(Image.open(Path(texture_path).with_name('T_Jungle_Abomination_E_M6.png')).convert('RGBA'))
    support=auxiliary[:,:,:3]>0
    if not (np.array_equal(support[:,:,0],support[:,:,1]) and np.array_equal(support[:,:,0],support[:,:,2])):
        raise ValueError('Packed channels have different support; emission assignment needs new source evidence')
    support=support[:,:,0]&(texture[:,:,3]>0)
    support_rgba=np.dstack([support.astype(np.uint8)*255]*3+[texture[:,:,3]])
    mask_tiles=[Image.fromarray(support.astype(np.uint8)*255)]
    elements=[];parts=[];surfaces=[];conversion_records=[]
    for ids in indexed_components(triangles):
        vids=np.unique(triangles[ids].ravel());p=vertices[vids]
        centered=p-p.mean(0);_,singular,vh=np.linalg.svd(centered,full_matrices=False)
        planar_error=float(abs(centered@vh[-1]).max())
        influenced=set(int(i) for i in owners[vids])
        if len(influenced)>1 or planar_error>unit_scale*.003:
            for tid in ids:surfaces.append({'triangles':[tid],'mixed':len(set(owners[triangles[tid]]))>1,'split_reason':'mixed_skin' if len(influenced)>1 else 'nonplanar'})
        else:surfaces.append({'triangles':ids,'mixed':False,'split_reason':None})
    for surface_no,surface in enumerate(surfaces):
        ids=surface['triangles'];vids=np.unique(triangles[ids].ravel());mapping={int(v):i for i,v in enumerate(vids)}
        tri=np.array([[mapping[int(v)] for v in t] for t in triangles[ids]])
        p=vertices[vids];suv=uv[vids]
        if surface['mixed']:
            owner=state['bone_names'].index('Head') # only hierarchy anchor; true weights retained for affine runtime
        else:owner=int(owners[vids[0]])
        owner_name=state['bone_names'][owner];owner_world=state['bb_world'][owner]
        basis=canonical_basis(plane_basis(p,tri),owner_world[:3,:3])
        part=None
        if not surface['mixed']:
            for candidate in parts:
                if not candidate['deforming'] and candidate['owner_index']==owner and np.max(abs(candidate['basis']-basis))<2e-5:
                    proposed=transform_points(candidate['inverse_world'],p)
                    if min(np.ptp(proposed,axis=0))<unit_scale*.003:
                        part=candidate;break
        if part is None:
            part_no=len(parts);name=f'p2_{owner_name.lower()}_{part_no:03d}'
            relative=owner_world[:3,:3].T@basis
            rotation=matrix_to_euler_zyx(relative)
            pivot=np.array(groups[owner_name]['origin'])
            world=owner_world@about(pivot,relative)
            group={'name':name,'uuid':uid('bone:'+name),'origin':pivot.tolist(),'rotation':rotation.tolist(),
                   'export':True,'visibility':True,'isOpen':False,'children':[]}
            groups[name]=group;groups[owner_name]['children'].append(group)
            part={'name':name,'owner_index':owner,'owner_bone':owner_name,'basis':basis,
                  'world':world,'inverse_world':np.linalg.inv(world),'deforming':surface['mixed'],'elements':[],'triangles':[],'glow':False}
            parts.append(part)
        local=transform_points(part['inverse_world'],p)
        lo=local.min(0);hi=local.max(0);flat=int(np.argmin(hi-lo));axes=[i for i in range(3) if i!=flat]
        flat_at=float(local[:,flat].mean());projection_error=float(abs(local[:,flat]-flat_at).max())
        lo[flat]=hi[flat]=flat_at
        face_names=[('west','east'),('down','up'),('north','south')][flat]
        area=sum(np.linalg.norm(np.cross(local[t[1]]-local[t[0]],local[t[2]]-local[t[0]]))/2 for t in tri)
        bbox_area=float(np.prod((hi-lo)[axes]));fills=abs(area-bbox_area)<max(1e-9,bbox_area*1e-5)
        coeff=np.linalg.lstsq(np.c_[local[:,axes],np.ones(len(local))],suv,rcond=None)[0]
        uv_error=float(abs(np.c_[local[:,axes],np.ones(len(local))]@coeff-suv).max())
        face_data={}
        if fills and uv_error<2e-7:
            for face in face_names:
                corner_uv=np.c_[face_corners(face,lo,hi)[:,axes],np.ones(4)]@coeff*texture_size
                data=rectangular_uv(corner_uv,2e-4)
                if data is None:face_data={};break
                face_data[face]=data
        tile_index=0;bake=None
        if not face_data:
            tile,bake=bake_tile(local,suv,tri,axes,lo,hi,texture,model_scale)
            tile_index=len(tiles);tiles.append(tile)
            emission_tile,_=bake_tile(local,suv,tri,axes,lo,hi,support_rgba,model_scale)
            mask_tiles.append(emission_tile.getchannel('R'))
            tile_records.append({'kind':'source_triangle_cutout','source_triangle_indices':ids,
                                 'original_vertex_indices':vids.tolist(),'bake':bake})
            for face in face_names:
                fc=face_corners(face,lo,hi)
                tuv=np.c_[(fc[:,axes[0]]-lo[axes[0]])/(hi[axes[0]]-lo[axes[0]])*tile.width,
                           (hi[axes[1]]-fc[:,axes[1]])/(hi[axes[1]]-lo[axes[1]])*tile.height]
                face_data[face]=rectangular_uv(tuv)
                assert face_data[face] is not None
        element_id=uid('element:'+','.join(map(str,ids)))
        el={'name':'source_faces_'+str(ids[0]),'type':'cube','uuid':element_id,'from':lo.tolist(),'to':hi.tolist(),
            'origin':groups[part['name']]['origin'],'rotation':[0,0,0],'autouv':0,'faces':face_data,
            'rescale':False,'locked':False,'visibility':True,'export':True,'color':surface_no%8,
            '_source_triangles':ids,'_atlas_tile':tile_index}
        elements.append(el);groups[part['name']]['children'].append(element_id)
        part['elements'].append(element_id);part['triangles']+=ids
        conversion_records.append({'element':element_id,'part':part['name'],'source_triangles':ids,
            'source_vertex_indices':vids.tolist(),'vertex_source_bones':[state['bone_names'][int(i)] for i in owners[vids]],
            'original_uv':suv.tolist(),'rest_vertices_java_internal':p.tolist(),'split_reason':surface['split_reason'],
            'deforming':surface['mixed'],'zero_thickness_axis':'xyz'[flat],
            'projection_error_visual_pixels':projection_error*model_scale,'direct_original_atlas':tile_index==0,
            'bake':bake,'tile':tile_index})
    atlas,placements=pack_tiles(tiles)
    for el in elements:
        ox,oy=placements[el.pop('_atlas_tile')]
        for data in el['faces'].values():
            u0,v0,u1,v1=data['uv'];data['uv']=[u0+ox,v0+oy,u1+ox,v1+oy]
            if not data['rotation']:del data['rotation']
    atlas.save(out/'atlas.png')
    mask_atlas,mask_placements=pack_tiles(mask_tiles)
    assert mask_placements==placements and mask_atlas.size==atlas.size
    mask_atlas.getchannel('R').save(out/'atlas_emission_support.png')
    for i,record in enumerate(tile_records):record.update({'tile':i,'offset':list(placements[i]),'size':list(tiles[i].size)})
    image_data=(out/'atlas.png').read_bytes()
    serialized_groups=[{k:v for k,v in group.items() if k!='children'} for group in groups.values()]
    def outline(node):return {'uuid':node['uuid'],'children':[outline(c) if isinstance(c,dict) else c for c in node['children']]}
    doc={'meta':{'format_version':'5.0','model_format':'free','box_uv':False},'name':'lucifer_p2',
         'model_identifier':'lucifer_p2','visible_box':[0,0,0],'variable_placeholders':'',
         'resolution':{'width':atlas.width,'height':atlas.height},'elements':elements,'groups':serialized_groups,
         'outliner':[outline(node) for node in outliner],
         'textures':[{'path':'atlas.png','name':'atlas.png','uuid':uid('atlas'),'id':'0','width':atlas.width,'height':atlas.height,
                      'uv_width':atlas.width,'uv_height':atlas.height,'particle':True,'visible':True,'internal':True,
                      'source':'data:image/png;base64,'+base64.b64encode(image_data).decode()}],
         'animations':[],'display_dungeons':{'checkpoint':'A_static','source_mesh_sha256':source['mesh_sha256'],
                      'unit_scale_java_pixels_per_ue_cm':unit_scale,'model_scale':model_scale,
                      'deforming_source_triangles':[r for r in conversion_records if r['deforming']]}}
    write_json(out/'lucifer_p2.bbmodel',doc)
    part_rows=[{'name':p['name'],'bones':[p['name']],'source_owner':p['owner_bone'],'glow':p['glow'],
                'deforming':p['deforming'],'elements':len(p['elements']),'source_triangles':p['triangles']} for p in parts]
    report={'source_mesh_sha256':source['mesh_sha256'],'source_vertices':len(vertices),'source_triangles':len(triangles),
      'covered_triangles':sum(len(r['source_triangles']) for r in conversion_records),'all_triangles_covered_once':sorted(t for r in conversion_records for t in r['source_triangles'])==list(range(len(triangles))),
      'original_bones':len(source['bones']),'parts':len(parts),'zero_thickness_cubes':len(elements),'atlas_size':list(atlas.size),
      'original_texture_pixels_unchanged':bool(np.array_equal(np.array(atlas)[placements[0][1]:placements[0][1]+texture.shape[0],placements[0][0]:placements[0][0]+texture.shape[1]],texture)),
      'direct_original_atlas_surfaces':sum(r['direct_original_atlas'] for r in conversion_records),
      'baked_source_cutout_surfaces':sum(not r['direct_original_atlas'] for r in conversion_records),
      'max_geometric_projection_error_visual_pixels':max(r['projection_error_visual_pixels'] for r in conversion_records),
      'maximum_cutout_cell_diagonal_visual_pixels':max((r['bake']['maximum_cutout_cell_diagonal_visual_pixels'] for r in conversion_records if r['bake']),default=0),
      'source_skeleton_validation':state['validation'],'unit_scale':unit_scale,'model_scale':model_scale,
      'glow_status':'Packed material emissive connection not proven; no invented mask.',
      'animations_authored':False,'limitations':['Nonrectangular triangles use finite-resolution alpha cutout tiles; reported cell diagonal bounds edge quantization, not mathematically exact triangular clipping.',
      'Four mixed-skin eyelid triangles retain their weights and original vertices for a later affine animation extension; current checkpoint contains no keyframes.']}
    write_json(out/'parts.json',part_rows);write_json(out/'atlas_regions.json',tile_records)
    write_json(out/'conversion_map.json',conversion_records);write_json(out/'validation/static_conversion.json',report)
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_skeleton_validation','limitations')},ensure_ascii=False,indent=2))
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-dir',type=Path,required=True);p.add_argument('--out-dir',type=Path,required=True)
    p.add_argument('--unit-scale',type=float,default=.0192);p.add_argument('--model-scale',type=float,default=10.)
    args=p.parse_args()
    convert(args.source_dir/'source/SK_Abomination_02.source.glb',args.source_dir/'source/skeleton.meta.json',
            args.source_dir/'T_Jungle_Abomination_M6.png',args.out_dir,args.unit_scale,args.model_scale)

if __name__=='__main__':main()
