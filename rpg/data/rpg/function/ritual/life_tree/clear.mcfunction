# 清除执行位置十二格内的阵心；残留粒子会在一秒内自然消散。
execute as @e[type=minecraft:marker,tag=rpg.ritual.life_tree,distance=..12] at @s run kill @e[type=minecraft:item_display,tag=rpg.ritual.life_tree.prop,distance=..8]
execute as @e[type=minecraft:marker,tag=rpg.ritual.life_tree,distance=..12] at @s run kill @e[type=minecraft:item_display,tag=rpg.ritual.life_tree.cross,distance=..8]
kill @e[type=minecraft:marker,tag=rpg.ritual.life_tree,distance=..12]
tellraw @s ["",{"text":"[秘仪] ","color":"#D596F2","bold":true,"italic":false},{"text":"附近的生命之树归于沉寂。","color":"gray","bold":false,"italic":false}]
