tag @s add rpg.fo.hit
scoreboard players set #stop rpg_fo 1
tag @s add rpg.fo.gd
scoreboard players operation @s rpg_fo_end = #now rpg_fo
scoreboard players add @s rpg_fo_end 60
execute store result score @s rpg_fo_ai run data get entity @s NoAI
scoreboard players set #b rpg_fo 0
execute if entity @s[tag=rpg.pope] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.mkb] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.jqb] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.lub] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.slb] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.usb] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.dtb] run scoreboard players set #b rpg_fo 1
execute if score #b rpg_fo matches 0 run data merge entity @s {NoAI:1b}
execute if score #b rpg_fo matches 1 run effect give @s minecraft:slowness 3 4 true
effect give @s minecraft:glowing 3 0 true
particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~1 ~ 0.4 0.8 0.4 0 40
playsound minecraft:block.anvil.place hostile @a[distance=..16] ~ ~ ~ 0.8 1.4
