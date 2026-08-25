# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/7_4
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m34
# 复利 —— 每一息都在增长的账，最后从经验与血里一起扣。
playsound minecraft:block.vault.reject_rewarded_player hostile @a[distance=..32] ~ ~ ~ 1 0.7
particle wax_on ~ ~1 ~ 4 1 4 0.12 92
particle trial_omen ~ ~1 ~ 3 1 3 0.08 64
execute as @a[distance=..10,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk7d_interest
