# Root Rot / NatureArmor 原始网格核验

只读原始导出几何与纹理，未改模型、Blockbench、游戏或正式资产。结论：整套原几何与 UV 不能逐值无损转换为纯 cuboid。此报告坐标均为 UModel glTF 局部米制坐标；已引用原组件/socket 属性证据，但未擅自假定未序列化值或应用装配变换。

## 资产身份

Root Rot 对应 NatureArmor。BP_NatureArmor 明确引用 NatureArmor 头盔及 SproutArmor 的躯干、双臂、双腿，并将材质覆盖为 MI_NatureArmor；这里的复用不是目测推断。此前 SproutArmor_Unique1 是另一套装备，停止使用它的颜色作 Root Rot 对照。

## 六部件几何

| 部件 | 导出顶点 | 三角形 | 四边形面 | 几何连通分组 | 分组判定 |
|---|---:|---:|---:|---:|---|
| helmet | 70 | 36 | 18 | 8 | {'open_cuboid_surface': 1, 'closed_cuboid': 1, 'rectangular_plane': 5, 'not_a_single_cuboid': 1} |
| body | 94 | 58 | 29 | 13 | {'rectangular_plane': 1, 'not_a_single_cuboid': 12} |
| left_arm | 20 | 10 | 5 | 1 | {'open_cuboid_surface': 1} |
| right_arm | 20 | 10 | 5 | 1 | {'open_cuboid_surface': 1} |
| left_leg | 24 | 12 | 6 | 1 | {'closed_cuboid': 1} |
| right_leg | 24 | 12 | 6 | 1 | {'closed_cuboid': 1} |

原始 positions/normals/tangents/UV0/UV1/三角形索引，以及每个三角形对、边界顶点、UV0 原始 64 像素坐标、绕序法线、边长、平面误差及矩形判定均完整保存于 JSON。几何连通按 2e-6 米误差判断；它是数值容差，不是“数学上完全无误差”的承诺。分组中的 not_a_single_cuboid 不等于所有面有缺陷：例如头盔内侧的两面是可分别保留的矩形，但不能合并 UV 后声称逐值相同。

### cube 化限制

- 胸甲 q1/q3 为梯形：两端宽 0.5757074356 与 0.5742926002 米，差 0.0014148355 米；这超过浮点误差，不能把两端强行同宽。
- 胸甲根条 q15/q16 为斜切平行四边形，邻边夹角的余弦分别 0.0429928875、0.0571348004；普通旋转矩形不能原样表达。
- 双靴几何为盒体，但 q0 的两个 U 边界分别为 -0.001953125 与 +0.001953125 像素，四角 UV 的仿射残差为 0.00390625 像素。微小差异仍被保留，未擅自取整。
- 头盔包含 6 面主体盒、5 面斜盒、5 张植物平面和 2 段内面；植物不是两颗六面立体芽。斜盒约 30°，大植物平面约 4.52°，小植物平面约 11.49°；精确顶点优先于这些四舍五入角度。

已验证的矩形面可在支持任意轴旋转、逐面 UV、隐藏面的编辑格式里表示为盒体表面或零厚度平面。必须保留植物的原始平面、原始旋转和双面材质处理；不可把植物膨胀成有六面的像素方块。单个面为矩形并不自动证明整个部件能以一个 cuboid 表示；请依据 JSON 的连通分组结果。

Java 资源模型/现有构建管线能否原样保留这些旋转、双面和 UV1 尚未验证。现在不能把“部分几何可用 cuboid/plane 参数表达”写成“整套无损转换或目标游戏中无损导出已通过”。通用 mesh 形式能保存原顶点/UV；是否接入目标管线是另一步。

### 原始 UV 共用已获得证据

- 左右靴 6 面的 UV0 逐面完全相同；原模型明确支持这项左右共用。
- 头盔植物面 12/13 共用 [42,48,47,53]，14/15 共用 [48,50,51,53]；这是原始几何中的重复图案。
- 胸甲有 12 条根须平面条带：1 条单面段，11 条各含 2 个折弯段；全部使用 U=[63,64] 的纹理列并有各自 V 范围。原作确有共用，但这不支持旧候选把躯干两列涂到六个面上的做法。

## 原始纹理与通道

- Albedo 的 alpha 与 Wiki 全部一致；3377 个可见像素 RGBA 差异为 0。仅 719 个完全透明像素的隐藏 RGB 不同，保留游戏原始值。
- T_NatureArmor_S 与 Wiki ShadowTexture 全部 4096 个 RGBA 像素一致，共 47 种颜色。
- S 的 A 全部为 255，不是透明裁切蒙版。R/G/B 非零像素数量依次为 41, 1398, 153。
- 两眼共 4 像素的 S 值为 (0,246,246,255)；植物图案也包含相同值和渐变值，不能根据此图把原材质发光范围声称为“只有眼睛”。
- 原材质明确绑定 Albedo=T_NatureArmor、Specular=T_NatureArmor_S；NaturalEmissive=0.7、Emissive=(0.69331,8,0,1)、ConstantEmissive=true、SpecularTexture=true。
- 这些绑定和像素值不能独自证明 master shader 的 R/G/B 逐通道公式。未获得公式前不命名通道用途、不重排、不调色。

## 待完成的原始依据

1. BP_NatureArmor 的实际组件/socket 属性与字节偏移已在 bp_reference_evidence.json 中解析并引用。未序列化的相对旋转/缩放不能称实测 identity；Paperdoll 的 native 骨架赋值仍有证据缺口。不能把原玩家 sockets 直接当作 Mossy Skeleton 怪物挂点。
2. 核对目标 Java/Blockbench 导出器是否能精确保留任意倾斜平面、双面、原始 UV0；UV1 是否为原灯光贴图坐标仍需 source property 依据。
3. 读取 M_MasterEquipment 的材质公式，区分原发光/高光通道与最终渲染效果；UModel glTF 调试材质不能作颜色验收。
