# 原作模型替换（第二批）记录

手工模型换成从《Minecraft Dungeons》本体提取的原件。所有原件版权归 Mojang 所有；本项目非商业，与 Mojang 无关联。
每个怪的来源写在 `_tools/<key>_dungeons_ref/SOURCES.md`。

## 怎么切换

- 默认用原件。
- 环境变量 `<KEY>_MODEL=legacy` 退回手工模型，例如 `POPE_MODEL=legacy`、`TOWER_GUARD_MODEL=legacy`。设好后重跑 `build.sh` 和 `rp_build.sh`。
- 战斗逻辑里依赖动作时长和出手帧的常量（`add_pope_fight.py`、`add_tower_guard.py`）也跟着这个开关走。

## 制作流程（不进构建）

- `python _tools/dungeons_models.py [key ...]`：读 `D:\agent\dungeons_extract\upgrade\` 下的导出，产物写到 `_tools/<key>_dungeons_ref/`。
  - 产物：`.bbmodel`、`parts.json`、`glow_bones.json`、`atlas.png`、`model_config.json`（动作时长、原作事件时刻）、`SOURCES.md`。
- `_tools/dungeons_variant.py` 在生成器里把怪指向这些产物。
  - 动作名不变，技能钩子照常工作。
  - 音效时刻默认按新旧动作时长等比换算；有原作事件的，在生成器里单独对准。
- `_tools/dungeons_conversion/blueprint.py` 读角色蓝图（SimpleConstructionScript），把挂在骨骼或插槽上的静态网格（头盔、盾、护甲、长矛）一并转进去。
  - 每个挂件成为一根自己的骨，名字取语义名（`shield`、`spear`…），玩法里按部件名找它的命令不用改。
- 手持物（`held`）：小怪手里显示的是载体自己的主手物品。原件版把它挂到原作的武器插槽 `J_R_Weapon` 上：
  - 待机第 0 刻按原版拿法摆好；
  - 之后跟着插槽骨运动（`display_mob.held_matrix` 的 `held_ref`）。
- 合并部件（`merge`）：眼、眉、鼻并进头部，减少实体。只合并静止变换能写进物品模型的骨，合并后它们不再单独动。

## 各怪

| 怪 | 原件 | 部件（旧→新） | 说明 |
|---|---|---|---|
| 利维坦 | SkeletonNecromancer | 13 | 杖头宝石按青色取发光（原作没有自发光图） |
| 别西卜 | NamelessKing | 10 | |
| 亚巴顿 | Wicked Wraith | 30 | 比旧版部件多 |
| 教皇 | ArchIllager | 12→15 | 杖头方块 SuperCube1 发光；按原作杖在左手 |
| 先锋罪仆 | SkeletonVanguard + BP_DesertShield | 8→12 | 盾碎的踉跄借普通骷髅的 GetHitFromTheFront |
| 沉没罪仆 | SunkenSkeleton | 7→7 | 动作借普通骷髅（Idle、Walk、BasicAttack）和先锋（近战突刺） |
| 幽魂罪仆 | TowerWraith | 7→13 | 动作借 Wraith（Idle、Walk2、BasicAttack） |
| 圣卫 | IllagerRoyalGuard + TowerGuard 蓝图挂件 | 9→15 | 头盔、护甲、护臂、护腿、长矛、盾都按蓝图挂上 |

教皇的时间常量（原件版）：

| 动作 | 原作动作 | 出手 / 结束（刻） |
|---|---|---|
| 攻击 | BasicAttackJump | 7 / 21 |
| 召唤 | SummonSingle | 22 / 42 |
| 施法 | SummonCircle | 7 / 34 |
| 瞬移离开 | TeleportIn | 第 17 刻跳 |
| 瞬移到达 | TeleportOut | 22 刻后结束 |
| 落地 | LandingFinalBoss | 20 刻 |
| 旋风 | DefeatedInawhirlwind 8.29 s | 第 160 刻碎，第 170 刻进心脏 |

- 原作的 TeleportIn / TeleportOut 命名和这里相反：TeleportIn 是消失，TeleportOut 是现身。按事件（mirror_in、mirror_out）对调过。
- 杖头挂点取出手那一刻杖头宝石的位置。

圣卫：长矛在攻击动作 0.6~0.7 s 刺到最前，命中改在第 14 刻（旧版第 16 刻）。
命中判定点仍是身前 1.6 格（`attack_hit`），原作长矛的矛尖这时伸到身前约 3 格，看起来比判定远。

手持物大小：沿用旧版（幽魂 1.15 倍、沉没 1 倍原版大小）。

## 玛门（第七柱）：猪灵商人

- 2026-11-12 用户按柱色（金橙）选定 Piglin Merchant。生成器是 `_tools/add_mammon_model.py`，key 为 `mammon_lord`。`rpg:mammon/` 已经被罪器弓占用，所以换了名字。
- 商人本身只有两段待机。行走和投掷借普通猪灵的动作：
  - 两套骨架同名骨的静止姿态一致，按骨名搬旋转（`generic.retarget_tracks`），位移用商人自己的骨长；
  - 猪灵的 J_Neck 并进商人的 J_Head；
  - 身体扭转压到 45%，否则背着货架的商人像要侧翻。
- 范围技能用自制的「聚金砸地」（`dungeons_models.py` 的 `custom_clips`）：双手举过头聚金，0.75 s 砸地。猪灵的近战是侧身大挥砍，不合适。
- 商人是友方 NPC，原作朝 +z，敌人朝 -z。显示时整体转 180°（`turn`，`display_mob.base_turn`）。
- 技能对应：
  - 什一税、收缴、利息、金狱、黄金终审蓄势 → 聚金砸地；
  - 清算 → 投掷。
- 声音暂用原版猪灵音效。原作音频导出器导不出来，要从 wiki 下载。

## 萨麦尔、贝利尔与三位领主的罪仆（2026-11-12）

用户选定：萨麦尔用红石巨怪（先给的红石傀儡被改掉），贝利尔用腐化坩埚（「那口锅」），无名者暂不做模型，并把对应的罪仆也加上。
共用的换装逻辑：领主在 `_tools/lord_look.py`，罪仆在 `_tools/servant_look.py`。

| 谁 | 原件 | 生成器 / key | 说明 |
|---|---|---|---|
| 萨麦尔（第五柱） | Redstone Monstrosity | `add_samael_model.py` / `samael_lord` | 动作全是原作的（射击、冲撞重击、砸地、熔岩重击、苏醒）；红石纹路和石头画在同一面上，没加发光；原作贴图 256×512，图集 1024² |
| 贝利尔（第六柱） | Corrupted Cauldron | `add_belial_model.py` / `belial_lord` | 见下 |
| 萨麦尔罪仆 | Mountaineer 红色变体 | `add_lord_servants.py` / `samael_servant` | 护肩、靴子按蓝图挂上，斧子不挂（手里画载体自己的武器） |
| 贝利尔罪仆 | Witch | 同上 / `belial_servant` | 和坩埚同主题、同为紫色；手里的东西画在捧药瓶的位置 |
| 玛门罪仆 | Piglin 近战变体 2 | 同上 / `mammon_servant` | 金甲红衣；猪灵朝 +z，转 180° |

贝利尔（腐化坩埚）：
- 药水材质原作就是品红紫（线性 0.48/0/0.42），只有颜色没有贴图。换成按第六柱色板画的 16×16 发光药水贴图（`_tools/dungeons_overrides/goo_belial.png`）。
- 坩埚眼睛朝 +z，转 180°。
- 原作没有行走，自制「颠步」：整口锅左右摇、每步跳起一点。
- 药水发光（用户要求）：药水面单独接一张 16×16、8 帧的动画贴图（`textures/item/belial_lord/goo.png` + `.mcmeta`），品红紫旋涡里气泡鼓起、闪白、破掉；元素全亮度（light_emission 15）。锅口不时冒发光的紫色气泡粒子。

罪仆的「咒使」原是幻术师，幻术师隐身时仍会画出本体和分身，没法换装。所以第五～七柱也和二～四柱一样改成掠夺者（`add_demon_minions.py` 的 `ROLE_OVERRIDES`，审计 `check_demon_minions.py` 同步）。

声音：原作音效，2026-11-12 经用户同意从 minecraft.wiki 下载（191 段，`_tools/dungeons_sounds/`，逐文件来源与校验在其 SOURCES.md）。个别没有对应原声的（砸地、颠步、登山者「稳住」、猪灵脚步）用原版声音事件（`display_mob` 的 sounds 支持 `{"type": "event"}`）。

## 别西卜、利维坦调整（2026-11-14，用户要求）

- **身高**：两位都调成普通骷髅大小，2 格（原来是 3.71 格）。
- **别西卜的眼睛**：原作的眼睛只画在发光贴图上，是两个蓝色像素，基础贴图上那里是暗的。转换器现在会在发光像素的位置单独贴一层全亮度的小面，颜色取发光贴图的颜色并提亮（`generic.convert`，对所有原作模型通用）。
- **整身全亮**：别西卜的发光贴图在透明处是白色，以前被当成整张发光，所有部件都是全亮度。发光识别现在会看透明度。
- **别西卜的杖头光球**：原作里光球是挂在武器插槽上的粒子（`PS_Nameless_GravityStaff`，沿杖身 100 cm），不是模型，转换时没有它。现在照用户确认过的旧版补上：三层套方块（半透明外层、白框、实心核心），斜立，绕杖身转，整颗发光。
  - 实现在 `dungeons_models.py` 的 `orb`，以及 `generic.cube_source`（合成方块挂件）。

## 没换的

- **无名者**：用户 2026-11-12 说先不做模型。
- **末影之心、虚空之颜（Arch-Visage）**：原作的星空是屏幕空间材质（`T_ArchIllagerAvatarSpace`）。直接转换只剩黑色外形，所以保留现有版本。
- **教皇特效**：原作粒子用的是通用发光材质和管道网格，没有可搬的贴图，保留现有特效。

## 已知

- 圣卫左眼虹膜在原作里是镜像骨（缩放 -1），这根骨的动作有约 1.3 px 误差。它已并进头部，跟头一起刚性运动。
- 用 `/kill` 杀掉载体后，罪仆的展示部件会残留。手工模型版同样如此，是原有行为，不是这次引入的。
