# 教皇 M1：页面证据与解释边界

核实日期：2026-11-04。来源通过本机 Edge 浏览器实际读取；网络文本抓取工具未能读取该 Wiki，因此不把抓取失败当作素材不存在。

## 页面证据

| 主题 | 核实结果 | 来源 |
|---|---|---|
| 外形 | 蓝袍、大项链和红宝石、高皇冠、权杖；横向较宽的头。没有三重冠或白袍依据。 | [角色页 Appearance](https://minecraft.wiki/w/Dungeons:Arch-Illager#Appearance) |
| 攻击共用 | 普通能量弹与近身推击共用 Basic attack 动画；页面的攻击延迟说明不等于 GIF 中可见的发射帧。 | [Basic attack](https://minecraft.wiki/w/Dungeons:Arch-Illager#Basic_attack)、[Melee attack](https://minecraft.wiki/w/Dungeons:Arch-Illager#Melee_attack) |
| 瞬移时长 | 页面写进、出各 0.9 秒。 | [Teleportation](https://minecraft.wiki/w/Dungeons:Arch-Illager#Teleportation) |
| 瞬移共用 | 图库把 Teleport_(Appear_Short).gif 标为战斗瞬移进出；另一截图说明消失采用缩短版 appear。它没有提供完整骨骼曲线，也没有明确要求将出现动画倒放。 | [图库 Animations 与 In-game](https://minecraft.wiki/w/Dungeons:Arch-Illager/Gallery) |
| 被吸走 | 页面描述权杖脱手并吸收角色、随后转化；掉冠、手的位置和结束姿态以已抽取图像为准。 | [Defeated in a whirlwind](https://minecraft.wiki/w/Dungeons:Arch-Illager#Defeated_in_a_whirlwind) |
| 权杖参考 | 独立权杖渲染明确标注 without emission；T_SuperStaff 标为权杖贴图，T_SuperCube 只标为 cube 贴图。没有提供发光遮罩或官方 UV 几何。 | [图库 Renders 与 Textures](https://minecraft.wiki/w/Dungeons:Arch-Illager/Gallery) |
| 主渲染缺陷 | 当前主渲染原文件为 666×999；文件页要求修复手臂 Z-fighting。该杂纹不能照搬为模型细节或拿来推断手部 UV。 | [主渲染文件页](https://minecraft.wiki/w/File:MCD_Arch-Illager.png) |

## 图像直接可见的事项

- 正面王座待机动图的权杖位于画面右侧，即角色**左手**；本项目 Java 模型空间对应左侧 -X。`staff` 结构应跟随 `left_hand`。挂点仍同时提供左右手，名称不能按画面左右调换。
- 瞬移动图包含显著的整人尺寸变化，以及长段透明尾帧。仅有 position/rotation 的本管线不能照搬缩放；后续姿态重建必须标为适配推断。
- 攻击动图能定位抬杖、前探和回收姿态，却未显示三发弹体各自的真实生成事件。模型方提供“出手姿态候选”，不替玩法方确定三连发间隔。
- 被吸走的两个 GIF 在末帧仍有可见人物；“全部部件收拢到同一中心”的终末段是项目交接要求，不能标为已观测原作曲线。
- 原作动图中权杖顶端会由橙黄变为粉紫。T_SuperCube 是不透明橙黄渐变图，不能把它叫作黑白发光遮罩。M1 未制作变色、半透明效果或特效。

以上图像证据的位置、帧号、秒数由 [动作表](motion/MOTION_STUDY.md) 和 [UV 表](uv/UV_MAP.md) 索引。候选区域与未定朝向以 UV 表中的状态为准；不得将重建候选描述为从游戏资产导出的官方模型。

## 版权

原始游戏素材版权归 Mojang Studios 所有；本项目非商业，与 Mojang 无关联。文件来源、下载方式和完整 SHA-256 见 [SOURCES.md](../SOURCES.md)。Wiki 页面文字许可与游戏素材版权分别处理；本报告是面向本项目的简要中文研究记录。
