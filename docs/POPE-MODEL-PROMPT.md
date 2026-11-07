你要在一个已有的 Minecraft Java 1.21.11 数据包+资源包项目里，为 Boss「教皇」建模并制作动作。外形和动作复刻《Minecraft Dungeons》的 Arch-Illager。全程用中文回复。

## 1. 项目与目标

仓库：D:\agent\claude\github-create\tralancer-rpg-1.21.11
主要参考：https://minecraft.wiki/w/Dungeons:Arch-Illager/Gallery
行为说明：https://minecraft.wiki/w/Dungeons:Arch-Illager

这个项目用 item_display 拼装模型，骑在隐身载体上，再把动画烘焙成 mcfunction。

先通读：
- `_tools/display_mob.py`：共用管线
- `_tools/add_tower_guard.py`：薄配置写法，含音效和 cues
- `_tools/add_abaddon_model.py`、`_tools/abaddon_geo.py`：最接近的 Boss 例子
- `_tools/tower_guard_ref/tower_guard.bbmodel`：模型源文件格式
- `_tools/tower_wraith_ref/SOURCES.md`：署名格式

## 2. 交付内容

- `_tools/pope_ref/pope.bbmodel`：模型和全部动作，这是事实来源
- `_tools/pope_ref/`：原始素材、音效、`SOURCES.md`、`sockets.json`、各阶段报告
- `_tools/add_pope_model.py`：薄配置，写法同 `add_tower_guard.py`
- 在 `_tools/rp_build.sh`、`_tools/build.sh` 挂上生成器，并放在 `add_tower_wraith.py` 之后、`add_pope_fight.py` 之前
- README「素材来源」增加一行署名

固定配置，不要改：key=`pope`，label=`教皇`，tag=`rpg.pope`，score=`rpg_pp`。

载体：隐身卫道士，写法同 `add_tower_guard.py`，`rpg:pope/summon` 只负责生成带 `rpg.pope` 标签的载体和部件。血量写 1000，其他战斗属性由玩法侧接管。

## 3. 玩法接口

玩法已经由另一个会话在做。它按下面的 clip 名调用 `rpg:pope/anim/enter/<clip>`，所以名字和顺序必须一致：

| 顺序 | clip | 循环 | 原作参照 | 玩法用途 |
| --- | --- | --- | --- | --- |
| 0 | `idle` | 是 | `MCD_Arch-Illager_Idle.gif` | 站立 |
| 1 | `walk` | 是 | `MCD_Arch-Illager_Run.gif` | 移动 |
| 2 | `attack` | 否 | `MCD_Arch-Illager_Basic_Attack.gif` | 三连能量弹、近身推击 |
| 3 | `summon` | 否 | `MCD_Arch-Illager_Summon_Circle.gif` | 环形召唤圣卫 |
| 4 | `cast` | 否 | `MCD_Arch-Illager_Summon_Single.gif` | 加护、圣血祭、收回契约 |
| 5 | `appear` | 否 | `MCD_Arch-Illager_Appear.gif` | 登场 |
| 6 | `teleport_in` | 否 | `MCD_Arch-Illager_Teleport_(Appear_Short).gif` | 瞬移出现，0.9 秒 |
| 7 | `teleport_out` | 否 | 同上，反向或按页面说明 | 瞬移消失，0.9 秒 |
| 8 | `whirlwind` | 否 | `MCD_Arch-Illager_Defeated_in_a_Whirlwind_in_game.gif` | 被权杖吸入，之后变成末影之心 |

报告里要写明每段的时长，以及 `attack`、`summon`、`cast` 的出手时刻（从 clip 开始算的秒数）。

`sockets.json` 要给出这些挂点，格式参考 `_tools/heart_of_ender_ref/m3_motion/sockets.json`，在 `idle` 和各段出手时刻取值：
- `staff_tip`：权杖顶端，能量弹和特效从这里发出
- `right_hand`、`left_hand`
- `head_top`：头顶

## 4. 不要做的事

- 不做玩法、AI、血量逻辑、技能、掉落、特效
- 不改 `_tools/add_pope_fight.py`、`rpg:pope_fight/`、`docs/POPE-DESIGN.md`，这些属于玩法会话
- 不改其他怪的模型和行为
- 不动末影之心的文件，`_tools/heart_of_ender_*` 由另一个任务负责
- 不动 opt_runtime_hotpaths 里的 DEVIL_SMOKE，不动 STRIDE=4 和 rpg.hurt 逻辑
- `display_mob.py` 尽量不改。确实要改时必须向后兼容，并证明现有怪的生成结果逐字节不变
- 同一工作区还有其他会话在改文件：只碰自己的路径，不要回滚、格式化或顺手修别人的改动
- `_data_loot.json`、`_guide_sections.json` 的换行差异是构建产物，不要提交
- 没有用户明确要求，不提交、不推送、不切分支
- 用户要求提交时，只暂存自己的路径，并使用：
  `git -c user.name=fanxing1515 -c user.email=fanxing1515@gmail.com commit`

## 5. 素材

地址：`https://minecraft.wiki/images/<文件名>`
curl 会被 Cloudflare 拒绝（403）。可用办法：在本机起一个 POST 接收页，用浏览器打开它，在该页面里 fetch wiki 的 /images/ 地址（响应带 ACAO *），再 POST 回本机。在 wiki 标签页里直接 POST 回本机会卡住。如果既没有浏览器也拿不到文件，停下来告诉用户。

下面文件名来自图库页面。图库里显示的是缩略图，下载时用不带 `120px-` 前缀的原文件名，下载后自行确认。

项目里已有，直接引用，不要重复存一份：
- `_tools/heart_of_ender_ref/MCD_Arch-Illager_(texture).png`（64×64）
- `_tools/heart_of_ender_ref/MCD_Arch-Illager_(shadow_texture).png`

要下载的渲染图和贴图：
- `MCD_Arch-Illager.png`：主要外形参照
- `MCD_Arch-Illagers_Staff.png`：权杖渲染图，无发光
- `T_SuperStaff.png`：权杖贴图
- `T_SuperCube.png`：方块贴图，核对是否属于权杖顶部

要下载的动图：
- `MCD_Arch-Illager_Idle.gif`、`MCD_Arch-Illager_Idle_Highblock_Halls_(front_view).gif`
- `MCD_Arch-Illager_Run.gif`、`MCD_Arch-Illager_Basic_Attack.gif`
- `MCD_Arch-Illager_Summon_Circle.gif`、`MCD_Arch-Illager_Summon_Single.gif`
- `MCD_Arch-Illager_Appear.gif`、`MCD_Arch-Illager_Teleport_(Appear_Short).gif`
- `MCD_Arch-Illager_Defeated_in_a_Whirlwind_in_game.gif`、`MCD_Arch-Illager_Defeated_in_a_Whirlwind.gif`

要下载的截图：
- `Arch-Illager_sit_in_his_throne_room_front_view.jpg`
- `Arch-Illager_ready_to_fight.png`
- `Arch-Illager_defeated.png`
- `Arch-Illager_defeated_in_a_whirlwind_lose_crowns.jpg`

音效（页面 Sounds 一节的实际链接为准，保留原名放到 `_tools/pope_ref/sounds/`，不下载 Music）：
- `Sfx_boss_ArchillagerIdle`、`Sfx_boss_ArchillagerHurt`、`Sfx_mob_archillagerHargh`、`Sfx_mob_archIllagerHaha`、`Sfx_mob_archIllagerLaugh`
- `Sfx_mob_archIllagerAppear`、`Sfx_mob_archIllager_mirrorIn`、`Sfx_mob_archIllager_mirrorOut`
- `Sfx_mob_archIllager_loadSpell`、`Sfx_mob_archIllager_spell`、`Sfx_mob_archIllager_spellDissapear`
- `Sfx_boss_archillagerSummonMobs`、`Sfx_boss_ArchillagerMagicImpact`、`Sfx_boss_ArchillagerWhirlwind`
- `Sfx_boss_archIllagerIntroGreetings`、`Sfx_boss_archillagerIntroLaugh`、`Sfx_boss_archillagerIntroFinalBlow`

Archvessel、Archvisage 开头的音效属于末影之心，不下载。

版权：素材可以使用，但必须署名。README「素材来源」和 `SOURCES.md` 要写明版权属于 Mojang、本项目非商业、与 Mojang 无关联。

## 6. 建模要求

- 按原作外形做：蓝袍、金属大项链和红宝石、皇冠、权杖。这次不改成三重冠或白袍，配色不做改动。
- 用 64×64 原贴图。先反推它的 UV 展开：每个面都要能说清取自贴图哪个区域，不允许目测贴图。
- 贴图放进一张图集，贴图以 base64 内嵌。
- 皇冠和权杖必须是独立部件，`whirlwind` 里要用到掉冠和权杖脱手。
- 权杖发光部分放在独立发光骨骼上。原作权杖的发光渲染看不到时，先照无发光渲染图做，并在报告里说明。
- 只有半透明才能实现的效果先不做。

## 7. 管线硬限制（来自 display_mob.py，违反会报错或显示错误）

- 坐标：Java 模型空间，+y 向上，生物面向 -z
- 只读 textures[0]
- 面的 uv 按 [u0,v0,u1,v1] 读取，texture 为 null 的面会跳过
- 每个部件内的元素，以该部件包围盒居中后坐标必须在 -16..32，也就是单个部件最多约 48 单位。大体型靠 model_scale 放大
- parts 的第一根骨骼是动画骨骼，可以有任意 rest 旋转。合并进来的子骨骼 rest 旋转只能绕一个轴，且不超过 ±45°
- 每个独立运动的部件就是一个 item_display 实体。目标不超过 12 个部件，超出要说明理由
- 动画通道只有 rotation 和 position，没有 scale。关键帧数值必须是纯数字，不能用 Molang；插值只支持 linear、catmullrom、step
- 同一时间只播放一段 clip
- clips 里 idle 和 walk 必须排在最前
- 动画名写成 animation.<clip>
- 关键帧旋转是在骨骼 rest 欧拉角上直接相加，position 直接相加，没有 Bedrock 的符号翻转
- 从 Bedrock geometry 导入 Blockbench 时，x、y 旋转会取反，x 位置会镜像。导入后要核对
- 载体隐身的处理方式参照 `add_abaddon_model.py`（tick_late）

工具：优先用 Blockbench。没有的话，用 Python 脚本直接生成 `.bbmodel`，脚本留在 `_tools/`，并保证 Blockbench 能正常打开。在 Blockbench 里手改过的内容，要写明生成脚本无法重现。

体型：游戏内身高约 2.6 格，靠 model_scale 实现。

## 8. 动作要求

每段动作在报告里标注「有动图」或「推断」。

对照方法：把动图抽帧，挑出关键姿态并标时间点，在 Blockbench 里摆姿势，最后把模型渲染和动图同一时刻并排对比。不要凭感觉做一段“差不多”的动作。

`teleport_out` 如果原作只有一段共用动画，就按页面说明处理，并在报告里写明。

`whirlwind` 只做到人物被吸走的结束姿态，不做旋风特效。结束时所有部件要能收拢到中心，因为之后末影之心会从这里升起。

音效用 sounds、cues、enter_cues 绑定到对应帧，写法同 `add_tower_guard.py`。

## 9. 分阶段交付（每阶段完成后先停下，等用户确认）

- M1 素材与结构：下载并校验素材，写 `SOURCES.md`，抽帧，交 UV 映射表、部件表和动作关键姿态表。
- M2 静态模型：交对照图（正面、侧面、背面、四分之三视角，和渲染图并排）。用户确认前不要开始做动作。
- M3 动作：交每段动作的关键帧对照图、时长表和 `sockets.json`。
- M4 接入与验证：跑通构建和测试，给出调试命令。

## 10. 验证

- 运行 `_tools/rp_build.sh`、`_tools/build.sh`，确认没有报错
- 运行 `_tools/rp_validate.py`，确认没有问题
- 运行 `_tools/server_test.py`，确认数据包没有函数加载错误（用法看脚本本身）
- 确认部件清理：载体被移除后没有残留的 item_display
- 能进游戏就截图验证；不能的话，明确写「未在真实游戏内看过」
- 不要因为构建通过就说完成。视觉还原度必须靠并排对照图判断

测试实例在 `D:\minecraft\PCL启动器\.minecraft\versions\1.21.11-Fabric 0.19.3`。同步前先问用户。

## 11. 这个项目踩过的坑

用户曾因为这些问题打回模型，请提前规避：
- 贴图映射靠目测。每块贴图都要能说清取自原图哪个位置
- 头、肩、手臂的相对位置不对，模型看起来松散。骨架要紧凑，以原图比例为准
- 手和肢体末端的朝向猜错后反复修改。拿不准时，把 2～3 个方案渲染出来让用户选，不要一直猜
- 把内衬放在已被别的部件占用的贴图区域，出现了杂色条
- 披风、背部部件前后装反。背面一定要检查
- 只看正面。每次对照都要包含侧面和背面

## 12. 汇报方式

如实汇报。没做的、没验证的、推断的都要写明，不要把推断说成复刻。遇到需要用户决定的问题就停下来问。
