# 世界掉落与锻造图标交付

日期：2026-11-23。依据同目录上级的 ART-BRIEF.md；本批只完成找图、绘图、像素导出和交付文件，未改物品定义、模型、字体映射或其他项目代码。

## 交付结果

18项：17张新绘的16×16透明PNG，以及1张保留原尺寸的地下城原包图纸素材。新绘材料为5–8色，六张称号各3色；全部生产PNG的Alpha仅0或255。总览见 PREVIEW.png，逐文件路径和SHA-256见 DELIVERY-MANIFEST.json。

原包素材优先：检索本机完整包索引的相关名称，并对候选导出/读取PNG进行目视。多数候选是模型表面展开图、场景纹理或半透明特效，不能直接代替简报要求的独立物品轮廓。采用一张原版纸张；其他17项新绘。没有把“未找到直接可用项”写成“游戏所有资源绝对不存在”。逐项检索依据见 item_source_search.md、element_source_search.md、title_source_search.md。

## 每项来源与采用版本

新绘使用内置 image_gen。绘制次数只统计生图调用，不把缩放、归并色板、透明度清理或选择采样位置算成新稿。

| ID / 名称 | 来源及次数 | 交付文件 | 尺寸 / 可见RGB色数 |
| --- | --- | --- | --- |
| `elite_badge` 精英徽记 | 绘制1次，采用第1张 | `elite_badge.png` | 16×16 / 5 |
| `sin_shard` 罪印碎片 | 绘制2次，采用第2张 | `sin_shard.png` | 16×16 / 5 |
| `blueprint_fragment` 图纸碎片 | 原包导出，未绘制 | `dungeons/T_Paper_Graph_02.png` | 32×32 / 10 |
| `blueprint_epic` 史诗图纸 | 绘制2次，采用第2张 | `blueprint_epic.png` | 16×16 / 7 |
| `blueprint_legend` 传说图纸 | 绘制2次，采用第2张 | `blueprint_legend.png` | 16×16 / 7 |
| `star_fragment` 星辰残片 | 绘制1次，采用第1张 | `star_fragment.png` | 16×16 / 6 |
| `wind_essence` 风之精魄 | 绘制1次，采用第1张 | `wind_essence.png` | 16×16 / 5 |
| `abyss_tear` 深海之泪 | 绘制1次，采用第1张 | `abyss_tear.png` | 16×16 / 6 |
| `molten_core` 熔核 | 绘制1次，采用第1张 | `molten_core.png` | 16×16 / 7 |
| `mountain_heart` 山岩之心 | 绘制1次，采用第1张 | `mountain_heart.png` | 16×16 / 7 |
| `temple_bronze` 圣殿铜 | 绘制1次，采用第1张 | `temple_bronze.png` | 16×16 / 6 |
| `grave_soil` 墓土 | 绘制1次，采用第1张 | `grave_soil.png` | 16×16 / 8 |
| `title_gate` 所罗门的门户 | 绘制1次，采用第1张 | `title_gate.png` | 16×16 / 3 |
| `title_ledger` 所罗门的账簿 | 绘制1次，采用第1张 | `title_ledger.png` | 16×16 / 3 |
| `title_waverer` 摇摆者 | 绘制1次，采用第1张 | `title_waverer.png` | 16×16 / 3 |
| `title_grandmaster` 大团长的朋友 | 绘制1次，采用第1张 | `title_grandmaster.png` | 16×16 / 3 |
| `title_meteor` 白昼流星 | 绘制1次，采用第1张 | `title_meteor.png` | 16×16 / 3 |
| `title_merchant` 被商人记恨 | 绘制1次，采用第1张 | `title_merchant.png` | 16×16 / 3 |

## 原版图纸的准确来源

- 原包路径：`Dungeons/Content/Decor/Prefabs/_Lab/Paper/T_Paper_Graph_02.uasset`。
- 游戏包位置：`D:/XboxGames/Minecraft Dungeons/Content/Dungeons/Content/Paks`。
- 导出文件：`dungeons/T_Paper_Graph_02.png`，原生32×32，10色，Alpha 0/255。
- SHA-256：`b11770722668582048e2d3cc771f5fa12a67e8ab9460e16af697c3440a0f57ac`。
- 已与本次候选导出的PNG逐字节核对一致，没有裁切、缩放、改色或透明度处理。

这张原图是带旧线稿的破边羊皮纸，供 `blueprint_fragment` 使用；它仍是完整原版纸张素材，尚不是裁成一角的16×16碎片。遵循简报“原图不是16×16的，导出原尺寸，我们来裁切和补边”，本批保留32×32交给后续适配，不另伪造一个16×16原版文件。

## 新绘与像素处理

17项共进行了20次生成。`sin_shard`、`blueprint_epic`、`blueprint_legend`各重画一次并采用第二张：罪印改为被断边截开的暗刻痕；两张图纸加宽纸面，用直刃、横护手和短柄表达武器线稿，分别保留紫绳与金绳/金边。其余14项采用第一张。

生成器底稿为1254×1254，不能直接当作16×16资源交付。按用户已经批准的文件级像素处理，使用 `export_native.py`：裁出有效Alpha区域、等比例最近邻取样至最大边14像素、居中放进16×16画布、归并到每张指定色板、Alpha以128为阈值变为0或255。无双线性或平滑缩放。

星晶、铜锭、史诗图纸和天平使用明确记录的采样位移，保留白色星点、十字压印、紫绳及天平盘底。账本色板收敛为深炭灰紫的黑皮明暗与纸页色。全部参数、每次提示词、生成原文件路径、采用次数在 `generation_manifest.json`；20张原始生成图保存在 `_generation/`，原生成文件亦保留原位。

像素整理只处理新绘底稿；原版纸张从未进入导出脚本的缩放分支。预览中的放大图只供查看，生产文件保持其上表尺寸。

## 验证

- 新绘17张均16×16、RGBA，Alpha集合恰为0和255；可见色全部来自各自受控色板；无可见纯黑像素。
- 罪印碎片每个可见像素均R=G=B，可供后续染色。
- 六张称号各3色。已查看16像素原图、放大图和8像素缩小预览；天平在8像素会合并托盘内部空隙，保留的是双盘、横梁与中央柱的整体意象。
- 已目视核对明暗方向、独立轮廓、主材料与关键符号；程序统计和PNG哈希见 `validation.json`。预览背景、中文名称不在生产PNG内。
- 未做游戏内字体注册、物品模型替换或实际客户端显示测试；这些不属于本次美术简报。

## 文件说明

- `world_art.zip`：18项生产图、总览、报告、三份原图检索记录、生成记录、验证数据、导出脚本及20张生成底稿。
- `PREVIEW.png`：6列×3行总览，包含原尺寸/2倍查看，称号另外显示8像素检查图。
- `DELIVERY-MANIFEST.json`：18项ID到生产文件的映射，原版纸张不在根目录伪装成新绘文件。
- `_inspection_*`：本机候选和采样检查资料，不属于交付图，不收入ZIP。

重新导出新绘图：在装有Pillow的Python环境执行 `python export_native.py`。脚本从随包的 `_generation/` 读取底稿，可重复生成17张PNG、validation.json和PREVIEW.png，不依赖桌面软件。


---

## 追加：精英词缀图标（2026-11-23）

完成与复核日期：2026-11-24。

已按更新后的ART-BRIEF.md追加11张精英怪名牌词缀图标，全部为16×16透明PNG，各3色，Alpha仅0或255，并包含指定Hex主色。此前18项生产图逐文件SHA-256核对未变化。累计交付29项生产图：28张16×16新绘图和1张保留32×32的原版图纸。

### 来源与尝试次数

先在本机原版包中查找并实际查看候选。附魔卡面常见256×256、复杂背景和多级透明；其他候选在主色、轮廓或主体上不符。原版小雪花与单骷髅仅作参考部件保留，未补边、改色或缩放：雪花为6×6白色单色，单骷髅为7×7白色单色，三枚原宽无法横排进16像素。本批11张最终字形因此新绘，详细候选包路径与尺寸见affix_source_a.md、affix_source_b.md、affix_source_c.md。

| 文件 | 词缀 | 指定主色 | 来源、绘制与采用次数 | 交付规格 |
| --- | --- | --- | --- | --- |
| `affix_swift.png` | 迅捷 | `#62D9E8` | 内置image_gen绘制1次，采用第1张 | 16×16 / 3色 |
| `affix_iron.png` | 铁壁 | `#B5B5B5` | 内置image_gen绘制1次，采用第1张 | 16×16 / 3色 |
| `affix_rage.png` | 狂怒 | `#FF6B5E` | 内置image_gen绘制1次，采用第1张 | 16×16 / 3色 |
| `affix_leech.png` | 吸血 | `#D97AD9` | 内置image_gen绘制2次，采用第2张 | 16×16 / 3色 |
| `affix_frost.png` | 寒霜 | `#E8F4FF` | 内置image_gen绘制1次，采用第1张 | 16×16 / 3色 |
| `affix_venom.png` | 剧毒 | `#70DB70` | 内置image_gen绘制1次，采用第1张 | 16×16 / 3色 |
| `affix_burst.png` | 爆裂 | `#FFA15C` | 内置image_gen绘制1次，采用第1张 | 16×16 / 3色 |
| `affix_summon.png` | 召唤 | `#A276BE` | 内置image_gen绘制2次，采用第2张 | 16×16 / 3色 |
| `affix_taint.png` | 罪染 | `#C86A92` | 内置image_gen绘制2次，采用第2张 | 16×16 / 3色 |
| `affix_holy.png` | 圣印 | `#FFD85A` | 内置image_gen绘制1次，采用第1张 | 16×16 / 3色 |
| `affix_champion.png` | 首领 | `#FFAA00` | 内置image_gen绘制1次，采用第1张 | 16×16 / 3色 |

本批共14次内置image_gen调用。原始生成图保存在 `_generation_affix/`；每次提示词、原生成文件路径、采用稿、三色调色板及采样偏移均记录于 `affix_generation_manifest.json`。原尺寸参考文件的精确路径、尺寸与哈希见 `affix_REFERENCE-MANIFEST.json`，三张参考不计入11张生产图。

### 像素整理与检查

使用用户此前批准的文件级像素处理：将新绘底稿裁至有效Alpha范围、最近邻采样至16×16画布、映射到指定三色调色板、清理为二值Alpha。通过取样位置选择保留形体和关键符号，不对原版参考图做缩放或改色。普通高分辨率生成稿不作为最终16×16资源。

吸血、召唤、罪染分别重画一次并采用第二稿，纠正了问号状獠牙、粘连的头部和与瞳孔融合的裂纹。召唤单独采用14×7有效区的非等比最近邻缩放与[-0.4,0.4]采样位移，保留三组成对眼窝和短颌；8px下相邻头部仍会连成紧凑组形，按三头整体意象辨认。其余图标采用等比例缩放。

- 11张实际PNG均16×16、RGBA、Alpha集合为0和255、3色；指定Hex主色真实存在于像素中，无可见纯黑或半透明边。
- 已检查16px原尺寸及8px最近邻缩小预览；总览中另放大8px结果供查看。静态字形检查不等于游戏客户端验证。
- 名牌图标仅表达各自轮廓和核心符号，圣印的亮感由金色和浅色块表示，最终PNG不带外发光或投影。
- 数据和哈希在 `affix_validation.json`；ID到文件映射在 `affix_DELIVERY-MANIFEST.json`。没有修改字体注册、名牌逻辑或其他项目代码。

### 新增交付文件

- `affix_*.png`：本次11张生产图。
- `AFFIX_PREVIEW.png`：新增11张总览，含16px、8px名牌示意、8px放大检查。
- `affix_icons.zip`：本次新增图及来源、验证、生成底稿、复现脚本。
- `world_art.zip`：已更新为全部29项生产图及两批记录；原版参考仍单列，不冒充词缀成品。
- `export_affix.py`：只复现这11张新图及其预览、验证文件；与随包 `export_native.py` 放在同一目录，装有Pillow后运行 `python export_affix.py`。
