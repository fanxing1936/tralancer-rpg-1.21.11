playsound minecraft:entity.player.levelup player @a[distance=..32] ~ ~ ~ 1 0.6
playsound minecraft:block.anvil.land player @a[distance=..32] ~ ~ ~ 0.7 0.7
particle wax_on ~ ~1 ~ 5 1 5 0.1 80
particle end_rod ~ ~1 ~ 5 1 5 0.05 40
execute as @e[type=#rpg:seal_hostile,distance=..10] at @s run function rpg:pact/s/a7_hit
attribute @s minecraft:scale modifier remove rpg:pact/avatar
attribute @s minecraft:attack_damage modifier remove rpg:pact/avatar
attribute @s minecraft:armor modifier remove rpg:pact/avatar
attribute @s minecraft:luck modifier remove rpg:pact/avatar
attribute @s minecraft:scale modifier add rpg:pact/avatar 0.15 add_value
attribute @s minecraft:attack_damage modifier add rpg:pact/avatar 3 add_value
attribute @s minecraft:armor modifier add rpg:pact/avatar 4 add_value
attribute @s minecraft:luck modifier add rpg:pact/avatar 3 add_value
particle flash{color:15114812} ~ ~1 ~ 0 0 0 0 1
title @s times 5 50 15
title @s title ["",{"text":"◆ ","italic":false,"color":"#8F7430","bold":true},{"text":"黄金终审","italic":false,"color":"#D19C26","bold":true},{"text":" ◆","italic":false,"color":"#8F7430","bold":true}]
title @s subtitle ["",{"text":"玛","italic":false,"color":"#D19C26","bold":true},{"text":"门 · 贪婪","italic":false,"color":"#D19C26","bold":true},{"text":" 𝔊𝔯𝔢𝔢𝔡","italic":false,"color":"#8F7430"},{"text":"  附身 20 秒","italic":false,"color":"#9C9A94"}]
