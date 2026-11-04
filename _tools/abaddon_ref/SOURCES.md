# 亚巴顿（悲惨幽魂）参考素材来源

原作：Minecraft Dungeons 的 Wretched Wraith（Mojang Studios），版权归 Mojang 所有。
页面：<https://minecraft.wiki/w/Dungeons:Wretched_Wraith>（Textures、Renders 与 Sounds 几节）。模型用本体贴图
`MCD_Wretched_Wraith_(texture).png`，按发光层 `T_Wicked_Wraith_E_01.png` 发光；本体渲染图与
正面图用来逐面核对贴图映射（正面图与贴图逐像素一致）；`T_WraithFB.png` 存档未用。
音效（不含 DLC 的 F/V 两套重复版本）15 组共 38 段全部存档，用到的见 `add_abaddon_model.py`。
wiki 没有悲惨幽魂的动作展示，亚巴顿播放塔中幽魂的动画（见 `../tower_wraith_ref/SOURCES.md`）。

文件经内置浏览器从 minecraft.wiki 的 `/images/<文件名>` 取得（站点的 Cloudflare 拒绝 curl），
按原文件名保存。本项目开源免费、非商业，与 Mojang 无关联。

## 原始素材

| 文件 | 字节 | SHA-256（前 16 位） | 来源页面 | 文件地址 |
|---|---|---|---|---|
| `MCD_Wretched_Wraith_(texture).png` | 8080 | `06a3c452fb25f3f1` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/MCD_Wretched_Wraith_%28texture%29.png> |
| `T_Wicked_Wraith_E_01.png` | 1394 | `e92e59388adcfbc8` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/T_Wicked_Wraith_E_01.png> |
| `MCD_Wretched_Wraith.png` | 84176 | `7bb380da6d7bcf7b` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/MCD_Wretched_Wraith.png> |
| `MCD_Wretched_Wraith_face.png` | 2601 | `e4ac2b8b104e45d6` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/MCD_Wretched_Wraith_face.png> |
| `T_WraithFB.png` | 694 | `e1d0b89ab9c66b99` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/T_WraithFB.png> |
| `sounds/WretchedWraithBasicAttackFoley-001_soundwave.ogg` | 9929 | `05f66b57c9fcf69e` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithBasicAttackFoley-001_soundwave.ogg> |
| `sounds/WretchedWraithBasicAttackFoley-002_soundwave.ogg` | 8803 | `c5c1c4dcc64bec5b` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithBasicAttackFoley-002_soundwave.ogg> |
| `sounds/WretchedWraithBasicAttackFoley-003_soundwave.ogg` | 9154 | `8f8440a72068b5c1` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithBasicAttackFoley-003_soundwave.ogg> |
| `sounds/WretchedWraithBasicAttackVocal-001_soundwave.ogg` | 7296 | `2543e356f86ce034` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithBasicAttackVocal-001_soundwave.ogg> |
| `sounds/WretchedWraithBasicAttackVocal-002_soundwave.ogg` | 7190 | `318fb1807eb3b422` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithBasicAttackVocal-002_soundwave.ogg> |
| `sounds/WretchedWraithBasicAttackVocal-003_soundwave.ogg` | 7262 | `ba8e634fe6750104` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithBasicAttackVocal-003_soundwave.ogg> |
| `sounds/WretchedWraithDeath-001_soundwave.ogg` | 21911 | `c002ca27c3546325` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithDeath-001_soundwave.ogg> |
| `sounds/WretchedWraithDeath-002_soundwave.ogg` | 22235 | `861c380c51213b70` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithDeath-002_soundwave.ogg> |
| `sounds/WretchedWraithHurt-001_soundwave.ogg` | 12249 | `798a18265a58843d` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithHurt-001_soundwave.ogg> |
| `sounds/WretchedWraithHurt-002_soundwave.ogg` | 12021 | `954681c77c35c1ce` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithHurt-002_soundwave.ogg> |
| `sounds/WretchedWraithHurt-003_soundwave.ogg` | 12381 | `c79198560b0c08f4` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithHurt-003_soundwave.ogg> |
| `sounds/WretchedWraithIdle-001_soundwave.ogg` | 12954 | `1efb9d772ed23563` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithIdle-001_soundwave.ogg> |
| `sounds/WretchedWraithIdle-002_soundwave.ogg` | 11134 | `5bc47ad701d6e57f` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithIdle-002_soundwave.ogg> |
| `sounds/WretchedWraithIdle-003_soundwave.ogg` | 11389 | `c80b746b06b5bd2e` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithIdle-003_soundwave.ogg> |
| `sounds/WretchedWraithIdle-004_soundwave.ogg` | 11258 | `3ba0b7b5e2e19e50` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithIdle-004_soundwave.ogg> |
| `sounds/WretchedWraithIdle-005_soundwave.ogg` | 12294 | `eaa8f26a4a90320b` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithIdle-005_soundwave.ogg> |
| `sounds/WretchedWraithIdle-006_soundwave.ogg` | 12041 | `1d1a11e44af749da` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithIdle-006_soundwave.ogg> |
| `sounds/WretchedWraithIntroFoley_soundwave.ogg` | 14744 | `9b7fd80c46c128c1` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithIntroFoley_soundwave.ogg> |
| `sounds/WretchedWraithIntroVocal_soundwave.ogg` | 8203 | `0af1d347e05eba66` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithIntroVocal_soundwave.ogg> |
| `sounds/WretchedWraithProjectileAttackFoley-001_soundwave.ogg` | 16647 | `34e9a11d2dffc2d6` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithProjectileAttackFoley-001_soundwave.ogg> |
| `sounds/WretchedWraithProjectileAttackFoley-002_soundwave.ogg` | 17681 | `bef6802a28328802` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithProjectileAttackFoley-002_soundwave.ogg> |
| `sounds/WretchedWraithProjectileAttackFoley-003_soundwave.ogg` | 16292 | `c859597f893de104` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithProjectileAttackFoley-003_soundwave.ogg> |
| `sounds/WretchedWraithProjectileAttackVocal-001_soundwave.ogg` | 9480 | `2eb405ae635e05ee` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithProjectileAttackVocal-001_soundwave.ogg> |
| `sounds/WretchedWraithProjectileAttackVocal-002_soundwave.ogg` | 8933 | `346e492106547bd7` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithProjectileAttackVocal-002_soundwave.ogg> |
| `sounds/WretchedWraithProjectileAttackVocal-003_soundwave.ogg` | 7949 | `cd03c555229f72fe` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithProjectileAttackVocal-003_soundwave.ogg> |
| `sounds/WretchedWraithProjectileCircleFoley-001_soundwave.ogg` | 16706 | `c60df332b76ae9b6` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithProjectileCircleFoley-001_soundwave.ogg> |
| `sounds/WretchedWraithProjectileCircleFoley-002_soundwave.ogg` | 15947 | `7d17c74de8519c13` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithProjectileCircleFoley-002_soundwave.ogg> |
| `sounds/WretchedWraithProjectileCircleFoley-003_soundwave.ogg` | 18759 | `b7416272617b2d63` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithProjectileCircleFoley-003_soundwave.ogg> |
| `sounds/WretchedWraithProjectileCircleVocal-001_soundwave.ogg` | 7528 | `bd629d2ac022299e` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithProjectileCircleVocal-001_soundwave.ogg> |
| `sounds/WretchedWraithProjectileCircleVocal-002_soundwave.ogg` | 7085 | `c834275211675ff7` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithProjectileCircleVocal-002_soundwave.ogg> |
| `sounds/WretchedWraithProjectileCircleVocal-003_soundwave.ogg` | 7594 | `451eb06bc83d8da6` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithProjectileCircleVocal-003_soundwave.ogg> |
| `sounds/WretchedWraithStunCrown-001_soundwave.ogg` | 7031 | `c9b9eff91bf37674` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithStunCrown-001_soundwave.ogg> |
| `sounds/WretchedWraithStunCrown-002_soundwave.ogg` | 7603 | `bc6874dfdcc99c0d` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithStunCrown-002_soundwave.ogg> |
| `sounds/WretchedWraithStunMove_soundwave.ogg` | 25169 | `1c9190f19ba0ee45` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithStunMove_soundwave.ogg> |
| `sounds/WretchedWraithSummon-001_soundwave.ogg` | 29988 | `50fe140c2f6db385` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithSummon-001_soundwave.ogg> |
| `sounds/WretchedWraithWalkIce-001_soundwave.ogg` | 21805 | `46746cf6b0fb19f2` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithWalkIce-001_soundwave.ogg> |
| `sounds/WretchedWraithWalkIce-002_soundwave.ogg` | 18998 | `b984d6d13217ca6d` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithWalkIce-002_soundwave.ogg> |
| `sounds/WretchedWraithWalkIce-003_soundwave.ogg` | 21700 | `02146163d98aeee9` | <https://minecraft.wiki/w/Dungeons:Wretched_Wraith> | <https://minecraft.wiki/images/WretchedWraithWalkIce-003_soundwave.ogg> |

## 由此派生（不是原始素材）

| 文件 | 说明 |
|---|---|
| `abaddon_atlas.png` | 本体贴图，另在第 127 行以下复制一份只留发光像素的头部展开图，画在略放大的头部外层上 |
| `abaddon.geo.json` | `abaddon_geo.py` 按贴图的方块展开图重建的初始几何 |
| `abaddon.bbmodel` | Blockbench 工程（模型与姿势），`add_abaddon_model.py` 的数据源 |
