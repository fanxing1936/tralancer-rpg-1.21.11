# 仅供玩家主动重新测试调查；绝不在加载或战斗中自动调用。
tag @s remove rpg.name.1
tag @s remove rpg.clue.1.1
tag @s remove rpg.clue.1.2
tag @s remove rpg.clue.1.3
tag @s remove rpg.clue.1.4
tag @s remove rpg.clue.1.5
scoreboard players set @s rpg_case1 0
tag @s remove rpg.name.2
tag @s remove rpg.clue.2.1
tag @s remove rpg.clue.2.2
tag @s remove rpg.clue.2.3
tag @s remove rpg.clue.2.4
tag @s remove rpg.clue.2.5
scoreboard players set @s rpg_case2 0
tag @s remove rpg.name.3
tag @s remove rpg.clue.3.1
tag @s remove rpg.clue.3.2
tag @s remove rpg.clue.3.3
tag @s remove rpg.clue.3.4
tag @s remove rpg.clue.3.5
scoreboard players set @s rpg_case3 0
tag @s remove rpg.name.4
tag @s remove rpg.clue.4.1
tag @s remove rpg.clue.4.2
tag @s remove rpg.clue.4.3
tag @s remove rpg.clue.4.4
tag @s remove rpg.clue.4.5
scoreboard players set @s rpg_case4 0
tag @s remove rpg.name.5
tag @s remove rpg.clue.5.1
tag @s remove rpg.clue.5.2
tag @s remove rpg.clue.5.3
tag @s remove rpg.clue.5.4
tag @s remove rpg.clue.5.5
scoreboard players set @s rpg_case5 0
tag @s remove rpg.name.6
tag @s remove rpg.clue.6.1
tag @s remove rpg.clue.6.2
tag @s remove rpg.clue.6.3
tag @s remove rpg.clue.6.4
tag @s remove rpg.clue.6.5
scoreboard players set @s rpg_case6 0
tag @s remove rpg.name.7
tag @s remove rpg.clue.7.1
tag @s remove rpg.clue.7.2
tag @s remove rpg.clue.7.3
tag @s remove rpg.clue.7.4
tag @s remove rpg.clue.7.5
scoreboard players set @s rpg_case7 0
tellraw @s ["",{"text":"[调查档案] ","color":"#DAA520","bold":true,"italic":false},{"text":"已清空你的七柱真名与罪证；下一次见证将从 1 / 3 开始。","color":"gray","italic":false}]
playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.8 1.0
