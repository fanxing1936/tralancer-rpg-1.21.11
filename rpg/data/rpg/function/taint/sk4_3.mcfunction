# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/4_3
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m18
# 蝇群 —— 苍蝇王名副其实。
playsound minecraft:entity.bee.loop_aggressive hostile @a[distance=..32] ~ ~ ~ 1 0.5
particle mycelium ~ ~1 ~ 2 1 2 0.3 80
execute at @s run function rpg:taint/sk4c_swarm
