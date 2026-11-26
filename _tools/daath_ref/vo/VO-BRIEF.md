# 达阿特试炼配音：英语配音生成任务

只生成音频，不改项目代码；只在 `_tools/daath_ref/vo/` 里写文件。

## 背景

达阿特试炼是玩家和自己影子的单人对决（`docs/DAATH-DESIGN.md`）。说话的只有一个角色：**影子，也就是玩家自己**。它不是反派，不威胁、不嘲讽，只陈述事实。玩家可能是任何性别，所以同一句由两条声线同时说，叠成一个「不是人的你」。

台词在 `_tools/daath_ref/lines.json`（**不要改它**）。只配 `"voiced": true` 的 23 条（S01～S23）。N01、N02 带数字，只有字幕。

## 怎么生成

- 用 OpenAI 的语音合成（`gpt-4o-mini-tts`，或当时更好的、支持 `instructions` 表演指令的语音模型）。API 密钥从环境变量取，不写进任何文件或日志。
- 朗读文本 = 该条的 `en`，一字不改。
- 表演指令 = `lines.json` 里的 `base` + 一个空格 + 该条的 `direction`。
- **每条生成 3 个 take**。每个 take 由下面三条素材合成：

| 素材 | 声线 | 表演指令附加 | 电平 |
| --- | --- | --- | --- |
| A 男声 | onyx | 无 | 0 dB |
| B 女声 | sage | 无 | −2 dB |
| C 耳语 | 与 A 相同 | `whispering, breathy, almost inaudible` | −14 dB |

声线名以生成时模型实际提供的为准；某条不可用就挑最接近的（低沉的男声、清冷的女声），在报告里写明。

## 合成与后期

1. A、B 各自剪掉首尾静音，再把 B 整句伸缩到与 A 等长（伸缩不超过 ±8%，超过就重新生成 B），起音对齐到 20 毫秒以内，叠加。要听起来是**一个人用两个嗓子说话**，不是两个人合唱。
2. 整体降调 **2 个半音**，速度不变（ffmpeg `rubberband=pitch=0.8909`，或 `asetrate` + `atempo`）。
3. C 同样降调，提前 60 毫秒进入，叠在下面。
4. 水下感：低通 5.5 kHz（12 dB/oct）的一份与原声按 40:60 混合；再加暗混响，湿声约 22%，尾音约 1.8 秒。S16、S17、S18、S20 四条**不做低通，混响减半**，它们要像人。
5. **Ogg Vorbis**（libvorbis，`-q:a 6`），**单声道、48 kHz**；响度 **−16 LUFS**，真峰值 ≤ **−1 dBTP**；开头静音剪到 50 毫秒，结尾留到混响尾音衰减完，不要硬切。不要用 Opus。

## 输出

```
_tools/daath_ref/vo/
  takes/<编号>_1.ogg  <编号>_2.ogg  <编号>_3.ogg     共 69 个
  REVIEW.md          一张表：编号 · 场合（when）· 英文台词 · 三个 take 的时长（秒，一位小数）
  picks.json         {"<编号>": 1, ...} 先全部填 1，用户听完改
  SOURCES.md         模型名与版本、实际用的声线、生成日期，以及这句声明：
                     "The English voice-over in the Da'at trial is AI-generated (OpenAI text-to-speech); it is not a human voice."
```

## 自检（全部通过才算完成）

1. 23 个编号 × 3 个 take 全在，都以 `OggS` 开头、编码 vorbis、单声道、48 kHz（`ffprobe`）。
2. 响度 −16 ± 1 LUFS，真峰值 ≤ −1 dBTP（`ffmpeg -af ebur128=peak=true`）。短于 1 秒的几条（S04、S12）测不准积分响度，用整条的 momentary 最大值核对。
3. 每个 take 0.4～12 秒。
4. REVIEW.md 里的英文与 lines.json 逐字一致。

任何一项没过，在 REVIEW.md 末尾写明原因，不要跳过。

## 不要做的事

- 不改 lines.json 和项目里任何别的文件。
- 除了生成所需的 API 调用，以及环境里缺 ffmpeg 时安装它，不下载任何东西。
