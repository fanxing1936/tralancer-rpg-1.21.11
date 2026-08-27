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
python add_squad.py ../rpg
# 玛门：七宗罪的最后一件罪器（弓）。要在 add_pact 之后 —— 税与买断都认柱位
python add_mammon.py ../rpg ../resourcepack
# 把包里原有的三件驱魔道具（替死人偶／圣水／天启星）接进驱魔体系
python add_holy_items.py ../rpg
python retype_longinus.py ../resourcepack ../rpg
# 如意金箍棒同样迁到原生下界合金枪，并保留独立 GUI／手持模型。
python retype_wukong.py ../resourcepack ../rpg
# 更新前旧武器的首批现代化：统一命中入口、玩家独立状态与 HUD 反馈。
# 必须早于 opt_actionbar，让新增提示也进入唯一 actionbar 出口。
python modernize_legacy_weapons.py ../rpg
# 高复杂度旧武器：随机连段、教条战斧纹饰与 flame/sweep/wind 镶嵌。
# 紧随首批迁移，避免两份生成器互相覆盖；仍早于统一 actionbar 收编。
python modernize_legacy_advanced.py ../rpg
# 游戏内的玩法总览书。数值读 _squad.json / _pact.json，与图鉴同源
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
# 玩家面板最后汇总驱魔档案、真名调查、契约、佣兵与个人 HUD 控制。
# 必须在驱魔扩展之后，才能读取完整目标与状态机。
python add_player_panel.py ../rpg
# 统一近期驱魔、仪式与面板的分隔线、层级、配色和非斜体文本规范。
python polish_recent_ui.py ../rpg
# 十源质先授旧约；真·十字架置于 Daath 后汇聚成新约，并接入上位契约状态与纹理。
# 必须晚于面板/UI 生成器，确保权柄完整度是最终 HUD 语义。
python add_divine_covenants.py ../rpg ../resourcepack
# 世界观第一章：空缺者事件、所罗门罪仆、别西卜 700 生命 Boss、
# 真名调查、完整四阶段驱魔、裁决逃脱与边缘者入院尾声。
# 必须晚于上位契约和玩家面板，才能复用最终接口并追加章节入口；
# 又必须早于领取箱，让四种裁决残响与边缘者档案自动进入分类。
python beelzebub_campaign_config.py
python add_beelzebub_campaign.py ../rpg
# 专属美术/UI规整层：章节色板、动态 Bossbar、关键 Title、Display 可读性、
# 裁决档案与双层 HUD 兼容。必须在章节生成后运行。
python polish_beelzebub_campaign_ui.py ../rpg ../resourcepack
# 独立无尽副本：完整 72 柱与 72 套编队、每五层七罪领主、三路线个人奖励。
# 晚于章节与玩家面板，才能建立互斥入口并追加面板按钮。
python add_endless_exorcism.py ../rpg
# 保底仪式物资与规范遗珍，随后接入付费祷告和持久待领记录。
python add_endless_supplies.py ../rpg
python add_prayer.py ../rpg
python add_drop_policy.py ../rpg
# 全量领取箱必须在所有 give 生成器之后运行，才能收齐驱魔工具、真名残页
# 与裁决奖励，并将旧目录中的物品按语义重新分类。
python make_boxes.py ../rpg
# 所有生成器（尤其领取箱）完成后再统一七罪姓名色与物品名字重：这样箱内
# 副本、散装 give、Boss 名牌、调查/裁决/面板会共享同一套最终规范。
python polish_demon_names.py ../rpg
# 两道门必须晚于领取箱生成，避免自然接引物被静默收进开局物资而绕开首次事件。
python add_entry_points.py ../rpg
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
python check_beelzebub_campaign.py ../rpg
python check_beelzebub_campaign_ui.py ../rpg ../resourcepack
python check_beelzebub_campaign_config.py ../rpg --require-wired
python check_beelzebub_narrative_ui.py ../rpg --story-contract
python check_endless_exorcism.py ../rpg
python check_entry_points.py ../rpg
python check_prayer_supplies.py ../rpg
python check_drop_policy.py ../rpg
python check_retired_mob_content.py ../rpg
# 攻击瞬爆不得回流成苦力怕或 fuse:0 TNT（后者会破坏地形）
python check_creeper.py ../rpg
echo
echo "== 4. per-tick profile =="
python profile_tick.py ../rpg
