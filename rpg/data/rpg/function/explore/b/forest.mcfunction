execute unless entity @s[tag=rpg.xb.forest] run return run function rpg:explore/first/forest
execute if score @s rpg_x_cd matches 1.. run return 0
scoreboard players set @s rpg_x_cd 8
title @s times 5 35 12
title @s title ["",{"text":"森林","color":"#E6DFCF","bold":true,"italic":false}]
title @s subtitle ["",{"text":"危险 I","color":"#70DB70","bold":true,"italic":false},{"text":" · 新手也能走  ","color":"#9C9A94","bold":false,"italic":false},{"text":"𝔉𝔬𝔯𝔢𝔰𝔱","color":"#8F7430","bold":false,"italic":false}]
