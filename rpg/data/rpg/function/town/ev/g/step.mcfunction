execute if score #ph rpg_te matches 2 if score #totem rpg_te matches 1 as @e[type=minecraft:marker,tag=rpg.te.cm] at @s if entity @e[type=minecraft:area_effect_cloud,tag=rpg.holy_water,distance=..5] run function rpg:town/ev/g/lit
execute if score #ph rpg_te matches 3 run function rpg:town/ev/g/hold
execute if score #ph rpg_te matches 4 run function rpg:town/ev/g/kneel_wait
