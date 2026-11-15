from pathlib import Path
import json,copy,sys,base64
R=Path('D:/agent/codex/TRA/work'); p=R/'lucifer_verdant'
sys.path.insert(0,str(R/'lucifer_original'))
import native_import as n
b=json.loads((R/'lucifer_original/body_for_blockbench.json').read_text(encoding='utf-8'))
a=json.loads((p/'verdant_for_blockbench.json').read_text(encoding='utf-8'))
w=json.loads((p/'weapon_native_input.json').read_text(encoding='utf-8'))
d=copy.deepcopy(b);d['project_name']='lucifer_verdant';d['armature_name']='MossySkeleton_SourceRig'
names={v['name']:v['id'] for v in b['bones']}
for part in d['parts']:part['name']='body__'+part['name'];part['textureIndex']=0
for src in a['parts']:
 part=copy.deepcopy(src);part['name']='armor__'+part['name'];part['textureIndex']=1
 for key,weights in part['weights'].items():
  part['weights'][key]=[[names[a['bones'][v]['name'].replace('J_Spine','J_L_Spine')],wt] for v,wt in weights]
 d['parts'].append(part)
part=copy.deepcopy(w['parts'][0]);part['name']='weapon__LuciferSerpentSpear';part['textureIndex']=3;d['parts'].append(part)
aux=p/'exported/Game/Actors/Equipment/Armor/EvocationRobe_Unique1/T_EvocationRobe_Unique1_S.png'
d['additional_textures']=[{'path':a['texture_path'],'width':64,'height':64},{'path':str(aux),'width':64,'height':64},{'path':w['texture_path'],'width':32,'height':32}]
(p/'lucifer_verdant_input.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
orig=n.checked
select='ModelProject.all.find(p=>p.name==="lucifer_verdant").select();'
def checked(tool,args=None):
 args=args or {}
 if tool=='risky_eval':args=dict(args,code=select+args['code'])
 return orig(tool,args)
exists=orig('risky_eval',{'code':'ModelProject.all.some(p=>p.name==="lucifer_verdant")'})
if exists:raise RuntimeError('Already exists, refusing duplicate')
orig('create_project',{'name':d['project_name'],'format':'free'})
n.checked=checked
checked('risky_eval',{'code':'Project.texture_width=64;Project.texture_height=32;Project.box_uv=false;true'})
textures=[{'path':d['texture_path'],'width':64,'height':32}]+d['additional_textures']
for t in textures:
 png=Path(t['path']).read_bytes();url='data:image/png;base64,'+base64.b64encode(png).decode()
 code='(()=>{const t=new Texture({name:'+n.js_literal(Path(t['path']).name)+',uv_width:'+str(t['width'])+',uv_height:'+str(t['height'])+',render_sides:"double"}).add(false);t.fromDataURL('+n.js_literal(url)+');return t.uuid;})()'
 checked('risky_eval',{'code':code})
print(n.import_data(d))
print(n.save_native('lucifer_verdant'))
