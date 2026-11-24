# 序章配乐：转成 Ogg Vorbis

只转码，不改项目代码；只写下面「输出」列出的文件。

## 背景

Minecraft 只能播放 **Ogg Vorbis**（不是 Opus，也不是 MP3、FLAC、WAV）。序章的四首配乐原件在本目录 `_tools/prologue_ref/bgm_src/`，来源和许可见同目录的 `SOURCES.md`。成品放进 `_tools/bgm_ref/`，项目的 `add_boss_bgm.py` 会从那里拷进资源包。

## 输入与输出

| 输入（本目录） | 输出 | 做法 |
| --- | --- | --- |
| `prologue_intro.flac` | `_tools/bgm_ref/prologue_intro.ogg` | 转码 |
| `prologue_waves.mp3` | `_tools/bgm_ref/prologue_waves.ogg` | 转码 |
| `prologue_michael.wav` | `_tools/bgm_ref/prologue_michael.ogg` | 转码 |
| `prologue_end.ogg` | `_tools/bgm_ref/prologue_end.ogg` | 已是 Vorbis，**原样拷贝**，不要重新编码 |
| — | `_tools/prologue_ref/bgm_src/REPORT.md` | 转码报告（见下） |

## 编码要求

- 编码器 libvorbis，质量 `-q:a 5`（约 160 kbps）。例：
  `ffmpeg -i prologue_intro.flac -vn -map_metadata -1 -c:a libvorbis -q:a 5 ../../bgm_ref/prologue_intro.ogg`
- 保留原采样率（intro 48 kHz，waves 与 michael 44.1 kHz）和立体声。背景音乐是流式播放，不需要单声道。
- `-vn`：MP3 里可能内嵌封面图，不要输出视频流。
- `-map_metadata -1`：去掉原文件的标签。
- 不剪辑、不淡入淡出、不改音量、不做响度归一化。intro 与 michael 是无缝循环曲，开头结尾一个采样都不要加减。
- 不要用 Opus（`libopus`）或 ffmpeg 自带的 `vorbis` 实验编码器。

## 自检（全部通过才算完成）

1. 四个输出文件都以 `OggS` 开头，第一个包里能找到 `\x01vorbis` 标识头。
2. 每个输出的时长与原件相差不超过 0.1 秒。
3. `prologue_end.ogg` 与原件逐字节相同。
4. 用 `ffprobe` 读每个输出，编码名是 `vorbis`。

## REPORT.md

一张表：文件名、编码、采样率、声道、时长（秒，一位小数）、大小（KB）、平均码率；再写出实际用的命令和 ffmpeg 版本。任何一项自检没过，写明原因，不要跳过。

## 不要做的事

- 不要改动、删除或移动 `bgm_src/` 里的原件。
- 不要改 `_tools/bgm_ref/` 里已有的其它曲子，也不要改 `SOURCES.md`、`add_boss_bgm.py` 或任何构建脚本。登记曲目由 Claude 做。
- 除了安装 ffmpeg（如果环境里没有），不要下载任何别的东西。
