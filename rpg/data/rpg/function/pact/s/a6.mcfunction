playsound minecraft:entity.evoker.prepare_summon player @a[distance=..32] ~ ~ ~ 1 0.6
playsound minecraft:block.beacon.power_select player @a[distance=..32] ~ ~ ~ 0.8 0.5
particle enchant ~ ~1.2 ~ 5 1.5 5 1 80
particle witch ~ ~1 ~ 5 1 5 0.2 60
execute as @e[type=#rpg:seal_hostile,distance=..12] at @s run function rpg:pact/s/a6_hit
attribute @s minecraft:scale modifier remove rpg:pact/avatar
attribute @s minecraft:armor modifier remove rpg:pact/avatar
attribute @s minecraft:armor_toughness modifier remove rpg:pact/avatar
attribute @s minecraft:scale modifier add rpg:pact/avatar 0.15 add_value
attribute @s minecraft:armor modifier add rpg:pact/avatar 8 add_value
attribute @s minecraft:armor_toughness modifier add rpg:pact/avatar 4 add_value
particle flash{color:14252761} ~ ~1 ~ 0 0 0 0 1
title @s times 5 50 15
title @s title ["",{"text":"◆ ","italic":false,"color":"#8F7430","bold":true},{"text":"紫宴朝圣","italic":false,"color":"#A057A9","bold":true},{"text":" ◆","italic":false,"color":"#8F7430","bold":true}]
title @s subtitle ["",{"text":"贝","italic":false,"color":"#A057A9","bold":true},{"text":"利尔 · 色欲","italic":false,"color":"#A057A9","bold":true},{"text":" 𝔏𝔲𝔰𝔱","italic":false,"color":"#8F7430"},{"text":"  附身 20 秒","italic":false,"color":"#9C9A94"}]
