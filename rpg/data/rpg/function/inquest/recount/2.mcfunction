# 罪证标签才是事实来源；分数只是显示缓存，不能继承旧测试残值。
scoreboard players set @s rpg_case2 0
execute if entity @s[tag=rpg.clue.2.1] run scoreboard players add @s rpg_case2 1
execute if entity @s[tag=rpg.clue.2.2] run scoreboard players add @s rpg_case2 1
execute if entity @s[tag=rpg.clue.2.3] run scoreboard players add @s rpg_case2 1
execute if entity @s[tag=rpg.clue.2.4] run scoreboard players add @s rpg_case2 1
execute if entity @s[tag=rpg.clue.2.5] run scoreboard players add @s rpg_case2 1
