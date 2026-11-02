# 宣传片制作说明

《破碎大陆 · TRALANCER RPG》宣传片的规格：
- 16:9，1920×1080，60 fps，约 82 秒（正片 75 秒，片尾署名 7 秒）
- 实机镜头和动态图形交替剪辑
- 字幕中文为主，下方加一行英文小字
- 配乐用 Minecraft Dungeons 原声

| 文件 | 作用 |
|---|---|
| `storyboard.md` | 分镜：逐镜头的时间、画面、字幕和配乐分段 |
| `SHOTLIST.md` | 实机录制清单，给录制的人看 |
| `SOURCES.md` | 所有外部素材的来源、授权和哈希 |
| `make_datapack.py` → `datapack/` | 拍摄布景数据包，命名空间是 `promo` |
| `install.py` | 把拍摄存档和资源包装进本机实例 |
| `render.py` | 渲染成片：动态图形、实机镜头、字幕和混音 |

不进仓库的目录（已写进 `.gitignore`）：
- `assets/music/`：配乐
- `raw/`：ReplayMod 渲染出的实机镜头
- `build/`：图标、单帧、混音等中间产物
- `out/`：成片

## 环境

- **Python 3.12**：需要 Pillow、numpy、imageio_ffmpeg。ffmpeg 用 imageio_ffmpeg 自带的那份，不需要另外安装。
- **字体**：Windows 自带的 `NotoSerifSC-VF.ttf`、`georgia*.ttf`、`times.ttf`。
- **游戏实例**：本机 1.21.11 实例的位置由 `_tools/mc_env.py` 解析。实例里需要有 ReplayMod、Complementary Reimagined 光影包和 `ffmpeg/bin/ffmpeg.exe`，来源见 `SOURCES.md`。

## 从头重做

1. **取配乐**：按 `SOURCES.md` 的表格，把四个 `.ogg` 放进 `_promo/assets/music/`，然后核对哈希。

2. **生成布景数据包**：

   ```bash
   python _promo/make_datapack.py
   ```

   武器清单从 `_tools/rpg_catalogue.py` 读取，要求正好 31 件。召唤和技能全部调用 `rpg/` 里现成的函数。

3. **装拍摄环境**：先关掉游戏客户端，再运行：

   ```bash
   python _promo/install.py
   ```

   它会做这些事：
   - 把「新的世界」复制成「破碎大陆-宣传片拍摄」，并改掉存档的显示名。
   - 把存档的数据包换成本分支的 `rpg/` 和 `_promo/datapack/`。
   - 把本分支的 `resourcepack/` 复制成 `resourcepacks/tralancer-rpg-promo`。

   它不会改这些东西，因为它们是别的会话的测试环境：「新的世界」「破碎大陆-美术风格检查」「tralancer-rpg」「tralancer-rpg-artstyle」、`options.txt`、`iris.properties`。

   以后数据包或资源包有更新，运行 `python _promo/install.py --refresh` 就行，存档不会重新复制。

4. **录实机镜头**：照 `SHOTLIST.md` 录制，再用 ReplayMod 渲染成 `_promo/raw/S1_land.mp4` 等文件。

5. **渲染成片**：

   ```bash
   python _promo/render.py
   ```

   输出 `_promo/out/tralancer-promo.mp4`。

   - 缺哪个实机镜头，对应位置就画占位卡；S5 用画出来的生命之树代替。这样没有录屏也能出片。
   - 调画面时可以用 `--still <秒>` 只出那一帧，存到 `build/`。
   - `--preview 30` 出 30 fps 的快速预览。

## 修改

- **改分镜或字幕**：`render.py` 里的 `shots()` 一张表管时间、画面和中英字幕。改完同步更新 `storyboard.md`。
- **改配乐分段或音效点**：改 `render.py` 里的 `MUSIC_PLAN` 和 `SFX_PLAN`。
- **改布景**：改 `make_datapack.py`，重新生成后运行 `install.py --refresh`。

## 内容限制

- 画面里的领主只有路西法，也就是参考 Dungeons 无名者做的那个模型。其余六位只以文字出现，例如七宗罪和七柱的名字。
- 圣卫可以出镜。
- 片尾必须保留 Mojang 版权和非商业声明。
