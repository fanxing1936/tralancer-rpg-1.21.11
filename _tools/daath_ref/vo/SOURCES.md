# 达阿特试炼英语配音来源

制作日期为 2026-11-25（新加坡时间）。英语原稿取自 `_tools/daath_ref/lines.json` 中 S01～S23 的 en 字段。

## 模型与声线

使用本机已有的 qwen-tts 0.1.1。Qwen3-TTS-12Hz-1.7B-VoiceDesign 生成音色参考，Qwen3-TTS-12Hz-0.6B-Base 为每句台词生成独立表演。新台词全部由本地模型合成。

A 为本次设计的低男中音，贴近、平静。B 为本次设计的清冷女声，咬字清楚。C 沿用 A 的说话人特征，另用气声耳语参考引导演绎。A、B 分别对应简报中要求的 onyx、sage 声部。

表演指令采用原稿 base、一个空格和各句 direction。耳语另附 whispering, breathy, almost inaudible。

## 合成与后期

女声按男声的实际发声长度匹配，最终采用的女声整句伸缩幅度最大为 7.04%。独立复测 69 条，男女声处理后在 −50 dBFS 阈值处的起音差最大为 16.25 毫秒。按男声 0 dB、女声 −2 dB 配比。对其中 34 个版本进一步对齐了句中音节和停顿。双声整体降调两个半音，语速保持原样。耳语沿用男声身份独立生成，降低其中过强的周期性发声，按男声参考降低 14 dB 后提前 60 毫秒进入。耳语同样降调两个半音。

常规台词用 40% 的 5.5 kHz 二阶低通与 60% 原声混合，暗混响湿声约 22%，衰减时间约 1.8 秒。S16、S17、S18、S20 使用直通声音与约 11% 湿声。所有版本均保留卷积尾音，以 libvorbis 质量参数 6 导出。

## AI 配音声明

> The English voice-over in this edition of the Da'at trial is AI-generated using Qwen3-TTS. No human performer recorded these lines.

简报为直接使用 OpenAI 合成的版本指定了以下声明。本版实际模型与声线来源见上文。

> The English voice-over in the Da'at trial is AI-generated (OpenAI text-to-speech); it is not a human voice.
