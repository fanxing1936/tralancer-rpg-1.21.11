execute unless entity @s[tag=rpg.xb.snowfield] run return run function rpg:explore/first/snowfield
execute if score @s rpg_x_cd matches 1.. run return 0
scoreboard players set @s rpg_x_cd 8
title @s times 5 35 12
title @s title ["",{"text":"雪原","color":"#E6DFCF","bold":true,"italic":false}]
title @s subtitle ["",{"text":"危险 II","color":"#E8D27A","bold":true,"italic":false},{"text":" · 建议第 2 阶  ","color":"#9C9A94","bold":false,"italic":false},{"text":"𝔖𝔫𝔬𝔴𝔣𝔦𝔢𝔩𝔡","color":"#8F7430","bold":false,"italic":false}]
