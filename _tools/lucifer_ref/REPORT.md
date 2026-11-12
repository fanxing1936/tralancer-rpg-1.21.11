# 路西法第一阶段：独立左眼发光、武器同色与九段动作

2026-11-08：模型、九段动作和正式函数接入完成。当前模型 SHA-256 `1b31cc7009b5fb8065641c46a8f2d6de725dc8106b11486aac9de2fd7374a530`，canonical与separate副本相同。原生606姿态、保存重开、构建与资源校验，以及实际独立服务器59项回归通过。尚未在真实Minecraft客户端审查画面，未同步用户游玩实例。

## 当前交付

- [lucifer.bbmodel](lucifer.bbmodel)、[审阅副本](separate/lucifer_verdant.bbmodel)。11 Mesh、22骨，原几何、UV、权重与4张source PNG保留；另加第5张独立眼发光PNG。
- [原生证据包](validation/eye_palette_slash/README.md)、[哈希索引](validation/eye_palette_slash/NATIVE_VALIDATION_INDEX.json)、[审阅页](VERDANT_REVIEW.html)、[Claude交接单](CLAUDE_HANDOFF.md)。
- [九动作动图与361帧](previews/visual_revision/manifest.json)、[九姿态总览](previews/visual_revision/nine_clips_contact_sheet.jpg)、[独立发光图层](lucifer_left_eye_emissive.png)。
- 旧9c16八动作模型及核验已[归档](validation/verified_clearance/README.md)，14931来源包[保持封存](verdant_animation_sources/README.md)，不伪写旧证据。

## 配色与发光

衣料34绿色源色映射到蛇矛主绿#22724E色度，10棕色映射到蛇矛深棕#4A3A3A色度，保持线性亮度与0.4暗色系数，灰金属保持。映射只在材质执行，原PNG不改。原辅助贴图白色发光保持。

角色自身左眼为-X，前脸源UV像素(13,12)、(14,12)，只有Head对应前脸使用；原生Mesh UV代码确认GPU=(u/64,1-v/32)。新增256×128独立RGBA发光层，核心#A855F7，校准linear E=[0.21756917,0.07220355,2.12951747]，外围halo_strength=0.14；嘴、右眼和限制范围外alpha为0。保留深度测试，无穿透眼片。bind、idle0/1秒正面射线未被帽衣遮挡，此检查不代表任意视角可见。

需加载[材质插件](native/lucifer_original_material.js)和[源精度插件](native/lucifer_source_precision.js)。Blockbench工作室灯光+ACES；眼周微光来自独立发光图层，未声称实现UE完整Bloom/specular/场景光照。最终配置见[saved_material_config](validation/eye_palette_slash/saved_material_config.json)。

## 动作

| 名称 | 秒 | 循环 |
| --- | --- | --- |
| `animation.idle` | 6.208334 | 是 |
| `animation.walk` | 0.791667 | 是 |
| `animation.attack` | 0.900000 | 否 |
| `animation.strong` | 1.116667 | 否 |
| `animation.cast` | 0.550000 | 否 |
| `animation.laugh` | 3.291667 | 否 |
| `animation.stun` | 1.625000 | 否 |
| `animation.rise` | 2.400000 | 否 |
| `animation.slash` | 1.050000 | 否 |

原八段来源与适配见历史来源包，attack/laugh已有110key修正保留。新增slash为用户要求的1.05秒横砍，1484key；独立clip，不添加伤害、不改战斗数值，玩法由后续技能控制器决定。

## 核验与边界

606 authored poses原生矩阵重放PASS，最大旋转误差约9.3259e-15、位置误差3.10205e-11 Java像素；保存重开包含9动作、5PNG、eye配置和材质启用状态回读PASS。实际保存文件检查和限定slash核验见新证据包。旧8段200Hz/attack-laugh1000Hz的Body/Head SAT结论仅适用于其原范围，不扩张为袍帽/四肢/场景或任意连续时间证明。

## Java与技能交接状态

正式入口为 `../add_lucifer_model.py`，支持当前原始Mesh/Armature。运行实现位于 `../lucifer_mesh_runtime/`，11个显示部件、2.4格绑定高度、seat=2、key=`lucifer_lord`、tag=`rpg.lu`、score前缀=`rpg_lu`。原始三角面通过原平面矩形代理与片元裁剪绘制，保留源UV；未把原网格近似替换成旧63方块候选。

两套构建脚本都在利维坦后生成P1，再运行已有P2生成器，最后合并共享着色器。P2原分支保留，未知着色器拒绝覆盖。7个第一柱技能只追加有守护条件的外观调用，原命令字节前缀保持；不改变伤害、冷却、掉落或出手tick。新slash仅提供 `rpg:lucifer_lord/play/slash`，未擅自新增伤害技能。

原空手载体保持空手，蛇矛只显示于独立部件；原本持物则完整复制、隐藏、恢复，攻击属性与掉落概率保持。P1 tick在P2之前，late隐身在tick_end后；重复dress幂等，束缚采用 `rpg.exorcism.bound` 并保持stun末帧。

完整构建通过后，又对最终播放策略定向再生成并执行服务器回归。隔离构建资源校验1306文件通过；当前项目范围生成后的资源校验1451文件通过。实际独立1.21.11服务器59/59通过，未发现数据包加载/解析错误，覆盖九动作入口、双载体、持物/属性、移动/束缚、真实阶段往返、死亡移除、寿命到期边界和驱魔成功清理。寿命测试校验12000初始化及降至1后的真实到期路径，并非挂机十分钟。详见[构建证据](validation/runtime_integration/BUILD_VALIDATION_INDEX.json)及[当前服务器证据](validation/runtime_integration/server/SERVER_VALIDATION_INDEX.md)。

**大笑的游戏播放采用20Hz同步逐帧。** 原作有约133°/33ms的转矛，实际Java平滑插值会造成躯干/头部穿模。当前只对laugh的全部11部件使用duration=0，其余八段保持duration=1；不改原生关键帧、时长或战斗逻辑。实际生成帧的200/1000Hz有限检查均无Body/Head碰撞，握点误差约1.03e-7格。此策略有50ms保持和明显快速姿势跳变，不宣称连续曲线逐渲染帧等价；[播放策略与取舍](validation/runtime_integration/laugh_playback/README.md)保留完整证据。

当前项目存在另一会话的P2并行更新。范围生成审计记录P1实际写入路径，保留并单列P2漂移，不宣称整个实时工作树与隔离测试包逐字相同。当前P1自有643个DP文件、48个RP文件及生成源与最终测试版本逐字一致。公共 `display_mob.py`、蛇矛生成器未修改。真实客户端的光照、边缘与声音播放仍待画面验收。

原模型版权归Mojang及原权利方，本项目非商业，与Mojang无关联。
