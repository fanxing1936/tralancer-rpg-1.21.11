你要在一个已有的 Minecraft Java 1.21.11 数据包项目里，把原版地狱堡垒的生成复制一套，改成黑石，作为新维度「失乐园」里自然生成的结构。全程用中文回复。下面写明的直接照做。

## 1. 已有的东西

- **仓库：** `D:\agent\claude\github-create\tralancer-rpg-1.21.11`，生成器都在 `_tools/`，用 Python 写，产物在 `rpg/`（数据包）。
- **新维度：** `rpg:paradise_lost`，生物群系也叫 `rpg:paradise_lost`（我正在做，参考 `_tools/prologue_world.py`）。地面是泥巴，高度在 y=80 上下起伏约 8 格，低处有水。
- **原版客户端 jar：** `python -c "import mc_env;print(mc_env.JAR)"`（在 `_tools` 目录运行）。
- **测试：** 用 `_tools/server_test.py`（无头服务端，路径从 `mc_env.py` 取），或自己开一份临时世界。不要动 `D:\minecraft\PCL启动器` 里的存档，用户正在玩。

## 2. 为什么不能直接改原版

原版 `minecraft:fortress` 的砖写死在 Java 里，数据包换不了。所以**逐个部件复制**，再用 `jigsaw` 结构按原版的连接方式拼起来，保证每座都不一样。

## 3. 取部件

1. 在临时世界的平地（下界或超平坦都行）用 `/place structure minecraft:fortress` 放出多座，直到下表每种部件至少有一个朝向是**南**（区块 NBT 里 `O` = 0）的实例。南向不需要旋转或镜像。
2. 部件的边界直接读区块 NBT：`structures.starts["minecraft:fortress"].Children[]` 里每个部件有 `id`、`BB`（六个数）、`O`。
3. 按 `BB` 把方块切出来，写成结构模板（`.nbt`，`DataVersion` 用 1.21.11 的）。空气要保留为空气；不属于这个部件的方块写成 `structure_void`。

| 部件 id | 说明 | 尺寸 x×y×z | 出口（朝前 +z 为 F，左 L，右 R；括号里是出口中心的局部坐标） |
| --- | --- | --- | --- |
| `nebs` | 直桥 | 5×10×19 | F(2,3) |
| `nebcr` | 十字桥 | 19×10×19 | F(9,3)、L(z=9,y=3)、R(z=9,y=3) |
| `nerc` | 十字室 | 7×9×7 | F(3,0)、L(z=3,y=0)、R(z=3,y=0) |
| `nesr` | 楼梯室 | 7×11×7 | R(z=3,y=6) |
| `nemt` | 烈焰台（刷怪笼） | 7×8×9 | 无 |
| `nece` | 城堡入口 | 13×14×13 | F(6,3)，接城堡类 |
| `nesc` | 小走廊 | 5×7×5 | F(2,0) |
| `nescsc` | 小走廊十字 | 5×7×5 | F(2,0)、L(z=2,y=0)、R(z=2,y=0) |
| `nescrt` | 小走廊右转（有宝箱） | 5×7×5 | R(z=2,y=0) |
| `nesclt` | 小走廊左转（有宝箱） | 5×7×5 | L(z=2,y=0) |
| `neccs` | 走廊楼梯（下行） | 5×14×10 | F(2,0) |
| `nectb` | 走廊 T 形阳台 | 9×7×9 | L、R（z 以实际门洞为准，y=0） |
| `necsr` | 地狱疣室 | 13×14×13 | F(6,3)、F(6,11) |
| `nebef` | 桥的尽头 | 5×10×8 | 无 |

入口在 z=0 面：桥类（`nebs`、`nebcr`、`nebef`）中心在局部 y=3；城堡入口、地狱疣室在 (6,3)；`neccs` 在 (2,7)；其余在 y=0、x 取中。上表凭原版源码整理，如果和切出来的实物门洞对不上，**以实物为准**，并在报告里写明。

## 4. 换方块

| 原方块 | 换成 |
| --- | --- |
| `nether_bricks` | `polished_blackstone_bricks` 约 80%、`cracked_polished_blackstone_bricks` 约 15%、`gilded_blackstone` 约 5%（写成结构处理器 `processor_list`，不要烘焙死，这样每座不同） |
| `nether_brick_stairs` | `polished_blackstone_brick_stairs`，方向属性照搬 |
| `nether_brick_fence` | `polished_blackstone_brick_wall`，连接属性改成墙的写法（`none/low/tall` 和 `up`） |
| `nether_brick_slab`（如有） | `polished_blackstone_brick_slab` |
| `soul_sand`、`nether_wart`、`lava` | 保留 |
| 烈焰人刷怪笼 | 保留刷怪笼，`SpawnData` 换成：烈焰人，`max_health` 40、`attack_damage` 9，标签 `rpg.pl` |
| 宝箱 | 保留，`LootTable` 写 `rpg:paradise/fortress_chest` |

原版会从桥底往下砌柱子直到碰到地面。`jigsaw` 不会。做法：直桥、十字桥、城堡入口、桥的尽头这四种，在切出来的模板下面照原版柱脚的位置往下补 16 格黑石砖柱，其余位置填 `structure_void`。

## 5. 拼装

- 每种部件在出口和入口放 `minecraft:jigsaw` 方块，`final_state` 写成那个位置原本的方块。
- 分三个池：`bridge`、`castle`、`end`，权重照原版：
  - 桥：直桥 30、十字桥 10、十字室 10、楼梯室 10（每座最多 3）、烈焰台 5（最多 2）、城堡入口 5（最多 1）；
  - 城堡：小走廊 25、小走廊十字 15、右转 5、左转 10、走廊楼梯 10（最多 3）、T 形阳台 7（最多 2）、地狱疣室 5（最多 2）。
- 「最多几个」在 `jigsaw` 里不能直接写，用合适的池结构（比如把稀有部件放进只在较浅层出现的子池）近似，并在报告里写清实际分布。
- 池子接不下时用 `nebef` 收尾（`fallback`）。
- 起点用十字桥。`max_depth` 和 `max_distance_from_center` 调到一座大约 100 到 200 格宽，和原版差不多。
- 起点高度：桥面比地表高约 8 格。

## 6. 交付

- 生成器 `_tools/add_blackstone_fortress.py`，运行方式 `python add_blackstone_fortress.py ../rpg`，**只依赖仓库里的文件**，不需要游戏在运行。
- 模板源文件 `_tools/fortress_ref/pieces/*.nbt`，抽取脚本放 `_tools/fortress_ref/extract.py`。
- 产物：
  - `rpg/data/rpg/structure/paradise/fortress/*.nbt`
  - `rpg/data/rpg/worldgen/processor_list/paradise/fortress.json`
  - `rpg/data/rpg/worldgen/template_pool/paradise/fortress/*.json`
  - `rpg/data/rpg/worldgen/structure/paradise/fortress.json`（`biomes` 写 `rpg:paradise_lost`）
  - `rpg/data/rpg/worldgen/structure_set/paradise/fortress.json`（`spacing` 26、`separation` 14，盐值 1795411）
- 还要一张掉落表占位 `rpg/data/rpg/loot_table/paradise/fortress_chest.json`，空池即可，内容我来填。
- 报告 `_tools/fortress_ref/REPORT.md`：14 种部件的实际尺寸与门洞、和上表不一样的地方、实际生成 20 座的部件数量统计、4 张截图（整体、桥、城堡内、烈焰台）。

**验收：** 在一个只有这份数据包的临时世界里，用 `/place structure rpg:paradise/fortress` 放 20 座，没有报错；没有残留的 `jigsaw` 方块和 `nether_brick*` 方块；桥面连续，走廊走得通。

不要改 `build.sh`、`add_paradise.py`、别的生成器或资源包，我来接线。不要下载任何外部文件。
