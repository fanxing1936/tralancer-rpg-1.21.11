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

## 14.6 一次取齐：潜影盒

`rpg:command/give/*` 一件件发，109 件装备能把背包塞爆好几轮。
`make_boxes.py` 把这四个函数直接打包成 `rpg:command/give/box` ——
一条命令给出 6 只潜影盒（武器红 ×2、道具蓝 ×2、升级材料黄 ×1、新锻装备绿 ×1），
每盒最多 27 件。

唯一的实质工作是语法搬家。give 命令写成 `id[custom_name=...,lore=[...]]`，
而潜影盒 `container` 条目里同样的数据是**按命名空间 id 索引的映射**：

```
{slot:0,item:{id:"minecraft:netherite_spear",count:1,
  components:{"minecraft:custom_name":...,"minecraft:lore":[...]}}}
```

`snbt.py` 本来就会解析方括号那种写法，所以每个值是**原样重新 dump 到全名键下**的
—— 值本身没有被重新序列化，盒里的物品和逐件 give 出来的完全一致。

（`weapon.mcfunction` 里有一条是 `give @s`（那个 vault 方块）而不是 `give @a`，
打包器两种都收，否则会漏掉一件。）

## 14.7 验证

* 无头 1.21.11：`give/weapon`（含改型后的朗基努斯长枪 + `lunge:3`）与
  `give/extra` 解析通过，`spawn/*_batch` 三个全部执行干净，零报错
* 尖牙实测：`lucifer_fangs` 一次生成 12 段（探针里连同对照共清掉 13 个实体）
* 材质包对客户端 jar 校验：`no problems found`（240 个文件）
* 三处安装副本与构建产物逐字节一致

---

# 第十五部分：命中那一刻的卡顿

## 15.1 循环内外翻 —— 但只翻能证明等价的

`legend1` 那一族的 `g*` 块里，**每一行都以同一个 `execute as @e[tag=rpg.hurt]` 开头**，
所以有东西挨打的那一刻，全实体表被"每行扫一遍"。

折成一次遍历（`execute as @e[tag=rpg.hurt] run function <body>`，
body 内一律对 `@s` 操作）就是第九部分对索引用过的同一招。
但这里**不能无条件照搬**：它把逐行遍历（对每行、对每个实体）换成了
逐实体遍历（对每个实体、对每行）。这两种顺序只在一种情况下不等价 ——
**后面的行写了前面的行会读的状态**。一次横扫打中两只怪时，
第二只会看到第一只把分数改过之后的值。

所以每个块先做一次**反向依赖检查**：

* 收集每行的**读**（`scores={...}`、`if score` 里的记分项，`tag=` 里的标签）
  与**写**（`scoreboard players set|add|remove|reset`、`tag @… add|remove`）
* 只有当**没有任何一行写了更早的行读过的东西**时才折叠

没有反向依赖 ⇒ 两种遍历顺序可交换 ⇒ 折叠是保行为的。

结果：

```
inverted blocks: 13  (117 lines -> 13 walks, 104 fewer)
left alone (would change behaviour):
  legend1/g2   15 lines  -- writes ashes that an earlier line reads
  legend1/g8   31 lines  -- writes sakura_step that an earlier line reads
```

`g8` 正是我手推时判断有风险的那个（樱怒的 `sakura_step` 状态机），
静态检查独立得出了同样的结论。这两块**原样保留** ——
宁可留着开销，也不把战斗逻辑悄悄改出 bug。

命中那一刻：**612 → 508 次全场遍历**，选择器开销 3520 → 3104。

## 15.2 一个被 validate.py 漏掉的错误

第一版折叠把整个 `execute as @e[tag=rpg.hurt] ` 前缀都剥掉了，
于是行首变成 `at @s on attacker ...` —— **少了 `execute` 这个词，根本不是命令**。

`validate.py` 报的是 `no problems found`，而无头服务器直接给出：

```
Failed to load function rpg:item/sword/legend/legend1/g5_body
Whilst parsing command on line 5: Unknown or incomplete command
```

这正是那套无头验证存在的理由 —— 静态校验只看组件与引用，
真正的命令语法只有游戏自己说了算。剥离改成保留 `execute`
（若剩下的只是 `run <cmd>` 则直接输出 `<cmd>`），重跑即干净。

## 15.3 顺带：限定传说

`[l·legend]` 半中半英，而且在两把武器上是**两种颜色**（`#ffcc33` 与 `#D84E4E`）。
统一成 **`[限定传说]`**，颜色 `#FFD700` 金黄 ——
比普通传说的原版 `gold`（#FFAA00）亮一档，两者仍分得开。
图鉴里也给了它独立的品质档 `--r-lgd`（浅色主题用压暗的 `#8A6B00`）。

---

# 第十六部分：第六位恶魔 · 利维坦

## 16.1 基底：重锤能用 consumable

查过语言文件，重锤只有 `subtitles.item.mace.smash_air` / `smash_ground`，
**没有 `.use`** —— 它不像鱼竿和长枪那样自带右键动作，
所以 `food` + `consumable` 那条路在它身上照常工作（亚巴顿也是重锤，走的同一条）。

编号 `custom_model_data = 1110007`（重锤上第一个空位），
`consume_seconds = 100110`。

## 16.2 贴图：又是重采样

上传是 128×128、13 色、31% 不透明，`block_factor` 仍然是 1 ——
不是整数倍放大。沿用第十三部分那套**多数表决**还原，
候选 16 / 32 / 64 各还原一遍直接看：16 糊成一团，64 只是 32 的加倍，
**32×32** 是原生网格（和蛇矛一样）。

## 16.3 配色：深蓝领衔，锚金呼应

作者定的代表色是**深蓝**，而贴图本身是**青铜绿 + 金**（一具沉在水里发绿的锚），
两者并不冲突 —— 前者是武器的强调色与粒子主调，后者是锚的金属。
最终取四色：

| 名称 | 色值 | 用处 |
|---|---|---|
| `ABYSS` | `#123E7C` | 深蓝，代表色 —— 强调色、漩涡主调、碾压爆闪 |
| `TRENCH` | `#081F42` | 更深，漩涡的喉咙 |
| `FOAM` | `#7FC8E0` | 浪沫，锚落水的一瞬 |
| `GOLD` | `#FCAE06` | 取自贴图（占 15%），锚的金属 |

## 16.4 ［沉锚］

右键消耗 **2 级经验**，向前方水平抛出巨锚。

`rotated ~ 0` 把俯仰归零 —— 无论抬头低头，锚都沿水平方向掷出 **8 格**，
不会因为仰视而飞上天。锚是往下沉的东西，这一条是主题要求的一部分。

锚落处 `summon minecraft:marker` 立一个锚点（marker 不跑 AI，几乎零开销），
张开半径 **7 格**的漩涡：

* **每刻**把范围内的敌人拖向锚心（`facing entity … feet` + `tp @s ^ ^ ^0.55`），并压上缓慢
* **每 10 刻**碾压一次，6 点 `minecraft:drown` 伤害 ——
  刻意对齐生物约 10 刻的无敌帧，打得更密只是浪费
* 计时归零时锚炸成一片浪花并自我清除

**凌空抛锚沉得更深**：起手时 `if block ~ ~-1 ~ air` 判定脚下悬空，
漩涡从 100 刻延到 160 刻。这是把重锤"从高处砸下"的本能翻译成锚的语言。

## 16.5 附魔与属性

五条全部能生效（`supported_items` 只管附魔台，见 14.3）：

`density 5` `breach 4` `wind_burst 3` —— 重锤自己的三条；
`smite 3` 在 `#enchantable/weapon`（含重锤）里；
**`impaling 5`** 名义上属于三叉戟，但它的效果是通用的 `minecraft:damage`，
条件只看目标是否 `#sensitive_to_impaling` —— 挂在重锤上照样对水生生物加伤，
是这套主题里最贴切的一条。

属性上给了它**锚的重量与巨兽的体魄**：伤害 +13、攻速 −3.3（全包最慢）、
移速 ×0.8、**最大生命 ×1.2**（六把恶魔武器里唯一给正向生命的）、
安全落地距离 ×2 —— 从高处砸下来不伤自己，正好配合凌空抛锚。

## 16.6 验证

* 无头 1.21.11：进度 1611 → **1612**，`give/extra` 解析通过
  （重锤 + `impaling` + `wind_burst` + 全部组件合法）
* 锚的全链路实测：`leviathan_drop` 生成 marker → 计分板读到
  `Marker has 85 [rpg_levi_time]`（设 100，已倒数）→ `pull` / `crush` /
  `leviathan` 逐个执行干净 → 计时归零自我清除
* 材质包对客户端 jar 校验：`no problems found`（242 个文件）

---

# 第十七部分：血税、握持、以及我自己造的卡顿

## 17.1 ［沉锚］的代价：血，不是经验

没有 CD 就得有别的东西拦住连点。代价改成 **每次献出 10 点生命 + 10 秒不幸**。

一个关键实现细节：**不能用 `damage`**。`damage` 要过生物约 10 刻的无敌帧 ——
连点右键时第二次之后的代价会被整个吞掉，等于白嫖。所以直接改写 `Health`：

```
scoreboard players remove @s rpg_levi_hp 10
execute store result entity @s Health float 1 run scoreboard players get @s rpg_levi_hp
```

这绕过护甲、抗性与无敌帧，每一次都实收 10 点。
（顺带查过：`minecraft:starve` 是**唯一**同时在 `bypasses_armor` 与
`bypasses_effects` 里的伤害类型，但它仍然过无敌帧，所以还是不够。）

起手前先量一次生命，不够就拒绝并播 `villager.no` ——
和包里其余主动技能付不起代价时的反应一致，而不是把人送走。

## 17.2 握持位置

`leviathan` 原本挂在 `huge_sword_handheld`（等比 2.06）下 ——
那是给细长对角线大剑调的。锚的贴图**填满整个 32×32**，
在那个尺度下直接淹掉整只手。改挂 `sword_handheld`（1.195），
包里用得最多、调得最准的那个变换，也正是单手重锤该有的尺寸。

## 17.3 我自己造的卡顿

加新技能时给每条守卫都配了个"第二条件"作为兜底：

```
execute unless entity @a[tag=rpg.h.deep_seek_tag1] if entity @e[tag=rpg.deep] run …
```

**`@e[tag=…]` 是不带索引的** —— 它要遍历全实体表。六条这样的兜底每刻各扫一遍，
花掉的比它们守卫的函数还多。空闲遍历从 221 涨到 248，是我自己加的。

修法分两种：

* **箭矢与锚**：标记只会落在特定类型上，所以把类型写在前面 ——
  `@e[type=minecraft:arrow,tag=rpg.deep]`、`@e[type=minecraft:marker,tag=rpg.levi.anchor]`。
  `type=` 是**带索引**的，于是全表遍历变成在该类型的名单里查一次。
* **藤蔓连击与原罪**：标记落在任意生物上，没有类型可以先筛。
  这两个效果只持续三秒和十秒，握持判定已经覆盖了绝大多数情况，
  兜底条件**直接删掉** —— 不值得每刻为它们全场扫一遍。

## 17.4 顺带挖出来的大头：com 的两段锻造逻辑

`rpg:command/com` **153 行、每刻无守卫**地跑，是全包最大的常驻开销。
按 `##` 分节分析后，有两段可以证明是可以整段挡住的：

| 段 | 命令数 | 每一行都需要 |
|---|---|---|
| `##洗练` | 42 | `rpg.i.diamond_tag1`（34/42 行直接点名，其余 4 行只是给它们喂计数，4 行是 `reset * random`）|
| `##武器分支` | 24 | `rpg.i.weapon_tag1`（**每一行**都要）|

也就是说：地上没有洗练石时，洗练那一整段不可能产生任何效果。
各用一次 `@e[type=minecraft:item,tag=…]` 的**带类型查找**挡住，
两段共 **66 条命令**移出常驻路径。

空闲命令数 **817 → 755**，守卫从 48 增到 50，被挡住的行数 470 → 536。

## 17.5 漩涡的粒子

每刻 36 粒 × 100 刻 ≈ 3600 粒，客户端明显吃不消。
削到每刻 13 粒，碾压那一下从 30+18 降到 14+10。

## 17.6 验证

* 无头 1.21.11：`com` / `com/xilian` / `com/branch` / `give/extra` /
  `leviathan_trigger` / `skills` / `tick` 全部执行干净，零报错
* 材质包对客户端 jar 校验：`no problems found`

## 17.7 还没动的

`rpg:command/damage_scan` 对 64 格内**每个实体**做一次
`data get entity @s Health`，开销随附近实体数量线性增长 ——
在刷怪笼或大群生物旁边，这才是剩下最贵的一项。
改法要么缩范围，要么改成只在实体数量少时全量扫，
两者都会改变行为，需要单独一轮，先记在这里。

---

# 第十八部分：蓄力，以及一个"能解析但不生效"的扣血

## 18.1 玩家 NBT 是只读的

17.1 里为了绕过无敌帧，扣血用的是直接改写生命值：

```
execute store result entity @s Health float 1 run scoreboard players get @s rpg_levi_hp
```

**这条对玩家不生效。** Minecraft 不允许通过 `/data` 或 `execute store … entity`
修改玩家 NBT —— 命令能解析、能执行、不报错，但什么也没发生。
所以那一版扣血形同虚设。

无头服务器没能抓到它，因为我当时是拿僵尸测的 —— **非玩家实体的 NBT 是可写的**，
在僵尸身上它工作得好好的。这是个只在玩家身上出现的失效。

改用 `damage`，伤害类型选 **`minecraft:starve`** ——
它是唯一同时位于 `#bypasses_armor` 与 `#bypasses_effects` 的类型，
护甲、保护附魔、抗性提升一概不减免，每次实收 10 点。

这次验证方式换了：给测试僵尸挂 `armor: 20` 再施放。
生命 **18.0 → 6.0** —— 如果护甲生效，10 点伤害对 20 护甲会被削到约 2 点。
没有被削，说明确实绕过了。

`starve` 仍然要过约 10 刻的无敌帧 —— 但这个顾虑随下面的蓄力一起消失了。

## 18.2 蓄力

`minecraft:using_item` 在按住右键期间**每刻都会响**，这正是蓄力需要的节拍
（包里的［王座］本来就是靠它把 `power_step` 一格格加上去的）。
每响一次攒一格，攒满 **30 刻（1.5 秒）**才真正抛锚。

满蓄那一刻用**精确判等** `scores={rpg_levi_charge=30}` 放锚，
而计数器随后继续 +1 越过 30 —— 所以按住不放只会抛一次，不会连抛。

**松手怎么判**：trigger 每刻把 `rpg_levi_hold` 顶回 3，每刻函数里扣 1。
一旦停手，3 刻内归零，蓄力随之清空 —— 也就没法靠连点攒。

蓄力期间有分层反馈：脚下持续冒水柱，10 刻后加深蓝尘，20 刻后转浪沫色，
锁链声每一档升高一次音调，满蓄时一记 `elder_guardian.curse`。

顺带一提：**蓄力恰好补上了无敌帧那个漏洞** ——
两次施放之间必然隔着 30 刻，远超 10 刻的无敌窗口，
`damage` 每一次都会真正落地。

---

# 第十九部分：破碎大陆，与两个记分板陷阱

## 19.1 蓄力根本没起来 —— 选择器里的 scores 要求分数已存在

蓄力计数写成了这样：

```
execute if entity @s[scores={rpg_levi_charge=..30}] run scoreboard players add @s rpg_levi_charge 1
```

**选择器里的 `scores=` 判定要求该记分项对这个实体已经有值。**
玩家第一次使用时 `rpg_levi_charge` 根本不存在 —— 条件恒假，
计数器永远起不来，技能也就永远放不出来。

无头服务器实测直接印证了它：第一次读分数返回
`Can't get value of rpg_levi_charge for Zombie; none is set`。

改成无条件 `scoreboard players add`（无值时按 0 起算，所以总能起步），
放锚仍用精确判等 `=30`，所以按住不放也只抛一次。

**同一个陷阱还埋在收尾里**：施放后用的是 `scoreboard players reset`，
那会把分数**删掉**而不是归零 —— 下一次使用又回到"没有值"的状态。
一并改成 `set … 0`。

修完的全链路实测：连打 30 次 trigger 之后
`rpg_levi_charge = 0`（说明攒满、放锚、归零都走到了）、
生命 20 → 6（血税落地）、`Marker has 58 [rpg_levi_time]`（漩涡在转）。

## 19.2 蓄力反馈

原来每刻只有 2~4 粒，等于没有。现在分四档：
脚下 12 粒深蓝尘 + 6 粒水柱常驻，10 刻后加一层浪沫色，
20 刻后加水花，25 刻后转锚金；锁链声逐档升调，满蓄一记
`elder_guardian.curse`。

另外在快捷栏上方加了**文字进度**：`沉锚 ▮▯▯ 起链` → `▮▮▯ 海涌` →
`▮▮▮ 将满` → `沉　锚`。粒子可能被地形挡住，文字不会。

## 19.3 破碎大陆

原本的「剧情章节」是十二条进度树条目。现在整节换成世界观本身
**《破碎大陆》Eretz Ha-Shevarim｜碎片之地**，按七卷结构排版：
创世 / 伊甸 / 权柄 / 堕天 / 魔神 / 百年战争 / 人的国度。

排版上新增了几件东西：希伯来文标题作为卷首、`.verse` 经文引用块
（带出处，左侧金线）、`.sins` 七宗罪对照网格 ——
七位领主与七宗罪的对应正好和包里六位恶魔武器互相印证
（路西法傲慢、利维坦嫉妒、贝利尔色欲、别西卜暴食、萨麦尔暴怒、
亚巴顿怠惰，只差玛门的贪婪）。

## 19.4 去掉"新增装备"这个概念

新锻装备本来就带着同样的标签、稀有度与技能格式，
分成两类只是历史包袱。现在：卡片上的「新锻」角标去掉，
第八节「新锻装备」整节删除，目录与罗马数字顺延（原 IX/X/XI → VIII/IX/X）。

## 19.5 随机掉落武器并入武器图鉴

战利品表里那批带**属性区间**的武器卡（血煞弯刀、严寒风暴、珊瑚突刺……）
原本单独挂在掉落图鉴下。现在移进武器篇，作为「随机掉落武器」小节，
和固定装备同页、同筛选器。掉落图鉴只保留权重与区间的总表，改名「掉落总表」。

---

# 第二十部分：署名、页首与固定深色

## 20.1 页首与署名

页首从「BRAND / 布兰德·宿命之途」换成
「Shevarim / אֶרֶץ הַשְּׁבָרִים / 破碎大陆 · 碎片之地」，导语取自世界观开篇的见证；
装备数量改为从 `_guide_sections.json` 现算（原本写死的「三十余件」早已过时）。

世界观原文入库为 `LORE.md`，README 与图鉴给出链接。
作者一栏改成三方对照：设定归作者，《破碎大陆》的叙事文案由 **ChatGPT**（OpenAI）落笔，
迁移／优化／图鉴生成由 **Claude**（Anthropic）完成。
署名同时出现在 README、`LORE.md` 卷首、图鉴的世界观节与页脚。

## 20.2 固定深色

图鉴原本是随viewer切换的三态配色（浅色 `:root` + `prefers-color-scheme` +
`[data-theme]`）。现在**这套深色就是设计本身**，不再是对读者设置的响应：

* 令牌全部落在裸 `:root` 上，**删掉浅色调色板、`prefers-color-scheme` 块与
  `[data-theme="dark"]` 块** —— 没有任何一条规则能把它翻成浅底
* 加 `color-scheme: dark`，让滚动条、搜索框光标这些浏览器自身的部件也跟着走
* `html` 与 `body` 都显式刷上 `--ground`，
  这样过度滚动的回弹、或视口高于内容时，背后不会露白

验证方式是把浏览器**强制切到浅色**再量计算样式：

```
browserPrefersLight : true
body background     : rgb(18, 16, 15)   ← #12100F
color-scheme        : dark
再补盖 data-theme="light" : rgb(18, 16, 15)  ← 仍然不变
```

三种状态（系统浅色、系统深色、viewer 显式选浅色）下都锁在深色。

---

# 第二十一部分：符文与符石（以及一个从未生效的子系统）

## 21.1 原本那三块符石根本不可能生效

包里有三块「镶嵌符石」（剑气 / 风暴 / 烈焰），**两个独立的原因**让它们
从来没有起过作用：

1. 它们的 `custom_data` 里**没有 `add_weapon_tag`**。
   而 `rpg:command/com/add`（把符文丢到武器上完成镶嵌的那条路）
   只认带这个标记的物品 —— 所以符石根本没法镶嵌上去。
2. 它们的进度触发条件是 `minecraft:using_item` 且
   `consume_seconds` 为 **1000000 / 2000000 / 3000000**，
   而全包物品里实际存在的值只有
   `100010 / 100020 / 100040 / 100050 / 100080 / 100110 / 240820 / 6000001`
   —— **没有一个对得上**，这条进度在原理上就不可能触发。

三处都补齐了：符石补上 `add_weapon_tag`，并挂上它们自己的进度所等待的那对
`food` + `consumable`；同时 `com/add` 学会在镶嵌时**把这两个组件也一起带过去**：

```
execute as @e[…tag=rpg.i.weapon_tag1] at @s if data entity <符石> Item.components.minecraft:consumable
  run data modify entity @s Item.components.minecraft:food set from entity <符石> …
```

不带这一步，镶嵌完的武器仍然不能右键，那条 `using_item` 进度依旧不会响。

**还有第三个问题**：三个 `*_trigger` 读蓄力分数时**完全没有握持判定** ——
一旦让它们真的能触发，攒满任何一块符石都会把三种效果一起放出来。
各补了一条 `tag=rpg.h.<flag>1`。

## 21.2 新增四枚被动符文

沿用既有形状（`quartz` 基底、`[名]镶嵌符文`、三行说明、
`<flag>_tag:1b,add_weapon_tag:1b`），技能都是新的：

| 符文 | 位置 | 效果 |
|---|---|---|
| ［枯萎］ | 🪓 剑 | 攻击时 1/4 概率使目标凋零 5 秒 |
| ［裂甲］ | 🪓 剑 | 攻击时破甲：虚弱 II + 发光 6 秒 |
| ［逆潮］ | 🛡 胸甲 | 生命跌破三成时回涌，再生 II 与抗性各 6 秒，30 秒一次 |
| ［钉影］ | 🏹 弓 | 箭矢命中后把目标钉住（缓慢 V + 挖掘疲劳）2.5 秒 |

［逆潮］的血量判定直接读 `damage_action` —— 那是 `rpg:command/index`
每刻已经抓好的血量，不额外做 `data get`。

## 21.3 新增三块主动符石

蓄力型，节拍与包里其余蓄力技能一致（进度每刻响一次、攒够才放）：

| 符石 | 蓄力 | 效果 |
|---|---|---|
| ［寒潮］ | 45 刻 | 环形寒潮：6 格内冻结、减速 V、外推一步 |
| ［震地］ | 55 刻 | 砸地：环形 8 点伤害、致盲、击飞 |
| ［噬影］ | 40 刻 | 遁入影中，出现在最近敌人**背后**并重创 12 点 |

［噬影］的绕背是 `facing entity … feet` 之后再 `positioned ^ ^ ^1.2` ——
朝向目标再往前一步，落点正好在它身后。

## 21.4 验证

* 无头 1.21.11：进度 1612 → **1615**（三块新符石的触发器），
  `give/item` 解析通过（7 件新物品含符石的 food/consumable 全部合法），
  `runes` / 三个 `*_burst` / `ebb_surge` / `com/add` 执行干净，零报错
* 图鉴刻印数 12 → **19**，小节标题与数量改为现算

---

# 第二十二部分：三件作者贴图武器，与刻印的独立纹理

## 22.1 三件新武器

贴图仍是重采样的 128×128，沿用多数表决还原到原生 **32×32**，
粒子配色逐件从各自的贴图上量：

| 武器 | 基底 | 品质 | 技能 | 主色 |
|---|---|---|---|---|
| **熔火之锤** | 重锤 | 限定传说 | 主动［熔流］ | `#FC9727` / `#C95300` / `#902104` |
| **破晓** | 下界合金剑 | 传说 | 被动［曦光］ | `#FCEA7A` / `#7A2800` / `#065B97` |
| **晶啸** | 下界合金斧 | 史诗 | 被动［共振］ | `#4C5D6C` / `#A9B2B8` / `#3E0D3B` |

技能都是新写的，并且刻意避开了已有效果：

* **［熔流］**：砸地后热浪**由内向外三重扩散**（半径 3 → 5 → 7，间隔 8 刻），
  每圈点燃并推开当中的敌人。它不留任何常驻场 ——
  计数器从 24 倒数，到零整段结束，场上不残留每刻跑的东西。
* **［曦光］**：对 `#minecraft:undead` 重创 6 点并爆金光，
  对其余生物则以强光致盲 4 秒。同一次挥击，两种结果。
* **［共振］**：命中时震荡**沿晶体传给目标周围 3 格**的敌人，
  范围判定挂在被命中者身上，不做全场扫描。

## 22.2 刻印的纹理：原本全都一样

包里的约定是**一个类别共用一张图**：九枚符文全挂 `custom_model_data` 1110002
（卷轴图），三块符石全挂 1110001（晶石图）。而新加的七件**完全没有
custom_model_data**，直接掉回原版石英 —— 七张卡片长得一模一样。

现在每一枚都有自己的图：取所属类别的底图，按它自己的强调色重新着色。
着色是**逐像素保留亮度**、把色度重映射到「黑 → 强调色 → 白」的渐变上，
所以原画的高光与暗部都还在，只是换了颜色。

顺带把原有的十二枚也一起上了色 —— 新的七件各有颜色而旧的十二件仍然雷同，
看上去会像是漏做了。现在图鉴里 **19 张卡片对应 19 张不同的图标**，
符文（卷轴）与符石（晶簇）两类形状也依然分得开。

## 22.3 开销

新增十件物品（7 刻印 + 3 武器）之后：

```
空闲   872 命令 / 281 次全场遍历   （此前 755 / 244）
守卫   55 道，挡住 566 行
```

每一个技能函数都在 `rpg:item/rune/runes` 与 `rpg:item/epic/epics`
的握持判定之后 —— 空闲一刻只多了十来次 `@a[tag=…]` 玩家检查（玩家表很短），
唯一的实体查找 `@e[type=minecraft:arrow,tag=rpg.rune.pin]` 带类型、走索引。

## 22.4 验证

无头 1.21.11：`give/item` / `give/extra` / `give/box` / `runes` / `epics` /
`tick` / `index` 全部执行干净，零报错；材质包对客户端 jar 校验 `no problems found`。

---

# 第二十三部分：改型、链锯与刻印调色

## 23.1 熔火之锤：改成斧子，蓄力代替经验

基底从 `mace` 改到 `netherite_axe`，显示变换换成包里最常用的
`sword_handheld`（等比 1.195）；品质降到**传说**。

**重锤的附魔按要求保留**，但有一条要说清楚：`density` 的效果是
`smash_damage_per_fallen_block`，只喂重锤的砸击 —— 换到斧子上它会出现在
提示框里但不产生效果（和 14.3 里朗基努斯的情况一样）。`breach`、`fire_aspect`、
`smite`、`unbreaking` 都照常生效。

技能取消了经验消耗，改成和利维坦一样的**蓄力**：`using_item` 在按住期间每刻响，
攒满 30 刻（1.5 秒）才砸下去，四档文字进度 `熔流 ▮▯▯ 起火 → ▮▮▯ 炽白 →
▮▮▮ 将落 → 熔　流`，松手 3 刻内清空。

计数依然用**无条件 `add`** —— 选择器里的 `scores=` 要求记分项已有值，
第一次使用时它不存在，条件恒假，这是 19.1 踩过的同一个坑。

## 23.2 破晓 → 熔岩链锯

改名、升到**限定传说**，被动改成主动，做成 **[切割链锯] 的上位**。

右键起锯，与藤蔓之鞭同一形状：起手只挂一个 60 刻倒计时，
之后每刻按节拍落刀 —— 在 50 / 40 / 30 / 20 / 10 / 1 六个刻各切一轮，
间隔 10 刻正好错开生物的无敌帧。

每一轮的特效照搬原版链锯的做法并烧红：在身前两格召出**放大 2.2 倍的
`evoker_fangs`**（原链锯就是用放大发光的獠牙表现锯齿），配
`trial_spawner_detection` 与熔岩粒子，切到 3.5 格内的一切。
獠牙统一认主，否则会连施法者一起咬。

## 23.3 刻印调色：三次才调对

第一版直接把强调色铺满亮度渐变 —— 太艳，像霓虹。

第二版整体压暗并按比例降饱和，结果只对本来就柔和的色有效：
纯色系（泣血 `dark_red`、风暴 `green`）**相对**降下来仍然是 S=0.70，
和其余的 S=0.25 完全不在一个调子上。

第三版改成**把每个强调色归一化到同一条带**里 —— 保留色相，
把饱和度与亮度都钳到固定区间。全部 19 张最大饱和度降到 **0.35**。

但钳死亮度又带来新问题：`white` 与 `gray` 这类近乎无彩的强调色被映射到同一个调子，
19 张图里有 3 张撞车。最后让亮度**带一点原色的成分**（`0.26 + 0.16 × 原亮度`），
既保住同一调子，又让每一枚重新可分 —— **19 张卡片 19 张不同图标**。

## 23.4 验证

* 蓄力实测：连打 30 次 `forge_trigger` 后 `rpg_forge = 24`
  （说明攒满、触发 `forge_cast`、脉冲计数器已就位）
* 链锯实测：`saw_trigger` 后 `rpg_saw = 60`，`saw_cut` 执行干净
* 进度 1615 → **1617**；`validate.py` 曾报出 6 处
  「unparsable compound」—— 是 `FORGE_TRIGGER` 模板漏了 `.format()`，
  双花括号原样落进了函数，补上后 `no problems found`
* 材质包对客户端 jar 校验通过

---

# 第二十四部分：獠牙落点、新古典装饰，与一个仍未收口的镶嵌

## 24.1 熔岩链锯：獠牙长在目标脚下

原来的写法是在玩家身前固定两格召獠牙 —— 目标一走位整轮就咬空，
只剩显式伤害在生效。现在改成**每个 3.5 格内的目标各自脚下**长出一口獠牙。

「持续受到伤害」也补上了：切过之后给目标挂 6 秒灼烧
（`data merge entity @s {Fire:120s}`）—— 六轮之间的空档由灼烧填满，
目标是一直在掉血，而不是每 10 刻才动一次。

## 24.2 新古典主义装饰层（已加，随后按作者要求移除）

曾经加过一层铜版画册页式的装饰：希腊回纹饰带、斑岩底浮雕徽章、
内联 SVG 月桂分隔、廊柱凹槽、四角挂线；刻意只落在版面家具上，
没有碰卡片（一百多张密集卡片再堆纹样会变噪音），字体也没新增
（Cinzel 本来就是图拉真柱式罗马大写）。

**作者看过之后认为不贴合，已整层移除。** 移除是干净的：
样式块、仅供装饰用的三个色令牌、两处月桂 SVG 全部删掉，
`plate-h` 的对齐回到原本的 `baseline`，罗马数字回到朴素的金色字。
页面从 277 KB 回到 270 KB，浏览器复核确认没有任何残留引用。

记在这里是因为它值得留一条：**这一版的装饰方向被否掉了**，
以后要再动版面风格，别再从新古典这条路走。

## 24.3 镶嵌不生效：修了一半，另一半还没收口

**确认并修好的**：`carry_components_on_inlay` 一直在往
`rpg:command/com/add` 里写 —— 而**那个文件根本没有任何地方调用**，
是原包里的一份遗留副本。真正生效的是 `rpg:command/com` 里的 `##符石附着` 段，
opt_guard 之后被折进 `com/g6`。补丁已改为写进真正生效的那一段，
`com/g6` 现在确实带着 `food` / `consumable` / `custom_data` / `lore` 四样。

**仍未收口的**：在无头服务器上我**没能复现一次成功的镶嵌**。
已经排除的：
* 两个索引标记都正确置上（`rpg.i.weapon_tag1` 与 `rpg.i.add_weapon_tag1`，同一刻同时存在）
* 两个物品同坐标，`distance=..1` 成立
* NBT 路径带引号与不带引号都能解析
* `weapon_level` 物品修饰符只改 lore（`replace_section`），不会冲掉 custom_data
* 直接调用 `com/g6` 同样没有效果

最可能的解释是**这套流程需要玩家在场**：`com` 里多处用 `@a[distance=..5]`，
而武器的「注册」本身走的是 `execute as @a[tag=rpg.h.sword_tag1] …`。
无头服务器上没有玩家，我用 `/summon` 造的物品实体也不等同于玩家真正丢出去的掉落物。

所以这一条**需要你在游戏里验一次**：把符石丢在已注册过的武器上，
看提示框有没有多出技能行。如果仍然不生效，把当时武器的
`/data get entity @e[type=item,limit=1,sort=nearest] Item.components` 发我，
我按真实数据继续查。

---

# 第二十五部分：驱魔体系

## 25.1 先说架构：屏幕下方只有一条 actionbar

这是这一版真正的重点。屏幕下方那条 actionbar **全局只有一份**，
而原先利维坦、熔火之锤、藤蔓之鞭各写各的 —— 谁最后写谁赢，必然互相打架。

现在改成**唯一出口**：技能不再直接写 actionbar，只更新两个分数并挂一个
三刻时效的占用声明；`rpg:hud/hud` 每刻按优先级挑一条渲染。
于是**蓄力条永远压过魔化条，蓄力一结束魔化条自己就回来**。

渲染一条进度条要按格数分支，一百多条命令全摊在一个函数里、
每刻每玩家都过一遍是纯浪费。所以拆成一层调度加每种条各一个函数：

```
execute if entity @s[scores={rpg_hud_t=1..,rpg_hud=1}] run function rpg:hud/s1
execute if entity @s[scores={rpg_hud_t=1..,rpg_hud=2}] run function rpg:hud/s2
execute if entity @s[scores={rpg_hud_t=1..,rpg_hud=3}] run function rpg:hud/s3
execute if entity @s[scores={rpg_hud_t=..0,rpg_taint=1..}] run function rpg:hud/taint
execute if entity @s[scores={rpg_hud_t=1..}] run scoreboard players remove @s rpg_hud_t 1
```

空闲一刻就是这五条落空的判定，真正的 105 条分支只在该显示时才进去。

## 25.2 魔化值

包里那条圣/魔轴（`holy_weapon_tag` / `devil_weapon_tag`）本来只驱动命中粒子，
现在第一次有了长期后果：握着魔器慢慢沾染，握着圣器慢慢洗去，
每 40 刻结算一次（逐刻结算既没必要也白费开销）。

| 档位 | 外显 |
|---|---|
| 0–30 尚可自持 | 灰条，无副作用 |
| 31–60 侵蚀渐深 | 身上泛起紫色暗纹 |
| 61–90 近乎失守 | 暗纹转赤，幽匿魂缠身 |
| 91–100 濒临魔化 | 得力量 I，但**握圣器会灼手**（每次结算掉 1 心）|

最后一档正是世界观里那句「使用越久，越接近原本的主人」——
力量确实上来了，代价是圣性之物开始排斥你。

## 25.3 空缺者

新出现的村民里约六分之一被标记为空壳，**平时与常人毫无分别**；
只有附近有人持圣器时才显形（发光 + 幽匿魂）。
每刻只处理三个新村民，避免村庄载入时集中掷点。

**杀掉空缺者不算驱魔** —— 罪落在动手的人身上（+6 魔化），
并在 actionbar 上留一句「你打碎的只是空壳」。

## 25.4 驱魔仪式：立图腾 → 浇圣水 → 递减 → 炸开

**立**：右键地面放下驱魔图腾。本体是 `item_display` —— 没有 AI、没有碰撞、
不参与任何战斗判定，只是一件立在那儿的东西，代价接近于零。

**浇**：圣水做成**滞留型**而不是喷溅型，这是关键。喷溅药水落地即散，
图腾没有任何东西可以感知；滞留药水会留下 `area_effect_cloud`，
那才是"浇上了"的凭据。熄着的图腾每刻看一眼身边三格有没有这朵云。

**递减**：点燃后共 200 刻，在 200 / 160 / 120 / 80 / 40 五拍上各净化一次，
每拍**一次比一次弱**（12 → 10 → 8 → 6 → 4 点魔化），
同时图腾自身按 1.0 → 0.88 → 0.74 → 0.58 → 0.40 一步步缩小，
肉眼能看出它在烧掉自己。

**炸开**：燃尽时把余威一次吐尽 —— 范围内空缺者全部驱出，
敌意生物受 6 点魔法伤害并被震飞，图腾自我清除。

实测走完整条链：立起（`["rpg.totem"]`）→ 云出现后点燃
（`rpg_totem=171`、`["rpg.totem","rpg.totem.lit"]`）→ 净化拍剥离了村民的
`rpg.vacant`（2 个标记 → 1 个）→ 燃尽后 item_display 自我清除
（`No entity was found`）。

## 25.5 关于生物自定义模型

顺带回答一个问题：**原版数据包不支持自定义生物模型**。
生物的几何体是写死在客户端里的，数据包改不了；
材质包能给现有生物换贴图，但同样改不了模型本身。

真正可行的是 **display 实体**（1.19.4 起）：`item_display` / `block_display` /
`text_display` 都在 1.21.11 里，把它们骑在一个隐形的载体上，
用材质包里的自定义物品模型拼出想要的形体 —— 这是"原版可用"的唯一路子，
也是空缺者将来如果要有独立外观时该走的方向。

## 25.6 开销与验证

* 空闲 872 → **1003 命令 / 281 → 287 次遍历**。多出来的基本都是玩家侧的
  分数判定（玩家表很短），全场遍历只多了 6 次
* 无头 1.21.11：进度 1617 → **1618**，仪式实测 ——
  摆齐四盏后 `rite/check` 走通，村民的 `rpg.vacant` 标记被剥离（2 个标记 → 1 个）；
  拆掉一盏后走失败分支，同样干净
* 中途 `rpg:rite/purge` 被服务器拒绝：`particle flash` 自 1.21.9 起
  **必须带 color**（本项目第 11 部分踩过同一个坑）。`validate.py` 不检查
  粒子参数，是服务器抓到的

---

# 26. 逆圣化，以及长出牙齿的空缺者

第 25 部分把驱魔体系立了起来，但它有一个结构性的缺口：**魔化值只有下行压力，
没有上行诱惑，而且没有终点。** 你只能被动沾染、主动洗掉；游戏从没有哪一刻
邀请你选择堕落，满值也只是给个力量 I。而世界观的核心恰恰是一场交易。

这一部分补的就是这个：给仪表盘一个终点（逆圣化），给驱魔一个非做不可的理由
（有牙的空缺者）。

## 26.1 逆圣化：同一支图腾，另一种烧法

卷六写着「负与负相乘，污染发生反转」。实现上没有另起炉灶 —— 复用驱魔图腾，
在点燃那一刻分岔：

```
execute if entity @a[distance=..7,scores={rpg_taint=100}] run function rpg:rite/light_inv
execute unless entity @a[distance=..7,scores={rpg_taint=100}] run function rpg:rite/light_pure
```

熄着的图腾等的是一朵 `area_effect_cloud`（所以圣水必须是滞留型），点燃时看一眼
旁边站着谁。有满魔化者在场，图腾就不再朝外净化，而是朝着那个人烧：五道灼烧
共 19 点魔法伤害，每道附带缓慢 III，光从暗红一路走到纯白。**人必须站在 7 格内
熬完** —— 走开或者倒下，仪式当场作废。

失败判定要连余下的节拍一起掐掉，否则后面几条会对着一个已经 `kill` 掉的 `@s`
继续跑：

```
execute unless entity @a[tag=rpg.inv.subject,distance=..7] run return run function rpg:rite/inv_fail
```

`return run` 是 1.20.2 之后的写法，它把被调函数的返回值当作**本函数**的返回值 ——
一行同时完成「执行失败流程」和「本函数到此为止」。

## 26.2 蓄力条反着算

反转要看的是「熬过去多少」，而图腾的 `rpg_totem` 是**倒着**数的。分数在图腾身上，
条画在玩家身上，两边不是同一个作用域，所以先把图腾的读数落到一个假名玩家上：

```
scoreboard players operation #inv_now rpg_hud = @s rpg_totem      # as 图腾
...
scoreboard players operation @s rpg_hud_p = #inv_full rpg_hud     # as 受术者
scoreboard players operation @s rpg_hud_p -= #inv_now rpg_hud
```

图腾烧掉的那部分，才是受术者已经撑住的部分。渲染仍旧走第 25 部分那条唯一出口，
只是多了一个占用编号（4 号：逆圣化），所以它天然压过魔化条，也不会和沉锚、
熔流打架。

## 26.3 圣痕：一次给足，不要每刻续

成功的回报是 3 分钟的圣痕。第一版写成每刻 `effect give ... 3 0 true` 续四五个
效果 —— 能用，但每刻五条命令白烧三分钟。改成授予那一下就按整段时长给足
（`effect give @s minecraft:strength 180 1 true`），此后每刻只剩计时、光晕和清场。

清场那一条最初是「守卫 + 被守卫的行」：

```
execute if entity @e[type=villager,tag=rpg.vacant,distance=..6,limit=1] run function rpg:taint/holy_purge
```

但守卫和它守的那行开的是**同一次走查**。守卫在这里一分钱也没省，反而在真有空壳
时把这次扫描付了两遍，还多一次函数调用。一行就够：

```
execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..6] at @s run function rpg:rite/free
```

守卫的价值在于「用便宜的判定挡住昂贵的一段」；当被挡的只有一行、而且那一行的
代价和守卫本身相等时，它就是纯粹的负担。

## 26.4 空缺者：三颗牙

原本的空缺者只有 8 行 —— 持圣器靠近会发光，杀掉加 6 点魔化，仅此而已。驱不驱
都行，于是没人驱。三处改动让它变成必须处理的东西：

* **蔓延**　每 400 刻一拍，随机挑**一个**空缺者向 8 格内伸手，1/4 命中。一个村子
  若无人过问会慢慢整片烂掉。节拍器用记分板而不是实体判定守 ——
  `scoreboard players add` 加一次比任何选择器都便宜。
* **撕壳**　被圣器照住 60 刻，或者挨第一次打，伪装就撑不住：放出两只凋灵怪，
  空壳本身获得速度 II 逃窜。两条路径汇到同一个 `vacant/tear`，用 `rpg.vac.torn`
  防重入。
* **附身转移**　杀死它，空壳**跳到 16 格内最近的村民身上**。附近再无躯体可用时，
  那东西赤裸地留在原地，化作三只「无处可去者」。**剑解决不了它** —— 这正是
  驱魔存在的理由。

转移需要在生物死亡那一刻拿到通知，而原版数据包只有一个口子：进度触发器
`minecraft:player_killed_entity`。实体谓词能不能按标签匹配是个问号，所以把它
单独抄成一个 predicate 文件在服务器上验了一遍：

```
execute as @e[type=villager,tag=rpg.vacant] if predicate rpg:probe_vac run say MATCHED
execute as @e[type=villager,tag=!rpg.vacant] if predicate rpg:probe_vac run say WRONGLY MATCHED
```

第一条打印，第二条不打印 —— `nbt` 谓词对 `Tags` 列表做的是**子集**匹配，可用。

## 26.5 两个 1.21.9 的坑

**其一：`LifeTicks` 改名了。** 凋灵怪的寿命字段在 1.21.9 之后是 `life_ticks`。
写错了不会报错 —— 服务器照常召唤，只是那一段 NBT 被静静丢掉，碎片变成永久存在。
`data get` 回来是「Found no elements matching LifeTicks」才露馅：

```
summon minecraft:vex 0 100 0 {life_ticks:600}
data get entity @e[type=vex,limit=1] life_ticks   ->  586
```

顺手把包里其余实体专有字段也验了：`Value`（经验球）、`Warmup`（唤魔者尖牙）、
`Motion`、`Health` 全部仍是大驼峰。改名是逐个字段挑的，不是全表改。

**其二：`scores=` 只认已经存在的分数。** 这是本项目第三次踩它。HUD 的状态条
挂在 `rpg_hud_t=..0` 上，而 `rpg_hud_t` 只有蓄力技能才会写。结果是：**一个从没
用过蓄力武器的玩家，魔化条永远不显示** —— 第 25 部分交付时就带着这个洞，只是
测试者恰好都先摸过利维坦。一行补上：

```
scoreboard players add @s rpg_hud_t 0
```

`add 0` 会把不存在的分数落成 0，是「确保这个分数有值」的最省写法。

## 26.6 build.sh 不该不管手持变换

提交前 `git status` 里躺着一个没人动过的文件：`twin_handheld.json` 从等比缩放
1.195 退回了作者原本的 `[1.46, 0.85, 0.85]` —— 正是当初报过两次的刀刃剪切。

原因是流程分家了。`add_twins` / `add_lucifer` / `add_leviathan` / `add_epics` /
`retype_longinus` 这几个生成器**同时**往数据包和材质包写，而 `fix_display.py`
只挂在 `rp_build.sh` 末尾。于是单独跑一次 `build.sh`，手持变换就被悄悄还原。
把它也接到 `build.sh` 末尾即可（`fix_display` 是幂等的：对已经等比的数值再解一次，
解出来还是同一组）。

教训不在这一个文件上：**凡是被两条流程共同写入的产物，修正必须挂在每一条流程的
末尾，而不是其中一条。**

## 26.7 开销与验证

* 空闲 1005 → **1094 命令 / 288 → 288 次遍历**。遍历没有增加 —— 命令数的涨幅
  几乎全在 `hotspots` 的静态模型里：它读不出记分板的值，只好把逆圣化条、圣痕条
  这些分数守卫后面的分支一并计入。实际每刻新增的工作是 6 条（HUD 三条、
  魔化一条、蔓延节拍器两条）
* 最坏情形 1587 → 1776，但那是仪式、碎片、四种进度条同时开火的假想值，
  实际互斥
* 函数 279 → 278（`holy_purge` 合并掉了）；进度 34 → 35
* 无头 1.21.11 实测，服务器零抱怨，四条路径逐条验过：谓词按标签匹配 ✓、
  附身转移把空壳搬到邻居身上（两个村民先后自报 vacant）✓、
  照够 60 刻撕壳并放出碎片、`rite/free` 顺手收走碎片 ✓、
  受术者不在场时 `return run` 让图腾自毁 ✓、圣痕光环净化空壳且计时正常递减 ✓
* 图鉴补上第 IX 节「驱魔体系」：魔化四档、空缺者三颗牙、仪式五拍的净化量与
  图腾尺寸、逆圣化的成败两栏。卷六早就写着逆圣化，此前却没有任何地方告诉玩家
  它怎么触发

---

# 27. 七十二柱契约：一本书，两种行为

第 26 部分把魔化值的两端补齐了 —— 底下有驱魔，顶上有逆圣化。但整条曲线仍然
是**被动**的：你只会不小心沾上，然后想办法洗掉。卷五写着「边缘者借用魔神的力，
魔神借契约进入边缘者的心」，而包里没有任何东西**邀请你选择堕落**。

契约补的就是这一步。它是一本书。

## 27.1 一本书，两种行为

`minecraft:using_item` 在按住右键期间**每刻都会响**。签约和动用都该是一次性的，
所以先用一个八刻的短锁去抖，再按有没有柱位分岔：

```
execute if entity @s[scores={rpg_pact_t=1..}] run return 0
scoreboard players set @s rpg_pact_t 8
execute unless entity @s[tag=rpg.pact] run function rpg:pact/sign
execute if entity @s[tag=rpg.pact] run function rpg:pact/invoke
```

手里这本是哪一柱，靠 `if items` 读 —— 只看主手那一件，不翻背包：

```
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:3}] run function rpg:pact/sign3
```

`*[...]` 这种「任意物品 + 组件断言」的写法在服务器上单独验过：对第三柱命中、
对第四柱不命中、`unless ... {pact_signed:1b}` 能正确识别未盖印的书。

## 27.2 力量借的是原件，不是仿制品

契约借的就是同一位魔神的力，表现理应一模一样。所以路西法那一柱直接调罪器
自己的施法路径：

```
tag @s add rpg.luci.cast
execute at @s anchored eyes run function rpg:item/extra/lucifer_lance
execute at @s rotated ~ 0 run function rpg:item/extra/lucifer_fangs
tag @s remove rpg.luci.cast
```

`lucifer_lance` 的伤害归属读的是 `@a[tag=rpg.luci.cast]` —— 把这个标签临时挂上，
它就能脱离武器独立跑。利维坦的落锚同理（血税不收：契约的代价是魔化，不是生命）。
只有那些和武器状态机缠死、没法独立调用的（亚巴顿的收割、别西卜的余烬、
萨麦尔的毒），才在契约这边另写一份同味道的。

## 27.3 恩赐与枷锁：写一次，长期生效

七柱各有一份恩赐和一份枷锁。第一反应是逐刻 `effect give`，但这类长期修正根本
不该按刻烧 —— 属性修饰符写一次就留在玩家身上：

```
attribute @s minecraft:max_health modifier add rpg:pact/3/boon0 6 add_value
attribute @s minecraft:max_health modifier remove rpg:pact/3/boon0
```

（资源路径里带 `/` 与数字都合法，服务器实测 20 → 26 → 20 干净往返。）
所以七柱里有五柱的常驻部分**每刻零开销**。只有两柱必须逐刻看：萨麦尔的攻击附毒
走 `rpg.hurt` + `on attacker`，玛门的拾取吸附要扫掉落物 —— 这两条各自挂在
自己柱位的分数判定后面，没签那一柱的人连函数都不会进。

玛门那条是全包第二个 NBT 匹配选择器（`nbt={PickupDelay:0s}`，用来放过刚扔出去的
东西）。NBT 选择器是最贵的一种，但它的候选集已经被 `type=minecraft:item` 和
6 格半径压得很小，而且只有签了第七柱的人才会付。

## 27.4 签完约不松手，力量就自己放出去了

八刻的锁意味着按住不放会**再响一次**。第二响时玩家已经有了柱位，于是走 invoke ——
签约当场把力量放了出去，还顺带扣了 3 点魔化。

修法不是把锁加长（那只是把窗口推远），而是**签约当场把冷却拉满**：柱中之力
得先与人相合。这一改顺带填掉了一处 `scores=` 空值陷阱 —— `rpg_pact_cd` 从签约
那一刻起就有值了，不必再指望第一次 invoke 去创建它。

## 27.5 书丢了就再也用不了

死一次把书掉了是常事。柱位记在玩家身上，书却没了 —— 重新拿一本空白的同柱之书，
`invoke` 只认 `pact_signed`，于是直接判成「攥错了书」，人就卡死在这儿。

加一条**重新盖印**：柱位对得上就地补签（`sign%d` 本身就是幂等的，属性先撤再加），
对不上才是真的攥错了。

```
execute if entity @s[scores={rpg_pact=3}] if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:3}] run return run function rpg:pact/sign3
```

## 27.6 玛门补上了第七宗罪

卷五的七宗罪表里，贪婪那一格一直是空的 —— 六位领主各有一件罪遗武器，玛门没有。
第七柱的契约填上了它：贪婪不制造东西，它只让已有的东西变多（8 格内掉落物尽数
翻倍）。翻倍的做法是把整堆的数量读出来乘二写回去，比逐件复制便宜得多：

```
execute store result score #gild rpg_pact run data get entity @s Item.count
execute if score #gild rpg_pact matches 1..32 run function rpg:pact/p7_double
```

只处理 32 及以下的堆 —— 再多翻倍就越过 64 的堆叠上限了。实测 5 → 10。

## 27.7 图鉴：从同一份数据长出来

第 X 节的七柱表不是手写的。`add_pact.py` 把七柱连同冷却、魔化代价、
`custom_model_data` 区段一起吐成 `_pact.json`，`emit_guide.py` 读回去渲染 ——
调一个数值，页面自己跟着走，这和 `n_of()` 当初解决的是同一个漂移问题。

顺带一个配色问题：罪器的强调色是给 Minecraft 的**深色 tooltip** 挑的，
路西法那支 `#00491c` 搬到图鉴的深色底上几乎是黑的。于是加了一层 `on_dark()`：
保住色相、把亮度抬到 0.62、饱和度收在 0.30–0.48。第一版还把七柱染重了两组
（别西卜与玛门同为黄、亚巴顿与利维坦同为蓝），改源色相分开，并给近乎中性的
来源留一条例外 —— 硬抬饱和度会把亚巴顿的「虚无」染成蓝色。

## 27.8 开销与验证

* 空闲 1094 → **1122 命令 / 288 → 292 次遍历**。新增的四条根命令全是玩家作用域，
  且各自带柱位判定；多出来的遍历是 `hotspots` 把两条柱位专属的 tick 一并计入了
  静态模型（它读不出记分板）
* 函数 278 → **316**，进度 35 → **36**
* 无头 1.21.11 实测，服务器零抱怨。整条签约链在替身身上跑通：
  柱位落到 3 ✓、冷却起手即 300 ✓、最大生命 20 → 26 ✓、书被盖印 ✓、
  毁约后 26 → 20 且柱位归零 ✓；七道力量逐个跑过，`give/extra` 与
  `give/box` 全部合法
* 贴图暂缺，七本书沿用原版附魔书外观。`custom_model_data` 已按柱位排好
  （1110031–1110037），美术补上时只要在材质包给 `enchanted_book` 加一段
  `range_dispatch`，数据包一个字都不用改

---

# 28. 多人适配：单人把三类错藏成了同一件事

这个包一直是在单人里写、在单人里测的。而单人恰好把三类完全不同的错误
**混成了同一件事**，所以它们全都藏得很好：

* **`@a` 就是"我"。** 只有一个玩家在线时，`@a[tag=...,limit=1,sort=nearest]`
  读起来就是"施法者"。两个人在线，它可能解析成**另一个人**。
* **一个标签就是一个开关。** 在同一次函数调用里生死的标签没问题；一旦跨刻
  存活，两个玩家就可能同时挂着它，此时任何不带距离的 `@a[tag=...]` 会一起打到。
* **`bossbar ... players @s` 是赋值，不是追加。** 写在 `execute as @a` 后面，
  每个玩家轮流把名单覆盖成自己。

外加一类卡顿：`execute as @a` 后面挂的一切，在 N 人服上要付 N 遍。

先写了 `mp_audit.py` —— 只报告不改写，因为每一处都需要人来判断当初的意图。

## 28.1 审计工具自己先踩了一个坑

审计第一版把 `damage_scan` 判成"已走索引，无需担心"。错的：它的选择器是
`@e[type=!#rpg:no_damage_track,...]` —— **否定**类型过滤。实体类型索引只能
回答"给我所有僵尸"，回答不了"给我所有不是这些的"；后者仍然要把盒子里每个
实体都访问一遍才知道要跳过谁。

```python
WALK  = re.compile(r"@e\[(?![^\]]*\btype=(?!!))[^\]]*\]")
TYPED = re.compile(r"@e\[[^\]]*\btype=(?!!)[^\]]*\]")
```

改完分类，最贵的那条立刻浮出来。

## 28.2 damage_scan：每人三次全表走查

它挂在 `execute as @a at @s` 后面，而三行各自开一次那个否定过滤的选择器 ——
**五个人在线就是每刻十五次全表走查**，全包最贵的一条按人数放大的路径。

三行的先后依赖全在**同一个实体身上**（先记血量、再对齐基准、再比对），
所以把循环翻过来，一次遍历、逐实体把三件事做完，结果逐字相同。
`opt_invert` 当初因为"有回写又有回读"保守地放过了它，但那个依赖是实体内的，
翻转恰好保留。

单人无头实测（`rpg.hurt` 每刻会被 `command/index` 抹掉，所以整个
"快照 → 打一下 → 重扫 → 断言"必须塞进同一刻）：

* 打了一下的实体被标记 ✓
* **刚出现的实体不被标记** ✓ —— 这条同样重要，它正是当年读档卡顿的修复

## 28.3 逆圣化：一处失败掐掉全世界

`rpg.inv.subject` 跨刻存活，而 `inv_fail` 里写的是不带距离的
`@a[tag=rpg.inv.subject]` —— **甲的图腾失败，会把地图另一头乙的仪式一起判掉。**

同一个标签还有第二个毛病：受术者若死在圈外，标签留在身上没人来摘，
下一场仪式的判定会被这个幽灵干扰。所以除了限距，再配一份寿命
（图腾总长 200 刻，给 220 刻），过期自动收场。两条都是玩家作用域，
没在做仪式的人一条也进不去。

## 28.4 熔岩链锯的獠牙认错主人

```
execute as @e[tag=rpg.saw.fang] run data modify entity @s Owner set from entity @p[tag=rpg.h.dawn_tag1] UUID
```

两处都是单人下看不出来的：`@e[tag=rpg.saw.fang]` 不带距离也不带类型，会把
**另一个玩家**刚召出来的獠牙一起改主人、连标签一起摘掉，对方那一轮当场断掉；
`@p[tag=rpg.h.dawn_tag1]` 取的是"离目标最近的持锯者"，两个人都拿着锯时，
伤害记到站得更近的那一个头上。

改法是包里已有的惯用形：挂一个**只在本次调用里存活**的施法者标签。
这里有一条支撑全部归属逻辑的不变量值得写下来：

> Minecraft 的命令执行是单线程的，一个函数跑完才轮到下一个。所以一个
> **在同一次调用里增删**的标签，另一个玩家的执行永远观察不到 ——
> `@a[tag=rpg.xxx.cast,limit=1]` 因此是精确的，而不是"碰巧最近的那个"。

按这条重新审了一遍，`rpg.luci.cast` / `rpg.pact.cast` / `rpg.levi.cast`
全部合规；真正越界的只有链锯那两行。

## 28.5 Boss 血条：三个人在场只有一个看得见

```
execute as @a[distance=..20] at @s run bossbar set minecraft:devil players @s
```

`bossbar ... players` 是**赋值**。逐个玩家写，等于每人轮流把整份名单覆盖成
自己，最后只有一个人看得见血条。一次设整组即可，顺带少跑 N−1 条命令。

**而且血条在全新服务器上根本不存在。** `command/bossbar.mcfunction` 建了
`minecraft:devil`，但**没有任何地方调用它** —— 作者本机存档里它之所以在，
是因为当年手敲过一次，而 bossbar 存在 level.dat 里。换一个全新的服务器存档，
Boss 一出场每条 `bossbar set` 都会报"没有这个 bossbar"。挂进 load 标签解决。

这个 bug 只有在**全新存档**上才会出现，所以本机怎么测都测不出来。

## 28.6 顺手：把标签选择器的类型补回去

`@e[tag=rpg.levi.anchor]` 要走一遍全实体表，`@e[type=minecraft:marker,
tag=rpg.levi.anchor]` 走类型索引。语义相同，代价差一个数量级 ——
而类型本来就写在召唤它们的那条 `summon` 里，不必手填。

`opt_type.py` 收集每个标签的来源，只对**从未**被 `tag ... add` 写过、
且所有召唤点类型一致的标签补类型（否则这个标签可能挂在任何实体上，
补类型会改语义）。67 处选择器因此从全表走查变成索引查询。

这不是多人专属的优化，但它和多人直接相关：全表走查的代价随世界里的实体数
增长，而实体数正是随在线人数增长的东西。

## 28.7 开销与验证

* **每多一个玩家的固定开销：1 次全表走查/刻**（原来是 3 次）。
  无条件的按人数入口只有四个，其中三个零走查；另有 19 个带柱位/分数判定的
  入口，每人每刻只付一次选择器判定，不做那件事就不进函数体
* 空闲遍历 292 → **275**；最坏情形 578 → **525**（`opt_type` 的功劳）
* 多人修正 13 处，选择器补类型 66 处（复查后见 28.8）
* 无头 1.21.11：服务器零抱怨（只剩一个离线环境取不到 Mojang 公钥的网络报错，
  与包无关）。单刻断言两条全过；血条在全新存档上被正确建出（max 1000）

一句话总结这一章：**单人测不出多人的错，因为单人下那些错全都长得像正确。**

## 28.8 复查：先怀疑自己上一轮的改动

第二遍不是把第一遍重做一次，而是换个方向 —— **先假设上一轮我改坏了东西**。
最可疑的当然是 `opt_type.py`：一个自动批量重写器，一口气改了 67 处选择器。

它确实改坏了一处。

`opt_type` 从 `summon` 推断类型，而它的正则抓的是**外层**类型，然后在整行里
找 `Tags:[...]`。包里的溺尸骑士是这个形状：

```
summon horse ~ ~ ~ {... Passengers:[{id:drowned, ... Tags:["king_tag"] ...}]}
```

于是 `king_tag` 被记成了 `horse`，重写出来的
`@e[type=minecraft:horse,tag=king_tag]` **一个实体都匹配不到** ——
王的那套逻辑静悄悄地没了。**语法完全合法**，所以 `validate.py` 不吭声，
服务器也不吭声；`hotspots` 甚至会因为它"走了索引"而报告变快了。

这类错误没有任何自动检查能抓到，只能靠**回头质疑自己的假设**。

修法上还有个二阶陷阱：只把 `Passengers:[...]` 挖掉是不够的。假如同一个标签
既直接召唤在 A 类型上、又作为 B 类型的骑手出现，挖掉之后只看得见 A，
收窄成 A 就会漏掉所有 B。所以最终规则是：**凡是在骑手块里露过面的标签，
一律不收窄**。宁可少省几处遍历 —— 在一个批量重写器里，"绝不改错"比
"多快一点"值钱得多。

收窄数从 67 降到 66，并且现在可以断言：没有任何被收窄的标签出现在骑手块里。

## 28.9 顺手捞到的一条：全世界绑一遍再逐个问

`item/chestplate/off` 是 `command/tick` 调的**第一个**函数，八行长这样：

```
execute as @e at @s if entity @s[scores={absorption=0..},tag=X] run ...
```

`@e` 不带任何过滤 = 世界上每一个已加载实体。对每一个都要 `as` 绑定、
`at` 重定位，然后再跑一次嵌套 execute 去问"你是不是我要找的"。
把条件折回选择器里，筛选就发生在遍历本身：

```
execute as @e[scores={absorption=0..},tag=X] at @s run ...
```

筛的是同一批实体，但不匹配的那些连执行上下文都不用建。`hotspots` 的遍历数
不会变 —— 它数的是选择器，而这一改省的是**每次遍历内部**的开销，
那是它模型之外的东西。

## 28.10 复查里确认没问题的部分

* `scoreboard players reset *`（10 处）—— 全服清分。看着吓人，但每一处的
  "算 → 用 → 清"都在同一个函数里连续发生，而命令执行是单线程的，
  中间插不进别人。安全
* `command/com` 里那 168 处不带距离的 `@a[tag=...]` —— 它们是**遍历**
  （"每个手持某物的玩家，改他自己手里那件"），不是**归属**
  （"找出施法者是谁"）。前者不带距离才是对的
* 上一轮那 12 处修正逐条对着产物看过，都在
* 归属用的 `@a[tag=...cast,limit=1]` 全部合规 —— 靠的是那条单线程不变量

## 28.11 关于让 Codex 复查

作者提议让 Codex 再看一遍。这台机器上没装 `codex` CLI（`F:/AGENT/codex`
只是个放旧版包的工作目录，npm 全局也是空的），所以这一遍还是自己过的。
不过换方向复查确实值了 —— `king_tag` 那个洞，正是第一遍绝不会发现的那类：
**它是第一遍的产物**。

---

# 29. 佣兵小队：让敌对生物听话

一个独立分支：花钱雇人，给他们配刀，指哪打哪。不与罪器、契约、驱魔任何一条
耦合 —— 玩家可以完全不碰前面那些体系，只带着一队人打。

## 29.1 唯一能从根上断掉的地方

要用尸壳的模型就得用尸壳这个实体，而尸壳是**敌对生物**：它自带
`NearestAttackableTargetGoal`，会主动打玩家和村民。而原版命令**没有任何办法
清除一个生物的当前目标** —— `Target` 不在可写 NBT 里，`AngryAt` 只对中立生物
有效。所以"让它别打老板"这件事**没法在事后补救**。

那种"打之前判断一下是不是自己人"的写法，总会有漏网的一刻。唯一能从根上断掉的
地方是**索敌半径**：

```
attributes:[{id:"follow_range",base:0}]
```

先做了对照实验才敢往下写：

| | 结果 |
|---|---|
| 普通生物 + 一个村民 | 当场砍死（`Villager was slain by ...`） |
| `follow_range: 0` + 一个村民 | 放着不管，村民满血 **20.0f** |

它永远不会自己选中任何东西，**因此也永远不可能误伤雇主**。这条安全性是
**结构性**的，不是判定兜出来的。

代价是它也不会自己打该打的人。于是移动与攻击全部由数据包驱动。

## 29.2 让它站住，然后自己开车

`movement_speed: 0` —— 让它自己的 AI 推不动它，省得和我们的位移打架。
（`NoAI` 不行：那样连重力都没了，人会浮在空中。）

位移用 `tp` 而不是 `Motion`：`Motion` 要先把朝向换算成 xz 分量，而沿
`^ ^ ^` 走一步不需要任何三角函数。

```
tp @s ~ ~ ~ facing entity <目标>
execute at @s rotated ~ 0 positioned ^ ^ ^0.22 if block ~ ~ ~ #minecraft:replaceable run tp @s ~ ~ ~
```

`rotated ~ 0` 把俯仰归零 —— 不然朝着高处的目标会走上天。客户端的走路动画是按
**位置变化**算的，所以 tp 出来的佣兵看起来仍然在走路。实测三刻走了 0.66 格，
正好是 3 × 0.22。

## 29.3 配武器不需要任何数值表

伤害读的是佣兵**自己的 `attack_damage` 属性**，而这个属性天然含手持武器：

```
空手                4.0
塞一把下界合金剑     11.0
```

所以"给佣兵配武器"这件事不需要维护任何武器数值表 —— 你把本包**任何一把**
自定义武器塞给他，他就按那把武器的数值打，包括以后新加的。

`damage` 的数值吃不了记分板，所以走**宏**（本包第一次用）：

```
execute store result storage rpg:squad atk int 1 run attribute @s minecraft:attack_damage get
function rpg:squad/strike_do with storage rpg:squad
```

```
$execute as @e[tag=rpg.sq.mark,...] run damage @s $(atk) minecraft:mob_attack by @e[tag=rpg.sq.striker,limit=1]
```

实测村民 20.0 → 16.0，与属性值一致。

## 29.4 换成尸壳带来的两件事

作者中途把卫道士换成了尸壳。尸壳省了一件事（**不怕阳光**，白天不自燃），
但多带来两件，都不是改个 id 能了事的：

**其一：它属于 `#minecraft:zombies`。** 本包每刻会给新出生的僵尸类重掷全套
战利品装备，还有几率直接替换成强化变种。不排除的话，刚雇来的人转头就被系统
当野怪重新配了装。已在 `zombie_batch` 那一行按标签摘出去。

**其二：尸壳泡在水里会转化成普通僵尸。** 而转化是**换一个实体** ——
标签与记分板一起没了，队员就这么凭空消失。所以佣兵不下水：踩到水立刻召回。

## 29.5 一个自己制造的静默故障

第一版 `squad/step` 服务器直接拒绝加载：

```
Whilst parsing command on line 6: Expected double at position 36: ...oned ^ ^ ^<--[HERE]
```

原因是**变量名撞了**：常量 `STEP = "0.22"` 在文件后面被同名的模板
`STEP = """..."""` 覆盖，于是 `positioned ^ ^ ^%(STEP)s` 展开成了整段模板文本，
命令里只剩 `^ ^ ^` 后面跟着一个 `#`。

`validate.py` 放过了它 —— 它不检查 `positioned` 的参数类型。又是服务器抓到的。
常量改名 `STRIDE`，并顺手全包扫了一遍有没有别的模板没展开干净。

## 29.6 多人从第一行就在考虑

前两部分刚把全包过了一遍多人适配，这一套是在那之后写的，所以从一开始就按
多人写：

* 每个雇主有一个 `rpg_squad` 编号，队员携带同一个编号。**认人靠编号比对，
  不靠"最近的玩家"**
* 雇主在自己那一段里临时挂 `rpg.sq.boss`，队员据此找人 —— 靠的是第 28 部分
  那条不变量：命令执行是单线程的，同一刻只可能有一个玩家挂着它
* 每刻只有**一条**玩家作用域判定；真正的遍历在雇主自己的函数里
* 一支队伍最多只有一个标记目标，所以"目标还在不在"在雇主那一层问一次就够，
  不必每个队员各开一次全表走查；剩下必须看距离的两条都限了上界

## 29.7 开销与验证

* **每多一个玩家的固定开销仍是 1 次全表走查/刻** —— 小队加的是一个
  *带标签判定*的入口（19 → 20 个），没雇人的玩家一条也进不去
* 空闲 275 → **283 次遍历**（多出来的是 `hotspots` 把标签守卫后的分支
  一并计入了静态模型；真正每刻新增的是一次选择器判定）
* 无头 1.21.11，服务器零抱怨，整条链路走真实的 `lead` 路径验过：
  召出佣兵 ✓、不被配装流水线抓走 ✓、不自主攻击村民（满血 20.0f）✓、
  三刻推进 0.66 格 ✓、宏伤害 20.0 → 16.0 ✓、
  配剑后攻击力 4 → 11 ✓、目标死亡后自动归队 ✓、退款战利品表产出正确 ✓

---

# 重建方式

```bash
bash "_tools/build.sh"
```

```bash
bash "_tools/rp_build.sh"
```

数据包流程：`migrate.py` → `optimize.py` + `opt_spawn.py` + `opt_misc.py`
　　　　　→ `add_items.py` + `add_skills.py` + `add_twins.py`
　　　　　→ `add_lucifer.py` + `add_leviathan.py`
　　　　　→ `add_runes.py` + `add_epics.py` + `add_exorcism.py`
　　　　　→ `add_pact.py` + `add_squad.py`
　　　　　→ `retype_longinus.py` + `make_boxes.py` + `fix_display.py`
　　　　　→ `opt_mp.py` → `opt_index.py` + `opt_type.py` + `opt_guard.py` + `opt_invert.py`
　　　　　→ `validate.py` → `hotspots.py`
材质包流程：`rp_migrate.py` → `import_twin_art.py` → `fix_art.py`
　　　　　→ `add_items.py` + `add_skills.py` + `add_twins.py`
　　　　　→ `add_lucifer.py` + `add_leviathan.py` + `add_runes.py` + `add_epics.py`
　　　　　→ `retype_longinus.py` → `fix_display.py`
　　　　　→ `rp_validate.py`
打包与安装：`package.py --install`（写回 1.21.11 实例的 resourcepacks 与各存档）
存档升级：`world_upgrade.py <存档路径> <临时目录>`
图鉴生成：`bash _tools/guide_build.sh`（含贴图内嵌）
贴图裁剪：`fix_art.py <材质包>`　新装备与技能：`add_items.py` / `add_skills.py`
闲置贴图反查：`unused_textures.py <材质包>`
无头实测：`server_test.py`（数据包）、`launch_test.py`（材质包）
多人审计：`mp_audit.py <数据包>`（只报告不改写）
多人修正：`opt_mp.py`　标签选择器补类型：`opt_type.py`

实机测试（会开一个 854×480 的临时客户端窗口，几十秒后自动关闭）：

```bash
python "_tools/launch_test.py" file/rpg_resourcepack_claude 200 "<临时 gameDir>"
```

两条流程当前均为 **no problems found**，数据包迁移幂等（重复运行不再产生改动）。
