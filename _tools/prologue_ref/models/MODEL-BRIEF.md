# 序章建模任务：路西法、天使士兵、座天使，以及 18 段过场动画

在 Blockbench 里做，只交 `.bbmodel` 与贴图；不改项目代码。只在 `_tools/prologue_ref/models/out/` 里写文件（不要改 `refs/` 里的原件）。

## 背景

《破碎大陆》序章：一千年前的哈米吉多顿，路西法带着别西卜、贝利尔、玛门与天使长米迦勒决战，必然落败。
过场由游戏里的展示实体演员演出：每个 `.bbmodel` 里的骨骼组会被转换成一个个物品模型，动画逐帧烘焙成函数。
所以模型必须满足下面的转换规则，动画用骨骼的旋转 / 位移 / 缩放关键帧来做。

参考文件在 `refs/`：

| 文件夹 | 内容 |
| --- | --- |
| `refs/michael/` | 米迦勒：`michael.bbmodel`（英雄骨架 + 六翼，256×256 图集 `atlas.png`）、`render.png`（游戏里的样子） |
| `refs/beelzebub/`、`refs/belial_lord/`、`refs/mammon_lord/` | 三位恶魔领主的模型、图集与渲染图 |
| `refs/watchling/` | 守望者（满身眼睛的末影族），座天使的风格参考 |

## 转换规则（每个模型都必须满足）

- 工程格式「Generic Model」（free），图集一张，尺寸 256×256（座天使可以 128×128）。
- **只用方块（cube），不用网格（mesh）。** 单个方块的旋转只能绕一个轴，角度是 22.5° 的倍数（−45 到 45）。需要更斜的角度时，放进一个带旋转的组里。
- 骨骼组的名字用英文，不能重名。
- 动画名写成 `animation.<名字>`，和 refs 里已有的动画一样；时间单位秒，帧率 20。
- 贴图像素风格、硬边，没有半透明（米迦勒是灵体，序章里是实体，所以也不要半透明）。

---

## 任务 1：路西法（堕天前的晨星）

**做法：复制 `refs/michael/michael.bbmodel`，在它上面改。** 保留全部 `J_` 开头的骨骼（`J_Root`、`J_Hip`、`J_Spine`、`J_Shoulders`、`J_L_Arm`、`J_R_Hand`、`J_R_Weapon`、`J_Head`……）的名字、层级与枢轴点不动，这样所有现成的英雄动作都能直接用。外观部分（盔甲、头部、翅膀、武器）可以改形、增减方块。

- **造型：** 最美的天使、早晨之子。白金天使甲：白色胸甲与护肩、金色镶边，胸口一颗小晨星；长发（金或浅金）；六翼，洁白羽翼、金色羽尖。
- **配色：** 白 `#FFFFFF`、暖白 `#FFF2C8`、金 `#F2CF7A` `#D4AF37`；**点缀一点蛇绿** `#5FD68C` `#00491C`（镶边内衬、腰带、翅膀内侧根部），绿只占很小的面积，它是路西法的特征色。
- **武器：** 右手（`J_R_Weapon` 下）拿一杆长枪「路西法」：白金枪身、蛇绿枪尖，长约 2.5 格。删掉米迦勒的脊骨与肋骨。
- **两张图集（同一套 UV）：**
  1. `out/lucifer/atlas.png`：正常的晨星路西法；
  2. `out/lucifer/atlas_possessed.png`：被敌基督的本源占据后：白甲染成暗红到黑，金色褪成锈铜，蛇绿变成病态的暗绿，眼睛发红，翅膀发黑。
- **输出：** `out/lucifer/lucifer.bbmodel`、两张图集、`out/lucifer/render.png`（正面渲染一张）。

## 任务 2：序章的米迦勒与天使士兵（用户 2026-11-22 指定）

两个模型都用《Minecraft Dungeons》原作的玩家英雄网格（`SK_Player_Master`，骨架 `Player_Master_Skeleton`），**保留原作 `J_` 骨骼的名字和层级**（和 `refs/michael/michael.bbmodel` 是同一套骨架，现成的英雄动作和本说明里的新动画都能直接用）。

- **序章的米迦勒**：皮肤用原作的 Corrupted Defender（`Skins/Corrupted_Defender/T_Corrupted_Defender`，wiki：https://minecraft.wiki/w/Dungeons:Corrupted_Defender）。
- **天使士兵**：皮肤用原作的 Sven（`Skins/Sven/T_Sven_Skin`，wiki：https://minecraft.wiki/w/Dungeons:Sven）。
- **盔甲（两者都穿）**：米迦勒现在的盔甲是霜冻护甲 `Actors/Equipment/Armor/SnowArmor_Unique1`（`BP_SnowArmor_Unique1` 的六件静态网格、骨架插槽和相对变换），但游戏里那份做成了半透明的灵体，**请从原作重新解包一份不透明的**，按蓝图的插槽与变换挂上去。配色改成神圣系列的大体配色：白 `#FFFFFF`、暖白 `#FFF2C8`、金 `#F2CF7A` `#D4AF37`，圣焰橙 `#FF805F` 只作点缀。
- **米迦勒另外加上**：六翼（照 `refs/michael/` 里六翼的结构与位置，实体不透明，白金配色）和右手的脊骨（照 `refs/michael/` 里 `J_R_Weapon` 下的 `spine`）。
- **天使士兵另外加上**：两片翼（比米迦勒的小、朴素，灰白），右手一把普通的长剑。
- 输出：`out/michael_prologue/michael_prologue.bbmodel` + `atlas.png` + `render.png`；`out/angel_soldier/angel_soldier.bbmodel` + `atlas.png` + `render.png`。

## 任务 3：座天使（新模型）

第三波的精英怪：一团悬在空中的「眼」，周围四只眼轮。`out/throne/throne.bbmodel` + `out/throne/atlas.png`。

- 顶层五个组，**名字必须是** `core`、`wheel_up`、`wheel_down`、`wheel_left`、`wheel_right`（玩家要分别打碎四只眼轮，代码按名字把它们隐藏）。
- `core`：直径约 1.5 格的球状一团，正中一只大眼，外面一圈金色的羽环。
- 四只眼轮：直径约 1.2 格的轮子，轮缘一圈小眼睛。位置相对 `core` 中心：上 (0, 2.2, 0)、下 (0, −2.0, 0)、左 (0, 0, 2.4)、右 (0, 0, −2.4)（单位：格；Blockbench 里 1 格 = 16）。
- 配色白金：白 `#FFFFFF`、`#FFF2C8`、金 `#F2CF7A` `#D4AF37`，瞳孔近黑 `#1A0500`，眼白之外可点一点圣焰橙 `#FF805F`。风格参考守望者的「满身眼睛」，但它是天使，干净、明亮。
- 动画：`animation.idle`（循环 2 秒：四只眼轮各自缓慢自转，core 轻微上下浮动）。

---

## 任务 4：18 段过场动画

每段的时长、动作都来自脚本书。做在对应模型的副本上，存成新文件（**不要改 refs 里的原件**，项目会按骨骼名把动画合并进去）。没写「循环」的都是播一次、停在最后一帧。

### 路西法（做在 `out/lucifer/lucifer.bbmodel` 里，8 段）

| 动画名 | 时长 | 动作 |
| --- | --- | --- |
| `address` | 4.5 秒 | 半转身面向身后的随从，抬手说话，最后一句「我不跪」时手猛地收回、挺直 |
| `look_up` | 1.5 秒 | 抬头仰望天空，身体微微后仰 |
| `seized` | 2.5 秒 | 突然僵住，身体抽搐几下，头向后仰，手指张开（被敌基督控制） |
| `pierced` | 2.0 秒 | 胸口被长矛贯穿：向后一顿、弯腰、踉跄半步 |
| `tear` | 2.5 秒 | 双手在身侧向外猛地撕开（撕开空间裂缝），翅膀张开 |
| `reach` | 1.5 秒 | 伸手向身侧的裂缝，向前倾 |
| `stomped` | 2.0 秒 | 被一脚踩倒：向后仰倒，四肢摊开，停在仰面朝天的姿势 |
| `pit_rise` | 2.0 秒 | 仰躺在坑底，慢慢抬起头，最后定在抬头看上方的姿势 |

### 米迦勒（做在任务 2 的 `out/michael_prologue/michael_prologue.bbmodel` 里，4 段）

| 动画名 | 时长 | 动作 |
| --- | --- | --- |
| `dive_cry` | 2.0 秒 | 自高空俯冲：身体前倾、六翼收拢向后，右手高举脊骨，最后半秒张口高呼（「谁似神！」） |
| `throw` | 1.5 秒 | 投标枪式：后撤蓄力、右手把脊骨用力掷出，跟随动作 |
| `stomp` | 1.0 秒 | 抬起右脚、重重踩下，身体随之下压 |
| `look_down` | 2.0 秒 | 低头俯视脚下的深坑，肩膀微沉（疲惫，不是得意） |

### 别西卜 / 贝利尔 / 玛门（各复制自己的 refs 模型，存为 `out/<文件夹名>/<文件夹名>_prologue.bbmodel`，每位 2 段，共 6 段）

| 动画名 | 时长 | 动作 |
| --- | --- | --- |
| `talk` | 2.4 秒，循环 | 说话时的手势：别西卜懒散地挥一下手；贝利尔轻慢地摊手、歪头；玛门搓手指、点一下胸前 |
| `flee` | 1.5 秒 | 回头看一眼（留下一句话），然后转身向前纵身一跃（跃进空间裂缝） |

---

## 交付清单

```
out/lucifer/lucifer.bbmodel          路西法模型 + 8 段动画
out/lucifer/atlas.png                正常图集
out/lucifer/atlas_possessed.png      被占据图集（同一套 UV）
out/lucifer/render.png
out/michael_prologue/michael_prologue.bbmodel  序章的米迦勒（Corrupted Defender + 重新解包的神圣配色霜冻护甲 + 六翼 + 脊骨）+ 4 段新动画
out/michael_prologue/atlas.png
out/angel_soldier/angel_soldier.bbmodel        天使士兵（Sven + 同一套盔甲 + 两翼 + 长剑）
out/angel_soldier/atlas.png
out/throne/throne.bbmodel            座天使模型 + idle 动画
out/throne/atlas.png
out/beelzebub/beelzebub_prologue.bbmodel     别西卜 + 2 段
out/belial_lord/belial_lord_prologue.bbmodel 贝利尔 + 2 段
out/mammon_lord/mammon_lord_prologue.bbmodel 玛门 + 2 段
out/REPORT.md                        每个文件做了什么、方块数、有没有偏离上面的规则
```

## 不要做的事

- 不改 `refs/` 里的文件，不改项目里任何别的文件。
- 不要用网格（mesh），不要用半透明贴图。
- 不要重命名或移动 `J_` 开头的骨骼；不要删掉现成的动画。
