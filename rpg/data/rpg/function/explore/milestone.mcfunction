# 探索点到档（as 玩家）
execute if score @s rpg_x_pt matches 50.. unless entity @s[tag=rpg.xm.0] run function rpg:explore/m/0
execute if score @s rpg_x_pt matches 150.. unless entity @s[tag=rpg.xm.1] run function rpg:explore/m/1
execute if score @s rpg_x_pt matches 300.. unless entity @s[tag=rpg.xm.2] run function rpg:explore/m/2
execute if score @s rpg_x_pt matches 500.. unless entity @s[tag=rpg.xm.3] run function rpg:explore/m/3
execute if score @s rpg_x_pt matches 800.. unless entity @s[tag=rpg.xm.4] run function rpg:explore/m/4
execute if score @s rpg_x_pt matches 1200.. unless entity @s[tag=rpg.xm.5] run function rpg:explore/m/5
