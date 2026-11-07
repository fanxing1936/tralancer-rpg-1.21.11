# Pact art generation report

## book_t2.png — 二阶「魂誓」

- Tool: built-in image_gen; transparent_background: true.
- Reference: ref_books.png.
- Generated once; copied without image processing. No project code changed.
- Visual review: seven books in requested order, thicker pages, gold corners/spine trim, central colored seals and colored page edges. Fine color variations remain; strict 16×16 alignment and maximum 16 colors per icon are not certified. No regeneration or scripted image modification performed, per BRIEF.md.

### Full prompt

Use case: precise-object-edit. Create ONE transparent PNG sprite sheet for Minecraft item art: tier 2 Soul Oath contract books. Input image is the tier 1 reference: retain its exact family resemblance, diagonal closed-book silhouette, orientation, chunky square pixel texture and single horizontal row of SEVEN books. Upgrade each book with a visibly thicker page block and cover, four dark-gold corner protectors on the front cover, ONE dark-gold spine band, ONE small central rune/seal lit in that pillar's bright accent, and ONE narrow bright-accent line along the page edge. Clearly more precious than tier 1 while still simple 16x16 item icons. No oversized jewels or intricate ornament.
Composition: exactly seven books, evenly spaced in ONE row, no other rows. Each book is designed on its own strict 16x16 logical pixel grid, enlarged nearest-neighbor with each square pixel about 10–12 image pixels. All blocks equal-size and aligned. Each book fills 80–94% of its cell, transparent margins on all sides and obvious fully transparent gaps between books. Wide narrow sprite strip.
Left-to-right pillar order and exact deep main / bright accent colors:
1 Lucifer pride #00491C / #5FD68C;
2 Leviathan envy #1B4F72 / #4F9EF0;
3 Abaddon sloth #6A6A70 / #A7AFC9;
4 Beelzebub gluttony #5A6B1E / #B5D957;
5 Samael wrath #7B241C / #FF5C52;
6 Belial lust #5B2C6F / #D97AD9;
7 Mammon greed #B7950B / #E6A23C.
All metal corners and spine band use dark gold #8F7430 with sparse holy-gold #D4AF37 highlights. Use muted pale pages and deep pillar-colored covers. Upper-left lighting, upper-left highlights, lower-right shadows. Outline two shades darker than each body's hue, never pure black. At most 16 colors per icon. Hard binary pixel edges, no antialiasing, no smoothing, no gradients, no semitransparency. Rune light and page-edge light are solid bright pixel accents with NO bloom or halo. True transparent alpha background; no background, no checkerboard, no cast shadows, no text, no labels, no frame. Preserve the reference book viewing angle and visibly blocky low resolution.


## seals.png — 2026-11-06

- Tool: built-in image_gen; transparent_background=true; one generation, original copied without image modification.
- File: seals.png
- Verification: 2172 x 724; 6590 distinct visible RGB colors; 614899 visible pixels outside the required palette; 625807 partial-alpha pixels; 944388 fully transparent pixels.
- Status: NOT compliant with exact five-color / binary alpha requirements. Visual grid is also not a strict 16 x 16 tile grid. Preserved original because BRIEF prohibits script modifications and limits this task to one generated image. No project code modified.

### Prompt

```text
Use case: stylized-concept.
Create exactly ONE transparent PNG sprite sheet for Minecraft item icons: five grayscale wax seals in ONE horizontal row, evenly spaced, left to right: 1 shield (vanguard), 2 arrow (hunter), 3 chalice (priest), 4 open eye (warlock), 5 axe (executioner). No text or numbers.
Each object is a round wax seal with a jagged irregular toothed wax perimeter and a raised embossed central emblem. All five use the same seal size and visual construction. Front facing. Emblems must be simple and legible at actual 16x16 resolution.
CRITICAL PIXEL GRID: each icon is designed on exactly a 16 by 16 logical pixel grid, each logical pixel a perfectly square equal-sized aligned solid-color block, enlarged about 10 to 12 physical pixels per logical pixel. Use very coarse authentic Minecraft pixel art, not detailed illustration or tiny pixels. Each seal occupies 13 to 15 cells of its 16x16 tile. Entire seals visible, transparent padding on all sides and clear fully transparent gaps between the five icons. Compact single row centered in canvas.
EXACT PALETTE ONLY: #1C1C1C #4A4A4A #808080 #BEBEBE #FFFFFF. No other RGB colors anywhere in visible artwork. These are neutral grayscale recoloring masters. Main wax #808080, outline #1C1C1C, shadows #4A4A4A, raised relief highlights #BEBEBE and #FFFFFF. Light from upper left, shadows lower right. Flat discrete color blocks; hard edges; NO antialiasing, gradients, blur, soft shading, semitransparent pixels or dithering. Alpha must be either fully opaque or fully transparent.
No books or book-shaped objects; no ribbons; no captions, letters, numbers, border, grid lines, checkerboard background, cast shadow, scenery, backdrop, or extra objects. Genuine transparent background.
```

