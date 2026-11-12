# 只有最终 Boss 路西法会变身；七罪恶魔领主路西法是常规的单阶段（用户 2026-11-09）。
execute unless entity @s[tag=rpg.lub] run return 0
# 打到 580 以下就变身；一击打穿 420、当刻进了镇压也照样变。
execute if score @s rpg_ex_stage matches 0 if score @s rpg_ex_hp matches ..580 run return run function rpg:lucifer_fight/morph/start
execute if score @s rpg_ex_stage matches 1.. run function rpg:lucifer_fight/morph/start
