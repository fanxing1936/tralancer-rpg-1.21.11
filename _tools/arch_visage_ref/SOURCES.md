# Arch-Visage 素材来源

原作 Minecraft Dungeons 的素材版权属于 Mojang。本项目非商业，与 Mojang 无关联。来源整理页为 [Minecraft Wiki：Heart of Ender](https://minecraft.wiki/w/Dungeons:Heart_of_Ender)，致谢页面贡献者。

原图与 GIF 共用 `../heart_of_ender_ref/` 存档，未修改；Arch-Visage 的 9 个音效在本目录 `sounds/` 保留原文件名，已与原存档逐字节比对。Music 未下载。下列 SHA 是本地存档指纹，不是发行者校验值。

| 文件 | 字节 | SHA-256（前 16 位） | 来源页面 | 文件地址 |
|---|---|---|---|---|
| `../heart_of_ender_ref/MCD_Arch-Visage.png` | 236861 | `ec1a117e355f9181` | <https://minecraft.wiki/w/Dungeons:Heart_of_Ender> | <https://minecraft.wiki/images/MCD_Arch-Visage.png> |
| `../heart_of_ender_ref/MCD_Arch-Visage_Spawn_Attack_in_game.gif` | 1674295 | `c3f7196e815ace77` | <https://minecraft.wiki/w/Dungeons:Heart_of_Ender> | <https://minecraft.wiki/images/MCD_Arch-Visage_Spawn_Attack_in_game.gif> |
| `../heart_of_ender_ref/MCD_Arch-Visage_Spawn_Attack.gif` | 2438126 | `63084c7d3fc0835a` | <https://minecraft.wiki/w/Dungeons:Heart_of_Ender> | <https://minecraft.wiki/images/MCD_Arch-Visage_Spawn_Attack.gif> |
| `../heart_of_ender_ref/MCD_Decal_Puddle_(texture).png` | 14896 | `fb28326ab01670ec` | <https://minecraft.wiki/w/Dungeons:Heart_of_Ender> | <https://minecraft.wiki/images/MCD_Decal_Puddle_(texture).png> |
| `../heart_of_ender_ref/MCD_Heart_of_Ender_(glow_effect_texture).png` | 2730 | `242e52383f566481` | <https://minecraft.wiki/w/Dungeons:Heart_of_Ender> | <https://minecraft.wiki/images/MCD_Heart_of_Ender_(glow_effect_texture).png> |
| `../heart_of_ender_ref/MCD_Heart_of_Ender.png` | 318059 | `8b32af4ca6b42239` | <https://minecraft.wiki/w/Dungeons:Heart_of_Ender> | <https://minecraft.wiki/images/MCD_Heart_of_Ender.png> |
| `sounds/Sfx_boss_ArchvisageBeamAttack-001.ogg` | 17275 | `97d9a71862a44c75` | <https://minecraft.wiki/w/Dungeons:Heart_of_Ender> | <https://minecraft.wiki/images/Sfx_boss_ArchvisageBeamAttack-001.ogg> |
| `sounds/Sfx_boss_ArchvisageBeamAttack-002.ogg` | 16515 | `cc58c516881b25d5` | <https://minecraft.wiki/w/Dungeons:Heart_of_Ender> | <https://minecraft.wiki/images/Sfx_boss_ArchvisageBeamAttack-002.ogg> |
| `sounds/Sfx_boss_ArchvisageBeamAttack-003.ogg` | 16620 | `b5437848b70f4295` | <https://minecraft.wiki/w/Dungeons:Heart_of_Ender> | <https://minecraft.wiki/images/Sfx_boss_ArchvisageBeamAttack-003.ogg> |
| `sounds/Sfx_boss_ArchvisageBeamLoop-001.ogg` | 19311 | `85b33dc2f8c677b5` | <https://minecraft.wiki/w/Dungeons:Heart_of_Ender> | <https://minecraft.wiki/images/Sfx_boss_ArchvisageBeamLoop-001.ogg> |
| `sounds/Sfx_boss_ArchvisageMortarShoot-001.ogg` | 8931 | `59e995105c3c7e2f` | <https://minecraft.wiki/w/Dungeons:Heart_of_Ender> | <https://minecraft.wiki/images/Sfx_boss_ArchvisageMortarShoot-001.ogg> |
| `sounds/Sfx_boss_ArchvisageMortarShoot-002.ogg` | 7885 | `e2b2df378c9c88da` | <https://minecraft.wiki/w/Dungeons:Heart_of_Ender> | <https://minecraft.wiki/images/Sfx_boss_ArchvisageMortarShoot-002.ogg> |
| `sounds/Sfx_boss_ArchvisageMortarShoot-003.ogg` | 8735 | `07b8678243300ee5` | <https://minecraft.wiki/w/Dungeons:Heart_of_Ender> | <https://minecraft.wiki/images/Sfx_boss_ArchvisageMortarShoot-003.ogg> |
| `sounds/Sfx_boss_ArchvisageTeleIn.ogg` | 12599 | `e1edcf540f14e959` | <https://minecraft.wiki/w/Dungeons:Heart_of_Ender> | <https://minecraft.wiki/images/Sfx_boss_ArchvisageTeleIn.ogg> |
| `sounds/Sfx_boss_ArchvisageTeleOut.ogg` | 17550 | `920d0193812bc8cc` | <https://minecraft.wiki/w/Dungeons:Heart_of_Ender> | <https://minecraft.wiki/images/Sfx_boss_ArchvisageTeleOut.ogg> |

## 派生材料

- `arch_visage.bbmodel`：当前事实来源，包含全部三个 clip；最新由 `../arch_visage_match_head.py` 将末影之心主模型头壳、薄颚与发光表面移入原AV动作，没有额外未记录的 Blockbench 手工编辑。旧 `arch_visage_author.py` 仅代表历史厚颚版，已保护当前工程不被旧入口覆盖。
- `atlas.png`：最新与末影之心主模型内嵌图集PNG逐字节相同，不再使用旧AV专属嘴面投影区。每面UV和源元素映射见 `atlas_regions.json`；原AV采样研究继续作为历史资料保留。
- 眼与牙像素继承 HE 原渲染的既有采样窗口；六个星窗继承 HE 原 711×711 星空裁片及用户接受的紫色转换。完整源窗口与逐像素公式引用 `../heart_of_ender_ref/m2_atlas/atlas_regions.json`、`m3_material/material_transform.json`、`m3_material_v3/material_changes.json`。本次没有重绘星点或新的牙齿图案。
- 44×44 原遮罩在 `[432,88,476,132)` 逐 RGBA 保留。两张口内层实际采样其中白色有效区 `[0,2,33,44)`，由独立生成后处理设置源取色常量 tint。其余黑色区的官方语义未知；未称其为已证实的 padding。无真正 bloom。
- `preview/`、`spawn_attack_preview.gif`：从当前 bbmodel 重新投影的离线 CPU 预览；不是原素材，也不是 Blockbench 或真实游戏画面。
- `calibration.json`、`refined_motion.json`：可见角点测量、约束拟合和隐藏深度假设；不是官方模型或原骨骼工程。

未采用的 6 秒动画只存档作版本差异参照；动作以 4.88 秒 in_game GIF 为准，不能把静态渲染的持续亮眼复制到全段。in_game 初段确实短暂出现亮眼，已按实际帧区分。
