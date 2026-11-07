playsound minecraft:entity.ender_dragon.growl player @a[distance=..32] ~ ~ ~ 0.8 1.4
particle ash ~ ~1 ~ 5 1.4 5 0.05 80
particle spore_blossom_air ~ ~1 ~ 5 1 5 0.05 60
execute as @e[type=#rpg:seal_hostile,distance=..10] at @s run function rpg:pact/s/a4_hit
attribute @s minecraft:scale modifier remove rpg:pact/avatar
attribute @s minecraft:attack_speed modifier remove rpg:pact/avatar
attribute @s minecraft:scale modifier add rpg:pact/avatar 0.15 add_value
attribute @s minecraft:attack_speed modifier add rpg:pact/avatar 1.5 add_value
particle flash{color:11917655} ~ ~1 ~ 0 0 0 0 1
title @s times 5 50 15
title @s title ["",{"text":"◆ ","italic":false,"color":"#8F7430","bold":true},{"text":"万蝇饕宴","italic":false,"color":"#8CA83D","bold":true},{"text":" ◆","italic":false,"color":"#8F7430","bold":true}]
title @s subtitle ["",{"text":"别","italic":false,"color":"#8CA83D","bold":true},{"text":"西卜 · 暴食","italic":false,"color":"#8CA83D","bold":true},{"text":" 𝔊𝔩𝔲𝔱𝔱𝔬𝔫𝔶","italic":false,"color":"#8F7430"},{"text":"  附身 20 秒","italic":false,"color":"#9C9A94"}]
