scoreboard players add @s rpg_mer_hoe 1
playsound minecraft:entity.villager.no neutral @a[distance=..16] ~ ~ ~ 1 1
execute if score @s rpg_mer_hoe matches 3.. run function rpg:merchant/hoe_done
