# 城镇英语配音来源

制作日期为 2026-11-27（新加坡时间）。朗读稿取自 `_tools/town_ref/lines.json` 的 109 条 `en` 字段。

## 模型与表演

本次采用本机 **qwen-tts 0.1.1**。Qwen3-TTS-12Hz-1.7B-VoiceDesign 生成 12 个角色的固定音色参考，Qwen3-TTS-12Hz-0.6B-Base 读取同一角色的参考音频与声纹，独立采样各 take。全部在本机推理。

| 模型 | 权重文件 SHA-256 前 16 位 |
| --- | --- |
| Qwen3-TTS-12Hz-1.7B-VoiceDesign | `391e8db219f292c5` |
| Qwen3-TTS-12Hz-0.6B-Base | `180b3b10eb1c9f1b` |

逐句表演指令以简报的角色基调、一个空格、原稿 `direction` 开头，再补充角色音域、咬字和录音要求。指令作为单独的文本条件传入 Base，英语朗读文本原样输入。以 12 个样本对比后，采用固定角色参考方案，12 个样本的测量声纹都与指定角色最近。个别发音重录还使用同角色已核对的读法引导咬字，并沿用该角色的固定声纹。吟游诗人 BD01～BD03 使用无伴奏的节奏吟诵。

## 角色声线

| 角色 | 简报中的 OpenAI 声线 | 本机实际参考音色 | 设计基调 |
| --- | --- | --- | --- |
| 神父 | echo | `priest` | 年长男声，温和，中低音带一点粗粝感 |
| 村长 | alloy | `elder` | 年长男声，朴实爽朗，带英格兰西部口音 |
| 审判官 | cedar | `inquisitor` | 干净的男中音，咬字精确，音调克制 |
| 兜帽人 | verse | `edgewalker` | 偏低的年轻成年男声，短句敏捷，带一点沙哑 |
| 女巫 | shimmer | `witch` | 年轻女低音，清楚贴近，情绪收在声线里 |
| 农妇 | coral | `farmwife` | 明亮的成熟女中音，语速较快，像篱边闲谈 |
| 农夫 | ash | `farmer` | 粗粝低男声，略带约克郡口音 |
| 少年 | nova | `youth` | 明亮的少年男高音，语调变化快 |
| 吟游诗人 | ballad | `bard` | 轻男高音，带凯尔特英语色彩，按歌谣节奏吟诵 |
| 守夜人 | onyx | `watchman` | 年长低男声，干哑而稳 |
| 孩子 | marin | `child` | 模拟约八岁孩子的轻柔高声区 |
| 罪仆 | sage | `servant` | 柔和、低沉的中性声线，语速从容，吐字轻软 |
| 旁白（EX01～EX19，2026-11-27） | fable | [序章 N01 Take 2](../../prologue_ref/vo/takes/N01_2.ogg) | 本机 qwen-tts 0.1.1 使用 Qwen3-TTS-12Hz-0.6B-Base，沿用新手开局的同一讲述者。参考音色源自 OpenAI fable。 |

## 后期与检测

使用本机 FFmpeg 9.0.2 整理音频，按 −50 dBFS 测定首尾边界，各留 50 毫秒静音。母带归一到 −16 LUFS，高峰值的片段另用四倍过采样的前瞻限幅，以 libvorbis 质量参数 6 输出单声道 48 kHz Ogg。对最终 Ogg 用 ffprobe 与 `ebur128=peak=true` 逐文件复测。另以本机 faster-whisper 1.2.1 的 small 模型核对英语朗读。

## AI 配音声明

> The English voice-over in the towns is AI-generated using local Qwen3-TTS models. No human performer recorded these lines.

简报为使用 OpenAI 合成的版本指定了下列声明。本批实际使用 Qwen3-TTS，来源见上文。

> The English voice-over in the towns is AI-generated (OpenAI text-to-speech); it is not a human voice.
