# 到第 7 阶：只提示一次，进不进由玩家在原质页自己按（add_daath.py）。绝不自动传送。
execute if entity @s[tag=rpg.dt.told] run return 0
tag @s add rpg.dt.told
playsound minecraft:block.end_portal.spawn player @s ~ ~ ~ 0.4 0.6
particle minecraft:squid_ink ~ ~0.1 ~ 1 0.05 1 0.02 40
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"深渊在你脚下打开了。","color":"#AAB4C3","bold":true,"italic":false},{"text":"在「原质」页里按「踏入深渊」。","color":"#E6DFCF","bold":false,"italic":false}]
