"""让 Blockbench 从磁盘完整打开已保存 M3 源文件，并核对再编译语义。"""
import hashlib,json
from pathlib import Path
from pope_blockbench import BlockbenchMCP
from pope_validate_motion import semantic_static,canonical_hash

REF=Path(__file__).resolve().parent/'pope_ref';OUT=REF/'m3'

def main():
    model=REF/'pope.bbmodel';doc=json.loads(model.read_text(encoding='utf-8'))
    spec=json.loads((REF/'m2/model_spec.json').read_text(encoding='utf-8'))
    original=json.loads((OUT/'blockbench_project.json').read_text(encoding='utf-8'))
    client=BlockbenchMCP();client.tool('create_project',{'name':'pope_m3_disk_check','format':'bedrock'})
    info=client.evaluate("(function(){if(Project.name!=='pope_m3_disk_check')throw Error('检查项目隔离');const data=JSON.parse(require('fs').readFileSync("+json.dumps(str(model)) +",'utf8'));Codecs.project.parse(data);Project.name='pope_m3_disk_check';return {uuid:Project.uuid,name:Project.name,animations:Animation.all.map(a=>({name:a.name,length:a.length,loop:a.loop})),elements:Cube.all.length,groups:Group.all.length};})()")
    prefix="const project=ModelProject.all.find(p=>p.uuid==="+json.dumps(info['uuid'])+");if(!project||project.name!=='pope_m3_disk_check')throw Error('项目隔离');project.select();"
    actual=client.evaluate('(function(){'+prefix+'if(!Texture.all.every(t=>t.img.complete&&t.img.naturalWidth>0))throw Error("贴图未加载");return Codecs.project.compile({raw:true});})()')
    assert canonical_hash(semantic_static(doc,spec))==canonical_hash(semantic_static(actual,spec))
    def animation_data(document):
        return [{'name':a['name'],'length':a['length'],'loop':a['loop'],'tracks':{
            bone:sorted([(k['channel'],float(k['time']),k['interpolation'],tuple(float(k['data_points'][0][x]) for x in 'xyz')) for k in animator['keyframes']])
            for bone,animator in a['animators'].items()}} for a in document['animations']]
    assert animation_data(doc)==animation_data(actual)
    report={'model_sha256':hashlib.sha256(model.read_bytes()).hexdigest(),'opened_from_disk':True,
            'static_semantics_unchanged':True,'all_numeric_tracks_roundtripped':True,'texture_loaded':True,
            'native':info,'unrecorded_manual_edits':False,'in_game_verified':False}
    (OUT/'validation/blockbench_disk_roundtrip.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    client.evaluate("(async function(){"+prefix+"project.saved=true;await project.close();const p=ModelProject.all.find(p=>p.uuid==="+json.dumps(original['uuid'])+");if(p&&p.name==='pope_m3_motion')p.select();return true;})()")
    print(json.dumps(report,ensure_ascii=True))

if __name__=='__main__':main()
