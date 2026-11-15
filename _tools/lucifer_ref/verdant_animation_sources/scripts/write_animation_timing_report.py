"""Build scoped animation evidence/timing notes from read-only task sources."""
from pathlib import Path
import hashlib, json, re

ROOT=Path(__file__).resolve().parent
REPO=Path(r'D:\agent\claude\github-create\tralancer-rpg-1.21.11')
SOURCE=ROOT/'necromancer_animation_source.json'
FROZEN='930867a3022a9544915e48f83c192d18be970d29777e731b6b4bec9f478bfcd1'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def record(p):
    p=Path(p)
    return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(name, data):
    (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    assert sha(SOURCE)==FROZEN
    source=json.loads(SOURCE.read_text(encoding='utf-8'))
    audit=json.loads((ROOT/'necromancer_animation_source_audit.json').read_text(encoding='utf-8'))
    function_names=['sk1_1','sk1_2','sk1_3','sk1_4','sk1_5','sk1_line','sk1b_thrust',
                    'sk1b_hit','sk1b_hit_holy','sk1c_lift','sk1c_lift_holy','sk1d_fall','sk1d_fall_holy','sk1e_reject','sk1e_reject_holy',
                    'cast','advent_tick','ult_start','ult_tick','ult_charge','ult_warn','ult_resolve','ultimate',
                    'ult1_warn','ult1_charge','ult1','ult1_fangs','ult1_hit','ult1_hit_holy']
    taint=REPO/'rpg/data/rpg/function/taint'
    function_sources=[record(taint/(n+'.mcfunction')) for n in function_names]
    for n in ['sk1_1','sk1_2','sk1_3','sk1_4','sk1_5','sk1b_thrust','sk1b_hit','sk1c_lift','sk1d_fall','sk1e_reject','ult1','ult1_hit']:
        assert not re.search(r'^\s*schedule\b',(taint/(n+'.mcfunction')).read_text(encoding='utf-8'),re.M)
    assert sorted(set(map(int,re.findall(r'Warmup:(\d+)',(taint/'sk1_line.mcfunction').read_text()))))==list(range(2,17,2))
    assert sorted(set(map(int,re.findall(r'Warmup:(\d+)',(taint/'ult1_fangs.mcfunction').read_text()))))==[4,8,12]
    fangs=json.loads((ROOT/'source_format/fangs_source.json').read_text(encoding='utf-8'))
    fangs.update({'mapped_class':'net.minecraft.world.entity.projectile.EvokerFangs -> ddw',
                  'mapped_fields':{'warmupDelayTicks':'e','tick':'g','dealDamageTo':'c'},
                  'mappings_lines':[110766,110785],
                  'damage_predicate':'--warmupDelayTicks == -8',
                  'entity_update_ordinal':'initial Warmup + 8',
                  'bytecode_proof':record(ROOT/'source_format/EvokerFangs.javap.txt'),
                  'bytecode_offsets':{'predecrement':224,'compare_minus8':238,'damage_call':299},
                  'boundary':'精确到实体 tick 调用次数；实体生成与世界 tick 阶段之间的相位未在真实游戏运行验证，不能把静态字节码审计写成游戏实测。'})
    legacy=[]
    for rel in ['_tools/leviathan_ref/leviathan.bbmodel','_tools/sunken_skeleton_ref/sunken_skeleton.bbmodel']:
        p=REPO/rel; d=json.loads(p.read_text(encoding='utf-8'))
        legacy.append({**record(p),'animations':[{'name':a['name'],'length_seconds':a['length'],'loop':a['loop']} for a in d['animations']],
                       'status':'项目重建动画，不是原游戏网格/动画导出'})
    original=[]
    for a in source['animations']:
        props=Path(a['psa_path']).with_suffix('.props.txt');text=props.read_text(encoding='utf-8')
        original.append({'name':a['short_name'],'frames':a['anim_info']['num_raw_frames'],'fps_including_RateScale':a['anim_info']['anim_rate'],
                         'duration_seconds':a['duration_seconds'],'last_sample_seconds':a['last_sample_seconds'],
                         'raw_SequenceLength_seconds':float(re.search(r'^SequenceLength = (.+)$',text,re.M)[1]),
                         'RateScale':float(re.search(r'^RateScale = (.+)$',text,re.M)[1]),
                         'psa':record(a['psa_path']),'props':record(props),'gif':a['reference_gif'],
                         'notifies_boundary':'props 中的 NotifyName 不能证明事件的准确秒数；未得到可靠触发 time/link 值，不使用异常 EndLink 值推断出手帧。'})
    clips=[
      {'index':0,'clip':'idle','loop':True,'source':'original Necromancer Idle PSA','adaptation':'原动作重定向到 Mossy 22 骨；持矛姿态另记录。','original_source_duration':original[0]['duration_seconds'],'impact_tick':None},
      {'index':1,'clip':'walk','loop':True,'source':'original Necromancer Walk PSA upper body; project Sunken walk leg phase reference','adaptation':'原上身曲线保留；下身悬浮改成双腿交替行走，这是用户要求的适配。Sunken 腿关键点 R(+25,-25,+25)、L(-25,+25,-25) 度，t=0,.5,1s，只提供步态幅度/相位参考，不能直接加到新骨架欧拉角。','original_source_duration':original[1]['duration_seconds'],'impact_tick':None},
      {'index':2,'clip':'attack','loop':False,'source':'original Necromancer BasicAttack PSA','adaptation':'法杖动作改为握蛇矛向前刺；选定释放/有效帧裁为 t=0，再恢复。不得把未核实的源帧当原游戏伤害事件。','original_source_duration':original[2]['duration_seconds'],'impact_tick':0},
      {'index':3,'clip':'strong','loop':False,'source':'original Necromancer StrongAttack PSA','adaptation':'对立即生效的重招将释放/重击姿态放在 t=0；后续恢复保留源动作依据。','original_source_duration':original[3]['duration_seconds'],'impact_tick':0},
      {'index':4,'clip':'cast','loop':False,'source':'project leviathan animation.cast','adaptation':'legacy cast 总长1.2s、原释放 cue 0.65s；不能原封不动接立即生效技能。将释放姿态裁首或调整时间为0，保留完整原时间映射。','original_source_duration':1.2,'impact_tick':0},
      {'index':5,'clip':'laugh','loop':False,'source':'original Necromancer Novelty PSA','adaptation':'用于30tick/1.5s大招警告。可裁选/重定时覆盖1.5s，或被 strong 在第30tick明确接管；原3.2916667s整段不能被称已完整播完。','original_source_duration':original[5]['duration_seconds'],'impact_tick':None,'warning_window_ticks':30},
      {'index':6,'clip':'stun','loop':False,'source':'original Necromancer Stun PSA','adaptation':'绑定驱魔束缚状态；结束/持有策略由运行时明确处理。未在本任务读取完整束缚运行时，不能声明已验证触发。','original_source_duration':original[4]['duration_seconds'],'impact_tick':None},
      {'index':7,'clip':'rise','loop':False,'source':'project leviathan animation.rise','adaptation':'沿用项目登场轨迹并重定向；原 SkeletonNecromancer/Animations 索引没有名为 Rise 或 Summon 的序列。Sleeping 不自动等同 Rise。','original_source_duration':2.4,'impact_tick':None}
    ]
    for c in clips:
        c['final_native_clip_duration_seconds']=None
        c['status']='动作来源/制作约束；最终 native 动作及视觉验证由主任务完成'
    skills=[
      {'hook':'sk1_1','clip':'attack','label':'原罪','immediate_effect_tick':0,'immediate_effect':'沿视线召唤8个尖牙；起手/蛇矛释放在0tick。','direct_damage_tick':None,'fang_warmups':list(range(2,17,2)),'fang_damage_entity_updates':list(range(10,25,2))},
      {'hook':'sk1_2','clip':'attack','label':'王矛','immediate_effect_tick':0,'direct_damage_tick':0,'damage_command':8,'immediate_effect':'^1..9九个位置命令同步执行，不是9tick序列；同次函数里伤害/缓速。'},
      {'hook':'sk1_3','clip':'cast','label':'高踞','immediate_effect_tick':0,'direct_damage_tick':0,'damage_command':3,'immediate_effect':'漂浮与魔法伤害立即下发。'},
      {'hook':'sk1_4','clip':'strong','label':'失坠','immediate_effect_tick':0,'direct_damage_tick':0,'damage_command':5,'immediate_effect':'漂浮/虚弱与魔法伤害立即下发；后续跌落不是本函数延迟伤害命令。'},
      {'hook':'sk1_5','clip':'strong','label':'王座回绝','immediate_effect_tick':0,'direct_damage_tick':0,'damage_command':6,'immediate_effect':'立即击退式传送、魔法伤害、缓速。'},
      {'hook':'ult1_warn','clip':'laugh','label':'大招警告','immediate_effect_tick':0,'direct_damage_tick':None,'immediate_effect':'只发提示、粒子、音效；30tick后由 ult1 接管。'},
      {'hook':'ult1','clip':'strong','label':'大招结算','immediate_effect_tick':0,'direct_damage_tick':0,'warning_relative_direct_damage_tick':30,'damage_command':18,'fang_warmups':[4,8,12],'fang_damage_entity_updates':[12,16,20],'nominal_warning_relative_fang_ticks':[42,46,50],'immediate_effect':'立即18伤害和漂浮；尖牙另按自己的实体计时延迟伤害。'}
    ]
    result={'schema':'lucifer-animation-source-timing-v1','status':'SOURCE_AND_TIMING_VERIFIED_FINAL_ANIMATION_NOT_YET_ACCEPTED',
            'scope':'只读原游戏动画、现有项目函数与Java1.21.11字节码；写 scratch 分析数据，不操作 Blockbench、不修改技能代码、不写最终动作。',
            'source_payload':record(SOURCE),'source_audit':record(ROOT/'necromancer_animation_source_audit.json'),
            'original_animations':original,'legacy_sources':legacy,'required_clip_order':clips,'SKILLS':{s['hook']:s['clip'] for s in skills},'skills':skills,
            'ultimate_counter':{'initial':30,'charge_called_before_decrement':True,'extra_pulse_update_ordinals':[11,21],'resolve_update_ordinal':30,'warning_to_resolution_seconds_at_20tps':1.5,
                                'scope':'连续每tick正常执行 ult_tick 的序列；被驱魔状态暂停/跳过 tick 的情况需由主运行时验证。'},
            'fangs_engine_evidence':fangs,'function_sources':function_sources,
            'rig':{'gltf_actual_bones':35,'psa_tracks':37,'target_mossy_bones':22,'parents_from':'paired original mesh glTF; PSA BONENAMES ParentIndex placeholder is not hierarchy',
                   'missing_tracks':[{'index':35,'name':'Staff1'},{'index':36,'name':'crown1'}],
                   'missing_tracks_status':'仅保留原始PSA数据，不加入新骨骼。6clips的config标RemoveTracks=all；Stun未标，但两者仍不属于原35骨mesh。',
                   'mapping':source['target_mapping'],'coordinate_rules':source['coordinate_rules']},
            'retarget':{'world_rotation':'R_t_world(t)=R_s_world(t)*R_s_bind_world^-1*R_t_bind_world',
                        'local_rotation':'R_t_local(t)=R_t_parent_world(t)^-1*R_t_world(t)',
                        'local_translation':'p_t_local(t)=p_t_bind_local + R_t_parent_bind_world^-1*R_s_parent_bind_world*(p_s_local(t)-p_s_bind_local)',
                        'root_parent':'identity basis and transform',
                        'reference':'source PSA USkeleton refpose; target body input bind. Frozen JSON also retains exported glTF bind and differences.',
                        'initial_pose':'零动作参考输入严格回到目标bind；动画第0帧通常是原站姿，不能强制当bind。进入动画是否混合属于明确适配。',
                        'marker_translation':'六个网格marker在所有原动作里局部位置范围都是0；PSA参考误差最高约5e-6 px。保持目标偏移，源数值微差可保留。',
                        'full_SE3_world_delta_warning':'完整SE3对不同marker原点引入杠杆位移；当前7clip中与保留target offsets方法差异最大约0.00897239px，Walk/Stun右臂有轻微量化旋转时出现。',
                        'do_not_freeze_joint_translations':'J_* 动作含真实局部位移，尤其手部；仅复制旋转会破坏原姿态。',
                        'final_native_serialization':'解出最终local quaternion后转原生Euler顺序，连续解包，再减native rest Euler；此减法只是输出适配，不能替代旋转重定向。',
                        'validator_module':str(ROOT/'audit_animation_source.py'),
                        'reference_frame_api':'reference_frame(data, original_clip_name, source_seconds) -> source_local/world and target_local/world matrices; source sampled with linear position+slerp rotation, clamp at last sample.',
                        'zero_motion_target_world_matrix_max_error':audit['zero_motion_target_world_matrix_max_error']},
            'limits':['没有操作Blockbench，没有完成native动作的逐帧视口验证。','没有运行真实Minecraft；本机1.21.11 jar仅被只读核对。','七段原动作与GIF播放总长不同；按姿态/原秒数核对，不能宣称相同GIF帧号就是相同秒数。','GetHitFront只作为第七份参考原动作保存，不自动增加第九个交付clip。','本任务没有确认sound触发映射、游戏孤立display清理或构建；不能把来源数据审计PASS当检查点B通过。'],
            'primary_sources':source['primary_sources']}
    save('animation_timing.json',result)
    lines=['# 路西法动作来源、技能时序与重定向依据','',
      '当前只完成原动作读取与静态数学验证；最终动作、Blockbench逐帧外观和真实游戏时序尚未在本子任务验收。没有修改技能代码或模型。',
      '',f'完整源文件：`necromancer_animation_source.json`，SHA256 `{FROZEN}`，已冻结。',
      '7 段原始 PSA 共 19,721 个骨关键帧；35 根原 mesh 骨与 37 条 PSA track 均保存，另含 Mossy 22 骨的映射、局部/世界 bind 矩阵。',
      '', '## 8 段交付动作的来源', '', '|顺序|clip|来源|原始有效时长/s|接入要求|','|---:|---|---|---:|---|']
    for c in clips:
        lines.append(f"|{c['index']}|{c['clip']}|{c['source']}|{c['original_source_duration']:.6f}|{c['adaptation']}|")
    lines += ['', '上表时长是来源，不是已经制作完成的最终 clip 时长。GetHitFront 原数据另保存用于参考，不新增交付 clip。',
              '', 'StrongAttack 的原 SequenceLength=2.875s、RateScale=1.5，所以实际 PSA 播放时长为1.91666668s。PSA Time=1 是一帧单位；秒数必须用 frame/AnimRate。UModel props 的事件名称没有足够可靠的触发时间，不能据此编造原出手帧。',
              '', '## 技能生效时刻', '', '|钩子|建议clip|直接效果/伤害|对齐|','|---|---|---|---|']
    for s in skills:
        lines.append(f"|{s['hook']}|{s['clip']}|{s['immediate_effect']}|{'警告后30tick，即本hook0tick' if s['hook']=='ult1' else '本hook0tick'}|")
    lines += ['', '沿视线的 sk1_1、sk1_2 均用 attack。sk1_2 的9个采样位置同一tick执行，不能按1到9tick分段。普通招式没有现成蓄力延迟，动作需以释放/命中姿态开始，再恢复；不能为了保留动作前摇而改战斗函数。',
              '', '大招：ult_start 写入30并立即警告；每次 ult_tick 先 charge 再减1，因此额外 charge 脉冲在第11/21次更新，结算在第30次更新，即20TPS下1.5s。若束缚状态暂停推进，真实墙钟时间随运行时暂停；这里记录的是更新序号。',
              '', '尖牙：Java1.21.11映射与本机字节码证明伤害判断是 `--warmupDelayTicks == -8`。原罪 Warmup2,4,…16 对应第10,12,…24次尖牙实体更新；大招 Warmup4/8/12对应第12/16/20次更新。大招另有警告后第30tick的立即18伤害。实体生成的世界tick相位未在游戏实测，因此不要把更新序号伪装为录制测量。',
              '', '## 22 骨重定向', '', '所有公共 J_* 关节的 bind 框架几乎重合；名称确实是 J_L_Hip / J_L_Spine，不要虚构 J_Hip / J_Spine 别名。body/head/R_arm/R_leg/L_leg 几何marker的原点或朝向与Mossy不同；6个marker的局部位置在7段原动作中均恒定。',
              '', '旋转先算源世界旋转变化，再施加于目标bind：', '', '```text',
              'Rt_world(t) = Rs_world(t) · inverse(Rs_bind_world) · Rt_bind_world',
              'Rt_local(t) = inverse(Rt_parent_world(t)) · Rt_world(t)',
              'pt_local(t) = pt_bind_local + inverse(Rt_parent_bind_world) · Rs_parent_bind_world · (ps_local(t) - ps_bind_local)',
              '```', '', '根骨父变换取单位矩阵。位移保留目标骨长/marker偏移，再传源局部位移变化；不能冻结所有J_*位置，手部真实动作位移明显。也不要对不同marker直接套完整SE(3) world delta，它会用源/目标原点差产生额外杠杆位移；本次7段中实测差异最大约0.00897239px。',
              '', '源参考用PSA保存的USkeleton refpose，目标用body输入bind。完整JSON同时保存glTF mesh bind与两者差值。PSA参考与动画key经历的UModel镜像/根骨共轭流程不同，不能共用转换式。BONENAMES父索引是导出器占位；真实父级来自配套glTF。末两条 Staff1/crown1 不属于35骨mesh，不新增幽灵骨。',
              '', '最终只在序列化时转目标local quaternion为Blockbench实际Euler顺序、解包连续角度，再减目标native rest Euler。不能用源Euler直接叠到目标rest。动画第0帧是源站姿，不等于bind；进入动画的混合须单独记录。',
              '', '## 独立验证和边界', '',
              f"`necromancer_animation_source_audit.json`：原19721键float32字节逐字节吻合；Java位置矩阵误差{audit['java_position_matrix_max_error_px']}；旋转矩阵最大误差{audit['java_rotation_matrix_max_error']:.3g}；零动作回目标bind的世界矩阵误差{audit['zero_motion_target_world_matrix_max_error']:.3g}。",
              '', '`audit_animation_source.py` 的 `reference_frame()` 可只读提供任意原动作时间点的目标局部/世界矩阵，供后续native payload对比。适配过的腿部、持矛和出手裁首需带来源时间/骨排除表，不能拿其偏差冒充源转换错误。',
              '', '未操作Blockbench，未更改模型、游戏安装、战斗逻辑、其他怪或构建脚本。本证据不能替代动作并排图、游戏内换装/技能检查、清理测试或检查点B验收。',
              '', '## 原始实现依据', '']
    lines += ['- [UEViewer PSA结构](https://github.com/gildor2/UEViewer/blob/master/Exporters/Psk.h)',
              '- [UEViewer PSA导出镜像、帧与占位父级](https://github.com/gildor2/UEViewer/blob/master/Exporters/ExportPsk.cpp)',
              '- [UEViewer glTF坐标转换及根骨共轭](https://github.com/gildor2/UEViewer/blob/master/Exporters/ExportGLTF.cpp)',
              '- [UEViewer UE4动画解压、FixRotationKeys、播放率](https://github.com/gildor2/UEViewer/blob/master/Unreal/UnrealMesh/UnAnim4.cpp)',
              '- [Mojang 1.21.11官方client mappings](https://piston-data.mojang.com/v1/objects/031a68bebf55d824f66d6573d8c752f0e1bf232a/client.txt)',
              '', '具体本机路径、文件SHA、源码下载副本、字节码读证及每条技能函数快照hash见 `animation_timing.json`。']
    (ROOT/'animation_source_and_timing.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    assert sha(SOURCE)==FROZEN
    print(json.dumps({name:record(ROOT/name) for name in ['animation_timing.json','animation_source_and_timing.md']},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
