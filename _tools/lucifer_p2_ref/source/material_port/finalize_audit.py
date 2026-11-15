"""Create a reviewable Jungle Abomination shader-evidence bundle only."""
from pathlib import Path
import hashlib, json, math, struct
import probe_shader as probe

OUT = Path(__file__).resolve().parent
OLD = Path(r'D:\agent\codex\TRA\work\lucifer_original')
SHADER = 'a76883453ab15344d2a4b5c87f3268361971f605'

def props(obj): return {p['name']: p['value'] for p in obj['properties']}
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    raw_info=json.loads((OUT/'raw_material_offsets.json').read_text())['materials'][0]
    data=Path(raw_info['raw_uexp']).read_bytes()
    folder=OUT/'M_JungleAbomination'
    name_map=json.loads((folder/'inline_names.json').read_text())
    names=name_map['names']
    env=probe.reader_env(data,names)
    candidates=json.loads((folder/'uniform_candidates.json').read_text())
    assert len(candidates)==2
    a,b=candidates
    assert data[a['start']:a['end']]==data[b['start']:b['end']]
    assert [a[k]['count'] for k in ('UniformVectorExpressions','UniformScalarExpressions','Uniform2DTextureExpressions','UniformCubeTextureExpressions')]==[18,24,5,0]
    parsed=json.loads((OUT/'M_JungleAbomination.parsed.json').read_text())
    override={}
    for field in ('ScalarParameterValues','VectorParameterValues','TextureParameterValues'):
        for item in props(parsed['exports'][0])[field]['items']:
            item=props(item)
            override[props(item['ParameterInfo'])['Name']]=item['ParameterValue']
    vectors=a['UniformVectorExpressions']['expressions']
    scalars=a['UniformScalarExpressions']['expressions']
    slots=[dict(buffer=f'cb3[{i}]',expression=env['summary_expr'](e),value=env['evaluate'](e,override),start=e['start'],end=e['end']) for i,e in enumerate(vectors)]
    slots += [dict(buffer=f'cb3[{18+i//4}].{"xyzw"[i%4]}',expression=env['summary_expr'](e),value=env['evaluate'](e,override)[0],start=e['start'],end=e['end']) for i,e in enumerate(scalars)]
    code=(folder/(SHADER+'.bin')).read_bytes()
    table=env['resource_table'](code)
    assert [(r['resource_index'],r['bind_index']) for r in table['TextureMap']['decoded_material_entries']]==[(0,3),(2,4),(4,5),(6,6),(8,7)]
    assert [(r['resource_index'],r['bind_index']) for r in table['SamplerMap']['decoded_material_entries']]==[(1,1),(3,2),(5,3),(7,4),(9,5)]
    asm=(folder/(SHADER+'.asm')).read_text()
    lines=asm.splitlines()
    def line(text):
        matches=[i+1 for i,s in enumerate(lines) if s==text]
        assert len(matches)==1,(text,matches)
        return matches[0]
    important = {
      'specular_sample': 'sample_b_indexable(texture2d)(float,float,float,float) r3.xyzw, v2.xyxx, t3.xyzw, s1, cb0[137].y',
      'albedo_sample': 'sample_b_indexable(texture2d)(float,float,float,float) r5.xyzw, v2.xyxx, t5.xyzw, s3, cb0[137].y',
      'natural_emissive_add_flash': 'mad r5.xyz, r5.xyzx, cb3[19].wwww, r6.xyzx',
      'B_times_color': 'mul r6.xyz, r3.zzzz, cb3[9].xyzx',
      'B_times_power': 'mul r6.xyz, r6.xyzx, cb3[20].wwww',
      'time_times_tempo': 'mul r0.w, cb0[136].z, cb3[21].x',
      'radians': 'mul r0.w, r0.w, l(6.283185)',
      'sine': 'sincos r0.w, null, r0.w',
      'divide_variation': 'div r0.w, r0.w, cb3[21].y',
      'add_min': 'add r0.w, r0.w, cb3[21].z',
      'lower_clamp_named_Max': 'max r0.w, r0.w, cb3[21].w',
      'pulse_times_color': 'mul r7.xyz, r0.wwww, cb3[9].xyzx',
      'constant_emissive_alpha': 'mul r8.xyz, r3.wwww, cb3[11].xyzx',
      'B_product_add_constant': 'mad r6.xyz, r6.xyzx, r7.xyzx, r8.xyzx',
      'add_extra': 'add r6.xyz, r6.xyzx, cb3[12].xyzx',
      'add_to_natural': 'add r5.xyz, r5.xyzx, r6.xyzx',
      'add_enchantment_G': 'mad r3.yzw, r4.xxyz, r3.yyyy, r5.xxyz',
      'status_color': 'mul r3.yzw, r3.yyzw, cb3[14].xxyz',
      'collection_and_selection': 'mad r4.xyz, cb2[0].xxxx, r3.yzwy, cb3[15].xyzx',
      'nonnegative_emission': 'max r4.xyz, r4.xyzx, l(0.000000, 0.000000, 0.000000, 0.000000)',
      'output': 'mad o0.xyz, cb0[139].xxxx, r3.xyzx, r4.xyzx',
    }
    trace={k:dict(line=line(v),instruction=v) for k,v in important.items()}
    matches=json.loads((folder/'matches.json').read_text())['matches']
    selected=next(r for r in matches if r['hash']==SHADER)
    shader_type_offset=selected['material_offsets'][0]+76
    ti,tn=struct.unpack_from('<ii',data,shader_type_offset)
    assert names[ti]=='TBasePassPSFNoLightMapPolicy' and tn==0
    archive=probe.ARCHIVE
    debug=[]
    for c in candidates:
        pos=data.index(b'Compiling Master_ModelMaterial:',c['end'])
        length=struct.unpack_from('<i',data,pos-4)[0]
        debug.append(dict(length_offset=pos-4,string_offset=pos,length=length,text=data[pos:pos+length-1].decode('ascii')))
    assert 'PCD3D_SM5' in debug[0]['text'] and 'PCD3D_SM4' in debug[1]['text']
    mpc_path=OLD/'MPC_Dungeons.parsed.json'
    mpc=props(json.loads(mpc_path.read_text())['exports'][0])
    death=props(mpc['ScalarParameters']['items'][0])
    stateid=mpc['StateId']
    collection_offset=data.index(bytes.fromhex(stateid),a['end'],debug[0]['length_offset'])
    master=json.loads((OUT/'Master_ModelMaterial.parsed.json').read_text())
    collection=next(e for e in master['exports'] if e['name']=='MaterialExpressionCollectionParameter_0')
    cp=props(collection)
    assert cp['ParameterName']==death['ParameterName']=='DeathEmissive'
    assert cp['ParameterId']==death['Id']
    # Exact serialized material/collection UB binding fields of this FMaterialShader.
    assert struct.unpack_from('<HIiHI',data,23905)==(3,1,1,2,1)
    p=override['EmissiveBPower'];c=override['EmissiveBColor'][:3]
    color_squared=[v*v for v in c]
    lo,hi=2-1/3,2+1/3
    result={
      'status':'B channel and NaturalEmissive formula closed by this instance compiled shader; no model changes',
      'scope':'Original cooked default parameters; runtime parameter updates and game display pipeline not captured',
      'source_archive':dict(path=str(archive),bytes=archive.stat().st_size,sha256=sha(archive)),
      'raw_uexp_sha256':sha(Path(raw_info['raw_uexp'])),
      'inline_name_map':name_map,
      'uniform_sets':candidates,'uniform_bytes_equal':True,'uniform_bytes':a['end']-a['start'],
      'compiler_descriptions':debug,'instance_overrides':override,'material_slots':slots,
      'shader':dict(selected,shader_type_offset=shader_type_offset,shader_type=names[ti],bin_sha256=sha(folder/(SHADER+'.bin')),dxbc_sha256=sha(folder/(SHADER+'.dxbc')),asm_sha256=sha(folder/(SHADER+'.asm'))),
      'resource_table':table,
      'collection':dict(source=str(mpc_path),source_sha256=sha(mpc_path),StateId=stateid,stateid_uexp_offset=collection_offset,parameter=death,parent_expression=collection,binding_uexp_offset=23905,material_ub=3,collection_ub=2),
      'instruction_trace':trace,
      'default_formula':{
        'A':'GPU sample of Texture RGB, t5/s3; not raw PNG bytes',
        'S':'GPU sample of Specular RGBA, t3/s1; not raw PNG bytes',
        't':'View uniform cb0[136].z, the time input used by the shader; no runtime buffer captured',
        'pulse':'max(sin(6.283185307179586*t*0.10000000149011612)/3 + 2, 0)',
        'emission':'0.6000000238418579*A + S.b*10*pulse*(C*C)',
        'C':c,'C_squared':color_squared,'pulse_range':[lo,hi],
        'B_RGB_multiplier_range':[[p*lo*v,p*hi*v] for v in color_squared],
        'conditions':'Enchanted=0; ConstantEmissiveColor.rgb=0; ExtraEmissiveScalar=0; Flash Color.rgb=0; DesaturateStart=-50 with zero Saturation; StatusColor.rgb=1; DeathEmissive=1; SelectionColor.rgb=0',
      },
      'limitations':[
        'All formulas describe shader sample values and serialized defaults, not a live GPU/game capture.',
        'SRGB is absent in both texture property exports. No new SRV/texture-constructor inspection was performed; equations intentionally use sampled values, not byte/255.',
        'Nonzero B support is the local extra pink pulsation support, not the full emission support: NaturalEmissive contributes wherever sampled base RGB is nonzero and fragments survive alpha/dissolve.',
        'Time pulse/HDR/color-squared/natural term are not reproduced by current Java light_emission=15 mask split.',
        'No Java integer light_emission value is asserted physically equivalent to NaturalEmissive=0.6.',
        'Runtime parameters, scene lighting, exposure, bloom, mip/filtering and exact temporal phase are not captured.',
      ]
    }
    (OUT/'jungle_material_evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    rows='\n'.join(f"| `{s['buffer']}` | {s['expression']} | `{s['value']}` | {s['start']}–{s['end']} |" for s in slots)
    instructions='\n'.join(f"{v['line']:3}: {v['instruction']}" for v in trace.values())
    report=f'''# Jungle Abomination 原始 shader 发光证据

结论：当前证据已闭合 **`_E` 蓝通道 → EmissiveB 额外粉色脉动项**，同时确证 **基础贴图 RGB × NaturalEmissive ≈ 0.6** 也直接加入材质发光。此前只看 cooked editor graph 得出的“B 通道未证实”限制，现在由该实例自己的 compiled shader 与 uniform/resource 表补足。没有修改模型、贴图、Java glow 配置、一阶段文件或游戏安装。

这不是 NatureArmor 公式迁移：本记录解析的是 `M_JungleAbomination` 的原始 inline shader resource，父材质 `Master_ModelMaterial` 只用于确认来源和共享 collection。提取脚本 `probe_shader.py` 只复用已有解析实现与原始 shader archive；反汇编调用系统 `d3dcompiler_47.dll!D3DDisassemble`。可运行 `python probe_shader.py`、`python finalize_audit.py` 重建本目录证据。

## 可复核的字节链

- M_JungleAbomination `.uexp`：{len(data)} 字节，SHA256 `{sha(Path(raw_info['raw_uexp']))}`；准确 pak 条目与逐条 SHA1 记录在 `raw_manifest.json`。
- inline name map：{name_map['start']}–{name_map['end']}，96 名。SM5 四数组：vector 10698–11549（18）、scalar 11549–12368（24）、2D texture 12368–12478（5）、cube 12478–12482（0）。另一 SM4 资源 122383–124167 的同 1784 字节逐字节相同。
- SM5 编译说明起点 {debug[0]['string_offset']}，明确 `Master_ModelMaterial`、`BLEND_Masked`、`TwoSided=1`；SinusEmissive、ConstantEmissive、EnchantmentMask、ExtraEmissive、TimedDissolve 均 True。完整原文在 JSON；没有仅凭实例开关名称判分支。
- 本实例 inline 记录中的 shader hash `{SHADER}` 精确匹配原始 SM5 archive 条目。记录偏移 {selected['material_offsets']}；FName `{names[ti]}` 在 {shader_type_offset}。原 shader `.bin`、裁切 `.dxbc` 和系统生成 `.asm` 均保留于 `M_JungleAbomination/`。
- `.bin` 前 196 字节为资源表。DXBC 声明 `CB3[24]`，恰好 18 vectors + 24 packed scalars / 4 = 24 float4。
- TextureMap token `0x03000003, 0x03000204, 0x03000405, 0x03000606, 0x03000807` 与 SamplerMap 确定五个纹理分别为 t3/s1…t7/s5。第 0 个 uniform 是 `Specular`，实例指定 `_E_M6`；第 2 个是 `Texture`，实例指定基础 `_M6`。因此 **t3/s1 = `_E`，t5/s3 = 基础贴图**。其他三个普通纹理的对象名不影响默认发光简式，此处不猜名称。
- collection StateId `{stateid}` 在实例 `.uexp` 的 {collection_offset}–{collection_offset+16}，与原 `MPC_Dungeons` 完全一致。父材质 CollectionParameter 的 ParameterId 与 `DeathEmissive` 第 0 scalar 相同，默认 1。shader-specific UB 字段在 23905 起依次为 material `(index=3,bound=1)`、collection count=1、collection `(index=2,bound=1)`；实际指令用 `cb2[0].x`。

## 已证实的默认分支

令 A 为 t5/s3 的 GPU 采样 RGB，S 为 t3/s1 的 GPU 采样 RGBA，C 为实例 EmissiveBColor.rgb。采样值指进入 shader 的浮点颜色，不能未经颜色空间处理便拿 PNG 的 byte/255 代替。

```text
C = [1, 0.13600000739097595, 0.9861199855804443]
pulse(t) = max(sin(2π × t × 0.10000000149011612) / 3 + 2, 0)
E_default(t) = A × 0.6000000238418579
             + S.b × 10 × pulse(t) × (C ⊙ C)
```

`t` 在原指令中精确是 View uniform `cb0[136].z` 的时间输入；这里未抓取运行时缓冲区、启动时间或当前相位。式中的 `2π` 是反汇编显示 `6.283185` 对应的 float 常量。时间若按标准 View 的秒值提供，周期约 10 秒；此记录不把具体运行时相位当已测结果。

`C ⊙ C` 是逐通道平方，有直接指令证据：B 先乘 C 和 Power，另一侧 pulse 又乘 C，随后二者相乘。不能简化成只乘一次 C。名为 `EmissiveB_Max` 的参数在这里参与 GPU **max** 运算，是 pulse 的下限；默认 0。

默认 pulse 范围为 5/3…7/3，B 项的 RGB 乘数范围约为 `{result['default_formula']['B_RGB_multiplier_range']}`，再乘实际采样 S.b；红/蓝可大于 1，属于 HDR 材质值。NaturalEmissive 乘的是整个基础贴图 RGB，无 `_E` 掩码，因此 `_E.b=0` 的非黑基础纹理仍可贡献发光。

默认简式采用解析出的 Enchanted=0、ConstantEmissiveColor.rgb=0、ExtraEmissiveScalar=0、Flash Color.rgb=0、DesaturateStart=-50/Saturation=0、StatusColor.rgb=1、DeathEmissive=1、SelectionColor.rgb=0。运行时可覆盖这些值；它们并非“游戏永远不变”的声明。

## 原指令逐行

以下行号均指 `M_JungleAbomination/{SHADER}.asm`；保留 full asm 供追踪寄存器覆盖、desaturation、enchantment 和最终 output。

```text
{instructions}
```

该 trace 中 `r3.z` 来自 `_E` B；`r3.w` 是 alpha，对应另一个 ConstantEmissive 分支，当前常量色为零。NaturalEmissive 加 Flash 后与 B 项合并，经 desaturation、附魔 G 项、StatusColor，再乘 collection 值、加 SelectionColor；默认参数使这些附加分支简化为上式。最终 emissive 寄存器在 `max(...,0)` 后直接加入 o0 RGB，没有在 [0,1] 截断；场景灯光和后处理另有各自路径。

## 参数与 packed uniform 对照

所有偏移为实例 `.uexp` 左闭右开字节范围。完整递归树、原始默认值、实例覆盖和资源表保存在 `jungle_material_evidence.json`。

| register | 原表达式 | 应用实例后的值 | 字节范围 |
| --- | --- | --- | --- |
{rows}

## 当前 Java 模型的明确边界

目前 `_E` 非零支持域分层有更强证据：它对应原材质 **B 通道额外粉色脉动项** 的空间支持域；R/G/B 的共同非零支持此前已独立核对。**它不是全部原材质发光范围**，因为 NaturalEmissive 的基础色项还作用于其余有颜色的可见表面。

当前 Java `light_emission=15` 分层没有表达原始 NaturalEmissive=0.6 基础自发光、上述颜色平方/HDR 强度和时间脉动。本文只完成证据，不改当前模型配置，也不将某个 Java 整数宣称为 0.6 的物理等价值。Blockbench 静态显示、Blender 几何/UV 对照、Java 游戏客户端表现仍是各自独立的验证边界。

两张纹理的属性导出都未序列化 SRGB；此分析没有新增纹理构造函数/SRV 格式捕获。上式故用 GPU 采样值表述，避免引入额外颜色空间假设。非零支持域在常规 sRGB 解码前后保持一致，但具体亮度不能把原图字节直接当 shader 线性采样值。

尚未实测：runtime material/collection 参数更新、精确时间相位、场景光照、曝光、Bloom、mip/filtering 以及 Minecraft 中最终亮度。完整原生 shader 公式的恢复不等于已复现原游戏最终画面。
'''
    (OUT/'JUNGLE_EMISSIVE_SHADER_AUDIT.md').write_text(report,encoding='utf-8')
    manifest=[]
    for path in sorted(OUT.rglob('*')):
        if path.is_file() and path.name!='evidence_manifest.json' and '__pycache__' not in path.parts:
            manifest.append(dict(path=str(path.relative_to(OUT)),bytes=path.stat().st_size,sha256=sha(path)))
    (OUT/'evidence_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({'report':str(OUT/'JUNGLE_EMISSIVE_SHADER_AUDIT.md'),'uniform_entries':len(slots),'shader':SHADER,'trace_lines':trace,'files':len(manifest)},ensure_ascii=False))

if __name__=='__main__': main()
