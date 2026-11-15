# Jungle Abomination 二阶段源资产清单

仅完成本体源资产提取与数值清点，未制作 bbmodel 动作，未接入战斗或资源包。游戏目录只读。

24 个指定包，135 个对象，0 个失败；15 个 AnimSequence、3 个 AnimComposite。工具固定 CUE4Parse 1.2.2 / Conversion 1.2.1，UE 4.22。

## 动画：实际 provider 索引快照顺序

`provider_order_snapshot.json` 在本次挂载后、任何排序之前记录 provider.Files.Values。以下按实际 ordinal 排列；不是候选文件的字母序，也不声称原作作者编排顺序。并发挂载可能使下次运行的 ordinal 不同。

| provider ordinal | 名称 | 类型 | 帧数 | 时长（秒） |
|---:|---|---|---:|---:|
| 90191 | jungleAbomination_Attack | AnimSequence | 60 | 2.4583333 |
| 90193 | jungleAbomination_death | AnimSequence | 40 | 1.625 |
| 90195 | jungleAbomination_fall | AnimSequence | 9 | 0.33333334 |
| 90197 | jungleAbomination_idle | AnimSequence | 179 | 7.4166665 |
| 90199 | jungleAbomination_land | AnimSequence | 72 | 2.9583333 |
| 90201 | jungleAbomination_ProjectileAttack | AnimSequence | 81 | 3.3333333 |
| 90203 | jungleAbomination_ProjectileAttack_End | AnimComposite | 复合；引用源81帧 | 0.5333333 |
| 90205 | jungleAbomination_ProjectileAttack_Loop | AnimComposite | 复合；引用源81帧 | 1.67 |
| 90207 | jungleAbomination_ProjectileAttack_Start | AnimComposite | 复合；引用源81帧 | 1.13 |
| 90209 | jungleAbomination_summon | AnimSequence | 44 | 1.7916666 |
| 90211 | jungleAbomination_vineAttack | AnimSequence | 46 | 1.875 |
| 90213 | jungleAbomination_vineAttackIdle | AnimSequence | 24 | 0.9583333 |
| 90215 | jungleAbomination_vineAttackSucessful | AnimSequence | 45 | 1.8333334 |
| 90217 | jungleAbomination_vineAttackUnsucessful | AnimSequence | 37 | 1.5 |
| 90219 | jungleAbomination_vulnerableFall | AnimSequence | 42 | 1.7083334 |
| 90221 | jungleAbomination_vulnerableGetUp | AnimSequence | 93 | 3.8333333 |
| 90223 | jungleAbomination_vulnerableStunCycle | AnimSequence | 22 | 0.875 |
| 90225 | jungleAbomination_walk | AnimSequence | 59 | 2.4166667 |

每段源路径、PSA、稀疏 tracks JSON、每骨通道键数、完整哈希均在 `inventory_phase2.json`。

**复合动画注意：** Start / Loop / End 都引用 ProjectileAttack 的片段；官方 CUE4Parse PSA 导出仍包含完整引用序列，不能把 PSA 时长当成复合片段时长。最终 clip 必须按下表源 segment 裁剪：

| 复合资产 | 源起点 | 源终点 | 播放倍率 | 循环数 |
|---|---:|---:|---:|---:|
| jungleAbomination_ProjectileAttack_End | 2.8 | 3.3333333 | 1.0 | 1 |
| jungleAbomination_ProjectileAttack_Loop | 1.13 | 2.8 | 1.0 | 1 |
| jungleAbomination_ProjectileAttack_Start | 0.0 | 1.13 | 1.0 | 1 |

建议最终清单仅把原 idle 和 walk 提到最前，其余保持本次 provider 索引顺序，保留原名与原始拼写。

## 骨架与缩放轨道

原骨架 40 根，父子层级和原 pivot/TRS 见 JSON。所有动作的 scale 通道均为空；rest scale 与 1 最大差异仅 5.96e-8，属于浮点精度。

| 索引 | 原骨名 | 父索引 |
|---:|---|---:|
| 0 | J_Root | -1 |
| 1 | J_Spine | 0 |
| 2 | J_Spine_01 | 1 |
| 3 | J_Neck | 2 |
| 4 | J_Head | 3 |
| 5 | Head | 3 |
| 6 | J_leftEye | 5 |
| 7 | J_l_eyelidTop | 6 |
| 8 | J_l_eyelidBottom | 6 |
| 9 | J_rightEye | 5 |
| 10 | J_r_eyelidBottom | 9 |
| 11 | J_r_eyelidTop | 9 |
| 12 | J_Jaw_01 | 5 |
| 13 | Je_JawEnd | 12 |
| 14 | J_L_Clavicle | 2 |
| 15 | Je_L_Clavicle | 14 |
| 16 | J_L_Arm | 15 |
| 17 | J_L_Elbow | 16 |
| 18 | J_L_Wrist | 17 |
| 19 | J_R_Clavicle | 2 |
| 20 | Je_R_ClavicleEnd | 19 |
| 21 | J_R_arm_01 | 20 |
| 22 | J_R_arm_02 | 21 |
| 23 | J_R_arm_04 | 22 |
| 24 | J_R_arm_06 | 23 |
| 25 | J_R_arm_08 | 24 |
| 26 | J_flower1 | 2 |
| 27 | J_Petal_01 | 26 |
| 28 | J_PetalEnd_01 | 27 |
| 29 | J_Petal_03 | 26 |
| 30 | J_PetalEnd_03 | 29 |
| 31 | J_Petal_05 | 26 |
| 32 | J_PetalEnd_05 | 31 |
| 33 | J_Petal_07 | 26 |
| 34 | J_PetalEnd_07 | 33 |
| 35 | J_Pelvis | 1 |
| 36 | J_R_Leg | 35 |
| 37 | Je_R_Leg | 36 |
| 38 | J_L_Leg | 35 |
| 39 | Je_L_Leg | 38 |

## 源几何尺寸（厘米）

使用原 UE reference TRS、刚性权重和稀疏 idle 轨道做蒙皮。UE Z 为竖直方向；未添加 Blueprint 放置变换。以下属于源网格包络，不是“游戏中站立高度”。

| 姿态 | X 宽 | Y 深 | Z 高 |
|---|---:|---:|---:|
| 原始 rest | 820.113087 | 550.048864 | 1062.736368 |
| idle 第一帧 | 864.682332 | 1087.296091 | 829.508518 |
| idle 全段采样并集 | 937.865079 | 1166.646377 | 859.244637 |

idle 全段共 1433 个样本（每源帧间隔 1/8，含所有源帧及结束保持），这是采样包络，不是连续时间的解析极值保证。rest 往返蒙皮最大误差 1.61e-13 cm。

若另一会话最终按 Mossy 200 cm → 2.4 格定标：rest 高约 12.7528 格，idle 首帧约 9.9541 格，idle 全段采样包络约 10.3109 格。共同缩放仍待一阶段实际配置确定；这些数字均不是最终游戏身高。

## 本体与材质

网格 1012 个导出顶点、514 个三角形、40 骨；基础贴图与 `_E` 图均为 512×512。源材质双面、Masked，阈值 0.1。

`M_JungleAbomination` 的 Texture 参数绑定基础图，Specular 参数绑定 `_E` 多通道图。实例明确配置 EmissiveBPower=10、品红发光颜色与相关开关。

已额外导出 `Master_ModelMaterial` 的 59 个对象，确认 packed map 的 R/G/B/A 均被通道选择节点读取；但 cooker 剥离了最终 EmissiveColor 所引用的 Multiply_12 等连接节点，因此无法仅据现有元数据确定“哪个通道＝发光遮罩”。不能把 `_E` 全部非黑像素或整块身体都设为发光。详见 `material_channel_evidence.json`。

## 附带资产：仅清单，不并入 Boss

原 Boss 本体已经包含 J_flower1 / Petal 骨骼。没有搜到独立的 Boss 花网格；一般丛林装饰花只列为名称候选，不视为已证实的召唤物。

| 包路径 | 证据分类 |
|---|---|
| Dungeons/Content/Decor/Prefabs/DingyJungle/JunglePlant/rough_models/BP_Jungle_flower.uasset | Name-only flower search candidate; no Boss linkage established |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vineAttack.uasset | Direct dependency reference in a Boss package; listed only |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vineAttackIdle.uasset | Direct dependency reference in a Boss package; listed only |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vineAttackSucessful.uasset | Direct dependency reference in a Boss package; listed only |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vineAttackUnsucessful.uasset | Direct dependency reference in a Boss package; listed only |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbominationVine/Animations/AbominationVine.uasset | Boss-named vine directory; listed only, not exported into the Boss |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbominationVine/Animations/AbominationVine_Burst.uasset | Boss-named vine directory; listed only, not exported into the Boss |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbominationVine/Animations/AbominationVine_Death.uasset | Boss-named vine directory; listed only, not exported into the Boss |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbominationVine/Animations/AbominationVine_Idle.uasset | Boss-named vine directory; listed only, not exported into the Boss |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbominationVine/AnimBP_AbominationVine.uasset | Boss-named vine directory; listed only, not exported into the Boss |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbominationVine/BP_AbominationVineCharacter.uasset | Boss-named vine directory; listed only, not exported into the Boss |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbominationVine/M_AbominationVine.uasset | Boss-named vine directory; listed only, not exported into the Boss |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbominationVine/SK_Abomination_Vine.uasset | Boss-named vine directory; listed only, not exported into the Boss |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbominationVine/SK_Abomination_Vine_PhysicsAsset.uasset | Boss-named vine directory; listed only, not exported into the Boss |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbominationVine/SK_Abomination_Vine_Skeleton.uasset | Boss-named vine directory; listed only, not exported into the Boss |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbominationVine/T_Vine_Arm.uasset | Boss-named vine directory; listed only, not exported into the Boss |
| Dungeons/Content/Actors/Characters/Enemies/PoisonQuillVine/Animations/PoisonQuillVine_Firing.uasset | Direct dependency reference in a Boss package; listed only |
| Dungeons/Content/Actors/Characters/Enemies/PoisonQuillVine/BP_JungleAbominationPoisonProj.uasset | Direct dependency reference in a Boss package; listed only |
| Dungeons/Content/Actors/Characters/Enemies/Whisperer/Vine_Trap/PS_JungleArenaBubble.uasset | Direct dependency reference in a Boss package; listed only |
| Dungeons/Content/Components/Enchantments/JunglePoisonMelee/BP_JunglePoisonMelee.uasset | Direct dependency reference in a Boss package; listed only |
| Dungeons/Content/Decor/Prefabs/_BambooBluffDecor/P_VineSummon.uasset | Direct dependency reference in a Boss package; listed only |
| Dungeons/Content/Decor/Prefabs/DingyJungle/JunglePlant/rough_models/MI_jungle_plant_plantflower_variant.uasset | Name-only flower search candidate; no Boss linkage established |
| Dungeons/Content/Decor/Prefabs/DingyJungle/JunglePlant/rough_models/SM_jungleflower_variant.uasset | Name-only flower search candidate; no Boss linkage established |
| Dungeons/Content/Decor/Prefabs/DingyJungle/JunglePlant/rough_models/Plant_with_Flowers.uasset | Name-only flower search candidate; no Boss linkage established |
| Dungeons/Content/Decor/Prefabs/DingyJungle/JunglePlant/MI_JungleFlower_Leafy.uasset | Name-only flower search candidate; no Boss linkage established |
| Dungeons/Content/Decor/Prefabs/DingyJungle/JunglePlant/rough_models/MI_jungle_plant_flowerbush1.uasset | Name-only flower search candidate; no Boss linkage established |
| Dungeons/Content/Decor/Prefabs/DingyJungle/JunglePlant/rough_models/MI_jungle_plant_plantflower.uasset | Name-only flower search candidate; no Boss linkage established |
| Dungeons/Content/Decor/Prefabs/DingyJungle/JunglePlant/rough_models/SM_jungleflower_2.uasset | Name-only flower search candidate; no Boss linkage established |
| Dungeons/Content/Decor/Prefabs/DingyJungle/JunglePlant/rough_models/T_Plant_with_Flowers.uasset | Name-only flower search candidate; no Boss linkage established |
| Dungeons/Content/Decor/Prefabs/DingyJungle/JunglePlant/SM_JungleFlower_Leafy.uasset | Name-only flower search candidate; no Boss linkage established |
| Dungeons/Content/Decor/Prefabs/DingyJungle/JunglePlant/T_JungleFlower_Leafy.uasset | Name-only flower search candidate; no Boss linkage established |
| Dungeons/Content/Decor/Prefabs/DingyJungle/JunglePlant/T_JungleFlower_Leafy_Emissive.uasset | Name-only flower search candidate; no Boss linkage established |

## 全部指定源包及导出

| 游戏内路径 | 结果 |
|---|---|
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_Attack.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_Attack.psa |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_death.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_death.psa |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_fall.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_fall.psa |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_idle.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_idle.psa |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_land.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_land.psa |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_ProjectileAttack.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_ProjectileAttack.psa |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_ProjectileAttack_End.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_ProjectileAttack_End.psa |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_ProjectileAttack_Loop.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_ProjectileAttack_Loop.psa |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_ProjectileAttack_Start.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_ProjectileAttack_Start.psa |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_summon.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_summon.psa |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vineAttack.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vineAttack.psa |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vineAttackIdle.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vineAttackIdle.psa |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vineAttackSucessful.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vineAttackSucessful.psa |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vineAttackUnsucessful.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vineAttackUnsucessful.psa |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vulnerableFall.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vulnerableFall.psa |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vulnerableGetUp.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vulnerableGetUp.psa |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vulnerableStunCycle.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vulnerableStunCycle.psa |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_walk.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_walk.psa |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/BP_JungleAbominationCharacter.uasset | 83 个对象的 UObject / 元数据 JSON |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/M_JungleAbomination.uasset | 1 个对象的 UObject / 元数据 JSON |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/SK_Abomination_02.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/SK_Abomination_02.glb |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/SK_Abomination_02_Skeleton.uasset | 2 个对象的 UObject / 元数据 JSON |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/T_Jungle_Abomination_E_M6.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons\Content\Actors\Characters\Enemies\JungleAbomination\T_Jungle_Abomination_E_M6.png |
| Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/T_Jungle_Abomination_M6.uasset | D:\agent\dungeons_extract\phase2_full\assets\Dungeons\Content\Actors\Characters\Enemies\JungleAbomination\T_Jungle_Abomination_M6.png |

素材版权归 Mojang 所有。本项目非商业，与 Mojang 无关联。
