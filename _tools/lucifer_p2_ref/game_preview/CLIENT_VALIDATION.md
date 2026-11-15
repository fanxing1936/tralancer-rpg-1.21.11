# Lucifer 二阶段：真实 Java 客户端材质验证

2026-11-08，现有官方 Minecraft Java 1.21.11 客户端已成功加载最终完整资源包，并在全新隔离单人世界显示二阶段模型。原生 F2 截图证实相同相机、相同 idle f0 下，phase 50 的亮区比 phase 150 更亮；实时生产材质时钟与 walk 动作也已在游戏画面中观察到。没有完成连续录像或 GIF。

## 环境与隔离

- 客户端：现有官方 1.21.11 jar，SHA-256 `1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd`。直接运行 `net.minecraft.client.main.Main`，没有 Fabric、用户 mods 或新下载程序。
- Java 21.0.12，LWJGL 3.3.3；复用现有 64 个 Windows x64 库及 asset index 29 的 4,591 个对象，缺失对象 0。原游戏 jar、libraries、assets 均只读。
- 新 gameDir：`D:\agent\dungeons_extract\phase2_client_test\game`。
- 新世界：该 gameDir 的 `saves\LuciferP2-Isolated`。材质/动作测试 helper 数据包仅在此存档内。
- 资源包来源：`D:\agent\dungeons_extract\phase2_b\build_workspace\resourcepack`，复制到隔离 gameDir 的 `resourcepacks\LuciferP2-Isolated`。原 PCL 实例的 resourcepacks、options、存档均未改动。
- 先用隔离专用服准备世界，绑定 `127.0.0.1:54590`。首次多人入口出现联机警示后没有点击继续，没有用参数跳过警示；改用本机单人世界。专用服已正常停止，退出码 0，世界在停止后复制。
- 客户端窗口仍保留，最后 UI 操作后已停止所有客户端输入。没有关闭用户正在查看的游戏，也没有操作一期 Blockbench 窗口。

完整启动参数、库清单、native DLL hashes 见 `launch_manifest.json`。其中 accessToken 是显式测试值 `0`，不是用户凭据。

## 固定姿态峰谷对照

场景是午夜（`time set midnight`）、晴天、时间和天气停止；灰混凝土平台上一个 NoAI、NoGravity 的测试 Vindicator 载体。载体通过实际 `rpg:lucifer_p2/dress` 生成模型，使用生产 `jungleabomination_idle/f0` 姿态。生产资源包和模型未为截图修改。

私有 helper 将 `minecraft:tick` 临时替换为空，避免动画和相位继续推进。相机命令为 `tp @s 0 69 15 180 10`；Minecraft 的整数字面坐标使实际 x/z 居中为 0.5 / 15.5（后续同一直接命令的客户端反馈已确认）。镜头、FOV、窗口和姿态在两张静态截图之间不变。F1 隐藏界面后使用游戏 F2，文件为原始 1280×800 PNG。

只改 8 个带 `rpg.lu2.pulse` 标签的显示部件 `custom_model_data.colors[2]`：

| 截图 | 相位/时间 | marker 整数 | 原 F2 文件 | SHA-256 |
|---|---|---|---|---|
| `phase50_peak.png` | 50 / 2.5 s | 2544434 | `2026-11-08_14.39.34.png` | `d6621f348d49324e9ad0375575de40c25d3bda0d8a1a622e1d4ba60130caf58e` |
| `phase150_trough.png` | 150 / 7.5 s | 2544534 | `2026-11-08_14.40.01.png` | `8419fbe9675743269d224d69c260dc87ca7a92258ec6e7f971a9d203f3386187` |

两份证据副本与 gameDir/screenshots 原文件逐字节一致；原路径、纳秒 mtime、字节数在 `original_screenshots.json`。夜间画面中主体、绿色枝叶、花和四个眼部区域均可见，未观察到旧 Blender 透明层的黑块。

`pulse_pixel_difference.json` 使用明确的像素诊断范围：x 430…890、y 150…730，任一帧 RGB 最大分量 >45 的四连通区域，过滤面积小于 8 的孤立星点。该 mask 不是整个模型精确 silhouette，也不覆盖暗部全部像素。

- mask 内 74,098 像素，795 像素在最高点更亮，0 像素变暗。
- `peak - trough` 最大 RGB 差为 `[3,20,4]`，最小为 `[0,0,0]`。
- 变化包围框 `[549,325,702,475]`，集中在眼部和粉色发光区域；mask 内其余像素相同。
- `pulse_model_difference_x16.png` 仅为绝对差值放大 16 倍的诊断图，原 F2 图未增强或改色。

这闭合了真实客户端的 marker tint、4096 源图集在 8192 物品 atlas 内的辅助数据寻址、材质分支执行和相位响应。较强红/蓝 HDR 经明确的显示曲线压缩后已经接近饱和，所以屏幕差值主要体现在绿色分量；不得把这说成原 UE 曝光/Bloom 的逐像素复现。

## 实时动作与脉动观察

随后私有 helper 仅调用生产 `rpg:lucifer_p2/material/tick` 和 `rpg:lucifer_p2/anim/jungleabomination_walk/tick`，保留 NoAI 载体位置，直接播放 walk 以免自动 stride 判为静止并切回 idle。侧边栏将实际 `#phase` 复制到可见的 `Phase` 项。

真实客户端画面中观察到四肢/头部连续变形，以及 Phase 138、10、105、44、184 等随时间推进并循环的值；粉色亮区持续脉动。它验证了运行中的实际 pose 变换与材质时钟，未测量墙钟周期精度，也未逐一实机复验 18 个动作。完整 18 动作的独立骨架/GPU与原生 Blockbench 证据另归档。

用户有桌面输入时工具提示需要重新观察；最终按要求停止了输入。没有制作或宣称已有连续 GIF/视频。用户仍可操作当前客户端。

## 日志审查与限制

`client_console_snapshot.log` 保留完整日志；`client_log_review.json` 列出检索规则、所有 ERROR/WARN 头和解释，未清洗掉问题。

- 实际 ResourceManager 加载 `vanilla, file/LuciferP2-Isolated`，实际 items atlas 为 `8192x8192x0`。
- shader/program/pipeline 编译或装载错误匹配为 0，缺失纹理/模型装载错误匹配为 0。运行目录的两个 core shader 与最终 build RP 逐字节相同。
- 离线 token 0 导致用户属性/Realms 认证失败，这是预期离线边界；没有尝试 Microsoft 登录。
- 初次本地 helper `p2_visual:setup` 使用了函数权限 2 不可用的 `tick freeze`，产生一次解析错误。该行在首次 `/reload` 前删除，后续 reload/setup 成功。这不是生产 RPG 函数错误。
- 首次单人进入时有 39 条 `Received passengers for unknown entity`，后续未复现；保留为集成警告，不把整体日志称为“无警告”。
- 全 RPG tick 初期有 5 次落后 40–148 ticks 的告警。后来 helper 隔离了材质/动作执行，本测试不代表完整战斗或多 Boss 性能通过。父任务另行优化/基准运行时。
- 初次 LWJGL 临时目录的磁盘空间探测有目录不存在警告，随后 renderer 正常初始化；launcher 已补建隔离临时目录。
- `.6 * A` 与 B 通道脉动的数值公式有原 DXBC/Uniform 和独立 float GPU 证据。本次夜景图直接显示基础微光，但没有在同一游戏场景切换 NaturalEmission=0 做独立消项对照。
- 这不是第三方 shader mod / Iris / OptiFine 的兼容验证，不添加世界照明或 Bloom，也不是原 UE HDR 后处理完整移植。
- 私有 helper 直接播放动作，不验证战斗 AI、玩家伤害或自动阶段切换。用于截图的存档与完整生产 tick 不同；交付生产 DP/RP 未被此 helper 修改。

`manifest.json` 给出本目录每个证据文件的字节数及 SHA-256。复算入口为上级 `finalize_evidence.py`。
