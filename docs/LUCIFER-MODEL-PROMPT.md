你要在一个已有的 Minecraft Java 1.21.11 数据包+资源包项目里，为七罪领主「路西法」做两个阶段的模型和动作。用户本机装了《Minecraft Dungeons》本体，所有模型、贴图和动画都**从本体提取后转换**，不手工建模、不对着图片摆姿势。全程用中文回复。

| 阶段 | 外形 | 动作来源 | 手持 |
| --- | --- | --- | --- |
| 一阶段 | Mossy Skeleton 的身体，穿 Root Rot Armor | Necromancer 的动画，重定向到 Mossy Skeleton 骨架 | 路西法专武「蛇矛」 |
| 二阶段 | Jungle Abomination | 它自己的动画 | 无 |

目标是一次做对。下面写明的东西直接照做，不用再调研或确认；只有第 8 节列出的检查点停下来等用户。

## 1. 仓库、游戏与参考

- 仓库：`D:\agent\claude\github-create\tralancer-rpg-1.21.11`
- 游戏：`D:\XboxGames\Minecraft Dungeons`，pak 在 `Content\Dungeons\Content\Paks\pakchunk*-WindowsNoEditor.pak`。已确认是 UE4 pak v8，索引加密，加密 GUID 全零，即只需要一把 AES 密钥。
- 外观核对用的 wiki 页面：
  - https://minecraft.wiki/w/Dungeons:Mossy_Skeleton
  - https://minecraft.wiki/w/Dungeons:Root_Rot_Armor
  - https://minecraft.wiki/w/Dungeons:Necromancer
  - https://minecraft.wiki/w/Dungeons:Jungle_Abomination

项目用 item_display 拼装模型，骑在隐身载体上，动画烘焙成 mcfunction，管线是 `_tools/display_mob.py`。动手前只读这几个文件，读完就开始做：

- `_tools/add_leviathan_model.py`：**主要模板**。它给第二柱领主（利维坦）穿模型，换装、技能钩子、隐身、发光的写法照抄，把「利维坦 / 第二柱」换成「路西法 / 第一柱」
- `_tools/add_sunken_skeleton.py`：`held=` 手持物的写法
- `_tools/add_heart_of_ender.py`：大体型 Boss 的 `model_scale` 和部件写法，二阶段参考
- `_tools/display_mob.py` 开头的文档字符串：坐标系、发光、手持物、动画规则
- `_tools/leviathan_ref/SOURCES.md`：署名格式

## 2. 提取（第一步，先做完再碰模型）

**工具：**
- 用开源的 CUE4Parse + CUE4Parse-Conversion，写一个小的 .NET 控制台程序，批量导出。FModel 是图形界面，不适合脚本化，只在核对时用。
- 本机没有 .NET SDK。允许用 `winget install Microsoft.DotNet.SDK.8` 安装，NuGet 包只用 CUE4Parse 官方发布的版本。除此之外不装、不下载任何其他可执行文件。
- 本机有 Blender 5.2，可用来渲染对照图（用后台模式加 Python 脚本）。

**AES 密钥：**
- 用 Dungeons 模组社区公开发布的那把密钥。
- 用解开 pak 索引来验证：索引能解析出文件列表才算对。
- 找不到公开密钥就停下来告诉用户。不要从游戏进程内存或 exe 里提取密钥。

**目录：**
- 原始导出放仓库外：`D:\agent\dungeons_extract\`。它不进 git。
- 只把最终用到的贴图、音效和中间数据放进 `_tools/lucifer_ref/` 与 `_tools/lucifer_p2_ref/`。
- **游戏目录只读，绝不写入或修改任何文件。**

**先打通一条再批量：** 密钥验证后，先把 Mossy Skeleton 的网格加一段动画完整导出一次，用 Blender 打开确认网格、贴图、动画都对。UE 版本和压缩设置由你自己确定，这一步对了再批量导出。

**要找的资产：** 先列出 pak 里所有路径，按名字筛选，不要猜路径。
- Mossy Skeleton 的 SkeletalMesh、Skeleton、贴图（含 `_E` 自发光图）、全部 AnimSequence
- Root Rot Armor 的各部件网格和贴图（盔甲一般是挂在英雄骨架上的独立网格）
- Necromancer 的 Skeleton 和全部 AnimSequence
- Jungle Abomination 的 SkeletalMesh、Skeleton、贴图（含 `_E`）、全部 AnimSequence，以及它召唤或附带的网格（如藤蔓、花）

**导出格式：** 网格用 glTF（带骨骼和权重），动画用 glTF 或 PSA，贴图用 PNG，原分辨率不缩放。

**清单：** 写一份 `D:\agent\dungeons_extract\INVENTORY.md`，内容包括：
- 每个资产的游戏内路径、导出文件、尺寸或时长
- 每个骨架的骨骼名列表
- 每段动画的名字、帧数和时长

## 3. 网格转成 bbmodel

管线只认方块（cube）。Dungeons 的模型本身也是方块拼成的，所以要**无损还原**，不是重新建模。

**每个方块的还原：**
- 网格按连通分量拆开。一个分量通常是一个长方体：8 个或 24 个顶点，12 个三角形。
- 在所属骨骼的局部空间里求出长方体的中心、尺寸和朝向。
  - 与骨骼轴对齐的，写成普通 cube。
  - 朝向有旋转的，给它单独建一根子骨骼，把旋转放在这根骨骼的 rest 上。
- 每个面的 UV 直接从网格的 UV 换算成贴图像素矩形 `[u0,v0,u1,v1]`，包括镜像和翻转。不要目测，也不要套 box UV 规则。
- 只有一面的薄片（树叶、花瓣这类）写成厚度为 0 的 cube，两面都给 UV。
- 不是长方体的分量（极少见）要单独列出，在报告里说明怎么处理的。

**骨骼：**
- 权重按刚性处理：每个分量归到权重最大的那根骨骼。
- 有分量的权重明显分散在多根骨骼上时，列进报告。
- 骨骼名、层级和 pivot 按原骨架保留。

**坐标换算：**
- UE 是 Z 向上、左手系，单位厘米。要换算到管线的 Java 模型空间：+y 向上，生物面向 -z，16 单位为 1 格。
- 换算的正确性用对照图验证：正面渲染必须和原作正面对得上，不能左右或前后反了。

**缩放：**
- 两个阶段用同一个缩放系数，这样两个阶段之间的体型比例和原作一致。
- 系数这样定：一阶段游戏内身高约 2.4 格，二阶段按同一系数算出多高就是多高。
- 二阶段超过 6 格时，在检查点 A 报告，让用户决定。

## 4. 一阶段：Mossy Skeleton + Root Rot Armor

**盔甲穿戴：** 盔甲网格是按英雄骨架做的，要挂到 Mossy Skeleton 的骨骼上。
- 按部位对应：头盔→头，胸甲→身体，袖子→两臂，下摆和护腿→两腿。
- 每个盔甲分量挂到对应的**同一根骨骼**上，这样动作自动跟随，不增加部件数。
- 两套骨架比例不同时，每个部位只允许一个统一的平移加缩放，要在报告里写出数值。
- 被盔甲完全挡住的骷髅面删掉。要用射线或渲染来判断「完全挡住」，不要凭感觉。

**贴图：** 身体和盔甲的贴图合成一张图集，以 base64 内嵌进 bbmodel，`textures[0]` 必须是这张图集。每块的来源和偏移写进 `atlas_regions.json`。

**发光：**
- 有 `_E` 自发光图的区域（如兜帽下的眼睛），放到发光骨骼上（`glow=`）。
- 发光骨骼只放自发光的方块，不要整块身体都发光。

**手持专武「蛇矛」：** 不要建武器模型。
- `held="weapon"`，写法同 `add_sunken_skeleton.py`，挂在右手骨骼上。
- 换装时把载体主手设成路西法专武：`minecraft:netherite_spear`，带 `custom_model_data={floats:[1110014.0f]}`，掉落几率 0。
- 武器的贴图和模型由 `_tools/add_lucifer.py` 生成，不要改它。
- 对照图里要能看到矛握在右手里，方向正确。

**动作：** Necromancer 的动画重定向到 Mossy Skeleton 的骨架上。
- 先比较两套骨架的骨骼名和 rest 姿态。同名骨骼直接按局部旋转的差量重定向，不同名的在报告里列出对应关系。
- Necromancer 没有、Mossy Skeleton 有的骨骼（如盔甲根须若有独立骨骼），用 Mossy Skeleton 自己同名动画的轨道，没有就保持 rest。
- 采样：按原动画的关键帧导出，不要逐帧烘满；同一根骨骼相邻关键帧变化小于 0.5° 的可以合并。
- 换算：管线把关键帧旋转**直接加**在 rest 欧拉角上，四元数差量不能这样加。正确做法是：每个采样点先求出骨骼局部的绝对欧拉角，顺序同 `display_mob.py` 的 `euler()`（ZYX），再减去 rest 欧拉角；相邻关键帧之间把角度展开（unwrap），避免插值时翻转 360°。

| 顺序 | clip | 循环 | 来源（按实际动画名对应） | 用途 |
| --- | --- | --- | --- | --- |
| 0 | `idle` | 是 | Necromancer Idle | 站立 |
| 1 | `walk` | 是 | Necromancer Walk。原作是悬浮滑行就改用 Mossy Skeleton 自己的 Walk 腿部轨道 | 移动 |
| 2 | `attack` | 否 | Necromancer 普通攻击 | 普通技能、持矛前刺 |
| 3 | `strong` | 否 | Necromancer 强力攻击 | 重招 |
| 4 | `cast` | 否 | Necromancer 施法或召唤 | 施法类技能 |
| 5 | `laugh` | 否 | Necromancer Novelty | 嘲讽、大招前摇 |
| 6 | `stun` | 否 | Necromancer Stun | 被驱魔法阵束缚 |
| 7 | `rise` | 否 | Necromancer 出场或 Spawn | 降临登场 |

找不到对应动画的行，在检查点 A 列出来，提出替代方案。

**技能映射：**
- 路西法的技能钩子在 `rpg/data/rpg/function/taint/` 下：`sk1_1` 到 `sk1_5`、`ult1_warn`、`ult1`。读各 `sk1*.mcfunction` 和 `ult1*.mcfunction`，弄清每招做什么、伤害在第几刻生效。
- 按招式内容给每个钩子挑一个 clip，写成 `SKILLS` 字典，写法同利维坦。凡是沿视线刺出蛇矛的招，用 `attack`。
- 出手帧要对准伤害生效的那一刻。对不上就改 clip 的播放速度或裁剪，不改技能代码。

## 5. 二阶段：Jungle Abomination

只做模型、动作和调试入口。阶段切换的战斗逻辑和二阶段技能不在本次范围内。

**模型：** 按第 3 节转换，贴图单独一张图集。
- 部件按骨骼的运动划分，不超过 20 个，超过就合并运动幅度最小的骨骼，并在报告里列出合并了哪些。
- 有 `_E` 自发光图的区域放到发光骨骼上。
- 它召唤或附带的网格（藤蔓、花等）先只列进清单，不建进二阶段模型。

**动作：**
- 导出它的全部动画，按原名转成 clip，名字写成 `animation.<原名小写>`。
- `idle` 和移动用的那段必须排在最前，其余按原顺序。

**接入方式：**
- 载体还是路西法本人：带 `rpg_dm_lord=1` 的卫道士。
- 切换信号是 tag `rpg.lu.phase2`，只由以后的战斗逻辑加上或去掉，生成器只读它。载体带它时穿二阶段模型，不带时穿一阶段模型。
- `rpg.lu` / `rpg.lu2` 仍是管线自己的「已穿好」标记（同利维坦的 `rpg.lv`），不要拿它们当切换信号。
- 加上或去掉 `rpg.lu.phase2` 后，旧阶段的部件和「已穿好」标记必须全部清掉，新阶段立刻穿上，不能两套同时存在。
- 每段动作都提供 `rpg:lucifer_p2/play/<clip>`，执行者是载体，供以后写技能时调用。

## 6. 交付内容

| 路径 | 内容 |
| --- | --- |
| `_tools/lucifer_ref/lucifer.bbmodel` | 一阶段模型和全部动作，事实来源 |
| `_tools/lucifer_p2_ref/lucifer_p2.bbmodel` | 二阶段模型和全部动作，事实来源 |
| `_tools/lucifer_ref/`、`_tools/lucifer_p2_ref/` | 贴图、音效、`SOURCES.md`、`REPORT.md`、对照图 |
| `_tools/convert_dungeons.py` | 从导出的 glTF/PSA 生成 bbmodel 的转换脚本，可重复运行 |
| `_tools/add_lucifer_model.py` | 一阶段薄配置，结构同 `add_leviathan_model.py` |
| `_tools/add_lucifer_p2_model.py` | 二阶段薄配置 |
| CUE4Parse 导出程序 | 放在 `D:\agent\dungeons_extract\exporter\`，不进仓库 |

**构建接入：** 在 `_tools/rp_build.sh` 和 `_tools/build.sh` 里，两个 `add_lucifer*_model.py` 都挂在 `add_leviathan_model.py` 的下一行。

**署名：** README「素材来源」加一行。

固定配置，不要改：

| 项 | 一阶段 | 二阶段 |
| --- | --- | --- |
| key | `lucifer_lord`（`lucifer` 已被蛇矛占用） | `lucifer_p2` |
| label | `路西法` | `路西法·二阶段` |
| tag | `rpg.lu` | `rpg.lu2` |
| score | `rpg_lu` | `rpg_lu2` |

`rpg:lucifer_lord/...` 和 `rpg:lucifer_p2/...` 下的函数都由生成器写，其他命名空间不手写函数。

**音效：**
- 用 wiki 上的原作音效（和本体一致，而且已经是 ogg）：Mossy Skeleton 页的 Attack、Death、Hurt、Idle、Step；Jungle Abomination 页 Sounds 一节的全部。
- 按原名放进各自的 `sounds/`，用 sounds、cues、enter_cues 绑定到帧，写法同利维坦。
- 下载办法：curl 会被 Cloudflare 拦截（403）。在本机起一个 POST 接收页，用浏览器打开 minecraft.wiki 任意页面，在页里 `fetch('/images/<文件名>')` 后 POST 回本机。拿不到就停下来告诉用户。

**来源记录：**
- `SOURCES.md` 每个文件写一行：文件名、字节数、sha256 前 16 位、来源（pak 内路径或 wiki 直链）。
- 写明版权归 Mojang 所有，本项目非商业，与 Mojang 无关联。README 和 `SOURCES.md` 都要写。

## 7. 管线硬限制（来自 display_mob.py，违反会报错或显示错误）

- **坐标：** Java 模型空间，+y 向上，生物面向 -z
- **贴图与 UV：** 只读 `textures[0]`；面的 uv 按 `[u0,v0,u1,v1]` 读取
- **部件数：** 一个独立运动的部件就是一个 item_display。一阶段不超过 12 个，二阶段不超过 20 个
- **部件大小：** 每个部件内的元素以包围盒居中后，坐标必须在 -16..32 之内
- **骨骼旋转：** `parts` 的第一根骨骼可以有任意 rest 旋转；合并进来的子骨骼只能绕一个轴转，且不超过 ±45°
- **违反上面两条时的处理顺序：**
  1. 旋转取整到最近的允许角度（单轴、±45° 以内），前提是任何顶点因此移动不超过 1 像素
  2. 不行就把方块并进最近的、满足条件的骨骼
  3. 最后才单独拆成一个部件。每一次拆分都列进报告，并保证总数不超上限
- **动画通道：**
  - 只有 rotation 和 position，没有 scale。原动画有缩放轨道的，在报告里列出，并说明怎么处理的
  - 关键帧只能写纯数字，不能用 Molang
  - 插值只能用 linear、catmullrom、step
- **clip：** 同一时间只播放一段；`idle`、`walk` 必须排在最前；动画名写成 `animation.<clip>`
- **关键帧叠加：** 旋转直接加在 rest 欧拉角上，位置直接相加
- **载体隐身：** 用 `tick_late` 处理，照抄利维坦

## 8. 流程：两个检查点

**检查点 A：提取与静态模型。** 做完提取、两个阶段的静态模型后停下，交出：

- `INVENTORY.md` 的摘要：找到了哪些资产、哪些没找到。
- 两个阶段的四视角对照图：正面、侧面、背面、四分之三。每张左边是 Blender 渲染的原网格，右边是转换后的 bbmodel，同一相机。一阶段要穿着盔甲、手持蛇矛。
- 每个视角的轮廓重合度（IoU），低于 0.97 的要说明原因。
- 部件表：部件名、包含的骨骼、是否发光。
- 两套骨架的骨骼对应表，以及盔甲每个部位的平移和缩放数值。
- 动画清单和第 4 节表格的对应方案，以及二阶段的动画列表。

用户确认前不要做动作。

**检查点 B：动作与接入。** 做完全部 clip、技能映射和构建接入后停下，交出：

- 数值验证：每段动作在管线烘焙的**每一刻**，比较原动画和管线 `posed_matrix` 算出的每根骨骼世界位置，给出最大误差和出现在哪一刻、哪根骨骼，单位是像素。
- 每段动作关键时刻的并排对照图，左原作、右转换结果。
- 时长表，以及技能钩子与 clip 的对照表，写明出手帧和伤害生效的那一刻。
- 调试命令：
  - `/function rpg:taint/lord1` 召唤路西法，确认换装、隐身、技能动作都正常。
  - 给它加上 `rpg.lu.phase2` tag 后变成二阶段，去掉后变回来，两次都不留残余部件。

## 9. 验证（每个检查点交付前都要过）

- `_tools/rp_build.sh`、`_tools/build.sh` 无报错
- `_tools/rp_validate.py` 无问题
- `_tools/server_test.py` 无函数加载错误
- 载体被移除、领主十分钟消散、驱魔成功、阶段切换之后，都没有残留的 item_display
- 能进游戏就截图；进不了就明确写「未在真实游戏内看过」
- 构建通过不等于完成，还原度要看对照图和数值误差

测试实例在 `D:\minecraft\PCL启动器\.minecraft\versions\1.21.11-Fabric 0.19.3`，同步前先问用户。

## 10. 不要做的事

- **游戏本体：** 只读。不改、不移动、不复制整个 pak 到别处。
- **改别人的东西：**
  - 不改路西法的战斗逻辑、技能数值、掉落和特效，只加换装与动作钩子
  - 不写阶段切换的条件和二阶段技能，只提供 `rpg.lu.phase2` 接入点和 `play/<clip>` 函数
  - 不改 `add_lucifer.py`，蛇矛的贴图和模型属于它
  - 不改其他怪的模型和行为
  - 不改 `display_mob.py`；必须改时要向后兼容，并证明现有怪的生成结果逐字节不变
  - 同一工作区还有其他会话在改文件：只碰自己的路径，不回滚、不格式化、不顺手修别人的改动
- **超出本次范围：** 不做半透明效果；不做 Jungle Abomination 的召唤物
- **git：**
  - `_data_loot.json`、`_guide_sections.json` 的换行差异是构建产物，不要提交
  - 没有用户明确要求，不提交、不推送、不切分支
  - 用户要求提交时，只暂存自己的路径，用 `git -c user.name=fanxing1515 -c user.email=fanxing1515@gmail.com commit`

## 11. 用户以前打回过的问题

- **贴图映射：** 映射靠目测。这次 UV 一律从网格换算，不许手填。
- **骨架比例：** 头、肩、手臂的相对位置不对，模型看起来松散。这次骨骼 pivot 一律取自原骨架。
- **肢体朝向：** 手和肢体末端的朝向反复猜错。这次用对照图和数值误差证明。
- **内衬取色：** 内衬放在了已被别的部件占用的贴图区域，出现杂色条。图集拼合后要检查区域不重叠。
- **前后与背面：** 披风、背部部件前后装反。每次对照都要包含侧面和背面。

## 12. 汇报

- **如实：** 没做的、没验证的、推断的都写明。从本体提取的叫「提取」，自己补的叫「补做」，不要混在一起说。
- **停下来问：** 遇到需要用户决定的事就停下来问，不要自己猜。
