execute unless entity @s[tag=rpg.xb.plains] run return run function rpg:explore/first/plains
execute if score @s rpg_x_cd matches 1.. run return 0
scoreboard players set @s rpg_x_cd 8
title @s times 5 35 12
title @s title ["",{"text":"平原","color":"#E6DFCF","bold":true,"italic":false}]
title @s subtitle ["",{"text":"危险 I","color":"#70DB70","bold":true,"italic":false},{"text":" · 新手也能走  ","color":"#9C9A94","bold":false,"italic":false},{"text":"𝔓𝔩𝔞𝔦𝔫𝔰","color":"#8F7430","bold":false,"italic":false}]
