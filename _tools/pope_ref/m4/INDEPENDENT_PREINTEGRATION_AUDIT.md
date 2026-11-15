# 教皇 M4 独立接入前审计

检查结果：通过。这是只读配置和素材审计，不是构建或游戏验证。

- 当前模型 SHA-256：`a419cc8dce1e796113a02c362ad184faea3bf09d5c908b26ac81e963babc624a`。
- 眼神 B；12 个部件、44 个元素、170 个有效面；权杖发光骨独立。
- model_scale = 1.3593362401199063；预期卫道士乘客座高 2.0 格，仍待运行时测量。
- 九段动作名称、顺序、时长与 M3 一致。
- 17 组声音、39 个 OGG 文件；59 项原始素材哈希与 M1 一致。
- 525 个挂点采样各含 staff_tip、right_hand、left_hand、head_top；挂点引用当前模型哈希。

## 接入注意事项

1. attack、summon、cast 的出手 cue 分别为 0.50 / 0.65 / 0.90 秒；建议非循环动作每刻采样，避免 0.65 秒被量化到晚一刻。
2. 共用管线在 enter 时立即播放 f0；非循环末帧播放后的下一刻自动回 idle。whirlwind 收拢在 7.00 秒，玩法须在回 idle 前交接/移除载体。
3. 0.9 秒瞬移只有旋转/位移，不包含透明度或缩放；动画完成不会自行隐藏。
4. 原音效尾声不截断。mirror_in 约 3.315 秒、mirror_out 约 2.201 秒、whirlwind 约 13.033 秒，长于动作片段；动画切换不会停止这些声音。
5. 不把 whirlwind 绑定到载体死亡回调；magic_impact 与三组 intro 音效只注册，不能自动假定命中或剧情时点。
6. 维度范围修正：没有空间限定的 @e 会跨维度选择；仅写 execute in 不足以限定范围。教皇自己的三个维度分发必须同时给载体与孤儿扫描加 distance=0..，否则每实体会被推进三次。初次静态审计漏掉此点，已由运行时测试发现。
7. summon 只设置 max_health/Health=1000 与承载展示所需字段；其他战斗属性留给玩法。载体隐身应以教皇 tick_late 在 rpg:command/tick_end 后恢复。
8. 运行时 hurt 绑定沿用 rpg.hurt 门控；不得为了声音改写通用受伤逻辑。

## 只读发现的玩法时序差异

当前 `_tools/add_pope_fight.py` 在本次审计时的值如下。这属于玩法会话的文件，本次未修改。

| 项目 | 模型 | 当前玩法 | 影响 |
|---|---:|---:|---|
| attack 出手 | 10 tick | 10 tick | 一致 |
| attack 结束 | 25 tick | 24 tick | 玩法早 1 tick 切 idle |
| summon 出手 | 13 tick | 20 tick | 玩法比模型出手晚 7 tick |
| cast 出手/长度 | 18 / 50 tick | 收回/加护在 40 tick 完成并切 idle | 事件时刻与动作尚未对齐，末段截断 |
| appear 长度 | 36 tick | 40 tick | 模型先回 idle 再等玩法结束 |
| teleport in/out | 各 18 tick | 各 18 tick | 时长一致；隐现效果未做 |
| whirlwind 收拢 | 140 tick | 60 tick 移除载体，70 tick 转入末影之心 | 当前玩法会截去模型后 4 秒和最终收拢 |

素材、管线及受保护玩法文件基线哈希详见 `independent_preintegration_audit.json`。本审计未运行构建、服务器或客户端；未在真实游戏内看过。

## 薄配置完成后的独立复审

`add_pope_model.py` 的 10 项配置/范围检查全部通过。摘要见 `independent_generator_audit.json`。

- 所有部件、glow、model_scale、seat、九段顺序与 M3 一致。idle 每 4 tick，其余每 tick 采样；出手声音恰在 10 / 13 / 18 tick。
- M3 sounds/cues/enter_cues 直接读取，不重复维护副本。hurt 沿用共用门控；无死亡回调。ambient=0.006 是本项目 M4 配置选择，不宣称还原原作频率。
- 三维度分发仅写在教皇 tick 包装中；late-hook 在 command/tick_end 后恢复载体隐身。未添加 AI、技能、粒子或伤害逻辑。
- build.sh 顺序为 tower_wraith → pope_model → 后续模型 → pope_fight；rp_build.sh 紧跟 tower_guard。
- display_mob.py、opt_runtime_hotpaths.py、add_pope_fight.py 以及 59 项原素材均与本审计基线哈希相同。
- 上述玩法时序差异仍存在，未越界修改。专用服务器/构建检查由主会话另行执行，本复审不替代它们。

## 三维度选择器修正后的复审

初次静态审计未发现没有空间限定的 `@e` 会跨维度选取实体；独立运行时测试发现三倍动画推进。已保留旧审计为 `independent_generator_audit_attempt1.json`，不能将它当作最终运行时通过证据。

最新生成器只在教皇自己的 `tick_dimension` 与 `tick_late` 中补 `distance=0..`。逐条检查：载体存在性/遍历、孤儿存在性/删除共 4 个选择器，late-hook 共 3 个，7 个全部具备空间范围。共用管线、热路径与玩法脚本哈希仍不变，模型哈希不变。最新静态审计共 12 项通过；最终逐刻运行时结果由独立测试报告提供。
