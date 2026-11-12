# Claude交接：路西法第一阶段已接入，可继续玩法

项目：`D:\agent\claude\github-create\tralancer-rpg-1.21.11`。本交接只完成外观、动作及播放接口；玩法数值与新技能设计由后续任务决定。

## 事实来源与外观

`lucifer.bbmodel`与`separate/lucifer_verdant.bbmodel`相同，SHA-256 `1b31cc7009b5fb8065641c46a8f2d6de725dc8106b11486aac9de2fd7374a530`。11 Mesh、22骨、原4PNG/几何/UV/权重保留；44源色映射使暗色衣服匹配蛇矛青绿与深棕，灰金属保持。

第5张独立图层为[lucifer_left_eye_emissive.png](lucifer_left_eye_emissive.png)，角色自身左眼(-X)紫色 `#A855F7`，眼周柔光0.14。Blockbench需加载`native/lucifer_original_material.js`与`native/lucifer_source_precision.js`。材质配置与贴图内嵌于模型；编辑独立PNG后须同步模型，不能只改派生atlas/预览图。

[九动作审阅](VERDANT_REVIEW.html)、[报告](REPORT.md)、[来源](SOURCES.md)、[原生606姿态/重开证据](validation/eye_palette_slash/NATIVE_VALIDATION_INDEX.json)。

## 正式生成与接口

生成器为 `_tools/add_lucifer_model.py`，实现位于 `_tools/lucifer_mesh_runtime/`。旧静态63方块导出器已归档，不再使用。依赖安装见该实现目录README。

```powershell
python _tools/add_lucifer_model.py resourcepack rpg
```

完整重建继续使用`_tools/build.sh`、`_tools/rp_build.sh`。它们已经安排P1 `--defer-shaders` → 已有P2生成器 → P1 `--finalize-shaders`，协调共享主/outline shader。不要把旧候选shader覆盖到正式包；修改P2后要核对当前owning source，未知override会停止生成。

固定key=`lucifer_lord`、载体tag=`rpg.lu`、score前缀=`rpg_lu`、seat=2、绑定高度2.4格。任何`rpg.advent`卫道士且`rpg_dm_lord=1`、未标`rpg.lu.phase2`，都会自动换装。载体攻击属性和原装备保持；视觉蛇矛独立显示。

调用动作时执行者必须为已换装的领主：

```mcfunction
execute as @e[type=minecraft:vindicator,tag=rpg.lu,sort=nearest,limit=1] at @s run function rpg:lucifer_lord/play/slash
```

`play/<clip>`共九项：idle、walk、attack、strong、cast、laugh、stun、rise、slash。只有idle/walk循环；slash为1.05秒独立横砍。`dress`重复调用有保护，`undress`恢复原持物且只清P1部件，保留其他乘客。

现有技能仅加视觉调用：sk1_1/sk1_2→attack，sk1_3→cast，sk1_4/sk1_5/ult1→strong，ult1_warn→laugh。原伤害与出手tick未改。**slash未绑定新增伤害、冷却、范围或触发机制**，按玩法需求选择调用即可。

## 状态与阶段

P1 tick必须先于P2 tick，P1 tick_late在command/tick_end后；生成器已保证顺序。真正阶段信号是`rpg.lu.phase2`，不能只看`rpg.lu2`。已有P2由另一个会话维护，仍有并行更新；修改前读当前源码，不覆盖其生成器或资源。

移动每4tick检查，idle/walk自动切换。`rpg.exorcism.bound`进入stun并保持末帧，解除回idle；play接口在束缚时有保护。具体玩法勿随意直接写动画计时score，优先调用play接口。

## 已验证与剩余边界

- 构建脚本与资源校验通过；7技能原命令字节前缀保留。当前项目已实际生成P1函数和资源，不是只有候选文件。
- 最终实际独立1.21.11服务器 **59/59通过**，包含双载体、九动作入口、移动/束缚、重复换装、原持物与攻击/掉落不变、真实阶段往返、死亡后移除清理、寿命到期边界及驱魔成功清理。[服务器证据](validation/runtime_integration/server/SERVER_VALIDATION_INDEX.md)。寿命是12000初始化与实际到期边界测试，并非挂机十分钟。
- 当前643个P1 DP文件、48个P1 RP文件及生成源与测试版本逐字一致；工作区另有P2并发改动，不声明整个实时工作树等同隔离包。
- **laugh使用20Hz全11部件同步逐帧**，其余八段使用平滑插值。原高速转矛在Java平滑路径实测穿模，当前策略有限200/1000Hz检查均无Body/Head碰撞，保留原模型关键帧；代价是50ms保持和快速姿势跳变。不要未经复核改回平滑。[完整证据与取舍](validation/runtime_integration/laugh_playback/README.md)。
- 尚未在真实客户端看过材质、边缘、声音和战斗整体效果。Blockbench/GPU/服务端证据各有范围，不等同完整UE渲染或实机验收。

召唤调试：`/function rpg:taint/lord1`。用户指定的测试实例为`D:\minecraft\PCL启动器\.minecraft\versions\1.21.11-Fabric 0.19.3`；原需求明确**同步前先问用户**，本次未同步。不要提交、推送或切分支，除非用户明确要求。
