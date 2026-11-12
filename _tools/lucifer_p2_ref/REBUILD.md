# 二阶段完整重建与调用

当前交付包含 40 根源骨、102 个显示部件、214 个 cube、18 个原名动作及微光/脉动材质。只负责二阶段；一期由独立会话维护。

在仓库根目录运行：

```powershell
python -B _tools/convert_dungeons.py --phase 2
python -B _tools/add_lucifer_p2_model.py
```

第一条由仓库内提取数据重建模型、稀疏动作、四片眼睑 affine 轨道、4096 图集及 core shader；第二条生成 RP/DP、38 个声音事件、25 个时间通知、18 个 play 入口和外观控制器。依赖 Python 3、NumPy、Pillow，以及 `_tools/mc_env.py` 指定的现有 1.21.11 客户端 jar。不会重新访问 Dungeons 游戏目录。原提取工具在仓库外 `D:/agent/dungeons_extract/exporter`。

共同尺度是 `0.0086339026833541152 blocks/cm`；运行时 `model_scale=7.1949189027950968`，内部仍为 `0.0192 BB/cm`。独立 `--authoring-model-scale 10` 固定原有栅格和曲线精度，须不小于运行尺度。两阶段单位拟合及 216 顶点证据见 `validation/scale_alignment/`。校准仅改外部尺度，几何、UV、18 动作及全部 atlas 字节保持不变。

`--output-dir` 可另指定转换目标；`--work-dir` 须为不存在、与输出互不包含的目录。`--static` 仅供显式复现 A 的静态阶段，拒绝覆盖已经有动作的模型。默认运行会生成完整 B，而非静态草稿。

当前项目的完整构建按 P1 `--defer-shaders` → P2 → P1 `--finalize-shaders` 顺序合并共同 core shader。单独在已有组合 shader 的 RP 上运行 P2 会拒绝覆盖；应运行完整构建，或对新隔离输出生成。合并验证见 `validation/combined_shader/AUDIT.md`。

```powershell
cd _tools
bash build.sh
bash rp_build.sh
python -B rp_validate.py ../resourcepack
```

游戏内调试：

```mcfunction
/function rpg:taint/lord1
/tag @e[type=minecraft:vindicator,tag=rpg.advent,scores={rpg_dm_lord=1},sort=nearest,limit=1] add rpg.lu.phase2
/function rpg:lucifer_p2/debug/play/jungleabomination_attack
/function rpg:lucifer_p2/debug/play/jungleabomination_walk
/function rpg:lucifer_p2/debug/sound/flower_open
/tag @e[type=minecraft:vindicator,tag=rpg.lu2,sort=nearest,limit=1] remove rpg.lu.phase2
```

`rpg:lucifer_p2/play/<原名小写>` 的执行者必须是已穿二阶段的载体；`debug/play/` 才会代玩家选附近载体。生成器只读取 `rpg.lu.phase2`，上述手动 tag 命令属于调试者。尚未制定的战斗切换条件、二阶段伤害技能和召唤物不在此实现内。

Blockbench 查看请加载 `native/lucifer_p2_material.js`，再打开 `lucifer_p2.bbmodel`。插件提供原式 HDR 材质和四片跨骨眼睑变形预览，保留原生保存往返字段。普通工程只使用第 0 张图集；缺面均显式禁用。材质公式和不含 Bloom 的显示映射见 `native/MATERIALS.md`。

未同步用户 PCL 实例。隔离客户端截图在 `game_preview/`；它们使用校准前外部 scale10，最终大小由新数值记录验证，见 `game_preview/SCALE_SCOPE.md`。不带 `--install` 的打包不会安装；实际实例同步仍按用户文档另行确认。
