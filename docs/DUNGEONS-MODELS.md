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

## 没换的

- **末影之心、虚空之颜（Arch-Visage）**：原作的星空是屏幕空间材质（`T_ArchIllagerAvatarSpace`）。直接转换只剩黑色外形，所以保留现有版本。
- **教皇特效**：原作粒子用的是通用发光材质和管道网格，没有可搬的贴图，保留现有特效。

## 已知

- 圣卫左眼虹膜在原作里是镜像骨（缩放 -1），这根骨的动作有约 1.3 px 误差。它已并进头部，跟头一起刚性运动。
- 用 `/kill` 杀掉载体后，罪仆的展示部件会残留。手工模型版同样如此，是原有行为，不是这次引入的。
