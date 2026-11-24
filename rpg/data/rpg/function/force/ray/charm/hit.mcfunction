tag @s add rpg.fo.hit
scoreboard players set #stop rpg_fo 1
tag @s add rpg.ally
tag @s add rpg.fo.ch
scoreboard players operation @s rpg_fo_end = #now rpg_fo
scoreboard players add @s rpg_fo_end 300
effect give @s minecraft:weakness 15 255 true
effect give @s minecraft:glowing 15 0 true
particle minecraft:heart ~ ~2 ~ 0.4 0.3 0.4 0 8
playsound minecraft:entity.allay.item_given hostile @a[distance=..16] ~ ~ ~ 1 0.6
