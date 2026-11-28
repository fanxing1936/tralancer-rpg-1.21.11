execute unless entity @s[tag=rpg.xb.eroded] run return run function rpg:explore/first/eroded
execute if score @s rpg_x_cd matches 1.. run return 0
scoreboard players set @s rpg_x_cd 8
title @s times 5 35 12
title @s title ["",{"text":"侵蚀沙漠","color":"#E6DFCF","bold":true,"italic":false}]
title @s subtitle ["",{"text":"危险 III","color":"#FFA15C","bold":true,"italic":false},{"text":" · 建议第 4 阶  ","color":"#9C9A94","bold":false,"italic":false},{"text":"𝔈𝔯𝔬𝔡𝔢𝔡 𝔇𝔢𝔰𝔢𝔯𝔱","color":"#8F7430","bold":false,"italic":false}]
