# 首席附魔师 M1 素材与结构审阅

目标是《Minecraft Dungeons II》的 The Prime Enchanter。以 Wiki 的原游戏基础贴图、无特效动作 GIF 和原作实机录像作为外观与动作依据。本次先交素材、UV、部件方案与关键姿态，按教皇流程在确认后进入 M2 静态模型。[角色与图库](https://minecraft.wiki/w/Dungeons_II:The_Prime_Enchanter#Gallery)

## 已核对的素材

11 段原尺寸 GIF 共 862 帧，已逐帧解码。Wiki 的 64×64 RGBA 基础贴图与公开数据镜像的 4096 个像素完全相同。Wiki 的 1000×1000 抬拳渲染用于核对侧脸、帽壳和棕护腕。Mojang 宣传图和实机选帧补足冰雷拳手性与披风背面。原件规格、文件哈希及引用见[素材来源](SOURCES.md)与[素材清单](source_manifest.json)。

静息和 11 段无特效动画显示灰色拳面与棕色护腕。官方图和实机录像的蓄力时段可见角色右拳冰蓝、左拳雷黄。M2 以灰拳和棕护腕作为本体，保留双拳挂点。冰电外盒及发光范围可按参考重建为独立附件，原始附件材质和独立音效目前缺少可核验文件。[官方战斗图](originals/bft-pe.jpg) · [实机选帧](m1/motion/gameplay/intro/contact.jpg)

## UV 与部件

逐面 UV 表以原图整数像素边界记录头、鼻、躯干、腿、袖、肩罩和帽壳。帽后有三根短飘带，背后有两片长披风。连拳与天降近帧可辨披风的折点和末端缺口。计划让两片披风的同高度段共用上、中、下三个枢轴。头帽、眼鼻与青色核心随头，袖与腕分骨，两片袍摆各随腿，初步预算 12 个展示部件。尚待试装的拳腕拼片、帽侧翻片及披风反面朝向均列在 UV 文档中。[UV 和部件表](m1/UV_AND_PARTS.md)

候选模型标识为 `prime_enchanter`、`rpg.prime_enchanter`、`rpg_pe`。原作酒红袍、青蓝帽饰和冰雷手性作为本次审阅基准。篡夺者设计稿里的 `usurper_holy` 白金皮肤可在接入该玩法时单独处理。M2 将用 Blockbench 比对正、侧、背和四分之三视角，测试帽带、披风与手腕相对位置。后续打包沿用 `display_mob.py` 单图集与数字位移、旋转通道。

## 动作依据

原 GIF 时长包含末帧停留。下表的 tick 是 20 TPS 下的初步取整，M3 需通过模型逐帧并排对照后定稿。关键姿态的帧号与出手锚点均来自可见姿势。实际伤害和召唤事件由玩法决定。

| 顺序 | 候选 clip | 原 GIF 时长 | 建议刻数 | 关键姿态 | 原作选帧 |
|---:|---|---:|---:|---|---|
| 0 | `idle` | 1.00 秒 | 20 | 双拳抱架，肩和披风有轻微起伏 | [选帧](m1/motion/keypose_sheets/idle.jpg) |
| 1 | `walk` | 0.92 秒 | 18 | 反相摆臂迈步，披风向后拖曳 | [选帧](m1/motion/keypose_sheets/walk.jpg) |
| 2 | `appear` | 2.37 秒 | 47 | 0.25 秒从上方出现，0.29 秒进入低伏落地候选，随后起身抱架 | [选帧](m1/motion/keypose_sheets/spawn.jpg) |
| 3 | `death` | 5.71 秒 | 114 | 仰身、前栽、屈膝，约 4.6 秒进入倒地段 | [选帧](m1/motion/keypose_sheets/death.jpg) |
| 4 | `forward_strike` | 2.50 秒 | 50 | 蓄势后快速直冲，1.50 秒伸拳最大 | [选帧](m1/motion/keypose_sheets/forward_strike.jpg) |
| 5 | `fury_fist` | 6.92 秒 | 138 | 两串拳，中间回架，约 5.50 秒双拳砸地 | [选帧](m1/motion/keypose_sheets/fury_fist.jpg) |
| 6 | `launch` | 3.96 秒 | 79 | 升至画外，1.13 至 2.21 秒无角色画面，回归时低伏 | [选帧](m1/motion/keypose_sheets/launch.jpg) |
| 7 | `lightning_slam` | 4.42 秒 | 88 | 1.96 秒开始大幅离地，2.17 秒附近高点，2.67 秒落地候选 | [选帧](m1/motion/keypose_sheets/lightning_slam.jpg) |
| 8 | `overcharge` | 3.58 秒 | 72 | 左拳举到头侧，约 1.92 至 2.83 秒保持 | [选帧](m1/motion/keypose_sheets/overcharge.jpg) |
| 9 | `hurt` | 2.29 秒 | 46 | 取 Staggered 的失衡、回摆和恢复 | [选帧](m1/motion/keypose_sheets/staggered.jpg) |
| 10 | `summon` | 2.25 秒 | 45 | 0.58 秒双拳举起的端姿 | [选帧](m1/motion/keypose_sheets/summon.jpg) |

`idle` 与 `walk` 拟循环。天降空帧和突进的局部伸长超出教皇所用的纯位移、旋转通道，后续审阅会展示近似方案及其与原帧的差异。超载 GIF 的 3.58 秒按观察记录，公开游戏数据里另有维持时间，二者留作玩法交接。完整帧时序和建议触发时点见[动作研究](m1/motion/MOTION_STUDY.md)与[关键姿态数据](m1/motion/keyposes.json)。

当前为 M1 研究交付，模型与动作尚未制作，未在真实游戏内看过。
