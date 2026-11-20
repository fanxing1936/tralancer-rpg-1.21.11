# 来源

米迦勒战的专属特效（`add_michael_fx_art.py`）用两路素材，构建时切帧、缩到 16 或 32 像素，再按米迦勒的两条色阶烘焙颜色。

## 《Minecraft Dungeons》本体（`dungeons/`，只读导出，2026-11-18）

| 文件 | 原作路径 | 用法 |
| --- | --- | --- |
| `T_FireBlock1x1.png` | `Effects/Materials/Fire/FireBlock/` | 16 帧火焰：圣焰（二阶段）、暖白金火（一阶段），火路、圣哉焰墙、炽天使火簇 |
| `T_FireSide.png`、`T_FireDroplet.png` | `Effects/Materials/Fire/` | 火舌（羽刃尾迹、飞行肋骨的尾火）、火滴（圣焰叠层） |
| `T_Feathers.png` | `Effects/Materials/Feather/` | 羽毛 |
| `T_Stars_16.png` | `Effects/Materials/Stars/` | 星芒 |
| `T_GodRayLight.png` | `Effects/Materials/Light/` | 神光（光柱） |
| `T_fullcircle_explosion_124_spritesheet.png` | `Effects/Materials/Generic/Circles/` | 爆环（字形）与地面冲击环（物品帧） |
| `T_Doves_Flipbook.png` | `Effects/Flairs/LevelUpFlairs/03/` | 白鸽（登场、消散） |
| `T_SmokeBallVariation.png` | `Effects/Materials/Smoke/` | 黑烟（守望者传送、死亡） |
| `T_Cracks.png` | `Effects/Materials/Cracks/` | 焦痕 |
| `T_Dissolve_32.png` | `Effects/Materials/Noise/` | 火路上的烬火（滚动动画） |

其余导出的贴图（弧光、漩涡、光束等）留作参考，没有进游戏。

## Codex 绘制（`anim/`，按 `ART-BRIEF.md`，2026-11-18）

睁眼六帧、守望之眼四帧、六翼爆开、燃羽、坠星、天火柱、骨刺破土、十字斩、炽天使光环、圣火环，以及炽天使圣印、眼印、七号角印。
提示词和尺寸见 `anim/REPORT.md`。

## 程序绘制（`add_michael_fx_art.py`）

新月弧光（一阶段白金、二阶段圣焰、270° 横扫）、圆环、扇区、X 印、地面裂线、光晕、全屏闪光与泛红、光芯。

版权：原作素材归 Mojang Studios 所有。本项目是非商业同人项目，与 Mojang 无关联。
