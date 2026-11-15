# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/7_4
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m34
# 复利 —— 每一息都在增长的账，最后从经验与血里一起扣。
playsound minecraft:block.vault.reject_rewarded_player hostile @a[distance=..32] ~ ~ ~ 1 0.7
particle wax_on ~ ~1 ~ 4 1 4 0.12 80
particle trial_omen ~ ~1 ~ 3 1 3 0.08 64
execute as @e[tag=rpg.unit.f,distance=..10] run function rpg:taint/sk7d_interest
# 玛门外观（add_mammon_model.py）
execute if entity @s[tag=rpg.mml] run function rpg:mammon_lord/skill/sk7_4
