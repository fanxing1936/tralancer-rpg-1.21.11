# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/4_2
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m17
# 吞噬 —— 他吃的是你那一顿。
playsound minecraft:entity.generic.eat hostile @a[distance=..32] ~ ~ ~ 1 0.6
playsound minecraft:entity.player.burp hostile @a[distance=..24] ~ ~ ~ 1 0.7
particle item_slime ~ ~1 ~ 2 1 2 0.2 60
execute as @a[distance=..7,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk4b_devour
