playsound minecraft:entity.warden.sonic_boom player @a[distance=..32] ~ ~ ~ 0.8 0.7
playsound minecraft:block.sculk_shrieker.shriek player @a[distance=..32] ~ ~ ~ 1 0.6
particle sculk_soul ~ ~1 ~ 5 1 5 0.03 80
particle soul ~ ~0.5 ~ 5 0.6 5 0.04 60
execute as @e[type=#rpg:seal_hostile,distance=..10] at @s run function rpg:pact/s/a3_hit
attribute @s minecraft:scale modifier remove rpg:pact/avatar
attribute @s minecraft:max_health modifier remove rpg:pact/avatar
attribute @s minecraft:armor modifier remove rpg:pact/avatar
attribute @s minecraft:scale modifier add rpg:pact/avatar 0.15 add_value
attribute @s minecraft:max_health modifier add rpg:pact/avatar 20 add_value
attribute @s minecraft:armor modifier add rpg:pact/avatar 4 add_value
particle flash{color:10989513} ~ ~1 ~ 0 0 0 0 1
title @s times 5 50 15
title @s title ["",{"text":"◆ ","italic":false,"color":"#8F7430","bold":true},{"text":"终末收割","italic":false,"color":"#8C90A1","bold":true},{"text":" ◆","italic":false,"color":"#8F7430","bold":true}]
title @s subtitle ["",{"text":"亚","italic":false,"color":"#8C90A1","bold":true},{"text":"巴顿 · 怠惰","italic":false,"color":"#8C90A1","bold":true},{"text":" 𝔖𝔩𝔬𝔱𝔥","italic":false,"color":"#8F7430"},{"text":"  附身 20 秒","italic":false,"color":"#9C9A94"}]
