# 原始蓝图引用与组件变换证据

范围：只读原始 PAK 提取文件，解析 ImportMap/ExportMap 与实际属性标签；未执行 Blueprint 字节码/native constructor，未修改模型。所有原始 payload 已逐文件校验 PAK SHA1，详见 `raw_manifest.json`。

## Mossy Skeleton：已证明实际 mesh assignment

`BP_MossySkeletonCharacter_C` 的 ExportMap SuperIndex 指向 `/Game/Actors/Characters/Enemies/BP_MobCharacter.BP_MobCharacter_C`。并非推测的 BP_SkeletonCharacter。

`Default__BP_MossySkeletonCharacter_C.Mesh` 实际 ObjectProperty 指向 export 46 `CharacterMesh0`；该组件的 `SkeletalMesh` ObjectProperty 实际指向 `/Game/Actors/Characters/Enemies/Skeleton/SK_Skeleton.SK_Skeleton`，`OverrideMaterials[0]` 指向 `M_MossySkeleton`。材料参数 `Texture` 实际赋值 `T_MossySkeleton`。这是属性赋值链，不是仅在 NameMap/ImportMap 出现名字。

组件原始 RelativeLocation=[0,0,-90]，RelativeRotation(Pitch,Yaw,Roll)=[0,-90.00020599365234,0]；相对 Capsule。未序列化 RelativeScale3D。原 `SK_Skeleton.Skeleton` 指向 `Skeleton_Skeleton`。

## NatureArmor：6 个实际组件 assignment

Root Rot 身份来自主任务的原贴图对照；本报告单独验证 NatureArmor 的实际 BP 赋值。父类为 native `/Script/Dungeons.GearActor`。六个 SCS root node 都明确附着于 native `Paperdoll`，且全部覆盖材质为 `MI_NatureArmor`。

| 原 mesh 文件名 | socket | RelativeLocation (UE XYZ) | RelativeRotation (Pitch,Yaw,Roll) |
|---|---|---|---|
| SproutARmor_SproutArmor | J_ShouldersSocket | [0.0, 141.0, -0.00206890725530684] | 未序列化（不冒称测得默认值） |
| SM_Helmet_NatureArmor | J_Head_Socket | 未序列化（不冒称测得默认值） | 未序列化（不冒称测得默认值） |
| R_Leg_SproutArmor | J_R_Leg_Socket | [0.0, 6.67572021484375e-06, 0.0] | [0.0, 0.0, -180.0] |
| L_Arm_SproutARmor | J_L_Shoulder_Socket | [-3.305845260620117, 4.653480052947998, -2.2016467937646667e-06] | 未序列化（不冒称测得默认值） |
| R_Arm_SproutArmor | J_R_Shoulder_Socket | [-0.27732276916503906, -4.629638671875, 0.0006945380591787398] | [4.0981132769957185e-05, 2.0324996512499638e-05, -179.99966430664062] |
| L_Leg_SproutArmor | J_L_Leg_Socket | [0.0, 7.000000096013537e-06, 0.0] | 未序列化（不冒称测得默认值） |

头盔路径 `/Game/Content_Season2/Actors/Equipment/Armor/NatureArmor/SM_Helmet_NatureArmor`。其余五件路径均在 `/Game/Content_DLC4/Actors/Equipment/Armor/SproutArmor/`。普通 Sprout 头盔及 SproutArmor_Unique1 材质不属于这条 assignment 链。

全部 component 的 RelativeScale3D 未序列化，template 都是 `/Script/Engine.Default__StaticMeshComponent`。变量名保留 FurArmor 历史标签，左右腿变量名还与 mesh/socket 反写；必须以 mesh assignment 和 socket 为准。

`MI_NatureArmor.Parent` 实际指向 `/Game/Actors/Equipment/M_MasterEquipment.M_MasterEquipment`；TextureParameterValues 的 Albedo=`T_NatureArmor`，Specular=`T_NatureArmor_S`。Master material 的实际标签为 BlendMode=`BLEND_Masked`、TwoSided=true。MI 存储的 BasePropertyOverrides 值不能在缺少 override flag 证据时单独当作生效覆盖。

## 原 socket 定义与装配边界

`SK_Player_Master.Skeleton` 明确赋值 `Player_Master_Skeleton`，后者含与这六个 attachment 名称一致的原始 SkeletalMeshSocket：

| Socket | Bone | 序列化 RelativeLocation |
|---|---|---|
| J_Head_Socket | J_Head | 未序列化（不冒称测得默认值） |
| J_ShouldersSocket | J_Shoulders | 未序列化（不冒称测得默认值） |
| J_R_Shoulder_Socket | J_R_Hand | [7.0, 65.0, 0.0] |
| J_L_Shoulder_Socket | J_L_Hand | [-4.0, -65.0, 0.0] |
| J_L_Leg_Socket | J_L_Foot | 未序列化（不冒称测得默认值） |
| J_R_Leg_Socket | J_R_Foot | 未序列化（不冒称测得默认值） |

**尚未证明的一级：** `BP_NatureArmor.Paperdoll` 没有序列化 SkeletalMesh assignment，template 为 native `Default__GearActor.Paperdoll`。未读取 native constructor，因此不能单凭 socket 同名宣称已证明 native Paperdoll 必然使用 SK_Player_Master。可用该原玩家骨架验证候选原始组合，但必须保留此证据界限。

怪物 `Skeleton_Skeleton` 不含上述六个 armor sockets。将盔甲穿到 Mossy 属于后续适配，不是原游戏已存在的装配。部件位置必须由骨骼世界变换 × socket 相对变换 × component 相对变换组成，再统一转换坐标系。当前表不能直接当作 Blockbench 世界坐标。

未序列化变换字段以 null 保留，不把缺省值冒称为原文件实测。这里未验证 runtime animation、Blueprint 字节码/构造行为或真实游戏画面。

完整字节偏移、SHA256、赋值引用、source dumps 在 `bp_reference_evidence.json`。独立解析器 `ue4_bp.py` 对所有选中包的 import/export table 边界及顶层 property None 终止符均通过；未解析 native 数据保留为剩余字节，不冒称整个类格式全部解析。

格式依据：[UEViewer package maps](https://github.com/gildor2/UEViewer/blob/master/Unreal/UnrealPackage/UnPackage4.cpp)；[UEViewer property tags](https://github.com/gildor2/UEViewer/blob/master/Unreal/UnObject.cpp)。
