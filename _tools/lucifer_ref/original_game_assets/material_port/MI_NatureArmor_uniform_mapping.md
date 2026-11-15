# NatureArmor 原材质：UniformExpressions、纹理绑定与静态发光

状态：已从本机原始 cooked 材质和原始 SM5 shader 字节恢复本材质需要的参数树与发光运算。此记录确认静态默认材质公式；不宣称已复现游戏运行时参数修改、场景灯光、曝光、Bloom 或完整游戏画面。

本次只读原始资产并写分析文件，没有修改游戏安装、原始贴图、模型、UV、骨架或 Blockbench 工程。配套结果为 `MI_NatureArmor_uniforms.json`；可用上一级目录的 `parse_legacy_uniforms.py` 重复解析。

## 1. 直接读取范围与交叉核验

输入材质为 `/Game/Content_Season2/Actors/Equipment/Armor/NatureArmor/MI_NatureArmor`，父材质为 `M_MasterEquipment`。读取 `.uexp` 中嵌入式 shader resource，不根据材质参数名称猜发光公式。

| 结构 | `.uexp` 字节范围（左闭右开） | 结果 |
| --- | --- | --- |
| Inline name map | 3990–7054 | 82 名，FString + 4 字节 name hash |
| SM5 vector expression 数组 | 8734–9323 | 13 项 |
| SM5 scalar expression 数组 | 9323–11415 | 23 项 |
| SM5 2D texture expression 数组 | 11415–11525 | 5 项 |
| SM5 cube texture expression 数组 | 11525–11529 | 0 项 |
| SM4 同四个数组 | 85458–88253 | 与 SM5 的 2795 字节逐字节相同 |
| Collection StateId | 11545–11561 | 与 `MPC_Dungeons.StateId` 完全相同 |
| 编译描述 FString | 长度字段 11611，正文 11615 | 原文明确本 SM5 编译分支 |

递归表达式的每个节点均保存 start/end、类型、参数信息、默认值与子节点。参数信息结构为 FName 8 字节、Association 1 字节、Index 4 字节。`FoldedMath` 还含 1 字节运算符和 4 字节 ValueType。后续空数组及编译 flags 没有全部命名；不把这段尾部冒称完整反序列化。它不影响上述四数组的界定与逐字节 SM4 交叉核验。

Legacy expression 序列化的原始工具实现参考 [DarkStarSword 的提取器](https://github.com/DarkStarSword/3d-fixes/blob/master/extract_unreal_shaders.py)。本解析补上 UE4.22 参数信息与本资产实际出现的 ScalarParameter、Floor、Min 等结构，并用实际字节边界验证；没有套用 UE5 的 frozen-memory layout。

原编译描述的有效开关为 ConstantEmissive=True、FlashBehavior=True、EnchantmentMask=True、Desaturation=False、SpecularTexture=False、ConstantSpecular=False。实例属性表的开关值若 `bOverride=false`，不能单独用作最终编译分支证据。

## 2. 材料缓冲区对应关系

本 SM5 pixel shader 标识为 `762fe3b6f361f38e14e6ec6c1b4e1f6f8a25d76c`。反汇编声明 `CB3[19]`。13 个 float4 vector 后接 23 个按四分量打包的 scalar，恰为 `13 + ceil(23/4) = 19` 个 float4。以下布局来自 legacy serializer、编译资源表及指令的共同核对；没有声称抓取过运行时 GPU 常量缓冲区。

| 输入 | 缓冲位置 | 来源/default 或实例 override |
| --- | --- | --- |
| Flash Color.rgb | cb3[2].xyz | 默认 [1,0,0] |
| Emissive.rgb | cb3[4].xyz | MI override [0.693310022354126,8,0] |
| EnchantmentColor.rgb | cb3[6].xyz | MI override [0,0.23574799299240112,1] |
| SelectionColor.rgb | cb3[7].xyz | 默认 [0,0,0] |
| StatusColor.rgb | cb3[9].xyz | 默认值保存在 JSON；只乘 BaseColor |
| Flash Timestamp | cb3[13].x，scalar 0 | -100 |
| Flash Seconds | cb3[13].y，scalar 1 | 0.10000000149011612 |
| EmissivePower | cb3[13].z，scalar 2 | 1 |
| NaturalEmissive | cb3[13].w，scalar 3 | MI override 0.699999988079071 |
| Power | cb3[14].x，scalar 4 | 0 |
| 附魔噪声权重 3Q | cb3[15].w，scalar 11 | 默认 0 |
| 附魔噪声权重 Q | cb3[16].x，scalar 12 | 默认 0 |
| EnchantmentAdd | cb3[16].y，scalar 13 | 0 |
| 附魔总权重 8Q | cb3[16].z，scalar 14 | 默认 0 |
| DeathEmissive | cb2[0].x | `MPC_Dungeons.ScalarParameters[0]`，默认 1 |

其中 `Q = min(4 * floor((Power + 1) / 4), 9) / 9`。JSON 保存所有 13 vector、23 scalar 的完整树、字节范围、静态值及缓冲位置。运算类型 0/1/2/3 对应加/减/乘/除；公开工具的枚举交叉依据为 [ArkServerApi 主仓库的 EFoldedMathOperation](https://github.com/ArkServerApi/AseApi/blob/master/version/Core/Public/API/ARK/Enums.h)，这是另一 UE4 游戏 API 的原始声明而非 Minecraft Dungeons 源代码，故只用于 enum 交叉检查。使用本材质的有限值计算，无须对除零、NaN 等非默认状态作假设。

Collection 的 StateId 在材质资源与 `MPC_Dungeons` 中相同；DeathEmissive 的 ParameterId 也由父材质 CollectionParameter 关联。默认值不意味着运行时不能更新。

## 3. 纹理绑定证据

Shader `.bin` 前 196 字节为 UE 资源表，随后才是 `DXBC`。材料使用 resource table 3。TextureMap 的五个 token 为：

`0x03000003, 0x03000204, 0x03000405, 0x03000606, 0x03000807`。

对应 buffer 3 的资源索引 0/2/4/6/8 绑定 t3/t4/t5/t6/t7。SamplerMap 对应 token 为 `0x03000101, 0x03000302, 0x03000503, 0x03000704, 0x03000905`，即交错的 sampler 资源 1/3/5/7/9 绑定 s1/s2/s3/s4/s5。资源表字段的用途见 [Epic FShaderResourceTable](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/RHI/FShaderResourceTable)，entry 的组成见 [Epic FRHIResourceTableEntry](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/RHI/FRHIResourceTableEntry)。本 token 的高 8、中 16、低 8 位分别解为 buffer/resource/bind，完整原数值同时保留以供复核。

| Uniform2DTextureExpressions 序号 | 原表达式 | SM5 register | 本实例实际纹理 |
| --- | --- | --- | --- |
| 0 | TextureParameter Specular，默认 texture index 1 | t3 / s1 | T_NatureArmor_S |
| 1 | TextureParameter Albedo，默认 texture index 0 | t4 / s2 | T_NatureArmor |
| 2 | Texture，texture index 2 | t5 / s3 | 父材质引用的附魔滚动噪声；此记录不为其源对象另作未经验证的命名 |
| 3 | Texture，texture index 5 | t6 / s4 | 父材质普通纹理引用；用于裁剪相关分支 |
| 4 | Texture，texture index 4 | t7 / s5 | 父材质普通纹理引用；用于 dissolve 分支 |

前两项由原材质实例 TextureParameterValues 解析到完整原始对象路径，而不是按文件名习惯推断。t3 采样写入 `r1.zw` 且使用 `t3.xwyz` swizzle，所以 r1.z 是辅助图 G，r1.w 是辅助图 B；接着 r1.w 乘 cb3[4].rgb，再乘 cb3[13].z。B 通道确用于基础发光，G 通道乘附魔发光。t4 RGB 乘 NaturalEmissive 后加入发光。

## 4. 颜色空间的证据与边界

原 T_NatureArmor 与 T_NatureArmor_S 的纹理属性均为 `CompressionSettings=TC_EditorIcon`、`LODGroup=TEXTUREGROUP_Pixels2D`，都没有序列化 SRGB。两者是常规 Texture2D；不能因 `_S` 后缀或“辅助图”用途就强行解释为线性。

[CUE4Parse 主仓库 UTexture.Deserialize](https://github.com/FabianFG/CUE4Parse/blob/master/CUE4Parse/UE4/Assets/Exports/Texture/UTexture.cs) 明确使用 `SRGB = GetOrDefault(nameof(SRGB), true);`。据此，两图均按标准 UE 的省略属性默认值 true 处理：采样 RGB 进入线性空间，alpha 保持线性。该结论有原始解析器实现支持；本次没有直接读取 Minecraft Dungeons 原生 UTexture 构造函数，也没有运行游戏捕获 SRV 格式，不将后者称为已证实。

[Microsoft DXGI_FORMAT](https://learn.microsoft.com/en-us/windows/win32/api/dxgiformat/ne-dxgiformat-dxgi_format) 说明 sRGB 格式的 RGB 使用 sRGB 编码而 alpha 为 gamma 1.0。离线求值对 RGB 使用分段转换：`c/12.92`（c≤0.04045），否则 `((c+0.055)/1.055)^2.4`，c 为 byte/255。Emissive 的 LinearColor 参数已经在线性空间，尤其绿色 8.0 必须保留 HDR 浮点值，不能再对它作 sRGB 解码，也不能量化为 8 位 PNG。

## 5. 发光公式与静态默认分支

令 A 为线性 albedo.rgb，S 为线性辅助图.rgb，C 为 Emissive.rgb，F 为 Flash Color.rgb，D 为 DeathEmissive。把上述 register 代回原指令，材质发光在场景曝光前为：

```text
flash = max(1 - (GameTime - FlashTimestamp) / FlashSeconds, 0)
noise1 = sample(t5, uv + RealTime * [0.6,-0.05]).r
noise2 = sample(t5, uv * 0.45 + RealTime * [0.2,0.1]).r
enchantment = (noise1*(3Q) * noise2*Q + EnchantmentAdd)
              * EnchantmentColor.rgb * (8Q) * S.g
E = (S.b*C*EmissivePower + A*NaturalEmissive
     + enchantment + F*flash) * D + SelectionColor.rgb
```

原始默认 Power=0，所以 Q=0，附魔项消失；EnchantmentAdd 也为 0。GameTime≥0 且 FlashTimestamp=-100 时，flash=0。SelectionColor.rgb=0、DeathEmissive=1。应用 MI_NatureArmor 的两项发光覆盖后得到：

```text
E_static = linear(T_NatureArmor_S).b * [0.693310022354126, 8, 0]
         + linear(T_NatureArmor).rgb * 0.699999988079071
```

这是“原始 cooked 默认状态 + 原 MI 参数”的静态移植公式。普通 albedo 仍承担 BaseColor；它通过 NaturalEmissive 另贡献发光，不能只留下辅助图亮点。E_static 不作 [0,1] 截断，源贴图、UV 和 alpha 不变。本阶段不需要制作 flash、附魔、dissolve 动画；完整表达式和这些运行时边界仍保留。

这里的静态发光还不等于游戏最终屏幕亮度。原 BasePass 随后参与曝光、雾、后处理等计算；Blockbench 或 Java 预览的显示管线不自动等同于 UE。
