# TRALANCER RPG 调试指令手册

> 共 89 个公开、可手动执行的调试／管理入口。适配 Minecraft Java 1.21.11。

所有命令默认需要开启作弊或拥有管理员权限。带 `@s` 的入口必须由目标玩家自己执行；命令方块或服务器控制台不会自动获得玩家上下文。

本手册只收录设计为人工调用的稳定入口。`*_worker`、每刻 tick、伤害结算、UI 刷新和阶段内部函数不是公共接口，手动执行可能制造半成品状态，因此不列入清单。

## 初始化

首次装包与测试世界基础设施

| 指令 | 用途 | 前置、影响与风险 |
|---|---|---|
| `/function rpg:command/soreboard` | 手动补建／修复全部计分项。 | 正常由 #minecraft:load 自动执行；仅在初始化异常或独立函数测试时手动调用。 影响：全存档；标记：恢复入口。 |
| `/function rpg:command/bossbar` | 手动补建四槽恶魔 Boss 血条。 | 正常由 #minecraft:load 自动执行；重复执行会出现已存在提示。 影响：全存档；标记：恢复入口。 |
| `/team add green` | 创建风袭掠夺者使用的 green 队伍。 | 管理员；召唤风袭小队前至少执行一次。 影响：全存档；标记：初始化。 |

## 测试物品发放

优先用潜影盒；@a 群体发放项已单独标注

| 指令 | 用途 | 前置、影响与风险 |
|---|---|---|
| `/function rpg:command/give/box` | 发放按类型整理的全套测试潜影盒。 | 会发给所有在线玩家（@a）；盒内覆盖当前全部自定义物品。 影响：全体背包；标记：群体发放。 |
| `/function rpg:command/give/weapon` | 发放全部武器、护甲与药剂。 | 会发给所有在线玩家（@a），多人服慎用。 影响：全体背包；标记：群体发放。 |
| `/function rpg:command/give/item` | 发放符文、符石、晶石与锻造材料。 | 会发给所有在线玩家（@a），多人服慎用。 影响：全体背包；标记：群体发放。 |
| `/function rpg:command/give/weapon_up_item` | 发放全部武器分支唱片。 | 会发给所有在线玩家（@a），多人服慎用。 影响：全体背包；标记：群体发放。 |
| `/function rpg:command/give/extra` | 发放额外／导入内容测试物品。 | 会发给所有在线玩家（@a），可能占用较多背包格。 影响：全体背包；标记：群体发放。 |
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
| `/function rpg:entities/drowned/king` | 召唤溺尸王、骑乘体、巨人与近卫。 | 在预定战场执行；一次生成整支编队。 影响：持久实体；标记：生成军团。 |
| `/function rpg:entities/piglin/king` | 召唤猪灵王、骑乘体、巨人与近卫。 | 在预定战场执行；一次生成整支编队。 影响：持久实体；标记：生成军团。 |
| `/function rpg:entities/illager/wind_vindicator` | 召唤完整风袭掠夺者小队。 | 必须先执行 /team add green；全队未声明永久，远离后可能自然消失。 影响：战斗实体；标记：生成军团。 |

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

## 第一章 · 空缺者

正式入口、调试台、补生与 Stage 0–10 跳转

| 指令 | 用途 | 前置、影响与风险 |
|---|---|---|
| `/function rpg:campaign/beelzebub/start` | 正式接受并创建第一章「空缺者」实例。 | 安全空地、管理员；会写入正常章节状态。 影响：章节存档；标记：正式入口。 |
| `/function rpg:campaign/beelzebub/abort` | 中止并清理附近第一章实例。 | 必须站在目标实例／控制器 72 格内执行；永久调查与首通档案不回滚。 影响：章节实例；标记：清理。 |
| `/function rpg:campaign/beelzebub/debug/menu` | 打开可点击的第一章完整调试台。 | 必须由玩家执行；建议作为第一章调试总入口。 影响：无；标记：推荐。 |
| `/function rpg:campaign/beelzebub/debug/start` | 以当前位置作为候选原点开启章节。 | 安全空地；仍会执行正式地形与朝向校验。 影响：章节存档；标记：创建实例。 |
| `/function rpg:campaign/beelzebub/debug/give_all_items` | 发放配置登记的全部第一章物品。 | 必须由玩家执行；不写完成、奖励或职业进度。 影响：自身背包；标记：常规。 |
| `/function rpg:campaign/beelzebub/debug/spawn_boss` | 按本章配置在实例内补生别西卜。 | 附近必须已有第一章控制器；已有 Boss 时不会重复生成。 影响：章节实体；标记：生成战斗。 |
| `/function rpg:campaign/beelzebub/debug/spawn_all_minions` | 按配置在实例内额外生成五名别西卜罪仆。 | 附近必须已有第一章控制器；不检查现存罪仆，重复执行会每次叠加五名。 影响：章节持久实体；标记：生成五名。 |
| `/function rpg:campaign/beelzebub/debug/list_positions` | 在聊天栏列出全部可配置相对坐标。 | 必须由玩家执行；只读，不改变实例。 影响：无；标记：只读。 |
| `/function rpg:campaign/beelzebub/debug/stage/0` | 跳转到 Stage 0「楔子｜第十三声钟」。 | 附近必须已有第一章控制器；自动清理旧阶段现场。 影响：章节实例；标记：不写首通。 |
| `/function rpg:campaign/beelzebub/debug/stage/1` | 跳转到 Stage 1「发现异常｜取得 3 份相互矛盾的记录」。 | 附近必须已有第一章控制器；自动清理旧阶段现场。 影响：章节实例；标记：不写首通。 |
| `/function rpg:campaign/beelzebub/debug/stage/2` | 跳转到 Stage 2「会回家的死者｜以圣器照见空缺」。 | 附近必须已有第一章控制器；自动清理旧阶段现场。 影响：章节实例；标记：不写首通。 |
| `/function rpg:campaign/beelzebub/debug/stage/3` | 跳转到 Stage 3「五席未满｜第1轮 · 封路与追猎」。 | 附近必须已有第一章控制器；自动清理旧阶段现场。 影响：章节实例；标记：不写首通。 |
| `/function rpg:campaign/beelzebub/debug/stage/4` | 跳转到 Stage 4「确认活动区域｜让三条运输记录彼此指认」。 | 附近必须已有第一章控制器；自动清理旧阶段现场。 影响：章节实例；标记：不写首通。 |
| `/function rpg:campaign/beelzebub/debug/stage/5` | 跳转到 Stage 5「调查真名与弱点｜排除 2 个错误答案」。 | 附近必须已有第一章控制器；自动清理旧阶段现场。 影响：章节实例；标记：不写首通。 |
| `/function rpg:campaign/beelzebub/debug/stage/6` | 跳转到 Stage 6「被撕去的判词｜准备 3 组仪式器具」。 | 附近必须已有第一章控制器；自动清理旧阶段现场。 影响：章节实例；标记：不写首通。 |
| `/function rpg:campaign/beelzebub/debug/stage/7` | 跳转到 Stage 7「万蝇腐宴｜Boss 与四阶段驱魔」。 | 附近必须已有第一章控制器；自动清理旧阶段现场。 影响：章节实例；标记：不写首通。 |
| `/function rpg:campaign/beelzebub/debug/stage/8` | 跳转到 Stage 8「四种不完整的裁决｜见证人印缺失」。 | 附近必须已有第一章控制器；自动清理旧阶段现场。 影响：章节实例；标记：不写首通。 |
| `/function rpg:campaign/beelzebub/debug/stage/9` | 跳转到 Stage 9「活着的人必须有名字｜救下米拉」。 | 附近必须已有第一章控制器；自动清理旧阶段现场。 影响：章节实例；标记：不写首通。 |
| `/function rpg:campaign/beelzebub/debug/stage/10` | 跳转到 Stage 10「边缘者登记｜选择驱魔道路后完成归档」。 | 附近必须已有第一章控制器；自动清理旧阶段现场。 影响：章节实例；标记：不写首通。 |
