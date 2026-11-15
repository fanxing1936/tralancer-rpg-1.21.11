# 首席附魔师 M2 静态模型审阅

[打开四视角并排对照](m2/preview/four_views_comparison.jpg) · [领口、肩罩与裙摆近景](m2/preview/collar_shoulder_skirt_comparison.jpg) · [打开已批准的 M2 静态模型](m3/accepted_m2.bbmodel) · [M3 动作审阅](M3_REVIEW.md)

模型保留原作的酒红袍、青蓝帽饰、青色额核和左右白黄镶边。静态拳架采用 Wiki 的常态灰拳、棕护腕。双拳在实机蓄力时出现右冰蓝、左雷黄的发光外框。基础贴图没有该效果的独立材质，本版保留手腕骨用于后续挂接。 [原作图库](https://minecraft.wiki/w/Dungeons_II:The_Prime_Enchanter#Gallery) · [双拳实机参考](m2/reference/emissive.png)

| 视角 | 参考 | 核对内容 |
|---|---|---|
| [正面](m2/preview/front_comparison.jpg) | 近正面垂臂渲染 | 眉下窄眼白、内侧亮块、长鼻、额核和胸袍 |
| [侧面](m2/preview/side_comparison.jpg) | 实机 15.50 秒侧偏背迈步 | 帽侧片、肩袖连接、拳腕和披风深度 |
| [背面](m2/preview/back_comparison.jpg) | 实机 15.00 秒转身 | 帽后三带、后颈片、两块披风和袍摆 |
| [四分之三](m2/preview/three_quarter_comparison.jpg) | Wiki 静态双拳架 | 眼白和鼻梁、肩领斜度、两拳相对高低、长袍轮廓 |

右栏的四张图来自同一个保存姿势。左栏各源镜头存在视角、动作和照明差异，尤其实机转身时披风被甩起。四分之三最接近本次静态拳架。右拳掌面和原图的翻转角仍有少量差异。 [参考帧和裁剪坐标](m2/reference/reference_metadata.json)

两道眉毛直接取原贴图同一块三列两行的阶形裁片，左右镜像。眉外侧厚，靠鼻的上缘低一阶，整条底边贴住窄眼白。靠鼻的白亮块按实机近景约 1.9∶1 宽高制作。红立领从颈根向上外翻，青肩罩沿上缘固定、下缘向外打开。白黄两片裙摆从腰侧向下外张。垂臂近景由同一模型临时摆姿渲染，四视图使用保存的拳架。 [本体取样依据](m2/BODY_UV.md) · [逐面 UV 表](m2/face_uv.csv)

拳架为后撤步，按四分之三图中可见的近侧黄纹左腿前探、远侧白纹右腿后撤摆姿。两靴底中心前后相差约 5.7 个模型单位，最低角的高度差小于 0.001。原图远侧脚被遮挡，后脚位置按轮廓重建。 [后撤步侧视](m2/preview/side.png)

两片背布各宽 5.35、展开长 24 个模型单位。两片同高度段共用上、中、下三个枢轴。外面取 `[57,2,64,20)`，内面镜像取 `[50,2,57,20)`。原图第二半末行中央三个透明像素对应双片末端缺口，几何两面都保持缺口。原作内外 UV 归属目前无法唯一确认，内面取样属于重建。帽后三带按原图 1∶2∶1 的像素宽度排列，末梢朝 V 增大的方向。 [披风与 UV 证据](m1/uv_cape_evidence.png)

Blockbench 5.2.2 已从磁盘重开并复编译，几何、层级、面 UV 和内嵌 PNG 校验一致。31 骨、59 盒件分为 12 个显示部件，156 个有效面均直接取样原始 64×64 PNG。领、肩罩和袍片的单轴子骨合并到对应显示部件。共用 `display_mob.py` 的逐部件 Java 模型转换检查通过。 [校验结果](m2/validation.json) · [四视渲染记录](m2/preview/render_evidence.json)

复现顺序为 `m2/make_static.py`、`m2/preview.py`、`m2/validate_static.py`，前两步使用本机 Blockbench MCP。当前交付为 M2 静态审阅版，未在真实游戏内看过。确认静态造型后进入 M3。
