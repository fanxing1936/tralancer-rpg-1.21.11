# 最终材质与小人眉眼

模型 SHA-256：`ebc5d7cfc16cc5e3e5f3357b82c6c99da29b468faafffe8c9d7f4ab9f1a1e106`。在 v3 淡紫外壳基础上，纳入有原贴图像素依据的小人粗眉/眼白候选，并让44×44原遮罩实际参与两个嘴腔发光面的显示。

## 小人脸部

采用 [图库核对后的六片眉眼 UV](../gallery_followup/pose_analysis/FACE_UV_CANDIDATE.md)，没有增加颜色、画新花纹或改动头鼻冠几何。继承候选原图集与既有紫色转换。静态 UV 的表情覆盖与冠几何差距仍保留；不能称找到了官方网格。

## 原44遮罩的实际使用

原 `MCD_Heart_of_Ender_(glow_effect_texture).png` 全部 RGBA 存于图集 `[432,88,476,132)`，原件和图集这44×44区域逐RGBA相同。原图上两行与右侧11列包含黑/灰像素，本实现仅将白色有效区 `[0,2,33,44)` 映射到嘴腔，实际 UV 为 `[432,90,465,132)`。没有把黑色区改成透明，也没有重画遮罩。

新增 `upper_mouth_raw44` 和 `lower_mouth_raw44` 两个单面零厚度平面，分别挂在现有头部/下颚的独立发光子骨上。它们位于上腔下表面 `y=25.998` 和下腔上表面 `y=26.002`；与原腔面相隔0.002模型单位，用于避免严格共面。没有增加展示实体，仍为21个部件；51个元素、26骨骼、7动作、3401关键帧。全部原49个候选元素、骨架、动作和21个部件包围盒中心不变。

两平面在 Java 物品模型中使用额外的 `tintindex:1`；对应item definition常量颜色为 `16765951`，即RGB `(255,211,255)`，直接取自 `Heart_of_Ender_prepare_to_shoot_beams.png` 的 `(1105,267)`。运行时将原遮罩白色RGB乘该颜色，再用原始alpha普通叠加；这不是把紫色烘焙进遮罩。每个元素维持 `light_emission:15`，不依赖周围光照。模型中的 `unhandled_root_fields.emissive_masks` 是上述面、UV与取色的事实来源，专用生成器读取它；公共 `display_mob.py` 未改。

这是真正引用原像素的局部发光表面，**不是自定义发光shader、屏幕bloom或动态光源**。44遮罩本身不包含眼牙图案，也不能单独提供源图全部紫光渐变；已接受的眼周、牙缘、壳体与嘴腔渐变继续保留。嘴腔的面位置、映射和混合方式属于实现推断，不冒充原作材质参数。

## 对照与验证

- [张嘴四分之三前后对照](mask_preview/three_quarter_comparison.png)、[正面](mask_preview/front_comparison.png)、[侧面](mask_preview/right_side_comparison.png)、[背面](mask_preview/back_comparison.png)：从两份模型重新渲染，原mask染色实际参与离线采样。
- [最终全部动作对照](motion_review/index.html)：254姿态，52页，含正/侧/背。
- [机器检查](validation.json)：原图集PNG未改变、原44RGBA相等、取色等于源像素、21部件中心未变、全部动作数值可烘焙。
- [逐面变更](material_changes.json)、[嘴部/光束预留点](sockets.json)。

模型已由原生 Blockbench 5.2.2 打开并另存副本；完整原生检查与服务端、资源包构建证据在最终验证目录分别记录。这里的图片为CPU离线近似，不是游戏截图；真实客户端透明排序、方向光与音效听感不能由这些图证明。

复现：`python -X utf8 _tools/heart_of_ender_finalize.py --promote`。它读取保留的眉眼候选、源贴图与配置，仅生成本目录和本任务主模型；不会覆盖历史v2/v3。旧动作生成入口已阻止覆盖最终材质。

版权属于Mojang Studios；本项目非商业，与Mojang无关联。来源与原件校验见 [SOURCES.md](../SOURCES.md)。
