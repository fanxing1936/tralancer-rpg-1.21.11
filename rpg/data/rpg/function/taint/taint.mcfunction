# 魔化：握着魔器慢慢沾染，握着圣器慢慢洗去。
# 每 40 刻结算一次 —— 逐刻结算既没必要也白费开销。
scoreboard players add @s rpg_taint_t 1
execute if entity @s[scores={rpg_taint_t=40..}] run function rpg:taint/step
