# 二阶段部件表

共 102 个 item_display、214 个 cube、40 根原骨。来源 `parts.json`，SHA-256 `6126a5f4c8af6c075112cacd24b8eb89b1382255e362a4de46c4f5303f19b007`。

8 个 glow 子骨仅标识原 `_E.B` 支持域，与父部件共用显示实体。最终 Java 元素使用 `light_emission=0, shade=true`，由 opt-in core shader统一计算基础微光和 HDR 粉色脉动，避免双重全亮。

四片原眼睑三角面由不同源骨驱动，使用源顶点推导的绝对 affine 轨道及两四元数/SVD 显示变换，包含奇异闭眼情况。没有把它们误归给单根骨。其余部件依原运动骨划分；超过20部件已获用户授权，未合并原骨运动以凑预算。

| 序号 | 部件 | 原几何归属骨 | 编译骨 | 含脉动层 | 跨骨眼睑 | cube |
|---|---|---|---|---|---|---:|
| 1 | `p2_j_l_elbow_000` | J_L_Elbow | `p2_j_l_elbow_000` | False | False | 4 |
| 2 | `p2_j_l_arm_001` | J_L_Arm | `p2_j_l_arm_001` | False | False | 4 |
| 3 | `p2_j_l_leg_002` | J_L_Leg | `p2_j_l_leg_002` | False | False | 1 |
| 4 | `p2_j_l_leg_003` | J_L_Leg | `p2_j_l_leg_003` | False | False | 1 |
| 5 | `p2_j_r_leg_004` | J_R_Leg | `p2_j_r_leg_004` | False | False | 1 |
| 6 | `p2_j_r_leg_005` | J_R_Leg | `p2_j_r_leg_005` | False | False | 1 |
| 7 | `p2_j_r_leg_006` | J_R_Leg | `p2_j_r_leg_006` | False | False | 1 |
| 8 | `p2_j_l_leg_007` | J_L_Leg | `p2_j_l_leg_007` | False | False | 1 |
| 9 | `p2_j_r_leg_008` | J_R_Leg | `p2_j_r_leg_008` | False | False | 1 |
| 10 | `p2_j_l_leg_009` | J_L_Leg | `p2_j_l_leg_009` | False | False | 1 |
| 11 | `p2_j_spine_010` | J_Spine | `p2_j_spine_010`, `p2_j_spine_010_glow` | True | False | 62 |
| 12 | `p2_j_l_elbow_011` | J_L_Elbow | `p2_j_l_elbow_011` | False | False | 1 |
| 13 | `p2_j_l_elbow_012` | J_L_Elbow | `p2_j_l_elbow_012` | False | False | 1 |
| 14 | `p2_j_spine_013` | J_Spine | `p2_j_spine_013` | False | False | 1 |
| 15 | `p2_j_spine_014` | J_Spine | `p2_j_spine_014` | False | False | 1 |
| 16 | `p2_j_spine_015` | J_Spine | `p2_j_spine_015` | False | False | 1 |
| 17 | `p2_j_spine_016` | J_Spine | `p2_j_spine_016` | False | False | 1 |
| 18 | `p2_j_spine_017` | J_Spine | `p2_j_spine_017` | False | False | 1 |
| 19 | `p2_j_spine_018` | J_Spine | `p2_j_spine_018` | False | False | 1 |
| 20 | `p2_j_spine_019` | J_Spine | `p2_j_spine_019` | False | False | 1 |
| 21 | `p2_j_spine_020` | J_Spine | `p2_j_spine_020` | False | False | 1 |
| 22 | `p2_head_021` | Head | `p2_head_021` | False | False | 1 |
| 23 | `p2_head_022` | Head | `p2_head_022` | False | False | 1 |
| 24 | `p2_head_023` | Head | `p2_head_023` | False | False | 1 |
| 25 | `p2_j_l_elbow_024` | J_L_Elbow | `p2_j_l_elbow_024` | False | False | 1 |
| 26 | `p2_j_l_arm_025` | J_L_Arm | `p2_j_l_arm_025` | False | False | 1 |
| 27 | `p2_j_l_arm_026` | J_L_Arm | `p2_j_l_arm_026` | False | False | 1 |
| 28 | `p2_j_l_arm_027` | J_L_Arm | `p2_j_l_arm_027` | False | False | 1 |
| 29 | `p2_j_l_arm_028` | J_L_Arm | `p2_j_l_arm_028` | False | False | 1 |
| 30 | `p2_j_l_arm_029` | J_L_Arm | `p2_j_l_arm_029` | False | False | 1 |
| 31 | `p2_j_l_arm_030` | J_L_Arm | `p2_j_l_arm_030` | False | False | 1 |
| 32 | `p2_j_l_arm_031` | J_L_Arm | `p2_j_l_arm_031` | False | False | 1 |
| 33 | `p2_j_l_arm_032` | J_L_Arm | `p2_j_l_arm_032` | False | False | 1 |
| 34 | `p2_j_l_elbow_033` | J_L_Elbow | `p2_j_l_elbow_033` | False | False | 1 |
| 35 | `p2_j_l_arm_034` | J_L_Arm | `p2_j_l_arm_034` | False | False | 1 |
| 36 | `p2_j_l_wrist_035` | J_L_Wrist | `p2_j_l_wrist_035` | False | False | 1 |
| 37 | `p2_j_l_wrist_036` | J_L_Wrist | `p2_j_l_wrist_036` | False | False | 1 |
| 38 | `p2_j_l_arm_037` | J_L_Arm | `p2_j_l_arm_037` | False | False | 1 |
| 39 | `p2_j_l_arm_038` | J_L_Arm | `p2_j_l_arm_038` | False | False | 1 |
| 40 | `p2_j_l_wrist_039` | J_L_Wrist | `p2_j_l_wrist_039` | False | False | 1 |
| 41 | `p2_j_l_wrist_040` | J_L_Wrist | `p2_j_l_wrist_040` | False | False | 1 |
| 42 | `p2_j_l_wrist_041` | J_L_Wrist | `p2_j_l_wrist_041` | False | False | 1 |
| 43 | `p2_j_l_wrist_042` | J_L_Wrist | `p2_j_l_wrist_042` | False | False | 1 |
| 44 | `p2_j_r_leg_043` | J_R_Leg | `p2_j_r_leg_043` | False | False | 1 |
| 45 | `p2_j_r_leg_044` | J_R_Leg | `p2_j_r_leg_044` | False | False | 1 |
| 46 | `p2_j_r_leg_045` | J_R_Leg | `p2_j_r_leg_045` | False | False | 1 |
| 47 | `p2_j_spine_046` | J_Spine | `p2_j_spine_046` | False | False | 1 |
| 48 | `p2_j_spine_047` | J_Spine | `p2_j_spine_047` | False | False | 1 |
| 49 | `p2_j_r_leg_048` | J_R_Leg | `p2_j_r_leg_048` | False | False | 1 |
| 50 | `p2_j_l_elbow_049` | J_L_Elbow | `p2_j_l_elbow_049` | False | False | 1 |
| 51 | `p2_j_l_elbow_050` | J_L_Elbow | `p2_j_l_elbow_050` | False | False | 1 |
| 52 | `p2_j_l_leg_051` | J_L_Leg | `p2_j_l_leg_051` | False | False | 1 |
| 53 | `p2_j_l_leg_052` | J_L_Leg | `p2_j_l_leg_052` | False | False | 1 |
| 54 | `p2_j_l_leg_053` | J_L_Leg | `p2_j_l_leg_053` | False | False | 1 |
| 55 | `p2_j_l_leg_054` | J_L_Leg | `p2_j_l_leg_054` | False | False | 1 |
| 56 | `p2_j_l_elbow_055` | J_L_Elbow | `p2_j_l_elbow_055` | False | False | 1 |
| 57 | `p2_j_r_arm_01_056` | J_R_arm_01 | `p2_j_r_arm_01_056` | False | False | 1 |
| 58 | `p2_j_r_arm_02_057` | J_R_arm_02 | `p2_j_r_arm_02_057` | False | False | 1 |
| 59 | `p2_j_r_leg_058` | J_R_Leg | `p2_j_r_leg_058` | False | False | 1 |
| 60 | `p2_j_r_arm_01_059` | J_R_arm_01 | `p2_j_r_arm_01_059` | False | False | 6 |
| 61 | `p2_j_r_arm_02_060` | J_R_arm_02 | `p2_j_r_arm_02_060` | False | False | 1 |
| 62 | `p2_j_r_arm_02_061` | J_R_arm_02 | `p2_j_r_arm_02_061` | False | False | 1 |
| 63 | `p2_j_r_arm_02_062` | J_R_arm_02 | `p2_j_r_arm_02_062` | False | False | 1 |
| 64 | `p2_j_r_arm_02_063` | J_R_arm_02 | `p2_j_r_arm_02_063` | False | False | 1 |
| 65 | `p2_j_r_arm_01_064` | J_R_arm_01 | `p2_j_r_arm_01_064` | False | False | 1 |
| 66 | `p2_j_r_arm_01_065` | J_R_arm_01 | `p2_j_r_arm_01_065` | False | False | 1 |
| 67 | `p2_j_r_arm_01_066` | J_R_arm_01 | `p2_j_r_arm_01_066` | False | False | 1 |
| 68 | `p2_j_r_arm_01_067` | J_R_arm_01 | `p2_j_r_arm_01_067` | False | False | 1 |
| 69 | `p2_j_r_arm_01_068` | J_R_arm_01 | `p2_j_r_arm_01_068` | False | False | 1 |
| 70 | `p2_head_069` | Head | `p2_head_069`, `p2_head_069_glow` | True | False | 11 |
| 71 | `p2_head_070` | Head | `p2_head_070` | False | False | 1 |
| 72 | `p2_head_071` | Head | `p2_head_071` | False | False | 1 |
| 73 | `p2_head_072` | Head | `p2_head_072` | False | False | 1 |
| 74 | `p2_head_073` | Head | `p2_head_073` | False | False | 1 |
| 75 | `p2_j_l_arm_074` | J_L_Arm | `p2_j_l_arm_074` | False | False | 6 |
| 76 | `p2_j_l_elbow_075` | J_L_Elbow | `p2_j_l_elbow_075` | False | False | 1 |
| 77 | `p2_j_l_leg_076` | J_L_Leg | `p2_j_l_leg_076` | False | False | 1 |
| 78 | `p2_j_r_leg_077` | J_R_Leg | `p2_j_r_leg_077` | False | False | 1 |
| 79 | `p2_head_078` | Head | `p2_head_078` | False | False | 1 |
| 80 | `p2_head_079` | Head | `p2_head_079` | False | False | 1 |
| 81 | `p2_j_r_arm_04_080` | J_R_arm_04 | `p2_j_r_arm_04_080` | False | False | 1 |
| 82 | `p2_j_r_arm_06_081` | J_R_arm_06 | `p2_j_r_arm_06_081` | False | False | 1 |
| 83 | `p2_j_l_wrist_082` | J_L_Wrist | `p2_j_l_wrist_082` | False | False | 8 |
| 84 | `p2_j_l_wrist_083` | J_L_Wrist | `p2_j_l_wrist_083` | False | False | 7 |
| 85 | `p2_j_l_wrist_084` | J_L_Wrist | `p2_j_l_wrist_084` | False | False | 1 |
| 86 | `p2_j_r_leg_085` | J_R_Leg | `p2_j_r_leg_085` | False | False | 1 |
| 87 | `p2_j_petal_01_086` | J_Petal_01 | `p2_j_petal_01_086` | False | False | 1 |
| 88 | `p2_j_spine_087` | J_Spine | `p2_j_spine_087`, `p2_j_spine_087_glow` | True | False | 4 |
| 89 | `p2_j_petal_05_088` | J_Petal_05 | `p2_j_petal_05_088` | False | False | 1 |
| 90 | `p2_j_petal_03_089` | J_Petal_03 | `p2_j_petal_03_089` | False | False | 1 |
| 91 | `p2_j_jaw_01_090` | J_Jaw_01 | `p2_j_jaw_01_090`, `p2_j_jaw_01_090_glow` | True | False | 5 |
| 92 | `p2_j_jaw_01_091` | J_Jaw_01 | `p2_j_jaw_01_091` | False | False | 1 |
| 93 | `p2_j_petal_07_092` | J_Petal_07 | `p2_j_petal_07_092` | False | False | 1 |
| 94 | `p2_head_093` | Head | `p2_head_093`, `p2_head_093_glow` | True | True | 1 |
| 95 | `p2_head_094` | Head | `p2_head_094`, `p2_head_094_glow` | True | True | 1 |
| 96 | `p2_head_095` | Head | `p2_head_095`, `p2_head_095_glow` | True | True | 1 |
| 97 | `p2_head_096` | Head | `p2_head_096`, `p2_head_096_glow` | True | True | 1 |
| 98 | `p2_j_spine_097` | J_Spine | `p2_j_spine_097` | False | False | 1 |
| 99 | `p2_j_spine_098` | J_Spine | `p2_j_spine_098` | False | False | 1 |
| 100 | `p2_j_l_wrist_099` | J_L_Wrist | `p2_j_l_wrist_099` | False | False | 2 |
| 101 | `p2_j_l_wrist_100` | J_L_Wrist | `p2_j_l_wrist_100` | False | False | 4 |
| 102 | `p2_j_l_wrist_101` | J_L_Wrist | `p2_j_l_wrist_101` | False | False | 2 |
