# 第一章统一配置与调试规范

第一章《空缺者》的配置源是根目录的 `_campaign_beelzebub_config.json`。它只保存结构化玩法数据，不保存剧情对白。修改配置后应重新运行 `_tools/build.sh`；不要直接编辑 `rpg/` 下的生成结果。

## 配置边界

配置覆盖本章实例内可生成或可领取的对象：

- 15 个物品引用：驱魔图腾、待确证残页、正式真名残页、别西卜媒介、6 件仪式工具、边缘者档案和4种裁决残响。
- 11 个角色/锚点定义：固定 Marker 控制器、空缺者母亲、米拉实体及被捕位置、别西卜和5名所罗门罪仆；`position_only` 条目只表示同一实体的转移落点。
- 33 个相对位置：上述11个实体位置、13个基础调查点，以及路线密文、假说审判、仪式校准各3个交互槽位。
- 队伍、加入阶段、作用距离、场地预检、调查读条、失败恢复、Boss 生命和罪仆多人血量。
- 调试入口名、阶段跳转范围与调试开关。

剧情文本、粒子编排和函数实现仍由生成器维护。这样改坐标/数值不需要在大量命令中查找，而改叙事也不会误伤实体归属协议。

章节身份协议仍是固定约束：控制器必须为 Marker，Boss 仍是别西卜／领主编号4，五名罪仆 `role` 仍为1至5，调试入口仍要求管理员权限。可调的是物品入口与身份、活体实体类型/名称/召唤函数、波次/职责/血量，以及全部本地生成位置；内部 ID 与归属标签不作为玩法参数开放。

## 坐标约定

所有 `spawn` 使用 Minecraft 本地坐标：`^左/右 ^上/下 ^前/后`。章节开始时以发起玩家脚下为原点，朝向吸附到四个正方向：

- `^ ^ ^19`：原点正前方19格。
- `^8 ^ ^18`：正前方18格、局部右侧8格。
- `^-10 ^ ^35`：正前方35格、局部左侧10格。

不要在配置中写 `~` 坐标或绝对坐标。加载器会在构建时拒绝它们，以免不同朝向的实例出现偏移。

`runtime.safe_plane` 的四组采样数组直接决定启动前检查范围，`headroom` 会逐层生成每个采样点的净空检查。扩大任一生成位置时，也要同步扩大采样数组；否则实体可能生成在未预检区域。玩法生成器与章节美术生成器读取同一组坐标，调查标签和地面道具不会各自漂移。

## 常用调整

### 移动 Boss 或罪仆

编辑 `actors.boss.spawn` 或 `actors.minions.<id>.spawn`。五名罪仆的 `wave` 可重新分组，但必须从1开始连续编号；`duty` 会进入每轮 Bossbar，`display_name` 会进入名字与对白。`role` 必须保持1至5，因为既有能力状态机按职责编号路由。

### 调整 Boss 与多人血量

编辑 `actors.boss.health` 或 `actors.minions.<id>.health_by_party`。单人使用罪仆原始召唤函数的默认血量；从2人到 `runtime.max_party_size` 的每个规模都必须有血量值。加入函数会在写成员标签前拒绝超员。别西卜默认700，章节生成后会按配置再次写入最大生命与当前生命，便于临时平衡测试。

### 更换物品或检测组件

每个物品都包含：

- `base_item`：物品本体；
- `match`：`execute unless items` 使用的组件匹配式；
- `give_function`：唯一发放入口；
- `item_model`：仅用于本章自己生成外观的奖励；
- `generated`：为 `true` 时，生成器会在配置指定的 `give_function` 路径写入物品，并让 `match` 中的 `custom_data` 成为实际身份。

器具箱只引用物品键，不重复写函数名。调整 `cache_loadouts` 即可改变三组领取内容。不得把同一物品键放入两个箱，校验器会拒绝重复分发。

### 调整调查节奏

`runtime.observation_ticks` 以20 tick = 1秒计算。异常、追踪、假说、器具箱和谜题选择分别有独立读条时间；`runtime.recap_hold_ticks` 控制每次案情复盘独占屏幕的阅读窗口，当前为200 tick（10秒）。失败恢复窗口在 `runtime.recovery`，其中米拉3分钟救援窗口当前是3600 tick。

`scene_points.route_cipher`、`scene_points.hypothesis_board` 与 `scene_points.ritual_calibration` 是三套新谜题的全部交互位置。调整它们时必须继续位于 `runtime.safe_plane` 的采样范围内；错误答案生成的短战斗也使用同一章节ID回收协议。

## 生成器接入映射

`_tools/add_beelzebub_campaign.py` 应通过 `_tools/beelzebub_campaign_config.py` 的 `load_config()` 加载配置。逐项接入位置如下：

| 配置路径 | 生成器消费者 |
|---|---|
| `runtime.dimension`、半径、队伍上限 | `write_preflight()`、`write_menu_and_membership()`、`write_start_and_controller()` |
| `runtime.safe_plane` | `write_preflight()` 的63+9地面/净空采样 |
| `runtime.observation_ticks`、`runtime.recap_hold_ticks` | `write_point_probe()`、五处阶段复盘门控 |
| `runtime.recovery` | `write_minions()`、`write_boss_and_rite()`、队伍失败恢复 |
| `visual.palette`、Display参数 | 顶部颜色常量、`display()`、全部章节UI |
| `items.investigation`、`items.media`、`items.ritual_tools` | `write_tracking_inquest_prep()`、`write_boss_and_rite()` |
| `items.rewards` | `reward_item()`、`write_completion_cleanup()` |
| `actors.npcs` | `write_stage0_2()`、`write_minions()`、`write_verdict_epilogue()` |
| `actors.boss` | `write_boss_and_rite()`、Boss归属与回收检查 |
| `actors.minions` | `write_minions()` 的召唤、实体类型、波次和多人血量 |
| `scene_points` | `write_stage0_2()`、`write_tracking_inquest_prep()` |
| `cache_loadouts` | `write_tracking_inquest_prep()` 的三组器具箱 |
| `debug` | 独立生成 `campaign/beelzebub/debug/*` |

完成接入后，生成器还应把 `manifest(config)` 写入 `data/rpg/chapter/beelzebub_config.json`。其中的SHA-256用于证明数据包确实由当前配置生成，避免调试时误装旧包。

## 调试入口契约

配置预留以下函数；它们应由主生成器创建，并保持管理员主动执行、默认不进入正常 tick：

- `/function rpg:campaign/beelzebub/debug/menu`：显示所有调试入口。
- `/function rpg:campaign/beelzebub/debug/start`：以当前位置和朝向创建测试实例。
- `/function rpg:campaign/beelzebub/debug/give_all_items`：发放本章全部调查/仪式/奖励物品。
- `/function rpg:campaign/beelzebub/debug/spawn_boss`：只在现有章节控制器内召唤本章 Boss。
- `/function rpg:campaign/beelzebub/debug/spawn_all_minions`：按配置位置召唤五名罪仆。
- `/function rpg:campaign/beelzebub/debug/list_positions`：在聊天栏列出语义位置和本地坐标。
- `/function rpg:campaign/beelzebub/debug/stage/<0..10>`：清理当前阶段临时实体后跳转，不能直接伪造永久奖励。

调试函数不得绕过章节ID/会话ID归属。所有阶段跳转会添加 `rpg.ch1.debug.no_commit`；即使预览 Stage 10 且玩家已有职业路线，也不得授予 `rpg_ch1_done`、`rpg_ch1_reward`、`rpg_ch1_next`、阅历或成就。需要结局回归时，应从正式章节入口正常游玩并结算。

## 校验命令

在 `_tools` 目录运行：

```powershell
python beelzebub_campaign_config.py --pack-root ../rpg
python beelzebub_campaign_config.py --positions
python check_beelzebub_campaign_config.py ../rpg
```

主生成器完成接入后，发布检查使用严格模式：

```powershell
python check_beelzebub_campaign_config.py ../rpg --require-wired
```

严格模式同时检查加载器接入、配置摘要、全部调试函数、阶段跳转和生成资源引用。
