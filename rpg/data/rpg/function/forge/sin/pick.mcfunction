# 选了第 rpg_fg_arg 柱
execute unless score @s rpg_sef matches 5.. run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　原质要到第 5 阶（美丽阶）才能锻罪器","color":"#C04A3C","bold":false,"italic":false}]
execute if score @s rpg_fg_arg matches 1 run return run function rpg:forge/sin/pick_1
execute if score @s rpg_fg_arg matches 2 run return run function rpg:forge/sin/pick_2
execute if score @s rpg_fg_arg matches 3 run return run function rpg:forge/sin/pick_3
execute if score @s rpg_fg_arg matches 4 run return run function rpg:forge/sin/pick_4
execute if score @s rpg_fg_arg matches 5 run return run function rpg:forge/sin/pick_5
execute if score @s rpg_fg_arg matches 6 run return run function rpg:forge/sin/pick_6
execute if score @s rpg_fg_arg matches 7 run return run function rpg:forge/sin/pick_7
