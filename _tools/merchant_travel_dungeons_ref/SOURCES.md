# 来源

来自本机《Minecraft Dungeons》原始游戏包，经项目 `dungeons_conversion/generic.py` 转换。

- 网格：`Dungeons/Content/Actors/Characters/Friendlies/Villager/SK_Villager`
- 原材质：`MI_Villager_TravellingMerchant`
- 原贴图：`Dungeons/Content/Actors/Characters/Friendlies/Villager/T_Villager_TravellingMerchant`

- 动作：`Villager_Idle` → `idle`、`Villager_Idle_LookAround` → `look`、`Villager_Bowing` → `bow`、`Villager_Examining` → `examine`

原始贴图在本目录保留逐字节相同的 PNG。图集打包原像素和 UV；神秘商人帽子有一个面按原纹理取样成切片。最外层静态方向组绕原点旋转 Y=180°，将源村民 -Z 朝向归一为 +Z 友方制作坐标，运行时仍使用 turn=180。面部与手臂的原骨骼运动保留。帽子按原蓝图的 J_Head 挂点跟随。
