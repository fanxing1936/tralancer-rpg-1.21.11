# TRALANCER RPG 调试指令手册

> 共 116 个公开、可手动执行的调试／管理入口。适配 Minecraft Java 1.21.11。

所有命令默认需要开启作弊或拥有管理员权限。带 `@s` 的入口必须由目标玩家自己执行；命令方块或服务器控制台不会自动获得玩家上下文。

本手册只收录设计为人工调用的稳定入口。`*_worker`、每刻 tick、伤害结算、UI 刷新和阶段内部函数不是公共接口，手动执行可能制造半成品状态，因此不列入清单。

## 初始化

首次装包与测试世界基础设施

| 指令 | 用途 | 前置、影响与风险 |
|---|---|---|
| `/function rpg:command/soreboard` | 手动补建／修复全部计分项。 | 正常由 #minecraft:load 自动执行；仅在初始化异常或独立函数测试时手动调用。 影响：全存档；标记：恢复入口。 |
| `/function rpg:command/bossbar` | 手动补建四槽恶魔 Boss 血条。 | 正常由 #minecraft:load 自动执行；重复执行会出现已存在提示。 影响：全存档；标记：恢复入口。 |

## 测试物品发放

优先用潜影盒；@a 群体发放项已单独标注

| 指令 | 用途 | 前置、影响与风险 |
|---|---|---|
| `/function rpg:command/give/box` | 发放按类型整理的全套测试潜影盒。 | 会发给所有在线玩家（@a）；盒内覆盖当前全部自定义物品，包括世界材料、图纸、罪印碎片、圣徽罪印与传承书。 影响：全体背包；标记：群体发放。 |
| `/function rpg:command/give/weapon` | 发放全部武器、护甲与药剂。 | 会发给所有在线玩家（@a），多人服慎用。 影响：全体背包；标记：群体发放。 |
| `/function rpg:command/give/item` | 发放属性晶石，以及装备养成的材料、符文与符石。 | 会发给所有在线玩家（@a），多人服慎用。 影响：全体背包；标记：群体发放。 |
| `/function rpg:command/give/weapon_up_item` | 发放六源（信念、希望、不屈、邪念、仇恨、傲慢）。 | 会发给所有在线玩家（@a），多人服慎用。 影响：全体背包；标记：群体发放。 |
| `/function rpg:command/give/extra` | 发放额外／导入内容测试物品。 | 会发给所有在线玩家（@a），可能占用较多背包格。 影响：全体背包；标记：群体发放。 |
| `/function rpg:command/give/michael` | 只发放米迦勒脊骨与米迦勒肋骨（[神圣] 双持圣骸）。 | 必须由玩家执行；主手一把、副手一把即触发［骨中之骨］。 影响：自身背包；标记：常规。 |
| `/function rpg:command/give/armor` | 只发放全部护甲（八套，含四套新护甲与神圣套补全）。 | 必须由玩家执行；穿齐同一套四件即触发套装加成。 影响：自身背包；标记：常规。 |
| `/function rpg:command/give/dungeons` | 只发放坟墓克星与竖琴弩（Minecraft Dungeons 原作武器）。 | 必须由玩家执行。 影响：自身背包；标记：常规。 |
| `/function rpg:command/give/forge` | 只发放装备养成的全部材料、六源、符文与符石各一件。 | 必须由玩家执行；副手拿装备、主手拿材料右键，器胚对准灵魂营火右键。 影响：自身背包；标记：常规。 |
| `/function rpg:inquest/give/all_tools` | 发放七罪媒介、仪式工具、三类粉笔和真名残页。 | 必须由玩家执行；用于驱魔流程联调。 影响：自身背包；标记：常规。 |
| `/function rpg:ritual/life_tree/give/all` | 发放卡巴拉血契、十源质与真·十字架。 | 必须由玩家执行；仅测试／管理入口。 影响：自身背包；标记：常规。 |

## 状态重置与清场

这些命令会移除个人进度、法阵或展示实体

| 指令 | 用途 | 前置、影响与风险 |
|---|---|---|
| `/function rpg:inquest/reset_self` | 重置执行者七柱真名、见证与案件进度。 | 必须由目标玩家自己执行；不会重置其他玩家。 影响：个人档案；标记：会丢进度。 |
| `/function rpg:inquest/debug/reset_career` | 重置执行者驱魔阅历、等级、路线和阶段奖励领取记录。 | 必须由目标玩家自己执行。 影响：个人档案；标记：会丢进度。 |
| `/function rpg:ritual/life_tree/clear` | 清除执行位置 12 格内的生命之树与展示物。 | 站在需要清理的法阵附近执行。 影响：附近实体；标记：清理。 |
| `/function rpg:ritual/life_tree/clear_all` | 清除当前维度所有生命之树与展示物。 | 不区分玩家和法阵；仅用于测试服收尾。 影响：整维度；标记：全局清理。 |

## Boss、试炼与军团

均在执行位置或附近生成实体／方块

| 指令 | 用途 | 前置、影响与风险 |
|---|---|---|
| `/function rpg:command/setblock` | 在脚下布置试炼刷怪笼与宝库。 | 站在测试点执行；会替换脚下及上方方块。 影响：附近方块；标记：会改地形。 |
| `/function rpg:command/summon` | 在脚下生成通用 1000 生命恶魔 Boss 与护卫。 | 预先初始化计分板和 Bossbar；两只生物未声明永久，远离后可能自然消失。 影响：战斗实体；标记：生成战斗。 |
| `/function rpg:command/summon_devil` | 连续召唤七罪领主，再调用一次契约柱位分派入口。 | 仅做全阵容压力测试；会生成 8 位十分钟 Boss。第 8 位受 #lord 分数影响，需先执行 /scoreboard players set #lord rpg_fall 0 才能固定为无名者。 影响：8 位临时 Boss；标记：高压生成。 |
| `/function rpg:taint/lord` | 按全局 #lord 分数召唤对应领主；0 或非 1–7 时召唤无名者。 | 这是契约柱位分派入口；需要固定无名者时先执行 /scoreboard players set #lord rpg_fall 0。 影响：1 位临时 Boss；标记：生成战斗。 |
| `/function rpg:taint/lord1` | 在执行位置召唤七罪领主：路西法（700 生命）。 | 预先初始化计分板和 Bossbar；不会自动建立驱魔法阵，十分钟后会自行消散。 影响：临时 Boss；标记：生成战斗。 |
| `/function rpg:taint/lord2` | 在执行位置召唤七罪领主：利维坦（700 生命）。 | 预先初始化计分板和 Bossbar；不会自动建立驱魔法阵，十分钟后会自行消散。 影响：临时 Boss；标记：生成战斗。 |
| `/function rpg:taint/lord3` | 在执行位置召唤七罪领主：亚巴顿（700 生命）。 | 预先初始化计分板和 Bossbar；不会自动建立驱魔法阵，十分钟后会自行消散。 影响：临时 Boss；标记：生成战斗。 |
| `/function rpg:taint/lord4` | 在执行位置召唤七罪领主：别西卜（700 生命）。 | 预先初始化计分板和 Bossbar；不会自动建立驱魔法阵，十分钟后会自行消散。 影响：临时 Boss；标记：生成战斗。 |
| `/function rpg:taint/lord5` | 在执行位置召唤七罪领主：萨麦尔（700 生命）。 | 预先初始化计分板和 Bossbar；不会自动建立驱魔法阵，十分钟后会自行消散。 影响：临时 Boss；标记：生成战斗。 |
| `/function rpg:taint/lord6` | 在执行位置召唤七罪领主：贝利尔（700 生命）。 | 预先初始化计分板和 Bossbar；不会自动建立驱魔法阵，十分钟后会自行消散。 影响：临时 Boss；标记：生成战斗。 |
| `/function rpg:taint/lord7` | 在执行位置召唤七罪领主：玛门（700 生命）。 | 预先初始化计分板和 Bossbar；不会自动建立驱魔法阵，十分钟后会自行消散。 影响：临时 Boss；标记：生成战斗。 |
| `/function rpg:pope_fight/summon` | 在执行位置开始教皇战：圣卫战 → 教皇 → 末影之心。 | 同一时间只允许一场；战场半径 40 格，没人满 60 秒判负清场。 影响：教皇战；标记：生成战斗。 |
| `/function rpg:pope_fight/debug/boss1` | 跳过圣卫战，直接从 Boss 一阶段开始。 | 同一时间只允许一场。 影响：教皇战；标记：生成战斗。 |
| `/function rpg:pope_fight/debug/boss2` | 直接进入 Boss 二阶段（末影之心）。 | 同一时间只允许一场。 影响：教皇战；标记：生成战斗。 |
| `/function rpg:pact/debug/materials` | 给执行者七柱祭品和五职材料。 | 逐项给予，背包满时掉在地上。 影响：七十二柱契约；标记：常规。 |
| `/function rpg:pact/debug/bond` | 把执行者的契合度加满。 | 需要已立约。 影响：七十二柱契约；标记：常规。 |
| `/function rpg:pact/debug/up` | 让执行者直接升一阶。 | 需要已立约，第三阶时无效。 影响：七十二柱契约；标记：常规。 |
| `/function rpg:pact/debug/lords` | 把七位领主记为已被执行者击败。 | 只影响真名阶的条件。 影响：七十二柱契约；标记：常规。 |
| `/function rpg:pope_fight/clear` | 清除教皇战的全部实体。 | 战斗卡住或测试收尾时使用。 影响：教皇战；标记：清理。 |
| `/function rpg:lucifer_boss/summon` | 在执行位置开始最终 Boss 路西法：晨星之蛇 → 知善恶树（古龙待做）。 | 同一时间只允许一场；战场半径 40 格，没人满 60 秒判负清场。与七罪领主路西法是两个 Boss。 影响：最终 Boss；标记：生成战斗。 |
| `/function rpg:lucifer_boss/debug/stage2` | 召唤后直接打到一阶段底线，走变身演出进入知善恶树。 | 同一时间只允许一场。 影响：最终 Boss；标记：生成战斗。 |
| `/function rpg:lucifer_boss/clear` | 清除最终 Boss 路西法的全部实体。 | 战斗卡住或测试收尾时使用。 影响：最终 Boss；标记：清理。 |
| `/function rpg:usurper_boss/summon` | 在执行位置开始篡夺者（达里奥·所罗门）战：所罗门之裔 → 篡夺圣灵。 | 同一时间只允许一场；战场半径 40 格。 影响：篡夺者；标记：生成战斗。 |
| `/function rpg:usurper_boss/debug/stage2` | 召唤后直接打到一阶段底线，走变身进入二阶段。 | 同一时间只允许一场。 影响：篡夺者；标记：生成战斗。 |
| `/function rpg:usurper_boss/clear` | 清除篡夺者战的全部实体。 | 战斗卡住或测试收尾时使用。 影响：篡夺者；标记：清理。 |
| `/function rpg:jacques_boss/summon` | 在执行位置开始圣殿大团长雅克战：圣殿之誓 → 火刑柱。 | 同一时间只允许一场；战场半径 40 格。 影响：雅克；标记：生成战斗。 |
| `/function rpg:jacques_boss/debug/stage2` | 召唤后直接打到一阶段底线，走火刑柱变身进入二阶段。 | 同一时间只允许一场。 影响：雅克；标记：生成战斗。 |
| `/function rpg:jacques_boss/clear` | 清除雅克战的全部实体（含大卫的幽灵与召来的圣卫）。 | 战斗卡住或测试收尾时使用。 影响：雅克；标记：清理。 |
| `/function rpg:jacques_ally/give` | 给自己一件圣殿誓约（右键召友军雅克 20 秒，冷却 3 分钟）。 | 必须由玩家执行；正常由击败雅克发放。 影响：雅克；标记：发放。 |
| `/function rpg:jacques_ally/debug/summon` | 在身前召一个友军雅克，不走冷却。 | 必须由玩家执行。 影响：雅克；标记：生成单位。 |
| `/function rpg:jacques_ally/debug/reset_cd` | 清掉自己的圣殿誓约冷却。 | 必须由玩家执行。 影响：雅克；标记：常规。 |
| `/function rpg:jacques_ally/clear` | 清掉所有友军雅克。 | 测试收尾时使用。 影响：雅克；标记：清理。 |
| `/function rpg:merchant/place/smith` | 在脚下放一位铁匠，面朝执行者看的方向。 | 持久存在，直到用 remove 移走。 影响：商人；标记：生成单位。 |
| `/function rpg:merchant/place/mystery` | 在脚下放一位神秘商人（每天换一次货），面朝执行者看的方向。 | 持久存在，直到用 remove 移走。 影响：商人；标记：生成单位。 |
| `/function rpg:merchant/place/luxury` | 在脚下放一位奢侈品商人，面朝执行者看的方向。 | 持久存在，直到用 remove 移走。 影响：商人；标记：生成单位。 |
| `/function rpg:merchant/place/travel` | 在脚下放一位迷途商人（不会自己离开），面朝执行者看的方向。 | 持久存在，直到用 remove 移走。 影响：商人；标记：生成单位。 |
| `/function rpg:merchant/remove` | 移走身边 4 格内最近的一位商人。 | 连同模型与名牌。 影响：商人；标记：清理。 |
| `/function rpg:merchant/admin/travel` | 立刻开始「迷途商人」事件。 | 会先结束正在进行的事件。 影响：世界事件；标记：常规。 |
| `/function rpg:events/admin/start_1` | 立刻开始「罪潮之夜」事件。 | 必须由玩家执行；会先结束正在进行的事件。 影响：世界事件；标记：常规。 |
| `/function rpg:events/admin/start_2` | 立刻开始「坠星」事件。 | 必须由玩家执行；会先结束正在进行的事件。 影响：世界事件；标记：常规。 |
| `/function rpg:events/admin/start_3` | 立刻开始「罪仆巡逻」事件。 | 必须由玩家执行；会先结束正在进行的事件。 影响：世界事件；标记：常规。 |
| `/function rpg:events/admin/start_4` | 立刻开始「寻宝者」事件。 | 必须由玩家执行；会先结束正在进行的事件。 影响：世界事件；标记：常规。 |
| `/function rpg:events/admin/start_5` | 立刻开始「空缺者显现」事件。 | 必须由玩家执行；会先结束正在进行的事件。 影响：世界事件；标记：常规。 |
| `/function rpg:events/admin/end` | 结束正在进行的事件。 | 没有事件时无效。 影响：世界事件；标记：清理。 |
| `/function rpg:saul_boss/summon` | 在执行位置开始疯人王扫罗战：十字军大元帅 → 甲碎 → 疯人王。 | 同一时间只允许一场；战场半径 40 格。 影响：扫罗；标记：生成战斗。 |
| `/function rpg:saul_boss/debug/stage2` | 召唤后直接打到一阶段底线，走甲碎演出进入二阶段。 | 同一时间只允许一场。 影响：扫罗；标记：生成战斗。 |
| `/function rpg:saul_boss/clear` | 清除扫罗战的全部实体（含碎甲、蛛网与老战友的幻影）。 | 战斗卡住或测试收尾时使用。 影响：扫罗；标记：清理。 |
| `/function rpg:daath_fight/summon` | 立刻进达阿特试炼（不看阶位与冷却）；已经在里面就退出来。 | 必须由玩家执行；单人场地，最多同时十六场。 影响：达阿特；标记：生成战斗。 |
| `/function rpg:daath_fight/debug/stage2` | 让自己的影子直接到一段底线，走面具演出进二段。 | 在场地里执行。 影响：达阿特；标记：生成战斗。 |
| `/function rpg:daath_fight/debug/despair` | 让自己的影子直接进绝境。 | 在场地里执行。 影响：达阿特；标记：生成战斗。 |
| `/function rpg:daath_fight/debug/skill/steal` | 影子立刻夺械；skill/ 下还有 chain、shoot、guard、step、grab 等各招。 | 在场地里执行。 影响：达阿特；标记：生成战斗。 |
| `/function rpg:daath_fight/debug/ult/ask` | 影子立刻放「问」；ult/ 下还有 reflect、ten、clash、shatter。 | 在场地里执行。 影响：达阿特；标记：生成战斗。 |
| `/function rpg:daath_fight/clear` | 离开达阿特：归还被夺走的东西、送回来处、清场。 | 必须由玩家执行。 影响：达阿特；标记：清理。 |
| `/function rpg:michael_boss/summon` | 在执行位置开始天使长米迦勒战：天使长·谁似神 → 骨中之骨 → 炽天使。 | 同一时间只允许一场；战场半径 40 格。 影响：米迦勒；标记：生成战斗。 |
| `/function rpg:michael_boss/debug/stage2` | 召唤后直接打到一阶段底线，走骨中之骨演出进入二阶段。 | 同一时间只允许一场。 影响：米迦勒；标记：生成战斗。 |
| `/function rpg:michael_boss/clear` | 清除米迦勒战的全部实体（含守望者、骨柱与注视的眼睛）。 | 战斗卡住或测试收尾时使用。 影响：米迦勒；标记：清理。 |
| `/function rpg:michael/debug/preview` | 在脚下放一个不动的米迦勒外观（不是战斗）；preview_watchling 放守望者。 | 清掉用 /function rpg:michael/debug/clear。 影响：米迦勒；标记：常规。 |

## 七柱罪仆

每柱包含一条五职整队命令与五条单体命令

| 指令 | 用途 | 前置、影响与风险 |
|---|---|---|
| `/function rpg:minion/summon/lucifer/all` | 一次召唤路西法麾下五职罪仆。 | 不检查 Boss、二阶段条件与人口上限；用于编队联调。 影响：持久实体；标记：生成五名。 |
| `/function rpg:minion/summon/lucifer/bael` | 单独召唤路西法麾下先锋「巴力」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/lucifer/agares` | 单独召唤路西法麾下猎手「阿加雷斯」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/lucifer/vassago` | 单独召唤路西法麾下司祭「瓦沙克」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/lucifer/samigina` | 单独召唤路西法麾下咒使「萨米基纳」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/lucifer/marbas` | 单独召唤路西法麾下处刑者「马尔巴士」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/leviathan/all` | 一次召唤利维坦麾下五职罪仆。 | 不检查 Boss、二阶段条件与人口上限；用于编队联调。 影响：持久实体；标记：生成五名。 |
| `/function rpg:minion/summon/leviathan/valefor` | 单独召唤利维坦麾下先锋「华利弗」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/leviathan/amon` | 单独召唤利维坦麾下猎手「亚蒙」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/leviathan/barbatos` | 单独召唤利维坦麾下司祭「巴巴托斯」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/leviathan/paimon` | 单独召唤利维坦麾下咒使「派蒙」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/leviathan/buer` | 单独召唤利维坦麾下处刑者「布耶尔」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/abaddon/all` | 一次召唤亚巴顿麾下五职罪仆。 | 不检查 Boss、二阶段条件与人口上限；用于编队联调。 影响：持久实体；标记：生成五名。 |
| `/function rpg:minion/summon/abaddon/gusion` | 单独召唤亚巴顿麾下先锋「古辛」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/abaddon/sitri` | 单独召唤亚巴顿麾下猎手「西迪」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/abaddon/beleth` | 单独召唤亚巴顿麾下司祭「贝雷特」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/abaddon/leraje` | 单独召唤亚巴顿麾下咒使「列拉金」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/abaddon/eligos` | 单独召唤亚巴顿麾下处刑者「艾利欧格」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/beelzebub/all` | 一次召唤别西卜麾下五职罪仆。 | 不检查 Boss、二阶段条件与人口上限；用于编队联调。 影响：持久实体；标记：生成五名。 |
| `/function rpg:minion/summon/beelzebub/zepar` | 单独召唤别西卜麾下先锋「桀派」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/beelzebub/botis` | 单独召唤别西卜麾下猎手「布提斯」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/beelzebub/bathin` | 单独召唤别西卜麾下司祭「巴钦」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/beelzebub/sallos` | 单独召唤别西卜麾下咒使「塞列欧斯」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/beelzebub/purson` | 单独召唤别西卜麾下处刑者「布松」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/samael/all` | 一次召唤萨麦尔麾下五职罪仆。 | 不检查 Boss、二阶段条件与人口上限；用于编队联调。 影响：持久实体；标记：生成五名。 |
| `/function rpg:minion/summon/samael/marax` | 单独召唤萨麦尔麾下先锋「莫拉格斯」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/samael/ipos` | 单独召唤萨麦尔麾下猎手「因波斯」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/samael/aim` | 单独召唤萨麦尔麾下司祭「艾姆」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/samael/naberius` | 单独召唤萨麦尔麾下咒使「纳贝流士」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/samael/glasya_labolas` | 单独召唤萨麦尔麾下处刑者「格拉夏·拉波拉斯」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/belial/all` | 一次召唤贝利尔麾下五职罪仆。 | 不检查 Boss、二阶段条件与人口上限；用于编队联调。 影响：持久实体；标记：生成五名。 |
| `/function rpg:minion/summon/belial/bune` | 单独召唤贝利尔麾下先锋「布涅」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/belial/ronove` | 单独召唤贝利尔麾下猎手「罗诺比」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/belial/berith` | 单独召唤贝利尔麾下司祭「比利士」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/belial/astaroth` | 单独召唤贝利尔麾下咒使「亚斯塔禄」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/belial/forneus` | 单独召唤贝利尔麾下处刑者「佛纽司」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/mammon/all` | 一次召唤玛门麾下五职罪仆。 | 不检查 Boss、二阶段条件与人口上限；用于编队联调。 影响：持久实体；标记：生成五名。 |
| `/function rpg:minion/summon/mammon/foras` | 单独召唤玛门麾下先锋「佛拉斯」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/mammon/asmoday` | 单独召唤玛门麾下猎手「阿斯摩太」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/mammon/gaap` | 单独召唤玛门麾下司祭「盖布」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/mammon/furfur` | 单独召唤玛门麾下咒使「佛尔佛尔」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
| `/function rpg:minion/summon/mammon/marchosias` | 单独召唤玛门麾下处刑者「马可西亚斯」。 | 在执行位置生成；可脱离 Boss 独立、永久存活。 影响：持久实体；标记：生成单体。 |
