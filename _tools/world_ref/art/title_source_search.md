# 六种称号图标：地下城原版检索

检索日期：2026-11-23。结论：六种称号均需要新绘。已检索本机完整包索引 `D:/agent/dungeons_extract/index/pak_files.tsv`，并查看下列已导出的原尺寸 PNG。原包路径以 `Dungeons/Content/` 为根，扩展名为 `.uasset`。

本说明不把模型 UV、图集或此前生成作品称作可直接使用的称号图标。未找到已导出 PNG 的候选仅记录索引事实，不推测其尺寸或透明度。

| 目标 | 原包候选 | 原尺寸 / 可见 RGB 色数 / Alpha | 实际查看与拒用原因 |
| --- | --- | --- | --- |
| `title_gate` 所罗门的门户 | `Dungeons/Content/Actors/Characters/Enemies/Illagers/Geomancer/GeomancerWall/T_Geomancer_Pillar_Wall.uasset` | 64×64 / 13 / 0、255 | 已查看。石柱模型的 UV 拼块，不是两根并立柱子的独立透明轮廓。环境 pillar/gateway 相关索引也主要为场景表面纹理。 |
| `title_ledger` 所罗门的账簿 | `Dungeons/Content/Actors/Characters/Enemies/Illagers/Enchanter/T_EnchantedBook.uasset` | 32×32 / 10 / 全255 | 已查看。展开书及装饰的 UV，不是合上的黑皮账本。 |
| `title_waverer` 摇摆者 | 未找到匹配的天平图标 | 未适用 | 在完整索引针对 balance/scales 等名称检索，未找到一半金、一半紫的天平。`force_ref/art/brand_sheet.png` 为此前生成作品，不能当地下城原版。 |
| `title_grandmaster` 大团长的朋友 | `Dungeons/Content/Actors/Characters/Enemies/Illagers/RoyalGuard/T_RoyalGuardShield.uasset` | 32×32 / 6 / 全255 | 已查看。盾的正反 UV 两片，蓝灰与金配色，无红十字，不适合作为直接使用的红色十字盾。 |
| `title_meteor` 白昼流星 | `Dungeons/Content/Effects/Materials/Stars/T_Stars_16.uasset` | 32×32 / 1 / 0、63、127、255 | 已查看。2×2 星光图集，每格16×16；没有尾巴，且保留半透明。不是单张带尾流星称号。 |
| `title_merchant` 被商人记恨 | `Dungeons/Content/Decor/Prefabs/Coins/T_Coin.uasset` | 8×8 / 4 / 0、255 | 已定点导出并查看。上方5行是金黄色矩形表面片，下方3行透明；没有独立圆形金币轮廓，也没有咬口，是场景金币表面纹理，不适合直接作咬缺金币称号。 |

## 已查看 PNG 的本机路径

- `D:/agent/dungeons_extract/colorscan/tex/assets/Dungeons/Content/Actors/Characters/Enemies/Illagers/Geomancer/GeomancerWall/T_Geomancer_Pillar_Wall.png`
- `D:/agent/dungeons_extract/colorscan/tex/assets/Dungeons/Content/Actors/Characters/Enemies/Illagers/Enchanter/T_EnchantedBook.png`
- `D:/agent/dungeons_extract/upgrade/towerguard/assets/Dungeons/Content/Actors/Characters/Enemies/Illagers/RoyalGuard/T_RoyalGuardShield.png`
- `D:/agent/dungeons_extract/upgrade/michael_fx/assets/Dungeons/Content/Effects/Materials/Stars/T_Stars_16.png`

尺寸、色数和 Alpha 由 Pillow 读取原文件核对；以上原图未缩放、未改色、未写回。

## T_Coin 定点补查

原尺寸PNG：[_inspection_badges/coin_check/assets/Dungeons/Content/Decor/Prefabs/Coins/T_Coin.png](_inspection_badges/coin_check/assets/Dungeons/Content/Decor/Prefabs/Coins/T_Coin.png)。通过现有CUE4Parse导出器从原包解包，1个Texture2D、0失败，UE4.22；没有缩放、裁切、改色或透明清理。PNG为8×8、4种可见RGB、Alpha仅0/255；可见包围盒为`(0,0,8,5)`。已实际目视其矩形金色表面片，确认不具备金币外轮廓或咬缺构图。导出元数据在同目录层级的`coin_check/metadata/`。

## 其他索引候选与检索边界

以下仅索引发现，不声称已经目视或符合需求：

- 黑账本相关：`Dungeons/Content/Decor/Prefabs/Book/T_Book.uasset`；`Dungeons/Content/Content_DLC6/Decor/Prefabs/_End_Structures_/TheStronghold/T_Book.uasset`。均属于场景 prefab 纹理路径，当前未找到对应既有导出 PNG。
- 金币相关：`Dungeons/Content/Decor/Prefabs/Coins/T_CoinStack0.uasset`、`Dungeons/Content/Decor/Prefabs/Coins/T_GoldBar.uasset`、`Dungeons/Content/Decor/Prefabs/Coins/T_GoldStack.uasset`。没有咬缺构图的名称命中，未把整套场景纹理直接当称号。
- 盾牌相关：`Dungeons/Content/Actors/Characters/Enemies/Illagers/TowerGuard/T_TowerGuardShield.uasset`、`Dungeons/Content/Actors/Characters/Enemies/SkeletonVanguard/T_DesertShield.uasset`、`Dungeons/Content/Decor/Prefabs/ShieldDecorative/T_TrophyShield.uasset`。名称不足以证明存在红十字盾面。
- 流星相关：`Dungeons/Content/Content_DLC6/Decor/Prefabs/_End_Structures_/FallingAsh+Meteors/T_AshParticles.uasset`。名称为灰烬粒子，不是可直接认定的流星图标。

本结论是为六种指定语义和字号可读性作的素材筛选，不声称原游戏全部资源中绝对不存在可组合的部件。按照简报，拒用这些不合适的直接候选后，六张称号采用新绘；各张最终生成次数和选稿由主报告记录。
