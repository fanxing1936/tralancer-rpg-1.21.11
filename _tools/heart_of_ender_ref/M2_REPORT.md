# Heart of Ender — M2 静态模型阶段报告

> 历史阶段记录：用户于 2026-11-04 选择 **R2**、确认静态造型并授权 M3 动作和参考紫色调色。已验收 R2 基线另存于 [m3_motion/accepted_R2.bbmodel](m3_motion/accepted_R2.bbmodel)，后续主文件会包含 M3 动作。本报告下文的“待确认/R0/未接入紫色”等是 M2 交付时的状态，不能用于判断当前主文件。R1/R2 对照已完成，见 [端盖对照](m2_endcaps/endcap_comparison.png)；M2 接口坐标已登记于 [m2_sockets.json](m2_sockets.json)。

日期：2026-11-04。仓库：`D:\agent\claude\github-create\tralancer-rpg-1.21.11`。

**当前交付是待用户确认的静态稿，不是完成版 Boss。** 主文件保留 R0 端盖姿态；R1、R2 是供并排选择的候选，不自动替换主文件。尚未开始 M3 动作、M4 Arch-Visage 模型与动作或 M5 构建接入。原样 44×44 发光遮罩已经存入图集，但紫色材质尚未接入或验证。

## 1. 当前主文件与审阅入口

| 内容 | 文件 / 状态 |
|---|---|
| 正式静态工程、后续事实来源 | [heart_of_ender.bbmodel](heart_of_ender.bbmodel) |
| 原渲染与正式 Blockbench 模型并排 | [m2_preview/reference_comparison.png](m2_preview/reference_comparison.png) |
| 正面、侧面、四分之三、背面 | [m2_preview/four_views.png](m2_preview/four_views.png) |
| 原生渲染记录、相机与来源哈希 | [m2_preview/render_evidence.json](m2_preview/render_evidence.json) |
| 结构复核和已知偏差 | [m2_geometry/STATIC_REVIEW.md](m2_geometry/STATIC_REVIEW.md) |
| 最新星点密度复核 | [m2_atlas/STAR_DENSITY_REVIEW.md](m2_atlas/STAR_DENSITY_REVIEW.md) |
| 端盖候选及原图标注 | [m2_geometry/endcap_options.json](m2_geometry/endcap_options.json)、[原图量测标注](m2_geometry/endcap_source_measurements.png) |

主模型当前为 **46 个 cube、26 个骨骼组、21 个展示部件、1 张 512×512 图集、0 段动画**。主文件 SHA-256：

`8b4738fdd60f8bab39d16716e5414c0b34ee23219a9c8d33b6906f7fc81942ed`

正式 preview、静态 validator 和导出审计均引用这个版本。结构复核文档最初审阅的是 41 个 cube 的首轮稿；后续星点密度调整将长表面细分为 46 个 cube，没有因此新增展示部件。最新星点复核和最终数值校验覆盖当前 46 个 cube 的版本，不能把首轮的元素统计当作当前统计。

## 2. 结构实现与推断边界

| 构成 | 展示部件 | 本次处理 |
|---|---:|---|
| 上颅、下颚、躯干 | 3 | 头与身紧接，下颚独立，保留后续张口动作所需层级 |
| 六条肢体，各近段与远段 | 12 | 两段方柱；没有追加缺乏证据的手掌、手指或脚掌 |
| 体内小人的头、身、双臂、双腿 | 6 | 独立骨架；顶部竖条、鼻合入头，短足合入腿 |
| 眼、前牙、侧牙发光骨骼 | 0 个额外部件 | 刚性合入头/颚对应 part，共三根发光子骨 |
| **合计** | **21** | 用户已接受约 21 个展示部件；增加 cube 不等于增加 item_display |

几何与相机的量测依据见 [GEOMETRY_STUDY.md](m2_geometry/GEOMETRY_STUDY.md) 和 [geometry_spec.json](m2_geometry/geometry_spec.json)。采用 Java 模型空间：+y 向上，面向 −z；前脸为 north，参考三分之四视角可见侧脸为 west。侧/背检查没有发现导入造成的前后倒装或新增断肢，但隐藏根点、肢段深度、背部形状仍是多种可能解中的工作假设。

原作下躯干和肢根有烟雾、渐隐。本稿采用不依赖半透明的几何：上躯干实心，下段保留后壁与窄侧缘，在前方留出体内小人的可见开口。**这是一种不透明渲染适配，不是已证实的原作内部拓扑。** 小人右侧在参考视角仍被壳体/肢体遮窄，背面也有明显遮挡；肢根因此显得比烟雾原作更硬、更连续。没有把这些差异写成“已还原”。

体内小人的贴图像素来源已核验，但部位语义和面朝向不等于已恢复原始 geometry。头和顶部竖条的候选较有依据；鼻为中等置信；身体中低置信；手臂、腿、脚的 UV 分配仍为低置信工作方案。灰细条由左右肢有意复用，暗蓝脚部岛仍可能属于其他小部件。具体证据与替代方案见 [ARCH_UV_NOTES.md](m2_atlas/ARCH_UV_NOTES.md)，不能仅凭图集边界正确就宣称小人的 UV 已精确复刻。

游戏体型和绑定对象仍未决定。`model_scale=null`；验证器只临时使用 1.0 做归一化矩阵检查，`seat=0` 也只是研究坐标。正/侧/背预览自动取景，不能拿图中尺寸当作游戏中的方块高度。本次没有改任何现有生物的模型或行为。

## 3. 原始图集、发光遮罩与颜色差异

图集为 [m2_atlas/atlas.png](m2_atlas/atlas.png)，完整来源矩形、采样方式及哈希见 [atlas_regions.json](m2_atlas/atlas_regions.json)。

- 身体使用原 711×711 星空素材的六个不同 128×128 窗口，图集内保持 1:1 原 RGBA，没有整张缩小或烘焙紫色。每个模型面的区域和原图坐标登记在 [m2_face_uv.json](m2_face_uv.json)。
- 头/颚目前使用 **4.5 源像素/模型单位**，躯干/肢体为 **13**。长表面通过细分满足窗口范围，外形和展示部件数不因此改变。头与躯干的星点尺寸/密度更接近参考；D 横肢局部仍偏稀，不能称星点分布逐点一致。量测阈值和限制均保留在星点复核报告中。
- 64×64 `T_ArchIllagerUndressed.png` 完整原样入图集。`T_ArchIllagerUndressed_S.png` 只作阴影贴图存档，不作为发光层。
- 眼与牙亮形从原始渲染的登记四边形进行最近邻采样，保留像素的 RGB/alpha 不变，剔除背景。没有补画图案或编造颜色。其五个提取区域均已独立重算采样来源，但四边形拟合不是官方 UV 解包结果；柔光外缘没有被完整保留。

**用户确认的第二张贴图是 44×44 `MCD_Heart_of_Ender_(glow_effect_texture).png`。它的完整原始 RGBA 已原样放入 `glow_mask_raw` 区域，没有调色、二值化或修改透明度；本稿没有把它作为白色半透明大矩形贴在模型上，也没有建立独立遮罩 shader。** 原样入图集只证明数据保存正确，不证明遮罩已参与运行时材质。

原星图是彩色 RGB 星点，小人本体含灰、蓝、金、绿等原色。当前预览仍呈现这些颜色，**实际紫色星空材质与粉紫小人效果尚未接入或验证**。`light_emission:15` 不会自动把白图或这些原色变紫。M5 若处理，应只在本模型的生成流程中实现兼容的专用材质/染色处理，再做游戏内验证；当前没有实现，更不能把保持原色当成紫色材质已经支持。

正式 Blockbench 预览只为眼、前牙和侧牙三个表面关闭材质面阴影，说明记录在 `render_evidence.json`。没有添加 bloom、改变曝光、给全身重着色或修改图集 alpha。这是静态审阅方式，不是 Minecraft 半透明排序或发光材质的测试结果。

## 4. 端盖 R0 / R1 / R2：仍需视觉选择

端盖滚转不能仅凭低对比截图猜定。以下角度是绕相应远段自身长轴的相对变化，候选 JSON 已换算为完整骨骼 rest Euler 替换值；不能把它们再逐项加到欧拉角上。

| 方案 | A 左上 | B 左中 | E 右前下 | 状态 |
|---|---:|---:|---:|---|
| R0 | 0° | 0° | 0° | 当前主文件，保留现状基线 |
| R1 | +12.204° | +15° | −7° | 中间角度候选，未采纳 |
| R2 | +12.204° | +29.060° | −14° | 边线方向优先候选，未采纳 |

A 有可量到的端盖轮廓；B 的内部边线低对比，拟合仍有约 10.79px RMS 偏差；E 即使以 −14° 匹配下沿斜率，其下沿位置仍偏低约 10px。仅改滚转不能同时解决 E 的边线方向与位置，不能按误差数字替用户选方案。候选保持中心线、立方体、pivot 与部件数，不是新的完整结构方案。

R1/R2 的正式 Blockbench 并排渲染正在由主作者生成；在路径、版本和图像实际核对前，本报告不把候选图登记为已完成成果，也不声称候选已通过主文件的 215 项验证。用户确认前，主文件保持 R0，M3 不开始。

## 5. 已做验证与没有做的验证

[m2_validation.json](m2_validation.json) 的最终结果为 **215 项检查通过，0 错误、0 警告，21 个 part**。这次在真实保存的 `.bbmodel` 上执行，不是只验证生成前的 Python 数据。

| 检查 | 证据与结论 |
|---|---|
| 静态工程格式 | 单张内嵌 PNG、0 段动画；骨骼/元素/outliner 唯一且对应完整 |
| 管线兼容 | 调用现有 `display_mob.py` 的只读加载、part_model 和矩阵函数；各 part 居中坐标满足 −16…32，合并骨旋转合法 |
| 发光骨与成本 | 三根发光子骨正确合并，未增加展示部件 |
| UV 可追踪 | **261/261 个非空面**与映射中的元素、归属骨、实际 UV、登记区域及源坐标吻合，无漏项或重复 |
| 原始像素 | 六星窗、原 44 遮罩、小人本体共八个 source_copy 区域逐 RGBA 一致；五个透视提取区域独立重算也一致 |
| 内嵌图集 | 实际 `.bbmodel` 解码的图集与外部 atlas RGBA 一致 |
| Blockbench 导出 | [m2_authoring_audit.json](m2_authoring_audit.json)：按 UUID 比较 772 个关键字段；非数字/层级一致，数值容差 5.01×10⁻⁶，实测最大差异约 5×10⁻⁶，来自五位小数导出 |
| 渲染版本 | 正式 preview、validator、导出审计均对应本报告开头的主模型 SHA |

以上验证没有运行 `_tools/build.sh`、`_tools/rp_build.sh`、`_tools/rp_validate.py` 或 `_tools/server_test.py`，也没有验证载体移除后的展示部件清理。M2 尚未生成调试召唤入口或运行时动画。**未在真实游戏内看过**；没有向 `D:\minecraft\PCL启动器\.minecraft\versions\1.21.11-Fabric 0.19.3` 的资源包或存档数据包目录同步。构建、加载、清理与实际渲染均留在 M5，不能用静态校验通过代替这些结论。

## 6. 事实来源与复现方法

事实来源是 `heart_of_ender.bbmodel`。本稿由研究规格与来源图集生成后，实际送入 Blockbench MCP 导入、由 Blockbench 导出，再从保存文件重新打开渲染；当前没有无法由脚本重现的额外手工模型修改。Blockbench 的导出小数精度和自动元数据以保存工程为准，不承诺不同软件版本产生完全相同的文件容器字节。

| 工具 | 职责 |
|---|---|
| `_tools/heart_of_ender_geometry_study.py` | 几何、相机规格和研究图；`--endcaps` 生成端盖候选量测 |
| `_tools/heart_of_ender_atlas.py` | 单图集、像素来源记录、小人候选 UV 研究 |
| `_tools/heart_of_ender_geo.py` | 生成静态候选数据，经 Blockbench 导出正式 `.bbmodel` 并审计 |
| `_tools/heart_of_ender_blockbench.py` | 本机已安装 Blockbench MCP 的连接封装 |
| `_tools/heart_of_ender_preview.py` | 读取保存的 `.bbmodel`，用 Blockbench 原生 WebGL 渲染对照图 |
| `_tools/heart_of_ender_validate.py` | 读取正式工程，输出静态与像素来源校验 JSON，不调用整包 build |

以下命令从仓库根目录执行；需要已安装的 Python、Pillow、NumPy，以及运行中的 Blockbench MCP。本次 MCP 端口为 **52907**，重现时应使用实际已配置且可连接的端口，不是要求修改其他服务。

```powershell
Set-Location 'D:\agent\claude\github-create\tralancer-rpg-1.21.11'
python -X utf8 _tools/heart_of_ender_geometry_study.py
python -X utf8 _tools/heart_of_ender_atlas.py
python -X utf8 _tools/heart_of_ender_geo.py --port 52907 --replace-static
python -X utf8 _tools/heart_of_ender_preview.py --port 52907
python -X utf8 _tools/heart_of_ender_validate.py
```

这是**重建当前静态稿**的流程，会重写本任务对应研究产物及静态工程，不是日常数据包构建步骤。`--replace-static` 只用于确认没有需要保留的手改之后；生成器发现已有动画时会拒绝覆盖。后续若在 Blockbench 手工改过或进入 M3，应继续以 `.bbmodel` 为事实来源，并更新复现说明，不能误跑 M2 重建流程抹掉后续工作。

只重新检查已有工程无需重建：

```powershell
python -X utf8 _tools/heart_of_ender_validate.py
```

## 7. 后续发射点坐标

嘴部中心、嘴部光束出口以及体内小人的十字光束发射点，**待主作者从最终静态工程提供并标明所属骨骼、坐标空间和朝向**。本报告没有从截图猜填坐标。游戏体型、载体座高尚未决定，因此也不提前填写世界坐标或格数偏移。该项补齐后仍只是后续接口定位，不包含光束、弹体或其他特效实现。

## 8. 来源与署名

原作角色、原始贴图、渲染图、动图和音效来自 Minecraft Dungeons，版权属于 **Mojang Studios**。本项目非商业，与 Mojang 无关联。参考整理来源为 [Minecraft Wiki：Heart of Ender](https://minecraft.wiki/w/Dungeons:Heart_of_Ender) 及 [Arch-Illager Gallery](https://minecraft.wiki/w/Dungeons:Arch-Illager/Gallery)；逐文件来源、字节数和存档哈希见 [SOURCES.md](SOURCES.md)。当前几何与动作研究中的推断不代表 Mojang 官方模型或实现。
