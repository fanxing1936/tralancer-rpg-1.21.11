scoreboard players add @s rpg_fg_burn 1
scoreboard players set @s rpg_fg_bt 100
particle minecraft:flame ~ ~1 ~ 0.2 0.3 0.2 0.01 3
execute if score @s rpg_fg_burn matches 5.. run function rpg:forge/rune/ember_burst
