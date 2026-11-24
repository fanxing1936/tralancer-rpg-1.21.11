# 序章配音：英语配音生成任务

只生成音频，不改项目代码；只在 `_tools/prologue_ref/vo/` 里写文件。

## 背景

《破碎大陆》序章的台词是中英双语，配音只配英语。台词原稿是 `_tools/prologue_ref/lines.json`（由脚本书导出，**不要改它**）。只配 `"voiced": true` 的 21 条：开场旁白 N01～N05、对话 D01～D06、米迦勒 M01～M04、路西法 L01、逃离留言 E01～E03、分离过场 X01～X02。

## 怎么生成

- 用 OpenAI 的语音合成（`gpt-4o-mini-tts`，或当时更好的、支持 `instructions` 表演指令的语音模型）。API 密钥从环境变量取，不要写进任何文件或日志。
- 朗读文本 = 该条的 `en` 字段，一字不改。不要读出说话人名字，不要加语气词。
- 表演指令 = 下表的「角色基调」+ 一个空格 + 该条的 `direction` 字段。
- **每条生成 3 条（take）**，让用户挑。

| speaker | 角色 | 声线（voice） | 角色基调（每条都加在 direction 前面） |
| --- | --- | --- | --- |
| narrator | 旁白 | fable | An old storyteller reading scripture aloud: slow, unhurried, reverent, close to the microphone. |
| lucifer | 路西法 | ash | Lucifer before the fall: a young man's baritone, warm and proud, controlled, rarely raises his voice. |
| michael | 米迦勒 | onyx | The archangel Michael: low, calm, grave authority, like a judge; never sneering. |
| beelzebub | 别西卜 | ballad | Beelzebub: gravelly, lazy, sounds like someone who has eaten too much; unbothered. |
| belial | 贝利尔 | sage | Belial: slow, light, silky, a mocking half-smile in the voice. |
| mammon | 玛门 | verse | Mammon: dry, quick, shrewd, like a merchant counting coins in his head. |
| antichrist | 敌基督 | ash（同路西法） | Lucifer's own voice, but something else speaks through it: slow, almost tender, certain. |

声线名以生成时模型实际提供的为准；某个声线不可用时，挑最接近「角色基调」的一个，并在报告里写明换成了什么。

## 后期处理

- 所有 take：转成 **Ogg Vorbis**（libvorbis，`-q:a 6`），**单声道、48 kHz**；响度归一到 **−16 LUFS**（integrated），真峰值不超过 **−1 dBTP**；首尾静音各剪到 50 毫秒。不要用 Opus。
- **X01（敌基督）额外处理**，每个 take 都做：
  1. 整体降调 3 个半音，速度不变（例如 ffmpeg `rubberband=pitch=0.8409`，或 `asetrate` + `atempo` 组合）；
  2. 用同一句、同一声线、表演指令改成 "whispering, breathy, almost inaudible" 再生成一条耳语，同样降调，以 −12 dB 叠在主声下面；
  3. 加一个大而暗的混响（湿声约 30%，尾音约 2.5 秒）；
  4. 再做一遍响度归一和首尾剪裁。

## 输出

```
_tools/prologue_ref/vo/
  takes/<编号>_1.ogg   <编号>_2.ogg   <编号>_3.ogg     每条三个 take（共 63 个文件）
  REVIEW.md          一张表：编号 · 说话人 · 英文台词 · 三个 take 的时长（秒，一位小数），方便用户逐条试听
  picks.json         {"<编号>": 1, ...} 先全部填 1，用户听完改成想要的 take
  SOURCES.md         模型名与版本、每个角色实际用的声线、生成日期，以及这句声明：
                     "The English voice-over in the prologue is AI-generated (OpenAI text-to-speech); it is not a human voice."
```

## 自检（全部通过才算完成）

1. 21 个编号 × 3 个 take 全部存在，都以 `OggS` 开头、编码 `vorbis`、单声道、48 kHz（用 `ffprobe` 核对）。
2. 每个文件的响度在 −16 ± 1 LUFS，真峰值 ≤ −1 dBTP（`ffmpeg -af ebur128=peak=true` 核对）。
3. 每个 take 的时长在 0.4～15 秒之间；超出的写进报告。
4. REVIEW.md 里的英文与 lines.json 的 `en` 逐字一致。

任何一项没过，在 REVIEW.md 末尾写明原因，不要跳过。

## 不要做的事

- 不要改 lines.json，也不要改项目里任何别的文件。
- 不要配 `"voiced": false` 的条目（界面文字、分离过场旁白 N06～N09 等）。
- 除了生成所需的 API 调用，以及环境里缺 ffmpeg 时安装它，不要下载任何别的东西。
