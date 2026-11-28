execute unless entity @s[tag=rpg.xb.war] run return run function rpg:explore/first/war
execute if score @s rpg_x_cd matches 1.. run return 0
scoreboard players set @s rpg_x_cd 8
title @s times 5 35 12
title @s title ["",{"text":"战争前线","color":"#E6DFCF","bold":true,"italic":false}]
title @s subtitle ["",{"text":"危险 V","color":"#FF3300","bold":true,"italic":false},{"text":" · 建议第 6 阶  ","color":"#9C9A94","bold":false,"italic":false},{"text":"𝔚𝔞𝔯 𝔉𝔯𝔬𝔫𝔱","color":"#8F7430","bold":false,"italic":false}]
