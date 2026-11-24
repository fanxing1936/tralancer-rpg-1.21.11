tp @s ~ ~ ~ ~15 0
particle minecraft:end_rod ^ ^0.1 ^4 0 0 0 0 1 force
particle minecraft:end_rod ^ ^0.1 ^-4 0 0 0 0 1 force
particle minecraft:end_rod ^4 ^0.1 ^ 0 0 0 0 1 force
particle minecraft:end_rod ^-4 ^0.1 ^ 0 0 0 0 1 force
particle minecraft:wax_on ~ ~1.5 ~ 2.5 1 2.5 0 2
execute unless score #zt rpg_fo matches 0 run return 0
execute if score #lv rpg_fo matches ..2 run effect give @a[distance=..4,gamemode=!spectator] minecraft:resistance 1 0 true
execute if score #lv rpg_fo matches 3 run effect give @a[distance=..4,gamemode=!spectator] minecraft:resistance 1 1 true
execute if score #lv rpg_fo matches 2.. run effect give @a[distance=..4,gamemode=!spectator] minecraft:regeneration 2 0 true
