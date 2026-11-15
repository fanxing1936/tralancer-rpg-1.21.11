"""Build/verify phase-B delivery inventory. Default is verification only.
Run after all evidence writers finish: python -B refresh_delivery_manifest.py --write
"""
from pathlib import Path
import argparse, hashlib, json

EXCLUDED_NAMES={'SOURCES.md','delivery_manifest.json'}

def digest(p):
    b=p.read_bytes();return len(b),hashlib.sha256(b).hexdigest()

def included(p):
    return p.is_file() and '__pycache__' not in p.parts and p.suffix.lower() not in {'.pyc','.pyo'} and p.name not in EXCLUDED_NAMES

def category(rel,p):
    # Probe programs remain authored programs even inside a folder named source.
    if p.suffix.lower() in {'.py','.java','.ps1','.cs','.js'}:return 'authored_program','本次编写的提取/转换/验证程序；不是原游戏素材；运行依赖及范围见文件正文'
    if rel.startswith('validation/scale_alignment/'):return 'scale_alignment_evidence','共享源单位尺度审计、隔离重建对照及应用记录；失败候选与最终应用范围分别标明'
    if rel.startswith('game_preview/'):return 'client_evidence','隔离 Java 客户端尝试、截图或日志证据；是否实际见到模型以本目录说明及截图为准'
    if rel.startswith('validation/runtime_numeric'):return 'runtime_numeric_evidence','Java显示实体运行时数值、插值及重载边界验证；不是客户端视觉截图'
    if rel.startswith('validation/server/'):return 'server_evidence','隔离服务器加载/函数执行验证；不是客户端视觉证据'
    if rel.startswith('validation/'):return 'validation_evidence','转换、兼容性、原数据比对或隔离验证记录；旧CUE参考与最终原时间语义以文件作用域为准'
    if rel.startswith('animations_preview/'):return 'generated_animation_preview','源数据驱动生成的动画预览；不是原游戏录像或Java客户端截图'
    if rel.startswith('reference_views/'):return 'generated_source_reference','原网格派生的参考视图；不是原游戏截图'
    if rel.startswith('comparison/'):return 'comparison_evidence','源网格/转换模型渲染或Blockbench查看对照；具体捕获方式见同目录说明'
    if rel.startswith('native/'):return 'native_editor_evidence','Blockbench原生导入/保存/查看及派生验证；不冒充原游戏素材'
    if rel.startswith('material/'):return 'generated_material_runtime','原材质证据驱动的Java材质派生文件与预览；core微光/pulse范围见材质报告'
    if rel.startswith('source/material_port/'):return 'material_source_audit','原始材质/compiled shader派生审计证据；非原始游戏截图或游戏可直接运行素材'
    if rel.startswith('source/'):return 'source_derived_evidence','提取或探针派生记录；未列于原source_manifest者不宣称为原始素材'
    if rel.startswith('sounds/'):return 'audio_unmapped','音频来源须参考原source_manifest；本分类不额外推断原始性'
    if p.suffix.lower()=='.md':return 'authored_documentation','依据本次源数据、构建与验证证据编写的文档'
    return 'generated_conversion','完整P2转换生成的模型/图集/索引或元数据；见conversion_manifest.json、atlas_regions.json'

def paths(ref):
    local=sorted((p for p in ref.rglob('*') if included(p)),key=lambda p:p.relative_to(ref).as_posix())
    tools=ref.parent
    external=[tools/n for n in ('convert_dungeons.py','add_lucifer_p2_model.py','display_mob.py')]+sorted((tools/'dungeons_conversion').glob('*.py'))
    return [(p.relative_to(ref).as_posix(),p)for p in local]+[('../'+p.relative_to(tools).as_posix(),p)for p in external]

def verify(ref,manifest):
    errors=[];listed={r['file']for r in manifest['files']};actual={r for r,_ in paths(ref)}
    if listed!=actual:errors.append({'inventory_missing':sorted(actual-listed),'inventory_extra':sorted(listed-actual)})
    for r in manifest['files']:
        p=ref/r['file']
        if not p.is_file():errors.append({'missing':r['file']});continue
        n,h=digest(p)
        if n!=r['bytes']or h!=r['sha256']:errors.append({'changed':r['file'],'actual_bytes':n,'actual_sha256':h})
    if errors:raise SystemExit(json.dumps(errors,ensure_ascii=False,indent=2))
    return {'files_verified':len(manifest['files']),'bytes_verified':sum(r['bytes']for r in manifest['files']),'all_records_match':True}

def write(ref):
    originals=json.loads((ref/'source_manifest.json').read_text(encoding='utf-8'));origins={r['file']:r for r in originals};records=[]
    for rel,p in paths(ref):
        n,h=digest(p);kind,description=category(rel,p)
        record={'file':rel,'bytes':n,'sha256':h,'category':kind,'source':description,'derived':True}
        if rel in origins:
            original=origins[rel]
            # Retain exact original provenance, URL and any other fields, while current bytes/hash describe delivery.
            record.update({k:v for k,v in original.items()if k not in {'file','bytes','sha256'}})
            record['original_manifest_bytes']=original.get('bytes');record['original_manifest_sha256']=original.get('sha256')
            record['category']='source_manifest_original_or_derived'
            if p.suffix.lower() in {'.py','.java','.ps1','.cs','.js'}:
                record['category']='authored_program';record['derived']=True
        if rel.startswith('../'):record.update(category='authored_conversion_runtime_program',source='本次转换或Java显示实体运行时程序；与原素材版权分开记录',derived=True)
        if rel.startswith('sounds/'):
            record['wiki_url']=record.get('wiki_url',record['source'])
        records.append(record)
    model=json.loads((ref/'lucifer_p2.bbmodel').read_text(encoding='utf-8'));assert len(model['animations'])==18
    oggs=list((ref/'sounds').glob('*.ogg'));assert len(oggs)==46
    result={'stage':'checkpoint_B_animated_runtime','scope':'phase_two_only','files':records,'model_sha256':digest(ref/'lucifer_p2.bbmodel')[1],'animations_authored':18,'runtime_integrated':True,
        'audio':{'ogg_files':46,'registered_events':38,'timed_bindings':25,'music_note':'Start/Loop为Wiki约30秒预览；不宣称完整原BGM。已下载音频与实际注册/定时绑定区分。'},
        'material_note':'现core微光及时间pulse已接入；源shader/Java实现边界及客户端验证限制见对应报告。',
        'manifest_excludes':['SOURCES.md','delivery_manifest.json','**/__pycache__/**','**/*.pyc','**/*.pyo'],
        'copyright':'Original Minecraft Dungeons assets © Mojang. Non-commercial; unaffiliated with Mojang.'}
    # Freeze all hashes before outputs; reject concurrent drift before publishing manifests.
    verify(ref,result)
    lines=['# 路西法二阶段逐文件来源','',
        'Minecraft Dungeons原素材版权归Mojang所有。本项目非商业，与Mojang无关联。转换程序、探针、验证报告及预览均按派生/创作类别分别列出。','',
        '阶段B：18个动画及运行时接入；46个Ogg、38个注册事件、25/25项启用通知完成定时绑定；最终运行尺度model_scale=7.194918902795097。Start/Loop音乐为Wiki约30秒预览，并非完整原BGM。现core微光与时间pulse已接入；视觉核验范围以客户端证据为准。','',
        '原source_manifest中的精确source、derived及既有wiki_url保留；当前交付字节和SHA独立核验。source目录中的Python探针仍是本次编写程序，不是原素材。生成渲染预览、原生编辑器查看、服务器测试和客户端证据分别标注。','',
        '完整SHA见delivery_manifest.json。排除本文件与delivery_manifest.json以避免循环，也排除Python缓存。可运行python -B refresh_delivery_manifest.py --verify复验所有记录及文件集合。','',
        '| 文件 | 字节 | SHA-256前16位 | 类别 | 来源 |','|---|---:|---|---|---|']
    for r in records:
        safe=lambda v:str(v).replace('|','&#124;').replace('\n',' ')
        lines.append(f"| `{r['file']}` | {r['bytes']} | `{r['sha256'][:16]}` | {r['category']} | {safe(r['source'])} |")
    (ref/'delivery_manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ref/'SOURCES.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return verify(ref,result)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--ref',type=Path);p.add_argument('--write',action='store_true');p.add_argument('--verify',action='store_true');a=p.parse_args()
    ref=(a.ref or Path(__file__).resolve().parent).resolve()
    if a.write:result=write(ref)
    else:result=verify(ref,json.loads((ref/'delivery_manifest.json').read_text(encoding='utf-8')))
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
