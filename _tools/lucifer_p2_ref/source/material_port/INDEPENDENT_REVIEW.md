# Jungle shader 独立复核

复核结论：**通过，但范围限定为该实例编译材质与其序列化默认/覆盖参数。** 原式确实包含独立的基础纹理发光项，因此当前 `_E` 非零遮罩只能表达额外粉色项的支持域，不能表示全部原始发光范围。没有采用 NatureArmor 的参数、纹理或公式。

## 独立检查的方法与字节证据

本复核直接重新读取 Jungle `.uexp` 和对应 shader `.bin`，用独立的小型 reader 解码名称表与四组 uniform，重新解压原始 SM5 archive 中唯一指定条目进行逐字节比较，并再次调用系统 D3DDisassemble 校验完整 ASM 一致。未运行原证据生成器，未提取新资产，未修改仓库、Blockbench、一阶段数据或原证据文件。

- Jungle `.uexp` SHA256：`1c9839a7161f990ea4591362ad04df53cad6b3a250572129a5c131aa6c3b1140`。
- shader：`a76883453ab15344d2a4b5c87f3268361971f605`；对应 archive 条目与 `.bin` 的 6286 字节完全一致。其哈希在 Jungle 原数据 24110、24292、40563、40745 四处存在；24186 的原始 FName 明确为 `TBasePassPSFNoLightMapPolicy`。
- inline 名称表 5372–8848，共 96 名；uniform 10698–12482，共 18 vector、24 scalar、5 texture、0 cube。第二资源 122383–124167 的 1784 字节完全一致。CB3[24] 与 18 个 vector 加 24/4 个 packed scalar 匹配。
- DXBC 从 `.bin` 偏移 196 开始；重新反汇编与现有 209 行 ASM 完全一致。ASM SHA256（文件原字节）：`76811ff6bf3c8cd1db74fab3a7f2a988155aba9d87376ea23d6e145267d3bf9a`。
- 资源表重新读取所得 TextureMap 为 `03000003 / 03000204 / 03000405 / 03000606 / 03000807`，SamplerMap 为 `03000101 / 03000302 / 03000503 / 03000704 / 03000905`。material UB=3 的成对资源索引将第 0 texture 绑定 t3/s1、第 2 texture 绑定 t5/s3；两项 uniform 名与该实例的对象覆盖分别为 Specular→`_E_M6`、Texture→`_M6`。
- 材质 collection 的原始 StateId 与已有 MPC_Dungeons 一致；该原文件哈希重新验证。第 0 scalar 为 DeathEmissive=1，父材质 ParameterId 匹配；原字节 23905 的 UB 记录为 material 3、单一 collection 2，与 ASM cb2[0].x 一致。

## 核心数据流

下列行号属于 `M_JungleAbomination/a76883453ab15344d2a4b5c87f3268361971f605.asm`。

| 证据 | 独立确认 |
| --- | --- |
| 79 | t3/s1 的完整 RGBA 写入 r3；后续使用 r3.z，确为 B 通道 |
| 93、99 | t5/s3 的 RGB 乘 cb3[19].w；scalar[7] 名为 NaturalEmissive，默认 0.6000000238418579，该实例未覆盖 |
| 100、101 | r6 = S.b × C × 10 |
| 102–107 | p = max(sin(cb0[136].z × tempo × 6.283185) / variation + min, floor)，实例/默认值分别约 0.1、3、2、0 |
| 108、110 | r7 = p × C，r6 = r6 × r7 + alpha分支，故产生逐通道 C²，不能只乘一次颜色 |
| 111、112 | ExtraEmissive 常量项后，与基础 RGB 项相加 |
| 113–127 | 默认 desaturation 系数为 0、Enchanted=0、StatusColor=1；collection 乘数默认 1，SelectionColor=0 |
| 178、199 | emission 仅下限钳制到 0 后加入输出；没有把该 HDR emission 上限钳制为 1。稍早的 mov_sat 钳制的是另一路 r3，不是保留 emission 的 r4 |

用 **GPU 纹理采样值** A=t5.rgb、S=t3.rgba，C=[1.0, 0.13600000739097595, 0.9861199855804443] 表述，已闭合的默认简式为：

```text
p(t) = max(sin(6.283185 * t * 0.10000000149011612) / 3 + 2, 0)
E_default(t) = 0.6000000238418579 * A + S.b * 10 * p(t) * (C ⊙ C)
```

这里 t 精确指 cb0[136].z。参数名 EmissiveB_Max 在指令中是 max 的下限参数，名称不能解释成输出上限。省略的默认项均已核对：Flash Color=0、ConstantEmissiveColor=0、ExtraEmissiveScalar=0、Enchanted=0、DesaturateStart=-50 与 Saturation=0、StatusColor=1、SelectionColor=0、DeathEmissive=1。静态开关已编入本 shader；这不是仅凭开关名称推断。

## 遮罩解释与尚未闭合的运行时问题

在这些默认值下 pulse 永远为正，C 的 RGB 也全非零，因此粉色附加项的空间支持由 S.b 非零决定。它不能替代总 emission 的支持：例如 S.b=0、A=[0.2, 0.4, 0.6] 时，基础 emission 仍为 [0.12000000476837158, 0.24000000953674316, 0.36000001430511475]。这是原指令可直接推出的反例，与 Minecraft 显示效果无关。

`_E` 各非零通道支持域相同是另一个图像核对结论；本复核所证明的真正 shader 输入是 **B**，并非任意 RGBA 非零。遮罩使用时仍需遵守真实几何 UV 与不透明度测试，不应把图集空白区域当可见表面。

本次未捕获运行时 constant buffer 或 material/collection 参数更新；默认值不代表战斗中永远不变。cb0[136].z 的实时时间、shader permutation 的实际 GPU 选择、曝光、Bloom、灯光与动态附魔/受伤/消散状态均未实测。公式适用于通过 opacity/discard 的表面；它没有复原整幅最终画面。

两纹理的颜色空间/SRV 读取方式尚未由本复核独立确定，故不把 PNG byte/255 当线性 shader 采样值。仅非零支持域的判断可避开常规 sRGB 解码的亮度差异。没有把 Java light_emission=15 或任何整数标为 NaturalEmissive=0.6 的等价实现，也没有创建新管线映射。

复核输入为 `JUNGLE_EMISSIVE_SHADER_AUDIT.md`、`jungle_material_evidence.json`、Jungle 原始包、该单一 shader 字节码与 ASM、已有 MPC_Dungeons 原数据。结果仅写入本报告；复核程序为 `independent_shader_review.py`。
