schedule function rpg:entry/endless/rearm 20t replace
execute if entity @e[type=minecraft:marker,tag=rpg.end.controller,limit=1] run return run tellraw @s ["",{"text":"[信物沉寂] ","color":"#FF3300","bold":true,"italic":false},{"text":"已有七柱回廊正在运行；请加入，或等本轮结束后再回应。","color":"gray","bold":false,"italic":false}]
execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run return run tellraw @s ["",{"text":"[信物沉寂] ","color":"#FF3300","bold":true,"italic":false},{"text":"第一章调查尚未结束；结案后再回应回廊。","color":"gray","bold":false,"italic":false}]
function rpg:endless/start
