# Jungle Abomination 原始 shader 发光证据

结论：当前证据已闭合 **`_E` 蓝通道 → EmissiveB 额外粉色脉动项**，同时确证 **基础贴图 RGB × NaturalEmissive ≈ 0.6** 也直接加入材质发光。此前只看 cooked editor graph 得出的“B 通道未证实”限制，现在由该实例自己的 compiled shader 与 uniform/resource 表补足。没有修改模型、贴图、Java glow 配置、一阶段文件或游戏安装。

这不是 NatureArmor 公式迁移：本记录解析的是 `M_JungleAbomination` 的原始 inline shader resource，父材质 `Master_ModelMaterial` 只用于确认来源和共享 collection。提取脚本 `probe_shader.py` 只复用已有解析实现与原始 shader archive；反汇编调用系统 `d3dcompiler_47.dll!D3DDisassemble`。可运行 `python probe_shader.py`、`python finalize_audit.py` 重建本目录证据。

## 可复核的字节链

- M_JungleAbomination `.uexp`：207909 字节，SHA256 `1c9839a7161f990ea4591362ad04df53cad6b3a250572129a5c131aa6c3b1140`；准确 pak 条目与逐条 SHA1 记录在 `raw_manifest.json`。
- inline name map：5372–8848，96 名。SM5 四数组：vector 10698–11549（18）、scalar 11549–12368（24）、2D texture 12368–12478（5）、cube 12478–12482（0）。另一 SM4 资源 122383–124167 的同 1784 字节逐字节相同。
- SM5 编译说明起点 12568，明确 `Master_ModelMaterial`、`BLEND_Masked`、`TwoSided=1`；SinusEmissive、ConstantEmissive、EnchantmentMask、ExtraEmissive、TimedDissolve 均 True。完整原文在 JSON；没有仅凭实例开关名称判分支。
- 本实例 inline 记录中的 shader hash `a76883453ab15344d2a4b5c87f3268361971f605` 精确匹配原始 SM5 archive 条目。记录偏移 [24110, 24292, 40563, 40745]；FName `TBasePassPSFNoLightMapPolicy` 在 24186。原 shader `.bin`、裁切 `.dxbc` 和系统生成 `.asm` 均保留于 `M_JungleAbomination/`。
- `.bin` 前 196 字节为资源表。DXBC 声明 `CB3[24]`，恰好 18 vectors + 24 packed scalars / 4 = 24 float4。
- TextureMap token `0x03000003, 0x03000204, 0x03000405, 0x03000606, 0x03000807` 与 SamplerMap 确定五个纹理分别为 t3/s1…t7/s5。第 0 个 uniform 是 `Specular`，实例指定 `_E_M6`；第 2 个是 `Texture`，实例指定基础 `_M6`。因此 **t3/s1 = `_E`，t5/s3 = 基础贴图**。其他三个普通纹理的对象名不影响默认发光简式，此处不猜名称。
- collection StateId `8c7e6ed2fcf7474b800a708faccedb12` 在实例 `.uexp` 的 12498–12514，与原 `MPC_Dungeons` 完全一致。父材质 CollectionParameter 的 ParameterId 与 `DeathEmissive` 第 0 scalar 相同，默认 1。shader-specific UB 字段在 23905 起依次为 material `(index=3,bound=1)`、collection count=1、collection `(index=2,bound=1)`；实际指令用 `cb2[0].x`。

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

默认 pulse 范围为 5/3…7/3，B 项的 RGB 乘数范围约为 `[[16.666666666666668, 23.333333333333336], [0.30826670017242525, 0.43157338024139535], [16.207210432686264, 22.69009460576077]]`，再乘实际采样 S.b；红/蓝可大于 1，属于 HDR 材质值。NaturalEmissive 乘的是整个基础贴图 RGB，无 `_E` 掩码，因此 `_E.b=0` 的非黑基础纹理仍可贡献发光。

默认简式采用解析出的 Enchanted=0、ConstantEmissiveColor.rgb=0、ExtraEmissiveScalar=0、Flash Color.rgb=0、DesaturateStart=-50/Saturation=0、StatusColor.rgb=1、DeathEmissive=1、SelectionColor.rgb=0。运行时可覆盖这些值；它们并非“游戏永远不变”的声明。

## 原指令逐行

以下行号均指 `M_JungleAbomination/a76883453ab15344d2a4b5c87f3268361971f605.asm`；保留 full asm 供追踪寄存器覆盖、desaturation、enchantment 和最终 output。

```text
 79: sample_b_indexable(texture2d)(float,float,float,float) r3.xyzw, v2.xyxx, t3.xyzw, s1, cb0[137].y
 93: sample_b_indexable(texture2d)(float,float,float,float) r5.xyzw, v2.xyxx, t5.xyzw, s3, cb0[137].y
 99: mad r5.xyz, r5.xyzx, cb3[19].wwww, r6.xyzx
100: mul r6.xyz, r3.zzzz, cb3[9].xyzx
101: mul r6.xyz, r6.xyzx, cb3[20].wwww
102: mul r0.w, cb0[136].z, cb3[21].x
103: mul r0.w, r0.w, l(6.283185)
104: sincos r0.w, null, r0.w
105: div r0.w, r0.w, cb3[21].y
106: add r0.w, r0.w, cb3[21].z
107: max r0.w, r0.w, cb3[21].w
108: mul r7.xyz, r0.wwww, cb3[9].xyzx
109: mul r8.xyz, r3.wwww, cb3[11].xyzx
110: mad r6.xyz, r6.xyzx, r7.xyzx, r8.xyzx
111: add r6.xyz, r6.xyzx, cb3[12].xyzx
112: add r5.xyz, r5.xyzx, r6.xyzx
125: mad r3.yzw, r4.xxyz, r3.yyyy, r5.xxyz
126: mul r3.yzw, r3.yyzw, cb3[14].xxyz
127: mad r4.xyz, cb2[0].xxxx, r3.yzwy, cb3[15].xyzx
178: max r4.xyz, r4.xyzx, l(0.000000, 0.000000, 0.000000, 0.000000)
199: mad o0.xyz, cb0[139].xxxx, r3.xyzx, r4.xyzx
```

该 trace 中 `r3.z` 来自 `_E` B；`r3.w` 是 alpha，对应另一个 ConstantEmissive 分支，当前常量色为零。NaturalEmissive 加 Flash 后与 B 项合并，经 desaturation、附魔 G 项、StatusColor，再乘 collection 值、加 SelectionColor；默认参数使这些附加分支简化为上式。最终 emissive 寄存器在 `max(...,0)` 后直接加入 o0 RGB，没有在 [0,1] 截断；场景灯光和后处理另有各自路径。

## 参数与 packed uniform 对照

所有偏移为实例 `.uexp` 左闭右开字节范围。完整递归树、原始默认值、实例覆盖和资源表保存在 `jungle_material_evidence.json`。

| register | 原表达式 | 应用实例后的值 | 字节范围 |
| --- | --- | --- | --- |
| `cb3[0]` | SelectionColor | `[0.0, 0.0, 0.0, 1.0]` | 10702–10739 |
| `cb3[1]` | EnchantmentColor | `[0.01680699922144413, 0.0, 0.020289000123739243, 1.0]` | 10739–10776 |
| `cb3[2]` | EnchantmentColor.swizzle[0, 1, 2] | `[0.01680699922144413, 0.0, 0.020289000123739243, 0.0]` | 10776–10826 |
| `cb3[3]` | DissolveTextureSize | `[2.0, 2.0, 0.0, 1.0]` | 10826–10863 |
| `cb3[4]` | Flash Color | `[0.0, 0.0, 0.0, 1.0]` | 10863–10900 |
| `cb3[5]` | Flash Color.swizzle[0, 1, 2] | `[0.0, 0.0, 0.0, 0.0]` | 10900–10950 |
| `cb3[6]` | ExtraEmissiveColor | `[1.0, 0.06124600023031235, 0.9911019802093506, 1.0]` | 10950–10987 |
| `cb3[7]` | ExtraEmissiveColor.swizzle[0, 1, 2] | `[1.0, 0.06124600023031235, 0.9911019802093506, 0.0]` | 10987–11037 |
| `cb3[8]` | EmissiveBColor | `[1.0, 0.13600000739097595, 0.9861199855804443, 1.0]` | 11037–11074 |
| `cb3[9]` | EmissiveBColor.swizzle[0, 1, 2] | `[1.0, 0.13600000739097595, 0.9861199855804443, 0.0]` | 11074–11124 |
| `cb3[10]` | ConstantEmissiveColor | `[0.0, 0.0, 0.0, 1.0]` | 11124–11161 |
| `cb3[11]` | ConstantEmissiveColor.swizzle[0, 1, 2] | `[0.0, 0.0, 0.0, 0.0]` | 11161–11211 |
| `cb3[12]` | FoldedMath[2](ExtraEmissiveScalar,ExtraEmissiveColor.swizzle[0, 1, 2]) | `[0.0, 0.0, 0.0, 0.0]` | 11211–11299 |
| `cb3[13]` | StatusColor | `[1.0, 1.0, 1.0, 1.0]` | 11299–11336 |
| `cb3[14]` | StatusColor.swizzle[0, 1, 2] | `[1.0, 1.0, 1.0, 0.0]` | 11336–11386 |
| `cb3[15]` | SelectionColor.swizzle[0, 1, 2] | `[0.0, 0.0, 0.0, 0.0]` | 11386–11436 |
| `cb3[16]` | DissolveTextureSize.swizzle[0, 1, 2] | `[2.0, 2.0, 0.0, 0.0]` | 11436–11486 |
| `cb3[17]` | DissolveTextureSize.swizzle[0, 1, 2].swizzle[0, 1] | `[2.0, 2.0, 0.0, 0.0]` | 11486–11549 |
| `cb3[18].x` | EnchantedEye | `150.0` | 11553–11578 |
| `cb3[18].y` | Enchanted | `0.0` | 11578–11603 |
| `cb3[18].z` | FoldedMath[2](Enchanted,EnchantedEye) | `0.0` | 11603–11666 |
| `cb3[18].w` | DissolveTextureSize.swizzle[0] | `2.0` | 11666–11716 |
| `cb3[19].x` | FoldedMath[2](Enchanted,[3.0, 3.0, 3.0, 3.0]) | `0.0` | 11716–11779 |
| `cb3[19].y` | FoldedMath[2](Enchanted,[1.0, 1.0, 1.0, 1.0]) | `0.0` | 11779–11842 |
| `cb3[19].z` | FoldedMath[2](Enchanted,[8.0, 8.0, 8.0, 8.0]) | `0.0` | 11842–11905 |
| `cb3[19].w` | NaturalEmissive | `0.6000000238418579` | 11905–11930 |
| `cb3[20].x` | Flash Timestamp | `-100.0` | 11930–11955 |
| `cb3[20].y` | Flash Seconds | `0.10000000149011612` | 11955–11980 |
| `cb3[20].z` | ExtraEmissiveScalar | `0.0` | 11980–12005 |
| `cb3[20].w` | EmissiveBPower | `10.0` | 12005–12030 |
| `cb3[21].x` | EmissiveB_SinusTempo | `0.10000000149011612` | 12030–12055 |
| `cb3[21].y` | EmissiveB_SinusVariation | `3.0` | 12055–12080 |
| `cb3[21].z` | EmissiveB_SinusMin | `2.0` | 12080–12105 |
| `cb3[21].w` | EmissiveB_Max | `0.0` | 12105–12130 |
| `cb3[22].x` | DesaturateStart | `-50.0` | 12130–12155 |
| `cb3[22].y` | DesaturateDuration | `4.0` | 12155–12180 |
| `cb3[22].z` | Saturation | `0.0` | 12180–12205 |
| `cb3[22].w` | Metallic | `0.30000001192092896` | 12205–12230 |
| `cb3[23].x` | DissolveStart | `-50.0` | 12230–12255 |
| `cb3[23].y` | DissolveDuration | `4.0` | 12255–12280 |
| `cb3[23].z` | AlphaOverride | `1.0` | 12280–12305 |
| `cb3[23].w` | FoldedMath[0](AlphaOverride,[0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612]) | `1.1000000014901161` | 12305–12368 |

## 当前 Java 模型的明确边界

目前 `_E` 非零支持域分层有更强证据：它对应原材质 **B 通道额外粉色脉动项** 的空间支持域；R/G/B 的共同非零支持此前已独立核对。**它不是全部原材质发光范围**，因为 NaturalEmissive 的基础色项还作用于其余有颜色的可见表面。

当前 Java `light_emission=15` 分层没有表达原始 NaturalEmissive=0.6 基础自发光、上述颜色平方/HDR 强度和时间脉动。本文只完成证据，不改当前模型配置，也不将某个 Java 整数宣称为 0.6 的物理等价值。Blockbench 静态显示、Blender 几何/UV 对照、Java 游戏客户端表现仍是各自独立的验证边界。

两张纹理的属性导出都未序列化 SRGB；此分析没有新增纹理构造函数/SRV 格式捕获。上式故用 GPU 采样值表述，避免引入额外颜色空间假设。非零支持域在常规 sRGB 解码前后保持一致，但具体亮度不能把原图字节直接当 shader 线性采样值。

尚未实测：runtime material/collection 参数更新、精确时间相位、场景光照、曝光、Bloom、mip/filtering 以及 Minecraft 中最终亮度。完整原生 shader 公式的恢复不等于已复现原游戏最终画面。
