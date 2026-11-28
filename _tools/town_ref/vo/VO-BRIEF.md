# 城镇与新手村：英语配音生成任务

只生成音频，不改项目代码；只在 `_tools/town_ref/vo/` 里写文件。全程用中文写报告。

## 背景

《破碎大陆》的城镇（新手村）里，神父、村长、审判官、边缘者、女巫和镇民会在福利、支线和三场全村副本里说话。字幕中英双语，配音只配英语（和序章、新手开局一样）。台词原稿是 `_tools/town_ref/lines.json`（**不要改它**），共 109 条，全部 `"voiced": true`。

## 怎么生成

- 用 OpenAI 的语音合成（`gpt-4o-mini-tts`，或当时更好的、支持 `instructions` 表演指令的语音模型）。API 密钥从环境变量取，不要写进任何文件或日志。
- 朗读文本 = 该条的 `en` 字段，一字不改。不要读出编号，不要加语气词。
- 表演指令 = 下面的「角色基调」+ 一个空格 + 该条的 `direction` 字段。
- **每条生成 3 条（take）**，让用户挑。
- 吟游诗人（BD01～BD03）是「半唱半念」：模型唱不了就用有节奏的吟诵，在 REVIEW.md 里注明。

| speaker | 角色 | 声线（voice） | 角色基调（每条都加在 direction 前面） |
| --- | --- | --- | --- |
| priest | 神父 | echo | A village priest in his sixties: kind, patient, a little tired, speaks like he has buried many people and still believes. |
| elder | 村长 | alloy | A plain-spoken village elder: practical, warm, a farmer's voice, worried about his people. |
| inquisitor | 审判官 | cedar | A Church inquisitor: cold, precise, never shouts; every sentence sounds like a verdict. |
| edgewalker | 兜帽人 | verse | A senior Edgewalker hiding in plain sight: low, quick, wry, a man used to running. |
| witch | 女巫 | shimmer | A wounded young woman the Church calls a witch: tired, clear, unafraid; quiet anger under it. |
| farmwife | 农妇 | coral | A busy farm woman gossiping over a fence: fast, a bit nervous, lowers her voice for secrets. |
| farmer | 农夫 | ash | A gruff farmer: slow, few words, superstitious. |
| youth | 少年 | nova | An excitable teenage boy who repeats rumours as if they were adventures. |
| bard | 吟游诗人 | ballad | A wandering bard singing a fragment of an old song, unaccompanied, half-spoken, half-sung. |
| watchman | 守夜人 | onyx | An old night watchman: hoarse, steady, a lantern-carrier who has seen strange things. |
| child | 孩子 | marin | A lost child of about eight: small voice, shy, then brave. |
| servant | 罪仆 | sage | A minor demon of the Seventy-Two speaking through candle smoke: soft, courteous, tempting, never hurried. |

声线名以生成时模型实际提供的为准；某个声线不可用时，挑最接近「角色基调」的一个，并在报告里写明换成了什么。同一角色的所有台词必须用同一个声线。

## 后期处理

所有 take：转成 **Ogg Vorbis**（libvorbis，`-q:a 6`），**单声道、48 kHz**；响度归一到 **−16 LUFS**（integrated），真峰值不超过 **−1 dBTP**；首尾静音各剪到 50 毫秒。不要用 Opus。

## 输出

```
_tools/town_ref/vo/
  takes/<编号>_1.ogg   <编号>_2.ogg   <编号>_3.ogg     每条三个 take（共 327 个文件）
  REVIEW.md          一张表：编号 · 角色 · 英文台词 · 三个 take 的时长（秒，一位小数），方便用户逐条试听
  picks.json         {"PR01": 1, ...} 先全部填 1，用户听完改成想要的 take
  SOURCES.md         模型名与版本、每个角色实际用的声线、生成日期，以及这句声明：
                     "The English voice-over in the towns is AI-generated (OpenAI text-to-speech); it is not a human voice."
```

## 自检（全部通过才算完成）

1. 109 个编号 × 3 个 take 全部存在，都以 `OggS` 开头、编码 `vorbis`、单声道、48 kHz（用 `ffprobe` 核对）。
2. 每个文件的响度在 −16 ± 1 LUFS，真峰值 ≤ −1 dBTP（`ffmpeg -af ebur128=peak=true` 核对）。
3. 每个 take 的时长在 0.4～15 秒之间；超出的写进报告。
4. REVIEW.md 里的英文与 lines.json 的 `en` 逐字一致。

任何一项没过，在 REVIEW.md 末尾写明原因，不要跳过。

## 不要做的事

- 不要改 lines.json，也不要改项目里任何别的文件。
- 除了生成所需的 API 调用，以及环境里缺 ffmpeg 时安装它，不要下载任何别的东西。

## 接入（给集成方，不是配音方的任务）

`picks.json` 里选中的 take 在构建时拷进资源包，登记成 `rpg:vo.town.pr01`…；没有 picks.json 或文件缺失时，那一句只显示字幕。
