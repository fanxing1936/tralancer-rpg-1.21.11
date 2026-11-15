"""把已保存的教皇 bbmodel 重新导入独立 Blockbench 工程，检查后关闭该检查页。"""
import hashlib,json
from pathlib import Path
from pope_blockbench import BlockbenchMCP
REF=Path(__file__).resolve().parent/'pope_ref'

def main():
    c=BlockbenchMCP();model=REF/'pope.bbmodel';doc=json.loads(model.read_text(encoding='utf-8'));spec=json.loads((REF/'m2/model_spec.json').read_text(encoding='utf-8'));original=spec['blockbench_project']['uuid']
    c.tool('create_project',dict(name='pope_m2_roundtrip_check',format='bedrock'))
    info=c.evaluate("(function(){if(Project.name!=='pope_m2_roundtrip_check')throw Error('检查工程隔离');Codecs.project.parse("+json.dumps(doc,ensure_ascii=False).replace('/',r'\u002f')+");Project.name='pope_m2_roundtrip_check';return {uuid:Project.uuid,name:Project.name,format:Format.id,elements:Cube.all.length,groups:Group.all.length,animations:Animation.all.length,textures:Texture.all.length};})()")
    result=c.evaluate("(function(){if(Project.uuid!=="+json.dumps(info['uuid'])+")throw Error('检查页变化');return {loaded:Texture.all.every(t=>t.img.complete&&t.img.naturalWidth>0),texture_sizes:Texture.all.map(t=>[t.img.naturalWidth,t.img.naturalHeight]),geometry_ready:Cube.all.every(c=>c.mesh&&c.mesh.geometry),element_ids:Cube.all.map(c=>c.uuid),group_ids:Group.all.map(g=>g.uuid)};})()")
    assert result['loaded'] and result['geometry_ready']
    assert set(result['element_ids'])=={e['uuid'] for e in doc['elements']}
    assert set(result['group_ids'])=={g['uuid'] for g in doc['groups']}
    result.pop('element_ids');result.pop('group_ids');result.update(info=info,model_sha256=hashlib.sha256(model.read_bytes()).hexdigest(),uuid_roundtrip=True,engine='Blockbench 5.2.2 Codecs.project.parse saved file')
    c.evaluate("(async function(){const p=ModelProject.all.find(p=>p.uuid==="+json.dumps(info['uuid'])+");if(!p||p.name!=='pope_m2_roundtrip_check')throw Error('检查页隔离');p.select();p.saved=true;await p.close();const original=ModelProject.all.find(p=>p.uuid==="+json.dumps(original)+");if(original)original.select();return true;})()")
    (REF/'m2/validation/blockbench_roundtrip.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
