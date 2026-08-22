# TRALANCER RPG — 1.21 → 1.21.11 升级（数据包 + 材质包）

目标版本：**Java 版 1.21.11**
数据包格式 `94.1`，资源包格式 `75.0`（数值取自本机 `1.21.11-Fabric.jar` 内的 `version.json`，非猜测）

## 目录说明

| 路径 | 内容 |
| --- | --- |
| `rpg\` | **升级后的数据包**，放进 `存档\datapacks\` |
| `resourcepack\` | **升级后的材质包**，放进 `.minecraft\resourcepacks\` |
| `rpg-datapack-1.21.11.zip` | 数据包的 zip 版（同内容，方便分发） |
| `rpg-resourcepack-1.21.11.zip` | 材质包的 zip 版 |
| `TRALANCER-RPG-图鉴.html` | **数据包图鉴**（可直接双击打开；另有在线版链接） |
| `_orig\` / `_orig_rp\` | 原始 1.21 数据包 / 材质包备份（未改动） |
| `_tools\` | 迁移、优化、校验、启动测试脚本 |

材质包已经顺带装进你的 1.21.11 实例里了：
`新建文件夹\versions\1.21.11-Fabric\resourcepacks\rpg_resourcepack_claude`
——进游戏在「选项 → 资源包」里启用即可（你 `options.txt` 里选中的仍是 ChatGPT 那版，我没有改动它）。

首次使用数据包需要像以前一样手动跑一次 `function rpg:command/soreboard` 建计分板。

---

# 第一部分：数据包

`pack.mcmeta` 按 1.21.9 之后的新格式重写（`supported_formats` 已废除，改为 `min_format` / `max_format`）：

```json
{ "pack": { "description": "TRALANCER RPG!", "pack_format": 94,
            "min_format": [94, 1], "max_format": 94 } }
```

共改写 **126 个文件**。括号内为改动处数。

## 1.1 版本迁移

### 实体 NBT

| 变更 | 说明 |
| --- | --- |
| `ArmorItems` / `HandItems` → `equipment` (140) | 1.21.5 合并为 `equipment:{head/chest/legs/feet/mainhand/offhand/body/saddle}` |
| `ArmorDropChances` / `HandDropChances` → `drop_chances` (87) | 改为按槽位命名的复合标签 |
| `SaddleItem` → `equipment.saddle` (8)、`body_armor_item` → `equipment.body` (5) | 马鞍与马铠并入 `equipment` |
| **玩家 `Inventory` 槽位 100–103 / −106 → `equipment` (39)** | 1.21.5 起玩家盔甲和副手已不在 `Inventory` 里，`nbt={Inventory:[{Slot:102b,…}]}` 这类判定恒为假 |
| `CustomName` 由 JSON 字符串改为 SNBT 文本组件 (113) | 1.21.5 起文本组件不再是 JSON 字符串 |
| 属性 ID 去掉分类前缀 (629) | `generic.max_health` → `max_health`、`player.entity_interaction_range` → `entity_interaction_range` |
| 空占位物品被丢弃 | `ArmorItems:[{Count:1},{},…]` 里没有 `id` 的占位项在新 `equipment` 里非法 |
| **补齐短向量 (48)** | `Rotation:[0f]`(38 处) → `[0f,0f]`、`Motion:[0d,0.2d]`(10 处) → `[0d,0.2d,0d]`。1.21.5 起向量长度严格校验，短一位整条 `summon` 直接失败——**你现在游戏日志里那条 `Failed to decode value '[0.0d,0.2d]' from field 'Motion'` 就是它** |

### 物品组件

| 变更 | 说明 |
| --- | --- |
| `custom_name` / `lore` 由 JSON 字符串改为 SNBT (221) | 否则物品名会原样显示成一串 JSON |
| `enchantments={levels:{…}}` → `enchantments={…}` (80) | 1.21.5 去掉了 `levels` 一层 |
| `attribute_modifiers={modifiers:[…]}` → `[…]` (45) | 直接是列表 |
| 属性修饰符 `id` 加引号 (111) | `id:1730544989627` 这种裸数字不是合法的命名空间 ID |
| `dyed_color={rgb:N}` → `dyed_color=N` (48) | 1.21.5 起是纯整数 |
| `custom_model_data=N` → `{floats:[N.0f]}` (66) | 1.21.4 改成多字段结构 |
| `fire_resistant={}` → `damage_resistant={types:"#minecraft:is_fire"}` (6) | 1.21.5 替换 |
| `show_in_tooltip` / `hide_additional_tooltip` → `tooltip_display` (28) | 统一到 `tooltip_display={hidden_components:[…]}` |
| **`food.eat_seconds` → `consumable.consume_seconds` (26)** | 1.21.5 起只有 `food` 组件的物品右键用不了，所有靠右键触发的镶嵌技能会全部失灵 |

### 战利品表 / 物品修饰器 / 进度

* `set_attributes` 的属性名同样去前缀。
* `set_custom_model_data` 的 `value` 字段已不存在 → 改写为
  `set_components → minecraft:custom_model_data:{floats:[…]}`（6 处）。
* 12 个 `minecraft:using_item` 进度原本靠 `food.eat_seconds` 的唯一数值区分武器，
  现改为精确匹配 `minecraft:consumable`；物品侧与判定侧写的是**完全相同的完整组件**，
  精确匹配依然成立。
* 进度 `display.background`：1.21.5 起是贴图 ID 而不是文件路径，
  `rpg:textures/…/cracked_deepslate_bricks.png` → `rpg:gui/advancements/backgrounds/cracked_deepslate_bricks`。
  材质包里的图片**不需要移动**（`textures/<id>.png` 就是解析规则，已用原版 jar 核对）。
* `trim_material/holy.json`：删除 1.21.5 已移除的 `ingredient` 与 `item_model_index`。
* `attribute @s minecraft:generic.armor get` → `minecraft:armor`。

## 1.2 卡顿优化

### 病因

每 tick 由 `#minecraft:tick` 触发的命令里有 **634 条带 `nbt={…}` 的选择器**：

* 640 条 `@a[nbt={SelectedItem:{components:{"minecraft:custom_data":{…}}}}]`
* 495 条 `@e[type=item,nbt={Item:{…}}]`
* 约 140 条 `nbt={Tags:[…]}` / `equipment`

`nbt=` 匹配会把**整个实体序列化成 NBT** 再比对；对玩家来说包含整个背包，一次就是几百微秒，
每 tick 六百多次足以吃掉几十到几百毫秒。再加上 `legend1.mcfunction` 里 380 行各自做一次
全世界 `@e` 扫描、并对**每个实体**执行 `data get entity @s Health`（同样是整体序列化），
服务端 tick 必然爆炸。

### 做法

1. **每 tick 建一次标签索引**（新增 `rpg:command/index`，排在 `#minecraft:tick` 最前）。
   88 个 custom_data 标志各判定一次，结果缓存成实体 tag：

   ```
   execute as @a if items entity @s weapon.mainhand *[minecraft:custom_data~{saber_tag:1b}] run tag @s add rpg.h.saber_tag1
   ```

   用 1.21.2 加入的 `execute if items` + 物品子谓词 `~`，**直接读槽位，不做实体序列化**。
   随后包内 1285 处 `nbt=…` 选择器全部改写成 `tag=rpg.h.… / rpg.i.… / rpg.e.…`。
2. **伤害检测重做**（`rpg:command/damage_scan`、`rpg:command/tick_end`）：
   改成以每个玩家为中心、只扫 64 格内、排除投射物 / 掉落物 / 展示实体
   （新增实体类型标签 `rpg:no_damage_track`，条目带 `required:false`，不怕将来改名）；
   受伤实体打 `rpg.hurt` 标签，`legend1` 的 178 行判定换成 `as @e[tag=rpg.hurt]`，顺序不变。
3. **怪物出生装备合并**（`rpg:command/spawn/*`）：骷髅/僵尸/苦力怕每族每 tick 6–11 次
   全实体扫描 → 3 次。保留两段式结构，掷骰召唤出的新怪同样能拿到装备。
4. **`@e` 收窄**：只可能打在玩家身上的标签，`@e[…]` 直接改成 `@a[…]`（10 处）。
5. **`nbt={Tags:["x"]}` → `tag=x`**（105 处），语义等价。
6. `rpg:entities/drowned/magic`（3568 条粒子命令的法阵）加了 `if entity @a[distance=..48]` 前置判断。

### 效果

| 指标（每 tick） | 优化前 | 优化后 |
| --- | ---: | ---: |
| 带 `nbt=` 的选择器 | **634** | **1** |
| 选择器综合开销估值 | 18 536 | 4 104 |
| 全实体 `data get entity Health` | 全世界所有实体 | 玩家 64 格内的生物 |

## 1.3 行为差异（有意的取舍）

1. **标志索引在 tick 开始时计算**：物品 custom_data 若在同一 tick 内被 `item modify` 改动，
   新值下一 tick 才被选择器看到（延迟 50 ms）。合成/洗练/附魔这类链式流程结果一致。
2. **伤害检测只覆盖玩家 64 格内的实体**：武器特效都要求攻击者手持特定物品
   （`SelectedItem` 只有玩家才有），近战/弓箭都在 64 格内，实际无影响。
3. **护甲标志只索引玩家**：`chestplate_tag` 这类判定本来就是玩家属性面板用的。

## 1.4 实机验证

`_tools/server_test.py` 用本机的 1.21.11 客户端 jar（里面自带 `net.minecraft.server.Main`）
起了一个**无窗口的专用服务器**，把数据包装进一个真实存档加载，然后从控制台喂命令进去。

* 服务端在加载时会逐行解析全部 94 个函数、战利品表、物品修饰器、进度——
  任何语法/组件错误都会带文件名和行号打到控制台。结果：**0 条**。
  这同时证明新写的 `execute if items entity @s weapon.mainhand *[minecraft:custom_data~{…}]`
  在 1.21.11 上是合法语法。
* 又直接执行了 **79 条真实命令**（60 条各不相同的 `summon`、16 条 `loot spawn`、
  16 条 `item modify`、以及 `index / tick / legend1 / warden / tick_end` 五个 tick 函数）。
  这一步才暴露出上面那两个短向量 bug；修好后重跑，除了「测试存档里没有 `green` 队伍」
  之外**没有任何报错**。

```
There are 2 data pack(s) enabled: [vanilla (built-in)], [file/rpg (world)]
```

## 1.5 数据包剩余事项

1. **`/team add green`**：`entities/illager/wind_vindicator` 召唤的卫道士带 `Team:green`，
   队伍不存在时服务端会刷 `Unable to add mob to team "green"`。你的正式存档里若已有这个队伍就无需处理。
2. **`legend1.mcfunction` 第 102–105 行是原包就有的死代码**
   （`advancement revoke @s …` / `execute as @s …` 直接写在函数顶层，没有执行实体，每 tick 静默报错）。
   属于原有 bug，本次原样保留，未擅自改动玩法。
3. **42 个函数没有被任何地方引用**：`command/give/*`、`command/soreboard`、`command/summon`
   这些显然是给管理员手动调用的；但 `item/sword/legend/legend`、`saber/saber`、`wukong/wukong`
   等是被 `legend1` 取代的旧版本，可以考虑删掉以缩短加载时间。同样未擅自删除。
4. **`rpg:holy` 纹饰不能再用下界之星在锻造台合成**：1.21.5 删掉了纹饰材料的 `ingredient` 字段，
   改由物品的 `minecraft:provides_trim_material` 组件提供。本包实际是用 `rpg:command/holy`
   物品修饰器直接赋予纹饰的，玩法不受影响；若想恢复锻造合成，给发放的下界之星加上
   `provides_trim_material="rpg:holy"` 组件即可。

---

# 第二部分：材质包

源文件用的是 `.minecraft\resourcepacks\rpg_resourcepack`（`pack_format 34` 的原版），
不是 `F:\AGENT\codex\rpg_resourcepack`——后者已经是 ChatGPT 改过的版本（`min_format 75`），
从原始文件重做才不会把它的问题继承下来。

`pack.mcmeta`：

```json
{ "pack": { "description": "TRALANCER RPG!", "pack_format": 75,
            "min_format": [75, 0], "max_format": 75 } }
```

## 2.1 三处结构性变化

### ① 1.21.4：`overrides` 彻底失效，改用「物品定义」

旧写法把 `custom_model_data` 判断写在 `models/item/*.json` 的 `overrides` 里，
1.21.4 起这个字段被忽略。新增 `assets/minecraft/items/` 下 9 个物品定义：

`netherite_sword` `netherite_axe` `mace` `totem_of_undying` `quartz`
`bow` `crossbow` `iron_axe` `netherite_chestplate`

* 纯 `custom_model_data` 的（剑/斧/锤/图腾/石英）→ `range_dispatch` on `minecraft:custom_model_data`，`index: 0`
  （正好对应数据包写的 `custom_model_data={floats:[N.0f]}`）。
* **弓**：`custom_model_data` 外层 × 每个变体内部再套
  `condition minecraft:using_item` + `range_dispatch minecraft:use_duration`（0.65 / 0.9 三段拉弓）。
* **弩**：`custom_model_data` 外层 × 每个变体内部
  `select minecraft:charge_type`（arrow / rocket）+ `condition using_item`
  + `range_dispatch minecraft:crossbow/pull`（0.58 / 1.0）。
  两套自定义弩（`crossbow_*` 与 `soul_hunter/crossbow_*`）都完整还原。
* **`trim_type` 预测值 → `select minecraft:trim_material`**（铁斧、下界合金胸甲）。
* 24 个模型文件里已失效的 `overrides` 段一并删掉（18 个文件）。

### ② 1.21.4：物品贴图从 `blocks` 图集搬到 `items` 图集

原包把纹饰覆盖层声明在 `atlases/blocks.json` 里，现在必须放 `atlases/items.json`，
否则 `chestplate_trim_holy`、`axe_trim_*` 这些拼合贴图根本不会生成。
已删除 `blocks.json`，新建 `items.json`（两个 source：原版四件套 + `holy`；自定义斧纹饰 + 全部 12 种材质）。

### ③ 1.21.5：盔甲纹饰贴图整体搬家 — **ChatGPT 那版漏掉的就是这条**

`trims/models/armor/<pattern>` → `trims/entity/humanoid/<pattern>` 和
`trims/entity/humanoid_leggings/<pattern>`。
原包（以及 ChatGPT 升级后的包）仍写着旧路径，结果 36 张纹饰底图全部找不到，
`holy` 自定义纹饰在盔甲上完全不显示。已按 1.21.11 原版的 36 条路径重写 `atlases/armor_trims.json`。

## 2.2 顺手修掉的旧毛病

* **`holy` 胸甲图标以前根本不会出现**。旧写法用 `trim_type: 1.1` 判断，
  而 `holy` 材质的 `item_model_index` 是 `0.45`，永远匹配不到 1.1。
  新的 `select` 按材质 ID 匹配（`when: "rpg:holy"`），现在真的能显示了。
* 旧的胸甲纹饰指向 `netherite_chestplate_netherite_darker_trim`，该模型在 1.21.11 已不存在；
  现在直接以原版 1.21.11 的物品定义为底再追加 `holy` 分支。
* 铁斧原本只有 9 种纹饰模型（漏了 `iron`），旧的阈值判断会退化成显示相邻材质的贴图；
  `select` 没有这种「就近退化」，所以补齐了 `iron` / `resin` / `holy` 三个模型（只是换一行贴图名）。
* `enchanted_glint_entity.png` → 1.21 已更名为 `enchanted_glint_armor.png`（原文件名早已无效）。
* 删除 3 个 1.19 时代的死文件（`enchanted_item_glint.png` 及其 mcmeta）和 4 个
  美工工程文件（`.pdn` / `.bbmodel`，游戏根本不读，白占体积）。

## 2.3 实机验证

写了两层验证：

**静态**（`_tools/rp_validate.py`）——以本机真实的 `1.21.11-Fabric.jar` 为准，
解析所有物品定义 / 模型 / 图集 / 字体 / 音效，把每个 `parent`、`textures.*`、
图集 source、`palette_key`、permutation 逐个解析到具体文件，并把
`paletted_permutations` 生成的虚拟贴图（如 `chestplate_trim_holy`）算作已存在。
同时报告「覆盖了 1.21.11 已经不存在的原版路径」这种沉默失效。

**实机**（`_tools/launch_test.py`）——用本机 Zulu 21 直接拉起 1.21.11 客户端
（独立的临时 gameDir，不碰你正在运行的实例，也不加载任何 mod），
等资源重载完成后读日志。同一套条件下两个包的对照结果：

| | ChatGPT 版 | 本次版本 |
| --- | ---: | ---: |
| 静态校验问题数 | 39 | **0** |
| 客户端日志 `Unable to find texture` | **36** | **0** |
| 15 张图集拼合 | 成功 | 成功 |

（唯一剩下的日志报错是 `Failed to fetch user properties`——离线账号登录，和材质包无关。）

## 2.4 材质包剩余事项

* `assets/rpg/textures/mob_effect/*.png`（7 张）放在 `rpg` 命名空间下，
  而原版状态效果图标读的是 `assets/minecraft/textures/mob_effect/`，
  所以这几张图**从来就没生效过**。原包就是这样，未擅自搬动——
  想让它们生效的话把目录改成 `assets/minecraft/textures/mob_effect/` 即可。
* `assets/minecraft/font/default.json` 只声明了本包新增的字形提供器；
  字体文件在各资源包之间是**合并**而不是覆盖，所以原版字体不受影响，无需补全。

---

# 第三部分：存档升级

升级后的存档已放在 **`新建文件夹ersions.21.11-Fabric\saves\新的世界 (4)`**，进 1.21.11 直接就能进。
原存档 `.minecraft\saves\新的世界 (4)` **原封未动**，可作备份。

## 3.1 做了什么

1. **整档转换**：用 1.21.11 客户端 jar 内自带的专用服务器跑 `--forceUpgrade`，
   把 **15 070 个方块区块 + 717 个实体区块 + POI** 全部过一遍 DataFixerUpper，
   而不是留给游戏边走边转。`level.dat` 的 `Data.DataVersion` 已由 `3953` 变为 `4671`，
   `Version.Name` 为 `1.21.11`。
2. **换上新数据包**：`datapacks/rpg` 替换为本次升级后的版本。
3. **顺带修好另外两个数据包**：存档里还有 `custom_trim_material_dp` 与 `custom_trimmable_item_dp`
   两个示例包，格式停留在 `pack_format 48`、标签目录还是 1.21 之前的 `tags/items/`，
   在 1.21.11 会直接加载失败。已一并升到 `94.1`、目录改为 `tags/item/`、
   并删除纹饰材料里 1.21.5 已移除的 `ingredient` / `item_model_index`。
4. **实机校验**：转换后再启动一次服务器确认加载正常：

```
There are 4 data pack(s) enabled: [vanilla (built-in)],
  [file/custom_trim_material_dp (world)], [file/custom_trimmable_item_dp (world)], [file/rpg (world)]
```

## 3.2 需要知道的两件事

1. **玩家背包里的旧物品会在第一次进档时才转换。**
   `level.dat` 里的 `Data.Player`（以及 `playerdata/*.dat`）仍是 `DataVersion 3953`——
   专用服务器不碰单人玩家数据，要等客户端加载时由原版 DataFixerUpper 转换。
   转换是自动的，但如果某件**旧的**镶嵌武器右键技能不触发，
   把它重新取一份（`/function rpg:command/give/weapon`）即可，新发的物品一定是新格式。
2. **三个 mod 数据包会提示缺失**：存档启用列表里有 `fabric`、`fabric-convention-tags-v2`、`axiom`。
   前两个由 Fabric API 提供（你的 1.21.11 实例已装），`axiom` 需要装 Axiom 模组，
   不装的话只是启动时一条提示，不影响游戏。

---

# 第四部分：数据包图鉴

给玩家看的说明书：起始配置流程、八大核心系统、69 件武具与符文的完整数据、
四大阵营生物图鉴、十二章剧情、指令速查。

* 在线版（可分享）：<https://claude.ai/code/artifact/3285549a-4550-45a0-8c19-5dc9617dc37b>
* 本地版：`TRALANCER-RPG-图鉴.html`，双击即可用浏览器打开

图鉴里的物品数据不是手写的，而是用 `_tools/extract_items.py` 直接从
`rpg:command/give/*` 的 give 指令里解析出来的——名称、稀有度、Lore、技能、
附魔、属性修饰符全部与数据包实际内容一致。生物数据同理来自各 `summon` 指令。

---

# 第五部分：本轮补充

## 5.1 战利品表里的装备（已补进图鉴第 VII 节）

之前的图鉴只收了 `give` 指令里写死的物品。战利品表里还有 **116 件**装备，
它们的属性是<b>区间随机</b>的，所以之前没被整理进去。现在全部补上了：

| 表 | 内容 |
| --- | --- |
| `rpg:trial/epic_sword` | **6 件精英武器**（血煞弯刀／严寒风暴／珊瑚突刺／珊瑚冲击／三叉钢刀／极寒之镰），带技能，锻造台用传说冶炼石产出 |
| `rpg:armor/*` | 怪物随身携带的武器与四件套护甲，共 49 条，`[uncommon]`～`[epic]` |
| `rpg:trial/*` | 试炼刷怪笼掉落的同类装备，数值更高，共 49 条 |
| `rpg:trial/trial(_ominous)` | 试炼奖励池，含试炼之匙、不死图腾、货币等，按权重列出了单抽概率 |
| `rpg:trial/valuable(_ominous)` | 珍品池 |

图鉴里每一条都标了**属性区间**（例如「攻击伤害 +6 ~ +9.5」）、随机附魔次数、
耐久损耗范围和被抽中的权重百分比。

## 5.2 材质包里没被使用的贴图

用 `_tools/unused_textures.py` 对着模型、图集、字体三处引用做了反查，105 张贴图里 38 张没有被引用。
其中大部分是<b>正常的</b>——原版会直接按固定路径读取它们：

* `gui/title/background/panorama_0..5`、`gui/title/edition`：主界面全景图，由游戏硬编码读取
* `misc/enchanted_glint_armor`、`enchanted_glint_item`：附魔光效，同样是硬编码
* `item/diamond_sword` 等 6 张：覆盖原版贴图，由**原版模型**引用
* `rpg:gui/advancements/backgrounds/*`：由**数据包**的进度引用，不是材质包内部引用

真正闲置的是 **21 张自定义武器贴图**，都是成套的、画好了却从没接上去的：

| 贴图组 | 张数 | 内容 |
| --- | ---: | --- |
| `azure_seeker*` | 6 | 蓝色弩，含拉弓 3 帧 + 箭 / 烟花火箭 |
| `baby_crossbow*` | 7 | 粉色小弩，含拉弓 3 帧 + 箭 / 烟花火箭，另有一张 `baby_crossbows` 双弩备用图 |
| `burst_gale_bow*` | 4 | 金色弓，含拉弓 3 帧 |
| `vine_whip` / `vine_whip_cast` | 2 | 绿色藤鞭，`_cast` 是抛出状态 → 钓竿 |
| `truthseeker` | 1 | 黑红长剑 |
| `mojang_banner_pattern` | 1 | 旗帜图案 |

## 5.3 用这些贴图做出来的五件装备

`/function rpg:command/give/extra`

| 装备 | 基底 | 品级 | 技能 | 关键属性 |
| --- | --- | --- | --- | --- |
| **蔚蓝追寻者** | 弩 | 传说 | 被动·潮涌（消耗 3 级经验射出潮涌之箭） | 穿透 4／力量 4／快速装填 3，氧气 +4 |
| **稚弩** | 弩 | 史诗 | 被动·毒药（箭矢附带剧毒） | 快速装填 4／多重射击／穿透 2，移速 +5% |
| **疾风迸发之弓** | 弓 | 传说 | 被动·连发（连续发射箭矢） | 力量 5／冲击 2／无限，移速 +10% |
| **藤蔓之鞭** | 钓竿 | 史诗 | 被动·淬毒（攻击时持续流血） | 攻击 +5、攻速 −1.5、**交互距离 +2** |
| **求真之刃** | 下界合金剑 | 史诗 | 被动·萤火（1/5 概率标记敌人并重击） | 攻击 +9、攻速 −2.4，锋利 4 |

做法上刻意遵守了三条约束：

1. **格式与既有装备完全一致**——稀有度前缀、两行诗、技能栏、`+---+` 分隔线、
   `custom_data` 标签、`custom_model_data` 编号，都照抄现有写法。
2. **技能复用已有处理逻辑**（`bubble` / `hunter` / `projectiles` / `potion` / `ink`），
   所以每刻命令数一条没增加，性能开销为零；它们同样能参与洗练、镶嵌、附魔、升级。
3. **材质包侧补齐了 19 个模型 + 5 个物品定义**，其中 `fishing_rod` 是新建的
   （原包没有钓竿定义），按原版形状写成「`custom_model_data` × 抛竿状态」两层结构。

模型编号分配：弩 `1110003`／`1110004`，弓 `1110002`，钓竿 `1110001`，下界合金剑 `1110011`——
都避开了已占用的编号。

**验证**：五条 `give` 指令已在真实 1.21.11 专用服务器上加载通过。
为确认这个检查不是摆设，还做了一次反向对照：故意把其中一个组件写回 1.21 的旧格式
（`enchantments={levels:{…}}`），服务器立刻报出
`Failed to load function rpg:command/give/extra … Whilst parsing command on line 4`，
改回后归零。

---

# 第六部分：本轮返工

## 6.1 教条战斧 —— 补进数据包

它的**技能逻辑和九个纹饰模型一直都在包里**（`legend1.mcfunction` 第 398–427 行、
`rpg:item/iron_axe_*_trim`），唯独 `give` 指令不在数据包里，所以之前既没被迁移、也没进图鉴。

现在它已迁移到 1.21.11 并写进 `rpg:command/give/weapon`：

| 迁移项 | 改动 |
| --- | --- |
| `custom_name` / `lore` | JSON 字符串 → SNBT |
| `enchantments={levels:{looting:1}}` | → `{looting:1}` |
| `attribute_modifiers={modifiers:[…]}` | → `[…]` |
| `generic.attack_damage` / `generic.attack_speed` | → 去前缀 |
| **两个修饰符共用同一个 `id`** | 拆成 `rpg:doctrine_axe/0` 与 `/1` —— 1.21.2 起同 id 会互相覆盖，这是原写法里的隐患 |

**锻造后的十种形态**（图鉴里已列成表）：给它镶上不同纹饰材质，攻击特效与外观同时改变。

| 纹饰 | 攻击时 |
| --- | --- |
| 钻石 | 目标缓慢 III·2s + 不祥试炼粒子 |
| 铁 | **自身**获得抗性提升 2s + 铁块柱粒子 |
| 金 | 目标受 2 点火焰伤害 + 金色流光 |
| 石英 | 目标凋零 III·2s + 横扫粒子 |
| 下界合金 | 目标黑暗 5s + 墨汁粒子 |
| 红石 | **自身**瞬间治疗 + 红石柱粒子 |
| 铜 | 目标缓慢 VI·1s + 铜绿流光 |
| 绿宝石 | 目标迅捷 III·2s（削弱其攻击节奏）+ 翠绿流光 |
| 青金石 | 不祥降临 + 附魔粒子 |
| 紫水晶 | 目标被向上掀起 + 紫色流光 |

## 6.2 五件新装备的贴图尺寸

原因不是模型，是**画布占比**：游戏会把物品贴图拉伸填满物品栏格子，所以决定视觉大小的是
"画面占画布多少"。包里原有武器都在 82–100%，而三张闲置贴图只有 34–66%，于是显得小一圈。

修法是**只裁剪、不重采样**（`_tools/fix_art.py`），按整套动画帧的并集包围盒裁成正方形，
一个像素都没有被缩放或插值：

| 贴图组 | 画布 | 画面占比 |
| --- | --- | --- |
| `baby_crossbow`（6 帧） | 32×32 → **12×12** | 38% → 100% |
| `vine_whip`（2 帧） | 32×32 → **17×17** | 53% → 100% |
| `truthseeker` | 32×32 → **21×21** | 66% → 100% |
| `azure_seeker`（6 帧）、`burst_gale_bow`（4 帧） | 不变 | 本来就是 100% |

同一套动画的所有帧共用一个裁剪框，拉弓/装填过程不会抖动。
`baby_crossbows`（备用双弩图）没有被任何模型引用，特意排除在包围盒之外，
否则会把真正在用的六帧一起撑小。

## 6.3 五个原创技能

之前那版复用了已有技能标签，等于抄。现在每件都有**自己的标签、自己的实现**
（`rpg:item/extra/*`，五个函数 + 一个入口）：

| 装备 | 技能 | 机制（包内独一份的地方） |
| --- | --- | --- |
| **蔚蓝追寻者** | 被动·**深潜** | 命中生物时把它**向下**拽（`Motion -1.1`）并叠加缓慢 IV + 挖掘疲劳。潮涌是往上抛，这个是往下拖 |
| **稚弩** | 被动·**顽劣** | **完全不加伤害**：反胃 + 虚弱 II + 发光 10s，纯粹让目标难受且无处可藏 |
| **疾风迸发之弓** | 被动·**裂空** | 命中点炸开风隙：**三格范围 AoE** 3 点伤害并把目标掀起。包里唯一的箭矢范围技 |
| **藤蔓之鞭** | 被动·**缠绕** | `facing entity … run tp @s ^ ^ ^1.4` 把目标**朝自己拽近**并钉住。包里没有第二个位移拉扯技；玩家只吃减速不被拉，避免 PvP 变筛子 |
| **求真之刃** | 被动·**洞悉** | 命中即发光；**目标生命值 < 20 时追加 4 点真实伤害**。血量直接读 `damage_action`——那是索引每刻已经抓好的，等于零额外开销的处决机制 |

代价：每刻命令数 1070 → **1145**（+75），选择器开销 4104 → 4562。
仍远低于优化前的 18 536，且带 `nbt=` 的选择器依旧是 1 个——
五个新标签都注册进了 `rpg:command/index`，走的是 `if items` 那条廉价路径。

**实机验证过程中服务器抓到我自己写的两个 bug**，都已修掉：

1. `damage @e[distance=..3,…]` —— `damage` 只接受**单个**目标，
   报 `Only one entity is allowed…`。改成先 `execute as @e[…] run damage @s`。
2. `particle flash` —— 1.21.9 起 `flash` 变成需要 `color` 参数的粒子，
   报 `Can't parse particle options: No key color`。换成 `enchanted_hit`。

修完重跑：六个技能函数全部加载并执行，零报错。

## 6.4 图鉴加上了贴图

`_tools/icons.py` 按客户端的解析顺序取图：
物品定义 → `custom_model_data` 分支 → 模型 → `textures.layer0`，
材质包里没覆盖的就回退到 1.21.11 原版 jar 里的贴图。
取到的 PNG 以 base64 内嵌进页面（Artifact 的 CSP 不允许外链图片），
用 `image-rendering:pixelated` + `object-fit:contain` 统一放进 46×46 的框里，
表格里则是 30×30。

**196 张图标，零加载失败。** 只有「玩家面板」这类头颅类物品没有平面贴图，留了占位框。

---

# 第七部分：鞭子连击与爆炸闪光

## 7.1 先把粒子语法试出来

`flash` 与 `tinted_leaves` 在 1.21.11 都要求 `color`，但**三元浮点会被拒绝**。
直接在专用服务器上把六种写法各跑一遍，结论：

| 写法 | 结果 |
| --- | --- |
| `flash{color:[1.0,0.85,0.4]}` | ❌ `Failed to parse either. First: Not a number; Second: Input is not a list of 4 elements` |
| `flash{color:16755200}` | ✅ 打包整数 |
| `flash{color:[1.0,0.85,0.4,1.0]}` | ✅ 四元浮点 |
| `tinted_leaves{…}` | 同上，三元 ❌，整数 ✅，四元 ✅ |

统一采用**打包整数 `0xRRGGBB`**——没有 ARGB/RGBA 顺序的歧义。

## 7.2 颜色直接从武器贴图里取

不是我挑的颜色，是从两张贴图的像素里数出来的（`png_tool.py` 统计不透明像素）：

| 武器 | 主色 | 占比 | 用作粒子色 |
| --- | --- | ---: | --- |
| 疾风迸发之弓 | `#E6A100` 主体金 / `#FFD637` 高光金 | 27% / 4% | **`#FFD637` = 16766519**（高光更像爆闪） |
| 藤蔓之鞭 | `#C3DB6C` 叶绿 | **46%** | **`#C3DB6C` = 12835692**（就是它自己的叶片色） |

## 7.3 藤蔓之鞭：改成连击

技能从「拽一下」扩成一套鞭法：

1. **拽近 + 钉住** —— 原有的 `facing entity … tp @s ^ ^ ^1.4` 与减速保留。
2. **连抽四鞭** —— 命中时给目标记 `rpg_vine_lash = 4`，之后**每刻抽一鞭**：
   2 点伤害 + `tinted_leaves` 叶片飞溅 + 暴击粒子 + 一声压低音调的抽击音效，计数减一。
3. **扫到旁边的人** —— 目标 2.5 格内最多 3 个同伴各记 2 鞭；鞭子本来就是打一片的。

一次命中因此变成 **1 次普通伤害 + 4 次追击（8 点）**，外加周围最多 3 个目标各 2 次。

两个细节：

* **击杀归属**：追击伤害用 `by @a[tag=rpg.h.vine_tag1,limit=1,sort=nearest]` 记在附近持鞭玩家名下，
  掉落和经验不会丢；14 格内没人持鞭时退回无归属伤害。
* **不会打自己人**：连击只挂在非玩家实体上（`type=!player`），也排除掉落物与经验球。

## 7.4 疾风迸发之弓：爆炸闪光

箭矢命中处现在先炸两层 `flash`（`~0.7` 与 `~1.4` 两个高度，做出纵向膨胀感），
再叠原有的 `gust_emitter_large` 与横扫粒子，然后才是三格 AoE 伤害与掀飞。

## 7.5 代价与验证

每刻命令 1145 → **1155**（+10），选择器开销 4562 → 4636。
仍不到优化前 18 536 的四分之一，带 `nbt=` 的选择器依旧只有 1 个。

新增计分板 `rpg_vine_lash`（dummy），已写进 `rpg:command/soreboard`。

专用服务器实测：数据包加载零报错，`vine` / `rift` / `skills` / `give/extra` 全部执行通过，
两种新粒子写法都被接受。

---

# 第八部分：双生剑与鞭击修正

## 8.1 藤蔓之鞭连击为什么"看不出生效"

真的有 bug，不是错觉。原写法是**连着四刻各抽一鞭**，
但生物受伤后有约 **10 刻无敌帧**——第一鞭之后的三鞭会被整个吃掉，
既不掉血也不闪红，所以完全看不出来。

改成**每 10 刻落一鞭**，正好错开无敌帧：计数器从 40 倒数，
只在 `30 / 20 / 10 / 1` 四个刻真正落鞭，两秒打完四鞭，四鞭全部生效。

顺便把反馈做足，现在不用猜：

* 每鞭一次叶片爆散 + 暴击粒子 + 横扫弧光
* 音调**逐鞭升高**（0.9 → 1.1 → 1.4 → 1.8），一耳朵能听出打到第几鞭
* 命中时给持鞭者一行 actionbar：**缠绕 鞭击命中**

（actionbar 那行若嫌吵，删掉 `rpg:item/extra/vine` 里带 `title … actionbar` 的一行即可。）

## 8.2 双生剑 · 雅斤与波阿斯

取名自所罗门圣殿门前的两根铜柱，与包里既有的亚巴顿／别西卜／贝利尔／萨麦尔同一套命名语域。
两把都是 **传说**，下界合金剑，模型编号 `1110012` / `1110013`。

| | 雅斤 Jachin（他必坚立） | 波阿斯 Boaz（力量在他） |
| --- | --- | --- |
| 技能类型 | **主动** | **被动** |
| 技能 | **立柱**：消耗 1 级经验，立起光柱，5 格内敌人被钉住（缓慢 251 + 挖掘疲劳）并受 6 点魔法伤害 | **承力**：每第 **3** 次命中打出一记强化打击，6 点额外伤害 + 虚弱 |
| 攻击 | +11（主手）/ +6（副手） | +9（主手）/ +5（副手） |
| 攻速 | −2.6 | −2.2 |
| 附魔 | 锋利 V·横扫 III·抢夺 II·耐久 III | 亡灵杀手 IV·击退 II·抢夺 II·耐久 III |

**联动［圣殿］**——任意一手雅斤、另一手波阿斯即成立（左右不限）：

* 立柱范围 **5 → 7 格**，并额外给自己 **伤害吸收 II·8 秒**
* 承力阈值 **3 → 2 次**
* 每次命中都会掠过一道紫金双色斩痕

取得：`/function rpg:command/give/extra`

技术上值得一提的两点：

1. **副手检测**是包里原本没有的。`rpg:command/index` 只索引了主手、盔甲与掉落物三种作用域，
   这次新增了 `rpg.o.*` 一段（`if items entity @s weapon.offhand …`），
   走的仍是那条不做 NBT 序列化的廉价路径。
2. **主动技能**沿用包里既有的机制：`food` + 独有 `consume_seconds`（100080，与现有 12 个都不冲突）
   → `minecraft:using_item` 进度 → 奖励函数，和风之回响／朗基努斯之枪是同一套。

## 8.3 贴图：已用你的原图

第二次贴图能拿到了——Claude Code 把会话附件缓存在
`~/.claude/uploads/<会话 id>/`，两张 PNG 就在那里。

两张都是 **128×128、干净的 8 倍最近邻放大**（逐块校验过，每个 8×8 方块同色），
所以取每第 8 个像素就能**无损还原成原始 16×16**——没有重采样，没有掉色。
`_tools/import_twin_art.py` 做这件事，并在 `_tools/twin_art/` 留一份副本，
将来上传缓存被清掉也能重建。

两把剑的配色因此和第一版的占位图不同（第二张其实是青粉，不是紫金）：

| | 主色 | 次色 |
| --- | --- | --- |
| 雅斤 | 紫刃 `#7A1695`（15%） | 金柄 `#F2D967`（14%） |
| 波阿斯 | 青刃 `#148291`（**23%**） | 品红刃口 `#DE8FF2`（13%） |

波阿斯的物品名颜色也随之从金色改成**青色**。

## 8.35 粒子随之重配

全部取自上表，不是我挑的：

| 效果 | 颜色 |
| --- | --- |
| 立柱（雅斤主动） | `dust_color_transition` **紫 → 金**；柱顶两层 `flash`，下层紫 `8001173`、上层金 `15915367` |
| 光柱扫到的目标 | 同一条紫 → 金渐变 |
| 承力强化打击（波阿斯被动） | `dust_color_transition` **青 → 品红**，外加一发品红 `flash` `14585842` |
| 圣殿联动 | **两道并行**：紫→金在 `~1`，青→粉在 `~1.2`，两把剑同时闪过 |

## 8.4 代价

每刻命令 1155 → **1194**，选择器开销 4636 → 4832。
仍不到优化前 18 536 的三分之一，带 `nbt=` 的选择器依旧只有 1 个。
新增计分板 `boaz`、`rpg_boaz_stack`；进度总数 1609 → 1610。

服务器实测：数据包零报错，`vine` / `twin` / `jachin_*` / `skills` / `give/extra` 全部加载执行通过。

---

# 第九部分：第二轮性能优化

加了这么多东西之后重新量了一遍。这次换了个更有意义的指标：
不是"每刻有多少条命令"，而是**每刻真正遍历几次实体表**——那才是卡顿的来源。
`_tools/hotspots.py` 会把 `#minecraft:tick` 链拆开逐函数统计，并分别给出
**空闲**（没人挨打、没 BOSS、天上没箭）与**满载**两个数字。

优化前：**每刻 558 次全实体表遍历**，其中
`legend1` 一个函数就占 271 次、`warden` 70 次、五个新技能约 93 次。

## 9.1 空标签的遍历：加一道闸

关键观察是：这些标签**绝大多数时刻是空的**——`rpg.hurt`（这刻没有东西受伤）、
`devil`（没召唤 BOSS）、`rpg.deep` / `rpg.rift`（天上没有对应的箭）。
于是每刻有五百多次遍历，是在整张实体表里找一个根本不存在的东西。

`_tools/opt_guard.py` 把**连续若干行、开头选择器完全相同**的段落挪进子函数，
外面只留一句：

```
execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g8
```

这么做**语义不变**：每行仍保留自己的 `as @e[...]`、顺序原样、上下文一致，
闸门只可能跳过那些"本来就一行都匹配不到"的段落。
共插入 **46 道闸，覆盖 380 行**。

（试过把阈值从 3 降到 2，闸门涨到 65 道但空闲开销一点没降——
多出来的闸自己也要走一遍表，正好抵消。已保留 3。）

## 9.2 标记索引：把循环里外翻过来

索引原本是每个标志一行：~110 行扫玩家表、~50 行扫掉落物表，
可这些判断**全都是逐实体的**，根本不需要按标志各扫一遍。

`_tools/opt_index.py` 把它翻成每个族群只遍历一次：

```
execute as @a                        run function rpg:command/index_player
execute as @e[type=minecraft:item]   run function rpg:command/index_item
```

子函数里全部落在 `@s` 上（`@s` 的选择器开销为零）。
**194 行折成 2 次遍历。**

## 9.3 效果

| 指标（每刻） | 本轮前 | 本轮后 |
| --- | ---: | ---: |
| **空闲时全实体表遍历** | **558** | **223** |
| 玩家表扫描 | 355 | 232 |
| 按类型索引的扫描 | 458 | 389 |
| 空闲时执行的命令 | 1104 | **776** |
| 带 `nbt=` 的选择器 | 1 | 1 |

对照最初的原包：选择器综合开销 **18 536 → 4 362**，
带 `nbt=` 的选择器 **634 → 1**，空闲遍历再砍掉六成。

## 9.4 验证

改索引结构是这轮风险最高的一步，所以做了两重验证：

1. **实机**：在专用服务器上 forceload 一块区块，丢下带 `gold_tag` 的金锭，
   跑 `rpg:command/index`，再读它的 `Tags`：

   ```
   Gold Ingot has the following entity data: ["probeB", "rpg.i.gold_tag1"]
   ```

   标记确实由折叠后的 `index_item` 打上了。

2. **静态**：把折叠后的索引拆回 `(族群, 槽位, 判定, 标记)` 四元组，
   共 **97 个标志**，"被清除的标记集合"与"被设置的标记集合"**完全一致，无遗漏无多余**。

数据包与材质包校验均 no problems found。

---

# 第十部分：五处返工

## 10.1 被动没生效 —— 计分板从没建过

`承力` 的判定是 `scores={boaz=0..}`，而 `boaz` 这个计分项是我这几轮才加的，
**只有手动跑一次 `/function rpg:command/soreboard` 才会创建**。
计分项不存在时，`scores=` 判定静默失败，技能自然一次都不触发。
（`vine` / `truth` / `rpg_vine_lash` / `rpg_boaz_stack` 同理。）

根治：新增 **`#minecraft:load`** 函数标签，指向 `rpg:command/soreboard`。
今后每次载入世界或 `/reload` 都会自动建好计分板，不必再记得手动跑。

实测（**没有**手动执行 soreboard）：`scoreboard objectives list` → **79 个计分项**，全部就位。

## 10.2 读档后卡一阵 —— 新实体被误判成"刚受伤"

`damage_scan` 靠 `damage_action`（本刻血量）与 `damage_timing`（上刻血量）比对判断受伤。
问题是**第一次见到某个实体时 `damage_timing` 根本没有值**，
`unless score 相等` 于是成立 —— 它被当成刚受伤，打上 `rpg.hurt`。

读档时区块是一批批加载的，于是每一批新实体都会触发一次**全部武器判定**，
表现就是"进档后卡一阵，然后自己好了"。

修法是第一次见到就先对齐基准：

```
execute as @e[…] unless score @s damage_timing = @s damage_timing run scoreboard players operation @s damage_timing = @s damage_action
```

（`unless score X = X` 在分数不存在时成立，是判断"这个分数有没有值"的惯用写法。）

实测：新召唤的僵尸 `damage_action=39 / damage_timing=39`，**不带 `rpg.hurt`**；
真打它 7 点后再扫，`damage_action=32 / damage_timing=39` —— 该触发的仍然触发。

## 10.3 光柱改打在敌人身上

原本光柱立在**自己脚下**，现在挪到**每一个被扫到的目标**身上，
而且按柱体分四层铺（`~0.2 / ~0.9 / ~1.8 / ~2.7`），横向收窄到 0.18，
看起来才是一根立起来的柱子而不是一团散雾。

粒子量同时大幅削减：施法者身上从 **200 粒降到 12 粒**，每个目标 26 粒。

## 10.4 双持不再反手

包里原有的 `sword_handheld` 给左手写的是 `rotation [-170,-90,-55]`，
那个 **-170 的 X 翻转**就是副手"反手拿"的来源。

新增 `rpg:item/twin_handheld` 作为双生剑的显示父模型，按原版 `item/handheld` 的做法，
左手只把 Y、Z 取反（`[0,90,-55]`），位移与右手一致 —— 两只手都是正手。

只作用于雅斤与波阿斯；其它武器仍用原来的 `sword_handheld`，没有动。
要全局改的话把同样的 display 覆盖进 `sword_handheld` 即可。

## 10.5 藤蔓之鞭改成右键连击

不再是"命中后自动抽"，改成**主动技能**：

* 右键长按发动，消耗 1 级经验
* 把 **6 格内**的敌人全部拽近一步并钉住
* 挂上 **3 秒 6 鞭**的持续连击（计数器 60 倒数，在 50/40/30/20/10/1 落鞭，
  仍是每 10 刻一鞭以错开无敌帧），音调逐鞭升高

当时的做法是给物品加 `food` + `consumable`，走进度 `minecraft:using_item` 触发 ——
**这条路在鱼竿上走不通**，原因见 11.1。

## 10.6 顺带

空闲遍历 223 → **221**（`vine` 的常驻判定改成右键触发后少了一段）。

---

# 第十一部分：第三轮返工

## 11.1 藤蔓之鞭：浮标就是鞭子

10.5 把连击改成 `food` + `consumable` 的右键主动技能，实测仍然不触发。

原因是**抛竿是鱼竿这个物品类写死的行为**，优先级在 `consumable` 组件之上。
右键鱼竿永远是甩钩，`minecraft:using_item` 那条进度根本没有机会响，
所以 `rpg:item/extra/vine_trigger` 从来没被调用过。剑、锤这些没有自带右键行为的
基底之所以能用这套机制，正是因为它们把右键让了出来。

与其和物品类抢右键，不如**把抛竿动作本身当成挥鞭**：

```
execute as @e[type=minecraft:fishing_bobber] on origin if entity @s[tag=rpg.h.vine_tag1,level=1..] at @s run function rpg:item/extra/vine_cast
execute as @e[type=minecraft:fishing_bobber] on origin if entity @s[tag=rpg.h.vine_tag1,level=..0] run playsound minecraft:entity.villager.no player @s
execute as @e[type=minecraft:fishing_bobber] on origin if entity @s[tag=rpg.h.vine_tag1] run tag @s add rpg.vine.reel
execute as @e[type=minecraft:fishing_bobber] at @s if entity @a[tag=rpg.vine.reel,distance=..48] run kill @s
tag @a[tag=rpg.vine.reel] remove rpg.vine.reel
```

`on origin` 把执行者从浮标换回它的主人。浮标一出现就换成一次鞭击，
同一刻把浮标收掉，鱼竿顺势弹回 —— 看起来正是甩鞭又收鞭，而且钩不到鱼。
命中判定与收鞭在同一刻完成，所以不会重复触发。

物品上的 `food` / `consumable` 和进度 `rpg:item/vine` 一并删掉（进度 1611 → **1610**）。

## 11.2 雅斤：立柱 → 称量

光柱和贝利尔的［朝拜］在观感与机制上都太近。换成一个这套世界观里更有分量的判决 ——

> 「你被称在天平里，显出你的亏欠」（但以理书 5:27）

**［称量］**：右键消耗 1 级经验，对范围内每个敌人升起一座紫金天平，然后按**剩余生命**分流：

| | 圣殿（双持）之外 | 与波阿斯双持 |
|---|---|---|
| 范围 | 6 格 | 9 格 |
| 生命厚（阈值以上）| 削 8 点 | 削 12 点 |
| 生命残（阈值以下）| **重创 14 点** | **重创 20 点** |
| 阈值 | 20（10 颗心）| 30（15 颗心）|
| 附带 | 全体发光 5 秒 | 再加自身吸收 II 8 秒 |

判决读的是 `damage_action` —— 那是 `rpg:command/index` 每刻已经抓好的血量，
所以这个"按血量分流"没有增加任何一次 `data get entity`。
残血的那一下额外给一记紫色爆闪与判决音，一眼能看出谁被判了。

## 11.3 握持变形：非等比缩放

第三人称下武器被拉长压扁，是包里**七个手持 display 父模型全都用了非等比缩放**：

| 父模型 | 原 scale | X/Y 比 |
|---|---|---|
| `sword_handheld` / `double_handheld` / `stick_handheld` / `twin_handheld` | `[1.46, 0.85, 0.85]` | 1.72× |
| `huge_sword_handheld` | `[2.5, 1.5, 1]` | 1.67× |
| `weapon_sword_handheld` | 右 `[1.46,1.46,0.85]` / 左 `[1.46,0.85,0.85]` | 两手不一致 |
| `long_handheld` | 右 `[2.23,2.33,2.31]` / 左 `[0.85,0.85,0.85]` | 两手差 2.7× |

`item/generated` 里刀身是**斜着画在一张 16×16 方形贴图上**的，
把 X 拉长 1.46 并不会"把刀身变长"，只会把整张画面斜着抻开 —— 那就是看到的变形。

`fix_display.py` 把每个父模型改成**单一等比缩放**，取原来两个平面轴的几何平均，
所以体积感基本保留、斜切消失；Y 方向的位移决定手握在刀柄哪一段，按同一系数一起缩放。
另外三个父模型的左手带着 `-170` 的 X 翻转（副手反手拿的老毛病），一并改成真正的镜像
（只取反 Y、Z）。这一步排在 `rp_build.sh` 最后，让包里所有手持变换只有一个出处。

## 11.4 图鉴图标改成真实合成

护甲、药水的图标此前直接取 `layer0`，只对"一层画完"的物品成立，别的全画错了：
皮甲显示的是**未染色的灰白生皮**，所有纹饰**整个消失**，药水是**空瓶**。

`icons.py` 改成走客户端的真实路径：

* item definition → `select`（按 `trim_material`）/ `range_dispatch`（按 `custom_model_data`）→ model
* model 的 `layer0..layerN` 逐层取出，第 *i* 层若有 `tints[i]` 就按物品自己的
  `dyed_color` / `potion_contents.custom_color` 相乘染色（没有就用 `default`）
* 自下而上 alpha 合成

纹饰贴图**根本不是文件**：`assets/minecraft/atlases/armor_trims.json` 用
`paletted_permutations` 在加载时生成 —— 灰度的 `trims/items/<部位>_trim.png`
每个像素在 8 色关键调色板 `trim_palette.png` 里查下标，换成
`color_palettes/<材质>.png` 同下标的颜色。这一步在 `icons.py` 里复现了，
所以 `helmet_trim_netherite` 这种并不存在的文件也能解析出来。

两个坑：

* **图集是少数会跨包合并而不是覆盖的资源**。材质包自带一份 `armor_trims.json`
  注册了自定义材质 `holy`；只读包里的会丢掉全部 12 种原版材质，只读 jar 里的会丢掉
  `holy`。两边都读、合并，共 17 种。
* 钻石头盔配钻石纹饰时，model 名直接指向 `helmet_trim_diamond_darker`
  （`override_armor_assets`），照着 model 走就自动对了。

顺带把 `png_tool.py` 补上了 1/2/4 位深与内存编解码（`decode()` / `encode()`），
玩家头颅按游戏的做法用默认皮肤的脸 + 帽子层合成。

结果：**108 件物品全部渲染成功，0 缺失**；23 件带染色/纹饰/药水色的图标与游戏内一致。
页面上仍然空白的 12 个图标是战利品表之间的**跳转指针**（`→ rpg:trial/...`），本来就不是物品。

附魔的物品另外加了一层 CSS 光泽 —— 用图标自身的轮廓做 mask，扫过一道紫色高光，
和游戏里附魔物品的观感对齐（`prefers-reduced-motion` 下静止）。

## 11.4b 灰度 + tRNS：被当成实心方块的贴图

11.4 上线后护甲图标变成了**纯色方块**，附魔光泽也跟着糊满整块图标。
两者其实是同一个 bug。

原版有一批物品贴图存成**灰度 PNG + `tRNS` 色键**。`tRNS` 在调色板图里是逐下标的
alpha 表（这一支本来就写对了），但在灰度/真彩图里含义完全不同 ——
它只存**一个「这个颜色算全透明」的键值**。解码器对灰度图一律填 alpha=255，
于是整张 16×16 全不透明：

| 贴图 | 编码 | 修前 | 修后 |
|---|---|---|---|
| `trims/items/helmet_trim` | grey + tRNS | 100% | **3%** |
| `trims/items/chestplate_trim` | grey + tRNS | 100% | **10%** |
| `item/leather_helmet` | grey + tRNS | 100% | **19%** |
| `item/iron_leggings` | grey + tRNS | 100% | **40%** |
| `trims/items/boots_trim` | grey + **A** | 7% | 7%（本来就对）|

全不透明的纹饰层因此把底下的甲整个盖住 —— 看到的就是一块纯色方块。
而附魔光泽用的正是**图标自身的 alpha 当 mask**，mask 是实心方块，光泽自然糊满整块。

`png_tool.decode()` 现在按色彩类型分别处理 `tRNS`：调色板图查表，
灰度/真彩图比对色键。全部 108 件物品里只剩玩家头颅是满格不透明 —— 一张脸本来就是实心的。

顺带把光泽收窄了：峰值透明度 .92 → .60，光带从 36% 宽收到 18%，周期 3.6s → 4.4s。

## 11.5 新锻装备并入图鉴

七件新装备原先单独占一节。它们的标签、稀有度、技能格式和其余装备完全一样，
现在**直接并进武器篇**（卡名后带「新锻」标记，共 25 件武器）；
第八节改成一张**出处对照表**，只说每件是从哪张贴图来的，不再重复整张卡片。

## 11.6 顺带：给新技能加闸

六个新技能此前每刻无条件跑。现在每条都先过守卫：

```
execute if entity @a[tag=rpg.h.deep_seek_tag1] run function rpg:item/extra/deep_seek
execute unless entity @a[tag=rpg.h.deep_seek_tag1] if entity @e[tag=rpg.deep] run function rpg:item/extra/deep_seek
```

没人拿着、场上也没有它留下的痕迹时整个函数跳过，空闲一刻只剩几次标签检查。
第二个条件是给"效果活得比挥击久"的技能留的 —— 箭矢要在射手换手后仍然飞完，
藤蔓之鞭的连击一旦起手也要抽满六鞭（为此给目标加了 `rpg.vine.lash` 标记，计数归零时摘掉）。

## 11.7 验证

* 真实 1.21.11 无头服务器：数据包加载无报错，探针逐个执行 `skills` / `vine_trigger` /
  `vine` / `jachin_weigh` / `jachin_cast` / `give/extra` / `tick`，全部干净
* 计分板审计：创建 78 个，被引用 71 个，**引用了却没创建的：0**
* 材质包对 1.21.11 客户端 jar 校验：`no problems found`（233 个文件）
* 三处安装副本与构建产物逐字节一致

---

# 第十二部分：第五位恶魔 · 路西法

## 12.1 规格对齐

对照前四把恶魔武器（亚巴顿 / 别西卜 / 萨麦尔 / 贝利尔）逐项对齐：

* `[DEVIL]` 前缀，`#999999` 粗体
* 两行称号，前半白、后半 `#999999` 粗体
* 一个技能块：`🗡主动技能[原罪]` + 说明行
* **五**条附魔（与其余四把一致）
* `unbreakable={}`，并用 `tooltip_display` 把「不可破坏」那行藏掉
* `custom_data` 带 `devil_tag`

## 12.2 初版：为什么不是 trident（已被 13.1 取代）

要求是长枪。Minecraft 没有 spear 物品，而 `trident` **自带右键投掷** ——
这正是 11.1 里鱼竿栽的那个跟头：物品类写死的右键行为压过 `consumable`，
主动技能永远不会触发。所以基底仍用 `netherite_sword`（全包唯一确定让出右键的近战基底），
"长枪"由两件事撑起来：

1. 挂在 **`rpg:item/long_handheld`** 下 —— 这是包里自带的长柄变换（等比 2.3），
   在此之前**一个使用者都没有**，正好给它。
2. **攻击距离 +3 格**，全包最远，这才是长枪真正的手感。

## 12.3 属性

| 属性 | 值 | 说明 |
|---|---|---|
| 攻击距离 | **+3** | 长枪的立身之本，全包最远（亚巴顿 +1）|
| 方块交互距离 | +1 | 跟着枪长一起给 |
| 攻击伤害 | +12 | 在别西卜 10 与贝利尔 13 之间 |
| 攻击速度 | −2.9 | 长柄的代价 |
| 移动速度 | ×1.06 | 蛇的轻捷 |
| 最大生命 | ×0.85 | 堕落的代价（贝利尔也有类似扣减）|

附魔：`sharpness 4 / bane_of_arthropods 5 / looting 3 / knockback 1 / sweeping_edge 2`
—— `bane_of_arthropods` 拉满是取"毒蛇"的味道。

## 12.4 ［原罪］

右键消耗 **2 级经验**，沿视线刺出一条 **12 格**的蛇矛。

线本身不需要递归：`positioned ^ ^ ^N` 是沿施法者视线方向取点，
所以 12 段直接展开成 12 组 4 行，生成期一次写好，只在施法时跑。

* 贯穿者立刻吃 **9 点魔法伤害**，并被种下**原罪**（10 秒）
* 带罪者每次挨打**额外还 4 点**；15 刻的间隔既避开无敌帧，
  也**断了"自伤触发自伤"的循环** —— 追加伤害会让目标下一刻又被判定为
  `rpg.hurt`，没有这道冷却就是个无限套娃
* 原罪在 150 / 100 / 50 三个刻各向 4 格内**最近一个尚且干净的敌人蔓延一次**

## 12.5 配色取自贴图

粒子颜色直接从蛇矛贴图上取，不另配一套：

| 名称 | 色值 | 用处 |
|---|---|---|
| 蝰绿 `VIPER` | `#35A15C` | 矛线主色、余罪的绿雾 |
| 嫩叶 `PALE` | `#8FDC7A` | 矛线高光、起手 |
| 毒黄 `VENOM` | `#E4E88C` | 蛇眼色 —— 中罪与加重时的爆闪 |
| 影绿 `DEEP` | `#12522F` | 蔓延、暗部过渡 |

配合 `sculk_soul` 铺矛线、`flash` 打中罪的一瞬、
`entity.warden_ambient` 高音做加重的提示音。

## 12.6 编号与验证

`custom_model_data = 1110014`（netherite_sword 上第一个空位），
`consume_seconds = 100100`（100010–100050、100080 已占）。

* 无头 1.21.11 服务器：`give/extra` 解析通过（`/give` 会在解析期校验全部组件），
  `lucifer_lance` / `lucifer` / `skills` 执行干净，无任何报错
* 进度 1610 → **1611**，计分板 78 → **80**
* 每刻代价：和其余新技能一样过守卫 —— 没人拿枪、场上也没有带罪者时整段跳过

## 12.7 顺带：神圣品质的颜色

包里 `[HOLY]` 前缀五处全是 `#ff3300`，图鉴却用了金色 `#F0D257`。
现已对齐：深色主题取游戏原值 `#FF3300`，浅色主题用压暗的 `#CC2900` 保证可读。

（另：`[DEVIL]` 在包里有三种写法 —— `#999999` ×5、`#660099` ×1、`#b00057` ×1。
图鉴目前仍用一个偏红的 `#DC6A62` 做恶魔色，因为纯灰 `#999999` 当卡片强调色
会比传说、史诗还黯淡。要改成灰的话是一行的事。）

---

# 第十三部分：路西法定稿

## 13.1 改用真正的 netherite_spear

1.21.11 **本来就有长枪**：`wooden_spear` 到 `netherite_spear` 七种，
外加一条 `#minecraft:spears` 物品标签和一个 `minecraft:spear_mobs` 触发器。
12.2 里"没有 spear 物品所以拿剑凑"的前提是错的。

更关键的是语言文件把长枪的右键行为写清楚了：

| 键 | 值 |
|---|---|
| `subtitles.item.spear.use` | **Charges with Spear** |
| `subtitles.item.spear.lunge` | Spear lunges |
| `advancements.adventure.spear_many_mobs.description` | Hit five mobs in the same **Charge attack** |

也就是说长枪**自带一个真正的使用动作**（蓄力 → 突刺）。
既然如此，`minecraft:using_item` 会直接在它身上触发 ——
**整套 `food` + `consumable` 的障眼法可以完全去掉**，
长枪保留自己的蓄力与突刺动画，而不是被替换成吃东西。

```json
{"criteria":{"requirement":{
  "trigger":"minecraft:using_item",
  "conditions":{"item":{
    "items":"minecraft:netherite_spear",
    "predicates":{"minecraft:custom_data":"{lucifer_tag:1b}"}}}}},
 "rewards":{"function":"rpg:item/extra/lucifer_trigger"}}
```

`custom_data` 谓词保证普通下界合金长枪不会误触发。

**一个必须处理的差别**：`consumable` 那条路靠一个大得离谱的 `consume_seconds`
让进度只在起手响一次；而 `using_item` 在**蓄力期间每刻都会响**。
所以 `lucifer_trigger` 前面压了一道 30 刻的冷却（`rpg_luci_use`），
否则按住右键会把经验一路抽干。

模型也照抄原版长枪的结构 —— `select` 判 `display_context`：
`gui / ground / fixed / on_shelf` 用平面图标，其余（也就是拿在手里）用专门的
in-hand 贴图。整体再包进 `custom_model_data` 分发，原版长枪不受影响。

## 13.2 附魔：长枪不吃 sweeping_edge

查了 `#minecraft:enchantable/*`：长枪在 `melee_weapon`、`durability`、
**`lunge`** 里，但**不在 `sweeping`** 里 —— 初稿写的 `sweeping_edge:2` 是无效的。
换成长枪专属的 **`lunge`**（`post_piercing_attack`：突刺命中后给一记前冲），
五条附魔全部合法：

`sharpness 4 / bane_of_arthropods 5 / looting 3 / knockback 1 / lunge 2`

## 13.3 贴图还原：不是整数倍放大

上传的图是 **1254×1254**，而且**不是最近邻放大** —— 被重采样过，
边缘带渐变，`import_twin_art.py` 那套"每隔 k 个像素取一个"会取到混色。
1254 也不整除任何常见网格。

改用**多数表决**还原：先统计出图自身的调色板（13 色），
再把画布切成 N×N 格，每格取**内部 76% 区域**的像素、吸附到调色板后投票，
票数最高的就是这一格的原色。内部像素远多于模糊边缘，所以原网格能精确复原。

N 的判定：边缘周期检测被透明边距干扰、方差法单调下降都不可靠，
最后是把 16 / 32 / 40 / 48 各还原一遍**直接看** ——
16 丢掉眼睛和獠牙，32 完整保留蛇头、瞳孔、獠牙与尾钩，40 / 48 开始出噪点。
**32×32** 就是原生网格。

in-hand 贴图不用另画：原版 `netherite_spear.png` 与
`netherite_spear_in_hand.png` 画在**互为镜像的对角线**上，
所以把 GUI 图水平翻转即可 —— 对像素画是无损的。

粒子配色随之从"目测"换成"实测"（按像素占比）：

| 色 | 占比 | 用处 |
|---|---|---|
| `#22724E` | 23.0% | 影绿，蔓延与暗部 |
| `#4AB276` | 21.1% | 蝰绿，矛线主色 |
| `#96CA76` | 8.1% | 嫩叶高光 |
| `#DAE282` | 4.3% | 蛇眼黄 —— 中罪与加重的爆闪 |

## 13.4 握持位置：把平移解出来，而不是猜

11.3 把缩放改成等比时，**顺手把平移按同一比例缩了** —— 那是错的，武器因此浮出手外。

Minecraft 的 display 变换是 `T · R · S`，渲染器再把模型居中，
所以模型空间里离精灵中心 `v` 的点最终落在 `p = T + R·S·v`。
对角线精灵的**握把端**是左下角 `v = (-.5,-.5,0)`；
旋转 `[0,-90,z]` 的矩阵行是 `(0,0,-1)`、`(sin z, cos z, 0)`、`(cos z, -sin z, 0)`，
于是

```
grip_y = T_y − (sx·sin z + sy·cos z) / 2
grip_z = T_z − (sx·cos z − sy·sin z) / 2
```

**平移和缩放不是正比关系**，中间隔着一个旋转。
所以现在的做法是：从作者的原始数值反解出握把位置，
再用新的等比缩放把同一个握把位置解回去。

两处自检：
* 拿原版 `item/handheld`（缩放 .85、平移 `[0,4,.5]`）走一遍，**原样返回**（代码里是个 assert）
* `weapon_sword_handheld` 原本平面内就是等比的 `[1.46,1.46]`，
  结果**一个数字都没变** —— 说明公式没有凭空移动本来就正确的变换

**等比缩放取多少**也换了依据。对画在 45° 对角线上的图，
缩放 `(sx, sy)` 会把对角单位向量拉到 `sqrt((sx²+sy²)/2)`，
而且**两条对角线拉伸系数相同** —— 这正是为什么那个畸变看起来是"斜切"而不是"拉长"。
取这个值，刀身长度与作者原本的**完全一致**。

| 父模型 | 原 scale | 等比 | 平移 Y |
|---|---|---|---|
| `sword_handheld` / `twin_handheld` | `[1.46,0.85]` | **1.195** | 6.75 → 6.60 |
| `double_handheld` / `stick_handheld` | `[1.46,0.85]` | **1.195** | 7.00 → 6.85 |
| `huge_sword_handheld` | `[2.5,1.5]` | **2.062** | 6.75 → 6.46 |
| `long_handheld` | `[2.23,2.33]` | **2.281** | 7.00 → 7.11 |
| `weapon_sword_handheld` | `[1.46,1.46]` | 1.460 | 7.50 → 7.50 |

Z 方向保留作者原值：斜切本来就发生在平面内，Z 只是精灵平面在手里的进深，
连带解出来会把巨剑往身体里推 3.7 单位，得不偿失。
最终每个父模型都落在作者原始数值的 0.3 单位以内 —— 只去掉斜切，不动手感。

## 13.5 贝利尔补上 devil_tag

五把恶魔武器里只有贝利尔的 `custom_data` 是 `{blil_tag:1b,sword_tag:1b}`，
**漏了 `devil_tag`**，所有按恶魔标记（`rpg.h.devil_tag1`）判定的逻辑都会跳过它。
已在 `opt_misc.py` 里补上，重建自动生效。

## 13.6 图鉴：display_context 要取 gui 分支

长枪的物品定义按 `display_context` 分叉，图鉴如果照旧走 `fallback`
会拿到**手持**贴图。`icons.py` 现在优先取 `when` 含 `gui` 的分支 ——
图鉴显示的就是背包里那张。

## 13.7 验证

* 无头 1.21.11：进度 **1611**（`using_item` + 物品谓词加载无报错），
  计分板 **81**，`give/extra` 解析通过（长枪 + `lunge:2` + 全部组件合法），
  `lucifer_trigger` / `lucifer_lance` / `lucifer` / `skills` 执行干净，零报错
* 材质包对客户端 jar 校验：`no problems found`（238 个文件）
* 三处安装副本与构建产物逐字节一致

---

# 第十四部分：尖牙、朗基努斯改型、召唤卡顿

## 14.1 路西法：幻魔者尖牙沿枪线破土

蛇矛之外再加一层 —— `minecraft:evoker_fangs` 沿同一条路径一节节炸开：

```
execute at @s rotated ~ 0 run function rpg:item/extra/lucifer_fangs
```

`rotated ~ 0` 把**俯仰归零**，所以无论抬头低头，尖牙都贴着地面前推，
而不是跟着视线飞到半空。12 段的 `Warmup` 逐段 +2，于是它们像唤魔者那样依次弹起。

一个必须处理的坑：**不设 `Owner` 的尖牙会连施法者一起咬**。
所以 12 段召完之后统一认主：

```
execute as @e[tag=rpg.luci.fang] run data modify entity @s Owner set from entity @a[tag=rpg.luci.cast,limit=1,sort=nearest] UUID
```

## 14.2 路西法配色

包里**每位恶魔各有自己的强调色**（萨麦尔 `#b00057`、贝利尔 `#660099`），
并不是统一的灰。路西法此前沿用了 `#999999`，现在换成蛇身的深绿 **`#00491c`** ——
`[DEVIL]` 前缀、称号的加粗后半、技能名都走这个色。

名字则相反：从 `green` 改成与其余恶魔一致的 **`aqua`**。

## 14.3 朗基努斯之枪：重锤 → 下界合金枪

叫枪就该是枪。改到 `minecraft:netherite_spear` 之后有三处连带必须一起改，
否则会静默失效：

**附魔**：五条原样保留。`supported_items` **只管附魔台和铁砧** ——
直接写进 `enchantments` 组件的附魔照常挂上，服务器解析零报错（已实测）。
真正决定它有没有用的是各自声明的**效果**：

| 附魔 | slots | 效果 | 在长枪上 |
|---|---|---|---|
| `breach 4` | `mainhand` | `armor_effectiveness` −15%/级 | **有效**，通用效果，不看物品类型 |
| `thorns 2` | `any` | `post_attack`（`enchanted: victim`）| **有效**，被打时反伤，握在手里也算装备槽 |
| `fire_aspect 3` | — | — | 有效 |
| `knockback 2` | — | — | 有效 |
| `density 4` | `mainhand` | `smash_damage_per_fallen_block` | 只喂重锤砸击，**长枪上不产生效果** |

`density` 保留是按作者要求；它会出现在提示框里但不做事。
想让这一格干活，可以换成长枪专属的 `lunge`（突刺命中后的前冲）。

**触发方式**。原本走 `food` + `consumable`，而长枪自带蓄力动作会把它顶掉 ——
和鱼竿那次一模一样。改成 `minecraft:using_item` + `custom_data~{power_tag:1b}`。

这里有个和路西法相反的细节：`using_item` 在蓄力期间**每刻都响**，
而［王座］的 `trigger.mcfunction` 本来就是靠这个把 `power_step` 一格格加上去的
—— 它本来就是"长按蓄力"型技能。所以长枪的蓄力和它是一一对应的，
**不能**像路西法那样加冷却。

**模型**。从 `huge_sword_handheld` 改成原版长枪的结构（`display_context` 分叉
+ 镜像的 in-hand 贴图），编号 1110003 从 `mace.json` 挪到 `netherite_spear.json`。

## 14.4 召唤生物时的卡顿

`rpg:command/tick` 里的生物检测原本是这样：

```
execute as @e[type=#minecraft:zombies,tag=!zombie] at @s run function rpg:command/spawn/zombie
execute as @e[type=#minecraft:zombies,tag=!zombie] run function rpg:command/spawn/zombie_gear
tag @e[type=#minecraft:zombies] add zombie
```

标记是有的，逻辑没错，但**完全没有封顶**。`zombie_gear` 里是四条
`loot replace entity`，每一条都会**真的掷一次战利品表**（随机附魔、随机属性）。
于是一次 `/summon` 一群、刷怪笼爆发、或者读档时区块成批载入 ——
几十只生物的上百次掷点全部挤在**同一刻**。那就是召唤生物时的那一顿。

现在每个族群改成守卫 + 封顶：

```
execute if entity @e[type=#minecraft:zombies,tag=!zombie,limit=1] run function rpg:command/spawn/zombie_batch
```

`zombie_batch` 里每刻只取 4 只：

```
tag @e[type=#minecraft:zombies,tag=!zombie,limit=4] add rpg.spawn.new
execute as @e[tag=rpg.spawn.new] at @s run function rpg:command/spawn/zombie
execute as @e[tag=rpg.spawn.new] run function rpg:command/spawn/zombie_gear
tag @e[tag=rpg.spawn.new] add zombie
tag @e[tag=rpg.spawn.new] remove rpg.spawn.new
```

先打标记再按标记干活，避免三条 `limit=4` 各自选到不同的四只。
余下的顺延到下一刻 —— 装备晚落地几百分之一秒，肉眼无差，
但尖峰被摊平了。空闲刻只剩三次 `if entity ... limit=1` 守卫。

## 14.5 还没做：使用武器时的卡顿

这一半**没有解决**，因为它需要的是一次有回归风险的重构，先说清楚现状：

`rpg:item/sword/legend/legend1` 已经有守卫（`if entity @e[tag=rpg.hurt]`），
所以平时不跑。问题在于**一旦打中**，它和它的十几个 `g*` 子函数
**各自重新遍历一遍 `@e[tag=rpg.hurt]`**：

| 函数 | 命令 | 全场遍历 |
|---|---|---|
| `legend1` | 147 | 63 |
| `legend1/g8` | 31 | 36 |
| `legend1/g7` | 24 | 30 |
| `legend1/g16` | 20 | 27 |
| `legend1/g12` | 18 | 24 |

空闲 798 命令 / 236 次遍历，命中那一刻升到 1207 命令 / **612 次遍历**。

解法和第九部分对索引做的**循环内外翻**是同一招：
把 `execute as @e[tag=rpg.hurt] run <每条效果>` 改成
`execute as @e[tag=rpg.hurt] run function <整段>`，段内一律对 `@s` 操作，
612 次遍历能压到个位数。

没有直接动手，是因为这要改动 300 多条实际战斗逻辑，
和索引那次不同（索引是纯粹的标记设置，语义上可证等价），
这里涉及顺序、条件与副作用，需要单独一轮改 + 验证。要做的话跟我说。

## 14.6 验证

* 无头 1.21.11：`give/weapon`（含改型后的朗基努斯长枪 + `lunge:3`）与
  `give/extra` 解析通过，`spawn/*_batch` 三个全部执行干净，零报错
* 尖牙实测：`lucifer_fangs` 一次生成 12 段（探针里连同对照共清掉 13 个实体）
* 材质包对客户端 jar 校验：`no problems found`（240 个文件）
* 三处安装副本与构建产物逐字节一致

---

# 重建方式

```bash
bash "_tools/build.sh"
```

```bash
bash "_tools/rp_build.sh"
```

数据包流程：`migrate.py` → `optimize.py` + `opt_spawn.py` + `opt_misc.py`
　　　　　→ `add_items.py` + `add_skills.py` + `add_twins.py` + `add_lucifer.py`
　　　　　→ `retype_longinus.py` → `opt_index.py` + `opt_guard.py` → `validate.py` → `hotspots.py`
材质包流程：`rp_migrate.py` → `import_twin_art.py` → `fix_art.py`
　　　　　→ `add_items.py` + `add_skills.py` + `add_twins.py` + `add_lucifer.py`
　　　　　→ `retype_longinus.py` → `fix_display.py`
　　　　　→ `rp_validate.py`
打包与安装：`package.py --install`（写回 1.21.11 实例的 resourcepacks 与各存档）
存档升级：`world_upgrade.py <存档路径> <临时目录>`
图鉴生成：`bash _tools/guide_build.sh`（含贴图内嵌）
贴图裁剪：`fix_art.py <材质包>`　新装备与技能：`add_items.py` / `add_skills.py`
闲置贴图反查：`unused_textures.py <材质包>`
无头实测：`server_test.py`（数据包）、`launch_test.py`（材质包）

实机测试（会开一个 854×480 的临时客户端窗口，几十秒后自动关闭）：

```bash
python "_tools/launch_test.py" file/rpg_resourcepack_claude 200 "<临时 gameDir>"
```

两条流程当前均为 **no problems found**，数据包迁移幂等（重复运行不再产生改动）。
