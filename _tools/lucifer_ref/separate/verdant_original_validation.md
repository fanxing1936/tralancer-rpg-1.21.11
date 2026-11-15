# Verdant Robe 原生保存独立回读核验

文件：`verdant_robe_original.bbmodel`
SHA-256：`9b925550ce92a88c28d8d8100d040fefaaca851c491aeae1a5af123cc6008354`

原始数据保真检查通过：**True**。直接解码四件原 glTF/bin 和原玩家骨架二进制 inverseBindMatrices，回读实际保存的 bbmodel；未以导入 JSON 替代原件真值，未操作 Blockbench。

实际保存：4 Mesh、128 顶点、64 三角形、38 骨、1 Armature。

| 部件 | 顶点/三角 | 坐标最大差（Java 像素） | UV 差（原图像素） | 三角顺序差 | 权重差 |
|---|---:|---:|---:|---:|---:|
| SageHat | 44/22 | 0 | 0 | 0 | 0 |
| R_Arm_EvocationRobe | 24/12 | 0 | 0 | 0 | 0 |
| MageRobe_Evocation | 36/18 | 0 | 0 | 0 | 0 |
| L_Arm_EvocationRobe | 24/12 | 0 | 0 | 0 | 0 |

反变换回原局部坐标的最大计算残差为 `4.440892098500626e-16` 米。原 component 非均匀缩放已逐点烘入坐标；独立 UE Euler 矩阵重算 component TRS 最大残差 `3.33066907387547e-16`。保留残差原值，不改记为 0。
JSON 包含全部 64 个三角形的原索引、原局部顶点、UV、native 面 UUID、实际保存坐标和纹理编号，另有 32 个原四边面 UV 覆盖表。
Mesh 父级差异 0；骨父级差异 0。原件是 StaticMesh，依据实际骨/socket 建立的每点权重 1 属于派生刚性绑定，未冒称原件原有蒙皮权重。

## 骨架与纹理

骨局部原点最大差 `0` Java 像素；Euler 矩阵相对归一化源四元数最大差 `3.828568698926949e-16`。
相对原十进制四元数的分量差 `3.935108000563403e-07`；累计世界原点差 `1.110223024625157e-14` Java 像素。原 glTF 四元数并非严格单位，Euler 表示转换不能声称逐值相同。
原 Albedo 与原 S 两张 PNG 内嵌字节均相等：**True**；RGBA 差异像素合计 **0**。逐文件 SHA-256 见 JSON。
S 贴图真实来源是 `EvocationRobe_Unique1/T_EvocationRobe_Unique1_S`，有本套 MI 引用依据；没有沿用 Root Rot 贴图或绿色发光向量。

## 原始 UV 使用

按原 UV 三角形与纹素方格的正面积交集统计；每原四边面两个三角形合并计一次，避免把对角线重复计数。另列纹素中心结果。黑色边界连通区仅标为 padding 候选，不当作已证实的材质语义。

| 类别 | 像素数 | 原件未覆盖 | 单原面覆盖 | 多原面共用 |
|---|---:|---:|---:|---:|
| transparent | 2808 | 2535 | 273 | 0 |
| opaque_nonblack | 1288 | 85 | 1174 | 29 |
| edge_connected_opaque_black_padding_candidate | 0 | 0 | 0 | 0 |
| isolated_opaque_black | 0 | 0 | 0 | 0 |
| effective_pattern_including_isolated_black | 1288 | 85 | 1174 | 29 |
| all_opaque | 1288 | 85 | 1174 | 29 |
| all_pixels | 4096 | 2620 | 1447 | 29 |

这些未用区和共用发生在原件本身，不是导入缺陷；忠实原件不能通过强行填满 atlas 或消除共用去改变原 UV。

## 核验范围

- 原始网格、UV、拓扑、刚性绑定和 PNG 保真；normals、tangents、UV1 逐值留在 sidecar，未声称 native importer 已消费。
- 装配依据原玩家 binary bind、帽子 socket 和其余直接骨挂点，保留原 BP component TRS；未序列化字段采用明确标注的标准缺省值。native Paperdoll 骨架赋值与参考图运行时姿势仍未证实。
- 本文件核验确认保存了白色 Emissive 参数、NaturalEmissive 和对应两张原纹理，及 native compiled 证明的 SpecularTexture=True。静态发光公式移植与主任务运行检查另有证据；本报告不凭 metadata 判定完整 Unreal 高光、粗糙度、Bloom、曝光或场景光照一致。
- 本次不操作 Blockbench，不测游戏运行、动作或生命周期。
