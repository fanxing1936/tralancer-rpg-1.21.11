# 故乡还在建：先在黑幕里等
execute unless entity @s[tag=rpg.tw.wait] run gamemode spectator @s
tag @s add rpg.tw.wait
effect give @s minecraft:blindness infinite 0 true
title @s actionbar ["",{"text":"正在为你的故乡清出一块平地……","color":"#9C9A94","bold":false,"italic":false}]
