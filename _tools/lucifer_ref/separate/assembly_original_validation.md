# 原始模型整合工程：独立回读核验

**结论：本次核验范围 PASS。** 当前实际保存的 Generic 整合文件完整保留已核验独立工程的几何、UV、骨骼与源贴图；发光配置引用正确且 HDR 参数未截断。此结论限定为数据保存和配置，不等于 Java 格式转换或原游戏画面验收。

文件：`lucifer_original_assembly.bbmodel`；SHA-256：`6edd3c8fbe961de7da84add78aea57d3c22a381428c7c25dff3aa30e34c6e061`。

输入 SHA-256：`ba80eafe5a45a989e49eb1a3c2bb433231d31e350fc72b6694f3ff57b9522edb`。

## 几何、面顺序与权重

1 个 armature、22 骨骼、12 mesh、468 顶点、210 三角面、468 条权重记录。对每个 mesh 同时比对实际独立 bbmodel、原始导入输入和冻结 expected；顶点键顺序、坐标、面序列、三角顶点绕序、逐角点 UV 全部精确一致。Native 随机 face ID 不作源身份要求；按保存的面序列比较。

| 整合 mesh | 顶点 / 三角面 | 纹理索引 | 权重骨名 | 坐标 / UV 最大差 |
| --- | ---: | ---: | --- | ---: |
| body__R_Leg | 36 / 12 | 0 | R_Leg | 0 / 0 |
| body__L_Leg | 36 / 12 | 0 | L_Leg | 0 / 0 |
| body__L_Arm | 36 / 12 | 0 | L_Arm | 0 / 0 |
| body__R_Arm | 36 / 12 | 0 | R_Arm | 0 / 0 |
| body__Head | 36 / 12 | 0 | Head | 0 / 0 |
| body__Body | 36 / 12 | 0 | Body | 0 / 0 |
| armor__SproutARmor_SproutArmor | 94 / 58 | 1 | J_Shoulders | 0 / 0 |
| armor__SM_Helmet_NatureArmor | 70 / 36 | 1 | J_Head | 0 / 0 |
| armor__R_Leg_SproutArmor | 24 / 12 | 1 | J_R_Foot | 0 / 0 |
| armor__L_Arm_SproutARmor | 20 / 10 | 1 | J_L_Hand | 0 / 0 |
| armor__R_Arm_SproutArmor | 20 / 10 | 1 | J_R_Hand | 0 / 0 |
| armor__L_Leg_SproutArmor | 24 / 12 | 1 | J_L_Foot | 0 / 0 |

本体权重与独立工程一致；盔甲按原 socket 父骨同名映射到本体骨 ID。两臂盔甲绑定 J_L_Hand / J_R_Hand，未错误绑定到 Arm。所有 mesh 原点与旋转为零，均直接挂在同一 armature 下；无新增几何变换。

## 骨骼与 bind world

22 骨父子关系与输入一致；每骨局部 origin 和 native Euler 与独立本体工程逐值一致。整条父子链计算出的所有世界矩阵（含根骨）与独立本体工程差值为 0。
相对归一化输入四元数得到的世界矩阵，最大浮点差为 `9.39873179284e-15`。这项残差单列，不冒称 native Euler 与未归一化原始四元数逐分量相同。

## 三张原图与 UV 尺寸

| 索引 | 原图 | PNG 尺寸 | UV 尺寸 | 原文件 / 独立工程 PNG 字节 |
| ---: | --- | --- | --- | --- |
| 0 | T_MossySkeleton.png | 64×32 | 64×32 | 均完全一致 |
| 1 | T_NatureArmor.png | 64×64 | 64×64 | 均完全一致 |
| 2 | T_NatureArmor_S.png | 64×64 | 64×64 | 均完全一致 |

盔甲两图的 uv_height 已确认为 64，没有沿用项目默认高度 32；三图 RGBA 差异像素均为 0。未合图、重采样或改变 alpha。

## 原始发光配置

保存的 dungeons_material_source 除 albedo / auxiliary UUID 随工程重建外，与独立盔甲工程完全一致；UUID 分别准确指向整合纹理 1 与 2，所有盔甲面绑定纹理 1，本体面绑定纹理 0。原 DXBC SHA 与辅助 PNG SHA 再次核对一致。

Emissive=[0.693310022354126,8,0]、EmissivePower=1、NaturalEmissive=0.699999988079071、DeathEmissive=1 均保持原值，未压成 8 位颜色。两图 sRGB 标记保留。
依据三图原字节独立求值，静态线性发光峰值为 `8.07491617080897`，与既有 GPU 验证的参考峰值一致。

既有 `emissive_gpu_validation.json` 来自独立盔甲项目 `root_rot_armor_original`，最大线性 RGB 误差 `2.26664449876e-06`、结果通过。本次只读核验确认相同纹理与材质配置移植完整，没有操作 Blockbench，也没有把先前独立项目 GPU 测量冒称整合项目的新测量。

## 范围与文件完整性

- 核验前后，整合与两套独立 bbmodel 的原文件字节均未变化。
- JSON 保留每部件、每骨、三图 hash、权重骨名和矩阵残差，便于复查。
- 这是保留原数据的 Generic 整合工程；Java 受限模型格式转换、动作和原游戏完整场景渲染属于后续阶段。
