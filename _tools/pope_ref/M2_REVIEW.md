# 教皇 M2 静态模型审阅

当前状态：静态审阅稿已交付，等待用户确认；尚未进入 M3。模型有 **0 段动画**。

事实来源：[pope.bbmodel](pope.bbmodel)。当前 SHA-256：`4f2d24f9c5da774cbf0be44d7895c7a449bd7a1f8f1442dcbd1f2eed83c575aa`。

## 审阅图

- [四分之三主对照](m2/preview/three_quarter_comparison.jpg)
- [正面 / 原作坐姿对照](m2/preview/front_comparison.jpg)
- [侧面 / 原作转身帧对照](m2/preview/side_comparison.jpg)
- [背面 / 原作瞬移帧对照](m2/preview/back_comparison.jpg)
- [全部四视角并排](m2/preview/four_views_comparison.jpg)
- [模型正交多视角](m2/preview/four_views_model.jpg)、[非持杖侧补充](m2/preview/right_side.png)
- [握杖 A/B 局部候选](m2/candidates/grip_choices.jpg)
- [眼位修正前后](m2/eye_fix/before_after.jpg)、[眼神 A/B 与各自原作参考](m2/eye_fix/eye_choices.jpg)
- [本地审阅页](m2/index.html)

正面参考是坐姿；侧面与背面来自动态转身/飞起帧。M2 模型保持同一个站姿，没有借用临时动画来假装姿势一致。主图相机约 yaw 42°、俯视 23°，为投影拟合，不是官方相机。原参考与模型均按完整可见外框等高排版；只裁切、最近邻缩放和并排，不修图或重新上色。

## 静态结构

| 项目 | 当前值 / 依据 |
|---|---|
| 显示部件 | 12；17 根骨骼、44 个立方体/平面、170 个可见面 |
| 身高 | 实际脚底 0 → 冠顶 30.6031714393 模型单位；`model_scale=1.359336240120` → 2.6 格 |
| 原图 / 图集 | 本体原64×64保留在128×64单图集；只用 textures[0]，PNG base64内嵌 |
| 头 | 12×7×6；与衣肩相接；静息侧倾8° |
| 鼻 | 2×4×1；28个原像素正好闭合六面，深灰面移到背面 |
| 冠 | 外廓4×11×4；独立骨；顶部齿壁0.3厚，金环原透明孔保留 |
| 项链 | 金环2片单轴旋转后合并body；红宝石2×2×1，完整16像素盒网 |
| 袍 / 披风 | 蓝袍、金边、白下缘；披风在+Z背侧；白片随衣摆，不作为白靴 |
| 腿脚 | 各3³暗青短裤、1×3×1金腿、朝-Z的红色薄脚板 |
| 权杖 | 角色左手（-X）；独立杖骨与独立staff_glow骨；杆纹理1×18像素，几何1×17按参考比例拟合；托盘3×1×3，顶部5³ |
| 半透明 | 未制作半透明效果；只保留原图透明孔与不透明表面 |

| part | 所含骨骼 |
|---|---|
| body | body, chain_right, chain_left |
| head | head, right_brow, left_brow |
| crown | crown |
| right_arm | right_arm |
| right_hand | right_hand |
| left_arm | left_arm |
| left_hand | left_hand |
| right_leg | right_leg |
| left_leg | left_leg |
| cape | cape |
| staff | staff |
| staff_glow | staff_glow |

空 root 只组织层级，不生成 item_display。链环为 body 下单轴±25°静态子骨；两眉为 head 下单轴±8°静态子骨，仍合并在同一个头部显示实体。所有独立动作部件均保留独立骨。冠可脱离头、杖可脱离左手、顶块可独立转动；本阶段仅建立结构，没有写动作。

## 眼睛反馈修正

用户指出眼睛有问题后，重新按主图头部12×7前面进行投影量测，确认旧眼区 `|X|=2.85..5.7` 向脸外偏约1.7单位。当前修正为 `|X|=1..4`，眼白外缘距脸边2单位；眉横片改为 `|X|=1..5`，竖片为 `|X|=3..5`，并加入两眉各自约±8°内压角度。眼高仍为1单位，未改颜色或原贴图。

**用户已选择并保存眼神 B（王座/正面Idle）**：白底3×1，鼻侧上半黑瞳约1.1×0.5，鼻侧留0.3单位白边，瞳面比白底前移0.02。白底取原眼岛 `[5,5,6,6]`，黑瞳取 `[3,5,5,6]`，不改色。**眼神 A 仅作参考对照**：主渲染/普通Idle的外侧1×1白、内侧2×1黑。两种表情都有原作依据，不能用王座的大白眼去假称主图也是如此。

[修正前诊断与像素测量](m2/eye_fix/EYE_REVIEW.md)、[已选B与原作](m2/eye_fix/eye_B_selected.jpg)、[眼神对照](m2/eye_fix/eye_choices.jpg)、[修正前后](m2/eye_fix/before_after.jpg)、[修改范围检查](m2/eye_fix/eye_fix_validation.json)。验证确认其余36元素、原有15骨骼定义未变，仍12个显示部件。B已写入pope.bbmodel；A/B对照渲染结束后恢复到已保存的B几何。局部正面对照临时把整头归正，以比较眼位，不是动画。

## UV 与仍属推断的部分

完整可追溯来源：[逐面表](m2/FACE_UV_TABLE.md)、[机器记录](m2/face_provenance.json)、[图集布局与结构](m2/model_spec.json)。面只取已登记区域，不把不透明深灰背景当透明或内衬。

M2修正了M1候选：鼻子是2×4×1完整盒网；吊坠是2×2×1完整盒网，排除了岛边43灰底；眼眉拆成11个有效像素，未整块贴6×6黑底；袖筒保留开放袖口，金边朝外。灰臂竖条只做90°像素复制进入图集额外区域，不用 face.rotation。[精确盒网研究](m2/uv_study/CLOTHES_UV.md)

**权杖顶部材质已作数值拟合，但不是官方UV文件。** 无发光单杖渲染的大面与底面对应 T_SuperCube 的 `[10,0,13,32]`，窄面对应 `[7,0,10,32]`。全部528个U区间与方向候选比较，RGB RMSE分别约1.295、0.773、4.447；整图铺满基线约59.801、51.014、43.741。拟合中性受光系数只用于证据比较，未烘焙到贴图。[数值方法与误差](m2/uv_study/CUBE_FIT.md)、[证据图](m2/uv_study/cube_numeric_fit.png)

顶部V方向、六面朝向和隐藏面只能推断：当前V全高，两个窄侧使用7..9列，其余面使用10..12列，对面复用。原作主渲染的浅橙发光、游戏帧中的粉紫发光与本模型普通受光的黄色不同。M2照无发光权杖材质做；没有改色、没有bloom或半透明。`staff_glow` 已标为独立发光骨，管线自发光接入留到M4。

衣片分割、背布内侧复用、上领深度、侧摆厚度与隐藏肩连接仍是重建。侧面可见少量白领，不能把当前结果宣称为官方几何。动态图中的衣摆张开与腿姿不同，必须在M3逐帧比对；M2只检查静态方向、来源和连接。

## 需要用户决定

原主渲染的手/杖相交处有可见Z-fighting，不能据此唯一确定手掌收口。交付两个原生渲染候选：

- **A（当前模型，推荐）**：灰握块在原细臂末端外扩0.05，包住杖杆；不新增大手掌，遮住共面红杖。
- **B**：手臂末端平接杖杆，手和杖无重叠；握持结构更简略。

握杖候选B只在同一工程临时渲染，随后恢复；没有保存进事实来源。这里的握杖方案与已选定的眼神B是两件独立事项。请确认整体静态外形和握杖方案后，再进入M3。

## 验证与制作方式

- [只读验证报告](m2/validation/MODEL_VALIDATION.md)：单内嵌图集原像素、170个面、真实UUID、层级/坐标、12部件、2.6格全部通过。只在内存调用 `load_bbmodel` 与 `part_model`，没有生成其他怪资源。
- [Blockbench重新打开记录](m2/validation/blockbench_roundtrip.json)：保存文件重新导入原生Blockbench 5.2.2，44元素、17骨骼、1纹理、0动画；纹理解码、几何与UUID一致。
- [原生渲染证据](m2/preview/render_evidence.json)：记录模型哈希和相机；不是Minecraft截图。
- **未在真实游戏内看过。** 未同步测试实例。构建、rp_validate、server_test与载体清理留在M4，当前不声称通过。

制作脚本通过已安装的Blockbench本机MCP调用原生Group/Cube/Texture API，再由Blockbench编译保存 `.bbmodel`；没有在Blockbench里做脚本无法重现的手工修改。Python只组织数值、原图拼贴、来源记录和对照图排版。重新运行M2制作脚本会重建静态模型；脚本拒绝覆盖已包含M3动画的文件。

复现顺序（本机Blockbench MCP端口52907须已启动）：

```text
python _tools/pope_make_static.py
python _tools/pope_preview_static.py
python _tools/pope_static_candidates.py
python _tools/pope_eye_review.py
python _tools/pope_validate_model.py
python _tools/pope_roundtrip.py
python _tools/pope_m2_report.py
```

本阶段未创建 `add_pope_model.py` 薄配置或挂接构建，避免无动画版本提前进入玩法。M4采用用户最新顺序：`build.sh` 为 `add_tower_wraith.py → add_pope_model.py → add_pope_fight.py`；`rp_build.sh` 仍在 `add_tower_guard.py` 后。[顺序记录](m2/validation/INTEGRATION_ORDER.md)

没有修改共用display_mob.py、玩法、末影之心或其他怪的文件；没有提交、推送或切换分支。

素材版权归 Mojang；本项目非商业，与 Mojang 无关联。完整来源与原文件哈希见 [SOURCES.md](SOURCES.md)、[source_manifest.json](source_manifest.json)。
