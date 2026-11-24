# 六项元素材料的原包检索

2026-11-23，只读检索本机《Minecraft Dungeons》完整包索引 `D:/agent/dungeons_extract/index/pak_files.json`、既有导出 PNG 和 `D:/agent/codex/TRA/UmodelSaved/Game`。本记录覆盖 `sin_shard`、`star_fragment`、`wind_essence`、`abyss_tear`、`molten_core`、`mountain_heart`。

检索词包括 shard、crystal、gem、core、tear、stone、amethyst、wind、whirl、star；同时排除仅能作为角色表面展开图的怪物、皮肤及装备 UV。检索名字只用于筛选，以下结论均结合 PNG 实际目视。没有将模型 UV 或白色特效径直认作物品图标。

## 查验的候选

原包路径均相对于 `Dungeons/Content/`；扩展名 `.uasset`。色数统计仅计 Alpha 非零像素的 RGB。

| 原包路径 | PNG 来源 | 原尺寸 | 可见 RGB 色数 | Alpha | 目视及适用判断 |
| --- | --- | --- | ---: | --- | --- |
| `Effects/Materials/Wind/T_WhirlWind.uasset` | `D:/agent/dungeons_extract/upgrade/fx/assets/Dungeons/Content/Effects/Materials/Wind/T_WhirlWind.png` | 64×64 | 1（白） | 多级，包含0，最大214 | 微弱白色旋风特效，没有球壳或独立材料轮廓；不直接用作风之精魄。 |
| `Effects/Flairs/HealingFlairs/02/T_Amethyst.uasset` | `D:/agent/claude/github-create/tralancer-rpg-1.21.11/_tools/force_ref/art/dungeons/T_Amethyst.png` | 16×16 | 7 | 0、255 | 紫色三尖晶簇，切面清楚；不符合浅灰白刻痕石片，也不符合深蓝星晶。可参考像素切面，不能标为目标材料原图。 |
| `Content_DLC6/Actors/Items/VoidShard/T_VoidShard.uasset` | `_inspection_elements/assets/Dungeons/Content/Content_DLC6/Actors/Items/VoidShard/T_VoidShard.png` | 32×32 | 4 | 0、255 | 白紫碎裂线条组成的方形表面贴图，没有独立的棱角石片剪影；不直接用作罪印碎片或星辰残片。 |
| `Content_DLC5/Actors/Items/Conduit/Vanilla_Conduit/T_Conduit_Wind.uasset` | `_inspection_elements/assets/Dungeons/Content/Content_DLC5/Actors/Items/Conduit/Vanilla_Conduit/T_Conduit_Wind.png` | 64×1024 | 2 | 0、255 | 青白长条帧纹理，没有球体轮廓，不是独立旋涡物件；不直接用作风之精魄。 |
| 同目录 `T_Conduit_Wind_Vertical.uasset` | `_inspection_elements/assets/Dungeons/Content/Content_DLC5/Actors/Items/Conduit/Vanilla_Conduit/T_Conduit_Wind_Vertical.png` | 64×1024 | 2 | 0、255 | 同类纵向条纹，不能直接作为小球内的气流图标。 |

## 导出记录

VoidShard 与两张 Conduit 候选使用现有 CUE4Parse 导出器 `D:/agent/dungeons_extract/exporter/bin/Release/net8.0/exporter.exe` 从本机游戏包导出，UE 版本4.22；此次3个指定 Texture2D 均成功，失败0。输出及导出器元数据仅写入 `art/_inspection_elements/`。未修改导出工具、游戏包、原图尺寸或 PNG 像素。

## 采用决定

六项材料均建议新绘：

- `sin_shard`：未找到可直接使用的浅灰白、带半个刻痕的独立碎石片。
- `star_fragment`：未找到深蓝晶体与白星点合为单件的材料图。
- `wind_essence`：现有旋风和 Conduit 纹理可解释风元素，但均无简报要求的小球物件轮廓。
- `abyss_tear`：未找到适合直接使用的深海蓝水滴宝石。
- `molten_core`：未找到开裂黑石壳包住熔光的独立材料图；Redstone 怪物 UV 不作为替代。
- `mountain_heart`：未找到灰褐岩块内嵌暗绿晶石的独立材料图。

该决定表示已查完整索引中的相关命名和上述视觉候选，没有声称游戏中绝不存在任何可改造部件。最终采用新绘以保留本批材料的独立语义与物品栏辨识度。
