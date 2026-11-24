# 圣徽、罪印与三组技能特效

## 地下城原版素材

从本机《Minecraft Dungeons》游戏包筛出 10 张透明 PNG，原尺寸收在 [dungeons/](dungeons/)。以下按技能列出可取用的部件。五张按简报绘制的完整构图仍在本目录，切帧坐标见下文。

| 用在哪里 | 原版图 | 取用方法 |
| --- | --- | --- |
| 圣徽 | [爱之勋章物品图](dungeons/T_LoveMedallion_GearIcon.png)、[圆形准星](dungeons/T_Target.png)、[星光图集](dungeons/T_Stars_16.png) | 勋章的金属包边和挂耳适合做吊坠参考，原中心是粉红心，外框呈菱形。需要简报里的圆徽时，可取准星的圆框和四向短线，再叠星光图集右上角的四芒星。 |
| 罪印 | [紫水晶](dungeons/T_Amethyst.png) | 原图是 16×16 的三尖晶簇，有清楚的紫色明暗切面。[重绘的罪印](sin_sigil.png) 借用晶面的阶梯边与明暗关系，把高光收在倾斜石块边缘，中央留给血红刻印。 |
| 圣链 | [原色金链](dungeons/T_Gold_Chain.png)、[锁链附魔链环](dungeons/T_Chain.png) | 金链自带四档金色。画布 16×16，链条实际在最左 5 列，用作重复链节时取左上角 5×16。附魔链环为 10×6 的灰白横段，可染白金。原作的锁链粒子通过 `PS_Chains_Beam → MI_Chain → T_Chain` 沿两端连线重复贴图；三股锁链收拢和末帧闭锁可用 [圣链六帧图](holy_chain_sheet.png)。 |
| 断罪印 | [伤害光环的目标标记](dungeons/T_DamageAuraTarget.png)、[星光图集](dungeons/T_Stars_16.png) | 标记出自 `AllyDamageBoost`，是 15×15 的四角白色括号，适合套在受印目标外侧，星光可以点亮秤轴。检索审判、天平、交易、附魔及古代狩猎符文后，未找到带秤臂和双盘的原图。主轮廓采用 [天平四帧图](brand_sheet.png)。 |
| 深渊之口 | [紫黑虚空扩散图集](dungeons/T_Circle_Full_Void_15_spritesheet.png)、[完整像素螺旋](dungeons/T_PixelSpiral.png)、[小螺旋](dungeons/T_SpiralSmall.png) | 虚空图集可直接取前六格作裂口出现时的地面扩张层。11×11 螺旋有半透明边，可叠在暗色中心后染紫、旋转；16×16 小螺旋带二值透明，适合小粒子。原图的扩散层没有齿圈，要表现獠牙开合可用 [深渊六帧图](abyss_maw_sheet.png)。 |

### 原图取格

- **虚空扩散**的原图为 64×32，4 列 × 2 行，每格 16×16。从左上开始按行读，六个有效格的左上角依次为 `(0,0)`、`(16,0)`、`(32,0)`、`(48,0)`、`(0,16)`、`(16,16)`。后两格完全透明。各有效格可见像素数依次为 5、37、89、137、177、177，最后两幅颜色图样不同。游戏材质引用了这张图，现有导出信息未标明播放速度或循环次序。
- **星光**的原图为 32×32，2 列 × 2 行，每格 16×16。右上 `(16,0)` 为清楚的十字星，左下 `(0,16)` 星形最大、射线最多。右下是斜向小星，可单独取用。四格是四种可选星形。

两处另有原版模型可查。罪印的碎石轮廓可参考支配之球碎片 `/Game/Decor/Prefabs/Cinematics/SK_OrbOfDominanceShardLoopAnimation`，原作的发光来自材质 `MI_OrbOfDominanceShard`，单独导出的径向渐变看不到石片外形。深渊的齿形和咬合可参考 `/Game/Actors/Characters/Enemies/Illagers/Evoker/Fang/SK_Evoker_Fang` 及同目录 `Animations/Evoker_Fang_Snap`。它的 64×64 贴图是铺在模型表面的 UV 图。

### 来源核对

下表为原包 `Dungeons/Content/` 下的包路径，扩展名均为 `.uasset`。交付的 PNG 已逐份和本机导出件比对，文件字节一致。8 张仅含全透明和全不透明两档 Alpha；星光与完整像素螺旋保留了原作的半透明。

| PNG | 原包路径 | 原尺寸 |
| --- | --- | --- |
| [T_LoveMedallion_GearIcon](dungeons/T_LoveMedallion_GearIcon.png) | `Actors/Items/LoveMedallion/T_LoveMedallion_GearIcon` | 24×24 |
| [T_Target](dungeons/T_Target.png) | `Effects/Materials/Target/T_Target` | 15×15 |
| [T_Stars_16](dungeons/T_Stars_16.png) | `Effects/Materials/Stars/T_Stars_16` | 32×32 |
| [T_Amethyst](dungeons/T_Amethyst.png) | `Effects/Flairs/HealingFlairs/02/T_Amethyst` | 16×16 |
| [T_Gold_Chain](dungeons/T_Gold_Chain.png) | `Content_DLC3/Decor/Prefabs/_Mountains/Gale_Sanctum_Props/GS_Lantern_Hanging_01/T_Gold_Chain` | 16×16 |
| [T_Chain](dungeons/T_Chain.png) | `Components/Enchantments/Chains/T_Chain` | 10×6 |
| [T_DamageAuraTarget](dungeons/T_DamageAuraTarget.png) | `Components/ArmorProperties/AllyDamageBoost/T_DamageAuraTarget` | 15×15 |
| [T_Circle_Full_Void_15_spritesheet](dungeons/T_Circle_Full_Void_15_spritesheet.png) | `Decor/Prefabs/_End_Structures_/LiquidVoid/T_Circle_Full_Void_15_spritesheet` | 64×32 |
| [T_PixelSpiral](dungeons/T_PixelSpiral.png) | `Effects/Materials/Generic/T_PixelSpiral` | 11×11 |
| [T_SpiralSmall](dungeons/T_SpiralSmall.png) | `Content_DLC6/VFX/T_SpiralSmall` | 16×16 |

## 按简报绘制的五张完整构图

两件手持物由绘制米迦勒双武器与羽毛的会话分别重绘。按用户在绘图会话补充的要求，两张成品均为 **16×16 透明 PNG**。绘图先参考地下城原图的轮廓与材质，再结合此前的双武器与羽毛画法。第三轮加强磨损、凿痕和明暗对比，随后在 16×16 网格收色、清理透明边和整理关键像素。三张技能序列的尺寸与取格方式见下文。

| 资产 | 交付 PNG 尺寸 | 帧数与使用方式 | 单帧目标 | 生成尝试 / 采用 |
| --- | --- | --- | --- | --- |
| [圣辉（项目名「圣徽」）· holy_sigil.png](holy_sigil.png) | 16 × 16 | 单张。暗金凹面衬托白星，外圈的短高光形成磨亮的金边，顶部留出挂耳孔。 | 16 × 16 | 本次重绘 3 次，采用第 3 张后整理像素。此前旧稿 1 次。 |
| [罪印 · sin_sigil.png](sin_sigil.png) | 16 × 16 | 单张。斜向深紫石块上刻有血红倒五边形，左上沿有亮紫断面，下缘保留深色缺口。 | 16 × 16 | 本次重绘 3 次，采用第 3 张后整理像素。此前旧稿 1 次。 |
| [圣链 · holy_chain_sheet.png](holy_chain_sheet.png) | 2172 × 724 | 6 帧，单次。三股链条靠拢，卷成闭环，第 6 帧下方锁扣发亮，可停在该帧。 | 32 × 32 | 2 次 / 第 2 张 |
| [断罪印 · brand_sheet.png](brand_sheet.png) | 2172 × 724 | 4 帧，循环。天平依次左低、回正变亮、右低、回正减光。 | 16 × 16 | 2 次 / 第 2 张 |
| [深渊之口 · abyss_maw_sheet.png](abyss_maw_sheet.png) | 2172 × 724 | 6 帧，循环。俯视漩涡里的尖齿向内卷合，第 4 帧开口最小，随后重新张开。 | 32 × 32 | 2 次 / 第 2 张 |

## 切帧坐标

坐标原点在原图左上角。每一行使用统一的方形取样框，每帧沿用同一个 Y 坐标和边长。用这些框能保留动作本身的位移，避免按每帧轮廓分别裁边造成跳动。

| 序列图 | 各帧左边界 X | 上边界 Y | 方框边长 | 相邻主体的最小水平间距 |
| --- | --- | ---: | ---: | ---: |
| 圣链 | 0、362、724、1086、1448、1810 | 181 | 362 | 84 px |
| 断罪印 | 0、543、1086、1629 | 90 | 543 | 100 px |
| 深渊之口 | 58、406、754、1102、1450、1798 | 210 | 320 | 55 px |

## 像素核对

三张序列图的主体均为单行，按上表裁格后完整落在各自方框内。间距取 Alpha 大于 127 的主体边界计算。按目标尺寸的像素中心作最近邻抽样，16 个特效姿态都保留了四周留白。

两张成品在 16×16 网格上逐像素检查。圣辉使用简报的 5 色，罪印使用 8 色，两图所有像素的 Alpha 都是 0 或 255。白星从暗金底上分出，紫石上的红线围住了中央的深色石面。

三张序列图有透明通道。检测到帧间仍散布少量非零 Alpha 像素，着色区域也含指定色表之外的过渡色。第二次生成重点收紧了这些约束，仍未达到逐像素限色和帧间 Alpha 全零。制作组切缩时可先以 Alpha 128 为界清理遮罩，再将可见像素归入简报对应的圣力五色或魔力八色。

<details>
<summary>查看五张入选原图的生成提示词</summary>


### holy_sigil.png

> New 16x16 Minecraft item sprite, drawn in the EXACT coarse pixel craft of these references. Image1 lantern shows the desired bold light-dark contrast and chunky old metal; image2 grimoire shows deliberate single-pixel wear and stepped material planes. Draw ONLY ONE round HOLY MEDALLION, not either reference subject.
> VERY IMPORTANT: this is SIXTEEN BY SIXTEEN pixels, not 32 or 64. Every art pixel is one HUGE solid square, every mark follows that single grid. Native 16x16 design enlarged with nearest neighbor. Tiny round gold body around 11-12 pixels across, a very small hollow loop on top. One clear dark brown outline and bottom-right thickness, left/top bright gold bevel, dark-gold recessed center. Raised gold CROSS with a small WHITE FOUR-POINT STAR at its center; gold cross tips show outside white star. A few asymmetrically distributed square edge highlights, two dark square nicks, and one chunky deep groove suggest aged metal. Texture is deliberate coarse single-pixel wear, NOT blurry paper grain. Build light, middle and shadow into distinct abrupt terraces like the reference lantern. Strong contrast from near-white to deep brown; do not leave a huge smooth flat disc.
> Use ONLY #FFFFFF, #FFF2C8, #FFD85A, #C9A646, #5A4410. Entire canvas 16x16 logical squares, keep 1 transparent logical pixel margin on every side, all pixels fully opaque or fully transparent. Place each facet as a connected cluster; sprinkle only a handful of meaningful wear pixels. Straight front view. No soft gradients, no glow, no realistic lighting, no interpolation, no curved vector lines, no tiny detail smaller than one logical pixel. Single item on genuine transparent background, no frame, no text, no background. A convincingly physical tiny relic with depth and rough pixel texture, not a smooth emblem illustration.

### sin_sigil.png

> Create ONLY ONE 16x16 pixel-art Minecraft inventory item: SIN STONE SEAL. Render with the exact chunky native pixel craftsmanship of attached reference1 tide runestone and reference2 grimoire: clear contrast, jagged contour, discrete material planes, purposeful single-pixel texture. NOT a smooth enlarged vector emblem.
> Hard requirement: SIXTEEN BY SIXTEEN logical pixels over the whole square canvas. Each pixel is one huge flat uniformly colored square. Leave 1 transparent pixel margin all sides. Deep purple irregular stone about 11 pixels wide and 13 tall, diagonal with a broken upper shoulder, a chipped corner and a blunt lower point. FOUR CLEAR PLANES: near-black lower-right thickness, deep-purple broad front, mid-purple upper-left flaked face, a few light-violet chipped edges. Include 3-4 coarse pixel pits/chips and two tiny one-pixel cracks. Strong abrupt value changes, visible tactile roughness; no smooth flat slab and no soft shading.
> The front has a large RED HOLLOW DOWN-POINTED FIVE-SIDED SHIELD engraved in the stone, around 6-7 pixels across and 7 pixels tall: flat top, two short near-vertical side edges, two diagonal stair steps meeting at a bottom point. One-pixel to two-pixel coarse stroke, dark empty center. Only five sides, no pentagram, no crossing lines, no stars. Main groove red #C0303C, dark trough #8B0A1E and #3A0610 selectively on lower-right to look CHISELED INTO stone, not a sticker. Most front remains dark purple. Only two pale-violet glints in edge cracks.
> Allowed exact inks ONLY: #120814 #2A0F40 #5B2A86 #A276BE #E2C6F2 #C0303C #8B0A1E #3A0610. Flat square pixels with hard light-dark boundaries. No gradients, no soft light, no glow fog, no microtexture, no blur, no antialiasing. Roughness comes from a few contrast pixels and broad facets like reference. Genuine transparent background. One icon only, no captions, no grid, no frame, no other objects. Native 16x16 design, shown enlarged WITHOUT adding finer pixels.

### holy_chain_sheet.png

> Create a production-ready transparent pixel-art sprite sheet. The delivered PNG has ONE SINGLE HORIZONTAL ROW containing EXACTLY SIX animation frames. Use a wide 3:1 canvas. Center the single row vertically; leave the top quarter and bottom quarter of the entire canvas fully transparent. Divide the width into six equal SQUARE frame cells, the side of each cell is ONE SIXTH the canvas width. Place each sprite entirely within the INNER 70 percent of its own square cell. This leaves broad completely EMPTY transparent vertical gutters between all six sprites. All six frame centers align to the same horizontal axis. No drawn grid or lines. The first frame must have visible chains. No second row.
> 
> The spell animation is three golden holy chains tightening to bind one invisible target. Design for a 32 by 32 pixel game texture, use only a small coarse grid of large square pixels and very few broad hard flat color patches. Chain links are simple chunky 3-pixel hollow square loops, not fine jewelry. The palette is ONLY #FFFFFF, #FFF2C8, #FFD85A, #C9A646, #5A4410. Outline dark gold, gold body, warm-white highlights and small square white glints. Flat hard-edge pixel rendering, radiance conveyed only by crisp highlight pixels on the links. EVERY visible pixel is fully opaque. EVERY empty pixel is fully transparent. NO semitransparency anywhere. NO bloom, NO halo, NO haze, NO soft glow, NO blur, NO antialiasing, NO shadows, NO ambient colored noise, NO detached particles.
> 
> Six square animation frames left to right:
> 1. Three short disconnected strands, upper left, upper right, bottom, aimed at an empty center.
> 2. Three chain strands have grown toward the center, three tips stop around center.
> 3. The three strands curl inward into a broken ring.
> 4. The chain ring is almost closed, three ends approach each other.
> 5. The ring is closed and tightening, simple near-circular chain loop.
> 6. A fully locked compact closed chain ring, a small bright square lock junction at bottom, four white pixel glints on its links. Stable held final pose.
> Keep the same central target scale and same cell center in every frame. The final ring fits in 70% of cell width. Keep every chain, lock and highlight in its cell with spacious full-alpha-zero margins. All objects fully in frame.
> 
> Minecraft Dungeons inspired blocky sprite texture. The six states must be unambiguously countable with WIDE fully transparent gaps. NO text, NO numbers, NO grid, NO background, NO checkerboard. NO red or orange. Five specified colors only. Genuine alpha transparent canvas.

### brand_sheet.png

> Edit this four-frame balance-scale sprite sheet. Preserve exactly the same four scales, same left-to-right poses (left tilted, upright bright, right tilted, upright dim), same equal horizontal spacing and same icon design. Correct the transparency: erase EVERY stray pixel in the empty background and every inter-frame gutter to exact transparent alpha 0. Keep each scale wholly inside its own equal-sized square cell with wide perfectly empty transparent gutters. Transparent pixels should be truly empty, not low-opacity colored dust. Convert all visible parts of the symbols to flat opaque chunky square pixel blocks; only exact solid opaque colors #FFFFFF #FFF2C8 #FFD85A #C9A646 #5A4410. Sharpen the outlines into stair-step pixel-art boundaries and remove smooth gradients, blur, antialiasing and translucent edge fringes. Use an extremely coarse 16 by 16 logical pixel grid per scale. Keep this one wide horizontal strip. Do not add frames or any objects, text, labels, grid, background or shadow.

### abyss_maw_sheet.png

> A production PIXEL ART sprite sheet, EXACTLY SIX complete separated circular abyss vortex symbols in ONE HORIZONTAL ROW. Wide canvas 3:1. The empty background MUST have alpha exactly zero everywhere, including gutters and outer margins, perfectly clean transparency with absolutely no stray pixels, haze or particles. The six symbols occupy six equal 1:1 square cells in a centered horizontal strip, x centers evenly spaced, identical scale. Make symbols smaller than the cells: symbol diameter is only 70% of cell width, leaving wide empty gutters. Leave at least 30 pixels of transparent margin outside the first and last sprite. No visible grid lines. In each square: top-down dark purple rotating abyss hole, central nearly black disk, surrounded by a ring of thick clockwise curved purple arms and SIX chunky triangular teeth pointing into the hole, tiny dark red tooth points. Animation phases successively rotate clockwise in six increments and the aperture gently closes and reopens. Frame 1 open, frame2 medium open, frame3 narrower, frame4 narrow, frame5 medium, frame6 open with advanced rotation so loop continues. Use an extremely coarse 32x32 pixel logical grid per frame. All art should look like a nearest-neighbor enlarged 32x32 game sprite, square stair-step pixel clusters, no fine grain, no speckles. Use EXACT solid flat colors only: #E2C6F2 pale violet, #A276BE violet, #5B2A86 dark purple, #2A0F40 deep purple, #120814 almost black, #C0303C muted red, #8B0A1E red shadow, #3A0610 darkest red. Dark central disk, purple vortex ring, limited pale-violet tooth highlights and tiny red points. Every colored pixel is fully opaque; background pixels fully transparent. No antialiasing, no interpolated colors, no partial opacity, no soft edge, no gradients, no glow, no texture noise, no shadow, no ground, no checkered background, no text or labels. Keep all SIX sprites complete and uncropped, evenly sized and separated by truly transparent gutters.

</details>
