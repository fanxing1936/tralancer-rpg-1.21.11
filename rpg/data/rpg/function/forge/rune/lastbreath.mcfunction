execute store result score #hp rpg_fg run data get entity @s Health
execute if score #hp rpg_fg matches 4.. run return 0
effect give @s minecraft:resistance 2 4 true
effect give @s minecraft:regeneration 3 1 true
scoreboard players set @s rpg_fg_lb 2400
particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.6 0.4 0.4 30
playsound minecraft:item.totem.use player @a[distance=..16] ~ ~ ~ 0.6 1.4
tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　［余生］护住了你，120 秒后才能再次生效","color":"#FFD85A","italic":false}]
