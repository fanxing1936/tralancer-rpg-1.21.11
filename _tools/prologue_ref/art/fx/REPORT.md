# 序章过场特效

三张图均为内置 image_gen 输出的原始透明 PNG，尺寸为 2172 × 724。每张只有一行。下面的坐标以左上角为原点，帧号 `i` 从 0 开始。截取方形单元后，用最近邻缩到 32 × 32 即可。

| 文件 | 帧数 | 单元边长 | 左上角 (x, y) | 使用顺序 |
| --- | ---: | ---: | --- | --- |
| [rift_sheet.png](rift_sheet.png) | 8 | 224 | (24 + 270 × i, 246) | 1 → 8 张开，第 8 帧可停留；8 → 1 闭合 |
| [green_smoke_sheet.png](green_smoke_sheet.png) | 8 | 224 | (24 + 270 × i, 246) | 1 → 8 → 1 循环 |
| [blood_decals.png](blood_decals.png) | 4 | 448 | (48 + 543 × i, 146) | 四张独立使用。依次为血泊、斜拖痕、散滴、半干斑 |

## 32 × 32 核对

按上表在内存试切全部 20 格，以 alpha ≥ 16 统计主体。每格主体完整落在边界内，外侧至少留一像素空隙。裂缝由 59 个可见像素增至 342 个，末帧保留深紫黑的开口和碎亮的浅紫边。绿烟八帧的尾端位于同一高度，末帧接回首帧时轮廓变化了 43 个像素，在其余相邻帧的变化范围内。四种血迹缩小后仍能分别识别。

原图方格间留有 46 像素或 95 像素的间隔。每道间隔均具有完全透明的列，间隔内另有零星 alpha 为 1/255 的像素。原图保留了生成器的边缘透明度。上述裁切和缩小只用于验收，交付的 PNG 与选定的生成源文件字节一致。

## 采用的生成提示词

### 空间裂缝

第一遍定八帧布局与从闭合到张开的轮廓。

```text
Use case: stylized-concept. Deliver the actual production sprite sheet PNG itself on a transparent canvas. Eight tiny evenly spaced 16-bit pixel-art space-rift icons, arranged in a single straight horizontal row, in chronological order from shut to open. Extremely wide composition, like printing eight little glyphs across the waist of a mostly empty page. Each sprite must be MICRO sized: height only 8 percent of page height, and must be visibly shorter than HALF the horizontal distance to the next sprite. Output a landscape image, transparent above, below, and between the eight tiny glyphs. Place exactly eight centers at horizontal percentages 6.25%, 18.75%, 31.25%, 43.75%, 56.25%, 68.75%, 81.25%, 93.75%, all at mid-height. Every icon fits inside its own square with generous margins all around. Actual subject: a vertical fracture in space like a tall jagged door. Read left to right: 1 hairline lilac slash, 2 serrated hairline, 3 narrow dark seam, 4 opening fissure, 5 torn black-violet opening, 6 widening portal, 7 nearly open, 8 fully open with thick void. The fully opened rift is roughly 3 parts wide, 5 parts tall. In all eight, use a stark thin stepped purple rim and a few lavender/white pixel sparks clinging to the edge with transparent gaps. The inside is opaque abyss purple-black #0D0614 and #2A0E3A, outline #7B3FBF and small #C9A0FF, rare #FFFFFF. Vintage tile-game art drawn with a square pencil, at an implied 24 pixels tall each. Integer square pixel clusters only. Hard silhouette meeting completely transparent air, flat spot colors, crisp corners. No painted glow, no gradients, no shadow, no haze, no outlines around cells or labels, no letters, no boxes, no checkerboard background. This is a tiny motif ribbon, not eight large posters. Preserve the huge vacant top and bottom margins and the wide gaps.
```

第二遍将第一遍的原图作为参考，仅增强裂口亮边。

```text
Recolor the supplied game-ready transparent sprite sheet. KEEP the exact layout, wide aspect ratio, empty margins, positions, count of 8, individual sizes and progressive portal silhouettes in the reference. Only recolor the narrow jagged rims all the way round the dark void and the luminous slit at left. Replace one half of the existing mid purple rim pixels with BRIGHT PALE LILAC #C9A0FF and a quarter with OPAQUE WHITE #FFFFFF, in chunky continuous zigzag pencil clusters. Leave enough #7B3FBF to outline the bright lip. Deep void remains #0D0614 and #2A0E3A. Accent the bright side of the rim so the tiny portal reads even when scaled to 32 by 32. All edges remain squared and opaque. Keep all of the original tiny sizes and generous padding, and the eight separate sprites in a single horizontal row. No bloom or atmospheric light, only brighter solid pixel clusters on the border. Transparent background. No text.
```

### 绿烟

```text
Produce a real transparent PNG pixel-art video-game effect atlas, very wide landscape 3:1, one thin horizontal row of EIGHT TINY separate emerald smoke wisps with lots of empty air. Each wisp only 15% of canvas height. Centers exactly at 1/16, 3/16, 5/16, 7/16, 9/16, 11/16, 13/16, 15/16 of the width, all at mid-height. Eight animation poses of ONE living thread of snake-green smoke escaping a spirit, a thin floating S-curve that coils up from one narrow deep-green tail to a broader softly curled but CRISP mint head. Fix the base of each wisp at the identical local center and height; the curl of the tip and the bend halfway along sway over a single eight-phase cycle. The first and last poses differ by only a small angular step so it loops. Like one animated candle wisp, not a beaded snake, plant, animal, flame, or runic icon. Make the body one substantial jade ribbon with two or three chunky ascending pixel bands, 4 to 7 pixels wide at the fullest bend at final 32x32, heights 22-26 logical pixels. Use #00491C forest shadow, #2FA866 emerald middle, #5FD68C snake-green face, and a small crisp #D8FFE6 pale mint highlight atop the curl in every frame. NES-style hard stepped chunky square pixel clusters, completely flat cel-shaded colors. No halo or glows: one crisp silhouette against transparent air; no outline box, no labels, no text. Please keep the eight sprites very small and separated by substantial uninterrupted empty transparent padding to fit square cut cells.
```

### 地面血迹

```text
A wide landscape 3:1 game sprite atlas with EXACTLY FOUR separate small top-down dark blood decal textures in a single horizontal straight row on actual fully transparent air. They are four floor stains only, no figures. Use a tiny 16-bit pixel-art pencil and a flat overhead camera; no perspective or raised edges, dark matte wine-red, no lighting or photographic shine. Same scale and visual center for each equal square cell, align centers at 12.5%,37.5%,62.5%,87.5% of width on the halfway line. Each shape occupies only 35% of the canvas height and remains surrounded by visibly wide transparent margin. Four DISTINCT silhouettes left to right: (1) a broad dense splash puddle with irregular scalloped rim and a few detached square spatters, (2) a long diagonal drag smear with two broken tapering tails, (3) a sparse group of 5 separate small dark droplets, no large central pool, (4) a wide almost flat, half-dried patch of dried blood with scraped-out tiny angular transparent cracks, dark central crust, only two muted red fragments near the edge. This last graphic should look crusted and stippled with broken edges, distinct from liquid splash number one. Only four main tones #3D0505, #5E0A0A, #7A0E0E, #9E1B1B. Keep gritty chunky square pixels with hard silhouette in each stain. The empty floor is 100% alpha zero. No shadows on the floor, absolutely no ground, text, panel borders, color legend or checkerboard. Four game-ready decals, each readable at 32×32.
```

