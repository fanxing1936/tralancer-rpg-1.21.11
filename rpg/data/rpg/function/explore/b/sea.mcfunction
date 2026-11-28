execute unless entity @s[tag=rpg.xb.sea] run return run function rpg:explore/first/sea
execute if score @s rpg_x_cd matches 1.. run return 0
scoreboard players set @s rpg_x_cd 8
title @s times 5 35 12
title @s title ["",{"text":"海与河","color":"#E6DFCF","bold":true,"italic":false}]
title @s subtitle ["",{"text":"危险 I","color":"#70DB70","bold":true,"italic":false},{"text":" · 新手也能走  ","color":"#9C9A94","bold":false,"italic":false},{"text":"𝔖𝔢𝔞𝔰 𝔞𝔫𝔡 ℜ𝔦𝔳𝔢𝔯𝔰","color":"#8F7430","bold":false,"italic":false}]
