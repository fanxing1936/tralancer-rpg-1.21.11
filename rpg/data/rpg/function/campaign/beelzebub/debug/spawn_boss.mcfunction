execute unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..96,limit=1] run return run tellraw @s ["",{"text":"[章节调试] 当前范围内没有第一章控制器。","color":"#8B2500","bold":false,"italic":false}]
tag @s add rpg.ch1.debug.caller
execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..96,sort=nearest,limit=1] at @s unless entity @e[type=minecraft:vindicator,tag=rpg.ch1.boss,distance=..72,limit=1] run function rpg:campaign/beelzebub/spawn/boss
tag @s remove rpg.ch1.debug.caller
