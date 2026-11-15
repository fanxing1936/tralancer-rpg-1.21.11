# 来源

从《Minecraft Dungeons》本体提取（只读），经 `_tools/dungeons_conversion/generic.py` 转换。

- 网格：`Dungeons/Content/Actors/Characters/Enemies/Illagers/Evoker/SK_IllagerEvoker`
- 动作：`IllagerEvoker_Idle`→idle、`IllagerEvoker_Walk`→walk、`IllagerEvoker_BasicAttack`→cast、`IllagerEvoker_StrongAttack`→strong、`IllagerEvoker_Summoning`→summon、`IllagerEvoker_NoveltyAnimation`→rise、`IllagerEvoker_GetHitFront`→hurt、`IllagerEvoker_Stun`→stun

版权归 Mojang 所有；本项目非商业，与 Mojang 无关联。

## 贴图

终末灾厄村民（End Illager）在原作里只出现在回响虚空结尾的预渲染动画（`Movies/DLC6/End_C2_Stronghold_Outro`），本体没有它的模型或贴图（2026-11-14 扫过全部 354 张角色贴图）。开发者说它像唤魔者，所以网格和动作用原作唤魔者 `SK_IllagerEvoker`；贴图是唤魔者的 `T_IllagerEvoker` 按动画改的：袍子和交叠的双臂改褐色、金边改米色、去掉兜帽层（`_tools/dungeons_overrides/make_end_illager.py` → `end_illager.png`）。
