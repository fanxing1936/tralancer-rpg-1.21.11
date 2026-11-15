"""Archive explicit source/adaptation/validation evidence only; no secrets or game bundles."""
from pathlib import Path
import hashlib,json,shutil

WORK=Path(__file__).parent
REF=Path(r'D:\agent\claude\github-create\tralancer-rpg-1.21.11\_tools\lucifer_ref')
DEST=REF/'verdant_animation_sources'
SEP=REF/'separate'
EXPECTED_MODEL='14931c0cb1584e5da36ff107e0b5bd953d013b0d3f2f385d57a729e36628f197'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))

def main():
    model=SEP/'lucifer_verdant.bbmodel';assert sha(model)==EXPECTED_MODEL
    payload=WORK/'animation_payload.json';pose=WORK/'animation_pose_reference.npz'
    native=read(SEP/'verdant_native_animation_validation.json')
    assert native['status']=='PASS' and native['payload_sha256']==sha(payload) and native['reference_sha256']==sha(pose)
    grip=read(WORK/'animation_grip_validation.json');assembly=read(SEP/'verdant_assembly_validation.json');math=read(WORK/'animation_payload_math_validation.json')
    assert grip['numeric_grip_checks_pass'] and grip['sha256']==EXPECTED_MODEL
    assert assembly['assembly_data_checks_pass'] and assembly['model_sha256_at_start']==EXPECTED_MODEL
    assert math['status']=='PASS' and math['payload_sha256']==sha(payload) and math['npz_sha256']==sha(pose)
    assert math['builder_sha256']==sha(WORK/'build_animations.py')
    for ext in ['json','md','samples.json']:
        src=WORK/('animation_grip_validation.'+ext);dst=SEP/('verdant_grip_animation_validation.'+ext)
        shutil.copy2(src,dst);assert sha(src)==sha(dst)
    DEST.mkdir(parents=True,exist_ok=True);records=[]
    def copy(src,rel,kind,extra=None):
        src=Path(src);dst=DEST/rel
        assert dst.resolve().is_relative_to(DEST.resolve())
        assert src.suffix.lower() not in {'.jar','.class','.pak','.exe','.dll'}
        assert not any(s in src.name.lower() for s in ['asset_key','bb_session','classpath'])
        assert not ('mappings' in src.name.lower() and src.stat().st_size>100000)
        h=sha(src);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
        assert sha(src)==h and sha(dst)==h
        records.append({'path':Path(rel).as_posix(),'kind':kind,'bytes':dst.stat().st_size,'sha256':h,**(extra or {})})
    # UModel preserves original source tracks in a documented export format. These are not authored replacement motions.
    exports=read(WORK/'necromancer_export_manifest.json')
    for a in exports['animation_exports']:
        src=Path(a['output']);assert sha(src)==a['sha256']
        copy(src,Path('original_game_exports/animations')/src.name,'original_game_motion_umodel_export',{'original_package':a['package'],'export_sha256_verified':True})
        for suffix in ['.props.txt','.config']:
            p=src.with_suffix(suffix)
            if p.exists():copy(p,Path('original_game_exports/animations')/p.name,'original_animation_export_metadata')
    rig=Path(exports['rig_gltf'])
    for ext in ['.gltf','.bin']:copy(rig.with_suffix(ext),Path('original_game_exports/rig')/rig.with_suffix(ext).name,'original_animation_rig_dependency')
    source_names=['necromancer_export_manifest.json','necromancer_animation_source.json','necromancer_animation_summary.json','necromancer_animation_source_audit.json']
    for name in source_names:copy(WORK/name,Path('source_evidence')/name,'source_parsing_or_source_audit')
    for name in ['animation_timing.json','animation_source_and_timing.md','leviathan_cast_rise_reference.json']:
        copy(WORK/name,Path('source_evidence')/name,'existing_project_reference_and_timing')
    for name in ['Psk.h','ExportPsk.cpp','ExportGLTF.cpp','UnAnim4.cpp','EvokerFangs.javap.txt','fangs_source.json']:
        copy(WORK/'source_format'/name,Path('source_evidence/format_and_timing')/name,'format_or_timing_primary_implementation_evidence')
    for name in ['weapon_source_review.md','weapon_existing_generated.json','weapon_native_input.json','weapon_native_validation.json','spear_in_hand.original.json','weapon_minecraft_mappings_excerpt.txt']:
        copy(WORK/name,Path('weapon_source')/name,'existing_java_resourcepack_weapon_evidence')
    for name in ['weapon_grip_alignment.json','lucifer_verdant_input.json','animation_payload.json','animation_pose_reference.npz','dark_palette_plan.json','dark_palette_config.json','dark_palette_runtime_result.json']:
        copy(WORK/name,Path('adapted')/name,'explicit_user_authorized_adaptation')
    # Freeze each current report only after checking its input fingerprint above.
    copy(WORK/'animation_payload_math_validation.json','validation/animation_payload_math_validation.json','independent_source_and_payload_math_validation')
    for name in ['verdant_native_animation_validation.json','verdant_grip_animation_validation.json','verdant_grip_animation_validation.md','verdant_grip_animation_validation.samples.json','verdant_assembly_validation.json','verdant_assembly_validation.md']:
        copy(SEP/name,Path('validation')/name,'final_native_or_saved_file_validation')
    scripts=['parse_necromancer_psa.py','audit_animation_source.py','write_animation_timing_report.py','build_animations.py','import_animations.py','import_assembly.py',
        'validate_animation_payload_math.py','validate_native_motion.py','validate_grip_animation.py','validate_verdant_assembly.py','capture_motion.py',
        'prepare_existing_weapon.py','extract_existing_weapon.py','ExistingWeaponExtractor.java','align_existing_spear_grip.py','adjust_dark_palette_040.py','package_final_animation_evidence.py']
    for name in scripts:copy(WORK/name,Path('scripts')/name,'implementation_or_validation_script')
    copy(WORK.parent/'lucifer_original/body_for_blockbench.json','dependencies/body_for_blockbench.json','verified_target_bind_rig_import_data')
    attack=next(c for c in grip['clips'] if c['animation']=='animation.attack')
    report_summary={'model_sha256':EXPECTED_MODEL,'payload_sha256':sha(payload),'reference_npz_sha256':sha(pose),
        'source_animation_json_sha256':sha(WORK/'necromancer_animation_source.json'),'native_status':native['status'],
        'native_authored_poses':sum(c['poses'] for c in native['clips']),'native_max_rotation_matrix_error':native['max_rotation_error'],
        'native_max_position_error_java_pixels':native['max_position_error_px'],'independent_grip_pass':grip['numeric_grip_checks_pass'],
        'independent_grip_samples':sum(c['sample_count'] for c in grip['clips']),'attack_start_and_hold':attack['immediate_damage_and_hold_samples'],
        'assembly_pass':assembly['assembly_data_checks_pass'],'geometry_material_core_sha256':assembly['frozen_core_sha256'],
        'payload_math_status':math['status'],'known_limits':grip['limits']}
    summaryfile=DEST/'FINAL_VALIDATION_INDEX.json';summaryfile.write_text(json.dumps(report_summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    records.append({'path':summaryfile.name,'kind':'final_evidence_index','bytes':summaryfile.stat().st_size,'sha256':sha(summaryfile)})
    text=f'''# Verdant 路西法：动作与握矛证据包

本包对应最终原生模型 `../separate/lucifer_verdant.bbmodel`，SHA-256 `{EXPECTED_MODEL}`。不复制最终模型本体；这里只封存其来源、适配输入、脚本和核验结果。原材质 shader 证据已在 `../verdant_sources/material_port/`，不重复封装。

## 原始来源与适配分开记录

| 目录 | 内容与含义 |
|---|---|
| original_game_exports | 7 个 Skeleton Necromancer 原动作 PSA、原导出 props/config、配套骨架 glTF/bin。PSA 是 UE Viewer 从本机原游戏转换的导出格式，未冒称原 UE 原始容器。 |
| source_evidence | 完整原动作 JSON、19,721 个键的源字节/坐标核验、35 骨源 mesh 与 37 track 记录、技能时序、项目 Leviathan cast/rise 参考及格式实现依据。 |
| weapon_source | 项目既有蛇矛模型/贴图生成证据、原客户端 ItemModelGenerator 导出的几何和原 UV；不是重新设计的矛。 |
| adapted | 22 骨重定向、最终 8 clip payload/NPZ、获准握点刚体平移、最终整合输入、0.40 深色 palette 配置。 |
| validation | 最终 payload 数学核验、Blockbench 实际骨矩阵核验、独立保存文件握点/前刺核验，以及整合几何/纹理核验。 |
| scripts | 对应当前输入的 builder、importer、只读 validator、capture 和武器适配实现；不含连接凭据。 |

`source_evidence/animation_source_and_timing.md` 和 timing JSON 保留其生成时的来源研究状态；其中“尚未最终验收”是历史阶段说明。最终当前状态以 `FINAL_VALIDATION_INDEX.json`、本 README 和 validation 内对应哈希的报告为准；没有篡改来源研究文件来伪装成最终检查。

原动作并非不加改动地用于最终角色：walk 将原悬浮下肢改成双腿行走；attack 改成持蛇矛前刺并从立即生效姿态开始；strong 裁选原重击释放段；cast/rise 来自项目已有 Leviathan 动作并换骨框架；所有持物运动保留原手部跟随，同时移除不适合当前蛇矛的法杖 socket 位移。GetHitFront 保存为来源参考，不新增第九个交付动作。每个最终 clip 的 `source` 与 `notes` 均在 payload 内。

蛇矛唯一几何调整为统一刚体平移到真实握点，原 PNG、UV、形状、尺度和朝向不变；平移与语义握点见 `adapted/weapon_grip_alignment.json`。法袍 palette `[0.40,0.40,0.40]` 是用户授权风格变动：surface 与自然发光共用变暗 Albedo，辅助 S.B 的白色主发光不乘 palette；原 PNG 字节未改变。

## 最终验证摘要

- 实际 Blockbench 5.2.2 执行全部 {report_summary['native_authored_poses']} 个作者姿态并对比参考骨世界矩阵：PASS；最大旋转矩阵差 `{native['max_rotation_error']:.16g}`，最大位置差 `{native['max_position_error_px']:.16g}` Java 像素。
- 独立读取最终 bbmodel 的 8 clip，共 {report_summary['independent_grip_samples']} 个采样，覆盖全部存储 key、段中点与 120 Hz 网格：握点接触及绑定检查 PASS。
- attack 在 t=0 和 0.06 秒，握点到矛尖偏离 Java -Z 均为 0°，向前伸出约 20.4707083 像素。原矛尾到矛尖轴偏差约 0.24433°，源图案中心线与握点中心的定义不同，不混作同一测量。
- body/armor 坐标、UV 和原纹理保真；武器施加已授权 Δ 后逐点差 0，形状距离重算只有双精度残差。最终模型几何/骨/纹理/material 指纹 `{assembly['frozen_core_sha256']}`。

数值通过有明确范围：laugh 中握点纹素棱柱部分角可伸出手臂约 0.10959 像素，中心仍接触；walk 插值最低脚底可到约 -0.019186 像素，未声称连续严格贴地。有限采样不是全时域碰撞证明；native 骨矩阵验证也不是 Minecraft 实机、命中/伤害、清理生命周期或完整原 Unreal 渲染验证。

## 完整性和复现

`source_manifest.json` 记录每个文件的相对路径、分类、字节数与 SHA-256，复制前后逐字节哈希核对。7 个 PSA 还与先前导出清单中的 SHA-256 比较。本包最终 payload 和 NPZ 分别为 `{sha(payload)}`、`{sha(pose)}`；native 验证和独立 payload 核验均指向这两个最终输入。

脚本保留产生当前证据时的真实路径与导入约定，是可检查的实现快照，不声称任意目录解压即能无配置执行。运行导入/capture 需要本机 Blockbench MCP 会话，运行客户端提取需要用户本机 Java 客户端；这些凭据、完整客户端 JAR、classpath、编译 class、大 mappings、游戏 PAK 和密钥均未封装。脚本引用本项目已有 display_mob.py、Leviathan 工程和原绑定数据时保留原路径，dependencies 补存目标 bind 输入；未重复复制其他怪物完整工程。

原游戏模型/动画及源素材版权归 Mojang Studios / Microsoft 和相关权利人；本包只记录用户本地授权提取与项目适配，不赋予额外再分发权。UE Viewer 源码片段保持其原声明。未上传网络或打包完整游戏资源。
'''
    doc=DEST/'README.md';doc.write_text(text,encoding='utf-8')
    records.append({'path':doc.name,'kind':'archive_documentation','bytes':doc.stat().st_size,'sha256':sha(doc)})
    manifest={'scope':'Final source/adaptation evidence archive; no keys, game PAKs, client JAR/classes/classpath/large mappings or full shader library.',
        'final_model_sha256':EXPECTED_MODEL,'source_game_version':'1.17.0.0','java_target_version':'1.21.11',
        'source_tool':{'name':'UE Viewer','build':1590,'sha256':exports['tool_sha256'],'official_repository':'https://github.com/gildor2/UEViewer'},
        'final_validation_index':'FINAL_VALIDATION_INDEX.json','files':records,
        'counts':{'files_excluding_manifest':len(records),'total_bytes_excluding_manifest':sum(r['bytes'] for r in records),'original_psa':7,'final_clips':8}}
    (DEST/'source_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    actual={p.relative_to(DEST).as_posix() for p in DEST.rglob('*') if p.is_file()}
    assert actual=={r['path'] for r in records}|{'source_manifest.json'}
    assert all(sha(DEST/r['path'])==r['sha256'] for r in records)
    assert sha(model)==EXPECTED_MODEL
    print(json.dumps({'counts':manifest['counts'],'model_sha256':EXPECTED_MODEL,'native_poses':report_summary['native_authored_poses'],'grip_samples':report_summary['independent_grip_samples']},ensure_ascii=False))

if __name__=='__main__':main()
