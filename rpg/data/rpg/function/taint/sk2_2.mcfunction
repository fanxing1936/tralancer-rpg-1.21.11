# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/2_2
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m7
# 溺没 —— 深海的规矩：在这儿，你不会呼吸。
playsound minecraft:entity.drowned.ambient_water hostile @a[distance=..32] ~ ~ ~ 1 0.5
particle bubble ~ ~1 ~ 3 1.2 3 0.2 120
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk2b_drown
