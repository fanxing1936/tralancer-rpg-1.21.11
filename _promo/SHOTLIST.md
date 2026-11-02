# 实机录制清单（ReplayMod + Complementary 光影）

一共要录 5 个镜头（S1–S5），都在存档「破碎大陆-宣传片拍摄」里完成。整个录制过程大约 15 分钟，渲染另算。

## 准备工作（只做一次）

1. **启动客户端**：用 PCL 启动 `1.21.11-Fabric 0.19.3`。实例里已经装好这些东西：
   - ReplayMod 2.6.28
   - 光影包 Complementary Reimagined r5.9.3
   - ReplayMod 渲染要用的 ffmpeg，放在 `ffmpeg\bin\ffmpeg.exe`
2. **换资源包**：选项 → 资源包，只启用 `tralancer-rpg-promo`，把 `tralancer-rpg` 和 `tralancer-rpg-artstyle` 移到左边（停用）。
   > 录完记得改回原来的组合。美术会话在用 `tralancer-rpg` 加 `tralancer-rpg-artstyle`。
3. **开光影**：选项 → 视频设置 → 光影包，选 Complementary Reimagined。
   > 录完把光影改回“关闭”，不然美术会话截的检查图会带上光影。
4. **试渲一段**：进存档走几秒，退出。打开 ReplayMod 的回放查看器（Replay Viewer），挑这段回放渲染 5 秒试片：
   - 1920×1080，60 fps，编码选 MP4 – High Quality。
   - 试片能出来，就说明 ReplayMod、Iris 和 Sodium 能一起用。
   - 如果提示找不到 ffmpeg，在渲染设置的 Command 一栏填完整路径：`D:\minecraft\PCL启动器\.minecraft\versions\1.21.11-Fabric 0.19.3\ffmpeg\bin\ffmpeg.exe`。

## 录制

进入存档「破碎大陆-宣传片拍摄」，ReplayMod 默认会自动开始录。先执行一次：

```
/function promo:setup
```

它会把时间定在黄昏、晴天、不刷怪，把你切成生存模式并给无敌、不饿。

| 镜头 | 做什么 | 时长 |
|---|---|---|
| **S1 大陆远景** | 挑一个视野开阔的高处站着，或者绕着地形走一圈。不用敲命令 | 约 20 秒 |
| **S2 武器长廊** | 找一块平地，面朝南（F3 里显示 `south` / +Z），执行 `/function promo:armory/spawn`。31 件武器会排成两排长廊，沿着长廊慢慢走到底 | 约 20 秒 |
| **S3 圣卫方阵** | `/function promo:clear`，然后 `/function promo:guards`。三名圣卫在前方列队冲过来，站着让他们打几下 | 约 20 秒 |
| **S4 别西卜** | `/function promo:clear`，然后 `/function promo:bz/summon`，正常和他打。中间依次执行 `/function promo:bz/cast1` 到 `cast5`，每条隔 3–4 秒，最后执行 `/function promo:bz/ult`（万蝇饕宴）| 约 60 秒 |
| **S5 生命之树** | `/function promo:clear`，然后 `/function promo:time/night`。站在平地上执行 `/function promo:tree`，原地等它展开 | 约 20 秒 |

都录完后退出存档，回放会自动保存。

## 渲染

在回放查看器里打开刚才那段回放：

1. 按镜头分别打相机关键帧（Path），用回放的自由视角运镜。
2. 渲染设置：1920×1080，60 fps，MP4 – High Quality，**开着光影**。
3. 每个镜头渲染成单独文件，渲染长度最好比下面写的多 1–2 秒，方便剪辑。按这个命名放进 `_promo/raw/`：

| 文件名 | 片中用多长 | 运镜建议 |
|---|---|---|
| `S1_land.mp4` | 4 秒 | 高空缓慢推近，夕阳在画面一侧 |
| `S2_armory.mp4` | 5 秒 | 齐腰高度沿长廊中线推轨，从勇者推到神圣 |
| `S3_guards.mp4` | 4 秒 | 低机位正面，圣卫迎着镜头冲过来 |
| `S4a_beelzebub.mp4` | 8 秒 | 降临的烟雾，接一个起手招式 |
| `S4b_feast.mp4` | 6 秒 | 万蝇饕宴，镜头拉远看清全貌 |
| `S5_tree.mp4` | 7 秒 | 俯视角缓慢环绕，看清整棵树 |

放好之后告诉我，我把占位卡换成这些镜头，再渲染成片。

## 如果录出来的镜头太短

渲染时多留几秒就行，剪辑会从中间截取需要的长度。
