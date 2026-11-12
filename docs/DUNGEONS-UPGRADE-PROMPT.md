你要在一个已有的 Minecraft Java 1.21.11 数据包+资源包项目里，用《Minecraft Dungeons》本体的原始资产做两批事：

- **第一批：** 给路西法二阶段「知善恶树」补齐原作特效。
- **第二批：** 把之前照 wiki 图片手工搭的模型，换成从本体提取的原件。

全程用中文回复。下面写明的直接照做，不用再调研；只在第 6 节的检查点停下来等用户。

## 1. 已有的东西

- **仓库：** `D:\agent\claude\github-create\tralancer-rpg-1.21.11`
- **游戏：** `D:\XboxGames\Minecraft Dungeons`。只读，不改、不移动、不整体复制 pak。
- **提取工具与索引：** `D:\agent\dungeons_extract\`
  - `exporter\`：CUE4Parse 导出程序，AES、UE 版本、压缩设置都已经调通。
  - `index\pak_files.tsv`：全部 134800 个文件的路径。
- **转换管线：** `_tools/convert_dungeons.py`、`_tools/dungeons_conversion/`，你做路西法二阶段时写的，照原流程用。
- **显示管线：** `_tools/display_mob.py`。
- **参考范例：** `_tools/add_lucifer_p2_model.py`。注意它的材质开关，默认 `plain`，原因见第 3 节第一条。

## 2. 第一批：知善恶树的原作特效

**用在哪：**
- 招式逻辑：`_tools/add_lucifer_fight.py`
- 设计：`docs/LUCIFER-P2-DESIGN.md` §3、§5
- 现有特效贴图：Codex 画的，在 `_tools/lucifer_p2_fx_ref/`，由 `_tools/add_lucifer_p2_fx_art.py` 处理

原作有对应资产的，用原作替换；原作没有的，保留 Codex 画的。

| 用途（现状） | 本体资产（`Dungeons/Content/Actors/Characters/Enemies/` 下） | 交付形式 |
| --- | --- | --- |
| 缠枝的藤蔓（现在用原版扭曲藤蔓方块顶替） | `JungleAbominationVine/SK_Abomination_Vine`、`T_Vine_Arm`，以及 `Animations/` 下的 4 段动作 | 展示实体模型和动作，规格见 `docs/LUCIFER-VINE-PROMPT.md`，那份的全部要求照做 |
| 禁果弹（现在是 Codex 画的苹果字形） | `PoisonQuillVine/BP_JungleAbominationPoisonProj`，以及它引用的 `PoisonQuillVine_Quill` 网格和贴图 | 一个 item 模型，用于飞行的 item_display，朝飞行方向 |
| 落地、坠天的冲击 | `JungleAbomination/PS_JungleAbominationLand`、`PS_JungleAbominationShockwave` | 读出这两个粒子系统引用的贴图，见下方说明 |
| 藤蔓破土的土块 | `QuickGrowingVine/ParticleEffect/QuickGrowingVine_Soil_ParticleSystem`、`PoisonQuillVine/ParticleEffects/PoisonQuillVine_Soil_Burst2_ParticleSystem` | 同上 |
| 毒刺和藤蔓的命中 | `PoisonQuillVine/ParticleEffects/PS_Hit_Posion_Quill`、`QuickGrowingVine/ParticleEffect/PS_VineHit` | 同上 |
| 罪约「失乐园」的尖根（现在是 Codex 画的 `root_spike`） | `Dungeons/Content/Effects/Flairs/RespawnFlairs/02/SM_Abomination_Vine`、`MI_AbominationVine` | item 模型 |

**粒子贴图的处理：**
- 粒子系统本身不转换，只导出它们引用的贴图，包括 SubUV 序列帧。
- 每张写明：来源粒子系统、帧数、行列排布、原始尺寸。
- 交付给 `add_lucifer_p2_fx_art.py` 使用。它按 16×16 或 32×32 定网格，所以你只交原图和元数据，不要自己缩放。

## 3. 第二批：手工模型换成原件

下表的模型都是早先照 wiki 图片手工搭的，或由图片推断。本体里有原件。

| 现有 key / 生成器 | 现在的外形 | 本体原件（`Dungeons/Content/` 下） |
| --- | --- | --- |
| `beelzebub` / `add_beelzebub.py` | Nameless One | `Actors/Characters/Enemies/NamelessKing/SK_NamelessKing` |
| `leviathan` / `add_leviathan_model.py` | Necromancer | `Actors/Characters/Enemies/SkeletonNecromancer/SK_SkeletonNecromancer` |
| `abaddon` / `add_abaddon_model.py` | Wretched Wraith | `Actors/Characters/Enemies/Wicked_Wraith/SK_WickedWraith_01` |
| `tower_wraith` / `add_tower_wraith.py` | Tower Wraith | `Actors/Characters/Enemies/TowerWraith/SK_TowerWraith` |
| `vanguard` / `add_vanguard.py` | Vanguard | `Actors/Characters/Enemies/SkeletonVanguard/SK_SkeletonVanguard` |
| `sunken_skeleton` / `add_sunken_skeleton.py` | Sunken Skeleton | `Content_DLC5/Actors/Characters/Enemies/SunkenSkeleton/SK_SunkenSkeleton` |
| `tower_guard` / `add_tower_guard.py` | Tower Guard | 动作在 `Actors/Characters/Enemies/Illagers/TowerGuard/Animations/`；网格先确认，可能复用 `Illagers/RoyalGuard/SK_IllagerRoyalGuard` |
| `pope` / `add_pope_model.py` | Arch-Illager | `Actors/Characters/Enemies/Illagers/ArchIllager/SK_ArchIllager`，另有 15 个粒子系统 |
| `heart_of_ender` / `add_heart_of_ender.py` | 末影之心 | `Actors/Characters/Enemies/Illagers/ArchVessel/SK_ArchIllagerAvatar`，先确认它就是末影之心 |
| `arch_visage` / `add_arch_visage.py` | 灾厄面容 | `Actors/Characters/Enemies/Illagers/ArchVisage/SK_ArchVisage` |

教皇战的特效也一样：`ArchIllager/` 下的 `PS_ArchIllager_Projectile`、`PS_ArchIllagerProjectileHit`、`PS_ArchIllager_StaffGlow_*` 等粒子系统，按第 2 节的方式导出贴图。用它们替换 `_tools/pope_fx_ref/` 里 Codex 画的对应项（光弹、命中、杖头光），并列出一张对照表。

**替换时必须守住接口。** 游戏逻辑依赖这些，换模型不能改：

- **身份：** key、tag、score 前缀不变。
- **部件数：** 不超过现在的数量。确实要超过的，在检查点说明。
- **动作：** clip 名字和时长、出手帧（技能时序对着它）、`sockets.json` 里的挂点（杖头、嘴部等）。
  - 原作动作和现有 clip 对不上的，列出对应表，由用户在检查点决定。
- **手持物：** `held=` 的手持武器位置。
- **用户以前确认过的外观细节**（见 `C:\Users\zhaoy\.claude\projects\D--agent-claude-github-create\memory\tower-guard-project.md`）：
  - 圣卫的脸跟原版卫道士一致；
  - 无名者杖头是方块套方块；
  - 利维坦杖头的青色发光；
  - 亚巴顿的手是垂挂的。
  
  原件与这些冲突时，先列出来让用户选，不要自己决定。
- **材质：** 不依赖自定义 core shader。用户开着 Iris 加 Complementary 光影，光影会替换掉 core shader：二阶段用了标记色加自定义着色器，结果只剩外形、满身黑块。所以一律用普通贴图，发光部位用 `light_emission`。
- **缩放：** 和现在的游戏内身高一致，除非用户另行确认。

**顺序：** 每个怪单独做、单独验收，不要一次全换。

1. 教皇、末影之心、灾厄面容（Boss 战的观感收益最大）
2. 别西卜、利维坦、亚巴顿
3. 三种罪仆和圣卫

## 4. 通用规格

- **转换：** 方块还原、UV 从网格换算、骨骼 pivot 取自原骨架、动画换算成绝对欧拉角减去 rest 并做展开，都照你做路西法二阶段时的方法。
- **数值验证：** 每段动作在烘焙的每一刻，比较原动画与 `posed_matrix`，报告最大误差。
- **对照图：** 四视角，原网格与转换结果并排，同一相机。
- **原始导出：** 放在 `D:\agent\dungeons_extract\` 下，不进仓库。仓库里只放最终用到的贴图、音效和中间数据。
- **来源：** `SOURCES.md` 每个文件写一行：pak 内路径、字节数、sha256 前 16 位。版权归 Mojang，本项目非商业，与 Mojang 无关联。

## 5. 不要做的事

- **玩法：** 不改战斗逻辑、技能数值和时序：`add_lucifer_fight.py`、`add_lucifer_boss.py`、`add_pope_fight.py`、驱魔系统和罪仆的玩法生成器。要接新特效或新模型的地方，在报告里列出调用接口，由用户转给负责玩法的会话。
- **`display_mob.py`：** 不改。必须改时要向后兼容，并证明现有怪的生成结果逐字节不变。
- **git：** 没有用户明确要求，不提交、不推送、不切分支。
- **共用工作区：** 只碰自己的路径，不回滚、不格式化别人的改动。
- **PCL 实例：** 同步前先问用户。

## 6. 检查点

**检查点 A：盘点（先做这个，然后停下）**

两批合起来交一张表，每一项写明：

- 本体里找到的确切路径，网格、骨架、动作、贴图、粒子系统都要
- 部件数估计
- 原作动作与现有 clip 的对应关系
- 和用户已确认外观的冲突
- 预计观感收益

用户据此选做哪几项。

**检查点 B：** 第一批完成。

**检查点 C 及以后：** 第二批每完成一个怪停一次。每次交：对照图、动作误差表、部件表、接口对照（clip、时长、出手帧、挂点前后对比）。

## 7. 验证

- `_tools/build.sh`、`_tools/rp_build.sh` 无报错，`_tools/rp_validate.py` 无问题
- `_tools/server_test.py` 无函数加载错误
- 换装、卸装、死亡和清场后没有残留的展示实体
- 能进游戏就截图；进不了就明确写「未在真实游戏内看过」

## 8. 汇报

如实写明没做的、没验证的、推断的。从本体提取的叫「提取」，自己补的叫「补做」。
