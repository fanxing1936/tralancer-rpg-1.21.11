# 破碎大陆 · Eretz Ha-Shevarim

> אֶרֶץ הַשְּׁבָרִים ｜ 碎片之地
>
> 这是破碎大陆的见证：世界曾经完整，后来因神陨、堕天与权柄的分裂而成为碎片。

一套 Minecraft **Java 版 1.21.11** 的 RPG 内容组合：数据包 + 材质包 + 一份完整图鉴。
世界观全文见 [`LORE.md`](LORE.md)，图鉴里也整合了同一份叙事。
原作是 1.21 版本，本仓库是它的 1.21.11 升级版，并在升级过程中做了性能重构与内容扩充。

数据包格式 `94.1`，资源包格式 `75.0`（取自 `1.21.11-Fabric.jar` 的 `version.json`）。

---

## 内容

| 路径 | 说明 |
| --- | --- |
| `rpg/` | 数据包 —— 放进 `存档/datapacks/` |
| `resourcepack/` | 材质包 —— 放进 `.minecraft/resourcepacks/` |
| `rpg-datapack-1.21.11.zip` | 数据包 zip（同内容，方便分发） |
| `rpg-resourcepack-1.21.11.zip` | 材质包 zip |
| `TRALANCER-RPG-图鉴.html` | **图鉴**，双击即可打开 |
| `DEBUG-COMMANDS.md` | **完整调试指令手册**（公开入口、前置条件、影响范围与风险） |
| `LORE.md` | **《破碎大陆》世界观全文**（圣经体叙事，七卷） |
| `DROP-POLICY.md` | 生物死亡掉落白名单及原版硬编码例外 |
| `ENGINEERING.md` | **持续维护的完整工程日志**（含每一处改动的原因与验证） |
| `_orig/` `_orig_rp/` | 原始 1.21 数据包 / 材质包备份，未改动 |
| `_tools/` | 迁移、优化、校验、打包、无头测试脚本 |

## 地图

配套的 **1.21.11 地图**（WorldPainter 灰度图地形，已装好本数据包）体积较大，
所以放在 [**Releases**](https://github.com/fanxing1936/tralancer-rpg-1.21.11/releases) 里而不是仓库树内。

下载后解压到 `.minecraft/saves/`，进游戏即可 —— 数据包已经在里面，计分板会自动建好。
注意：Release 里地图内置的是删减前的数据包，用本分支时请把存档 `datapacks/` 里的旧包换成新构建的 ZIP。

原图是 1.21 存档，用 `_tools/world_upgrade.py` 走真实 1.21.11 服务器的
`--forceUpgrade` 全量转换（262144 个区块逐个过 DataFixerUpper，
不是进游戏后边走边转），`level.dat` 与抽样区块的 DataVersion 均为 **4671**。
分发前已移除作者的 `playerdata` / `advancements` / `stats`，玩家从头开始。

## 安装

1. 数据包放进存档的 `datapacks/`，材质包放进 `resourcepacks/` 并在游戏里启用。
2. 进入世界。计分板会由 `#minecraft:load` 自动建好，**不需要**再手动跑
   `function rpg:command/soreboard`。
3. 取装备：

```
/function rpg:command/give/box
```

一次给出 **13 只潜影盒**：武器 2 箱，以及防具、符文镶嵌、锻造升级、药剂功能、
测试物、罪约契约、上位契约、卡巴拉秘仪、驱魔器具、真名档案、裁决遗物各 1 箱。
其中上位契约箱含旧约与新约，卡巴拉秘仪箱含血契、十源质与真·十字架。
（想逐件取仍可用 `give/weapon`、`give/item`、`give/weapon_up_item`、`give/extra`。）

## 内容概览

* **31 件武器**：剑、斧、弓、弩、重锤、长枪，分勇者 / 史诗 / 传说 / 恶魔 / 神圣五档
* **七位恶魔领主**：路西法、利维坦、亚巴顿、别西卜、萨麦尔、贝利尔与玛门
* **35 名所罗门罪仆**：七柱各辖先锋、猎手、司祭、咒使、处刑者五职；每名罪仆拥有独立命名术式、柱位配色、蓄势边界与命中反馈
  司祭启用原生 AI 与 0.28 基础移速，保留治疗和增益术式；重载后已生成的司祭也会自动修复。
* **圣殿双柱**：雅斤与波阿斯，左右手双持触发联动
* **14 件护甲**、12 种药水、符文、镶嵌石、磨刀石与武器升级树
* **恶魔生态**：35 名具备独立职责、技能和掉落的所罗门罪仆，以及七宗罪领主
* **卡巴拉生命之树**：卡巴拉血契、十源质、Daath 节点与真·十字架转化仪式
* **上位契约**：十源质归位后显化的『旧约』，以及权与力合一后的『新约』

当前开发范围只保留 **装备、恶魔生态、契约体系** 三块。第一章战役《空缺者》、无尽驱魔《七柱回廊》、
圣所祷告与佣兵小队已从本地分支移除（生成器、校验、配置、文档一并删除），需要时可从 `main` 分支的历史找回。

全部条目连同**按游戏内真实合成的图标**（染色、盔甲纹饰、药水颜色、附魔光泽）
都在 `TRALANCER-RPG-图鉴.html` 里。

## 卡巴拉生命之树与上位契约

手持 `[秘仪]卡巴拉血契` 长按右键，会依照玩家朝向在地面展开生命之树。将
`[源质]01 · 王冠` 至 `[源质]10 · 王国` 分别带入对应圆心并长按右键；十源质全部
归位后，仪式主持者只会获得一次 `[契约]旧约`。长按契约书即可与上帝立约。

`[已立约]旧约` 每 20 秒给予 1 秒生命恢复 I，并在每轮魔化结算后抵消 2 点积累。
长按右键施展 `[十诫净界]`：净化 10 格内的恶魔，造成其 20% 最大生命值伤害；
生命不高于 25% 的目标直接斩杀。技能冷却为 **30 秒**。

十源质归位后，站入 **Daath 节点**圆心并手持 `[秘仪]真·十字架` 长按右键。
十件源质展示物会向十字架汇聚；仪式结束时十字架、旧约与整棵生命之树一同收束，
主持者获得未签订的 `[契约]新约`。测试或制作时可用
`/function rpg:ritual/life_tree/give/all` 领取卡巴拉血契、十源质与真·十字架。

签订新约后，魔化显示会由 **权柄完整度**取代，并免疫失明与黑暗。权柄上限为 100，
每 **2 秒恢复 1 点**；新约的三种持物用法共用同一条上位契约冷却：

| 操作 | 权能 | 实际效果 | 冷却 |
| --- | --- | --- | --- |
| 普通长按新约 | `[创世净光]` | 向前延伸 20 格；恶魔受到 25% 最大生命值伤害与 15 点基础伤害，并获发光 8 秒、虚弱 I 6 秒 | 20 秒 |
| 潜行长按新约 | `[伊甸敕界]` | 半径 8 格；恶魔受到 15% 最大生命值伤害与 10 点基础伤害，并获缓慢 III、虚弱 II、发光各 8 秒；范围玩家清除失明、黑暗、凋零、中毒、缓慢、虚弱，并获生命恢复 II、抗性 I、伤害吸收 II 各 6 秒 | 30 秒 |
| 手持七罪契约书长按 | `[赦免]` | 直接动用该柱契约之力；不签订恶魔契约、不增加魔化，也不承受契约反噬 | 15 秒 |

玩家面板的“契约与权柄”页另有两项权柄消耗技：`[终末圣裁]` 消耗 25 点并为下一次
对恶魔的攻击覆印 30 秒，净化目标、附加 20% 最大生命值与 10 点基础伤害，目标生命
不高于 20% 时直接斩杀；`[圣子恩赐]` 消耗 35 点，净化并救治 12 格内最近的一名
其他玩家。范围内没有同伴时不会扣除权柄。

七罪领主处于真名调查阶段时仍保留 **175 / 700 生命**的仪式保护线，旧约斩杀不能
跳过调查与裁决。领主被法阵束缚后，`[十诫净界]`、`[创世净光]`、`[伊甸敕界]`、
`[终末圣裁]` 不再直接扣血，分别改为增加 **20 / 25 / 15 / 20 点稳定度**；普通恶魔、罪仆与蝇群仍
承受完整的百分比伤害。

要解除旧约或新约，手持对应的 `[已立约]` 契约书，在 **6 格内燃着的驱魔图腾**旁
长按右键。图腾的燃烧状态会被消耗，契约书恢复为未签订状态，契约常驻效果与冷却
一并清除。

上位契约文本沿用全包既有语法：秘仪物品使用 `[秘仪]` / `[源质]`，契约书使用
`[契约]` / `[已立约]`；Lore 以 `🜏` 分层，正文保持灰色，仅关键名词使用圣金、
秘仪紫或权柄青。技能提示、权柄状态与五格冷却条都由唯一的 Actionbar 出口合成，
玩家面板也会在新约生效时把“契约与侵蚀”切换为“契约与权柄”。

## 重建

```bash
bash _tools/rp_build.sh       # 材质包
bash _tools/build.sh          # 数据包（最后跑，收回材质生成器写入的数据侧文件）
bash _tools/guide_build.sh    # 图鉴
python _tools/package.py --install
```

两个包都是**从 `_orig/` `_orig_rp/` 的原始 1.21 副本重新生成的**，不是手工改的。
请保持“材质包 → 数据包”的顺序：若干共用生成器在制作材质时也会写数据侧入口，
最后的数据包构建会统一重新现代化、收编 HUD 并执行多人校验。任何修改都应该改
`_tools/` 里对应的生成脚本，而不是改输出。

`rp_build.sh`、`guide_build.sh` 和无头测试需要本地 1.21.11 实例（客户端 jar、库与 Java 21）。
位置统一由 `_tools/mc_env.py` 解析：按顺序找第一个存在的候选实例（作者的 HMCL 实例、PCL 实例），
也可用环境变量 `RPG_MC_GAME` / `RPG_MC_VERSION` / `RPG_MC_JAVA` 指向别处；`python _tools/mc_env.py`
会打印当前解析结果。`build.sh` 不依赖 jar，缺 jar 时只会跳过进度字段比对。

玛门弓与驱魔图腾的贴图由 `import_art.py` 从作者本机的原画目录裁出；没有原画目录的机器会改用
仓库里 `_art_crops/` 中上一次裁好的结果，因此任何机器上的完整重建都不会把它们降级成占位图。

验证手段：`_tools/server_test.py` 会用客户端 jar 起一个真实的 1.21.11 无头服务器加载数据包，
`validate.py` / `rp_validate.py` 对着同一个 jar 校验两个包。

## 作者与致谢

| | |
|---|---|
| **仓库作者** | 原始 RPG 内容、全部美术、世界观设定与整体方向 |
| **ChatGPT**（OpenAI） | 《破碎大陆》世界观叙事文案 —— [`LORE.md`](LORE.md) 的圣经体行文 |
| **Claude**（Anthropic） | 1.21.11 迁移、性能重构、图鉴生成，以及路西法、利维坦、圣殿双柱等新增内容的实现与验证 |
| **Codex**（OpenAI） | 美术/UI 规整、文档与发布验证 |

**字体**：Actionbar 上层的恶魔招式提示与封印状态位图，由 Minecraft 客户端自带的
[GNU Unifont](https://unifoundry.com/unifont/) 字形烘焙而成（GPLv2+ 附字体嵌入例外 / SIL OFL 1.1 双许可）。
全包的配色与文字规范见 [`ART-STYLE.md`](ART-STYLE.md)。

世界观由作者设定、ChatGPT 落笔成文，再由 Claude 整合进图鉴与数据包；
每一处实现判断、踩过的坑与修正都记在 [`ENGINEERING.md`](ENGINEERING.md) 里。

感谢这段三方的合作。

### 素材来源

圣卫（塔卫）、别西卜（无名者）、利维坦（死灵法师）、亚巴顿（悲惨幽魂）与三位领主麾下罪仆（先锋、沉没骷髅、塔中幽魂）的原始贴图与音效取自
**Minecraft Dungeons**（Mojang Studios），经由 [minecraft.wiki](https://minecraft.wiki) 获取，
版权归 Mojang 所有。本项目开源、免费、非商业，与 Mojang 及 Microsoft 无任何关联。

| 生物 | 原型 | 来源页面 | 用到的素材 |
|---|---|---|---|
| 圣卫 | Tower Guard | <https://minecraft.wiki/w/Dungeons:Tower_Guard> | 本体、盾牌、长戟贴图及其发光层；全部 13 组共 56 段音效 |
| 别西卜 | Nameless One | <https://minecraft.wiki/w/Dungeons:Nameless_One> | 本体贴图与发光层；全部 16 组共 40 段音效 |
| 别西卜麾下罪仆 | Vanguard | <https://minecraft.wiki/w/Dungeons:Vanguard>（另有 [Skeleton](https://minecraft.wiki/w/Dungeons:Skeleton)、[Glaive](https://minecraft.wiki/w/Dungeons:Glaive) 页） | 骷髅本体、沙漠盔甲、沙漠盾牌、长戟贴图；先锋全部 6 组共 18 段音效 |
| 利维坦 | Necromancer | <https://minecraft.wiki/w/Dungeons:Necromancer> | 本体贴图与发光层；Sounds 一节全部 28 段音效 |
| 利维坦麾下罪仆 | Sunken Skeleton | <https://minecraft.wiki/w/Dungeons:Sunken_Skeleton> | Tier 1～3 贴图（模型用 Tier 1）；全部 8 组共 27 段音效 |
| 亚巴顿 | Wretched Wraith | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | 本体贴图与发光层（渲染图、正面图用于核对）；15 组共 38 段音效；动画用塔中幽魂的 |
| 亚巴顿麾下罪仆 | Tower Wraith | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | 本体贴图与发光层（绿色变体存档）；全部 13 组共 45 段音效；动画参照页面动图重做 |

逐个文件的来源记在 [`_tools/tower_guard_ref/SOURCES.md`](_tools/tower_guard_ref/SOURCES.md) 与
[`_tools/beelzebub_ref/SOURCES.md`](_tools/beelzebub_ref/SOURCES.md)、
[`_tools/vanguard_ref/SOURCES.md`](_tools/vanguard_ref/SOURCES.md)、
[`_tools/leviathan_ref/SOURCES.md`](_tools/leviathan_ref/SOURCES.md)、
[`_tools/sunken_skeleton_ref/SOURCES.md`](_tools/sunken_skeleton_ref/SOURCES.md)、
[`_tools/abaddon_ref/SOURCES.md`](_tools/abaddon_ref/SOURCES.md)、
[`_tools/tower_wraith_ref/SOURCES.md`](_tools/tower_wraith_ref/SOURCES.md)。模型几何、姿势与动画是在
Blockbench 里按原作外观重做的；图集里原贴图之外的部分（皇冠、法袍、护肩、法杖头的嵌套方块等）
用原贴图的像素与配色补画。
