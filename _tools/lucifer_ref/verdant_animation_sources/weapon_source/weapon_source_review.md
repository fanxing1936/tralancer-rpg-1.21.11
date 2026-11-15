# 现有路西法蛇矛：直接导入输入与右手挂点

本次只读仓库、Minecraft 1.21.11 客户端和已经导出的原始 Dungeons 骨架。输出全部在本 scratch 目录；未修改 `add_lucifer.py`、资源包 PNG/JSON、骨架或任何 Blockbench 工程，未操作 UI/Blockbench。

## 可直接使用的输入

- `weapon_native_input.json`：与既有 `body_for_blockbench.json` 相同的 `parts / vertices / faces / weights` 结构，另附源文件 hash、全部原始几何、纹理原字节 data URL 和坐标矩阵。
- 只向既有原始身体 rig 追加 `parts[0]` 和该纹理。`bones[]` 是映射上下文，不应再创建 22 根重复骨骼。
- `parts[0].vertices` 已经变换到现有原始身体的全局 bind 坐标；不再应用 `binding.world_matrix_from_generated_pixels`。
- 全部 552 个 wedge 的权重是 `[[16,1.0]]`。源 skin joint id 16 对应 `J_R_Weapon`；导入时按 id/name 映射到现有 ArmatureBone UUID。
- 138 个四边面可由 Generic Mesh 原样保存；若导入器只支持三角面，可按同一角点顺序拆成 276 三角面，UV 仍逐角保留。
- `weapon_native_validation.json` 保存本次数据检查结果；`prepare_existing_weapon.py` 可重复构建适配输入。

## 现有武器的真实来源

仓库 `resourcepack/assets/rpg/models/item/lucifer_in_hand.json` 继承 `minecraft:item/spear_in_hand`，只指定 `layer0=rpg:item/lucifer_in_hand`。当前 `netherite_spear` item 定义中 CMD 1110014 的分支也记录在输入 manifest。

`_tools/add_lucifer.py` 第 170 行附近的 `build_texture()` 已将 GUI 图水平镜像生成手持图；本次逐像素比较确认当前 `lucifer_in_hand.png` 与 `lucifer.png[:,::-1]` 完全相等。导入直接使用现成手持 PNG，**不再镜像**。

原 PNG 为 32×32，161 个非透明像素，alpha 仅为 0/255。PNG SHA-256：

`f3e429eda393da49c249b8f118f7e764951de265b630d738a32a522013b90dee`

父模型直接从本机 1.21.11 客户端 jar 读取，保存在 `spear_in_hand.original.json`。原第三人称右手参数为：rotation `[5,270,-40]`，translation `[0,2,2]`，scale `[1.7,1.7,0.85]`。

## 几何不是重新设计

`item/generated` 没有静态 elements；其几何由客户端根据已有贴图透明度生成。本次以 Mojang 官方 1.21.11 mappings 确认类名后，直接调用本地客户端的：

- `ItemModelGenerator.processFrames`（混淆类 `hqj`）；
- `FaceInfo` 与 `BlockElementFace` 的角点、逐顶点 UV API；
- `ItemTransform.apply`（混淆类 `hqk`），取得真正的 float32 第三人称变换矩阵。

`ExistingWeaponExtractor.java` 只为 SpriteContents 提供已有 PNG 的宽高、单帧和 alpha==0 查询；生成几何与 UV 运算仍由客户端原方法执行。没有重画像素、描摹轮廓或手写替代武器模型。客户端 root-package class 的字节副本位于 scratch `client_classes_readonly_copy`，用于避免自定义分析类与签名 jar 默认包的 signer 冲突；安装 jar 本身未改。

结果：137 个 generated elements，其中第一项含正反 2 面，另外 136 项各含一个轮廓侧面，共 138 面。独立统计 PNG 的可见/透明相邻边得到 136，与侧面数完全一致。前后厚度是原客户端的 `z=7.5..8.5`；当前 1.21.11 轮廓 UV 内缩是 `0.1` texel，已保留客户端产生的实际 float 值。

`weapon_existing_generated.json` 保存原客户端元素与逐角数据。`*_javap.txt` 和 `weapon_minecraft_mappings_excerpt.txt` 提供对应方法字节码/官方映射证据。源 UV 回读最大误差为 0。这里保留模型 UV；游戏纹理 atlas 拼接、过滤和最终渲染不在此导入验证范围内。

## 原始右手挂点证据

`D:/agent/codex/TRA/work/lucifer_original/Skeleton_Skeleton.parsed.json` 第 69–108 行记录：

```text
SkeletalMeshSocket_0
SocketName = J_R_WeaponSocket
BoneName   = J_R_Weapon
```

该 socket 只序列化这两个属性，没有非默认相对平移、旋转、缩放 override；socket-to-bone 采用引擎默认单位变换。原始 `SK_Skeleton.gltf` 层级是：

```text
J_R_Arm (joint 14)
└─ J_R_Hand (joint 15)
   ├─ J_R_Weapon (joint 16)
   └─ R_Arm (joint 17，身体右臂 mesh 的权重骨)
```

武器应绑定 `J_R_Weapon`，不以 `R_Arm` 代替。输入保留 glTF 原节点索引、原始 socket 属性、源 glTF 转换后的 bind matrix，以及现有原生保存身体的 bind matrix。两者按既有归一化 quaternion / Euler 表达比较，最大矩阵差约 `4.98e-15`；不宣称恢复了 glTF 导出前 UE quaternion 的全部精度。

## 明确的跨游戏持物适配

`display_mob.py` 文档第 26–33 行及代码第 334–342 行定义了既有 Java 人形持物规则。`add_sunken_skeleton.py` 使用 `held="weapon"`，并在 `thirdperson_righthand` 模式复制原物品，没有另建武器模型。

原始 Dungeons socket 是可信挂点；现有蛇矛是 Java 资源包物品，没有“原 Mossy 手持此蛇矛”的原资产。二者之间需要显式适配，不能把适配当成原作武器绑定数据。

本输入的默认适配保留 Java 持物朝向与原物品 display transform，仅将旧规则的固定 arm→grip 平移换成真实 `J_R_Weapon` 位置。矩阵均为 row-major，乘列向量：

```text
H = Rx(-90°) · Ry(180°) · T(1/16, 2/16, -10/16)
A = diag(-16, -16, 16, 1)
h = translation(A·H) = (1, -10, -2)  [浮点表达有微量尾差]
P = 客户端 ItemTransform.apply 的原矩阵，已含 T(-0.5,-0.5,-0.5)
B = 原 J_R_Weapon 的 native bind world matrix

W = T(B.translation) · T(-h) · A · H · P · S(1/16)
L_socket = inverse(B) · W
```

`W` 为原模型像素坐标到身体全局坐标；`L_socket` 为相同点到骨局部坐标。输入同时保存严格沿用旧 arm-pivot 固定偏移的另一矩阵，供对照，不默默覆盖来源。默认适配与该旧版本只差一个固定平移。

全局 vertices 配合 J_R_Weapon 的权重后，原生 Armature 在 bind 姿态保持其位置，在动作中按该骨跟随。武器握持美术姿态、遮挡、动作轨迹与 Java 游戏内最终表现仍需主任务导入后检查；本次没有制作动作或宣称这些检查通过。

## 数值检查

| 项目 | 结果 |
| --- | --- |
| generated elements / quad faces / wedges | 137 / 138 / 552 |
| 独立 alpha 边界与客户端侧面 | 136 / 136 |
| 源 UV 回读误差 | 0 |
| 全部权重对应原 J_R_Weapon | 是，均为 1.0 |
| world→源模型坐标逆变换最大误差 | `3.552713678800501e-15` |
| `B·L_socket` 与 `W` 最大差 | `1.7763568394002505e-15` |
| PNG 再次镜像 | 未执行 |
| 原始源文件写入 | 未执行 |

几何的 full-plane 包围盒包含透明区域，不应用它判断矛尖或握把实际像素的占据范围。
