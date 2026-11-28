execute unless entity @s[tag=rpg.xb.mesa] run return run function rpg:explore/first/mesa
execute if score @s rpg_x_cd matches 1.. run return 0
scoreboard players set @s rpg_x_cd 8
title @s times 5 35 12
title @s title ["",{"text":"平顶山沙漠","color":"#E6DFCF","bold":true,"italic":false}]
title @s subtitle ["",{"text":"危险 III","color":"#FFA15C","bold":true,"italic":false},{"text":" · 建议第 4 阶  ","color":"#9C9A94","bold":false,"italic":false},{"text":"𝔐𝔢𝔰𝔞 𝔙𝔞𝔩𝔩𝔢𝔶","color":"#8F7430","bold":false,"italic":false}]
