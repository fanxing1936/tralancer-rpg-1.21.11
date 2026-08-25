# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/5_5
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m25
# 怒潮 —— 暴怒从中心炸开，把所有人赶出他的呼吸。
playsound minecraft:item.mace.smash_ground_heavy hostile @a[distance=..32] ~ ~ ~ 1 0.7
particle sweep_attack ~ ~1 ~ 3 1 3 0 26
particle crit ~ ~1 ~ 4 1 4 0.22 96
particle dust{color:[0.89,0.30,0.30],scale:2.4} ~ ~1 ~ 4 1 4 0.05 72
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] at @s run function rpg:taint/sk5e_surge
