# 教皇战特效贴图来源

`raw/`、`anim/`、`bar/` 的图由 Codex CLI 的内置 image_gen 绘制，提示词见各目录的 `REPORT.md`，任务书见 `ART-BRIEF.md`、`ANIM-BRIEF.md`、`BAR-BRIEF.md`、`SLASH-BRIEF.md`。
`add_pope_fx_art.py` 把母图缩到像素网格并收进项目色板；REPORT 里的尺寸不符是预期的，最终尺寸由该脚本决定。

| 母图处理 | 说明 |
| --- | --- |
| `orb` | 母图中心是镂空的，脚本补成白色内核 |
| `puddle` | 母图内部接近透明，脚本补成近黑，星空来自原作贴图 |
| `mark_fill` | 序列帧只有裂纹和外缘，脚本加半透明底 |
| `beam` | 序列帧叠在静态光束上，否则远处看着断续 |

原作参考（只作风格参考，版权归 Mojang）：`refs/` 里的三张图，来源见 `../heart_of_ender_ref/SOURCES.md` 和 `../pope_ref/SOURCES.md`。
星空贴图 `MCD_Decal_Puddle_(texture).png` 见 `../heart_of_ender_ref/SOURCES.md`。
血条形状按原作者的 `resourcepack/assets/minecraft/textures/font/story/2/` 横幅，由脚本生成。

`preview.png` 是 2026-11-05 在客户端里的截图（Sodium，无光影）。
