execute unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..96,limit=1] run return run tellraw @s ["",{"text":"[章节调试] 当前范围内没有第一章控制器。","color":"#8B2500","bold":false,"italic":false}]
execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..96,sort=nearest,limit=1] at @s run function rpg:campaign/beelzebub/debug/stage/3_worker
tellraw @s ["",{"text":"[章节调试] ","color":"#B8A98B","bold":true,"italic":false},{"text":"已跳转到 Stage 3；未写入永久进度。","color":"gray","bold":false,"italic":false}]
