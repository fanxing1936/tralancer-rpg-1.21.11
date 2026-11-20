# 米迦勒战单簇圣焰交付报告

[holyflame_sheet.png](holyflame_sheet.png) 包含 **8 帧单簇圣焰，1 行 × 8 列，从左到右**。实际尺寸为 **2172 × 724 px**，格式为 RGBA PNG。内置 `image_gen` 共生成四版，交付第 4 版原图，生成时开启 `transparent_background: true`。复制前后 SHA-256 一致。

## 验收结果

| 项目 | 实际结果 |
| --- | --- |
| 火焰与循环 | 每帧可辨一簇独立的侧视圣焰，有白热核心、圆底和摇摆的阶梯状火舌。第 3、7 帧附近可见方形火星。第 8 帧卷回、第 1 帧抬起，静态观察可接续。循环未实际播放。 |
| 单元与基线 | 原画布为 3:1，含纵向留白。按等大的 **271 × 271 px** 逻辑单元检查，首格左上角为 `(2, 273)`，水平步长为 271 px。按 Alpha ≥ 224 计，八帧主体底部均在 `y = 543`，底边中心在各格内漂移约 3.5 px。仍有低 Alpha 像素越出逻辑格。 |
| 32 × 32 阅读目标 | 按上述逻辑格只读采样，八帧主体均触及采样网格的最后一行。交付文件保留生成尺寸。 |
| 帧间全透明空隙 | 七处间隙肉眼可辨，但散点打断了透明带。从左到右，主体间最长连续全透明列分别为 **3、3、3、4、9、13、3 px**，未达到明显全透明间隔的要求。 |
| 六色色板与硬边 | 在 287,152 个 Alpha > 0 的像素中，**99.87%** 的 RGB 超出指定六色，**99.38%** 为半透明。可见方块与阶梯轮廓，但存在软边和杂点，严格色板、硬边及外缘棋盘式抖动均未通过。 |

第 1 版的帧间杂点较多，第 2 版收紧了轮廓和基线，第 3 版扩大了主体间距但仍有明显散点。选用第 4 版是因为它的圆底和火舌形变更清楚，八帧主体基线一致，七处帧间都能测到连续透明列。交付图保留内置工具生成的原始像素。

## 交付版本的实际提示词

```text
A game art PNG sprite sheet, transparent background. One row of exactly eight little 8-bit palette-limited pixel icons, all part of one looping holy fire animation. Use the widest panorama option. The eight icons align on one baseline with equal spacing, each centered in its own identical invisible square, all touching the bottom of the square. Only the one slim strip of squares is occupied; upper and lower canvas margins are empty. Allow extremely wide fully transparent spaces between the icons. Each flame is about 20 pixels wide and 28 pixels tall when seen on a 32×32 pixel grid. Use the visual language of flat, opaque square mosaic tiles. Each tile is a hard square with a single uniform color. Just six colors, white #FFFFFF, warm white #FFF5EE, peach #FFD0BD, coral #FF805F, vivid red-orange #FF3300, and deep red #7A1600. Make each silhouette a bold solid cutout with a small solid white core, layered broad fills of those colors, and a few checker-dithered pixels at the tongue tips only. Cutout transparency is strictly all or nothing. No stray pixels anywhere. Design the poses as eight sequential phases of one fire of the same size: centered upright tongue, tongue rising right, rightward curl with one square spark, tongue turning inward, centered upright tongue, tongue rising left, leftward curl with one square spark, tongue turning inward toward pose one. The broad rounded base is identical and anchored in every pose, with only the two upper flame tongues changing silhouette. Wide blank gaps contain zero ink. No soft effects, no cast shadows, no ground, no logs, no gray backdrop, no checkerboard backdrop, no visible dividers, no lettering.
```
