effect give @s minecraft:instant_health 1 0 true
scoreboard players remove #lost rpg_pv_n 40
execute if score #lost rpg_pv_n matches 1.. run function rpg:pvp/heal
