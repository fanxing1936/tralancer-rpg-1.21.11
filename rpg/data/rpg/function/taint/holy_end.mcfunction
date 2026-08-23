# 圣痕淡去，人落回凡人。
scoreboard players set @s rpg_holy 0
effect clear @s minecraft:strength
effect clear @s minecraft:resistance
effect clear @s minecraft:regeneration
effect clear @s minecraft:fire_resistance
effect clear @s minecraft:absorption
particle end_rod ~ ~1 ~ 0.4 0.7 0.4 0.06 40
playsound minecraft:block.beacon.deactivate master @s ~ ~ ~ 0.8 1.2
function rpg:hud/m32
