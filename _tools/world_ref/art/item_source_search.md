# 世界物品原包检索记录：徽记、图纸、圣殿铜、墓土

本记录只提供经包索引定位、原尺寸导出并实际目视的候选与取舍依据，最终采用项由主代理选择。未改项目代码、原包或已有成品图。没有把候选缩放、裁切、补边、改色或清理Alpha。检查时的放大仅在内存中显示，未另存预览图片。

## 搜索范围与提取依据

- 简报：`../ART-BRIEF.md`。负责 `elite_badge`、`blueprint_fragment`、`blueprint_epic`、`blueprint_legend`、`temple_bronze`、`grave_soil` 六项。
- 全包索引：`D:/agent/dungeons_extract/index/pak_files.json`。按 scroll / parchment / blueprint / paper / badge / medal / token / coin / trophy / elite / copper / bronze / ingot / soil / dirt / grave / bone 及相关 UI 分类检索，并跟读材质引用，非仅在已有导出小集合搜索。
- 原包根：`D:/XboxGames/Minecraft Dungeons/Content/Dungeons/Content/Paks`。CLI只读游戏包。
- 既有工具：`D:/agent/dungeons_extract/exporter/bin/Release/net8.0/exporter.exe`；CUE4Parse 1.2.2 / Conversion 1.2.1、UE4.22。通过 `UTexture2D.Decode` 导出首个可用Mip，PNG记录明确 `first available mip, no resizing`。
- 初次23包：29对象、0失败；补充6包：6对象、0失败。共取得26张PNG；其余为材质/表达式元数据。日志见 `_inspection_badges/export_report.json` 与 `_inspection_badges/more/export_report.json`，每对象原路径见对应 `metadata/`。

## 六项结论（候选，不代替最终选稿）

| 任务项 | 原图候选与结论 |
| --- | --- |
| elite_badge | `mapicon_raidcaptain` 最具精英敌人/战利品标记语义，但实际是灰铁面盔，不是暗金金属章。其余候选为白头骨、粉红强力符号或UI边框。若必须保留暗金实体徽章与中间獠牙，新绘更贴合；若优先原图，可由主代理选择队长面具作为明确折中。 |
| blueprint_fragment | `T_Paper_Graph_02` 是旧纸残页，有卷角、撕边和图示线；最值得优先目视。它不是单一三角纸角，但语义适合纸质图示碎片。`Graph_01` 是另一张方格图表整页。 |
| blueprint_epic | Graph两张可承担图纸语义，但没有紫色细绳和武器图示；若稀有度差异是关键，应新绘，不应把现有纸页描述成原版紫绳卷轴。 |
| blueprint_legend | 同上，没有金色系绳或烫金纸边。现有UI卷轴是大尺寸拼接部件，不适合作为完整物品图。 |
| temple_bronze | `T_Gold_GearIcon` 是现成完整金属锭图，24×24、8色、二值Alpha；但视觉是鲜亮黄金，无旧青铜/十字。`T_GoldBar`、`T_IronIngots_Small` 只是UV。若不能接受黄金替代青铜，应新绘。 |
| grave_soil | 没找到能独立读作一捧土的候选。所见Dirt是地表平铺，Gravestone是墓石UV，TastyBone是肉骨头，DirtNap是竹笋复活预览；都不能满足墓土的基本物件语义，应新绘。 |

## 原尺寸PNG逐项核验

颜色数只计Alpha大于0的可见RGB；Alpha列列出所有取值或档数。即便原图不是16×16、色数超过32或有半透明，也保留原样导出并在此明示，不据此声称它已满足最终游戏贴图规格。

| 原PNG / 本地路径 | 原尺寸 | 可见色数 | Alpha | 实际目视与适合度 |
| --- | --- | ---: | --- | --- |
| [T_TastyBone_GearIcon.png](_inspection_badges/assets/Dungeons/Content/Actors/Items/TastyBone/T_TastyBone_GearIcon.png) | 24×24 | 10 | 0/255 | 红褐肉块连白骨的小型物品，是肉骨头；不能冒充混骨墓土。 |
| [BadOmens_Icon.png](_inspection_badges/assets/Dungeons/Content/Actors/Items/Tokens/BadOmens_Icon.png) | 64×64 | 2 | 0/254/255 | 白色獠牙面具/灾厄头形，可作战斗符号；不是暗金金属徽章。还含Alpha254，不能称二值透明。 |
| [mapicon_dificulty.png](_inspection_badges/assets/Dungeons/Content/Actors/Items/Tokens/DifficultyToken/mapicon_dificulty.png) | 64×64 | 12 | 255 | 灰铁面盔、红眼与底部火焰，整张不透明方底；不是独立金属徽章。 |
| [mapicon_raidcaptain.png](_inspection_badges/assets/Dungeons/Content/Actors/Items/Tokens/DifficultyToken/mapicon_raidcaptain.png) | 64×64 | 14 | 0/255 | 灰铁面盔与红眼，有明确精英/队长战斗语义；可作原图优先的风格折中候选，但不是暗金奖章。 |
| [mapicon_mystery.png](_inspection_badges/assets/Dungeons/Content/Actors/Items/Tokens/MysteryToken/mapicon_mystery.png) | 64×64 | 39 | 0/255 | 灰白面盔/骷髅与红眼，可作危险代币符号；39可见色且与暗金徽记描述差距大。 |
| [T_Gold_GearIcon.png](_inspection_badges/assets/Dungeons/Content/Content_DLC4/Actors/Items/Gold/T_Gold_GearIcon.png) | 24×24 | 8 | 0/255 | 明确独立金锭图标，可用于金属锭语义。鲜亮金黄，不是旧青铜，也无十字压印；是否接受由主代理决定。 |
| [T_CW_Dirt.png](_inspection_badges/assets/Dungeons/Content/Content_DLC4/Decor/Materials/PropMaterials/T_CW_Dirt.png) | 32×32 | 7 | 255 | 暗褐土壤平铺纹理，无土堆轮廓、骨片或锈钉；不能直接当墓土。 |
| [Loader_hunt_badge.png](_inspection_badges/assets/Dungeons/Content/Content_DLC4/UI/Materials/LoadingScreen/Loader_hunt_badge.png) | 26×26 | 274 | 255 | 紫色四符号方框加载徽记，全不透明，274色；属于UI牌面，非战利品物件。 |
| [T_DirtAtlas.png](_inspection_badges/assets/Dungeons/Content/Decor/Prefabs/_BambooBluffDecor/T_DirtAtlas.png) | 16×16 | 84 | 255 | 褐色地表图集，全不透明、84色；没有土堆/骨片/锈钉物件形。 |
| [T_Paper_Graph_01.png](_inspection_badges/assets/Dungeons/Content/Decor/Prefabs/_Lab/Paper/T_Paper_Graph_01.png) | 32×32 | 11 | 0/255 | 可供图纸类选稿：旧羊皮纸整页，有方格与红色折线。不是武器线稿；无紫/金系绳。 |
| [T_Paper_Graph_02.png](_inspection_badges/assets/Dungeons/Content/Decor/Prefabs/_Lab/Paper/T_Paper_Graph_02.png) | 32×32 | 10 | 0/255 | 图纸碎片最值得优先目视：破边、卷角、旧纸与红色示意线清楚。仍是较完整残页，不是单一三角纸角；无紫/金系绳。 |
| [T_Paper_Text_01.png](_inspection_badges/assets/Dungeons/Content/Decor/Prefabs/_Lab/Paper/T_Paper_Text_01.png) | 32×32 | 14 | 0/255 | 文字/符号纸页，旧纸材质和破边可参考；可读作档案，图纸语义弱于Graph两张。 |
| [T_Paper_Text_02.png](_inspection_badges/assets/Dungeons/Content/Decor/Prefabs/_Lab/Paper/T_Paper_Text_02.png) | 32×32 | 12 | 0/255 | 卷角文字纸页，旧纸材质可参考；没有武器图示与稀有度系绳。 |
| [T_IronIngots_Small.png](_inspection_badges/assets/Dungeons/Content/Decor/Prefabs/Anvil/T_IronIngots_Small.png) | 16×16 | 18 | 255 | 铁锭模型UV面及红色剩余区，全不透明；不适合直接作青铜锭物品。 |
| [T_GoldBar.png](_inspection_badges/assets/Dungeons/Content/Decor/Prefabs/Coins/T_GoldBar.png) | 16×16 | 9 | 0/255 | 带展开面和底部色条的模型UV；不是独立透视金锭图标，不能因名称GoldBar直接采用。 |
| [T_Gravestone0.png](_inspection_badges/assets/Dungeons/Content/Decor/Prefabs/Gravestone/T_Gravestone0.png) | 64×64 | 15 | 255 | 墓石模型UV，多块石面与深色背景；不是一捧墓土。 |
| [T_TrophyShield.png](_inspection_badges/assets/Dungeons/Content/Decor/Prefabs/ShieldDecorative/T_TrophyShield.png) | 32×32 | 16 | 0/255 | 木盾+银边，外侧还有支架/附属UV区域；不是暗金小徽记，整张不能当物品贴图。 |
| [T_DirtNapRespawnFlair_cosmetic.png](_inspection_badges/assets/Dungeons/Content/UI/Materials/Cosmetics/02/T_DirtNapRespawnFlair_cosmetic.png) | 512×512 | 3743 | 255 | 512方形复活特效预览：竹笋、绿色地面与浮粒，带背景；名称含Dirt但不符合墓土。 |
| [paperbackleft.png](_inspection_badges/assets/Dungeons/Content/UI/Materials/Inventory2/Enchantment/Scroll/paperbackleft.png) | 2048×2048 | 306 | 248档（0–255） | 2048方形大型UI羊皮纸左侧面板/边缘，有248档Alpha；不是可直接用的卷轴物品。 |
| [papercenter.png](_inspection_badges/assets/Dungeons/Content/UI/Materials/Inventory2/Enchantment/Scroll/papercenter.png) | 20×1520 | 15 | 0/255 | 20×1520的UI中缝长条；可作界面拼接，非完整纸张/卷轴。 |
| [boss_skull.png](_inspection_badges/more/assets/Dungeons/Content/UI/Materials/Boss/boss_skull.png) | 128×64 | 6 | 13档（0–255） | 白色长角头骨及投影/暗部，128×64、13档Alpha；战斗符号而非暗金实体徽记。 |
| [levelicon_hard.png](_inspection_badges/more/assets/Dungeons/Content/UI/Materials/Difficulty/levelicon_hard.png) | 50×50 | 1 | 40档（0–255） | 白色骷髅轮廓，50方形、40档Alpha；没有金属材质或奖章形。 |
| [levelicon_insane.png](_inspection_badges/more/assets/Dungeons/Content/UI/Materials/Difficulty/levelicon_insane.png) | 61×50 | 1 | 63档（0–255） | 白色长角骷髅轮廓，61×50、63档Alpha；没有金属材质或奖章形。 |
| [powerful_icon.png](_inspection_badges/more/assets/Dungeons/Content/UI/Materials/Inventory2/Enchantment/Inspector/powerful_icon.png) | 128×128 | 45 | 0/3/4/111/112/255 | 粉红菱形内嵌黑骷髅，是强力UI符号；45色且含半透明，非暗金金属徽记。 |
| [unique_bullit.png](_inspection_badges/more/assets/Dungeons/Content/UI/Materials/Inventory2/Inspector/unique_bullit.png) | 67×58 | 136 | 120档（0–255） | 橙金六角空心小UI点，67×58、136色/120档Alpha；无尖角/獠牙标记，也不是实物奖章。 |
| [enchant_powerful_icon.png](_inspection_badges/more/assets/Dungeons/Content/UI/Materials/Mobs/enchant_powerful_icon.png) | 33×34 | 1 | 0/2/17/18/27/28/255 | 洋红色抽象方旋纹，单色UI符号且含半透明；不是徽记物件。 |

## 精确原包路径

以下路径来自包索引并由实际导出元数据确认；扩展名为 `.uasset`。上表链接给出原尺寸源PNG。

| PNG | 原包路径 |
| --- | --- |
| T_TastyBone_GearIcon.png | `Dungeons/Content/Actors/Items/TastyBone/T_TastyBone_GearIcon.uasset` |
| BadOmens_Icon.png | `Dungeons/Content/Actors/Items/Tokens/BadOmens_Icon.uasset` |
| mapicon_dificulty.png | `Dungeons/Content/Actors/Items/Tokens/DifficultyToken/mapicon_dificulty.uasset` |
| mapicon_raidcaptain.png | `Dungeons/Content/Actors/Items/Tokens/DifficultyToken/mapicon_raidcaptain.uasset` |
| mapicon_mystery.png | `Dungeons/Content/Actors/Items/Tokens/MysteryToken/mapicon_mystery.uasset` |
| T_Gold_GearIcon.png | `Dungeons/Content/Content_DLC4/Actors/Items/Gold/T_Gold_GearIcon.uasset` |
| T_CW_Dirt.png | `Dungeons/Content/Content_DLC4/Decor/Materials/PropMaterials/T_CW_Dirt.uasset` |
| Loader_hunt_badge.png | `Dungeons/Content/Content_DLC4/UI/Materials/LoadingScreen/Loader_hunt_badge.uasset` |
| T_DirtAtlas.png | `Dungeons/Content/Decor/Prefabs/_BambooBluffDecor/T_DirtAtlas.uasset` |
| T_Paper_Graph_01.png | `Dungeons/Content/Decor/Prefabs/_Lab/Paper/T_Paper_Graph_01.uasset` |
| T_Paper_Graph_02.png | `Dungeons/Content/Decor/Prefabs/_Lab/Paper/T_Paper_Graph_02.uasset` |
| T_Paper_Text_01.png | `Dungeons/Content/Decor/Prefabs/_Lab/Paper/T_Paper_Text_01.uasset` |
| T_Paper_Text_02.png | `Dungeons/Content/Decor/Prefabs/_Lab/Paper/T_Paper_Text_02.uasset` |
| T_IronIngots_Small.png | `Dungeons/Content/Decor/Prefabs/Anvil/T_IronIngots_Small.uasset` |
| T_GoldBar.png | `Dungeons/Content/Decor/Prefabs/Coins/T_GoldBar.uasset` |
| T_Gravestone0.png | `Dungeons/Content/Decor/Prefabs/Gravestone/T_Gravestone0.uasset` |
| T_TrophyShield.png | `Dungeons/Content/Decor/Prefabs/ShieldDecorative/T_TrophyShield.uasset` |
| T_DirtNapRespawnFlair_cosmetic.png | `Dungeons/Content/UI/Materials/Cosmetics/02/T_DirtNapRespawnFlair_cosmetic.uasset` |
| paperbackleft.png | `Dungeons/Content/UI/Materials/Inventory2/Enchantment/Scroll/paperbackleft.uasset` |
| papercenter.png | `Dungeons/Content/UI/Materials/Inventory2/Enchantment/Scroll/papercenter.uasset` |
| boss_skull.png | `Dungeons/Content/UI/Materials/Boss/boss_skull.uasset` |
| levelicon_hard.png | `Dungeons/Content/UI/Materials/Difficulty/levelicon_hard.uasset` |
| levelicon_insane.png | `Dungeons/Content/UI/Materials/Difficulty/levelicon_insane.uasset` |
| powerful_icon.png | `Dungeons/Content/UI/Materials/Inventory2/Enchantment/Inspector/powerful_icon.uasset` |
| unique_bullit.png | `Dungeons/Content/UI/Materials/Inventory2/Inspector/unique_bullit.uasset` |
| enchant_powerful_icon.png | `Dungeons/Content/UI/Materials/Mobs/enchant_powerful_icon.uasset` |

## 未形成PNG的追踪结果

- `Dungeons/Content/UI/Materials/MissionSelectMap/inspector/trial/VariationBadge.uasset` 是材质，实际纹理引用 `Dungeons/Content/UI/Materials/Chests/asset_secretchest.0`，属于宝箱提示，不是独立精英奖章；没有把材质名当作徽章图。
- `Dungeons/Content/UI/Materials/Inventory2/Enchantment/Scroll/LeftScroll.uasset` 与 `RightScroll.uasset` 是材质实例，引用 `ScrollFlipbook`；同目录导出的 `paperbackleft` 与 `papercenter` 证实为界面大纸面拼接部件，不是带紫/金系绳的物品卷轴。
- Copper命中包括玩家Copper皮肤、导电装置和海底铜像/锈蚀雕像贴图；不是青铜锭图。Blueprint名称大量命中UE逻辑蓝图，未把这些代码包当作图纸贴图。

记录边界：检索覆盖全索引的相关命名与分类，并目视上述26张目标候选，不是对全游戏每一张无关贴图逐张穷举。因此“未找到合适项”表述的是本次有据的搜索结果。
