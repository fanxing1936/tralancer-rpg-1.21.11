# 原始 Root Rot：Blockbench 原生保存独立回读核验

文件：`root_rot_armor_original.bbmodel`
SHA-256：`8c0a2041aba3552c2006c5453ffe2c92aba8f9cfcca7e4648ae94bcc7404acfd`

此前 `40026a601c25c79a42c11912923b61a145948a90a88f4c60923484df8ccd1889` 已由主任务确认的材质保存更新替代：增加原 S 贴图及材质来源 metadata。本报告核验当前保存版本，不把合法版本变化列为模型错误。

直接解码原六部件 glTF/bin 及原玩家骨架 glTF/bin，结合明确列出的 armor_assembly.json，再逐项回读实际 bbmodel。未将导入 input JSON 当作源真值，未操作 Blockbench、未修改模型。

## 网格数据保真

实际保存为 6 Mesh、252 顶点、138 三角形、38 骨和 1 Armature。

| 部件 | 顶点/三角 | 坐标最大差（Java像素） | UV差（原图像素） | 三角顺序差 | 权重差 |
|---|---:|---:|---:|---:|---:|
| body | 94/58 | 0 | 0 | 0 | 0 |
| head | 70/36 | 0 | 0 | 0 | 0 |
| right_leg | 24/12 | 0 | 0 | 0 | 0 |
| left_arm | 20/10 | 0 | 0 | 0 | 0 |
| right_arm | 20/10 | 0 | 0 | 0 | 0 |
| left_leg | 24/12 | 0 | 0 | 0 | 0 |

反变换回原网格局部米制坐标后最大计算差为 `4.440892098500626e-16`；这是真实浮点计算残差，未改记为 0。原 UV0、三角形索引顺序/绕序、刚性权重、父级是否一致以表中及 JSON 实际值为准。
JSON 每部件的 source_to_native_triangle_face_mapping 逐一列出全部 138 个原三角形索引、原局部顶点、UV、native 面 UUID/顶点键/保存坐标/纹理编号；另含 69 个原四边面的 UV 覆盖表。
Mesh 父级差异 0；骨骼父级差异 0。
原件是 StaticMesh；每点绑定 1 到原 socket 所属骨是导入时依据挂点建立的刚性绑定，不是声称原 StaticMesh 本来拥有皮肤权重。

## 骨骼数值与表示

骨局部原点最大差：`0` Java像素。
Euler 矩阵相对归一化源四元数矩阵最大差：`3.828568698926949e-16`。
Euler 回算四元数相对原 glTF 四元数分量最大差：`3.935108000563403e-07`。
父子链累计世界原点最大差：`1.110223024625157e-14` Java像素。
glTF 的十进制四元数未必严格单位；native 存储 Euler。归一化/表示转换残差单列，不能宣称 raw quaternion 逐值一致。

## 贴图与原始 UV 覆盖

内嵌 Albedo 与 S 两张 PNG 字节均完全相等：`True`；合计 RGBA 差异像素：`0`。两张原/内嵌 PNG 的 SHA-256 逐项保存在 JSON textures 表。
覆盖采用原 UV 三角形与纹素方格的正面积交集；同一四边面的两个三角形合并计一次，避免把对角线误算复用。另报告纹素中心采样结果。覆盖限制在原 64×64 图幅，没有按未经证实的 wrap 扩展。

| 类别 | 像素数 | 原件未覆盖 | 单原面覆盖 | 多原面复用 |
|---|---:|---:|---:|---:|
| transparent | 719 | 411 | 286 | 22 |
| opaque_nonblack | 1562 | 218 | 1161 | 183 |
| edge_connected_opaque_black_padding_candidate | 1809 | 1800 | 0 | 9 |
| isolated_opaque_black | 6 | 6 | 0 | 0 |
| effective_pattern_including_isolated_black | 1568 | 224 | 1161 | 183 |
| all_opaque | 3377 | 2024 | 1161 | 192 |
| all_pixels | 4096 | 2435 | 1447 | 214 |

原始有效图案分类共 1568 像素，其中 224 像素在这六件原网格中未被覆盖，183 像素被多个原面共用。这些未用区与复用属于原件自身的数据，不是导入缺陷；忠实原件不得强行补全或消除。未用区域的坐标/连通分区与完整 69 面 UV 表均在 JSON。
左右靴、重复植物平面和 U=[63,64] 根须列的复用均有原网格直接依据。黑底边界连通分类只是 padding 候选，不能当作已证明材质语义。

## 条件装配与材质边界

- 装配矩阵从原玩家 binary inverse bind、原 socket、组件变换组成；省略的 native 属性默认值是明确条件，不是读取到的实测值。原 GearActor Paperdoll 赋值与参考图运行时姿势仍未证实。
- 本文件审计未执行 native runtime bind-deform；主任务的实际运行检查单独记录。
- 原 normals、tangents、UV1 与源逐值核对并留在 sidecar，未声称已被 native importer 消费。
- 当前文件已保存原 Albedo/S 贴图与材质来源 metadata。本次文件审计不判定实际渲染 shader 是否已完整生效，也不称原 Unreal 发光母材质、Bloom、曝光或光照已一致；用户要求的发光材质移植由主任务单独验证。
- .props 是序列化观察值；有效静态开关必须依据 native compiled permutation，不把 props 中 SpecularTexture 等数值自动当作有效开关。
