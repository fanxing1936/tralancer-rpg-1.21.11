scoreboard players set #clock rpg_mn_tick 0
scoreboard players set #casts rpg_mn_tick 0
execute as @e[tag=rpg.demon.minion] at @s run function rpg:minion/entity_tick
execute as @e[type=minecraft:vex] at @s run function rpg:minion/role/vex_tick
