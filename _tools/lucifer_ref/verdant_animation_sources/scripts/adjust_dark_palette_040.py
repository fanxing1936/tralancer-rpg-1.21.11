"""Update only the selected assembly's palette config and shader uniform."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT.parent/'lucifer_original'))
from native_import import checked

code='''(()=>{
ModelProject.all.find(p=>p.name==="lucifer_verdant").select();
const protectedState=()=>{const r=Codecs.project.compile({raw:true});return JSON.stringify({elements:r.elements,textures:r.textures,animations:r.animations,groups:r.groups,outliner:r.outliner,resolution:r.resolution})};
const before=protectedState();
const otherConfigs=()=>JSON.stringify(ModelProject.all.filter(p=>p.name!=="lucifer_verdant").map(p=>[p.name,p.dungeons_material_source]));
const othersBefore=otherConfigs();
const previous=Project.dungeons_material_source.palette_tint_linear;
Project.dungeons_material_source.palette_tint_linear=[.40,.40,.40];
LuciferOriginalMaterial.apply(Project);
Canvas.updateAll();
const c=Project.dungeons_material_source;
const material=Project.textures.find(t=>t.uuid===c.albedo_uuid).getOwnMaterial();
return {project:Project.name,previous_palette_tint_linear:previous,status:LuciferOriginalMaterial.status(),config:c,
active_uniforms:{palette_tint_linear:material.uniforms.sourcePaletteTintLinear.value.toArray(),emissive:material.uniforms.sourceEmissiveColor.value.toArray(),emissive_power:material.uniforms.sourceEmissivePower.value,natural:material.uniforms.sourceNaturalEmissive.value},
protected_geometry_texture_animation_unchanged:protectedState()===before,other_project_configs_unchanged:otherConfigs()===othersBefore,
source_projects:ModelProject.all.filter(p=>['verdant_robe_original','root_rot_armor_original'].includes(p.name)).map(p=>{const c=p.dungeons_material_source;const t=p.textures.find(t=>t.uuid===c?.albedo_uuid);return {name:p.name,has_palette_override:Object.hasOwn(c||{},'palette_tint_linear'),uniform:t?.getOwnMaterial()?.uniforms?.sourcePaletteTintLinear?.value?.toArray()}}),
shader_contains_tint:material.fragmentShader.includes('sourceSRGBToLinear(original.rgb) * sourcePaletteTintLinear'),auxiliary_expression_unchanged:material.fragmentShader.includes('vec3 primary = auxiliary.b * sourceEmissiveColor;'),saved_by_this_task:false};
})()'''
r=checked('risky_eval',{'code':code})
assert r['project']=='lucifer_verdant' and r['active_uniforms']['palette_tint_linear']==[.4,.4,.4]
assert r['active_uniforms']['emissive']==[1,1,1]
assert r['protected_geometry_texture_animation_unchanged'] and r['other_project_configs_unchanged']
assert all(s['uniform']==[1,1,1] and not s['has_palette_override'] for s in r['source_projects'])
path=ROOT/'dark_palette_runtime_result.json';old=json.loads(path.read_text())
history=old.get('candidate_history',[])
if not history:history.append({'palette_tint_linear':[.24,.24,.24],'preview':old.get('preview_comparison'),'decision':'Too dark; green pattern contrast hard to read, superseded by 0.40.'})
old.update(r);old['candidate_history']=history;old.pop('preview_comparison',None)
path.write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'dark_palette_config.json').write_text(json.dumps(r['config'],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
plan=json.loads((ROOT/'dark_palette_plan.json').read_text());plan['config_patch']['palette_tint_linear']=[.4,.4,.4]
plan['revision']='0.24 superseded by 0.40 to preserve visible green texture detail.'
(ROOT/'dark_palette_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:r[k] for k in ['project','previous_palette_tint_linear','active_uniforms','protected_geometry_texture_animation_unchanged','other_project_configs_unchanged','source_projects']},ensure_ascii=False))
