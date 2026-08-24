# 溺没 —— 深海的规矩：在这儿，你不会呼吸。
playsound minecraft:entity.drowned.ambient_water hostile @a[distance=..32] ~ ~ ~ 1 0.5
particle bubble ~ ~1 ~ 3 1.2 3 0.2 120
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk2b_drown
