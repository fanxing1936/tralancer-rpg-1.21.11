# 首席附魔师 M3：动作审阅

[打开 11 段并排对照](m3/index.html) · [Blockbench 模型](prime_enchanter.bbmodel) · [挂点](sockets.json) · [素材来源](SOURCES.md)

按用户批准的 M2 静态模型，由 Astra Ultra 对照 11 段原作 GIF 重新制作姿态。未沿用上一版动作的骨骼角度。M2 的体块、骨骼静态姿势、UV 和原贴图保持一致；动作保存在 `.bbmodel` 中。审阅图左侧为原作 GIF 解码帧，右侧为 Blockbench 5.2.2 在相同时间的原生渲染。每段的整幅对照锁定摄影机，另有局部放大、侧面和背面。并排动图按 GIF 原始延迟播放，页面里的循环仅用于审阅。 [Minecraft Wiki 原作图库](https://minecraft.wiki/w/Dungeons_II:The_Prime_Enchanter#Gallery)

| ID | 动作 | 依据 | GIF 时长 | 模型时长 | 循环 | 对照 |
|---:|---|---|---:|---:|:---:|---|
| 0 | `idle` 待机 | 有动图 | 1.000 s | 1.00 s（20 tick） | 是 | [6 组](m3/preview/idle/keyframes.jpg) |
| 1 | `walk` 行走 | 有动图 | 0.920 s | 0.90 s（18 tick） | 是 | [6 组](m3/preview/walk/keyframes.jpg) |
| 2 | `appear` 登场 | 有动图 | 2.370 s | 2.35 s（47 tick） | 否 | [10 组](m3/preview/appear/keyframes.jpg) |
| 3 | `death` 倒地 | 有动图 | 5.710 s | 5.70 s（114 tick） | 否 | [11 组](m3/preview/death/keyframes.jpg) |
| 4 | `forward_strike` 前冲重拳 | 有动图 | 2.500 s | 2.50 s（50 tick） | 否 | [13 组](m3/preview/forward_strike/keyframes.jpg) |
| 5 | `fury_fist` 狂拳连击 | 有动图 | 6.920 s | 6.90 s（138 tick） | 否 | [19 组](m3/preview/fury_fist/keyframes.jpg) |
| 6 | `launch` 跃起回场 | 有动图 | 3.960 s | 3.95 s（79 tick） | 否 | [11 组](m3/preview/launch/keyframes.jpg) |
| 7 | `lightning_slam` 雷霆砸地 | 有动图 | 4.420 s | 4.40 s（88 tick） | 否 | [15 组](m3/preview/lightning_slam/keyframes.jpg) |
| 8 | `overcharge` 过载蓄力 | 有动图 | 3.580 s | 3.60 s（72 tick） | 否 | [9 组](m3/preview/overcharge/keyframes.jpg) |
| 9 | `hurt` 失衡受击 | 有动图 | 2.290 s | 2.30 s（46 tick） | 否 | [8 组](m3/preview/hurt/keyframes.jpg) |
| 10 | `summon` 召唤 | 有动图 | 2.250 s | 2.25 s（45 tick） | 否 | [9 组](m3/preview/summon/keyframes.jpg) |

## 姿态锚点

以下从每段开始计时。锚点取 GIF 的可见姿态；真实游戏的伤害、召唤和特效触发时刻未验证。模型长度对齐 20 TPS，关键姿态仍使用源帧实际起点。

| 动作 | 原帧与时间 |
|---|---|
| `appear` | f7：0.290 s，低伏落地 |
| `death` | f112：4.670 s，俯卧落定 |
| `forward_strike` | f36：1.500 s，右拳最大前伸 |
| `fury_fist` | f18：0.750 s，首轮前伸；f33：1.380 s，首轮转身；f90：3.750 s，次轮前伸；f95：3.960 s，张臂；f108：4.500 s，次轮转身；f132：5.500 s，双拳砸地 |
| `launch` | f27：1.130 s，离开画面；f53：2.210 s，回场触地 |
| `lightning_slam` | f47：1.960 s，起跳；f64：2.670 s，低伏落地 |
| `overcharge` | f46：1.920 s，举拳蓄力端势 |
| `hurt` | f11：0.460 s，后仰失衡 |
| `summon` | f14：0.580 s，双拳首次完整举起 |

`sockets.json` 提供待机与各锚点的左右拳、额纹、帽顶、落地中心候选点。数值用未缩放的模型单位，+Y 向上、−Z 朝前；挂点位置和方向随姿态采样。拳与额纹是模型表面锚点，落地中心是根骨在模型地面的投影。

## 肢体放大

按原尺寸 GIF 的袖口、拳端和肩甲纹理边测量。表中比例是模型骨骼的局部 X、Y、Z 三轴拟合值。局部 Y 沿手臂长轴，X 与 Z 控制横截面。拳套和肩甲由上级臂骨一起带动。

| 动作 | 原帧 | 缩放 |
|---|---|---|
| [前冲重拳](m3/preview/forward_strike/scale_comparison.jpg) | f34–38，1.420–1.580 s | 右臂先加粗并伸至 `1 × 1.4 × 2`，f36 沿手臂长轴伸至两倍（`1 × 2 × 1.5`）。f37 还剩约 15% 伸长，f38 恢复原尺寸。 |
| [雷霆砸地](m3/preview/lightning_slam/scale_comparison.jpg) | f62–65，2.580–2.710 s | 左臂横向先扩至 `1 × 1 × 2`，f64 落地达到 `1.5 × 1 × 2`，f65 恢复原尺寸。 |

其余九段也复核了原尺寸帧，其中行走、举拳和连击的轮廓变化可由转角和遮挡解释。可复测的像素坐标和抽查说明记录在 [攻击动作量测](m3/astra_strike_scale.py) 与 [其余动作复核](m3/astra_other_scale.py)。

## 复刻范围与验证

- Blockbench 模型保留原生缩放关键帧。Java 验证使用本角色专用的 [缩放转换](m3/scale_motion.py)，将完整骨骼姿态转换成现有显示部件能读取的矩阵。20 TPS 烘焙把 f35、f36 和 f64 的峰值落在最近的刻，最大偏移 20 毫秒。雷霆砸地的 f63 和 f64 落在同一刻，Java 烘焙以 f64 的落地峰值为准。
- 原作有时将左右披风甩成不同角度。M2 每段披风的左右片共用骨骼；这一版保留三段摆动，在 `fury_fist` 砸地和 `death` 扑倒时，两片分开的幅度仍小于原作。
- `appear` 开头、`launch` 中段的透明段用向上出画近似。审阅镜头看不到模型；实际游戏还需要单独验证可见范围与挂点。`lightning_slam` 的高跳按整幅对照检查，局部放大只用于查看骨骼姿势。
- [验证记录](m3/validation.json) 核对磁盘模型原生重开、原贴图、12 个显示部件、两个循环闭合、117 组关键帧与 20 TPS 内存烘焙。11 段并排动图覆盖 862 个源帧，其中登场 6 个、回场 26 个透明源帧已逐帧核对。此阶段未运行整包构建或服务器测试。
- [补缩放前的 Astra 模型](m3/astra_before_scale.bbmodel) 留档。缩放和旋转均以本页链接的 Blockbench 模型为准。

**未在真实游戏内看过。** 本阶段停在 M3 审阅，尚未接入构建、玩法或测试实例。
