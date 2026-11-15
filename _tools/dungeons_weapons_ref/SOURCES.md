# 来源

从《Minecraft Dungeons》本体提取（只读），由 `_tools/add_dungeons_weapons.py` 还原成物品贴图。

- 坟墓克星（Grave Bane）：`Dungeons/Content/Actors/Equipment/MeleeWeapons/Glaive_Unique1/`
  - `T_Glaive_Unique1.png`（34×34）：武器像素，黑底；第 0 行左端 9 格是色板，不在网格上
  - `T_GlaiveUnique1_S.png`：发光层，只作参考
- 竖琴弩（Harp Crossbow）：`Dungeons/Content/Actors/Equipment/RangedWeapons/ScatterCrossbow_Unique1/`
  - `T_HarpCrossbow.png`（38×38）：四格（每格 19，格内第 0 行是色板）各一帧，按 `SM_HarpCrossbow1~4.glb` 的 UV 对应
    1 左上（弦松、未上弦）、2 左下（拉到一半）、3 右上（上好箭）、4 右下（拉满）
  - `T_HarpCrossbow_S.png`：发光层，只作参考

两把原作武器都是贴图挤出厚度的网格。武器像素按网格 UV 实测：
坟墓克星覆盖的 116 格正好是贴图里除色板外的全部非黑像素；
竖琴弩每帧覆盖的格子正好是对应格里的全部不透明像素。所以贴图原格还原，不重画。

版权归 Mojang 所有；本项目非商业，与 Mojang 无关联。
