# 宣传片素材来源

本项目开源免费、非商业，与 Mojang Studios、Microsoft 没有关联。
Minecraft Dungeons 的音乐、贴图和音效版权归 Mojang Studios 所有。片尾已逐条署名。

## 配乐：Minecraft Dungeons 原声

这些文件取自 minecraft.wiki，是 Mojang 要求截短后的 30 秒版本。站点的 Cloudflare 会拒绝 curl，所以是在内置浏览器里打开 `Dungeons:Music` 页面，再从页面里下载 `/images/<文件名>`。文件存在 `_promo/assets/music/`，不进仓库。

| 文件 | 曲目 | 作曲 | 字节 | SHA-256（前 16 位） | 片中位置 |
|---|---|---|---|---|---|
| `Bgm_env_titleScreen2DMain-001.ogg` | Finnbacka（标题画面） | Peter Hont | 313617 | `0814b15e31616d3e` | 0–12s 开场 |
| `S1_bgm_env_thtoBossLoop-001.ogg` | The Tower · Boss | Peter Hont | 367614 | `46dda8fd6a239da5` | 12–30s 装备 |
| `Bgm_env_deteNamelessFightLong-001_soundWave.ogg` | Necromancer（无名者之战） | Johan Johnson | 246473 | `d5f3189bb1562cdd` | 30–52s 恶魔生态 |
| `Bgm_mob_obpiBossStage1Loop-001.ogg` | The Arch-Illager · Stage 1 | Peter Hont | 381132 | `930b2263ecd227ad` | 52–82s 契约与收尾 |

每个文件的来源是 `https://minecraft.wiki/images/<文件名>`。曲目信息见 <https://minecraft.wiki/w/Dungeons:Music>。

## 音效

音效直接复用仓库里已有的参考素材，来源分别记在：
- `_tools/beelzebub_ref/SOURCES.md`：无名者，共 4 段
- `_tools/tower_guard_ref/SOURCES.md`：塔卫，1 段

片中具体用了哪几段，见 `render.py` 里的 `SFX_PLAN`。

## 画面

- **武器、符文、契约的图标**：从仓库里的 `TRALANCER-RPG-图鉴.html` 导出，本项目自绘。
- **七本罪约契约书的原画**：取自 `_tools/pact_art/`，本项目自绘。
- **实机镜头**：在本项目的数据包和资源包里录制，用 ReplayMod 渲染，光影是 Complementary Reimagined。
- **字体**：本机 Windows 自带的思源宋体（NotoSerifSC）、Georgia 和 Times New Roman。

## 录制工具

工具都装进了 PCL 实例 `1.21.11-Fabric 0.19.3`，下载后都用 Modrinth API 给出的 SHA-512 校验过。

| 文件 | 来源 | 字节 |
|---|---|---|
| `mods/replaymod-1.21.11-2.6.28.jar` | <https://modrinth.com/mod/replaymod> | 15799987 |
| `shaderpacks/ComplementaryReimagined_r5.9.3.zip` | <https://modrinth.com/shader/complementary-reimagined> | 553397 |
| `ffmpeg/bin/ffmpeg.exe` | 复制自本机 Python 的 `imageio_ffmpeg`（ffmpeg 7.1），供 ReplayMod 渲染用 | — |
