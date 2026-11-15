# 首席附魔师素材来源

角色出自《Minecraft Dungeons II》，英文名 The Prime Enchanter。角色与原游戏素材版权归 Mojang Studios、Microsoft 及相关权利人所有。本项目为非商业同人项目，与 Mojang Studios 无关联。游戏素材来源与托管站点分别记录。 [Minecraft 使用指南](https://www.minecraft.net/en-us/usage-guidelines)

## 静态资料

| 文件 | 原件规格 | 用途与来源 |
|---|---|---|
| `originals/MCD2_Prime_Enchanter_(texture).png` | 64×64 RGBA PNG | 建模 UV 所用的原游戏基础贴图。与 MCFUN 独立镜像的 4096 个 RGBA 像素全部一致，包含透明像素。镜像所指资源是 `FrostbiteDesert_Boss/T_Frostbite_Desert_Boss.uasset`。 [Wiki 文件页](https://minecraft.wiki/w/File:MCD2_Prime_Enchanter_%28texture%29.png) · [MCFUN 镜像](https://mcfun.cc/Minecraft-Dungeons-2/assets/database/4625383f9792b14091ce1682.png) |
| `originals/MCD2_Prime_Enchanter_Render.png` | 1000×1000 RGBA PNG | 抬拳三分之四侧视，能核对手套体积、帽袍侧边、下垂披风。 [Wiki 文件页](https://minecraft.wiki/w/File:MCD2_Prime_Enchanter_Render.png) |
| `originals/Prime_Enchanter_render.webp` | 512×512 RGBA WebP | 待机近前方三分之四角度，可补充双臂放下和披风展开状态。MCFUN 与 MetaBot 所载文件逐字节相同。 [MetaBot 角色页](https://metabot.gg/en/minecraft-dungeons-2/bosses/the-prime-enchanter) · [WebP 原件](https://metabot.gg/web/mcd2/mobs/the-prime-enchanter.webp) |
| `originals/bft-pe.jpg` | 1920×1080 RGB JPEG | Mojang 官方《Battle for Tokyo》宣传图。可核对帽饰飘带、披风纵边、拳套蓄力的冰蓝与雷黄配色。 [Mojang 发布页](https://www.minecraft.net/en-us/article/dungeons-ii-battle-for-tokyo) · [JPEG 原件](https://www.minecraft.net/content/dam/minecraftnet/games/spicewood/game-characters/bft-pe.jpg) |
| `originals/dungeons2launch_4.jpg` | 1280×720 RGB JPEG | Mojang 官网游戏上线文章的三人近正面图。中间的首席附魔师可用于核对拳套 L 形发光描边和护腕。 [Mojang 发布页](https://www.minecraft.net/en-us/article/minecraft-dungeons-ii-is-live) · [JPEG 原件](https://www.minecraft.net/content/dam/minecraftnet/games/spicewood/key-art/dungeons2launch_4.jpg) |
| `originals/MCD2_Wallpaper_Prime_Enchanter1080x1920.jpg` | 1080×1920 RGB JPEG | Mojang 官网壁纸 ZIP 的未修改成员。用于观察跳跃蓄拳角度、发光描边，按壁纸页许可作本地个人非商业展示参考。 [Mojang 壁纸页](https://www.minecraft.net/en-us/collectibles) · [ZIP 原件](https://www.minecraft.net/content/dam/minecraftnet/games/spicewood/software/Prime_Enchanter.zip) |
| `originals/MCD2_Credits_artwork_*.png` | 3 张制作人员名单概念图 | 可辅助理解头巾和披风的飘动以及落地动作的轮廓。以最终游戏画面校准实际比例及节奏。 [Wiki 图库](https://minecraft.wiki/w/Dungeons_II:The_Prime_Enchanter#Gallery) |

宣传图的画面左拳为角色右手，呈冰蓝色。画面右拳为角色左手，呈雷黄色。两个静态站点渲染显示褐色包边与灰色未激活拳面。官网宣传图同时显示三条从帽顶向后翻起的蓝色飘带，以及带浅色纵边的蓝披风。

## 动作资料

Minecraft Wiki 角色页列出 11 段动画。搜索索引还保留早期的 `Prime Enchanter` 页面内容。素材清单收录 20 个源文件，11 个 GIF 的 862 帧均完整解码。原件校验值与每帧延时记录在 [source_manifest.json](source_manifest.json)。 [当前角色页](https://minecraft.wiki/w/Dungeons_II:The_Prime_Enchanter) · [早期页面标题](https://minecraft.wiki/w/Dungeons_II:Prime_Enchanter)

| Wiki 原件名后缀 | 帧数 | 原 GIF 帧延时之和 |
|---|---:|---:|
| `Idle.gif` | 24 | 1.00 秒 |
| `Walk.gif` | 22 | 0.92 秒 |
| `Spawn.gif` | 57 | 2.37 秒 |
| `Forward_Strike.gif` | 60 | 2.50 秒 |
| `Fury_Fist.gif` | 166 | 6.92 秒 |
| `Launch.gif` | 95 | 3.96 秒 |
| `Lightning_Slam.gif` | 106 | 4.42 秒 |
| `Overcharge.gif` | 86 | 3.58 秒 |
| `Staggered.gif` | 55 | 2.29 秒 |
| `Summon.gif` | 54 | 2.25 秒 |
| `Death.gif` | 137 | 5.71 秒 |

MCFUN 引用的原游戏资源路径以 `FrostbiteDesert_Boss/Animation/` 为目录，可独立核对 `Forward_Strike`、`Fury_Fist`、`Launch`、`Lightning_Slam`、`Overcharge`、`Summon`、`Staggered`、`Spawn` 的资源身份。过载条目记录中段 `Loop Seconds=5`。具体姿态与片段时长以对应 GIF 为依据。 [原游戏数据公开镜像](https://mcfun.cc/minecraft-dungeons-2/database/mobs/frostbitedesertboss-3cb796eb24/data/)

实机对照可参考 Video Game News 的首发版战斗录制 0:35–3:25、ZaFrostPet 的战斗录像，以及 Ben-Gun 的合集 18:09–21:06。这些链接对应玩家实机录制，可补充临场比例和遮挡视角。 [Video Game News](https://www.youtube.com/watch?v=KorV2SgmFWU) · [ZaFrostPet](https://www.youtube.com/watch?v=DZ4S_rc236A) · [Ben-Gun 合集](https://www.bilibili.com/video/BV1rgap62Eki/)

## 证据范围

目前来源可核对帽袍的可见轮廓、原始基础像素、拳套冰雷手性和不同动作的外观。未定位到公开的原始骨架、完整正交四视图、独立冰雷拳套材质或发光遮罩。发光范围需从官方渲染及动作画面核对，正交侧背视角需参考原贴图展开与 GIF 中的转身帧。

原始数据列有 Wwise 事件 `sfx_mob_FBDBoss_attack_hitmarker_Play`，现有公开资料尚无本角色独立可解码音效文件。正式音效清单以有原件的条目为准。 [事件资源记录](https://mcfun.cc/minecraft-dungeons-2/database/mobs/frostbitedesertboss-3cb796eb24/data/)
