execute store result score #h rpg_alc run data get entity @s Health
execute unless score #h rpg_alc matches ..5 run return 0
scoreboard players set @s rpg_po_ud 0
effect give @s minecraft:resistance 3 2 true
effect give @s minecraft:regeneration 3 2 true
execute at @s run particle minecraft:soul ~ ~1 ~ 0.4 0.8 0.4 0.05 40
playsound minecraft:item.totem.use player @s ~ ~ ~ 0.6 0.6
tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　不灭：你在致命的一击里撑住了。","color":"gray","bold":false,"italic":false}]
