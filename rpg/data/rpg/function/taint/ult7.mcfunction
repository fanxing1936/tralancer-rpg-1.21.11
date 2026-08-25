# 黄金终审 —— 场上的财富、经验与性命在同一刻结算。
particle wax_on ~ ~1 ~ 5 1.5 5 0.16 72 normal
particle end_rod ~ ~1 ~ 4 1 4 0.08 72 normal
particle flash{color:16765754} ~ ~1 ~ 0 0 0 0 1 normal
particle firework ~ ~1 ~ 5 1.5 5 0.18 72 normal
particle totem_of_undying ~ ~1 ~ 4 1 4 0.16 72 normal
playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..36] ~ ~ ~ 1.2 0.55
playsound minecraft:entity.player.levelup hostile @a[distance=..36] ~ ~ ~ 1.1 0.45
execute at @s as @e[type=minecraft:item,distance=..12] at @s run function rpg:taint/ult7_seize
execute as @a[distance=..10,gamemode=!spectator,gamemode=!creative] run function rpg:taint/ult7_hit
