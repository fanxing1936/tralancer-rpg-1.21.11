tag @s add rpg.ex.claim2
execute if score @s rpg_ex_path matches 1 run function rpg:inquest/give/bell
execute if score @s rpg_ex_path matches 2 run function rpg:inquest/give/nail
execute if score @s rpg_ex_path matches 3 run function rpg:inquest/give/incense
tellraw @s ["",{"text":"[职业解锁] ","color":"#FFF2A8","bold":true,"italic":false},{"text":"获得本路线的第一件仪式工具。","color":"gray","italic":false}]
