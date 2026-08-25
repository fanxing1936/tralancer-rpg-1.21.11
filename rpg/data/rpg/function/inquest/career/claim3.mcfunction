tag @s add rpg.ex.claim3
execute if score @s rpg_ex_path matches 1 run function rpg:inquest/give/chalk2
execute if score @s rpg_ex_path matches 2 run function rpg:inquest/give/chalk1
execute if score @s rpg_ex_path matches 3 run function rpg:inquest/give/chalk3
tellraw @s ["",{"text":"[职业解锁] ","color":"#FFF2A8","bold":true,"italic":false},{"text":"获得本路线的仪式粉笔。","color":"gray","italic":false}]
