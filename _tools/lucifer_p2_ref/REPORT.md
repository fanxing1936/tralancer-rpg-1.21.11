# 路西法二阶段：动作、音效、材质与游戏接入

本交付只覆盖 Jungle Abomination 二阶段。一阶段由独立会话维护。用户已确认检查点 A，并授权完成 B 的全部动作、音效、微光、脉动和外观接入；原先 A 的报告与静态工程保留在 `validation/checkpoint_a_approved/`。

入口文件是 [lucifer_p2.bbmodel](lucifer_p2.bbmodel)。[18段并排动画](animations_preview/index.html)、[游戏内截图](game_preview/phase50_peak.png)、[动作时长与误差](ANIMATIONS.md)、[音效通知表](SOUNDS.md)、[重建及调试命令](REBUILD.md) 可直接查看。

## 模型与同比例尺寸

本体提取24个包、135个对象，失败0；源网格1012顶点、514三角形、40根原骨。成品102个显示部件、214个cube（11个实体箱体、203个零厚度面）、150个组。用户已允许超过20部件，未牺牲原骨运动以凑预算。召唤藤蔓/花等附加资产列入源清单，没有新增召唤实体。

所有UV由源网格换算；原512² PNG未缩放覆盖。对非矩形UV、扭曲面和三角cutout进行源数据驱动转换；四片眼睑跨骨三角形保留精确源顶点映射。封闭不透明原箱体才合并外表面，开放/含alpha孔洞的箱体继续保留双面薄片。不承诺相机进入实心箱体后的内部面等价。

共同尺度已按当前一期成品校准：一期包含帽子但排除独立武器的高度为44.47583139202386 BB，整体定为2.4格；216个原骷髅顶点与native的 `diag(-16,16,-16)` 对应误差为0。两阶段统一为 **0.008633902683354115 blocks/cm**；二阶段内部0.0192 BB/cm、外部 `model_scale=7.194918902795097`。待机首帧源几何829.5085cm，对应 **7.1619格高**。首帧高度沿用早期CUE参考的t=0几何数据，没有用旧全clip包络冒充最终UE时间验收。这不是碰撞箱，也不独立证明原游戏Actor额外缩放。

这次校准只修改外部尺度与两项metadata；elements、groups、outliner、18段animations、textures逐字段不变，所有atlas PNG逐字节不变。独立authoring scale10保留原有栅格和关键帧精度。完整证据见 [尺度审计](validation/scale_alignment/APPLIED.md)。此前约10格估算及真实客户端截图使用校准前scale10，保留其原作用域。

原四视角基线IoU：正面0.999719411、侧面0.999359951、背面0.999706165、四分之三0.999611249，均大于0.97。它们是相同相机、可见alpha轮廓的基础表面对照；不是最终HDR发光的Blender逐像素等价测试。最终分层在原生Blockbench及Minecraft客户端另有实际证据。旧Blender共面透明层黑条问题不被改写成已经修复的原样Blender渲染结果。

## 18段动作与眼睑

15个AnimSequence、3个AnimComposite全部转为原名小写 `animation.<clip>`。idle/walk排首，其余保留捕获provider顺序；原拼写Sucessful/Unsucessful保留。三段ProjectileAttack composite按原0…1.13、1.13…2.8、2.8…3.3333333秒精确裁剪。UE4.22端点时间与最短路径NLERP经过源代码核对；未使用导出器错误N/L采样或SLERP。

源40骨使用稀疏数字position/rotation轨道，绝对欧拉减rest并unwrap；源scale通道为空。四片跨骨眼睑新增绝对affine轨道，运行时用两四元数/SVD组成显示变换，支持零scale的闭眼。管线扩展显式opt-in；同一时刻仍只播放一段clip。

最终尺度下逐一重放全部 **18段、787个输出tick、80,274个实际实体目标**。覆盖1012个源顶点，另单列1712个Java箱体角点。真实JOML1.10.8按Minecraft float32、两次NBT解码、五位SNBT、稀疏保持及脉动额外重载组成变换。

| 指标 | 最终最大误差（视觉像素） | 位置 |
|---|---:|---|
| 源40骨世界pivot与posed_matrix | 0.048847594 | vineattacksucessful，tick1，J_R_arm_08 |
| 序列化的16个可观测原owner pivot | 0.043237711 | vulnerablegetup，tick16，J_L_Wrist |
| 源对应实际Java几何顶点 | 0.097027864 | idle，tick42，p2_j_l_wrist_082，源顶点645 |
| 四片眼睑原三角顶点 | 0.000551702 | walk，tick40，p2_head_095，源顶点957 |
| 静态投影/箱体恢复 | 0.001039406 | jaw，源顶点943 |
| 任意额外同值quaternion解码后的保守总界 | **0.097054241 < 0.1** | 精确枚举全部目标的归一化轨道，最多2状态/周期2 |

24根源骨没有独立显示实体，不能把序列化实体指标冒称直接测到全部40骨。以上是每个输出tick的目标几何验证，不是连续时间、客户端tick间插值、整个GPU姿态栈或原引擎逐像素相等保证。[完整数值、每段时长、最大误差骨/时刻](validation/runtime_numeric_scaled/FINAL_NUMERIC_ACCEPTANCE.md) 和 [18段关键姿态/GIF](animations_preview/index.html) 分别提供数值与视觉证据。

## 微光与10秒脉动

该实例原Jungle BasePass的DXBC及uniform绑定独立确证了 `_E.B`：

```text
E(t) = 0.60000002384*A + S.b*10*pulse(t)*C²
C = [1,0.13600000739,0.98611998558]
pulse(t) = max(sin(2π*t*0.1)/3+2,0)
```

完整4096²单图集包含参考、非发光/发光互补alpha层及辅助数据象限 `[19,237,原B,255]`；只有原8个含额外发光的部件更新相位。最终Java模型统一light_emission0，由严格marker与数据guard识别的paper item_display core shader计算普通光照、基础0.6微光和HDR粉色脉动，再经过明确ACES+sRGB与原版fog。不产生世界照明或Bloom；曝光映射为目标呈现选择，不声称完整复刻UE后处理。

服务器共享200tick时钟，20TPS时10秒周期；可保持所有Boss同相。连续正弦相对最小值的单tick采样误差上界0.6284%，墙钟时间随TPS变化。源游戏初始相位未恢复。

实际GL33验证1040个启用样本覆盖全部200相位和亮/暗光照，最大RGBA误差9.06283e-7；288个普通输入/marker碰撞样本与原版差0。Blockbench实际HDR framebuffer覆盖149像素×3时刻，最大误差3.81470e-6、峰值19.61466；18段动画1735时刻、20820个GPU眼顶点检查通过，包含非单位Canvas和奇异闭眼。

P1组合shader在私有RP执行finalize后也实际编译/链接/绘制通过，剥除P1块后与纯P2逐字节相同，普通分支像素差0。P2 atlas没有P1识别像素，944个UV角点在sprite内部。此项未声称P1专属像素正确或组合shader已经载入Minecraft；见 [共存审计](validation/combined_shader/AUDIT.md)。

## 音效与外观接入

46个原Ogg全保留原字节，注册38个事件，25个启用的原时间通知绑定帧；30条通知逐项校验，两个idle SoundCue因原volume0静音。音量、有效wave池和Walk vocal 50%空分支保留；随机pitch、Unreal并发/衰减/no-repeat未完全移植。Flower LOOP按具名原通知映射并每87ticks重复，状态退出取消未来重放，已发出4.326秒样本自然结束，避免全局stopsound误伤其他Boss。Projectile没有源声音通知，未猜测发射声。

3个音乐事件只供手动debug，Start/Loop是30秒Wiki预览。2个藤蔓补充声音只注册，不建召唤物。失败藤蔓Foley在源资产里实际引用成功声，保留原异常。逐通知tick、证据与限制见 [SOUNDS.md](SOUNDS.md)。

载体为 `rpg_dm_lord=1` 的卫道士；外部tag `rpg.lu.phase2` 只读，`rpg.lu`/`rpg.lu2`是各自已穿好标记。dress先通过optional P1 undress回调恢复一期拥有的主手备份，再清理旧显示；退出二期清理自己的部件后通过optional P1 dress回调返回。直接入口和正常tick顺序均可用，载体UUID精确挂载，marker/外部display及另一Boss不受换装清理影响。自然死亡fallback与显式death声去重。

18段均提供 `rpg:lucifer_p2/play/<原名小写>`，另有玩家附近选取的debug/play与38个手动试听入口。load/tick在构建里接入；late隐藏位于command/tick_end之后。二阶段战斗条件、伤害技能和召唤物按原范围保留给后续逻辑，不虚构技能伤害帧表。

## 验证与实际游戏范围

| 最终检查 | 结果 | 证据 |
|---|---|---|
| 冻结源完整build | 退出0，153.74秒 | [build_results](validation/final_build/build_results.json) |
| 完整rp_build及rp_validate | 退出0，61.09/0.27秒 | [资源校验](validation/final_build/rp_validate.log) |
| 全新生成DP真实服务器 | **25/25通过**，函数加载/解析错误0；服务器副本8270文件与构建输出逐项相同，无generated临时补丁 | [runtime_results](validation/final_build/runtime_results.json) |
| 项目内最终自有文件更新 | 1698个P2文件；102模型/787帧与数值输入一致；保留现有组合shader及P1 dress/tick原字节 | [integration_manifest](validation/integration_final/integration_manifest.json) |
| 项目内资源检查 | no problems found（1451 files） | [最终日志](validation/integration_final/rp_validate.stdout.txt) |
| 完整构建包 | DP8270文件、RP1306文件，逐ZIP CRC检查通过 | [数据包](release/rpg-datapack-1.21.11.zip) / [资源包](release/rpg-resourcepack-1.21.11.zip) / [哈希](release/release_manifest.json) |

25项包括：只读phase信号、无重复穿装、102部件计数、多载体独立、双向换装、主手备份恢复、直接dress入口、外部marker/display及旋转保留、载体移除、实际十分钟消散倒计时分支、实际驱魔完成分支、花循环在idle退出。消散用原倒计时设1进入实际分支，没有等十分钟墙钟；驱魔验证完成分支，不冒称玩家走完整仪式。

完整包是构建开始时的冻结快照。构建后一期独立会话只改了laugh的interpolation_duration从1到0；该差异、冻结SHA及README文档更新原样归档，P2模型/runtime始终稳定。未覆盖一期源码或输出，未声称验证最新一期视觉；此差异不改变通过验证的二期生命周期接口。[漂移分类](validation/final_build/source_drift_classified.json)。

共享display_mob默认路径回归：10个真实既有配置、87渲染部件+2held、4291个完整生成文件逐字节一致，359冻结输入不变。P1是后来独立mesh renderer，不使用此cube默认路径；其双向回调另验。旧生成器的性能瓶颈vehicle.NBT每部件重复序列化全部乘客已改为原生vehicle类型判断；此前两只NoAI Boss共204显示部件、200tick的隔离基准由187.58降到16.31ms/tick。这是受控旧尺度测试，不等同完整战斗客户端TPS，也不冒充最终尺度新的性能测量。

现有原版Java1.21.11在新gameDir/单人世界实际加载完整RP，8192²物品atlas内正确显示二期。午夜同姿态F2峰/谷原图有795个选定模型像素在峰值变亮、0变暗，最大RGB差[3,20,4]；实际walk与相位循环已观察。没有录成连续视频，也没有逐一实机播放18段。截图使用校准前scale10；最终7.1949的几何/序列化结果另有上述验证，未声称重新拍过最终大小。

客户端shader、texture/model装载错误为0；完整日志保留初次unknown passenger警告、旧性能版本落后tick、离线Realms401及已移除的私有helper tick-freeze权限错误。它们不被隐去或描述成“所有日志无警告”。第三方shader/Iris/OptiFine兼容、UE原曝光/Bloom和完整战斗AI不在通过范围内。[实际客户端报告](game_preview/CLIENT_VALIDATION.md) 保留全部边界。

未修改Dungeons安装目录，未同步用户PCL实例，未提交、推送或切换分支。重建脚本与来源清单见 [REBUILD.md](REBUILD.md)、[SOURCES.md](SOURCES.md)、`delivery_manifest.json`。原作素材版权归Mojang所有；本项目非商业，与Mojang无关联。
