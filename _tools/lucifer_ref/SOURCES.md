# 当前版本：紫色左眼、武器同色 Verdant Robe 与九段动作

2026-11-08 当前事实来源为 `lucifer.bbmodel`，SHA-256 `1b31cc7009b5fb8065641c46a8f2d6de725dc8106b11486aac9de2fd7374a530`。用户将盔甲换为 [Verdant Robe](https://minecraft.wiki/w/Dungeons:Verdant_Robe)，要求改暗、与蛇矛同色、左眼紫色发光与淡光晕，并增加横砍。当前为44色材质映射、独立第五张发光图及九段动作；原四张PNG、几何与UV保留。下方旧Root Rot和模板重建登记均为历史记录。

- 用户定制发光图层：[lucifer_left_eye_emissive.png](lucifer_left_eye_emissive.png)，256×128 RGBA、467字节，SHA-256 `a67c4f42c4228a8281262f438f62c9a09811de4c6fd64185f2a56f584c2e8d22`。按原Head UV定位自身左眼 `(13,12)/(14,12)` 后生成；核心紫色 `#A855F7`，外围透明度柔化、材质强度0.14。是用户授权的新制作层，不冒称原游戏自带紫眼。
- [九动作、发光图层与配色的当前证据](validation/eye_palette_slash/NATIVE_VALIDATION_INDEX.json)
- [当前九动作预览](previews/visual_revision/manifest.json)

- [Verdant 原游戏包、材质、网格与逐文件哈希](verdant_sources/SOURCES.md)
- [七段原始 PSA、已有 cast/rise、适配脚本的历史封存](verdant_animation_sources/README.md)
- [成品来源和变更边界](REPORT.md)
- [整合每面映射与刚体握点记录](separate/verdant_assembly_validation.json)

所有原游戏资产版权归 Mojang 及原权利方；本项目非商业，与 Mojang 无关联。

---

# 路西法第一阶段：原始素材来源

## 2026-11-07 原始游戏模型与材质补充

已从本机 `D:\XboxGames\Minecraft Dungeons\Content` 取得原始 Mossy Skeleton / Root Rot Armor 网格、贴图与材质证据，取代此前目测重建候选。原包及逐文件哈希见 [original_game_assets/SOURCES.md](original_game_assets/SOURCES.md)；原始静态发光公式、DXBC、UniformExpressions 见 [material_port](original_game_assets/material_port/MI_NatureArmor_uniform_mapping.md)。当前分别核验和合体情况见 [REPORT.md](REPORT.md)。下方 Wiki 下载清单仍是原始参考文件的来源记录，不等同于当前模型网格来源。

Minecraft Dungeons 原作素材版权归 Mojang 所有。本项目非商业，与 Mojang 无关联。

下载日期：2026-11-07（Asia/Singapore）。curl.exe 实测可取得原始文件，Python urllib 被拒绝，最终使用 curl.exe 原文件链接。未使用 NNpx 缩略图或 .ogg.mp3。动作仅已下载参考 GIF，检查点 A 尚未制作动画。

| 文件名 | 字节数 | SHA-256 前 16 位 | 来源页面 | 直链 |
|---|---:|---|---|---|
| `MCD_Mossy_Skeleton.png` | 24937 | `548cfb68504a7144` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/MCD_Mossy_Skeleton.png> |
| `MCD_Mossy_Skeleton_Aiming.png` | 43278 | `7cd6f7605fa14e10` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/MCD_Mossy_Skeleton_Aiming.png> |
| `T_MossySkeleton.png` | 2366 | `fdcbe40f0556da0c` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/T_MossySkeleton.png> |
| `MCD_Root_Rot_Armor.png` | 58468 | `8152957158a529aa` | <https://minecraft.wiki/w/Dungeons:Root_Rot_Armor> | <https://minecraft.wiki/images/MCD_Root_Rot_Armor.png> |
| `Root_Rot_Armor_texture.png` | 859 | `44a796927cb17dd6` | <https://minecraft.wiki/w/Dungeons:Root_Rot_Armor> | <https://minecraft.wiki/images/Root_Rot_Armor_texture.png> |
| `RootRotArmor_ShadowTexture_(MCD).png` | 1075 | `00917716e88e9799` | <https://minecraft.wiki/w/Dungeons:Root_Rot_Armor> | <https://minecraft.wiki/images/RootRotArmor_ShadowTexture_%28MCD%29.png> |
| `Root_Rot_Player_Inventory_dressing.png` | 1051665 | `45ce918d86d4a4a0` | <https://minecraft.wiki/w/Dungeons:Root_Rot_Armor> | <https://minecraft.wiki/images/Root_Rot_Player_Inventory_dressing.png> |
| `MCD_Necromancer_Idle.gif` | 10653891 | `dbac771c04da6cad` | <https://minecraft.wiki/w/Dungeons:Necromancer> | <https://minecraft.wiki/images/MCD_Necromancer_Idle.gif> |
| `MCD_Necromancer_Walk.gif` | 1291239 | `7e415c8076be325a` | <https://minecraft.wiki/w/Dungeons:Necromancer> | <https://minecraft.wiki/images/MCD_Necromancer_Walk.gif> |
| `MCD_Necromancer_BasicAttack.gif` | 1401745 | `b788dc5b4768b649` | <https://minecraft.wiki/w/Dungeons:Necromancer> | <https://minecraft.wiki/images/MCD_Necromancer_BasicAttack.gif> |
| `MCD_Necromancer_StrongAttack.gif` | 1310083 | `8357df84530b93a9` | <https://minecraft.wiki/w/Dungeons:Necromancer> | <https://minecraft.wiki/images/MCD_Necromancer_StrongAttack.gif> |
| `MCD_Necromancer_Stun.gif` | 2394245 | `cdd7cf7815464233` | <https://minecraft.wiki/w/Dungeons:Necromancer> | <https://minecraft.wiki/images/MCD_Necromancer_Stun.gif> |
| `MCD_Necromancer_Novelty.gif` | 1902308 | `58a77a06ad1e77c2` | <https://minecraft.wiki/w/Dungeons:Necromancer> | <https://minecraft.wiki/images/MCD_Necromancer_Novelty.gif> |
| `MCD_Necromancer_GetHitFront.gif` | 2006550 | `95d21b96b136b87d` | <https://minecraft.wiki/w/Dungeons:Necromancer> | <https://minecraft.wiki/images/MCD_Necromancer_GetHitFront.gif> |
| `sounds/DLC_sfx_mob_MossySkeletonAttack-001.ogg` | 7135 | `e988cdc7b5a521d0` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_MossySkeletonAttack-001.ogg> |
| `sounds/DLC_sfx_mob_MossySkeletonAttack-002.ogg` | 6867 | `e29fc0dc8ddd779d` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_MossySkeletonAttack-002.ogg> |
| `sounds/DLC_sfx_mob_MossySkeletonAttack-003.ogg` | 7267 | `faba9f11b11ced77` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_MossySkeletonAttack-003.ogg> |
| `sounds/DLC_sfx_mob_MossySkeletonHurt-001.ogg` | 13211 | `180a102bc1b3ba27` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_MossySkeletonHurt-001.ogg> |
| `sounds/DLC_sfx_mob_MossySkeletonHurt-002.ogg` | 10764 | `c985e21a8f2bd5e3` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_MossySkeletonHurt-002.ogg> |
| `sounds/DLC_sfx_mob_MossySkeletonHurt-003.ogg` | 11097 | `ce37bcb563f9d8fa` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_MossySkeletonHurt-003.ogg> |
| `sounds/DLC_sfx_mob_MossySkeletonHurt-004.ogg` | 12094 | `33c36e23c86dda55` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_MossySkeletonHurt-004.ogg> |
| `sounds/DLC_sfx_mob_MossySkeletonIdle-001.ogg` | 13217 | `4265fd67e373f1b9` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_MossySkeletonIdle-001.ogg> |
| `sounds/DLC_sfx_mob_MossySkeletonIdle-002.ogg` | 16215 | `a5bf620d4a71eeeb` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_MossySkeletonIdle-002.ogg> |
| `sounds/DLC_sfx_mob_MossySkeletonIdle-003.ogg` | 15523 | `6e2f596e13dbc268` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_MossySkeletonIdle-003.ogg> |
| `sounds/DLC_sfx_mob_MossySkeletonStep-001.ogg` | 11324 | `be222e4a8698f878` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_MossySkeletonStep-001.ogg> |
| `sounds/DLC_sfx_mob_MossySkeletonStep-002.ogg` | 8374 | `60a70e91069eb590` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_MossySkeletonStep-002.ogg> |
| `sounds/DLC_sfx_mob_MossySkeletonStep-003.ogg` | 8917 | `b469c8250f97f776` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_MossySkeletonStep-003.ogg> |
| `sounds/DLC_sfx_mob_MossySkeletonStep-004.ogg` | 9240 | `4359c184f1d390f8` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_MossySkeletonStep-004.ogg> |
| `sounds/DLC_sfx_mob_mossySkeletonArrowWhoosh-001_soundWave.ogg` | 15646 | `f744372ef7f5406c` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_mossySkeletonArrowWhoosh-001_soundWave.ogg> |
| `sounds/DLC_sfx_mob_mossySkeletonArrowWhoosh-002_soundWave.ogg` | 11440 | `1c96a879593591f6` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_mossySkeletonArrowWhoosh-002_soundWave.ogg> |
| `sounds/DLC_sfx_mob_mossySkeletonArrowWhoosh-003_soundWave.ogg` | 14311 | `2a8cf42c5edb1d5e` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_mossySkeletonArrowWhoosh-003_soundWave.ogg> |
| `sounds/DLC_sfx_mob_mossySkeletonArrowWhoosh-004_soundWave.ogg` | 17432 | `b4eef52f6174e6e8` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_mossySkeletonArrowWhoosh-004_soundWave.ogg> |
| `sounds/DLC_sfx_mob_mossySkeletonArrowWhoosh-005_soundWave.ogg` | 12878 | `1cac4443b4b964a5` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_mossySkeletonArrowWhoosh-005_soundWave.ogg> |
| `sounds/DLC_sfx_mob_mossySkeletonArrowWhoosh-006_soundWave.ogg` | 17336 | `d96fb3fa91ca3e49` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_mossySkeletonArrowWhoosh-006_soundWave.ogg> |
| `sounds/DLC_sfx_mob_mossySkeletonDeath-001_soundWave.ogg` | 14314 | `f7503f566772412b` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_mossySkeletonDeath-001_soundWave.ogg> |
| `sounds/DLC_sfx_mob_mossySkeletonDeath-002_soundWave.ogg` | 16354 | `4e0ae7fd40cc4739` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_mossySkeletonDeath-002_soundWave.ogg> |
| `sounds/DLC_sfx_mob_mossySkeletonDeath-003_soundWave.ogg` | 14235 | `88f8eeef6f30fc18` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_mossySkeletonDeath-003_soundWave.ogg> |
| `sounds/DLC_sfx_mob_mossySkeletonDeath-004_soundWave.ogg` | 16387 | `d380b734470e482a` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_mossySkeletonDeath-004_soundWave.ogg> |
| `sounds/DLC_sfx_mob_mossySkeletonDeath-005_soundWave.ogg` | 15230 | `32b17a8782500111` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_mossySkeletonDeath-005_soundWave.ogg> |
| `sounds/DLC_sfx_mob_mossySkeletonDeath-006_soundWave.ogg` | 14277 | `98eaaf5fd1a8a0ac` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_mossySkeletonDeath-006_soundWave.ogg> |
| `sounds/DLC_sfx_mob_mossySkeletonDeath-007_soundWave.ogg` | 14370 | `92fca043d818c6f5` | <https://minecraft.wiki/w/Dungeons:Mossy_Skeleton> | <https://minecraft.wiki/images/DLC_sfx_mob_mossySkeletonDeath-007_soundWave.ogg> |

## 项目内复用来源

- 指定项目骨架与该模板的逐面 UV：`../sunken_skeleton_ref/sunken_skeleton.bbmodel`（仅提取分析，未修改）。按该目录 `SOURCES.md`，其几何是本项目按贴图网格重建的产物，**不是 Mojang 原始网格或原始 UV 证据**；继承它只证明符合指定模板，不能证明 Mossy Skeleton 全身外观。
- 后续动作模板：`../leviathan_ref/leviathan.bbmodel`（项目重建/派生工程，不是取得的 Mojang 原始网格；尚未复制/修改动作）。
- 手持蛇矛：`../../resourcepack/assets/rpg/models/item/lucifer_in_hand.json` 与同名贴图，归 `../add_lucifer.py` 生成，本次未修改。
- Java 1.21.11 自带 `minecraft:item/spear_in_hand`：仅提取第三人称变换用于核对，详见 `validation/weapon_reference.json`。

## 检查点 A 派生产物

下表模型均为本项目制作的工程，不是取得的 Mojang 原始网格。先前候选重建属于历史过程；当前用户要求以忠实原作为准，仅允许有原始依据的左右对称共用纹理，未知面仍不验收。**独立本体、独立盔甲和旧合体均未验收，UV 审计及原始几何证据问题解决前暂停整合。** 原始素材完整内嵌，不等于派生模型的几何和 UV 已得到原作证明。

| 文件 | 字节数 | SHA-256 前16位 | 派生来源与处理 |
|---|---:|---|---|
| `lucifer.bbmodel` | 54210 | `f9d317d3efcdd329` | 当前保存的旧合体草稿：继承项目 Sunken 模板，删除遮挡身体几何，增加 Root Rot 候选外层；后在 Blockbench 收窄双靴并原生保存；0动作、未验收，不是两套独立工程重新整合结果 |
| `lucifer_atlas.png` | 5717 | `9ee9e10fd79f9823` | 旧合体草稿图集128×128：身体alpha阈值128，另有绿色亮部候选补偿与内衬复制；未获当前还原度验收，不代表现独立本体的原始PNG |
| `FACE_UV_MAP.json` | 201375 | `43fe3cfffadada2a` | 旧脚本准备版360面的历史候选映射记录；记录来源坐标、图集坐标、依据/推断和处理，不是当前两套独立工程全部面的实测证明 |
| `static_config.json` | 1311 | `fd9822a261a715c2` | 旧合体静态候选配置：7部件、双眼发光、2.4格缩放、seat2.0、held=weapon；未进行动作/运行时接入 |
| `separate/mossy_skeleton_body.bbmodel` | 10440 | `742a2114592c5b84` | 当前独立本体：6元素、7骨骼、36面；几何与UV继承项目Sunken模板，双臂中立；经运行中Blockbench恢复原始 `T_MossySkeleton.png` 后原生保存，内嵌PNG字节完全相同、RGBA差异0；0动作，几何/整体还原度未验收 |
| `separate/root_rot_armor.bbmodel` | 45392 | `df696b7cb8c6b80d` | 当前独立盔甲：59元素、16骨骼、344有纹理面、64×128派生图集；仍含绿色候选补偿及无原始依据的复用，418有效源像素未用、228有效源像素复用；0动作、未验收 |

独立本体内嵌的原始 PNG SHA-256 为 `fdcbe40f0556da0c54983d7a9ccfbf30ec98e9ddd609045548e240c2105a97c0`，与原文件一致；此前100个alpha改动已纠正，旧本体保存在 `separate/history/`。当前本体208个源像素的左右臂/腿共用可以核对到指定Sunken模板，按用户的有依据对称例外记录，但模板本身为项目重建，不能冒充原始Mossy全身证据。

独立工程当前审计见 `separate/uv_audit_body.md`、`separate/uv_audit_armor.md` 与 `separate/validation.json`；未知原始几何证据缺口见 `separate/source_gap_check.md`。`FACE_UV_MAP.md` 与上表旧JSON均保留为旧合体过程记录，不能据此声称当前独立工程全部通过。后续状态以 `REPORT.md` 中的最新用户约束与未验收说明为准。
