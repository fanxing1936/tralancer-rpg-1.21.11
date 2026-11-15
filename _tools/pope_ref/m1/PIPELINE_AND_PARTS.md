# 教皇 M1：管线核对与部件结构方案

日期：2026-11-04。此文是 M1 的实现约束和结构提案，不是已完成模型或动作。尚未生成 `pope.bbmodel`，尚未接入构建，未在真实游戏内看过。模型比例、部件边界、枢轴位置和时长以素材抽帧、UV 反推及之后用户确认的 M2/M3 结果为准。

## 已阅读的项目依据

| 来源 | 本次核对内容 |
|---|---|
| `_tools/display_mob.py` | 全文：模型读取、部件合并、坐标变换、动作采样、声音、动画状态、挂接和孤儿清理 |
| `_tools/add_tower_guard.py` | 薄配置、隐身卫道士及乘客召唤、音效/cues/enter_cues |
| `_tools/add_abaddon_model.py` | `tick_late` 在 `rpg:command/tick_end` 后恢复隐身；没有复制其玩法挂接 |
| `_tools/abaddon_geo.py` | 从贴图展开推导几何；脚本不能复现后续 Blockbench 手改的声明 |
| `_tools/tower_guard_ref/tower_guard.bbmodel` | 实际模型格式、UUID/outliner 层级、逐面 UV、嵌入贴图、动画关键帧 |
| `_tools/rp_build.sh`、`_tools/build.sh` | 教皇生成器将来均插在 `add_tower_guard.py` 紧后 |
| `_tools/rp_validate.py`、`_tools/server_test.py`、`_tools/mc_env.py` | 资源验证和真实专用服务器加载检查的调用方式 |

本次没有修改上述文件，也没有运行构建。现有脚本不是新模型的视觉正确性证明。

## 固定接口

固定 `key="pope"`、`label="教皇"`、`tag="rpg.pope"`、`score="rpg_pp"`。载体为隐身 `minecraft:vindicator`，`Health:1000f` 与 `minecraft:max_health=1000`。外观召唤器仅建立载体、标签、外观乘客与必要的持久/静音/隐身设置；不复制圣卫的护甲、移动、攻击、抗击退和索敌属性配置，不建立技能、掉落、阶段转换或 AI。

| 固定编号 | clip | 循环 | 入口 |
|---:|---|---|---|
| 0 | idle | 是 | `rpg:pope/anim/enter/idle` |
| 1 | walk | 是 | `rpg:pope/anim/enter/walk` |
| 2 | attack | 否 | `rpg:pope/anim/enter/attack` |
| 3 | summon | 否 | `rpg:pope/anim/enter/summon` |
| 4 | cast | 否 | `rpg:pope/anim/enter/cast` |
| 5 | appear | 否 | `rpg:pope/anim/enter/appear` |
| 6 | teleport_in | 否 | `rpg:pope/anim/enter/teleport_in` |
| 7 | teleport_out | 否 | `rpg:pope/anim/enter/teleport_out` |
| 8 | whirlwind | 否 | `rpg:pope/anim/enter/whirlwind` |

`teleport_in` 与 `teleport_out` 各为用户指定的 0.9 秒，即 18 刻；其他长度和出手时间应由抽帧报告定出，不能从圣卫动作借用。`.bbmodel` 内名称使用 `animation.<clip>`；`Mob.clips` 中的循环布尔值与 `.bbmodel` 的 `loop` 字段必须一致，前者控制运行时循环，后者控制曲线端点插值。

## 提议的部件预算：最多 12 个 item_display

以下是预算结构，不是对未完成的 Arch-Illager 骨骼数据的断言。所有可见部件保持原作蓝袍、金属项链、红宝石、皇冠与权杖配色。UV 不在此文猜定，逐面取样由独立 UV 表负责。

| # | display / 首骨骼 | 父骨骼提案 | 包含内容 | 单独运动的理由 |
|---:|---|---|---|---|
| 1 | body | root | 躯干蓝袍、项链及红宝石、固定衣领 | 躯干俯仰、呼吸、受吸动作；项链若没有独立摆动证据先刚性合并 |
| 2 | head | body | 头、鼻、固定面部几何 | 转头/仰头，与肩保持紧凑 |
| 3 | crown | head | 完整皇冠 | whirlwind 的脱冠；不可合并进 head |
| 4 | right_arm | body | 右上臂/袖上段 | 右肩抬举与摆臂 |
| 5 | right_hand | right_arm | 右前臂与手（是否需要分肘以抽帧为准） | 右手姿态与手部挂点 |
| 6 | left_arm | body | 左上臂/袖上段 | 召唤动作的左肩抬举 |
| 7 | left_hand | left_arm | 左前臂与手（是否需要分肘以抽帧为准） | 握杖姿态、脱手和左手挂点 |
| 8 | right_leg | root | 右腿/鞋与随腿运动的袍下段（若原素材支持） | 跑动及被吸走时独立姿态 |
| 9 | left_leg | root | 左腿/鞋与随腿运动的袍下段（若原素材支持） | 跑动及被吸走时独立姿态 |
| 10 | cape | body | 后背披布/袍后摆（名称与分界待 UV/背面参照核定） | 后摆变化；不得将正面衣料装到背面 |
| 11 | staff | left_hand | 权杖非发光主体 | whirlwind 脱手；不可合并进手 |
| 12 | staff_glow | staff | 有来源证据的权杖不透明发光实体部分 | 独立发光骨骼，必要时独立运动；不制作半透明光晕 |

`root` 是空的控制骨骼，不建立第 13 个 display。没有独立肘运动证据时可把 `right_hand`、`left_hand` 几何合并回各臂，保留空挂点骨骼，降为 10 个 display；此选择必须由关键姿态证据决定。发光部分若原参照无法辨认，不用猜测几何补足预算，先记录缺证并按无发光权杖渲染建模。

持杖手已按 `MCD_Arch-Illager_Idle_Highblock_Halls_(front_view).gif` 的正面逐帧参照核对：权杖位于画面右侧，对应角色左手（Java -X）；因此 staff 的父骨骼为 left_hand，不沿用圣卫右手持武器的习惯。

普通动作里 crown 随 head、staff 随左手、staff_glow 随 staff。脱冠和脱手不是修改 `.bbmodel` 层级：在固定层级下，用父矩阵逆变换把目标世界路径换算成本地 `position/rotation`，烘焙为纯数值键。这样不需要改共享管线，也不会把脱手权杖一直锁在手心。

`parts` 的第一项为 body，可作为孤儿清理时的锚点；不要让一个只有辅助骨骼而没有几何的空部件排在首位。总实体预算是 1 个载体 + 最多 12 个 item_display。

## 坐标、缩放及模型格式

`display_mob.py` 使用 Java 模型空间，+Y 向上、朝向 -Z；与已读取的圣卫模型一致，右侧骨骼在 +X，左侧在 -X。Bedrock 导入中的 X 镜像、X/Y 旋转符号变化只发生在导入过程，写入 `.bbmodel` 后关键帧值不再翻转。

实际圣卫文件的 `meta` 为 `format_version: "5.0"`、`model_format: "bedrock"`、`box_uv: false`，但管线按已存储的 Java 空间 `from/to/origin/rotation` 读取。`groups` 定义 UUID、名字、origin、rotation；真正层级在 `outliner`，元素由 UUID 引用。`animations[].animators` 按骨骼 UUID 索引。模型的唯一图集放在 `textures[0].source` 的 PNG base64 data URL；`resolution` 与贴图尺寸一致。

约 2.6 格的身高由 `model_scale` 达成。先在 M2 测量标准站姿脚底至冠顶高度 H（模型单位），再取 `model_scale = 2.6 × 16 / H`。权杖高出冠顶的部分另报，不把举杖后的总包围盒误当身体身高。载体 scale 和视觉 model_scale 是两个参数，不能为了身高改载体战斗体积；先保持卫道士默认 scale=1、seat=2.0，M4 通过服务器/客户端确认脚底落地位置。

所有模型部件按自有包围盒居中后必须在 -16..32；`part_model` 对每个输出端点做检查，超出会退出。不要把体型直接拉到超大几何后再依赖 display 缩放掩盖错误。

## 管线已核实的易错点

1. `load_bbmodel` 只读 `textures[0]`。所有原贴图必须放到同一图集，以无损复制和明确坐标偏移记录来源；不可让第二张贴图承担权杖。
2. `part_model` 只取面的 `[u0,v0,u1,v1]` 和非空 `texture`。它不转存面 UV 的 `rotation`，也不直接转存元素自己的旋转。因此需要 90° 旋转的 UV 不能只写 face.rotation；几何旋转应使用可支持的骨骼，UV 旋转若必要则在图集中做可追溯的整块变换。端点倒序只能表达轴向翻转。
3. 每个 display 只采样 `members[0]` 的骨骼链。合并到同一部件的其他骨骼只贡献静态几何；给这些子骨骼加独立动画键不会产生对应运动。独立运动必须分成 display。
4. 首骨骼允许任意 rest 欧拉角。合并的静态子骨骼应尽量零旋转；需要旋转时，只采用单层、单轴、绝对值≤45°。当前导出并不是通用的多层旋转几何烘焙器，不应依赖复杂嵌套的合并旋转。
5. 动画只收 `rotation`/`position`、`linear`/`catmullrom`/`step` 和纯数字值。旋转为 `Rz × Ry × Rx`，把关键帧欧拉值直接加到 rest 欧拉值上，不能把 rest 与动画当成另两个矩阵相乘。position 在该骨骼的父坐标中相加。
6. 骨骼 glow 导出为元素 `light_emission:15`、`shade:false`。它没有额外的光照半径，也不是屏幕泛光，不自动生成半透明光晕。该模型不做旋风、粒子、技能特效。
7. 每个 clip 时长被四舍五入到 0.05 秒的刻；非循环采样应使用 step=1，保证 0.9 秒的末帧及出手采样存在。循环可先用 idle=4、walk=2，但最终以轮廓运动是否丢姿势决定。
8. `cues` 把秒数四舍五入为刻，再放到满足 `(t-step,t]` 的采样帧。step>1 时声音可能延迟到后续采样帧，所以关键出手段应 step=1。`enter_cues` 仅在进入动作时播一次；循环 f0 上的普通 cue 会每圈重播。
9. `enter/<clip>` 把计数清零并立即调用 tick，因此 f0 在调用当天生效，计数会变为 1。报告的 0 秒指调用入口这一刻，不能因内部计数加一把声音/出手全错开一刻。客户端补间仍需视觉检查。
10. idle/walk 按载体水平位移自动切换，采样保持 `STRIDE=4`。其他 clip 播放时移动检测还会更新，但不会中途强制改成 walk。不能同时叠加两个 clip。
11. 非循环动作播放到末采样后下一次 tick 会回 idle，不支持 `.bbmodel` 的“保持末帧”模式。这是现有共享管线行为，M3/M4 交接时间必须明确。
12. `rpg.hurt` 门控和 `HurtTime:10s` 的受伤声音逻辑直接复用，不修改。生成器只会重写自己的 `pope/anim` 和 `pope/debug`；跨会话不得在这两个生成目录里放手写玩法函数。

权杖发光颜色另有限制：动作参照中的顶端会随时间由橙黄变到粉紫，而已取得的 `T_SuperCube.png`（32×32）只有橙黄渐变。共享管线没有贴图切换或材质颜色动画通道，静态 `light_emission` 无法复刻这种变色。继续遵守原贴图和原配色，不重涂粉紫版本，不新增变色 shader 或粒子。M2 先按无发光权杖渲染确定形状，独立 `staff_glow` 骨骼只使用能够确认的原始橙黄贴图面；这只能表达有来源依据的不透明明亮部分，不能宣称完整复刻原作发光表现。

## whirlwind 与瞬移末姿的边界

在现有通道约束下，部件可以脱离、旋转、向同一中心移动。可以保证每个刚性部件的选定中心点在末帧汇聚；不能把这些部件的实际体积缩成一点。头部、躯干和整根权杖仍有体积，简单把中心重叠会留下可见外壳。这必须在 M3 对照中展示，不得把“中心点重合”写成“模型完全消失”。

当前提议保持共享管线不变：whirlwind 表达掉冠、脱手和人物被吸的可见姿态，末姿向转阶段中心收拢；最终消失和末影之心生成由玩法侧在末姿完成时接管。模型会话只报告确切结束时间，不实现转换逻辑。若用户要求不借助玩法移除、仅凭这段 clip 就完全隐没，现有 rotation/position 约束不能实现，需要先重新确认实现边界。

同理 teleport_out 无透明度或 scale 通道，不能在 clip 内做渐隐；不能用随意缩小/藏到极远坐标冒充原动画。是否在瞬移中采用原作可见收势及由玩法隐藏/转移，需在 M1 素材与行为证据中明确。现有非循环自动回 idle 也意味着玩法不能在末帧后无限等待。

## M3 挂点方案

根目录最终 `sockets.json` 参考现有 `heart_of_ender_ref/m3_motion/sockets.json` 的字段：`bbmodel_sha256`、`coordinate_system`、`model_scale`、`carrier_seat`、`samples`。样本至少包含 idle 的 t=0，以及 attack/summon/cast 的所有最终出手秒数。

每个样本给出 `staff_tip`、`right_hand`、`left_hand`、`head_top` 的 `bone`、`local_unposed_point`、`posed_model_point`、`bone_forward_minus_z` 与状态说明。`local_unposed_point` 是该项目几何使用的未摆姿模型坐标，不冒充相对骨轴的零原点局部坐标。`posed_model_point` 由 `posed_matrix` 乘点算出；另列视觉 scale 后的格单位位置便于玩法使用，说明其相对载体脚底、朝向旋转和 seat 补偿，不能只给 display 的 NBT translation。

head_top 取头顶，不自动取皇冠最尖点；若玩法需要冠顶可另行注明。staff_tip 的位置与发射方向分开记录：骨骼 -Z 朝向不一定就是沿权杖轴或原作能量弹方向。未验证的方向要标“候选”。

## M4 待执行验证（本次均未执行）

| 检查 | 需要留下的证据 |
|---|---|
| 构建 | `_tools/rp_build.sh`、`_tools/build.sh` 的完整日志与退出码；注意 `build.sh` 会重建整个 rpg，需在与其他会话不互相覆盖的可控副本进行，不能误删共享现场改动 |
| 资源 | `python _tools/rp_validate.py resourcepack`，核对零问题；缺客户端 jar 时如实记录 |
| 模型结构 | 单图集 base64、逐面 UV 有来源、无越界、全部 clip 顺序正确、9 个入口存在、无 Molang/scale、至多12个部件 |
| 姿态数值 | .bbmodel 实际采样、关键帧对照和 sockets 同一 SHA；出手时刻与烘焙帧/cue 一致；末帧中心收拢但不夸大体积消失 |
| 服务端 | `python _tools/server_test.py <独立测试目录> [等待秒数]`；先准备 `<测试目录>/packtest/datapacks`，脚本自身不复制数据包；通过 `MC_PROBE_FILE` 加入教皇入口/计数/清理探针 |
| 服务端结果判读 | 不能只看 exit code：脚本打印 `server reached 'Done'`、`server complaints`，没有在抱怨存在时主动以非零码退出；要读日志确认函数全部加载及探针结果 |
| 隐身顺序 | `pope/tick` 在 `rpg:command/tick_end` 前、`pope/tick_late` 在它后；清掉隐身后下一刻应恢复；不影响其他怪 |
| 清理 | 召唤一个载体后数部件为预期值；移除载体、等死亡/卸载流程结束后部件为0；多只并存时不误杀仍骑乘的部件；断开骑乘后由孤儿扫描清理 |
| 真实客户端 | 正/侧/背/四分之三视角，逐 clip、发光、握杖、脱冠、脱手、脚底高度及补间视觉；若无法进入，明确写“未在真实游戏内看过” |
| 共享不变 | 默认不改 display_mob.py；若确需改，先在隔离输出保存现有各怪生成物清单与 SHA-256，再逐字节比较新旧输出，不以“构建通过”代替兼容证明 |
| 工作区保护 | 不提交、不推送、不切分支；不暂存其他会话文件；排除 `_data_loot.json`/`_guide_sections.json` 换行；不改 DEVIL_SMOKE、STRIDE、rpg.hurt、玩法和末影之心路径 |

服务器检查允许只读取已有客户端依赖来启动独立测试目录，不等于同步到用户实例。同步到 `D:\minecraft\PCL启动器\.minecraft\versions\1.21.11-Fabric 0.19.3` 前必须另问用户。
