# 新手开局英语旁白来源

制作日期为 2026-11-23（新加坡时间）。朗读原稿为 `_tools/onboard_ref/lines.json` 的 W01～W10。

## 声线与模型

实际声线取自序章现用的 N01 Take 2。它沿用了最初由 OpenAI fable 生成的合成旁白。新台词分别参考 N01 Take 2 和 N04 Take 2 的发音与节奏，以延续同一讲述者的声线。W09 的第一版还参考了同句第二版的连读，帮助读清 “broke into”。

制作使用本机已有的 qwen-tts 0.1.1 和 Qwen3-TTS-12Hz-0.6B-Base。模型权重 SHA-256 前 16 位为 180b3b10eb1c9f1b。三十条旁白均为本次独立合成，未调用付费 API。

朗读文本与表演指令分别输入。每句先使用简报的角色基调与原稿 direction，再加入与序章一致的贴近、低沉和词组连读要求。W03 在 “war in heaven” 上加重，W07 在 “like empty houses” 放慢，W08 贴近耳语，W09 的两次 “fell” 逐步积累，到 “beneath your feet” 收低。

## W10 专名

拼读目标为 EH-rets ha-sheh-vah-REEM。Take 1 使用 Eretz Ha-sheh-vah-reem。Take 2 使用 Eretz Ha-Shevarim。Take 3 使用 Eretz Ha-sheh-vah-reem。三个版本都完整生成了这一句。

## 音频处理

保留各版录音自身的语速和音高。用现有 FFmpeg 将音频整理为 48 kHz 单声道，以 libvorbis 质量参数 6 编码。响度与真峰值根据解码后的 Ogg 复测，首尾静音按 −50 dBFS 测量。

## AI 配音声明

> The English voice-over in this edition of the onboarding narration is AI-generated using Qwen3-TTS, with an earlier synthetic narrator voice reference originally generated using OpenAI text-to-speech. No human performer recorded these lines.

简报为直接使用 OpenAI 合成的版本指定了以下声明。本版的实际合成来源见上文。

> The English voice-over in the onboarding narration is AI-generated (OpenAI text-to-speech); it is not a human voice.
