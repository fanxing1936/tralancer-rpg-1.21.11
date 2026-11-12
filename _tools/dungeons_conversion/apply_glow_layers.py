"""Partition static candidate faces into complementary non-glow/glow alpha layers.

This maps the user's _E glow instruction onto the supplied RGB support mask;
it does not infer cooked shader intensity, channel semantics, or pulse behavior.
"""
from __future__ import annotations
import argparse
import base64
from collections import Counter,defaultdict
import copy
import hashlib
import json
import math
from pathlib import Path
import shutil
import uuid

import numpy as np
from PIL import Image

NS=uuid.UUID('9287c346-af06-48c1-a411-77933ccbf57e')


def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def write(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def pixel_digest(array):return hashlib.sha256(np.ascontiguousarray(array).tobytes()).hexdigest()
def uid(name):return str(uuid.uuid5(NS,name))


def window(face,width,height):
    if face.get('texture')!=0:raise ValueError('Only atlas texture 0 is supported')
    uv=[float(round(v))if abs(v-round(v))<1e-4 else float(v)for v in face['uv']]
    x0,x1=math.floor(min(uv[0],uv[2])),math.ceil(max(uv[0],uv[2]))
    y0,y1=math.floor(min(uv[1],uv[3])),math.ceil(max(uv[1],uv[3]))
    if not(0<=x0<x1<=width and 0<=y0<y1<=height):raise ValueError(f'Invalid UV rectangle {face["uv"]}')
    return x0,y0,x1,y1


def shifted_face(face,offset):
    result=copy.deepcopy(face);u,v=offset
    result['uv']=[face['uv'][0]+u,face['uv'][1]+v,face['uv'][2]+u,face['uv'][3]+v]
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate',type=Path,default=Path(r'D:\agent\dungeons_extract\phase2_candidate_boxed'))
    parser.add_argument('--mask',type=Path,default=Path(r'D:\agent\dungeons_extract\phase2_candidate\atlas_emission_support.png'))
    parser.add_argument('--output',type=Path,default=Path(r'D:\agent\dungeons_extract\phase2_candidate_glow'))
    args=parser.parse_args()
    if args.output.resolve()==args.candidate.resolve():raise ValueError('Output must differ from input')
    model=read(args.candidate/'lucifer_p2.bbmodel');parts=read(args.candidate/'parts.json')
    mapping=read(args.candidate/'conversion_map.json');regions=read(args.candidate/'atlas_regions.json')
    original=np.asarray(Image.open(args.candidate/'atlas.png').convert('RGBA')).copy()
    mask=np.asarray(Image.open(args.mask).convert('L'))
    height,width=mask.shape
    if original.shape[:2]!=(height,width):raise ValueError('Mask/atlas dimensions differ')
    if set(np.unique(mask))-{0,255}:raise ValueError('Support mask must contain only 0 or 255')
    support=mask>0
    if np.any(support&(original[:,:,3]==0)):raise ValueError('Support contains non-visible source pixels')
    layers={'nonglow':original.copy(),'glow':original.copy()}
    layers['nonglow'][:,:,3]=np.where(support,0,original[:,:,3])
    layers['glow'][:,:,3]=np.where(support,original[:,:,3],0)
    offsets={'reference':(0,0),'nonglow':(width,0),'glow':(0,height)}
    packed=np.zeros((height*2,width*2,4),dtype=np.uint8)
    packed[:height,:width]=original;packed[:height,width:]=layers['nonglow'];packed[height:,:width]=layers['glow']
    overlap=int(np.count_nonzero((layers['nonglow'][:,:,3]>0)&(layers['glow'][:,:,3]>0)))
    alpha_error=int(np.abs(layers['nonglow'][:,:,3].astype(np.int16)+layers['glow'][:,:,3].astype(np.int16)-original[:,:,3]).max())
    recompose=np.where(support[:,:,None],layers['glow'],layers['nonglow'])
    if overlap or alpha_error or not np.array_equal(recompose,original):raise ValueError('Layer partition is not lossless')
    group_by_name={g['name']:g for g in model['groups']};input_groups=copy.deepcopy(model['groups'])
    map_by_id={m['element']:m for m in mapping}
    if len(map_by_id)!=len(mapping):raise ValueError('Duplicate conversion map element ids')
    element_splits={};glow_children=defaultdict(list);glow_names={};output_elements=[];output_mapping=[];source_map=[];transparent=[]
    face_count=Counter();element_count=Counter()
    region_count=max(r['tile']for r in regions)+1
    for element in model['elements']:
        old_id=element['uuid'];source=map_by_id[old_id];part=source['part']
        by_layer={'nonglow':{},'glow':{}};face_masks={}
        for name,face in element['faces'].items():
            x0,y0,x1,y1=window(face,width,height)
            counts={role:int(np.count_nonzero(layer[y0:y1,x0:x1,3]))for role,layer in layers.items()}
            face_masks[name]={'atlas_window':[x0,y0,x1,y1],'effective_alpha_pixels':counts}
            if not any(counts.values()):face_count['fully_transparent_removed']+=1
            for role,count in counts.items():
                if count:
                    by_layer[role][name]=shifted_face(face,offsets[role]);face_count[role]+=1
        produced=[]
        for role in ('nonglow','glow'):
            if not by_layer[role]:continue
            new=copy.deepcopy(element);new_id=old_id if role=='nonglow'else uid('glow_element:'+old_id)
            new.update(uuid=new_id,faces=by_layer[role],name=element['name']+'_'+role)
            new['_glow_source_element']=old_id;new['_glow_layer']=role
            output_elements.append(new);element_count[role]+=1
            if role=='glow':
                glow_name=part+'_glow';glow_names[part]=glow_name;glow_children[part].append(new_id)
            record=copy.deepcopy(source);record['element']=new_id
            record['pre_glow_element']=old_id;record['atlas_layer']=role;record['atlas_layer_offset']=list(offsets[role])
            record['geometry_owner_bone']=glow_names[part]if role=='glow'else part
            record['source_pixel_partition']='original_alpha & support'if role=='glow'else'original_alpha & !support'
            record['active_faces']=list(by_layer[role]);record['original_source_triangles']=source['source_triangles']
            if isinstance(source.get('tile'),int):record['tile']=source['tile']+(region_count if role=='nonglow'else region_count*2)
            if 'tiles'in source:record['tiles']=[t+(region_count if role=='nonglow'else region_count*2)for t in source['tiles']]
            record['source_face_records_note']='Nested source_face_records/face_provenance retain pre-glow UV and tile coordinates for traceability; actual emitted faces use atlas_layer_offset.'
            output_mapping.append(record);produced.append({'element':new_id,'layer':role,'faces':list(by_layer[role])})
        element_splits[old_id]=next((x['element']for x in produced if x['layer']=='nonglow'),None)
        source_map.append({'source_element':old_id,'part':part,'source_triangles':source['source_triangles'],
                           'layer_elements':produced,'face_support':face_masks})
        if not produced:transparent.append(copy.deepcopy(source))
    part_uuid={name:group_by_name[name]['uuid']for name in glow_names}
    part_by_uuid={v:k for k,v in part_uuid.items()}
    def update_outline(nodes):
        output=[]
        for node in nodes:
            if isinstance(node,str):
                replacement=element_splits.get(node,node)
                if replacement is not None:output.append(replacement)
            else:
                new=copy.deepcopy(node);new['children']=update_outline(node.get('children',[]))
                if node['uuid']in part_by_uuid:
                    part=part_by_uuid[node['uuid']];name=glow_names[part]
                    new['children'].append({'uuid':uid('glow_bone:'+name),'children':glow_children[part]})
                output.append(new)
        return output
    model['outliner']=update_outline(model['outliner'])
    for part,name in glow_names.items():
        parent=group_by_name[part]
        model['groups'].append({'name':name,'uuid':uid('glow_bone:'+name),'origin':copy.deepcopy(parent['origin']),
                                'rotation':[0,0,0],'export':True,'visibility':True,'isOpen':False})
    element_per_part=Counter(m['part']for m in output_mapping)
    for part in parts:
        name=part['name'];part['elements']=element_per_part[name]
        part['glow_bones']=[glow_names[name]]if name in glow_names else[]
        if name in glow_names:part['bones'].append(glow_names[name])
        # The parent part stays non-emissive; only the new child is listed in Mob.glow.
        part['glow']=False
    model['elements']=output_elements;model['resolution']={'width':width*2,'height':height*2}
    texture=model['textures'][0]
    texture.update(width=width*2,height=height*2,uv_width=width*2,uv_height=height*2,path='atlas.png',name='atlas.png')
    original_bones=[g for g in input_groups if g['name']not in {p['name']for p in parts}]
    if len(original_bones)!=40:raise ValueError(f'Expected 40 original bones, got {len(original_bones)}')
    if model['groups'][:len(input_groups)]!=input_groups:raise ValueError('Existing skeleton/group fields changed')
    original_triangles=set(t for m in mapping for t in m['source_triangles'])
    output_triangles=set(t for m in output_mapping+transparent for t in m['source_triangles'])
    if original_triangles!=output_triangles:raise ValueError('Lost source triangle provenance')
    all_outline=[]
    def collect(nodes):
        for node in nodes:
            if isinstance(node,str):all_outline.append(node)
            else:collect(node.get('children',[]))
    collect(model['outliner'])
    if Counter(all_outline)!=Counter(e['uuid']for e in output_elements):raise ValueError('Outliner membership mismatch')
    source_elements={e['uuid']:e for e in read(args.candidate/'lucifer_p2.bbmodel')['elements']}
    max_uv_translation_residual=0.0
    for element in output_elements:
        source_element=source_elements[element['_glow_source_element']]
        for key in ('from','to','origin','rotation'):
            if element[key]!=source_element[key]:raise ValueError(f'Geometry changed: {key}')
        role=element['_glow_layer'];du,dv=offsets[role]
        for name,face in element['faces'].items():
            old=source_element['faces'][name]
            if {k:v for k,v in face.items()if k!='uv'}!={k:v for k,v in old.items()if k!='uv'}:
                raise ValueError('Non-UV face attributes changed')
            residual=max(abs(a-b-d)for a,b,d in zip(face['uv'],old['uv'],(du,dv,du,dv)))
            max_uv_translation_residual=max(max_uv_translation_residual,residual)
    if max_uv_translation_residual>1e-9:raise ValueError('UV mapping changed beyond floating translation')
    # Blockbench's free-format parser iterates all six constructed CubeFaces and
    # reads template.faces[face].texture. Disabled faces must be explicit nulls.
    for element in output_elements:
        for face_name in ('north','east','south','west','up','down'):
            element['faces'].setdefault(face_name,{'uv':[0,0,0,0],'texture':None})
    args.output.mkdir(parents=True,exist_ok=True)
    shutil.copy2(args.candidate/'atlas.png',args.output/'atlas_reference.png')
    shutil.copy2(args.mask,args.output/'atlas_emission_support.png')
    for role,layer in layers.items():Image.fromarray(layer,'RGBA').save(args.output/f'atlas_{role}.png')
    Image.fromarray(packed,'RGBA').save(args.output/'atlas.png')
    texture['source']='data:image/png;base64,'+base64.b64encode((args.output/'atlas.png').read_bytes()).decode('ascii')
    new_regions=[]
    for role,base in [('reference',0),('nonglow',region_count),('glow',region_count*2)]:
        for old in regions:
            region=copy.deepcopy(old);region['source_tile']=old['tile'];region['tile']=old['tile']+base;region['layer']=role
            region['offset']=[old['offset'][i]+offsets[role][i]for i in range(2)]
            region['layer_partition']='unchanged_reference'if role=='reference'else('alpha & support'if role=='glow'else'alpha & !support')
            new_regions.append(region)
    report={'source_candidate':str(args.candidate.resolve()),'source_model_sha256':digest(args.candidate/'lucifer_p2.bbmodel'),
            'source_atlas_sha256':digest(args.candidate/'atlas.png'),'source_mask_sha256':digest(args.mask),
            'semantic_basis':'The original Jungle BasePass pixel shader a76883453ab15344d2a4b5c87f3268361971f605 confirms auxiliary B as the additional pink emissive term. R/G/B nonzero supports coincide here; source alpha is respected. This Java light_emission=15 partition represents only that support, not the original NaturalEmissive=0.60000002384 base term, HDR intensity or time pulse. See source/material_port/JUNGLE_EMISSIVE_SHADER_AUDIT.md.',
            'original_atlas_size':[width,height],'output_atlas_size':[width*2,height*2],
            'atlas_regions':{role:{'offset':list(offset),'size':[width,height]}for role,offset in offsets.items()},
            'support_pixels_including_derived_cutouts':int(np.count_nonzero(support)),
            'original_opaque_pixels':int(np.count_nonzero(original[:,:,3])),
            'non_glow_opaque_pixels':int(np.count_nonzero(layers['nonglow'][:,:,3])),
            'glow_opaque_pixels':int(np.count_nonzero(layers['glow'][:,:,3])),
            'layer_alpha_overlap_pixels':overlap,'max_alpha_sum_error':alpha_error,
            'pixel_compositing_equals_previous_atlas':bool(np.array_equal(recompose,original)),
            'reference_region_pixel_identical':bool(np.array_equal(packed[:height,:width],original)),
            'reference_png_bytes_identical':digest(args.output/'atlas_reference.png')==digest(args.candidate/'atlas.png'),
            'source_bones_preserved':40,'existing_groups_preserved':len(input_groups),'added_glow_bones':len(glow_names),
            'parts_before':len(parts),'parts_after':len(parts),'elements_before':len(mapping),'elements_after':len(output_elements),
            'nonglow_cubes':element_count['nonglow'],'glow_cubes':element_count['glow'],'face_counts':dict(face_count),
            'fully_transparent_elements_omitted':len(transparent),'source_triangles_preserved':len(original_triangles),
            'triangle_partition_note':'A source triangle may appear in both layer records, but their effective alpha supports are disjoint. Source attribution is conserved as a set and in glow_source_map.json; multiplicity is intentional masked partitioning.',
            'geometry_and_rotation_changed':False,'only_uv_translation_applied':True,'rest_zero_glow_children':True,
            'max_uv_translation_roundoff_pixels':max_uv_translation_residual,
            'layers':{role:{'file':f'atlas_{role}.png','file_sha256':digest(args.output/f'atlas_{role}.png'),
                             'rgba_pixel_sha256':pixel_digest(layer)}for role,layer in [('reference',original),*layers.items()]},
            'output_atlas_sha256':digest(args.output/'atlas.png'),
            'visual_verification':'Not rendered by this script; root should render the single combined atlas and verify per-bone emission assignment.',
            'glow_bones':list(glow_names.values())}
    model.setdefault('display_dungeons',{})['glow_layering']={k:report[k]for k in ['semantic_basis','glow_bones','parts_after','glow_cubes','pixel_compositing_equals_previous_atlas']}
    write(args.output/'lucifer_p2.bbmodel',model);write(args.output/'parts.json',parts)
    write(args.output/'conversion_map_before_glow.json',mapping);write(args.output/'conversion_map.json',output_mapping)
    write(args.output/'glow_source_map.json',source_map);write(args.output/'glow_bones.json',list(glow_names.values()))
    write(args.output/'transparent_source_elements.json',transparent);write(args.output/'atlas_regions.json',new_regions)
    if (args.candidate/'validation').exists():shutil.copytree(args.candidate/'validation',args.output/'validation',dirs_exist_ok=True)
    baseline_validation=read(args.candidate/'validation/static_conversion.json')
    write(args.output/'validation/static_conversion_before_glow.json',baseline_validation)
    baseline_validation.update(total_elements=len(output_elements),atlas_size=[width*2,height*2],
                               parts=len(parts),glow_cubes=element_count['glow'],nonglow_cubes=element_count['nonglow'],
                               glow_bones=len(glow_names),glow_layering_report='glow_layering.json',
                               zero_thickness_cubes=sum(any(abs(a-b)<=1e-12 for a,b in zip(e['from'],e['to']))for e in output_elements),
                               solid_cubes=sum(all(abs(a-b)>1e-12 for a,b in zip(e['from'],e['to']))for e in output_elements))
    baseline_validation['all_triangles_covered_once_before_layer_partition']=baseline_validation.pop('all_triangles_covered_once',None)
    baseline_validation['source_triangles_preserved_after_layer_partition']=len(original_triangles)
    baseline_validation['glow_coverage_note']=report['triangle_partition_note']
    baseline_validation['glow_status']=report['semantic_basis']
    write(args.output/'validation/static_conversion.json',baseline_validation)
    write(args.output/'validation/glow_layering.json',report)
    print(json.dumps({k:report[k]for k in ['parts_after','elements_after','glow_cubes','nonglow_cubes','added_glow_bones','source_bones_preserved','layer_alpha_overlap_pixels','pixel_compositing_equals_previous_atlas']},indent=2))


if __name__=='__main__':main()
