scoreboard players remove @s rpg_fg_blh 400
effect give @s minecraft:instant_health 1 0 true
execute if score @s rpg_fg_blh matches 400.. run function rpg:forge/stone/blood_heal
