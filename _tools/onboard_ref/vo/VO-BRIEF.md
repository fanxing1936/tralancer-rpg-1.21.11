# 新手开局 · 世界观旁白：英语配音生成任务

只生成音频，不改项目代码；只在 `_tools/onboard_ref/vo/` 里写文件。

## 背景

《破碎大陆》新玩家第一次进入世界时，在黑屏里先听一段世界观旁白（约一分钟），然后才起名字。字幕中英双语，配音只配英语。台词原稿是 `_tools/onboard_ref/lines.json`（**不要改它**），共 10 条，编号 W01～W10，全部是旁白，全部 `"voiced": true`。

这段旁白和序章开头的旁白（`_tools/prologue_ref/lines.json` 的 N01～N05）是同一个讲述者，声线和基调要一致。

## 怎么生成

- 用 OpenAI 的语音合成（`gpt-4o-mini-tts`，或当时更好的、支持 `instructions` 表演指令的语音模型）。API 密钥从环境变量取，不要写进任何文件或日志。
- 朗读文本 = 该条的 `en` 字段，一字不改。不要读出编号，不要加语气词。
- 表演指令 = 下面的「角色基调」+ 一个空格 + 该条的 `direction` 字段。
- **每条生成 3 条（take）**，让用户挑。

| speaker | 角色 | 声线（voice） | 角色基调（每条都加在 direction 前面） |
| --- | --- | --- | --- |
| narrator | 旁白 | fable（和序章旁白相同） | An old storyteller reading scripture aloud: slow, unhurried, reverent, close to the microphone. |

声线名以生成时模型实际提供的为准；fable 不可用时，挑最接近「角色基调」的一个，并在报告里写明换成了什么。

W10 里的希伯来名 `Eretz Ha-Shevarim` 读作 EH-rets ha-sheh-vah-REEM；如果模型读错，可以在朗读文本里临时改写成这个音标拼法生成，但 REVIEW.md 里照原文记。

## 后期处理

所有 take：转成 **Ogg Vorbis**（libvorbis，`-q:a 6`），**单声道、48 kHz**；响度归一到 **−16 LUFS**（integrated），真峰值不超过 **−1 dBTP**；首尾静音各剪到 50 毫秒。不要用 Opus。

## 输出

```
_tools/onboard_ref/vo/
  takes/<编号>_1.ogg   <编号>_2.ogg   <编号>_3.ogg     每条三个 take（共 30 个文件）
  REVIEW.md          一张表：编号 · 英文台词 · 三个 take 的时长（秒，一位小数），方便用户逐条试听
  picks.json         {"W01": 1, ...} 先全部填 1，用户听完改成想要的 take
  SOURCES.md         模型名与版本、实际用的声线、生成日期，以及这句声明：
                     "The English voice-over in the onboarding narration is AI-generated (OpenAI text-to-speech); it is not a human voice."
```

## 自检（全部通过才算完成）

1. 10 个编号 × 3 个 take 全部存在，都以 `OggS` 开头、编码 `vorbis`、单声道、48 kHz（用 `ffprobe` 核对）。
2. 每个文件的响度在 −16 ± 1 LUFS，真峰值 ≤ −1 dBTP（`ffmpeg -af ebur128=peak=true` 核对）。
3. 每个 take 的时长在 0.4～15 秒之间；超出的写进报告。
4. REVIEW.md 里的英文与 lines.json 的 `en` 逐字一致。

任何一项没过，在 REVIEW.md 末尾写明原因，不要跳过。

## 不要做的事

- 不要改 lines.json，也不要改项目里任何别的文件。
- 除了生成所需的 API 调用，以及环境里缺 ffmpeg 时安装它，不要下载任何别的东西。

## 接入（给集成方，不是配音方的任务）

`picks.json` 里选中的 take 在构建时由 `onboard_text.py` 抬响、拷进资源包，登记成 `rpg:vo.onboard.w01`…；字幕的显示时长自动改用配音的真实长度。没有 picks.json 或文件缺失时，那一句只显示字幕、按预估时长播放。
