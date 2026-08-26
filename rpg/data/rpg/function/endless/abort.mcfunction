execute unless entity @e[type=minecraft:marker,tag=rpg.end.controller,distance=..96,sort=nearest,limit=1] run return run tellraw @s ["",{"text":"[无活动副本]","color":"#AAB4C3","bold":false,"italic":false}]
tag @e[type=minecraft:marker,tag=rpg.end.controller] remove rpg.end.controller.current
tag @e[type=minecraft:marker,tag=rpg.end.controller,distance=..96,sort=nearest,limit=1] add rpg.end.controller.current
execute as @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] at @s run function rpg:endless/cleanup
