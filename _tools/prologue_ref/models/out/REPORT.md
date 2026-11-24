# 《破碎大陆》序章模型交付

路西法常态使用 Kelptomaniac 和 Full Metal Armor，敌基督侵染后换成 End Rogue 和 Dark Armor。两套外观共用同一份模型和过场动画。常态右手持 TRA 蛇枪「路西法」，切换到侵染形态时蛇枪随即消失。米迦勒使用 Corrupted Defender、重新解包的实体霜冻甲与赤橙六翼。天使士兵使用 Sven、银白霜冻甲和浅灰白翼。这些英雄外观在原作中共用英雄模型 `SK_Player_Master`，角色身份来自各自的原版皮肤。

## 文件

以下路径相对于本报告。表内 PNG 展示图均由 Blockbench 正面附近的正交视图截取，尺寸为 960 × 960，背景透明。

| 文件 | 内容 |
| --- | --- |
| [lucifer/lucifer.bbmodel](lucifer/lucifer.bbmodel) | 498 个方块，129 个组，包含可由图集切换的两套盔甲。保留英雄骨架和 33 段原动画，新增 8 段过场。常态右手枪长按模型比例折合 40 像素，即 2.5 格。 |
| [lucifer/atlas.png](lucifer/atlas.png) | 256 × 256 常态图集。Kelptomaniac 的衣物和额上海藻采用蛇绿，脸和四肢使用米迦勒的肤色。全金属甲的金饰取自古金羽尖，其余部分保留原版钢灰。与模型内嵌 PNG 字节相同。 |
| [lucifer/atlas_possessed.png](lucifer/atlas_possessed.png) | 256 × 256 附身图集。将模型的唯一纹理替换为此文件即可同时显出炭黑铁灰的 End Rogue、Dark Armor 实际几何、黑羽及红眼，收起常态甲件和整杆蛇枪。 |
| [lucifer/render.png](lucifer/render.png) | 常态正面持枪照，以展示姿势展开蛇枪侧面。 |
| [lucifer/render_possessed.png](lucifer/render_possessed.png) | 侵染形态的空手正面照，展示 End Rogue 的红眼、Dark Armor 黑盔和黑羽。 |
| [michael/michael_prologue.bbmodel](michael/michael_prologue.bbmodel) | 424 个方块，115 个组。重新装配实体六件霜冻甲，保留 33 段原动画，新增 4 段过场。Corrupted Defender 面容和六翼保留。实体图集内嵌于模型。 |
| [michael/render.png](michael/render.png) | 本轮配色修订补充的持脊骨正面照，可直接比较护甲、羽翼和武器上的赤橙色。 |
| [michael/throw.gif](michael/throw.gif) | Blockbench 侧面投掷预览，包含蓄力、出手和尖端向前的飞行。 |
| [angel_soldier/atlas.png](angel_soldier/atlas.png) | 256 × 256 的 Sven 图集。可直接使用米迦勒的 424 方块模型和原 UV。银色霜冻盔下可见 Sven 的面部，六翼共用完整的浅灰羽纹。 |
| [angel_soldier/render.png](angel_soldier/render.png) | 使用士兵图集与英雄模型，仅显示中间一对翼。 |
| [throne/throne.bbmodel](throne/throne.bbmodel) | 981 个方块，203 个组。潮涌核心球壳、金虹膜竖瞳、24 片轻羽与四只金轮保留。含待机、行走、奔跑、眨眼及两段带前进位移的动作。 |
| [throne/atlas.png](throne/atlas.png) | 128 × 128 单图集。在原透明区添加了所有轮眼共用的 16 × 12 闭眼裁片，保留原金边、透明轮廓及全部原裁片。 |
| [throne/render.png](throne/render.png) | 新模型睁眼时的 Blockbench 正面截图，960 × 960，透明背景。 |
| [throne/movement.gif](throne/movement.gif) | 同比例、固定机位、实时速度的 Blockbench 走跑对照。地面网格每格对应游戏里的一格。 |
| [throne/blink.gif](throne/blink.gif) | Blockbench 主眼与单只眼轮的同步近景，可观察上下眼睑闭合与重新睁开。 |
| [beelzebub/beelzebub_prologue.bbmodel](beelzebub/beelzebub_prologue.bbmodel) | 别西卜。82 个方块，46 个组。保留 5 段原动画，新增懒散挥手和转身跃离。 |
| [belial_lord/belial_lord_prologue.bbmodel](belial_lord/belial_lord_prologue.bbmodel) | 贝利尔。195 个方块，37 个组。保留 5 段原动画，新增轻慢回应和跃离。 |
| [mammon_lord/mammon_lord_prologue.bbmodel](mammon_lord/mammon_lord_prologue.bbmodel) | 玛门。129 个方块，79 个组。保留 5 段原动画，新增搓手点胸和跃离。 |

## 三位领主的堕落前天使形态

三位天使单独交付在各领主的 `prefall/` 目录。每套使用《Minecraft Dungeons》的 `SK_Player_Master` 英雄骨架，以及序章路西法侵染形态的三对黑羽。头盔为独立挂件。每个目录含自带图集的模型、同内容的 `atlas.png`、Blockbench 戴盔全身照 `render.png` 和卸盔面容 `face.png`。三位的截图可在[同框对照图](prefall_lords.png)查看。

| 天使身 | 人物、装备与配色 | 过场动作 |
| --- | --- | --- |
| [别西卜](beelzebub/prefall/beelzebub_prefall.bbmodel) | Blacksmith 的完整原皮肤，穿六件 Turtle Armor（`TurtleArmor`）。开面龟甲采用领主的暗橄榄至黄绿色阶，露出眉眼和棕须。胸前浅色甲片轻调为黄绿米色，腰带与铁扣沿用原色。139 个方块。 | 抬起一只手懒散地挥过，再垂下。 |
| [贝利尔](belial_lord/prefall/belial_lord_prefall.bbmodel) | Amethyst Scout 的完整原皮肤，深肤色、淡紫发，搭配紫色下装与深靴。沿用四件原装 Teleportation Robes（`EndRobes`），开面兜帽、袍身和双袖均为深紫底配浅金边。133 个方块。 | 打开双臂摊手，同时侧头。 |
| [玛门](mammon_lord/prefall/mammon_lord_prefall.bbmodel) | Baako 身体，穿六件原装 Golden Piglin Armor（`PiglinArmor_Unique1`）。黑褐甲面带橙金色条纹，配炭黑皮革。胸坠沿用地下城猪灵商人的金饰几何，腰间钱袋使用商人的皮革与金币裁片。197 个方块。 | 双手收拢，拇指与食指搓动，然后抬手点胸。 |

每位有各自的 `animation.talk`（2.4 秒循环）与 `animation.flee`（1.5 秒，回望、转身、展翼跃离），均按英雄骨架重新制作。三套黑翼均保留 24 个原羽翼方块。别西卜龟甲按不透明原色一对一映射到领主黄绿色阶，保留原像素纹样、明暗层次与 Alpha。贝利尔和玛门两张 64 × 64 护甲原图已与解包贴图逐像素核对 RGBA，8,192 个像素全部一致。三份模型均已在 Blockbench 打开，并用项目转换器检查了部件及两段过场的逐帧姿态。当前游戏演员仍使用原序章模型。

## 游戏素材与配色

- **路西法。** 本机游戏包导出的 `Actors/Characters/Player/Master/Skins/Kelptomaniac/T_Kelptomaniac` 与 `Actors/Equipment/Armor/FullPlateArmor_Unique1/T_FullPlateArmor` 分别对应图集左上两块 64 × 64 区域。两块区域保留原始 UV、纹样和透明遮罩。衣物从深蛇绿过渡至亮蛇绿，色阶包含 `#00491C`、`#2FA866` 和 `#5FD68C`。脸部和四肢采用米迦勒 Corrupted Defender 皮肤实际使用的六档肤色，保留 Kelptomaniac 的青蓝头发、眼白和瞳孔。游戏外观表的 `kelptomaniac` 使用材质 `MI_Kelptomaniac` 和共用英雄骨架。常态主体的 79 个方块已按原皮肤 UV 取色，其中 19 个方块的派生裁片重新烘焙。全金属甲与其衍生裁片上的四档金色取自本模型六翼贴图。护甲原图上共替换 96 个金饰像素，钢灰甲板使用解包原色。护甲的六件几何来自 `FullPlateArmor`，安装位置、方向及大小取自 `BP_FullPlateArmor_Unique1`。
- **侵染后的路西法。** 游戏外观表中的 `endrogue` 指向 `End_Rogue/MI_EndRogue`。侵染主体以 `T_EndRogue_Skin` 为底图，保留 End Rogue 的兜帽、面罩、绑带和衣褶的原像素分布，以 Dark Armor 的炭黑、铁灰和暗红重配色，保留原眼位的红色高光。79 个英雄方块的裁片采用暗甲原图提取的 19 级灰色和 3 级深红，主体的青绿与蓝紫已移除。按游戏 `DarkArmor/BP_DarkArmor` 蓝图重装胸甲、头盔、左右肩四个实际挂件，使用原版 `T_DarkArmor`。真实蓝图虽有配套腿网格可供导出，此套装备的蓝图只挂这四件。230 个源三角各转换一次，得到 115 个方块。附身图集右下 128 × 128 专供暗甲，常态图在此透明。附身图把旧全金属甲的纹理区域设为透明，因此同一套 UV 即可切换甲件轮廓。
- **路西法的枪与翼。** 枪身取项目 `resourcepack/assets/rpg/textures/item/lucifer_in_hand.png` 和已导出的原持枪物品几何 `_tools/lucifer_ref/verdant_animation_sources/weapon_source/weapon_existing_generated.json`。保留 137 个原物品方块、UV 朝向与镂空，沿项目已有的第 (18, 19) 像素握点等比缩放并绑定 `J_R_Weapon`。侵染图集把蛇枪独占的 32 × 32 区域设为全透明，137 个枪方块在这套形态下全部不可见。六翼沿用参考米迦勒的 24 个翼方块、骨组和翼形。两人在序章中分别使用各自的羽色。
- **米迦勒。** 从本机游戏包重新导出英雄本体、`Skins/Corrupted_Defender/T_Corrupted_Defender`、`SnowArmor_Unique1/T_SnowArmor_Unique1` 和 `FrostArmor_Body / Head / Arm_L / Arm_R / Leg_L / Leg_R` 六件几何，按原蓝图插槽装配。原皮肤逐像素保留。盔甲保留原版像素明暗，盔甲与羽翼采用脊骨武器的暗红橙 `#A1260B` 和赤橙 `#FF3300`，由珊瑚橙过渡到骨色高光。可见像素全部实体化。
- **天使士兵。** 从同一游戏包重新导出 `Skins/Sven/T_Sven_Skin`，把原皮肤逐像素保留在图集内。沿用英雄骨架、六件甲的原始 UV 和六翼的镂空，兵甲单独使用银灰色阶。士兵图集中已移除米迦勒个人武器的可见像素。
- **座天使。** 主眼取自 `Content_DLC6/Actors/Characters/Enemies/Endersent/T_EyeofEnder`，将原眼纹的亮斑、虹膜和竖瞳映射成暖白、琥珀金与近黑。球壳取自潮涌核心的 `Content_DLC5/Actors/Items/Conduit/SM_OceanSphereC`。源网格的 485 个体素合并为 13 个方块，414 个外露单位面逐一吻合，三轴直径均为 24 模型像素（1.5 格）。主眼保留原有金色虹膜、深色竖瞳和两处白色高光；121 个可见眼纹像素保持原正面位置和 UV，跨台阶处沿球壳折面贴合。背面嵌入末地传送门 `EndPortal/SM_EyeofEnder_01` 的立体浮雕，保留原网格的阶梯外缘与 UV。羽冠使用 `Actors/Items/LightFeather/SM_LightFeather` 和 `T_LightFeather`，将原羽片的成对表面合并成实心方块，前后两列各 12 片。四只眼轮取虚弱之锣 `Actors/Items/GongOfWeakening` 的金属纹理与轮缘造型，重组为八段镂空轮框，并在正反面镶上末影眼纹。全模型朝 −X。
- **座天使待机与眨眼。** `animation.idle` 每 8 秒循环一次，主眼缓慢转向两侧并停住注视，羽冠随动作张合。主眼与每轮正反两面的 16 只小眼都有实体眼睑，待机、走、跑中均会眨眼。`animation.blink` 时长 1.2 秒，可单独触发一次。闭合时虹膜与竖瞳被眼睑盖住，再从中缝睁开。
- **座天使走跑。** `animation.walk` 和 `animation.run` 适合由演员控制世界位置。行走每 1.6 秒一轮，左右眼轮降至下轮高度，三个承重轮交替抬起、前伸和推地。奔跑每 0.8 秒一轮，两侧轮与下轮交替蹬地，主眼前倾，上轮维持平衡。过场可直接使用 `animation.walk_forward` 和 `animation.run_forward`，4.8 秒内沿 −X 分别前进 4.5 格和 18.9 格，由动作本身提供位移。
- **座天使验证。** 原 684 个方块与 62 个组保留原 UUID、几何、UV 及中立姿态。项目转换器按 20 fps 检查了六段动作共 574 个时点。以实际轮缘为地面接触点计算，行走全程有两至三轮支撑，奔跑每个周期有两次三轮同时离地。带前进位移时，各轮持续接地的相邻采样帧沿前进方向的滑移为零。
- **三位领主。** 几何与角色身份来自各自的参考模型。动作底姿分别来自地下城的 `NamelessKing_Walk`、`CauldronBoss_Idle` 和 `PiglinMerchant_Idle1`。

## 过场动作

下表名称在文件中均带 `animation.` 前缀。新动作采用 20 fps，台词循环动作首尾相接，单次动作使用 Blockbench 的 `hold` 停在末帧。

| 角色 | 动作与时长 |
| --- | --- |
| 路西法 | `address` 4.5 秒、`look_up` 1.5 秒、`seized` 2.5 秒、`pierced` 2 秒、`tear` 2.5 秒、`reach` 1.5 秒、`stomped` 2 秒、`pit_rise` 2 秒。 |
| 米迦勒 | `dive_cry` 2 秒、`throw` 1.5 秒、`stomp` 1 秒、`look_down` 2 秒。 |
| 别西卜、贝利尔、玛门 | 每位各有 `talk` 2.4 秒循环、`flee` 1.5 秒单次。 |

路西法的说话、抽搐、受创、撕裂、迈步和倒地使用解包的 `Player_Master_Idle`、`ShowOff`、`Stun`、`GetHitFront`、`Emote_MightySword`、`Walk_Glaive` 与 `DownedFloor_Initiate` 等英雄动作姿态，再按台词与镜头节拍调整。控制发作时左手四指与拇指展开，常态右手握枪，侵染态空手。倒地末帧与坑底首帧在全部 33 根动作骨上逐通道相接。坑底镜头随后抬头，视线朝上。

米迦勒在蓄力末段把脊骨尖端对准目标，0.75 秒离手后沿抛物线尖端朝前飞行。校验以原武器贴图的握点 (25.75, 25.75) 和尖端 (3.5, 3.5) 为准。按 20 fps 检查每个飞行关键帧，尖端与轨迹切线的夹角均小于 0.001°。投掷动画只用旋转和位移，便于现有转换器读取。右手持脊骨的默认展示收起备用双肋，原双持动作仍保留在文件里。

## 与原说明的差异及验证

1. 按最后指定的外观替换三位英雄。路西法采用 Full Metal Armor 的原版纹样与羽尖同色金饰，米迦勒新增赤橙实体材质，天使士兵使用 Sven。两位英雄的全部 `J_` 骨名、层级、枢轴和基准旋转与参考一致。原动画按原参数保留，包含其原有的帧率。
2. 贝利尔参考模型是带眼的炼药锅，以锅柄外摊、锅体侧倾和勺子摆动表达摊手、歪头。玛门的参考骨架使用整臂，通过两腕端交替靠近、细颤和点胸表达搓指。
3. 贝利尔的原 512 × 512 图集重排成 256 × 256，54 个源裁片保留像素，390 个有纹理的面只平移 UV。别西卜的 64 个半透明像素二值化，两个超出图集左边界约 0.002 像素的 UV 端点收回边界。参考模型中的缺省方块面补为无纹理面，以便 Blockbench 5.2.2 正常打开。
4. 对 6 个交付模型检查 Generic Model 格式、单图集、方块类型、英文组名唯一性、骨骼引用、UV 边界及透明度。本版通过项目 `display_mob` 读取器按有几何的骨组在内存中生成 378 个物品部件，其中座天使占 199 个。原 18 段角色过场已检查骨骼姿态。路西法八段动作逐帧抽查枪纹可见像素与头部内部区域，未发现相交。
5. Blockbench 已打开六个模型并抽看关键姿态，另行加载了附身图集、Sven 士兵图集。两套路西法甲件分别检查了在对应图集中的可见像素。五份角色参考模型与项目中的对应原件按文件内容核对一致。验证范围为 Blockbench 预览与项目转换器，没有进行 Minecraft 客户端内的整段序章联排。

本次解包、转换和动画中间件集中在 `_work/`，与上表中的交付文件分开。自动审批拒绝了清理中间件的删除操作，这些文件仍保留在本地。

## 领主补充动作

三位堕落前天使各追加六段动画，片名均带 `animation.` 前缀。下表时间以秒计，分角色的三个时间依次为别西卜、贝利尔、玛门。所有关键帧落在 0.05 秒的网格上。

| 动作 | 时长与播放方式 | 关键时点和姿态 |
| --- | --- | --- |
| `kneel_down` | 1.20 秒，`hold` | 从原待机开始。身体分别于 0.20、0.10、0.00 秒后开始下沉。1.20 秒时右膝侧着地，左脚在前撑稳，低头收翼，停住末帧。 |
| `kneel_idle` | 3.00 秒，`loop` | 0.00 秒承接落膝，1.50 秒胸背与翼羽达到呼吸峰值，3.00 秒回到同一跪姿。 |
| `kneel_up` | 1.20 秒，`once` | 0.00 秒从跪姿开始，0.60 秒处于起身中段，1.20 秒回到各自原待机首帧。 |
| `bow` | 1.80 秒，`once` | 三人分别在 0.35、0.20、0.15 秒开始俯身，手收向胸前。最低姿态分别保持在 0.85–1.35、0.70–1.20、0.60–1.10 秒，上身前倾 31°、30°、29°。1.80 秒回到原待机。 |
| `look_up` | 1.20 秒，`hold` | 别西卜在 0.25–0.85 秒后撤，贝利尔在 0.10–0.65 秒，玛门在 0.05–0.45 秒。左脚先抬、后撤、再落地，右脚支撑，胸颈合计上仰约 35°，翼半张。 |
| `shield` | 0.60 秒，`hold` | 手臂先抬到眉眼前，随后偏头后仰。三位的手臂分别在 0.45、0.30、0.20 秒到位，上身在 0.55、0.40、0.30 秒到位，翼向前护住两侧。 |

别西卜以沉肩、迟半拍的宽幅动作承重。贝利尔行礼时空出一手向外舒展，挡光时换左手护脸。玛门用更短的反应时间，空着的手往金币挂坠收。后撤动作让左脚后移 0.42 个模型单位，按三个序章演员现有的模型比例折合约 0.197 格。骨架根节点的水平位移全程为零。

原英雄骨架每条腿都是整块。跪姿利用现有腿部与护甲骨组摆出后侧平放、前脚支撑的姿态，再以模型原点的水平面校正膝侧前缘与前脚底。下翼以贴图上可见的羽尖定位。动作对照图使用同一比例的 Blockbench 正交相机，行礼取最低点，跪姿呼吸取中点，起身取回站末帧。

贝利尔的长袍另用原有下摆骨组绕腰缝轻提，让后摆随下跪离开地面。胸片与腰缝连接点保持原位。各模型同目录的 `_v1.bbmodel` 是修改前的逐字节备份。

落地测量取 Blockbench 实际绘制的面，按图集 Alpha 排除透明像素。三位在完整跪姿及跪姿呼吸中的右膝侧和左脚底均贴合 Y = 0，下翼尖与地面相距约 0.00001 个模型单位。起身末帧照原待机回放，保留了原鞋底相对原点已有的约 −0.053 至 +0.006 个模型单位偏差。

衔接核对覆盖别西卜的 99 个组、贝利尔的 97 个组、玛门的 114 个组。用项目转换器展开每个骨组的旋转与位移，缺省通道计零。逐轴核对后，下跪末帧等于跪姿待机的首帧、末帧，也等于起身首帧。起身和行礼的末帧均等于原待机首帧。另在 Blockbench 原生播放器逐组比较上述时点的世界变换矩阵，差值均为零。六段合计每位 186 个 20 fps 采样时点，三位共 558 个。

六翼另按 80 fps 抽查关键帧之间的线性插值，共 2,178 个姿态。核验使用贴图不透明区域的面交线，翼根周围 0.38 个模型单位作为连接区单列。连接区外，三人均未出现新的翼对翼或翼对身体部件的穿插。原待机已与手臂或甲片接触的羽片，在退出时可能扫过同一部件的相邻贴图面。逐部件核对后，其接触半径及交线总长均未超过原待机。完全共面的重合面不计入该项交线测量。全部采样中，可见羽片最低点均在地面或其上方。

游戏当前的 `LORD_CLIPS` 播放清单尚未注册这六个新片名。本次验收覆盖模型、项目转换器与 Blockbench，未在 Minecraft 客户端联排。

[别西卜动作对照](beelzebub/prefall/actions_beelzebub.png) · [贝利尔动作对照](belial_lord/prefall/actions_belial.png) · [玛门动作对照](mammon_lord/prefall/actions_mammon.png)
