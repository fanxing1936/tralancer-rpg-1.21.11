#!/bin/sh
# Rebuild the upgraded pack from the pristine 1.21 copy in _orig/.
set -e
cd "$(dirname "$0")"

# 让 _tools/sitecustomize.py 被 Python 启动时自动导入。
# 它给所有生成器的**写**操作套了一层有上限的重试 —— 这台机器上
# 实时扫描会让刚复制出来的文件随机返回 Errno 22，每次挂在不同的生成器。
# 详见该文件顶部的排查记录。
export PYTHONPATH="$(pwd)${PYTHONPATH:+:$PYTHONPATH}"
rm -rf ../rpg
cp -r ../_orig ../rpg
# 复制完两千来个文件之后要缓一下再动手。
#
# 实测：在这台机器上 `cp -r` 返回时，Windows 还没把新建文件的句柄放干净
# （实时扫描在后面追），紧接着的第一个写操作会随机撞上
# `OSError: [Errno 22] Invalid argument` —— 每次挂在不同的文件，
# 看起来像"构建不确定"，其实是复制还没落稳。
# 停一下比事后重试便宜，也比误判成生成器有 bug 省事。
sleep 5
echo "== 1. version migration 1.21 -> 1.21.11 =="
python migrate.py   ../rpg
echo
echo "== 2. tick-path optimisation =="
python optimize.py  ../rpg
python opt_spawn.py ../rpg
# 变种召唤的滚雪球：召出来的变种没打已处理标记，下一刻又被重掷一遍
python opt_cascade.py ../rpg
python opt_misc.py  ../rpg
# 苦力怕的变种体系整段摘掉（作者决定）——苦力怕就是原版苦力怕
python drop_creeper_variants.py ../rpg
# 同步退役僵尸/骷髅变种、风袭掠夺者、溺尸军团和猪灵军团；
# 放在生成优化之后，确保原始整段扫描与优化后的 batch 入口一并摘除。
python drop_legacy_mob_factions.py ../rpg
# 攻击瞬爆改成粒子、声音与分段伤害：同刻结算，但不生成 TNT、不破坏地形
python instant_boom.py ../rpg
python add_items.py ../resourcepack ../rpg
python add_skills.py ../rpg
python add_twins.py  ../resourcepack ../rpg
python add_lucifer.py ../resourcepack ../rpg
python add_leviathan.py ../resourcepack ../rpg
python add_runes.py ../rpg ../resourcepack
python add_epics.py ../resourcepack ../rpg
python add_exorcism.py ../rpg ../resourcepack
python add_pact.py ../rpg ../resourcepack
python build_combat_prompt_font.py ../resourcepack
# 玛门：七宗罪的最后一件罪器（弓）。要在 add_pact 之后 —— 税与买断都认柱位
python add_mammon.py ../rpg ../resourcepack
# 把包里原有的三件驱魔道具（替死人偶／圣水／天启星）接进驱魔体系
python add_holy_items.py ../rpg
python retype_longinus.py ../resourcepack ../rpg
# 如意金箍棒同样迁到原生下界合金枪，并保留独立 GUI／手持模型。
python retype_wukong.py ../resourcepack ../rpg
# 米迦勒脊骨／肋骨：[神圣] 双持圣骸。要在 add_twins 之后（借它的副手索引块），
# 早于 opt_index、make_boxes、polish_ui 与 polish_vfx。
python add_michael.py ../resourcepack ../rpg
# Minecraft Dungeons 原作武器：坟墓克星、竖琴弩（[传说]，圣殿大团长雅克的武器）。
# 同米迦勒：早于 opt_index、make_boxes、polish_ui 与 polish_vfx。
python add_dungeons_weapons.py ../resourcepack ../rpg
# 更新前旧武器的首批现代化：统一命中入口、玩家独立状态与 HUD 反馈。
# 必须早于 opt_actionbar，让新增提示也进入唯一 actionbar 出口。
python modernize_legacy_weapons.py ../rpg
# 高复杂度旧武器：随机连段、教条战斧纹饰与 flame/sweep/wind 镶嵌。
# 紧随首批迁移，避免两份生成器互相覆盖；仍早于统一 actionbar 收编。
python modernize_legacy_advanced.py ../rpg
# 游戏内的玩法总览书。数值读 _pact.json，与图鉴同源
python add_book.py ../rpg
# 把所有直接写 actionbar 的地方收回统一 HUD（它只有一行，谁最后写谁赢）
python opt_actionbar.py ../rpg
# 上面这些生成器同样会往 ../resourcepack 写手持变换，而它们写的是作者
# 原本的非等比缩放。rp_build.sh 末尾跑 fix_display 就是为了这个 ——
# 这里不跑，单独重建数据包就会把刀刃的剪切和副手反握又装回去。
python fix_display.py ../resourcepack
# 作者原图裁成图标该有的尺寸（弓的四阶段共用一个裁剪框）
python import_art.py "F:/筑梦 MCBE/新建文件夹" ../resourcepack
# 还没画好的贴图先拿原版的逐字节顶上 —— 已存在的文件一律不碰
python art_placeholder.py ../resourcepack
echo
echo "== 2b. guard the empty-tag entity walks =="
# 多人适配：单人下看不出来的归属错、全局标签互踩，以及按人数放大的遍历
python opt_mp.py ../rpg
python opt_index.py ../rpg
# 「圣器在身」：主手、副手、四个护甲槽任一满足（必须在 opt_index 之后）
python opt_holy.py ../rpg
python opt_type.py ../rpg
python opt_guard.py ../rpg
# 把与 @s 无关的存在性判定从 as @e 循环里提出来（O(n²) -> O(n)）
python opt_hoist.py ../rpg
python opt_invert.py ../rpg
# Boss 战与全域真实热路径：必须在 guard/invert 生成 g0..g4 后收尾。
python opt_runtime_hotpaths.py ../rpg
# 七柱真名调查与四阶段驱魔必须在热路径收尾后接入：这样既能复用最终的
# advent_tick / rite/beat 结构，也不会被后续优化脚本重新覆盖。
python add_true_name_rite.py ../rpg
# 在真名与四阶段基础上接入反仪式、分支裁决、职业成长与圣物工具。
# 必须最后运行，避免前面的生成器覆盖法阵状态机。
python add_exorcism_expansion.py ../rpg
# 压制后的 Boss 二阶段：稳定度争夺、压场开幕与仪式器物右键布置。
python add_ritual_phase2.py ../rpg
# 七罪普通罪仆：灾厄村民模型、每柱独立支援技、召唤上限、寿命与掉落生态。
# 必须晚于二阶段生成器，才能挂接最终 advent/exorcism 热路径。
python add_demon_minions.py ../rpg
# 参考图比例的贴地生命之树：十一圆、二十二路径、十刻粒子刷新。
# 晚于驱魔热路径生成，确保锚点守卫不会被前序脚本覆盖。
python add_life_tree_particles.py ../rpg
# 花朵盾徽血契展开法阵，十色染料归位十源质；奖励由后续上位契约阶段接管。
python add_kabbalah_covenant.py ../rpg
# 玩家面板最后汇总驱魔档案、真名调查、契约与个人 HUD 控制。
# 必须在驱魔扩展之后，才能读取完整目标与状态机。
python add_player_panel.py ../rpg
# 统一近期驱魔、仪式与面板的分隔线、层级、配色和非斜体文本规范。
python polish_recent_ui.py ../rpg
# 十源质先授旧约；真·十字架置于 Daath 后汇聚成新约，并接入上位契约状态与纹理。
# 必须晚于面板/UI 生成器，确保权柄完整度是最终 HUD 语义。
python add_divine_covenants.py ../rpg ../resourcepack
# 契约的深契、戒律、柱页与柱印：要接管上面写好的模型表、面板和 HUD。
python add_pact_depth.py ../rpg ../resourcepack
# 物品贴图按原生网格存储（最后一个写物品贴图的生成器之后）：整数倍放大
# 的无损还原，新约按 ART-STYLE D6 重建；单独重建数据包也要收回来
python fix_texture_grid.py ../resourcepack
python add_forge.py ../resourcepack ../rpg
# 世界怪物掉落表 + 禁用原版合成（add_world_loot.py）：必须在 add_drop_policy 之前
python add_world_loot.py ../rpg
python add_drop_policy.py ../rpg
# 批量护甲与套装加成：要在 add_demon_minions 之后（往罪仆掉落表里追加），
# 早于 make_boxes 与 polish_ui；也晚于全部 opt_*，套装检测不会被改写。
python add_armor_sets.py ../rpg
# 全量领取箱必须在所有 give 生成器之后运行，才能收齐驱魔工具、真名残页
# 与裁决奖励，并将旧目录中的物品按语义重新分类。
python add_alchemy.py ../rpg --items
python make_boxes.py ../rpg
# 所有生成器（尤其领取箱）完成后再统一七罪姓名色与物品名字重：这样箱内
# 副本、散装 give、Boss 名牌、调查/裁决/面板会共享同一套最终规范。
python polish_ui.py ../rpg
# 圣卫（塔卫，展示实体生物）：只写 rpg:tower_guard/ 与 #minecraft:tick 一条入口，
# 放在所有选择器优化之后，免得被改写；仍早于封印遗物这一最终层。
python add_tower_guard.py ../resourcepack ../rpg
# 圣卫的另外两种：重盾（原作皇家卫兵）、术士（原作终末灾厄村民，唤魔者网格褐袍）；rpg:holy_guard/summon 三选一
python add_holy_guards.py ../resourcepack ../rpg
# 别西卜换上无名者模型：只加外观与音效，挂进 sk4_*、ult4*、advent_gone 末尾，
# 不动标签、血量与招式；共用 display_mob.py 管线。
python add_beelzebub.py ../resourcepack ../rpg
# 别西卜麾下五名罪仆换上 Dungeons 先锋外观（塞列欧斯改用掠夺者底子，见 add_demon_minions.py）
python add_vanguard.py ../resourcepack ../rpg
# 利维坦换上 Dungeons 死灵法师模型（挂进 sk2_*、ult2*、advent_gone），
# 麾下五名罪仆换上沉没骷髅外观（派蒙改用掠夺者底子）
python add_leviathan_model.py ../resourcepack ../rpg
# 玛门（第七柱）外观：猪灵商人，原作模型（mammon_lord_dungeons_ref/）
python add_mammon_model.py ../resourcepack ../rpg
# 萨麦尔（第五柱）：红石巨怪；贝利尔（第六柱）：腐化坩埚；三位领主的罪仆（共用 lord_look.py / servant_look.py）
python add_samael_model.py ../resourcepack ../rpg
python add_belial_model.py ../resourcepack ../rpg
python add_lord_servants.py ../resourcepack ../rpg
# 篡夺者一阶段外观：附魔师（usurper_dungeons_ref/）
python add_usurper_model.py ../resourcepack ../rpg
# 圣殿大团长雅克：原作玩家英雄网格 + 赫克斯皮肤 + 英雄铠甲，坟墓克星与竖琴弩（jacques_dungeons_ref/）
python add_jacques_model.py ../resourcepack ../rpg
# 疯人王扫罗：原作玩家英雄网格 + 织网者皮肤 + 坚毅铠甲，千刀（saul_dungeons_ref/、saul_ghost_dungeons_ref/）
python add_saul_model.py ../resourcepack ../rpg
# 米迦勒灵体：原版 Cloudwatcher、霜冻护甲和双持武器及动作。
python add_michael_spirit_model.py ../resourcepack ../rpg
# 天使长米迦勒：半透明灵体 + 六翼（michael_dungeons_ref/，build_michael_model.py）；守望者（watchling_dungeons_ref/）
python add_michael_model.py ../resourcepack ../rpg
# 篡夺者战的特效素材：原作附魔台符文、灵魂图腾法阵、六芒星、唤魔者尖牙（usurper_fx_ref/）
python add_usurper_fx_art.py ../resourcepack
python add_lucifer_model.py ../resourcepack ../rpg --defer-shaders
python add_lucifer_p2_model.py ../resourcepack ../rpg
# 原作 Abomination Vine：缠枝破土的藤蔓（dungeons_conversion/generic.py 转换）
python add_lucifer_vine_model.py ../resourcepack ../rpg
python add_lucifer_model.py ../resourcepack ../rpg --finalize-shaders
python add_sunken_skeleton.py ../resourcepack ../rpg
python add_abaddon_model.py ../resourcepack ../rpg
python add_tower_wraith.py ../resourcepack ../rpg
python add_pope_model.py ../resourcepack ../rpg
python add_prime_enchanter_model.py ../resourcepack ../rpg
# 篡夺者二阶段外观：首席附魔师的冰电改篡夺白金，帽顶加原作王冠（须在上面两步之后）
python add_usurper_holy_look.py ../resourcepack
# 末影之心与灾厄面容：仅调试模型/动作，不绑定现有怪物或接入战斗逻辑。
python add_heart_of_ender.py ../resourcepack ../rpg
python add_arch_visage.py ../resourcepack ../rpg
# 教皇战特效贴图：母图在 pope_fx_ref/raw/（Codex 绘制），这里定网格和色板
python add_pope_fx_art.py ../resourcepack
# 路西法二阶段特效贴图：母图在 lucifer_p2_fx_ref/（Codex 绘制），这里定网格和色板
python add_lucifer_p2_fx_art.py ../resourcepack
# 原作静态道具：毒刺弹、藤臂尖根
python add_lucifer_props.py ../resourcepack
# 最终 Boss 路西法的位图血条：饰物与标题在 lucifer_boss_ref/bar/（Codex 绘制）
python add_lucifer_boss_art.py ../resourcepack
# 篡夺者的位图血条：饰物与标题在 usurper_boss_ref/bar/（占位，正式稿见 BAR-BRIEF.md）
python add_usurper_boss_art.py ../resourcepack
# 雅克的位图血条：饰物与标题在 jacques_boss_ref/bar/（占位：原作图标与哥特字体）
python add_jacques_boss_art.py ../resourcepack
# 扫罗的位图血条：饰物与标题在 saul_boss_ref/bar/（占位：原作图标与哥特字体）
python add_saul_boss_art.py ../resourcepack
# 米迦勒的位图血条、羽毛与骨头的物品模型（占位在 michael_boss_ref/bar/）
# 米迦勒专属特效贴图：原作素材 + Codex 序列帧（michael_fx_ref/），字体 rpg:michael_vfx
python add_michael_fx_art.py ../resourcepack
python add_michael_boss_art.py ../resourcepack
python add_boss_bgm.py ../resourcepack
# 教皇战（docs/POPE-DESIGN.md）：调用各模型的函数，放在所有模型之后。
python add_pope_fight.py ../rpg
# 路西法二阶段「知善恶树」的变身与招式（docs/LUCIFER-P2-DESIGN.md）；要在两阶段外观、
# 驱魔与罪仆生成器之后，挂接最终的 advent_tick 与 sk1/ult1。
python add_lucifer_fight.py ../rpg
# 最终 Boss 路西法（docs/LUCIFER-BOSS-DESIGN.md）：复用上面的招式时间线，要在它之后
python add_lucifer_boss.py ../rpg
# 篡夺者（达里奥·所罗门）Boss：docs/USURPER-DESIGN.md
python add_usurper_boss.py ../rpg
# 圣殿大团长雅克 Boss：docs/JACQUES-DESIGN.md
python add_jacques_boss.py ../rpg
# 友军雅克：圣殿誓约召他并肩作战 20 秒（docs/JACQUES-ALLY.md）
python add_jacques_ally.py ../rpg ../resourcepack
# 疯人王扫罗 Boss：docs/SAUL-DESIGN.md
python add_saul_boss.py ../rpg
# 天使长米迦勒 Boss（docs/MICHAEL-DESIGN.md）
python add_michael_boss.py ../rpg
# 《破碎大陆》序章（Claude Docs 方案书 / 脚本书）：维度与群系、大厅选角、三波、五段过场、双语字幕。
# 要在米迦勒 Boss 之后：序章模式挂在它的血线钩子 #rpg:michael_boss/prologue_hp 上；台词来自 prologue_ref/lines.json
python add_prologue_models.py ../resourcepack ../rpg
python add_prologue.py ../resourcepack ../rpg
# Final ownership layer: deterministic sealed-relic agitation, ordered active
# slots, abilities and the persistent two-layer HUD.  Nothing gameplay/UI may
# overwrite these products after this point.
python add_seal_relic.py ../rpg
# 封印遗物层写的播报行（[遗物休眠]、[利维坦・反制] 等）补上〖〗暗色样式（ART-STYLE §12）。
python polish_ui.py ../rpg --broadcasts
# 玩家面板换成对话框：要在所有写面板的生成器和文字规范化之后。
# 第二个参数：顺带把游戏内菜单底换成深色（inworld_menu_background.png）。
python add_panel_dialog.py ../rpg ../resourcepack
# 特效收口（docs/VFX-SPEC.md）：force 只留给预警和大招，数量／速度／尺寸收进各档上限，
# 旧柱色闪光折回亮色。放在最后，前面所有生成器（含封印遗物层）写的粒子都经过这一道。
python polish_vfx.py ../rpg
# 友军单位接入：敌方技能里选玩家的 @a/@p/@r 也算上友军，玩家的范围技能避开友军。
# 要在所有生成器与收口之后（它改写的是最终产物）。
python add_ally_units.py ../rpg
python add_forge.py ../resourcepack ../rpg --late
# 新手开局：序章 → 黑屏欢迎与起名 → 抽身份 → 锻造教学。要在序章、锻造、面板、HUD 都生成完之后（它往这些产物里接钩子）。
python add_onboard.py ../rpg ../resourcepack
# 原质等级、力条与生命力：在新手开局之后接钩子（add_sephira.py，方案书第三版）
python add_sephira.py ../rpg
# 力与技能：圣徽 / 罪印、技能页、两棵技能树（add_force.py，接在原质之后）
python add_force.py ../rpg ../resourcepack
# 精英怪（add_elites.py）：要在 add_force 之后（往 rpg:force/hit 里接圣印词缀）
python add_elites.py ../rpg
# 罪器锻造与材料转换（add_forge_world.py）：锻造对话框按钮 50..69；往罪仆掉落表里加罪印碎片
python add_forge_world.py ../rpg
# 图纸、特殊材料、卡巴拉物品与契约书的来源（add_world_items.py）
python add_world_items.py ../rpg
# 随机事件、每日悬赏与面板「旅程」页（add_events.py）
python add_events.py ../rpg
# 小支线、彩蛋与称号（add_quests.py）：接在事件之后（往旅程页和各系统里挂钩子）
python add_quests.py ../rpg
# 黑石堡垒（Antigravity，docs/FORTRESS-PROMPT.md；交付前跳过）
if [ -f add_blackstone_fortress.py ]; then python add_blackstone_fortress.py ../rpg; fi
# 失乐园：维度、自由猎杀、河庭试炼、宝库（add_paradise.py）
python add_eden_gate.py ../rpg
python add_paradise.py ../rpg ../resourcepack
# 失乐园与主世界的背景音乐（读 add_paradise 的分区与河庭）
python add_world_bgm.py ../rpg
# 商人（add_merchants.py）：铁匠/神秘/奢侈品/迷途商人，接在支线之后（挂事件 6、玛门的账本、金锄彩蛋）
# 药水、炼药与制器（add_alchemy.py）：商人要卖它的东西，所以在商人之前
python add_alchemy.py ../rpg
python add_merchants.py ../rpg
# 商人外观（Codex：地下城 SK_Villager + 四套商人材质/帽子，idle/look/bow/examine）
python add_merchant_models.py ../resourcepack ../rpg
# 领取箱补齐（add_give_boxes.py）：make_boxes 之后才有的材料、图纸、圣徽与传承书；接在所有生成物品的步骤之后
python add_give_boxes.py ../rpg
# 世界掉落与锻造的新图标（Codex 交付，world_ref/art）
python add_world_art.py ../resourcepack
python add_elite_bar_art.py ../resourcepack
# 药水、驱魔器具、残页、罪物、传承书、钥匙的图标（Codex：relic_ref/art，没到先用原版图）
python add_relic_art.py ../resourcepack
echo
echo "== 3. validation =="
python validate.py  ../rpg
# 拿原版当字典，比对进度触发器的条件字段名（写错是完全静默的）
python check_adv.py ../rpg
python check_ritual_phase2.py ../rpg
python check_demon_minions.py ../rpg
python check_life_tree_particles.py ../rpg
python check_kabbalah_covenant.py ../rpg
python check_divine_covenants.py ../rpg ../resourcepack
python check_seal_relic.py ../rpg
python check_drop_policy.py ../rpg
python check_retired_mob_content.py ../rpg
# 攻击瞬爆不得回流成苦力怕或 fuse:0 TNT（后者会破坏地形）
python check_creeper.py ../rpg
# effect give 的时长只收整数秒；带 t 后缀会让整份函数拒绝加载，validate 抓不到
python check_effect_duration.py ../rpg
# 色板自检（对比度、同族色差）＋产物里不得残留七柱旧色写字；生成器里
# 未登记的 Hex 先只警告（ART-STYLE.md §1.6）
python check_ui_palette.py ../rpg
# 特效分级预算：超档、滥用 force、每刻常驻超预算、深色闪光都会让构建失败
python check_vfx_budget.py ../rpg
echo
echo "== 4. per-tick profile =="
python profile_tick.py ../rpg
