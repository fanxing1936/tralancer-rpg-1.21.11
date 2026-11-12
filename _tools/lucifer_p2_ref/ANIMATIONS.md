# 二阶段18段原作动作

15个AnimSequence与3个AnimComposite均已制作。名称为 `animation.<原名小写>`，idle/walk排首，其余保留提取provider枚举顺序（不是作者播放顺序）；Sucessful/Unsucessful原拼写不修正。

原时长不变；20Hz用ceil计算tick数。循环采样0..ceil−1；非循环采样含ceil，超原长度部分clamp，ceil+1回idle；death末帧保持。循环策略为目标控制器选择，未伪称所有源Loop端点强制相等。

| clip（省略 jungleabomination_） | 源秒 | ceil ticks | 结束策略 | 40骨最大px（骨@tick） | 序列化顶点最大px（源顶点@tick） |
|---|---:|---:|---|---|---|
| `idle` | 7.4166665 | 149 | 循环 | 0.00617528 (J_L_Wrist@17) | 0.09702786 (645@42) |
| `walk` | 2.4166667 | 49 | 循环 | 0.03218113 (Je_R_ClavicleEnd@24) | 0.05695416 (668@3) |
| `attack` | 2.4583333 | 50 | 第51tick回idle | 0.03645267 (Je_R_ClavicleEnd@8) | 0.05270458 (470@8) |
| `death` | 1.625 | 33 | 末帧保持 | 0.01438595 (J_R_arm_08@12) | 0.01611452 (514@16) |
| `fall` | 0.33333334 | 7 | 第8tick回idle | 0.01749798 (Je_L_Leg@2) | 0.03779622 (55@2) |
| `land` | 2.9583333 | 60 | 第61tick回idle | 0.02759128 (J_R_arm_08@2) | 0.05262628 (668@28) |
| `projectileattack` | 3.3333333 | 67 | 第68tick回idle | 0.02559123 (Je_JawEnd@11) | 0.02948043 (928@11) |
| `projectileattack_end` | 0.5333333 | 11 | 第12tick回idle | 0.00696499 (J_R_arm_08@7) | 0.00731880 (543@7) |
| `projectileattack_loop` | 1.67 | 34 | 循环 | 0.00184686 (J_r_eyelidTop@22) | 0.00749677 (871@17) |
| `projectileattack_start` | 1.13 | 23 | 第24tick回idle | 0.02559123 (Je_JawEnd@11) | 0.02948043 (928@11) |
| `summon` | 1.7916666 | 36 | 第37tick回idle | 0.03626720 (J_R_arm_06@31) | 0.04904018 (670@14) |
| `vineattack` | 1.875 | 38 | 第39tick回idle | 0.04165933 (J_R_arm_08@26) | 0.04235378 (533@26) |
| `vineattackidle` | 0.9583333 | 20 | 循环 | 0.04664971 (J_R_arm_08@3) | 0.04757672 (543@9) |
| `vineattacksucessful` | 1.8333334 | 37 | 第38tick回idle | 0.04884759 (J_R_arm_08@1) | 0.05468413 (5@33) |
| `vineattackunsucessful` | 1.5 | 30 | 第31tick回idle | 0.03699778 (J_R_arm_08@26) | 0.03777292 (534@26) |
| `vulnerablefall` | 1.7083334 | 35 | 第36tick回idle | 0.01806437 (J_L_Wrist@6) | 0.02937699 (670@2) |
| `vulnerablegetup` | 3.8333333 | 77 | 第78tick回idle | 0.04308030 (J_L_Wrist@16) | 0.05737299 (36@14) |
| `vulnerablestuncycle` | 0.875 | 18 | 循环 | 0.00848960 (J_l_eyelidTop@16) | 0.01179285 (481@16) |

ProjectileAttack三个Composite按源片段裁剪：Start 0…1.13秒，Loop 1.13…2.8秒，End 2.8…3.3333333秒，再将局部时间归零；没有复制整个动作冒充三段。

UE4.22的关键帧端点使用(N−1)/L时间关系与最短路径NLERP；未沿用导出器N/L或SLERP的错误时间基准。普通40骨保留源稀疏关键帧并按误差自适应补点，输出纯数字绝对欧拉减rest，处理角度展开。源scale通道为空；四片眼睑使用推导affine，明确作为管线扩展。

上述每段误差覆盖全部实际输出tick。40骨位置来自完整曲线/posed_matrix比较；运行实体只直接表示16个可观测原几何owner，另24根原骨没有独立entity。序列化指标使用真实模型JSON、mcfunction的float32/五位SNBT、真实JOML和稀疏保持后的实体状态，不把透明矩形角点冒称原顶点。详情见 `validation/runtime_numeric_scaled/`。

每段关键时刻原作/转换并排图、18个GIF及4组眼部特写见 `animations_preview/index.html`。图像为相同相机下离线几何/UV证据；不冒充18段游戏录像。素材内模态/UV与最终模型字段相同，最终共同缩放另有证据。

二阶段技能与伤害逻辑按任务范围未新增，因此没有虚构技能出手/伤害tick对照。每段都提供执行者为载体的 `rpg:lucifer_p2/play/<原名小写>`；音效真实源时刻见 `SOUNDS.md`，可供之后战斗逻辑接入。
