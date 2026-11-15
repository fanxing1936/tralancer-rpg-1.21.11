# 原玩家与 Mossy 原骨架 bindworld 只读比对

结论：六个盔甲插槽父骨的完整绑定世界矩阵一致；原玩家 bind-space 装配可以直接叠到 Mossy bind-space，坐标对齐不需要猜测平移、缩放或形变。未做任何整合或调整。

| 部件 | 原插槽 | 父骨 | 原点差距 Java px | 线性矩阵最大差 |
|---|---|---|---:|---:|
| body | J_ShouldersSocket | J_Shoulders | 5.58309442853e-15 | 0 |
| head | J_Head_Socket | J_Head | 5.77315972805e-15 | 0 |
| right_leg | J_R_Leg_Socket | J_R_Foot | 0 | 0 |
| left_arm | J_L_Shoulder_Socket | J_L_Hand | 0 | 0 |
| right_arm | J_R_Shoulder_Socket | J_R_Hand | 0 | 0 |
| left_leg | J_L_Leg_Socket | J_L_Foot | 0 | 0 |

原装甲顶点在两组对应父骨下的最大差距：5.77315972805e-15 Java px（浮点数值零）。两个 rig 均用二进制 inverseBindMatrices 求逆，并和节点层级独立交叉验证。

20 个同名骨的逐项原点、完整矩阵与误差见 JSON。另单独比较 J_Hip↔J_L_Hip、J_Spine↔J_L_Spine，不把改名当成同名。

## 不能忽略的差异

- `Head`：原点差 2.69238946593e-06 px，方向差 0.593083002261°，线性矩阵最大差 0.0102112959936。父级分别为 `J_Head` / `J_Neck`。
- `J_R_Arm`：原点差 0 px，方向差 180°，线性矩阵最大差 2.00000011921。父级分别为 `J_Shoulders` / `J_Shoulders`。

盔甲实际使用 J_R_Hand 和 J_Head，二者完全对齐；不要改绑到 J_R_Arm 或 Head。不能据六个父骨相同就宣称整套骨架或运行时动画完全相同。

## Native Paperdoll 证据仍不足

现有 NatureArmor、SproutArmor、SproutArmor_Unique1 蓝图都直接继承 native `/Script/Dungeons.GearActor`。Paperdoll 的模板指向 native `Default__GearActor.Paperdoll`，三套都未序列化 `SkeletalMesh` 属性。现有 raw 中没有 native constructor/CDO 的网格赋值，故不能确定 `Paperdoll.SkeletalMesh=SK_Player_Master`。

NatureArmor 的 Player_Master_Run 动画引用、玩家 skeleton assignment、六个插槽名以及 bindworld 一致，都只是相关证据，不补上缺失的 native 属性赋值。

本报告仅证明绑定坐标系可以直接对齐，不证明原图姿态、实际游戏造型没有穿插、动画重定向完成或 monster 原生拥有玩家盔甲插槽。未改动任何导入输入或模型。
