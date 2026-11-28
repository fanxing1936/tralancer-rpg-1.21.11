# 补件（2026-11-28）：英雄底子的城镇 NPC 各换一张皮肤 + 两个食物图标

用户原话：「npc的基座皮肤都是一个皮肤，每个都不同的换一下」「这些npc给你的物品美术风格没有统一」。

## 1. 皮肤（贴图，只动 `prepare_heroes.py` 的皮肤选择，然后重出成品）

现在六套英雄底子的城镇外观都用 `SK_Player_Master` + `T_Valorie_Skin`，脸、手、皮肤完全一样：
`town_priest`、`town_bard`、`town_watchman`、`town_witch`、`town_edgewalker`、`town_inquisitor`。

要做的：

- 在 `prepare_heroes.py` 里给每个 key 指定一张**不同的地下城原作英雄皮肤**（`T_*_Skin.png`，从同一份英雄导出的 `assets` 里找，
  比如 Hal、Hex、Baako、Hedwig、Tyler 等，Valorie 最多留给其中一个）。皮肤要和角色身份相称（神父年长、和善；吟游诗人年轻；
  守夜人粗犷；女巫、边缘者阴沉；审判官冷硬）。只换 `MI_Valorie` 那个材质槽的贴图覆盖，网格、骨架、盔甲、配色、动作全部不动。
- 重新运行生成，覆盖这六个 `../town_<key>_dungeons_ref/`（`atlas.png`、`.bbmodel` 等），`SOURCES.md` 里写明改用的皮肤名。
- 若某张皮肤的 UV 与 `SK_Player_Master` 不合（贴上去错位），换另一张，不要手画修补。
- 乡民（`SK_Villager` 的长者、农妇、农夫、少年、孩童）已经各有贴图，不用动。
- 做完在 `REPORT.md` 末尾追加一节，列出每个 key 用了哪张皮肤，附一张六人并排的预览 `_work/skin_review.png`。

## 2. 两个食物图标（放到 `../town_ref/art/`）

规格同 `town_ref/ART-BRIEF.md`：16×16，Alpha 只用 0/255，左上光、和现有 `ration`、`welfare_pack`、`home_scroll` 一套。

| 文件名 | 画什么 |
| --- | --- |
| `rye_bread.png` | 教堂分的黑麦面包：一条深褐色的圆头面包，表面三道斜割口，割口露浅色面心 |
| `smoked_meat.png` | 腌熏肉：一块用麻绳捆着的深红褐色熏肉，一侧露一段白色脂肪边 |

在 `town_ref/art/REPORT.md` 末尾追加一节。

## 不要做

- 不要运行 `build.sh`，不要改 `rpg/`、`resourcepack/` 或任何 `add_*.py`；不要动别的模型。
