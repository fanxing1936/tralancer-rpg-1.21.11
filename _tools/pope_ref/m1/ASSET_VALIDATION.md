# 教皇 M1 素材校验

采集日期：2026-11-04。校验结果：全部通过。

本报告只证明文件完整性与可解码性，不证明模型还原度、动作定稿或游戏内兼容。未在真实游戏内看过；没有逐段人工听完音频。

## 范围与方法

- 本次下载：18 个视觉文件、39 段音效（17 组），总计 57 文件；引用已有贴图 2 张。
- 检查文件签名、实际字节数、完整 SHA-256，并逐项对比 download_log.jsonl 的成功写入记录。
- Pillow verify 后重新打开每张图；GIF 逐帧 seek/load/转为 RGBA 完整解码，时长为每帧 duration 的总和。
- FFmpeg 使用 -xerror 完整解码每段 OGG 为内存 PCM s16le；记录退出码、错误输出、解码样本数和声道/采样率。没有截取前几秒代替完整检查。
- 原始素材仅被读取，未转码覆盖；两张 heart_of_ender_ref 贴图没有复制。
- 清单无 Music、Archvessel、Archvisage；sounds 目录的 .ogg 与清单严格一致。

工具：Python 3.12.10；Pillow 12.3.0；ffmpeg version 7.1-essentials_build-www.gyan.dev Copyright (c) 2000-2024 the FFmpeg developers。

复现：在仓库运行 `python _tools/pope_validate_sources.py`。输出本报告、`m1/asset_validation.json` 和 `SOURCES.md`，不写入原始素材。

## 图片与 GIF 实测

| 文件 | 尺寸 | 帧数 | GIF 总时长（秒） | 校验 |
|---|---|---:|---:|---|
| `MCD_Arch-Illager.png` | 666×999 | 1 | — | 通过 |
| `MCD_Arch-Illagers_Staff.png` | 342×956 | 1 | — | 通过 |
| `T_SuperStaff.png` | 32×32 | 1 | — | 通过 |
| `T_SuperCube.png` | 32×32 | 1 | — | 通过 |
| `MCD_Arch-Illager_Idle.gif` | 666×999 | 101 | 4.04 | 通过 |
| `MCD_Arch-Illager_Idle_Highblock_Halls_(front_view).gif` | 500×500 | 101 | 4.04 | 通过 |
| `MCD_Arch-Illager_Run.gif` | 500×500 | 61 | 1.83 | 通过 |
| `MCD_Arch-Illager_Basic_Attack.gif` | 500×500 | 32 | 1.28 | 通过 |
| `MCD_Arch-Illager_Summon_Circle.gif` | 500×500 | 51 | 2.04 | 通过 |
| `MCD_Arch-Illager_Summon_Single.gif` | 500×500 | 63 | 2.52 | 通过 |
| `MCD_Arch-Illager_Appear.gif` | 500×500 | 249 | 9.96 | 通过 |
| `MCD_Arch-Illager_Teleport_(Appear_Short).gif` | 500×500 | 135 | 5.4 | 通过 |
| `MCD_Arch-Illager_Defeated_in_a_Whirlwind_in_game.gif` | 800×800 | 161 | 6.44 | 通过 |
| `MCD_Arch-Illager_Defeated_in_a_Whirlwind.gif` | 800×800 | 200 | 8.0 | 通过 |
| `Arch-Illager_sit_in_his_throne_room_front_view.jpg` | 1920×992 | 1 | — | 通过 |
| `Arch-Illager_ready_to_fight.png` | 667×711 | 1 | — | 通过 |
| `Arch-Illager_defeated.png` | 1101×720 | 1 | — | 通过 |
| `Arch-Illager_defeated_in_a_whirlwind_lose_crowns.jpg` | 1920×1080 | 1 | — | 通过 |
| `../heart_of_ender_ref/MCD_Arch-Illager_(texture).png` | 64×64 | 1 | — | 通过 |
| `../heart_of_ender_ref/MCD_Arch-Illager_(shadow_texture).png` | 64×64 | 1 | — | 通过 |

GIF 文件总时长包含导出的完整片段，不等同于自然动作周期或最终 clip 时长；后续剪辑/重定时必须在动作报告记录。每帧原始 duration 见 JSON。

## 音效完整解码

| 文件 | PCM 解码时长（秒） | 声道 | 采样率 | 解码结果 |
|---|---:|---:|---:|---|
| `sounds/Sfx_mob_archIllager_loadSpell-001_soundWave.ogg` | 1.18458 | 2 | 44100 | 通过 |
| `sounds/Sfx_mob_archIllager_mirrorIn-001_soundWave.ogg` | 3.314671 | 2 | 44100 | 通过 |
| `sounds/Sfx_mob_archIllager_mirrorOut-001_soundWave.ogg` | 2.201338 | 2 | 44100 | 通过 |
| `sounds/Sfx_mob_archIllager_spell-001_soundWave.ogg` | 2.316349 | 2 | 44100 | 通过 |
| `sounds/Sfx_mob_archIllager_spellDissapear-001_soundWave.ogg` | 1.904104 | 2 | 44100 | 通过 |
| `sounds/Sfx_mob_archIllagerAppear-001_soundWave.ogg` | 1.783605 | 2 | 44100 | 通过 |
| `sounds/Sfx_mob_archIllagerHaha-001_soundWave.ogg` | 1.972902 | 2 | 44100 | 通过 |
| `sounds/Sfx_mob_archIllagerHaha-002_soundWave.ogg` | 3.224671 | 2 | 44100 | 通过 |
| `sounds/Sfx_mob_archillagerHargh-001_soundWave.ogg` | 2.297438 | 2 | 44100 | 通过 |
| `sounds/Sfx_mob_archillagerHargh-002_soundWave.ogg` | 2.902018 | 2 | 44100 | 通过 |
| `sounds/Sfx_mob_archillagerHargh-003_soundWave.ogg` | 2.100907 | 2 | 44100 | 通过 |
| `sounds/Sfx_mob_archillagerHargh-004_soundWave.ogg` | 2.645374 | 2 | 44100 | 通过 |
| `sounds/Sfx_mob_archIllagerLaugh-001_soundWave.ogg` | 3.281565 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerHurt-001.ogg` | 0.657982 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerHurt-002.ogg` | 0.76254 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerHurt-003.ogg` | 1.204717 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerHurt-004.ogg` | 1.065941 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerHurt-005.ogg` | 0.760068 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerHurt-006.ogg` | 1.080363 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerIdle-001.ogg` | 4.102018 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerIdle-002.ogg` | 3.300907 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerIdle-003.ogg` | 3.845374 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerIdle-004.ogg` | 3.498662 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerIdle-005.ogg` | 2.53907 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerIdle-006.ogg` | 3.0978 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerIdle-007.ogg` | 2.100091 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerIdle-008.ogg` | 2.322404 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerIdle-009.ogg` | 3.223492 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerIdle-010.ogg` | 2.351293 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerIdle-011.ogg` | 3.825306 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerIdle-012.ogg` | 2.010431 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerIdle-013.ogg` | 2.592698 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_archillagerIntroFinalBlow.ogg` | 4.962449 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_archIllagerIntroGreetings-001.ogg` | 3.219841 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_archillagerIntroLaugh-002.ogg` | 3.771769 | 2 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerMagicImpact-001.ogg` | 1.673719 | 1 | 44100 | 通过 |
| `sounds/Sfx_boss_archillagerSummonMobs-001.ogg` | 3.916213 | 1 | 44100 | 通过 |
| `sounds/Sfx_boss_archillagerSummonMobs-002.ogg` | 3.143764 | 1 | 44100 | 通过 |
| `sounds/Sfx_boss_ArchillagerWhirlwind.ogg` | 13.032993 | 2 | 44100 | 通过 |

## 重复内容与下载记录

不同原文件名即使字节相同也保持原名，不自行删除或重命名；分组与实际声音链接仍以网页清单为准。

本次没有不同文件名但内容完全相同的记录。

主渲染 manifest 的 initial_url、Original file 页面和当前 URL 均保留；download_log.jsonl 第57条成功记录与本地哈希一致。该 JSONL 只记录成功保存，不将缺少的失败条目伪造成已有日志。
