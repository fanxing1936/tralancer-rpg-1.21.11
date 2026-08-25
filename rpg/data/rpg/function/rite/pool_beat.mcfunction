scoreboard players set @s rpg_rite 0
particle end_rod ~ ~0.2 ~ 2.0 0.1 2.0 0.02 24
particle dust{color:[1.0,0.98,0.86],scale:1} ~ ~0.2 ~ 2.0 0.1 2.0 0.01 16
execute as @a[distance=..4] run scoreboard players remove @s rpg_taint 1
execute if entity @s[tag=rpg.holy_water.strong] as @a[distance=..4] run scoreboard players remove @s rpg_taint 1
execute as @a[distance=..4,scores={rpg_taint=..-1}] run scoreboard players set @s rpg_taint 0
execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..4] at @s run function rpg:vacant/scald
