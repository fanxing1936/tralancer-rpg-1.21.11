# 首席附魔师 M4 接入

肩罩修订版位于 `D:/agent/codex/TRA/outputs/prime-enchanter-shoulder-caps-higher/`。领口两侧的青蓝肩罩沿各自手臂局部 Y 轴比前一版再抬高 0.6，累计比首次 M4 抬高 1.8，肩罩顶由 23.76 到 24.36。外翻板与其铰点一起移动，肩关节、红袖、拳套、挂点和动作关键帧沿用首次 M4 的位置和参数。垂臂四视角和抬拳对照使用模型渲染。召唤的 0.58 秒、过载的 1.92 秒均测到肩罩与头盒局部重叠。前冲和砸地的缩放峰值也列在抬拳对照中。

从首次 M4 的 `.bbmodel` 与 `sockets.json` 可用 [raise_shoulders.py](m4/raise_shoulders.py) 复现肩罩修订，再由原模型生成器烘焙。M2 和 M3 的参数与对照仍为相应阶段的记录。

下文记录首次 M4 交付及其测试。

`_tools/add_prime_enchanter_model.py` 在数据包和资源包构建中读取 [Blockbench 成品](prime_enchanter.bbmodel)。它从同一个模型生成 12 个显示部件、64×64 贴图和 11 段动画，共 726 个 Java 姿势帧。游戏内模型站立高度约 2.6 格。召唤生成隐身卫道士和乘客模型，载体生命值 1000。

```mcfunction
/function rpg:prime_enchanter/summon
/function rpg:prime_enchanter/debug/anim/forward_strike
/function rpg:prime_enchanter/debug/anim/lightning_slam
```

单个载体可通过 `execute as` 调用 `rpg:prime_enchanter/anim/enter/<clip>`。

```mcfunction
/execute as @e[type=minecraft:vindicator,tag=rpg.prime_enchanter,sort=nearest,limit=1] at @s run function rpg:prime_enchanter/anim/enter/summon
/kill @e[type=minecraft:vindicator,tag=rpg.prime_enchanter]
```

| 编号 | 动作 | 时长（刻） |
|---:|---|---:|
| 0 | `idle` | 20，循环 |
| 1 | `walk` | 18，循环 |
| 2 | `appear` | 47 |
| 3 | `death` | 114，保持末帧 |
| 4 | `forward_strike` | 50 |
| 5 | `fury_fist` | 138 |
| 6 | `launch` | 79 |
| 7 | `lightning_slam` | 88 |
| 8 | `overcharge` | 72 |
| 9 | `hurt` | 46 |
| 10 | `summon` | 45 |

动作帧从 0 编号。登场 f0–4 和跃起回场 f23–43 暂时清空显示部件的物品，登场 f5 与回场 f44 恢复可见。非循环动作播完回待机，倒地动作保持末帧，供玩法选择移除时机。要预览倒地，给活着的载体调用 `debug/anim/death`。

前冲 f29、f30 和砸地 f53 烘焙完整缩放姿态，腕和袖口使用同一时刻的骨骼矩阵。砸地的相邻源帧在 20 TPS 下共用落地峰值，详见 [M3 缩放对照](M3_REVIEW.md)。原作独立音效没有可用原件，资料和事件名称记在 [素材来源](SOURCES.md)。

[挂点数据](sockets.json) 保留模型空间坐标。接入时以载体脚底为原点，零朝向下将模型位置 `[x,y,z]` 转为 `[-x,y,-z] × 1.15 / 16` 格，再随载体转向。乘客座高为 2.0 格，显示部件的变换已扣除该偏移。

构建在隔离副本中按 `rp_build.sh`、`build.sh`、`rp_validate.py resourcepack` 的顺序执行，三个命令均退出 0，最终资源包检查未发现问题。`server_test.py` 的隔离世界成功启动并加载数据包，未发现函数解析错误。测试日志中的离线认证与平坦世界初始配置消息属于测试环境。全量构建还报告了仓库既有色板和教皇特效提示。

成品 ZIP 根目录均含 `pack.mcmeta`。使用时把数据包 ZIP 放入目标世界的 `datapacks`，把资源包 ZIP 放入客户端的 `resourcepacks` 并启用。两个 ZIP 都是完整的 TRALANCER RPG 包，建议在测试世界中以这两个文件作为同一版本使用。交付文件保存在 `D:/agent/codex/TRA/outputs/prime-enchanter-m4/`。

用交付数据包 ZIP 启动原版 1.21.11 专用服务器，248 项断言全部通过，函数和命令错误为 0。覆盖 11 段动作切换、26 个隐藏帧、三个缩放峰值、倒地保持末帧、跨维度独立播放以及载体移除后的乘客清理。59 组姿势共核对 708 个实际部件变换。

原版 Java 1.21.11 客户端在独立世界里检查了待机、右臂前冲放大、左臂砸地放大、登场和跃起回场的隐藏与重新出现。成品目录中的 PNG 是游戏内截图，攻击画面取放大峰值的静止姿势。独立测试使用的 1,258 个首席附魔师数据文件和 25 个材质文件均与交付 ZIP 逐字节相同。正式游戏实例没有同步此次交付。
