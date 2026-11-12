# 藤蔓每刻：寿命倒数，部件跟随根。
execute if entity @e[type=minecraft:armor_stand,tag=rpg.luv.root,limit=1] as @e[type=minecraft:armor_stand,tag=rpg.luv.root,tag=rpg.luv] at @s run function rpg:lucifer_vine/follow
execute if entity @e[type=minecraft:armor_stand,tag=rpg.luv.root,limit=1] as @e[type=minecraft:armor_stand,tag=rpg.luv.root,tag=rpg.luv] run function rpg:lucifer_vine/life
execute if entity @e[type=minecraft:item_display,tag=rpg.luv.part,predicate=!rpg:lucifer_vine/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.luv.part,predicate=!rpg:lucifer_vine/riding]
