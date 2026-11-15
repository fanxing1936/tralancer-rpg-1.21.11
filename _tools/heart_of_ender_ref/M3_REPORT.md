# M3：Heart of Ender 动作与紫色材质

> **历史材质 v1 快照。** 本报告对应 `15abda3a…fe1f4d`，工程已保留为 [baseline.bbmodel](m3_material_v2/baseline.bbmodel)。下文的「当前」「主模型」「最终」及「未同步」均指当时状态，不代表正在修订的材质 v2。局部透明、眼嘴荧光及独立游戏探针的后续状态见 [MATERIAL_V2_REPORT.md](m3_material_v2/MATERIAL_V2_REPORT.md)。旧动作证据与已知姿态局限继续保留。

**M3 审阅版已生成，待用户视觉审阅；不宣称全部动作已精确还原。** 用户已选择 R2、确认静态形态并授权 M3，以及「发紫光、斑点全部变紫」。本阶段只处理 Heart of Ender 动作与材质，未进入 M4 Arch-Visage 或 M5 接入。

本报告对应主模型 SHA-256：`15abda3ad7c372907257c581bac8822dc7f98feebb7c98e9ca538773fbfe1f4d`。Fourside 可见冠轴修正、E1 收肢方案和 cross_beam 的 C1 抬肢方案已合并；以下哈希、原生渲染、验证及坐标均对应这一版，不引用中间阶段号作为最终结果。

## 审阅入口与事实来源

- 历史主工程：[baseline.bbmodel](m3_material_v2/baseline.bbmodel)。保存后的 `.bbmodel` 是本报告版本的事实来源；7 段动作，顺序为 `idle, walk, mortar, cross_beam, sink, rise, death`。
- 整组审阅入口：[m3_preview/index.html](m3_preview/index.html)。已生成 **254 张关键帧原生 PNG、512 张连续原生 PNG、52 页并排图、7 个 GIF**；并排图位于 `m3_preview/boards/*.png`，由 [review_index.json](m3_motion/review_index.json) 登记和排版。
- 连续预览为 7 个 **12.5 fps** GIF，只供看节奏；不能代替原始 25 fps 逐帧证据、最终模型中的关键帧或管线 20 Hz 烘焙结果。`idle` / `walk` 去掉重复终帧，分别 200 / 100 帧、16 / 8 秒；非循环片段预览保留末姿一帧，比模型时长多 0.08 秒，仅作为 GIF 展示，不改变 `.bbmodel` 的 clip 时长。
- 制作入口：[heart_of_ender_animate.py](../heart_of_ender_animate.py)。它组合独立登记的外壳/小人轨道，经原生 Blockbench 导出，验证导出未改变值、时间与插值；不挂到构建流程，也不自动覆盖未经确认的手改工程。
- 静态基线：[accepted_R2.bbmodel](m3_motion/accepted_R2.bbmodel)。21 个展示部件；当前模型保持 R2 的元素几何、UV、骨骼 rest 和连接，动作不增加部件。数量由外壳身/头/颚 3 个、六肢各两段共 12 个、小人身/头/四肢 6 个组成，以保留各段独立运动。21 超过初始 16 目标，数量已由用户在 M2 确认。

## 每段动作的来源与边界

来源页面：[Minecraft Wiki — Heart of Ender](https://minecraft.wiki/w/Dungeons:Heart_of_Ender)。有动图表示存在直接二维姿态证据，不表示取得原作骨骼、三维深度或原始关键帧。

| clip | 时长 / 播放 | 证据标签 | 使用的具体来源与实现边界 |
|---|---|---|---|
| `idle` | 16 s / 循环 | **外壳有动图；小人有动图** | 外壳依据 `MCD_Heart_of_Ender_Idle.gif` 完整 400 帧、16 秒观测；没有只截前 4 秒复制。可见眼线/肢端约束姿态，烟雾遮挡的连接、深度和骨骼分配仍为推断。小人嵌入 Docile 三周期。 |
| `walk` | 8 s / 循环 | **外壳推断；小人有动图** | 外壳依据 `Heart_of_ender_crawling_with_decal_trail.png` 与页面 Crawl 文字。A/C/E、B/D/F 两组三肢交替支撑是明确设计推断，不是原作步态实录；未把 Vengeful Heart 模型姿态照搬过来。小人使用 `MCD_Arch-Illager_Anxious.gif` 的 8 秒动作。 |
| `mortar` | 4 s / 单次 | **推断** | 页面 Mortar barrage 描述后仰并从嘴发射 13 个紫色弹体，结合 `Minecraft-dungeons-heart-of-ender.jpg`。4 秒时长与蓄势/收势为推断；1.2–2.8 秒保留张口阶段，不把「13 个弹体」编成 13 次下颚脉冲。没有弹体。 |
| `cross_beam` | 4 s / 单次 | **外壳推断；小人有动图** | 外壳依据 `Heart_of_Ender_prepare_to_shoot_beams.png`、`Heart_Of_Ender_laser.jpg` 与页面 Cross beam 文字，采用 C1 六肢外上扬姿态开放小人视线。小人 `MCD_Arch-Illager_Fourside.gif` 完整 2 秒映射到 1–3 秒；0–1、3–4 秒为推断蓄势/收势。页面顺时针是光束扫描，未强行让整个外壳或小人自转。没有光束。 |
| `sink` | 2 s / 单次 | **推断** | 依据页面 Arch-Visages 相关沉地描述和 `Heart_of_Ender_in_game.png`。仅用根骨 position 下移，未用 scale 或裁图冒充沉地；时长为推断。 |
| `rise` | 2.4 s / 单次 | **推断** | 同上；只用 position 升起。并未把它称作原作 sink 的已知倒放。 |
| `death` | 4 s / 单次 | **推断** | 依据 `Hero_kills_Heart_of_Ender_Arch-Illager_disappear.jpg` 与死亡文字说明。低头、肢体向内蜷曲，小人在 3.2–3.8 秒以自身 position 最后沉地消失；**外壳不整体沉地**，也不能称所有肢端降低（A 端会升高）。过程为推断，不加 scale、碎裂或粒子，运行时死亡触发未制作。 |

详细轨道与来源索引：[shell_motion.json](m3_motion/shell_motion.json)、[shell_measurements.json](m3_motion/shell_measurements.json)、[inner_motion.json](m3_motion/inner_motion.json)、[inner_REVIEW.md](m3_motion/inner_REVIEW.md)。小人的最新原生复核与残差见 [inner_NATIVE_REVIEW.md](m3_motion/inner_NATIVE_REVIEW.md)，它区分探针与最终全组证据，不将早期“待预览”记录冒作最新结果。原始 M1 关键姿态研究保留在 [POSES.md](analysis_poses/POSES.md)。

**最终 cross_beam 外壳轨道来自 [shell_cross_open_options.json](m3_motion/shell_cross_open_options.json) 的 C1，制作入口显式覆盖 `shell_motion.json` 中保留的旧 cross 轨道。** C1 保持六肢近段的关节根位置，只用旋转抬肢；整体 `shell_root` 在 1–3 秒仍上移 7 个模型单位，让身体升起。没有采用 C2 对上/中层肢根额外下移的方案。固定已确认的肢根使上层末端较参考截图偏高，近正面匹配相机也只是对源截图的假设；六肢扇形层次与小人暴露程度改善，不等于唯一原作深度解。

## 小人重定时与原生镜头约定

Docile 原片 4.8 秒，在 16 秒 `idle` 中放 3 周期，每周期 `16/3 = 5.333333…` 秒，播放速度为原片 **90%**（慢 10%，在用户允许范围内）。映射为 `t = k×16/3 + u/0.9`，`k=0,1,2`、`u` 为原片秒数；零基源帧 `f` 的 `u=f/25`。详见 [inner_time_map.csv](m3_motion/inner_time_map.csv)。

Anxious 以 1:1 时间嵌入 `walk`。原片 7.96 秒与 0 秒手臂姿态不同，8 秒循环闭合不自动证明视觉无跳动；必须检查接缝。Fourside 的全部 50 帧按 `t=1+f/25` 保留，最后源帧落在 2.96 秒并保持到 3 秒；快速转折没有改成匀速旋转。25 Hz 来源到 20 Hz 运行时采样仍有差异，12.5 fps 预览更不能覆盖每个快速转折。

外壳对照使用固定正交镜头。cross_beam 全景为容纳上扬肢端，整段固定使用正交高度 96、target Y=26；没有逐帧缩放取景或修改模型来藏裁切。小人孤立对照的相机随 `shell_root` 变换，**只剥离壳体的整体动作**；不会追随 `inner_root` 把小人自身起伏、转身和前后仰抵消掉。相机与模型不镜像源图，渲染时间与变换误差记在各批原生 `render_evidence.json`。这是便于对照的测量约定，不声称恢复原作相机。

最终内层冠轴修正保留头部原 pivot、几何和 **0 个 head position 改动**，但为保持头身连接并恢复脸中心几何代理，调整了整人 `inner_root` position，最大修正长 **2.226836 个未缩放模型单位**，不能称“只改头旋转”。冠根绝对位置残差仍最高约 **44.38 px**；Fourside 45 的过长下伸已收回，但模型底部仍比源低 **21 px**。最终全 50 帧、9 页原生并排已逐页复核，未发现新的明确冠轴反向或头身断连；脸中心代理的数学零误差仍不等于真实眼纹或整个轮廓吻合。

## 紫色材质与已知面部差距

新的 [m3_material/atlas.png](m3_material/atlas.png) 保持 512×512 布局，M2 历史图集未改。六个星窗取自原 711×711 图的登记窗口，不整图缩小；源渲染 `(295,224)` 的 `[172,3,193,255]` 是紫色色相锚点。逐像素保留 `V=max(R,G,B)`、alpha、黑点掩码与星点尺寸，全部非黑星图像素转入参考紫色系列。体内小人使用源渲染实测粉紫色带，顶部条使用较暗紫色带；这是用户授权的调色，不称 Undressed 原色。

全模型 fullbright 让材质不受场景光照压暗。紫色星点与近白/粉白眼牙保持不同亮度层级；眼牙原采样 RGBA 未改。**fullbright 不产生投射光或 bloom。44×44 `glow_mask_raw` 原始 RGBA 完整保留在图集中，但当前未被自定义 shader 消费，不能称遮罩已接入光效。** 未新增公共 shader、粒子、光环、地面拖痕或半透明烟雾方案。

小人脸部仍有明确差距：现有头部 UV 不包含参考的紫色 L 形与白色条纹，粉紫色带也压缩了原灰纹对比。原贴图未分配角落存在特殊材质像素，但缺少其到面部的可靠映射；原渲染脸边界又受辉光和遮挡影响。依本轮决定保留已确认 UV，不镜像拼脸、不用 GIF 编画、不增加面部几何。详见 [FACE_UV_REVIEW.md](m3_material/FACE_UV_REVIEW.md) 与 [原像素证据](m3_material/face_forensics_closeup.png)。

顶部条使用静态原渲染的较暗紫色；与有强辉光的 Docile/Anxious GIF 对照时仍显得更暗，本次没有用 bloom 掩盖这项差别。小人每条手臂/腿只有一根运动骨，无法独立复现肘、膝、踝的弯曲；首批完整对照中，Anxious 源帧 35/39 的前伸细条长度和遮挡、Docile 的脚尖及前后腿轮廓仍有适配差距，不能称逐像素吻合。

取色/转换：[MATERIAL_NOTES.md](m3_material/MATERIAL_NOTES.md)、[material_transform.json](m3_material/material_transform.json)、[material_audit.json](m3_material/material_audit.json)。原作素材版权属于 Mojang；本项目非商业，与 Mojang 无关联。

## 音效登记与特效接口

[heart_of_ender_audio.py](../heart_of_ender_audio.py) 已提供 `SOUNDS`、`CUES`、`ENTER_CUES`，可在 M5 薄生成器中直接传入；归档 47 个 HE 声音文件。**本阶段没有写入运行时音效 JSON 或 mcfunction，没有在游戏中听过。** GIF 无音轨，动作声音落点是作者推断：

| 动作 | 已登记声音时间 |
|---|---|
| idle / walk 进入 | 分别为外壳低吼、小人低吟 |
| walk | 0–7 秒每整数秒一个落脚声；交替三肢只放一声 |
| mortar | 1.2 秒 |
| cross_beam | 1.0 秒 |
| sink / rise | 分别 0.4 / 0.2 秒 |
| death 进入 | 消散声 |

弹体落地/爆炸等效果声音仅归档，未绑定到不存在的特效；环境长音未循环叠加。声音时点检查使用 20 Hz，循环片段要求 `t < length`，避免把声音放到不会烘焙的闭合端帧。

嘴部与光束预留坐标见 [m3_motion/sockets.json](m3_motion/sockets.json)，已刷新并核对对应本报告主模型哈希。坐标为 Java 模型空间：+Y 向上、面向 −Z，未乘 `model_scale`，不是 Minecraft 方块世界坐标。静态原始点为：

| 名称 | 所属骨骼 | 未摆姿模型点 `(x,y,z)` |
|---|---|---|
| mouth_center | shell_head | `(0,26,-10.808)` |
| cross_beam_center | inner_body | `(0,-1.25,2.9)` |
| cross_north | inner_body | `(0,-1.25,2.025)` |
| cross_east | inner_body | `(1.4,-1.25,2.9)` |
| cross_south | inner_body | `(0,-1.25,3.775)` |
| cross_west | inner_body | `(-1.4,-1.25,2.9)` |

嘴部点跟随上颅的闭嘴缝，张口后是上唇出口候选，不是上下颚动态中点。四侧光束点只是小人躯干表面接口，原作准确发射骨与扫描方向未知；JSON 另存各指定时刻的摆姿坐标和骨骼前向，供未来特效使用。本阶段未生成任何特效。

## 验证结果与待用户判断的差距

[validation.json](m3_motion/validation.json) 对本报告模型 **78 项通过、0 错误**：7 clips / **3401 keys / 21 parts**。检查覆盖纯数字 rotation/position、支持的插值、循环首尾矩阵、居中部件范围、发光标记、图集一致性、声音时点和 20 Hz **内存**烘焙。保存模型的元素、UV、骨骼 rest 与 accepted R2 逐值一致；内嵌图集与磁盘 M3 图集逐RGBA一致。

| 对应证据 | 最后版本结果 |
|---|---|
| 主工程 | `15abda3ad7c372907257c581bac8822dc7f98feebb7c98e9ca538773fbfe1f4d` |
| M3 图集 PNG | `1a5796f592a75b46adc8710f6bc9661a6c47c15330a26a7903f89e7e394d81da` |
| 冻结内层轨道 | `dd35064ce1bc61a7a349a8f15d4a81d83dc12ab908d1dae2e56aed8de08a3696` |
| 254 张关键图的原生/公共管线骨矩阵最大误差 | `7.407150350857705e-6`，涉及保存后时间精度；不是像素还原误差 |
| 512 张连续图的原生/公共管线骨矩阵最大误差 | `1.7763568394002505e-14` |
| 全部原生 PNG | **766 个文件 SHA-256 逐个匹配**各批渲染登记 |
| 对应关系 | authoring / validation / sockets / 两批 render 与 B、E 候选 evidence 均指向本报告主模型 |
| 审阅页链接 | HTML 本地链接缺失 **0** |

证据：[authoring_audit.json](m3_motion/authoring_audit.json)、[关键图 render_evidence](m3_preview/render_evidence.json)、[连续图 render_evidence](m3_preview/continuous/render_evidence.json)、[delivery_check.json](m3_motion/delivery_check.json)。原生帧使用保存模型、原生 Animation timeline 与 WebGL；仅将对应材质设为 fullbright，没有后期染紫、bloom、形变或重绘。

七段动作的正/侧/背页已实际查看，未见背面材质突然换区、眼牙跑到背面或彩色条纹。766 张原生图另做全量像素筛查：不透明低绿色通道的星点类像素中，未检出非紫色残留；未检出绿色主导像素。眼牙亮形保持，未见 UV 沿表面滑动。数值与材质检查通过不等于动作轮廓完全还原。

仍需用户依据并排图判断：

1. **B 肢遮挡歧义。** 源 `idle f015 / 0.6 s` 的可见方向与端点约束冲突。[B 肢同版两方案原生对照](m3_preview/b_f015_options/comparison.png) 中，主稿优先末端位置，另一候选优先可见朝向；烟雾下肢段归属/连接仍不唯一，不能用端点拟合误差声称姿态问题已解决。
2. **Fourside 肢体隐藏深度。** 第 43/44/45 帧按各自可见端点拟合，暂用 E1 向后收肢；第 42 帧对应不清，保留原态。[第45帧 E1 / E2 同版原生对照](m3_preview/f45_options/comparison.png) 已刷新，E1 为主稿，E2 朝相机侧仅作候选；43/44 的 E2 仍仅为数据候选。**E1 是制作选择，尚非用户验收。** 方向、冠根位置、脚底残差及脸纹差距见上文和最新内层复核。
3. **cross_beam 的源截图适配。** [近正面 C1 对照](m3_preview/boards/cross_reference_view_01.png) 可见六肢向外上扬、小人暴露程度改善；固定肢根使上层末端偏高，近正面镜头是假设，源半透明/烟雾也未复现。未选择 C2 肢根下移，不以改变已确认连接来强追单张截图。
4. **循环和刚体适配。** Anxious 原末帧与初帧并非同姿，数学首尾闭合不保证接缝速度平滑；Docile 脚尖/腿轮廓、Anxious 35/39 前伸臂与遮挡仍有差异。没有把关节数限制用作掩盖可见错误的理由，也没有称全部关键姿态逐像素还原。

预览地面使用顶面固定在同一 `ground_y`、向下深 200 单位的不透明体积，模拟地块遮挡，不修改模型动作。已检查更新后的 sink/rise/death 主对照及正侧背页：sink 终态完全沉没；rise 从地面下升起；death 3.8 秒小人在四个方向均被地面遮挡，外壳仍保留可见。这个结果属于原生预览，不能代替实际 Minecraft 地面与载体运行时检查。

未运行 `_tools/rp_build.sh`、`_tools/build.sh`、`_tools/rp_validate.py` 或 `_tools/server_test.py`；这些属于 M5。未做真实游戏内的资源包效果、音效、载体移除后的 item_display 清理测试。**未在真实游戏内看过，未同步测试实例。** 绑定对象与游戏体型大小尚未确定；本阶段未改现有生物、AI、血量、技能或掉落，未改公共 `display_mob.py`、`DEVIL_SMOKE`、`STRIDE=4` 或 `rpg.hurt`，未提交、未推送、未切分支，未进入 M4/M5。
