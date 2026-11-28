# 城镇与新手村贴图交付报告

按 [ART-BRIEF.md](../ART-BRIEF.md) 的逐项表格交付 29 张成品，包含 11 张物品图标、2 张称号图标、5 张界面图标、4 套特效和 7 张人物贴图。请求中的总数为 27，交付以简报列出的文件名为准。

成品存于 `art/`，采用的原包贴图存于 `art/dungeons/`，保持原包文件名、原尺寸和解码像素。先查本机《Minecraft Dungeons》PAK 索引，再用已有 CUE4Parse 导出器查看候选。新绘使用内置 `image_gen`。下表的「次数」统计生图调用，采用编号按该项生图顺序标记。

## 物品、称号及界面图标

18 张均为 16×16 RGBA PNG。图标以主体的透明包围盒确定取样范围，落到原生网格后量化至固定平涂色板，将 Alpha 收到 0 或 255。徽章第 2 张将教堂改为高反差剪影。通行符和地图碎片在 16 格上校正了十字蜡印和红叉的细线，归途纸卷保留了右上的小余烬，断剑缩格后提高了三粒碎片的亮度。

| 成品 | 原包查找结果 | 生图次数 / 采用 | 主体提示 |
| --- | --- | --- | --- |
| `town_badge.png` | `T_LoveMedallion_GearIcon` 为菱形心章，构图与用途不符 | 2 / 第 2 张 | 铜圆章、尖顶教堂剪影、短绶带 |
| `eden_pass.png` | `T_Paper_Graph_02` 无蜡封，英雄卷轴命中的是粒子系统 | 1 / 第 1 张 | 折叠羊皮纸、金色十字蜡印和暗红纸边 |
| `home_scroll.png` | 英雄卷轴相关资产只有法术粒子候选，未见一端带余烬的卷纸图标 | 1 / 第 1 张 | 右上斜放的纸卷、卷端橙色余烬 |
| `black_candle.png` | `T_EvilCandle`、`T_CandleNew`、`T_EndCandle` 是场景模型的表面贴图 | 1 / 第 1 张 | 短粗黑蜡烛、紫火、蜡泪 |
| `pact_scroll.png` | 实查纸页图只有图表或记录纹样，未见紫手印契约 | 1 / 第 1 张 | 暗红羊皮纸、底部紫色手印 |
| `map_shard.png` | `T_Map` 与 `T_MapTable_Map` 为完整地图模型表面，缺少碎边和红叉 | 1 / 第 1 张 | 撕角旧地图、蓝河和红叉 |
| `wanted.png` | 纸页候选未见同时具备钉子、红边和人头剪影的告示 | 1 / 第 1 张 | 钉在顶端的告示、人头剪影、红色上沿 |
| `welfare_pack.png` | `T_Satchelofnourishment_Icon_Inventory`、`T_Satchelofneed_Icon_Inventory` 为箱形道具，装饰用麻袋只有模型贴图 | 1 / 第 1 张 | 扎口粗麻袋，露出面包和小药瓶 |
| `temper_star.png` | `T_RuneCubeStars` 为小点图，无独立五角白热星轮廓 | 1 / 第 1 张 | 白热星芯、橙金五角边缘 |
| `ration.png` | `T_Food1_Icon_Inventory` 是裸面包，缺少包布与十字 | 1 / 第 1 张 | 布包面包、布上刺绣十字 |
| `holy_fire.png` | `T_Buff_Burning_Icon`、`T_Burning_Icon` 只有火焰，`T_HealingAuraOwner` 是光环 | 1 / 第 1 张 | 托住一簇圣金火焰的手掌 |
| `title_guardian.png` | `T_RoyalGuardShield` 是盾面 UV，无尖顶房子图案 | 1 / 第 1 张 | 粗轮廓的小盾，盾面尖顶房子 |
| `title_bard.png` | `T_HarpCrossbow` 是弩的 UV，没有独立竖琴轮廓 | 1 / 第 1 张 | 三色小竖琴 |
| `tab_fuse.png` | 工作台、商人操作和武器图标未见两剑交点带火的组合 | 1 / 第 1 张 | 两把交叉的剑，交点一团火 |
| `tab_salvage.png` | 拆解关键词命中界面控件、掉落资源和声音，未见断剑图标 | 1 / 第 1 张 | 断成两节的剑与散落碎片 |
| `ev_granary.png` | 苍蝇相关候选为环境粒子，未见独立苍蝇图标 | 1 / 第 1 张 | 黑绿轮廓、暗绿身体及亮绿翅膀 |
| `ev_hollow.png` | 未见无五官灰白脸图标；生图首张出现额头破洞，第 2 张填平 | 2 / 第 2 张 | 连续灰白皮肤的无脸头像 |
| `ev_witch.png` | 女巫相关命中怪物贴图和头像，未见火刑柱图标 | 1 / 第 1 张 | 木柱和底部火堆 |

图标提示词共用透明底、原生 16 格、左上高光、右下阴影和同色相深描边。称号以 `_tools/world_ref/art/title_*` 为参考，界面图标参考 `affix_*`，物品对照 `resourcepack/assets/rpg/textures/item/world/`。各项差异以表中主体提示为准。

## 特效竖条

每套从上至下每 32 像素为一帧。裁切各帧并归到 32×32 网格，使用固定色板和二值 Alpha。已逐帧检查动势与透明边缘，并对照 `resourcepack/assets/rpg/textures/item/michael_vfx/` 和 `force_vfx/` 的硬边与亮部用色。

| 成品 | 尺寸 / 帧数 | 原包来源与取舍 | 生图次数 / 采用 | 主体提示与成品处理 |
| --- | --- | --- | --- | --- |
| `fx_flies.png` | 32×256 / 8 | `P_Flies` 为运行时粒子系统，未见适用竖条 | 1 / 第 1 张 | 14 个黑绿小点，取生成首帧点群作 1–2 像素粒子，每帧推进 45° 相位并循环 |
| `fx_rev_circle.png` | 32×256 / 8 | `T_TotemOfRegenerationRunes` 为 128×128 散列白符号 | 1 / 第 1 张 | 紫色符文环，首帧逆时针按 45° 生成相位，中心每帧固定一枚暗红像素 |
| `fx_fuse_spark.png` | 32×192 / 6 | `dungeons/T_SparkSeq.png` 原尺寸 48×16，三格白碎星，作为生图编辑参考 | 1 / 第 1 张 | 白橙中心、向外溅出的金色火星，第 6 帧剩 6 个不透明像素 |
| `fx_holy_flame.png` | 32×256 / 8 | `dungeons/T_FireBlock1x1.png` 原尺寸 32×512、16 帧橙火，作为生图编辑参考 | 1 / 第 1 张 | 深金轮廓、接近白色的芯与左右轻摆的金白火苗 |

特效的原包路径如下。

- `Dungeons/Content/Decor/Prefabs/DingyJungle/Jungle_DesignAssets/Ruby/T_SparkSeq.uasset`
- `Dungeons/Content/Effects/Materials/Fire/FireBlock/T_FireBlock1x1.uasset`

## 人物贴图

七张均为 64×64 RGBA PNG。五套镇民共用 `resourcepack/assets/rpg/textures/item/merchant_smith/atlas.png`，已逐像素确认它与下列黑匠原图相同。其余村民原图用于查找对应服装。生成器重排了 UV 岛，因此选取生成稿的布料色块和纹理，按原商人 UV 回贴到外衣区域，再按原图明暗调整衣服。每套均恢复原头脸、眼鼻、手和颈，保留透明区域的 RGBA。

| 成品 | 原图文件（均 64×64） | 生图次数 / 采用 | 服装或面部提示 |
| --- | --- | --- | --- |
| `villager_farmer.png` | `dungeons/T_Villager_Blacksmith.png` 基底，`dungeons/T_Villager_Farmer.png` 参考 | 1 / 第 1 张 | 草帽色粗布、褐色围裙、卷袖口 |
| `villager_fisher.png` | 同一黑匠基底，`dungeons/T_Villager_Fisherman.png` 参考 | 1 / 第 1 张 | 灰蓝厚外套、黄褐油布围裙 |
| `villager_innkeeper.png` | `dungeons/T_Villager_Blacksmith.png` 基底及参考 | 1 / 第 1 张 | 酒红马甲、白衬衫、深色围裙 |
| `villager_child.png` | 同一黑匠基底，`dungeons/T_Villager_Unemployed.png` 参考 | 1 / 第 1 张 | 淡绿短上衣及布补丁 |
| `villager_elder.png` | 同一黑匠基底，`dungeons/T_Villager_Cleric.png` 参考 | 1 / 第 1 张 | 深绿长袍、金腰带、浅色毛领 |
| `hollow_land.png` | `dungeons/T_Zombie.png`，`SK_Zombie` 身体贴图 | 1 / 第 1 张 | 面部整块填成同一肤色，灰褐和旧白平民衣服 |
| `hollow_water.png` | `dungeons/T_Drowned.png`，`SK_Drowned` 身体贴图 | 1 / 第 1 张 | 两层面部 UV 各自填成单色，灰褐和旧白衣服，保留水草和青色身体 |

人物原包路径如下。

- `Dungeons/Content/Actors/Characters/Friendlies/Villager/T_Villager_Blacksmith.uasset`
- `Dungeons/Content/Actors/Characters/Friendlies/Villager/T_Villager_Farmer.uasset`
- `Dungeons/Content/Actors/Characters/Friendlies/Villager/T_Villager_Fisherman.uasset`
- `Dungeons/Content/Actors/Characters/Friendlies/Villager/T_Villager_Unemployed.uasset`
- `Dungeons/Content/Actors/Characters/Friendlies/Villager/T_Villager_Cleric.uasset`
- `Dungeons/Content/Actors/Characters/Enemies/Zombie/T_Zombie.uasset`
- `Dungeons/Content/Content_DLC5/Actors/Characters/Enemies/Drowned/T_Drowned.uasset`

## 自检结果

| 检查 | 结果 |
| --- | --- |
| 文件与格式 | 简报列出的 29 个文件名全部有对应的 RGBA PNG。另交 9 张原包 PNG |
| 16 网格 | 18 张图标均为 16×16，可见 RGB 为 3–12 色，两张称号各 3 色 |
| 动画 | 4 套均宽 32，帧数依次为 8、8、6、8，套内各帧像素均有变化 |
| Alpha | 29 张成品和 9 张原图的 Alpha 均只有 0 和 255 |
| 原图 | 与原包导出的 PNG 逐字节一致，保留原尺寸 |
| 镇民 UV | 五张均与商人原图的 Alpha 逐像素一致。每张仅调整 1,442 个可见衣服像素，实查保护区含 2,654 个头脸、颈、手及透明像素，均与原图相同 |
| 无脸 UV | 两张与各自原图的 Alpha 逐像素一致。僵尸的一块脸和溺尸的两块脸分别通过单色检查 |
| 目视 | 已检查放大图标、逐帧特效与人物贴图，验收范围为离线 PNG 与原模型 UV |

简报所列自检项均通过。


## 追加（2026-11-28）：寄往邻镇的信

| 成品 | 原包查找 | 生图次数 / 采用 | 成品规格 |
| --- | --- | --- | --- |
| `letter.png` | 已查本机《Minecraft Dungeons》PAK 索引。纸类候选为纸页贴图和附魔界面的卷轴纸面，未找到符合简报的信封图标。 | 内置 `image_gen` 1 次，采用第 1 张 | 16×16 RGBA PNG，10 个可见颜色，Alpha 仅有 0 和 255 |

绘制提示为微向右上倾斜的米黄折叠信封，三角封口压一枚小红蜡印，角上露出一截弯曲的细绳。主体使用左上奶油色高光、右下棕褐阴影和深棕单像素描边，保留透明背景和硬边。成品在 16 像素网格上收整了轮廓、蜡印与绳尾，并与 `town_badge.png`、`pact_scroll.png`、`map_shard.png` 做了并排目视检查。

## 追加（2026-11-28）：黑麦面包与腌熏肉

按 `town_models_ref/SKIN-BRIEF.md` 补画两张食物图标。先查本机 `D:/agent/dungeons_extract/index/pak_files.tsv`，食物目录命中 `Food1/T_Food1_Icon_Inventory`、`Food1/T_Bread_Minecraft` 与 `Food3/T_Food3_Icon_Inventory`、`Food3/T_Porkchop_Minecraft`，未查得名称明确对应黑麦或麻绳腌熏肉的资产。本次依补件的具体画面要求，在原生 16 像素网格上逐格新绘，未采用原包贴图。

| 成品 | 绘制次数 / 采用 | 画面与自检 |
| --- | --- | --- |
| `rye_bread.png` | 手工像素稿 1 次，采用第 1 稿 | 深褐圆头面包，三道斜割口露浅色面心。16×16 RGBA，7 个可见颜色，114 个不透明像素，Alpha 仅 0/255 |
| `smoked_meat.png` | 手工像素稿 1 次，采用第 1 稿 | 深红褐色熏肉，麦秆色麻绳交叉捆扎，右侧露白色脂肪边。16×16 RGBA，8 个可见颜色，128 个不透明像素，Alpha 仅 0/255 |

两张采用左上高光、右下阴影和深同色相轮廓。已与 `ration.png`、`welfare_pack.png`、`home_scroll.png` 并排放大目视检查，采用相近的暖褐与奶油高光色、硬边色块和透明背景。尺寸、色数和 Alpha 检查均通过。
