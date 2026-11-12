你要在一个已有的 Minecraft Java 1.21.11 数据包+资源包项目里，把《Minecraft Dungeons》的 Abomination Vine（Jungle Abomination 召出的藤蔓）从本体提取出来，做成展示实体模型和动作。它用在路西法二阶段「知善恶树」的招式里。全程用中文回复。

这次是小件，沿用你做二阶段 Jungle Abomination 时的整套提取和转换流程，下面写明的直接照做，不用再调研或确认。只在第 5 节的检查点停下来等用户。

## 1. 已有的东西

- 仓库：`D:\agent\claude\github-create\tralancer-rpg-1.21.11`
- 提取工具和原始导出：`D:\agent\dungeons_extract\`（`exporter\`、`INVENTORY.md`）
- 转换脚本：`_tools/convert_dungeons.py`、`_tools/dungeons_conversion/`
- 二阶段成品：`_tools/lucifer_p2_ref/`、`_tools/add_lucifer_p2_model.py`
- 战斗逻辑：`_tools/add_lucifer_fight.py`（我写的）。它现在用原版扭曲藤蔓方块顶替藤蔓，你交付后由我替换
- 设计文档：`docs/LUCIFER-P2-DESIGN.md`

`INVENTORY.md` 已经列出藤蔓相关的资产，但还没有导出：

- `Dungeons/Content/Actors/Characters/Enemies/JungleAbominationVine/SK_Abomination_Vine`
- `Dungeons/Content/Actors/Characters/Enemies/JungleAbominationVine/M_AbominationVine`
- `.../Animations/AbominationVine`
- `.../Animations/AbominationVine_Burst`
- `.../Animations/AbominationVine_Idle`
- `.../Animations/AbominationVine_Death`

## 2. 交付内容

| 路径 | 内容 |
| --- | --- |
| `_tools/lucifer_vine_ref/lucifer_vine.bbmodel` | 模型和全部动作，事实来源 |
| `_tools/lucifer_vine_ref/` | 贴图、`SOURCES.md`、`REPORT.md`、对照图 |
| `_tools/add_lucifer_vine_model.py` | 生成器 |

构建接入：在 `_tools/build.sh` 和 `_tools/rp_build.sh` 里，挂在 `add_lucifer_p2_model.py` 的下一行。

固定配置：

| 项 | 值 |
| --- | --- |
| key | `lucifer_vine` |
| tag | `rpg.luv` |
| 缩放 | 和二阶段**同一个**系数 `0.0086339026833541152 blocks/cm`，这样藤蔓和树的比例与原作一致 |

## 3. 运行时接口

战斗逻辑只调用下面三个函数，其余由你决定：

| 函数 | 执行者与位置 | 作用 |
| --- | --- | --- |
| `rpg:lucifer_vine/spawn` | 任意执行者，位置是藤蔓根部 | 原地召出一根藤蔓，立刻播 `burst`，播完自动转 `idle` 循环。新藤蔓带 tag `rpg.luv.new`，召出后由我给它记上领主编号 |
| `rpg:lucifer_vine/retract` | 执行者是这根藤蔓的根实体 | 播 `death`，播完清掉这根藤蔓的全部部件 |
| `rpg:lucifer_vine/clear` | 执行者是根实体 | 立刻清掉，不播动画（领主消失时用） |

其他要求：

- **根实体：** 不可被攻击、不受重力，例如 marker 或 armor_stand marker。部件骑在它上面。
- **兜底：** 根实体自带寿命分数，默认 200 刻。我忘记调用 `retract` 时它也会自己收掉，不留残余。
- **朝向：** 每根随机偏转一个 yaw，避免一排藤蔓看起来一模一样。
- **出土时刻：** 报告里写明 `burst` 第几刻藤蔓尖端出土，伤害判定要对准这一刻。

## 4. 预算

同屏最多同时存在 16 根藤蔓，所以：

- **部件数：** 每根不超过 4 个部件，即全场不超过 64 个 item_display。超了就合并运动幅度最小的骨骼，在报告里列出合并了哪些。
- **动画写法：** 用一次 `data merge` 设目标再交给客户端插值，不要逐刻改实体。`data ... entity` 会序列化整个实体。
- **选择器：** 不用 `nbt=` 选择器。

## 5. 检查点

只有一个检查点：全部做完、接进构建后停下来，交出以下内容：

- 四视角对照图：原网格与转换结果并排，同一相机
- 四段动作的时长表，以及 `burst` 出土那一刻
- 数值误差：每段动作在烘焙的每一刻，最大的顶点误差
- 部件表
- 调试命令：在脚下召出一根，等它出土、待机，再调用 `retract`

## 6. 验证

- **构建：** `_tools/build.sh`、`_tools/rp_build.sh` 无报错，`_tools/rp_validate.py` 无问题
- **服务器：** `_tools/server_test.py` 无函数加载错误
- **残留：** 调用 `retract`、`clear`，以及等寿命到期之后，都没有残留的展示实体
- **实机：** 能进游戏就截图；进不了就明确写「未在真实游戏内看过」

## 7. 不要做的事

- **游戏本体：** 只读，不改、不移动。
- **别人的文件：** 不改 `add_lucifer_fight.py`、`add_lucifer_p2_model.py`、`display_mob.py`，也不改二阶段的模型和动作。
- **git：** 没有用户明确要求，不提交、不推送、不切分支。
- **共用工作区：** 只碰自己的路径，不回滚、不格式化别人的改动。

## 8. 汇报

如实写明没做的、没验证的、推断的。从本体提取的叫「提取」，自己补的叫「补做」。
