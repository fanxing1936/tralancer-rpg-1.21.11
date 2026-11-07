# Heart of Ender 与 Arch-Visage 最终交付

> 本文记录首轮完整交付的冻结结果。后续按用户要求，将 Arch-Visage 头部统一为主模型外形；最新版本、并排图和本轮验证见 [末影面容同头版](../arch_visage_ref/head_match_v1/index.html)。本轮保留已安装体型，未把其他会话的体型或玩法改动混入同步；下文旧模型哈希及测试数字按当时版本理解。

本次交付包含两个可编辑 `.bbmodel`、全部指定动作、来源归档、原音效、并排对照、薄生成器与独立调试入口。未绑定或替换现有生物，没有玩法、AI、血量、掉落、光束、弹体、拖痕或光环粒子。绑定对象和正式 Boss 体型仍留给后续玩法任务；调试比例采用 `model_scale=1`。

**未在真实游戏内看过本次最终版本。** 离线图片、Blockbench 读写与真实服务端检查分别提供证据，不能用构建成功代替视觉验收。客户端透明排序、音效听感和最终体型尚无实机结论。

## 模型与对照入口

| 内容 | 交付 |
|---|---|
| Heart of Ender 主模型 | [heart_of_ender.bbmodel](heart_of_ender.bbmodel) |
| Heart of Ender 动作 | [254 姿态、52 页对照](final_material/motion_review/index.html)；[关键姿态总览](final_material/motion_review/overview.png) |
| 最终材质与小人眉眼 | [材质报告](final_material/MATERIAL_REPORT.md)；[图库原像素核对](gallery_followup/pose_analysis/FACE_UV_CANDIDATE.md) |
| Arch-Visage 主模型 | [arch_visage.bbmodel](../arch_visage_ref/arch_visage.bbmodel) |
| Arch-Visage 动作 | [122 个源时刻对照与连续预览](../arch_visage_ref/index.html)；[关键姿态并排](../arch_visage_ref/key_pose_comparison.png)；[正侧背和四分之三](../arch_visage_ref/four_views.png) |
| 结构与源动作研究 | [结构测量表](analysis_structure/STRUCTURE.md)；[源动作关键姿态表](analysis_poses/POSES.md) |

`.bbmodel` 是事实来源，单图集内嵌 base64。HE 保留用户确认的 R2 结构：六肢各两段，加身/头/颚3部件和小人6部件，共 **21 个 item_display**；超出16的原因是保留这些独立运动，数量此前已经用户接受。最终51元素、26骨骼、7动作、3401关键帧。Arch-Visage 为 **5 个 item_display**：上壳、下颚、眼光、上口光、下口光，共11元素、6骨骼、3动作、988关键帧。

## 动作证据

| 模型 / clip | 时长与播放 | 原作证据和推断边界 |
|---|---|---|
| HE `idle` | 16秒循环 | **有动图**：完整400帧外壳参考；小人Docile 4.8秒重定时为每周期5.333秒，共3周期，原速90%（慢10%）。 |
| HE `walk` | 8秒循环 | 外壳**推断**：爬行截图 `Heart_of_ender_crawling_with_decal_trail.png` 与页面攻击间隙爬行文字；小人Anxious **有动图**，8秒原速。 |
| HE `mortar` | 4秒单次 | **推断**：页面后仰并吐出13弹体的说明及 `Minecraft-dungeons-heart-of-ender.jpg`；只做后仰张口，无弹体。 |
| HE `cross_beam` | 4秒单次 | 外壳**推断**：`Heart_of_Ender_prepare_to_shoot_beams.png`、`Heart_Of_Ender_laser.jpg` 和页面文字；小人Fourside **有动图**，2秒50帧嵌入1–3秒。顺时针扫描属于未来光束特效，未用外壳自转冒充。 |
| HE `sink` / `rise` | 2 / 2.4秒单次 | **推断**：页面Arch-Visages沉地说明与 `Heart_of_Ender_in_game.png`，仅position下沉/上升。 |
| HE `death` | 4秒单次 | **推断**：`Hero_kills_Heart_of_Ender_Arch-Illager_disappear.jpg` 与页面死亡说明，小人最后沉地消失，外壳保留。 |
| AV `spawn_attack` | 4.88秒单次 | **有动图**：以in_game版为准，92个存储帧按累计时间展开122个25fps采样；3.68秒后保留1.20秒空白。 |
| AV `idle` / `walk` | 各1秒循环 | 地下静态技术占位，为满足管线首序要求；不称原作待机/行走。召唤默认直接播放 `spawn_attack`。 |

运行时按20Hz烘焙，AV 4.88秒量化为98 ticks，即4.90秒，多0.02秒。其他时长均整tick。所有通道只有纯数字rotation/position，没有scale或Molang。同一clip已经合并外壳与小人动作。

有动图不代表取得原作三维骨骼；单视角隐藏深度、遮挡肢段和部分关节分配仍是推断。HE保留B肢归属、Fourside冠根最高约44.38px及第45帧底部约21px残差；小人静态UV不能覆盖动态眼神。AV仍有约10–25px局部边界和牙形差距。具体局限见 [HE动作报告](final_material/motion_review/MOTION_REVIEW_REPORT.md) 和 [AV报告](../arch_visage_ref/M4_REPORT.md)。

## 材质与声音

黑底星空来自711原图的登记窗口，以最近邻保留星点，不整张缩小；用户要求的紫星点、全身淡紫、眼周/嘴腔渐变沿最终材质保留。小人的眉眼从原64贴图分片映射，未找到官方三维模型。

44×44遮罩原RGBA完整保留；两个嘴腔面实际引用白色区 `[0,2,33,44)`，运行时乘原截图采样 `(255,211,255)`，没有把紫色烘焙回遮罩。图集、每面UV和原图取样位置见 [HE材质记录](final_material/material_changes.json) 与 [AV逐面来源](../arch_visage_ref/atlas_regions.json)。独立发光骨骼保留；HE的刚性发光子骨并入其所属展示部件，未增加实体。

这是全亮材质和局部alpha过渡，没有自定义屏幕bloom或动态照亮方块。最终预览采用CPU普通透明混合，无法证明真实客户端的透明批次排序正确。

HE归档13组47个原音效，运行时绑定8事件31原件；AV归档5组9个原件。进入动作和指定帧cue已生成。GIF没有音轨，音画落点属于推断；未给不存在的弹体/受伤玩法附加声音。原版 `stopsound` 无法按发声实体区分，同模型的暂停/切片可能停止附近另一实例的同事件声音，不影响另一种模型或其他怪。

## 调试命令

安装数据包与资源包并刷新后，在空地使用：

```mcfunction
/function rpg:heart_of_ender/debug/spawn
/function rpg:arch_visage/debug/spawn
```

HE可逐一播放：

```mcfunction
/function rpg:heart_of_ender/debug/anim/idle
/function rpg:heart_of_ender/debug/anim/walk
/function rpg:heart_of_ender/debug/anim/mortar
/function rpg:heart_of_ender/debug/anim/cross_beam
/function rpg:heart_of_ender/debug/anim/sink
/function rpg:heart_of_ender/debug/anim/rise
/function rpg:heart_of_ender/debug/anim/death
```

AV重新播放与通用控制：

```mcfunction
/function rpg:arch_visage/debug/anim/spawn_attack
/function rpg:heart_of_ender/debug/pause
/function rpg:heart_of_ender/debug/resume
/function rpg:heart_of_ender/debug/stop
/function rpg:heart_of_ender/debug/clear
/function rpg:heart_of_ender/debug/clear_all
/function rpg:arch_visage/debug/clear_all
```

`pause/resume/stop/clear` 两模型均有。玩家调用作用于本维32格内最近载体；由载体作为执行者调用则只作用于该实例。`stop` 回到idle，AV因此藏回地面。单次动作结束保持末姿，不自动触发玩法。`clear_all` 清理各维当前已加载的本模型实例；未声称能立即删除卸载区块的实体，重新加载后孤儿部件会被tick清理。

旧独立材质探针包保留，不自动卸载。如场内还有其静态样品，可在所在维度用 `/function he_material_probe:clear` 清掉，再测试正式调试入口。

## 嘴部与未来光束接口

Java模型空间，+Y向上、面向−Z。下表为未摆姿绝对模型点，不是骨骼相对坐标；接入时按对应骨骼变换，再乘 `model_scale/16` 并加调试载体放置偏移。

| HE接口 | 骨骼 | 未摆姿 `(x,y,z)` |
|---|---|---|
| mouth_center | shell_head | `(0,26,-10.808)` |
| cross_beam_center | inner_body | `(0,-1.25,2.9)` |
| cross_north | inner_body | `(0,-1.25,2.025)` |
| cross_east | inner_body | `(1.4,-1.25,2.9)` |
| cross_south | inner_body | `(0,-1.25,3.775)` |
| cross_west | inner_body | `(-1.4,-1.25,2.9)` |

嘴点随上颅，是上唇候选，不称张口后的动态中点。HE各时刻摆姿坐标和方向见 [sockets.json](final_material/sockets.json)；AV提供上下前唇动态中点和各关键时刻坐标，见 [AV sockets.json](../arch_visage_ref/sockets.json)。这些是后续接口候选，不是原作官方发射骨。未生成光束。

## 构建、验证与安装状态

本报告与最终生成使用以下源模型SHA-256：

| 模型 | SHA-256 |
|---|---|
| Heart of Ender | `ebc5d7cfc16cc5e3e5f3357b82c6c99da29b468faafffe8c9d7f4ab9f1a1e106` |
| Arch-Visage | `268d11878897ac78e6b527dfd970769c8711724614c790c3c82c9f4acf6f412f` |

| 验证 | 结果与证据 |
|---|---|
| `_tools/rp_build.sh` | 最终源快照完整运行通过，退出码0；[日志](build_validation/rp_build.log)。 |
| `_tools/build.sh` | 最终源快照完整运行通过，退出码0；[日志](build_validation/build.log)。 |
| `_tools/rp_validate.py resourcepack` | 通过，`no problems found`；[日志](build_validation/rp_validate.log)、[构建记录](build_validation/build_results.json)。 |
| 原 `_tools/server_test.py` | 使用真实1.21.11、完整最终数据包和独立世界；成功到达Done、数据包启用、无函数加载或命令错误。原脚本报告的4条complaints均为本地离线模式标准提示，完整保留，没有隐藏其它错误；[结果](build_validation/server_test_result.json)、[原始控制台](build_validation/server_test.log)。 |
| 原生Blockbench 5.2.2打开/另存 | 两模型通过；骨层级、动画、UV、图集RGBA与遮罩元数据语义保留，0未解释差异。编辑器把数值正规化至5位小数/数字字符串，最大差小于0.000005模型单位，未声称文件字节相同；[原生报告](final_validation/native_report.json)。 |
| 生成幂等与数值 | 35检查组通过；1855个输出文件两次逐字节相同；17768个部件姿态对源模型重烘焙，最大分量误差0.000005；40个已接入音频保持原字节，4个原遮罩面染色正确；[报告与复跑入口](m5_generated/validation.json)。 |
| 共享工作区保护 | 3830个无关文件逐字节不变，五份共享JSON的非本任务条目不变，公共管线与受保护文件不变；1850个本任务专属输出与完整快照逐字节一致；[报告](build_validation/workspace_integration.json)。 |
| 最终离线视觉交付 | HE254姿态/52页；AV122源时刻+4视图/21页，所有登记PNG哈希和链接通过。AV起身眼位错误已修，s005两眼中心偏差0.91/1.45px，s002提前露白像素为0；这不是全部视觉像素误差。 |

真实服务器运行时 **255/255检查通过，0函数/命令错误**：[中文验证报告](final_validation/FINAL_TEST_REPORT.md)、[机读结果](final_validation/server_report.json)。覆盖HE七段/AV三段动作、多点真实实体变换、循环/单次结束、暂停恢复、stop；每模型4实例分布在主世界/下界/末地，逐tick只推进一次，最近实例控制和owner归属正确。`clear` 与直接移除载体后的已加载部件残留均为0，HE清理不误删AV。66次帧读取共比较986个部件目标变换，最大误差约1.386×10⁻⁷；这是服务端保存的目标变换，不是客户端插值画面。

用户明确允许同步正式调试内容后，已完成 [最小增量安装计划](build_validation/install_plan.json)：新增1848文件、合并5份共享索引、删除0，不覆盖其它模型目录或pack.mcmeta。五份原索引已先备份；1853文件写后SHA全部正确，共享索引的其它条目逐值不变；再次规划为0项待写、1853项一致。[安装回执](build_validation/install_receipts/20261104T163152.911174Z.json)、[独立写后验证](build_validation/install_verification.json)。

实际目标为用户指定的 `D:\minecraft\PCL启动器\.minecraft\versions\1.21.11-Fabric 0.19.3`，资源包写入 `resourcepacks\tralancer-rpg`，数据包写入 `saves\新的世界\datapacks\tralancer-rpg`。未操作游戏界面、未替用户刷新当前世界；在游戏中执行 `/reload` 并按 `F3+T` 重载资源后再用上述命令测试。两个测试服务器与专属Blockbench实例均已正常退出。

## 文件边界与复现

正式入口为 [`add_heart_of_ender.py`](../add_heart_of_ender.py)、[`add_arch_visage.py`](../add_arch_visage.py)，已挂入两个原构建入口。模型制作脚本与历史素材研究保留；HE复现链和保护策略见 [最终材质报告](final_material/MATERIAL_REPORT.md)，AV复现链见其M4报告。原生Blockbench仅另存测试副本，未手工改动主模型；生成脚本可以复现最终内容。

构建脚本会清空整包目录，因此本次完整构建在任务专用源码快照中执行；共享工作区只由两个生成器更新本任务命名目录和五份必要索引，并核对无关文件。未改公共 `display_mob.py`、DEVIL_SMOKE、STRIDE=4 或 `rpg.hurt`，不提交 `_data_loot.json` / `_guide_sections.json` 的构建换行，不改 `_tools/michael_ref/`。未提交、未推送、未切分支。

原作素材版权属于 **Mojang Studios**；本项目非商业，与Mojang无关联。逐文件字节数、SHA-256前16位、来源页面和文件地址见 [HE SOURCES.md](SOURCES.md)、[补充图库 SOURCES.md](gallery_followup/SOURCES.md) 与 [AV SOURCES.md](../arch_visage_ref/SOURCES.md)，README已同步署名。没有下载Music。

交付前复核84个M1原件和4个补充图库原件，88个文件字节数与存档SHA全部一致：[原素材复核](build_validation/original_sources_check.json)。这些SHA是本地归档指纹，不是发行者提供的官方校验值。
