# 路西法第一阶段原始网格运行时

入口：`python _tools/add_lucifer_model.py <resourcepack> <datapack>`。
依赖：`python -m pip install -r _tools/lucifer_mesh_runtime/requirements.txt`。

事实来源为 `../lucifer_ref/lucifer.bbmodel`。保留源三角平面、UV和原图，
11个显示部件包含独立蛇矛；`play/slash`是独立横砍接口，不增加伤害。
原空手载体保持空手，视觉蛇矛只放在显示实体上，避免装备改变近战属性。

正式构建先在利维坦生成后调用 `--defer-shaders`，运行已有二阶段生成器，
再调用 `--finalize-shaders` 合并两阶段材质。未知着色器会停止构建。
二阶段原分支保留；公共 `display_mob.py` 和蛇矛生成器不修改。

模型与材质、实际服务器测试范围及20TPS插值限制见
`../lucifer_ref/REPORT.md`、`../lucifer_ref/CLAUDE_HANDOFF.md`。
