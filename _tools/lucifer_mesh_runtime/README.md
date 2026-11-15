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

## 普通材质（默认，2026-11-13）

原来的出图方式（每个三角面指向图集里的数据像素，由自定义核心着色器还原贴图）在资源包不带该着色器、或开着 Iris/光影包时，会整个显示成绿色。用户在实机截图里看到了这个问题，并要求不要用三角网格。

现在默认是 `plain_material.py`：
- 把两两共边、共面、贴图是轴对齐矩形的三角合回原来的矩形面，直接用原贴图像素（60 个面）。
- 原作本来就斜的面（法袍下摆、帽子侧面，共 9 个），每块作为一整块烘焙，精度是每个原像素对应 4×4，最近邻取样。
- 左眼发光改为贴在那两个像素上的一片全亮度小方块。

模型源是 `_tools/lucifer_ref/separate/lucifer_verdant.bbmodel`（用户指定，内容与 `lucifer.bbmodel` 相同）。

设 `LUCIFER_MATERIAL=shader` 可回到着色器方案。
