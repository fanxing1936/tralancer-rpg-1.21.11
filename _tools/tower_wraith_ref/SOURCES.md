# 亚巴顿麾下罪仆（塔中幽魂）参考素材来源

原作：Minecraft Dungeons 的 Tower Wraith（Mojang Studios），版权归 Mojang 所有。
页面：<https://minecraft.wiki/w/Dungeons:Tower_Wraith>（Textures、Sounds 与 Renders 几节）。模型用黑色本体贴图 `T_TowerWraith.png`，
眼睛与宝石按发光层 `T_TowerWraith_S.png` 发光；绿色变体贴图与本体渲染图一并存档作参照。
音效 13 组共 45 段全部存档，其中用到的见 `add_tower_wraith.py`。动画参照页面上的
Idle、Walk、IceCloud、ModeChange 等动图在 Blockbench 里重做。

文件经内置浏览器从 minecraft.wiki 的 `/images/<文件名>` 取得（站点的 Cloudflare 拒绝 curl），
按原文件名保存。本项目开源免费、非商业，与 Mojang 无关联。

## 原始素材

| 文件 | 字节 | SHA-256（前 16 位） | 来源页面 | 文件地址 |
|---|---|---|---|---|
| `T_TowerWraith.png` | 2227 | `2aa0622f69515a06` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/T_TowerWraith.png> |
| `T_TowerWraith_S.png` | 894 | `993971d86dafda74` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/T_TowerWraith_S.png> |
| `T_TowerWraith_Green.png` | 2221 | `817d42d2a311899e` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/T_TowerWraith_Green.png> |
| `MCD_Tower_Wraith_(Black).png` | 320839 | `0d89a9bf1572d927` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/MCD_Tower_Wraith_%28Black%29.png> |
| `sounds/Sfx_mob_towerWraithAttack-001_soundWave.ogg` | 15461 | `436426822bac686e` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithAttack-001_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithAttack-002_soundWave.ogg` | 16148 | `44132589c39dd000` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithAttack-002_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithAttack-003_soundWave.ogg` | 16028 | `5965e4ec4b6017bb` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithAttack-003_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithAttack-004_soundWave.ogg` | 16935 | `09aac361009f73ea` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithAttack-004_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithAttack-005_soundWave.ogg` | 16594 | `504e904760fbd175` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithAttack-005_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithAttackVocal-001_soundWave.ogg` | 9218 | `bf137a5073ddad1d` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithAttackVocal-001_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithAttackVocal-002_soundWave.ogg` | 9016 | `3ea8ca2dd569207a` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithAttackVocal-002_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithChange-001_soundWave.ogg` | 11500 | `6c7a1e2b29c00e70` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithChange-001_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithChange-002_soundWave.ogg` | 12072 | `aac536cb468a2a8c` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithChange-002_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithChange-003_soundWave.ogg` | 11338 | `3ba0a1a67a3a72b1` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithChange-003_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithDeath-001_soundWave.ogg` | 34812 | `28d69196ef2021eb` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithDeath-001_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithDeath-002_soundWave.ogg` | 36004 | `010f309ec4b3d7f3` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithDeath-002_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithDeathVocal-001_soundWave.ogg` | 21084 | `a5e8c5dfa56abcbb` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithDeathVocal-001_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithDeathVocal-002_soundWave.ogg` | 21369 | `bfb7e61d23ce0064` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithDeathVocal-002_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithEmber-001_soundWave.ogg` | 26530 | `492bfdd906cc3d5a` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithEmber-001_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithEmber-002_soundWave.ogg` | 26177 | `6d3501fe8ddef7ad` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithEmber-002_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithEmber-003_soundWave.ogg` | 28212 | `2afa20568da562a3` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithEmber-003_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithEmber-004_soundWave.ogg` | 11436 | `326737782b230f7d` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithEmber-004_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithEmber-005_soundWave.ogg` | 10526 | `672b960cc9861945` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithEmber-005_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithFly-001_soundWave.ogg` | 19782 | `dba087a533127be5` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithFly-001_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithFly-002_soundWave.ogg` | 18463 | `bb0a82404d092292` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithFly-002_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithFly-003_soundWave.ogg` | 20886 | `12d6e3f6ed0978c3` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithFly-003_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithFly-004_soundWave.ogg` | 18959 | `6268972bcbdf9b9e` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithFly-004_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithFly-005_soundWave.ogg` | 18179 | `6827fae0d17dff38` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithFly-005_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithHurt-001_soundWave.ogg` | 17514 | `59064df44349898d` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithHurt-001_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithHurt-002_soundWave.ogg` | 17279 | `02676967f9d9cfcf` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithHurt-002_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithHurt-003_soundWave.ogg` | 24882 | `80bc1b3f767994a3` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithHurt-003_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithHurtVocal-001_soundWave.ogg` | 13330 | `432fda8648aaa373` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithHurtVocal-001_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithHurtVocal-002_soundWave.ogg` | 14675 | `89bd1b9478083981` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithHurtVocal-002_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithHurtVocal-003_soundWave.ogg` | 12089 | `526ea827c9551fdd` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithHurtVocal-003_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithIdle-001_soundWave.ogg` | 29890 | `28e3ed8857ccffe1` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithIdle-001_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithIdle-002_soundWave.ogg` | 19801 | `4a34cfd47ab59758` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithIdle-002_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithIdle-003_soundWave.ogg` | 22525 | `70041f3ab2587ad0` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithIdle-003_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithIdle-004_soundWave.ogg` | 20452 | `03170de62171af2e` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithIdle-004_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithIdle-005_soundWave.ogg` | 17701 | `a54224fe229b91d6` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithIdle-005_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithStun-001_soundWave.ogg` | 23591 | `4c2aac518a313d0a` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithStun-001_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithStun-002_soundWave.ogg` | 21000 | `347407fcff0f3498` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithStun-002_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithTeleportIn-001_soundWave.ogg` | 22664 | `a3d1ec8aea3a317f` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithTeleportIn-001_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithTeleportIn-002_soundWave.ogg` | 23284 | `5e743086c6ced288` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithTeleportIn-002_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithTeleportIn-003_soundWave.ogg` | 22211 | `865dbb999a7c3600` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithTeleportIn-003_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithTeleportIn-004_soundWave.ogg` | 22089 | `dc17f41b5cf6624e` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithTeleportIn-004_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithTeleportOut-001_soundWave.ogg` | 21128 | `f0fd0115eabad85d` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithTeleportOut-001_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithTeleportOut-002_soundWave.ogg` | 23308 | `66ac665c28ea0096` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithTeleportOut-002_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithTeleportOut-003_soundWave.ogg` | 23963 | `986c8014fed6b321` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithTeleportOut-003_soundWave.ogg> |
| `sounds/Sfx_mob_towerWraithTeleportOut-004_soundWave.ogg` | 24185 | `8da6bf13a8e10e3f` | <https://minecraft.wiki/w/Dungeons:Tower_Wraith> | <https://minecraft.wiki/images/Sfx_mob_towerWraithTeleportOut-004_soundWave.ogg> |

## 由此派生（不是原始素材）

| 文件 | 说明 |
|---|---|
| `tower_wraith.geo.json` | `tower_wraith_geo.py` 按贴图的方块展开图重建的初始几何 |
| `tower_wraith.bbmodel` | Blockbench 工程（模型、姿势与动画），`add_tower_wraith.py` 的数据源；亚巴顿也播放其中的动画 |
