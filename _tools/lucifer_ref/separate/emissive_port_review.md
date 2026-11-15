# 原始静态发光移植独立审阅

审阅日期：2026-11-07。只读审查代码、原 ASM、已保存工程和 GPU 数组；本次未操作 Blockbench、未重新发起 GPU 渲染、未修改模型或贴图。

结论：当前默认静态发光方程与已核对的 DXBC 数据流一致，未发现该范围内的算法错误。原始 HDR 参数 8.0 保留，NaturalEmissive 使用未乘 StatusColor、未经 saturate 的线性 albedo。发现的 GPU 数组方向文案错误已由主任务修正，复读确认脚本与 JSON 均为 top-down；数据 hash 未变。此审阅不表示完整原游戏画面或检查点 A 已完成。

## 1. 代码与源指令对应

代码为 `../native/lucifer_original_material.js` 第 33–44 行；应用配置为 `D:/agent/codex/TRA/work/lucifer_original/apply_original_material.py` 第 27 行起。

原指令来自 `D:/agent/codex/TRA/work/lucifer_original/shader/MI_NatureArmor/762fe3b6f361f38e14e6ec6c1b4e1f6f8a25d76c.asm`：

| 检查项 | 源指令依据 | 当前实现与结论 |
| --- | --- | --- |
| 主发光通道 | 85 行先作 `t3.xwyz` 再写 `.zw`，故 `r1.w=T3.B`；86、100 行乘颜色和强度 | `auxiliary.b * Emissive * EmissivePower`，一致 |
| 自然发光 | 99 行 `T4.rgb * cb3[13].w` | 使用原 albedo 的线性 RGB，一致 |
| StatusColor 与 saturate | 103 行才修改后续表面颜色；99 行发光已经求值 | 发光函数没有套 StatusColor 或 `[0,1]` 截断，一致 |
| 全局发光乘数 | 102 行乘 `cb2[0].x` | 最后乘 DeathEmissive，一致 |
| 非负限制 | 196 行对完整发光取 `max(...,0)` | 保留下限 0，无上限 1 截断，一致 |
| 默认附魔、flash、selection | 98、101、102 行；参数树记录默认 Power=0、时间戳 -100、SelectionColor=0 | 在所声明的 GameTime≥0、无运行时覆盖状态下均为 0，因此静态函数可省略这些零项 |

在已记录的默认状态中：

```text
E = max((S_linear.B * [0.693310022354126, 8.0, 0.0] * 1.0
         + A_linear.rgb * 0.699999988079071) * 1.0, 0)
```

插件第 68 行以 `THREE.Vector3` 写入原线性颜色，8.0 没有经过颜色字符串、8 位图像或 sRGB 参数解码。`sourceEmissionEnabled=1` 为默认启用状态。

两张采样纹理均作 sRGB→线性转换，与现有原资产属性及 UE 省略 SRGB 属性默认 true 的解析证据一致。该证据及其限制见 scratch `shader/MI_NatureArmor_uniform_mapping.md` 第 4 节；本审阅没有新增原游戏运行时 SRV 捕获证据。

## 2. 原始贴图与保存

已回读 `root_rot_armor_original.bbmodel`，SHA-256 为 `8c0a2041aba3552c2006c5453ffe2c92aba8f9cfcca7e4648ae94bcc7404acfd`。其内嵌 `T_NatureArmor.png`、`T_NatureArmor_S.png` 的 PNG 字节均与 extracted 原文件完全相等；未把发光烘焙进 albedo。基础色 alpha 只含 0/255。

`lucifer_source_precision.js` 对三个原始工程名调用原生 codec 的 `{raw:true}` 后使用 `JSON.stringify`，避免默认编译器的 5 位小数舍入。常规非压缩保存覆盖本次范围；其显式 bypass 的 compressed 路径没有取得同样的浮点保留保证。

材质插件通过 project codec 的 compile/parse/parsed 事件保存和恢复参数，并重建运行时 ShaderMaterial。着色器运行逻辑依赖该本地插件；`.bbmodel` 中的参数记录本身不会让未加载插件的 Blockbench 自动实现同一渲染。

## 3. 已保存 GPU 结果的独立复算

审阅读取 `D:/agent/codex/TRA/work/lucifer_original/emissive_gpu_rgba32.npy`，从两张源 PNG 和报告中的原始参数重新计算 CPU 参考值，未调用含 Blockbench 操作的验证脚本。

| 项目 | 结果 |
| --- | --- |
| npy 数据 SHA-256 | 与 `emissive_gpu_validation.json` 一致：`1f4505f297f2abfa2f0791bb25dc3b7fee7920d8a24465f27c2ef54194655eec` |
| RGB 最大绝对误差 | `2.2666444987606837e-06` |
| RGB RMSE | `9.674382713441381e-08` |
| 所比较 alpha 掩码差异 | `0` 像素 |
| 参考 HDR 最大值 | `8.074916170808972` |
| 已记录 GPU HDR 最大值 | `8.074915885925293` |
| GPU 大于 1 的 RGB 分量数量 | `76` |

结果满足现有 `1e-5` 容差，数值残差非零；不应写成 GPU 与原 D3D 逐位完全一致。该验证覆盖静态发光片元函数及当前源图裁剪掩码，完整游戏场景、采样 LOD、运行时 dissolve/dither/状态覆盖等没有由此验证。

## 4. 预览与已修问题

插件第 45–50 行将 raw HDR 路径和展示路径分开：`sourcePreviewMode=2` 输出原线性发光；常规预览将 Blockbench 表面光照与发光相加，再使用 Three.js ACESFilmicToneMapping 和 sRGB 编码。配置明确记录 exposure=1、Blockbench studio light、bloom=false。这些属于审阅显示设置，不能称为已复现 UE 场景灯光、后处理或 Bloom。

初读时 `validate_emissive_gpu.py` 在 `[::-1]` 翻转后以图像 top-down 顺序保存 npy/hash/texel 坐标，但 JSON encoding 仍标为 framebuffer bottom-up。主任务已经补上翻转后的准确说明；复读脚本第 28 行及 JSON 均为 `source-image top-down after framebuffer flip`。此标注错误已修，未改变数值数据。

## 5. 审阅快照

| 文件 | SHA-256 |
| --- | --- |
| `../native/lucifer_original_material.js` | `121178b04f75e2483f83dab65e9b8b94694c0e03e659a23658a798719b79f5e4` |
| `../native/lucifer_source_precision.js` | `7f7367c3fb164a69408ff570871adf1a9cb471085f803416768eaa5fb470e29b` |
| scratch `apply_original_material.py` | `840852bf96ced41223c01308d2219550f004ff35785c81d3d51026397c077c97` |
| `emissive_gpu_validation.json`（方向说明已修） | `76b54048c95b08385d3e7c806c74194fba67eb92ff1e994f6e2d63bcac80b1a5` |
| scratch `validate_emissive_gpu.py`（方向说明已修） | `cbab8f159eed62eb8db5945b08acce2c39269cc74150b5e6ab378680d9db4b59` |
