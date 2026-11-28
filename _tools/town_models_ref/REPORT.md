# 城镇外观交付

在 `_tools` 目录运行 `python add_town_models.py ../resourcepack ../rpg`。生成器直接读取 25 套 `*_dungeons_ref` 成品，构建时无需读取游戏安装或运行导出器。

以载体为 `@s` 调用 `#rpg:town_dress` 可按类型和标签换装。此入口把巨型空心人置于普通空心人之前。也可直接调用 `rpg:town_models/<key>/dress` 或 `rpg:town_models/<key>/anim/<动作>`。生成器把 `dress_any` 追加到原有函数标签，并注册模型跟随和动画所需的 tick、load 函数。道具由 `rpg:town_models/prop/<名>` 在当前执行位置与朝向摆放。

## 角色

显示实体数包含随载体移动的模型部件，守夜人的灯笼计为一个。骨骼栏依次为原作骨骼数与转换后的 Blockbench 组数，后者包含几何分组和挂件。高度为按比例换算的基准高度，动作栏记录源片段时长。

| key | 资产与材质 | 骨骼 / 组 | 显示实体 | 高度（格） | 动作（秒） |
| --- | --- | ---: | ---: | ---: | --- |
| `town_priest` | `SK_Player_Master` + Soul Robe / `T_SpiritRobe` 白底金边 | 38 / 74 | 25 | 1.87 | idle 3.333，talk 1.500 |
| `town_elder` | `SK_Villager` + `villager_elder.png` | 36 / 54 | 17 | 2.00 | idle 4.958，look 2.300 |
| `town_bard` | `SK_Player_Master` + Bard's Garb Unique1 / `T_BardsGarb_Unique1` | 38 / 76 | 27 | 1.87 | idle 3.333 |
| `town_watchman` | `SK_Player_Master` + Reinforced Mail / `T_ReinforcedMail`，右手原作挂点配 Java 原版灯笼 | 38 / 78 | 28 | 1.87 | idle 3.333 |
| `town_witch` | `SK_Player_Master` + Bard's Garb / `T_BardsGarb` 紫色版，省去头帽组件 | 38 / 74 | 26 | 1.87 | idle 3.333 |
| `town_edgewalker` | `SK_Player_Master` + Evocation Robe / `T_EvocationRobe` 紫色版，头部采用 Soul Robe 原作 `Helmet_SpiritRobe` 兜帽 | 38 / 76 | 25 | 1.87 | idle 3.333 |
| `town_inquisitor` | `SK_Player_Master` + Dark Armor / `T_DarkArmor` 黑底金边 | 38 / 77 | 29 | 1.87 | idle 3.333，walk 4.333，attack 0.800 |
| `town_folk_a` | `SK_Villager` + `villager_farmer.png` | 36 / 54 | 17 | 2.00 | idle 4.958，look 2.300 |
| `town_folk_b` | `SK_Villager` + `villager_fisher.png` | 36 / 54 | 17 | 2.00 | idle 4.958，look 2.300 |
| `town_folk_c` | `SK_Villager` + `villager_innkeeper.png`，比例 0.85 | 36 / 54 | 17 | 1.70 | idle 4.958，look 2.300 |
| `town_child` | `SK_Villager` + `villager_child.png`，比例 0.6 | 36 / 54 | 17 | 1.20 | idle 4.958 |
| `town_hollow` | `SK_Zombie` + `hollow_land.png` | 22 / 28 | 6 | 2.00 | idle 3.333，walk 1.667，attack 1.833 |
| `town_hollow_big` | `SK_DrownedNecromancer` + 原作 `DrownedNecromancer_02.png`，比例 1.8 | 35 / 61 | 18 | 3.60 | idle 6.200，walk 1.600，attack 1.833 |

- 英雄沿用 Valorie 皮肤贴图、装备蓝图组件变换和骨架挂点。英雄待机采用 `Player_Master_Idle_Glaive`，审判官移动和攻击采用 `Player_Master_Walk_Glaive` 与 `Player_Master_GlaiveUnique1Combo_Attack1`。牧师 talk 截取了待机前 1.5 秒。村民使用 `Villager_Idle` 与 `Villager_Idle_LookAround`，两种空心人对应各自原作 idle、walk 和 basic attack。各段精确时长和源资产路径见各目录的 `model_config.json`。
- 牧师将原袍的两档颜色映射至 `#FFD85A`、`#FFF2A8`，其余袍身映射白色明暗。女巫用 `#5B2C6F` 和 `#B48AD8` 分主布和饰边。边缘者的衣身与兜帽分别按原贴图 UV 映射紫色，以 `#A276BE` 为主色。审判官按原亮暗像素分配 `#2A2428` 黑底及 `#D4AF37` 金边。映射以源色和亮度为依据，保持坐标、像素网格与 Alpha。六张已验收的角色替换贴图继续沿用各自的原网格与 UV。
- 友方的源预览统一朝 +Z，显示管线使用 `turn=180`。走路由载体的水平位移驱动，攻击由原版 AI 命中目标后切入，攻击片段播完返回移动判定。换装只生成显示乘客并隐去原载体模型，AI、攻击伤害和声音由原载体及已有剧情接线提供。

## 静态道具

尺寸按 X 宽、Y 高、Z 深记录，单位为格。静态网格使用一个转换根组，吊笼保留 5 根源骨骼和原悬挂枢轴。其余道具的最低点按执行位置 Y 对齐。完整包路径、材料、尺寸及转换统计见 `prop_report.json`。

| key | 原作网格 | 骨骼或根组 | 显示实体 | 尺寸（格） |
| --- | --- | ---: | ---: | --- |
| `pyre` | `SM_Bonfire` | 1 | 17 | 3.056 × 2.733 × 2.645 |
| `cage` | `SK_HangingVillagerCage` | 5 | 4 | 2.250 × 3.623 × 2.246 |
| `grave_a` | `SM_Gravestone0` | 1 | 1 | 1.466 × 1.383 × 1.062 |
| `grave_b` | `SM_Gravestone1` | 1 | 1 | 0.710 × 0.677 × 0.635 |
| `candles_a` | `SM_EvilCandles_01` | 1 | 1 | 1.438 × 1.125 × 3.313 |
| `candles_b` | `SM_EvilCandles_02` | 1 | 1 | 1.008 × 0.813 × 1.398 |
| `cauldron` | `SM_Cauldron_Witch` | 1 | 9 | 2.500 × 2.192 × 1.544 |
| `bell` | `SM_Bell` | 1 | 1 | 3.000 × 3.938 × 0.875 |
| `barrel` | `SM_Barrel` | 1 | 1 | 1.000 × 1.438 × 1.000 |
| `crate` | `SM_Crate` | 1 | 1 | 1.000 × 1.000 × 1.000 |
| `crate_pile` | `SM_CratePile` | 1 | 1 | 1.476 × 2.000 × 2.125 |
| `cart` | `SM_CartBroken` | 1 | 16 | 3.416 × 1.466 × 3.856 |

柴堆、木桶、墓碑 A 和破车沿用原蓝图尺寸与朝向。墓碑 B 参照同目录墓碑 A 的蓝图比例。钟和锅由原始几何确定竖直朝向。道具使用原作 albedo，锅保留其同源发光层。继承自其他资产的通用发光贴图已排除，避免把宝箱或干草的纹理叠到道具表面。

## 验证

- 从空骨架生成了 13 套角色与 12 套道具。解析了隔离输出的 675 份 JSON，检查了 2,037 份函数文件中的模型、函数和纹理引用。以含原有字符串和可选对象项的 `town_dress` 标签重复生成，确认原项保留且 `dress_any` 只有一个。
- 逐张比对了四套装备的五张重配色贴图，原尺寸、逐像素 Alpha 和指定色值均通过检查。
- 本地 Java 1.21.11 隔离服验证了重复换装、重叠载体乘客分配、look 动作、巨型标签优先级、道具朝向、普通僵尸走路和实战命中切换、孤立部件回收。成人村民、幼年村民、1.8 倍巨型僵尸的乘坐偏移分别实测为 1.95、0.975、3.6225 格。
- 外观通过离线模型渲染抽查。游戏客户端的最终场景画面待接线后验收。自检输出目录已删除。

## 追加（2026-11-28）：六套英雄底子 NPC 换肤

六张 64×64 皮肤均取自同一份地下城英雄皮肤导出 `chartex/assets`。按下表为 `SK_Player_Master` 的 `MI_Valorie` 材质槽指定原作贴图，原包路径记在各成品的 `SOURCES.md`。

| key | 原作皮肤 | 可见特征 |
| --- | --- | --- |
| `town_priest` | `T_Pake_Skin.png` | 浅白胡须和眯眼，贴合年长神父 |
| `town_bard` | `T_Baako_Skin.png` | 短深色头发、年轻面容 |
| `town_watchman` | `T_Darian_Skin.png` | 红褐胡须、粗眉 |
| `town_witch` | `T_Hedwig_Skin.png` | 深色面部、紫红头发 |
| `town_edgewalker` | `T_Shikoba_Skin.png` | 深色发肤与紫色兜帽相衬 |
| `town_inquisitor` | `T_Warrior_Skin.png` | 冷灰头部配色、棱角分明的面部 |

从六个成品 `.bbmodel` 的待机首帧离线渲染预览，核对脸、眼睛和手部的贴合。逐像素比对确认图集差异限于皮肤及其烘焙图块，同时确认嵌入图集与 `atlas.png` 逐字节一致，元素、UV、骨架、盔甲贴图及动画数据与换肤前一致。

![六位城镇 NPC 换肤并排预览](_work/skin_review.png)
