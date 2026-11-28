你要在一个已有的 Minecraft Java 1.21.11 数据包+资源包项目里，用《Minecraft Dungeons》本体的原始资产，给城镇里的人、副本里的怪和几样小道具做外观。全程用中文回复。下面写明的直接照做，不用再调研。

## 1. 已有的东西

- **仓库：** `D:\agent\claude\github-create\tralancer-rpg-1.21.11`
- **游戏：** `D:\XboxGames\Minecraft Dungeons`。只读，不改、不移动、不整体复制 pak。
- **提取工具与索引：** `D:\agent\dungeons_extract\`（`exporter\` 已调通，`index\pak_files.tsv` 是全部文件路径）。
- **转换管线：** `_tools/dungeons_models.py`、`_tools/dungeons_conversion/`；显示管线 `_tools/display_mob.py`。
- **参考范例：**
  - 村民网格 + 换材质：`_tools/add_merchant_models.py`（四位商人，`SK_Villager`）。
  - 英雄网格 + 地下城盔甲：`_tools/add_jacques_model.py` 与 `dungeons_models.py` 里的 `jacques` 配置（`socket_attach`、原作挂点），`_tools/add_saul_*`、`_tools/add_daath*` 也是这一套。
  - 静态道具：`_tools/add_eden_gate.py` 旁边用到的地下城道具做法，或任何现有的 `item_display` 静态模型。
- **新贴图（Codex 上一轮交付，已验收）：** `_tools/town_ref/art/`
  - `villager_farmer.png`、`villager_fisher.png`、`villager_innkeeper.png`、`villager_child.png`、`villager_elder.png`：和 `resourcepack/assets/rpg/textures/item/merchant_smith/atlas.png` 同一 UV。
  - `hollow_land.png`（SK_Zombie 的身体贴图改成无脸）、`hollow_water.png`（SK_Drowned 同理）。

## 2. 要做的外观

载体实体由我来召唤，你只做「给载体穿上」。每个 key 生成 `rpg:town_models/<key>/dress`（以载体执行、at 载体脚下；挂上模型并跟随）和需要的 `rpg:town_models/<key>/anim/<动作>`。
另外生成一个总入口 `rpg:town_models/dress_any`：按下表的标签判断该穿哪一套，并把它加进函数标签 `#rpg:town_dress`（`data/rpg/tags/function/town_dress.json`，追加，不要覆盖已有的值）。

| key | 载体与标签 | 网格与材质 | 动作 |
| --- | --- | --- | --- |
| `town_priest` | NoAI 村民，`rpg.tnpc.priest` | 英雄网格 + **Soul Robe**，袍子重配色成白底金边（圣金 `#FFD85A`、浅金 `#FFF2A8`） | idle、talk（有就用，没有用 idle 的一段） |
| `town_elder` | NoAI 村民，`rpg.tnpc.elder` | `SK_Villager` + `villager_elder.png` | idle、look |
| `town_bard` | NoAI 村民，`rpg.tnpc.bard` | 英雄网格 + **Bard's Garb_Unique1** | idle |
| `town_watchman` | NoAI 村民，`rpg.tnpc.watchman` | 英雄网格 + **Reinforced Mail**，手里提一盏灯（原版灯笼的 item_display 也行） | idle |
| `town_witch` | NoAI 村民，`rpg.tnpc.witch` | 英雄网格 + **Bard's Garb**，重配色成暗紫（`#5B2C6F`、`#B48AD8`）；不要尖帽 | idle |
| `town_edgewalker` | NoAI 村民，`rpg.tnpc.hood` | 英雄网格 + **Evocation Robe**，兜帽拉下，配色紫（`#A276BE`） | idle |
| `town_inquisitor` | **卫道士**（会走会打），`rpg.te.inq` | 英雄网格 + **Dark Armor**，重配色黑底金边（`#2A2428`、`#D4AF37`） | idle、walk、attack |
| `town_folk_a` | NoAI 村民，`rpg.tnpc.farmwife` | `SK_Villager` + `villager_farmer.png` | idle、look |
| `town_folk_b` | NoAI 村民，`rpg.tnpc.farmer` | `SK_Villager` + `villager_fisher.png` | idle、look |
| `town_folk_c` | NoAI 村民，`rpg.tnpc.lad` | `SK_Villager` + `villager_innkeeper.png`，整体缩到 0.85 | idle、look |
| `town_child` | NoAI 幼年村民，`rpg.tnpc.child` | `SK_Villager` + `villager_child.png`，整体缩到 0.6 | idle |
| `town_hollow` | **僵尸**，`rpg.te.hol`（不带 `rpg.te.big`） | `SK_Zombie` + `hollow_land.png` | idle、walk、attack |
| `town_hollow_big` | **僵尸**（体型属性 1.8），`rpg.te.big` | `SK_DrownedNecromancer`（原贴图），模型按载体体型放大 | idle、walk、attack |

英雄网格用 `SK_Player_Master`，盔甲用原作的盔甲网格与原贴图（重配色的那几套只改颜色，不改图案）。友方 NPC 原作朝 +z，显示时整体转 180°（`turn`，同商人）。
会动的载体（卫道士、僵尸）要跟随走路与攻击切换动作，照 `add_tower_guard.py` / 罪仆那一套。

## 3. 静态道具

每样生成 `rpg:town_models/prop/<名>`：在执行位置放一个（或一组）`item_display`，带标签 `rpg.tw.prop`、`rpg.tw.prop.<名>`，朝向用执行时的朝向。

| 名 | 原件 | 用在 |
| --- | --- | --- |
| `pyre` | `SM_Bonfire` | 刑台下的柴堆 |
| `cage` | `SK_HangingVillagerCage`（静止一帧就行） | 广场上关女巫的吊笼 |
| `grave_a`、`grave_b` | `SM_Gravestone0`、`SM_Gravestone1` | 墓地 |
| `candles_a`、`candles_b` | `SM_EvilCandles_01`、`SM_EvilCandles_02` | 林中祭坛 |
| `cauldron` | `SM_Cauldron_Witch` | 边缘者营地 |
| `bell` | `SM_Bell` | 教堂门口 |
| `barrel`、`crate`、`crate_pile` | `SM_Barrel`、`SM_Crate`、`SM_CratePile` | 粮仓里的杂物 |
| `cart` | `SM_CartBroken` | 商队的破车 |

## 4. 交付

- 每个 key 一个 `_tools/<key>_dungeons_ref/`（`dungeons_models.py` 的输出格式）。
- 一个生成器 `_tools/add_town_models.py`：运行方式 `python add_town_models.py ../resourcepack ../rpg`，写出上面所有函数、模型与贴图，并把 `rpg:town_models/dress_any` 追加进 `#rpg:town_dress`。
- 贴图是原作导出的，重配色的几套只做颜色映射；`ART-STYLE.md` 第 4 节对「作者原画例外」的处理照旧。
- 声音用原版的，不要下载新的。
- 报告写在 `_tools/town_models_ref/REPORT.md`：每个 key 用了哪些资产、骨骼数、实体数、重配色的做法、各段动作的时长；道具的尺寸。
- 自检：**不要往 `../resourcepack`、`../rpg` 里写**（那边可能正在构建）。自检时输出到 `_tools/town_models_ref/test_rp` 与 `_tools/town_models_ref/test_dp`（先在 test_dp 里建一个只有 `data/rpg/tags/function/` 的空骨架），跑通、JSON 都能解析就算过；自检目录做完删掉。

不要改 `build.sh`，也不要改别的生成器；我来接线。不要向我提问，做完为止。
