# 来源

篡夺者战（`add_usurper_fx_art.py`、`add_usurper_holy_look.py`）用到的特效贴图和道具模型，都从《Minecraft Dungeons》本体提取（只读，2026-11-14），在构建时重新切片、缩到 16 或 32 像素，再染色或重着色。

## 贴图

| 文件 | 原作路径 | 用法 |
| --- | --- | --- |
| `T_CastingTotem.png` | `Actors/Items/SoulTotemOfCasting/T_CastingTotem` | 附魔台符文 14 枚；三角法阵（叠成所罗门六芒星） |
| `T_TotemOfRegenerationRunes.png` | `Actors/Items/TotemOfRegeneration/T_TotemOfRegenerationRunes` | 符文参考 |
| `vfx/T_Circle_Full_15_spritesheet.png`、`vfx/T_fullcircle_dissolvedArc_15_spritesheet.png` | `Effects/Materials/Generic/Circles/` | 小冲击环（pop） |
| `vfx/T_fullcircle_explosion_64_spritesheet.png` | 同上 | 爆环（burst）、地面冲击环（shock） |
| `vfx/T_PixelHollowRadial_32.png` | 同上 | 地面圆环；圣雷砸地的扩张电环 |
| `vfx/T_fullsquareEdgeless_15_spritesheet.png` | 同上（原作 `SM_SquareDonut` 方形冲击的贴图序列） | 方形冲击环（天降、砸地、授权） |
| `vfx/T_HollowHexagonClean.png`、`vfx/T_MagicSymbolHiRes.png`、`vfx/T_MysteriousShapedCirclePixelated.png` | `Effects/Materials/Generic/` | 六边形、漩涡、光晕盘 |
| `vfx/T_Stars_16.png` | `Effects/Materials/Stars/` | 星芒 |
| `vfx/T_GodRayLight.png` | `Effects/Materials/` | 神光（光柱） |
| `vfx/T_Cracks.png` | `Effects/Materials/` | 地裂 |
| `vfx/T_Clouds_64.png` | `Effects/Materials/Noise/` | 附魔光束的滚动纹理（原作 `MI_EnchantedBeam`） |
| `vfx/T_Combat_Stab_Grayscale.png` | `Effects/Materials/Combat/` | 书页横扫的弧光 |
| `vfx/T_Combat_LongSlash_GrayScale.png`、`vfx/T_Slash_Grayscale.png` | `Effects/Materials/Combat/` | 二阶段连拳、突进的弧光 |
| `vfx/T_ElectricArcs.png` | `Effects/Materials/Electric/` | 电弧火花（16 种） |
| `vfx/T_ElectricStraight.png` | `Effects/Materials/Electric/` | 竖直闪电；权柄线 |
| `vfx/T_LightningSpline_1M.png` | `Content_DLC6/Decor/Prefabs/_End_Structures_/Voidstorm/` | 地面闪电网（storm） |

## 模型（经 `_tools/dungeons_conversion/generic.py` 转换）

| 目录 | 原作网格 | 用法 |
| --- | --- | --- |
| `fang/` | `Actors/Characters/Enemies/Illagers/Evoker/Fang/SK_Evoker_Fang` | 所罗门封印闭合时钻出的尖牙 |
| `crown/` | `Actors/Characters/Friendlies/Villager/Merchants/SM_Crown`；贴图是豪华商人 `T_Villager_LuxuryMerchant`（王冠的 UV 落在这张图上） | 二阶段帽顶的王冠，重着色为篡夺白金 |
| `pillar/` | `Actors/Characters/Enemies/Illagers/Geomancer/Pillar/SK_Geomancer_Pillar`（贴图 `T_Geomancer_Pillar_Wall`） | 神力超载的白金圣坛 |
| `totem/` | `Effects/Meshes/TotemOfUndying/SK_TotemOfUnDying` | 切阶段时死亡保护挡下致命一击 |

首席附魔师模型本身见 `_tools/prime_enchanter_ref/SOURCES.md`。

版权归 Mojang Studios 所有；本项目为非商业同人项目，与 Mojang 无关联。
