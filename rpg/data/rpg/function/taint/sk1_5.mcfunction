# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/1_5
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m5
# 王座回绝 —— 靠得太近的人会被王座本身拒斥。
playsound minecraft:block.beacon.deactivate hostile @a[distance=..32] ~ ~ ~ 1 0.55
particle end_rod ~ ~1.5 ~ 2.5 1.2 2.5 0.08 72
particle enchanted_hit ~ ~1 ~ 3 1 3 0.15 64
execute as @a[distance=..6,gamemode=!spectator,gamemode=!creative] at @s run function rpg:taint/sk1e_reject
