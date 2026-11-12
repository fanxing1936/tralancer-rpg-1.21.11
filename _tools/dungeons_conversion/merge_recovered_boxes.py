"""Optional conservative box restoration for an already generated static candidate.

Only closed, opaque boxes whose six existing planes share one part frame are
merged. Open/alpha-cutout boxes retain both-sided planes so their inner surfaces
remain visible. Atlas pixels and copied face UV/rotation dictionaries never change.
"""
from __future__ import annotations
import argparse
from collections import Counter
import copy
import hashlib
import json
import math
from pathlib import Path
import shutil
import uuid

import numpy as np
from PIL import Image

NAMESPACE=uuid.UUID('080ca163-8e69-4849-ab08-682b64bd3a65')
FACE_NAMES={0:('west','east'),1:('down','up'),2:('north','south')}


def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def write(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def face_corners(face,lo,hi):
    axes={'west':(0,0),'east':(0,1),'down':(1,0),'up':(1,1),'north':(2,0),'south':(2,1)}
    axis,side=axes[face];other=[i for i in range(3)if i!=axis]
    corners=[]
    for a,b in ((0,0),(0,1),(1,0),(1,1)):
        p=lo.copy();p[axis]=(lo,hi)[side][axis]
        p[other[0]]=(lo,hi)[a][other[0]];p[other[1]]=(lo,hi)[b][other[1]];corners.append(p)
    return np.array(corners)


def face_alpha_min(face,alpha):
    if face.get('texture')!=0:return None
    uv=face['uv']
    # Do not include an adjacent texel solely due to original floating noise.
    uv=[float(round(v))if abs(v-round(v))<1e-4 else float(v)for v in uv]
    x0,x1=math.floor(min(uv[0],uv[2])),math.ceil(max(uv[0],uv[2]))
    y0,y1=math.floor(min(uv[1],uv[3])),math.ceil(max(uv[1],uv[3]))
    if x0<0 or y0<0 or x1>alpha.shape[1]or y1>alpha.shape[0]or x0>=x1 or y0>=y1:return None
    return int(alpha[y0:y1,x0:x1].min())


def outliner_parent_ids(nodes,result,parent=None):
    for node in nodes:
        if isinstance(node,str):result[node]=parent
        else:outliner_parent_ids(node.get('children',[]),result,node['uuid'])


def rewrite_outliner(nodes,replacement):
    result=[]
    for node in nodes:
        if isinstance(node,str):
            value=replacement.get(node,node)
            if value is not None:result.append(value)
        else:
            node=copy.deepcopy(node);node['children']=rewrite_outliner(node.get('children',[]),replacement);result.append(node)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate',type=Path,default=Path(r'D:\agent\dungeons_extract\phase2_candidate'))
    parser.add_argument('--recovery',type=Path,default=Path(r'D:\agent\dungeons_extract\phase2_analysis\recovery_geometry.json'))
    parser.add_argument('--output',type=Path,default=Path(r'D:\agent\dungeons_extract\phase2_candidate_boxed'))
    parser.add_argument('--tolerance',type=float,default=1e-5,help='Maximum floating-point corner alignment residual, internal model pixels')
    args=parser.parse_args()
    if args.candidate.resolve()==args.output.resolve():raise ValueError('Output must differ from the source candidate')
    model=read(args.candidate/'lucifer_p2.bbmodel');parts=read(args.candidate/'parts.json')
    mapping=read(args.candidate/'conversion_map.json');recovery=read(args.recovery)
    elements={e['uuid']:e for e in model['elements']};map_by_id={m['element']:m for m in mapping}
    alpha=np.asarray(Image.open(args.candidate/'atlas.png').convert('RGBA'))[:,:,3]
    parents={};outliner_parent_ids(model['outliner'],parents)
    replaced_elements={};replacement_ids={};new_maps={};decisions=[]
    model_scale=float(model.get('display_dungeons',{}).get('model_scale',1))
    for box in recovery['primitives']:
        if box['type']!='box':continue
        triangles=set(box['triangle_indices'])
        maps=[m for m in mapping if triangles.intersection(m['source_triangles'])]
        record={'recovery_box':box['primitive'],'source_triangles':sorted(triangles),
                'source_faces':len(box['faces']),'elements_considered':[m['element']for m in maps]}
        reasons=[]
        if box.get('missing_faces'):reasons.append('open_box_preserve_visible_inner_sides')
        if len({m['part']for m in maps})!=1:reasons.append('faces_in_different_parts')
        if any(not set(m['source_triangles']).issubset(triangles)for m in maps):reasons.append('candidate_element_contains_unrelated_source_triangles')
        if set(t for m in maps for t in m['source_triangles'])!=triangles:reasons.append('source_triangle_coverage_mismatch')
        if len(maps)!=6:reasons.append('needs_exactly_six_whole_plane_elements')
        if len({parents.get(m['element'])for m in maps})!=1:reasons.append('different_outliner_parent_frame')
        chosen=[elements[m['element']]for m in maps]
        if any(any(abs(float(a))>1e-12 for a in e.get('rotation',[0,0,0]))for e in chosen):reasons.append('element_local_rotation_not_zero')
        if any(m.get('deforming')for m in maps):reasons.append('deforming_source_geometry')
        if reasons:
            record.update(status='skipped',reasons=reasons);decisions.append(record);continue
        lo=np.min([e['from']for e in chosen],axis=0);hi=np.max([e['to']for e in chosen],axis=0)
        if np.any(hi-lo<=args.tolerance):reasons.append('combined_box_is_degenerate')
        faces={};face_provenance={};max_displacement=0
        for e,m in zip(chosen,maps):
            old_lo=np.array(e['from']);old_hi=np.array(e['to']);extent=old_hi-old_lo
            flat=np.where(abs(extent)<=1e-12)[0]
            if len(flat)!=1:
                reasons.append('candidate_is_not_one_zero_thickness_plane');continue
            axis=int(flat[0]);level=float(old_lo[axis]);side=0 if abs(level-lo[axis])<=abs(level-hi[axis])else 1
            face=FACE_NAMES[axis][side]
            if face in faces:reasons.append('duplicate_box_face');continue
            if face not in e['faces']:reasons.append('outward_uv_face_missing');continue
            displacement=float(np.linalg.norm(face_corners(face,old_lo,old_hi)-face_corners(face,lo,hi),axis=1).max())
            max_displacement=max(max_displacement,displacement)
            if displacement>args.tolerance:reasons.append('plane_bounds_do_not_match_one_box_within_numeric_tolerance')
            minimum=face_alpha_min(e['faces'][face],alpha)
            if minimum!=255:reasons.append('alpha_or_unknown_material_makes_inner_sides_potentially_visible')
            faces[face]=copy.deepcopy(e['faces'][face])
            face_provenance[face]={'old_element':e['uuid'],'old_outward_face':face,'old_face_dictionary':copy.deepcopy(e['faces'][face]),
                                   'source_triangles':m['source_triangles'],'tile':m.get('tile'),'bake':m.get('bake'),
                                   'alpha_minimum':minimum,'max_corner_displacement_internal_pixels':displacement}
        if len(faces)!=6:reasons.append('six_distinct_box_faces_not_covered')
        if reasons:
            record.update(status='skipped',reasons=sorted(set(reasons)),max_corner_displacement_internal_pixels=max_displacement,
                          faces_examined=face_provenance);decisions.append(record);continue
        old_ids=[e['uuid']for e in chosen];first_id=next(e['uuid']for e in model['elements']if e['uuid']in old_ids)
        new_id=str(uuid.uuid5(NAMESPACE,'box:'+str(box['primitive'])+':'+','.join(sorted(old_ids))))
        new=copy.deepcopy(elements[first_id]);new.update(name='recovered_box_'+str(box['primitive']),uuid=new_id,
                                                        **{'from':lo.tolist(),'to':hi.tolist(),'faces':faces,
                                                           '_source_triangles':sorted(triangles),'_merged_source_elements':old_ids,
                                                           '_recovery_box':box['primitive']})
        new.pop('_atlas_tile',None);new['_atlas_tiles']=sorted(set(m.get('tile',0)for m in maps))
        replaced_elements[first_id]=new
        for old in old_ids:replacement_ids[old]=new_id if old==first_id else None
        merged_map={'element':new_id,'part':maps[0]['part'],'source_triangles':sorted(triangles),
                    'geometry_kind':'solid_cube','recovery_box':box['primitive'],'zero_thickness_axis':None,
                    'deforming':False,'split_reason':None,'direct_original_atlas':all(m['direct_original_atlas']for m in maps),
                    'bake':None,'tiles':new['_atlas_tiles'],'source_face_records':copy.deepcopy(maps),'face_provenance':face_provenance,
                    'projection_error_visual_pixels':max(float(m.get('projection_error_visual_pixels',0))for m in maps)+max_displacement*model_scale}
        vertices={}
        for m in maps:
            for index,owner,source_uv,position in zip(m['source_vertex_indices'],m['vertex_source_bones'],m['original_uv'],m['rest_vertices_java_internal']):
                value=(owner,source_uv,position)
                if index in vertices and vertices[index]!=value:raise ValueError('Conflicting original vertex metadata')
                vertices[index]=value
        order=sorted(vertices);merged_map['source_vertex_indices']=order
        for key,i in [('vertex_source_bones',0),('original_uv',1),('rest_vertices_java_internal',2)]:merged_map[key]=[vertices[v][i]for v in order]
        new_maps[first_id]=merged_map
        record.update(status='merged',new_element=new_id,part=maps[0]['part'],old_elements=old_ids,face_provenance=face_provenance,
                      max_corner_displacement_internal_pixels=max_displacement,max_corner_displacement_visual_pixels=max_displacement*model_scale,
                      inner_faces_removed=6,interior_visibility_reason='All six exterior faces are closed and fully opaque; inside faces are occluded from external viewpoints.')
        decisions.append(record)
    original_element_count=len(model['elements'])
    model['elements']=[replaced_elements.get(e['uuid'],e)for e in model['elements']if e['uuid']not in replacement_ids or e['uuid']in replaced_elements]
    model['outliner']=rewrite_outliner(model['outliner'],replacement_ids)
    output_mapping=[new_maps.get(m['element'],m)for m in mapping if m['element']not in replacement_ids or m['element']in new_maps]
    counts=Counter(m['part']for m in output_mapping)
    for part in parts:part['elements']=counts[part['name']]
    original_coverage=Counter(t for m in mapping for t in m['source_triangles'])
    final_coverage=Counter(t for m in output_mapping for t in m['source_triangles'])
    if original_coverage!=final_coverage or any(n!=1 for n in final_coverage.values()):raise ValueError('Source triangle ownership changed')
    outline={};outliner_parent_ids(model['outliner'],outline)
    if set(outline)!=set(e['uuid']for e in model['elements']):raise ValueError('Outliner-element identity mismatch')
    merged=[r for r in decisions if r['status']=='merged']
    report={'source_candidate':str(args.candidate.resolve()),'source_candidate_model_sha256':sha(args.candidate/'lucifer_p2.bbmodel'),
            'source_recovery':str(args.recovery.resolve()),'source_recovery_sha256':sha(args.recovery),
            'tolerance_internal_pixels':args.tolerance,'tolerance_visual_pixels':args.tolerance*model_scale,
            'merged_boxes':len(merged),'skipped_boxes':len(decisions)-len(merged),'elements_before':original_element_count,
            'elements_after':len(model['elements']),'elements_reduced':original_element_count-len(model['elements']),
            'parts_before':len(parts),'parts_after':len(parts),'solid_cubes_after':len(merged),
            'zero_thickness_cubes_after':len(model['elements'])-len(merged),'source_triangles':len(final_coverage),
            'source_triangles_preserved_once':True,'uv_and_rotation_dictionaries_copied_without_change':True,
            'atlas_sha256':sha(args.candidate/'atlas.png'),'atlas_changed':False,
            'max_corner_displacement_visual_pixels':max((r['max_corner_displacement_visual_pixels']for r in merged),default=0),
            'render_validation':'Not performed by this postprocessor. Root should compare external and cavity views before adopting.',
            'interior_policy':'Skip every open or alpha-cutout box; discard inward duplicates only for closed fully opaque boxes. Looking from inside a solid box is intentionally outside the external-surface equivalence claim.',
            'decisions':decisions}
    model.setdefault('display_dungeons',{})['box_postprocess']={k:report[k]for k in ['merged_boxes','elements_before','elements_after','max_corner_displacement_visual_pixels','interior_policy']}
    args.output.mkdir(parents=True,exist_ok=True)
    for name in ('atlas.png','atlas_regions.json'):shutil.copy2(args.candidate/name,args.output/name)
    write(args.output/'lucifer_p2.bbmodel',model);write(args.output/'parts.json',parts);write(args.output/'conversion_map.json',output_mapping)
    base_validation=read(args.candidate/'validation/static_conversion.json')
    write(args.output/'validation/static_conversion_before_box_merge.json',base_validation)
    base_validation.update(zero_thickness_cubes=report['zero_thickness_cubes_after'],solid_cubes=report['solid_cubes_after'],
                           total_elements=report['elements_after'],box_postprocess_report='box_merge_report.json',
                           max_additional_box_alignment_error_visual_pixels=report['max_corner_displacement_visual_pixels'])
    base_validation['box_merge_count_note']='direct_original_atlas_surfaces/baked_source_cutout_surfaces count original source plane surfaces, not postprocessed element count.'
    write(args.output/'validation/static_conversion.json',base_validation)
    write(args.output/'validation/box_merge_report.json',report)
    if sha(args.output/'atlas.png')!=report['atlas_sha256']:raise ValueError('Atlas bytes changed')
    print(json.dumps({k:report[k]for k in ['merged_boxes','skipped_boxes','elements_before','elements_after','parts_after','source_triangles_preserved_once','max_corner_displacement_visual_pixels']},indent=2))


if __name__=='__main__':main()
