# 序章英语配音来源

本版在 2026-11-22（新加坡时间）制作。英语台词取自原稿中 21 条需要配音的 en 字段。本版使用本机已有的 Qwen3-TTS 和音频处理工具，未产生 API 费用。新生成的录音将表演指令与朗读文本分别输入。

## 角色与表演

| 角色 | 音色参考 | 本版的表演方向 |
| --- | --- | --- |
| 旁白 narrator | 上一版各句的 Take 1，原始声线 OpenAI fable | 经历过往事的老人，在闭室内贴近听者低声开口。词组连读，回忆涌上来时音调抬起，在句末回落。 |
| 路西法 lucifer | 上一版 D01_1，原始声线 OpenAI ash | 保留温暖、自信的男中音。轻声快速说到转折，拒绝时收低，命令时短促有力。 |
| 米迦勒 michael | 上一版 M02_1，Qwen3 设计的角色音色 | 威严中带着疲惫和惋惜。战吼短而有起落，审判台词低沉且有清楚的辅音。 |
| 别西卜 beelzebub | 上一版 D02_1，原始声线 OpenAI ballad | 保留粗粝感，语气漫不经心，几个短词连成一口气。 |
| 贝利尔 belial | 上一版 D04_1，Qwen3 设计的角色音色 | 把柔滑、略带嘲意的声音放到低音区。问句轻挑一下，笑意在结尾收住。 |
| 玛门 mammon | 上一版 D06_1，Qwen3 设计的角色音色 | 像贴近对方谈一桩不愿让人听见的交易。虚词带过，落在条件和筹码上的重音干脆。 |
| 敌基督 antichrist | 与路西法共同使用上一版 D01_1 | 保留同一人的音色，主声低落、肯定，独立录制的气声耳语跟随同一句话。 |

## 生成与混音

- 本机使用 qwen-tts 0.1.1。表演参考使用 [Qwen3-TTS-12Hz-1.7B-VoiceDesign](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign)，参考音色合成使用 [Qwen3-TTS-12Hz-0.6B-Base](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base)。两个本地模型权重的 SHA-256 前 16 位依次为 `391e8db219f292c5` 和 `180b3b10eb1c9f1b`。
- 各句分别给出连读、重音和音调转折指令。M03 另参考上一版该句较清楚的读法，以保留 “rebuke” 的词尾。每句保留三种独立表演。新录的三个方向分别偏向克制的叙述、中段加紧、转折时略微放开。
- 后期以同编号上一版的声音为基准调整音高和节奏，保留共振峰和自然的句内起伏。部分台词加入极轻的暗色早期反射。低声短句优先保留起音和尾辅音，采用较轻的处理。
- X01 每个 take 都有各自生成的主声与耳语。在角色音区调整之后，两层均额外降调三个半音。耳语按均方根电平校准至主声下方 12 dB。暗色卷积混响使用约 55 毫秒预延迟、2.5 秒衰减，干湿电平匹配后按 70∶30 混合。
- 成品采用 libvorbis 质量参数 6 编码。各 take 的时长、试听入口及最终 Ogg 的实测范围见 [REVIEW.md](REVIEW.md)。上一版采样来源和原文件均保存在 [上一版配音.zip](上一版配音.zip)。

## 本版采用的录音

63 个成品中，有 39 个取自本次新生成的表演，另有 24 个使用上一版相同角色、相同编号的独立表演，重新处理了音区、句内起伏和语速，以保留吐字与人物声线。

沿用并重新处理的版本为 `D04_2`、`D05_1`、`D05_2`、`D05_3`、`D06_1`、`D06_2`、`D06_3`、`E03_2`、`E03_3`、`M01_1`、`M01_2`、`M01_3`、`M02_1`、`M02_2`、`M02_3`、`M03_1`、`M03_2`、`M03_3`、`M04_1`、`M04_2`、`M04_3`、`X02_1`、`X02_2`、`X02_3`。

## AI 配音声明

> The English voice-over in this edition of the prologue is AI-generated. It uses Qwen3-TTS and earlier synthetic performances or voice references, including voices originally generated with OpenAI text-to-speech. No human performer recorded these lines.

原简报为上一版中直接用 OpenAI.fm 生成的录音指定了以下声明。

> The English voice-over in the prologue is AI-generated (OpenAI text-to-speech); it is not a human voice.
