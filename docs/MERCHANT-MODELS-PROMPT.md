你要在一个已有的 Minecraft Java 1.21.11 数据包+资源包项目里，用《Minecraft Dungeons》本体的原始资产做四位商人的外观。全程用中文回复。下面写明的直接照做，不用再调研。

## 1. 已有的东西

- **仓库：** `D:\agent\claude\github-create\tralancer-rpg-1.21.11`
- **游戏：** `D:\XboxGames\Minecraft Dungeons`。只读，不改、不移动、不整体复制 pak。
- **提取工具与索引：** `D:\agent\dungeons_extract\`（`exporter\` 已调通，`index\pak_files.tsv` 是全部文件路径）。
- **转换管线：** `_tools/dungeons_models.py`、`_tools/dungeons_conversion/`。
- **显示管线：** `_tools/display_mob.py`。
- **参考范例：** `_tools/add_mammon_model.py` 和它用的 `_tools/lord_look.py`。玛门就是地下城的猪灵商人，商人是友方 NPC，原作朝 +z，显示时整体转 180°（`turn`）。

## 2. 要做的四位商人

网格都是同一个村民：`Dungeons/Content/Actors/Characters/Friendlies/Villager/SK_Villager`。区别在材质实例和头上的道具（都在 `Friendlies/Villager/` 和 `Friendlies/Villager/Merchants/` 下）。

| key | 用途 | 材质 | 道具 |
| --- | --- | --- | --- |
| `merchant_smith` | 铁匠 | `MI_Villager_Blacksmith` | 无 |
| `merchant_mystery` | 神秘商人 | `MI_Villager_MysteryMerchant` | `SM_MysteriousMerchantCap` |
| `merchant_luxury` | 奢侈品商人 | `MI_Villager_LuxuryMerchant` | `LuxuaryMerchantHat`（材质）与对应网格；如果帽子网格是 `SM_Crown`，用它 |
| `merchant_travel` | 迷途商人（随机事件里出现） | `MI_Villager_TravellingMerchant` | 原作有就带上 |

道具要挂在头骨上，位置照原作的挂点；找不到挂点就按眼睛看到的对齐，并在报告里写明。

## 3. 动作

`Friendlies/Villager/Animations/` 下：

| 原作动作 | 项目里的名字 | 循环 |
| --- | --- | --- |
| `Villager_Idle` | `idle` | 是 |
| `Villager_Idle_LookAround` | `look` | 否 |
| `Villager_Bowing` | `bow` | 否（成交时播） |
| `Villager_Examining` | `examine` | 否（打开交易时播） |

## 4. 交付

- 每位商人一个 `_tools/<key>_dungeons_ref/`（`dungeons_models.py` 的输出格式）。
- 一个生成器 `_tools/add_merchant_models.py`，照 `add_mammon_model.py` 的写法：
  - 运行方式 `python add_merchant_models.py ../resourcepack ../rpg`；
  - 每个 key 生成 `rpg:<key>/dress`（以载体实体执行，给它挂上模型并跟随）和 `rpg:<key>/anim/<动作>`（播一次指定动作）；
  - 载体是一只 `NoAI`、无敌、不可见的村民，带标签 `rpg.mer` 和 `rpg.mer.<key 去掉 merchant_ 的部分>`（例如 `rpg.mer.smith`）。逻辑那一侧（交易、摆放、事件）我来写，你不用管。
- 声音用原版村民的音效，不要下载新的。
- 贴图是原作导出的，不要自己重画；网格规则照 `ART-STYLE.md` 第 4 节对「作者原画例外」的处理。
- 报告写在 `_tools/merchant_models_ref/REPORT.md`：每位商人用了哪些资产、骨骼数、实体数、道具的挂点、各段动作的时长。

不要改 `build.sh`，也不要改别的生成器；我来接线。
