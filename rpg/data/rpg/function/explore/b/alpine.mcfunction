execute unless entity @s[tag=rpg.xb.alpine] run return run function rpg:explore/first/alpine
execute if score @s rpg_x_cd matches 1.. run return 0
scoreboard players set @s rpg_x_cd 8
title @s times 5 35 12
title @s title ["",{"text":"高山","color":"#E6DFCF","bold":true,"italic":false}]
title @s subtitle ["",{"text":"危险 IV","color":"#FF6B5E","bold":true,"italic":false},{"text":" · 建议第 5 阶  ","color":"#9C9A94","bold":false,"italic":false},{"text":"𝔄𝔩𝔭𝔦𝔫𝔢","color":"#8F7430","bold":false,"italic":false}]
