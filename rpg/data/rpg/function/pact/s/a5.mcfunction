playsound minecraft:entity.ravager.roar player @a[distance=..32] ~ ~ ~ 1 0.8
playsound minecraft:entity.generic.explode player @a[distance=..32] ~ ~ ~ 0.8 0.7
particle soul_fire_flame ~ ~1 ~ 5 1 5 0.08 80
particle lava ~ ~1 ~ 4 1 4 0 24
execute as @e[type=#rpg:seal_hostile,distance=..10] at @s run function rpg:pact/s/a5_hit
attribute @s minecraft:scale modifier remove rpg:pact/avatar
attribute @s minecraft:attack_damage modifier remove rpg:pact/avatar
attribute @s minecraft:movement_speed modifier remove rpg:pact/avatar
attribute @s minecraft:scale modifier add rpg:pact/avatar 0.15 add_value
attribute @s minecraft:attack_damage modifier add rpg:pact/avatar 4 add_value
attribute @s minecraft:movement_speed modifier add rpg:pact/avatar 0.03 add_value
particle flash{color:16735314} ~ ~1 ~ 0 0 0 0 1
title @s times 5 50 15
title @s title ["",{"text":"◆ ","italic":false,"color":"#8F7430","bold":true},{"text":"血怒天罚","italic":false,"color":"#C4433A","bold":true},{"text":" ◆","italic":false,"color":"#8F7430","bold":true}]
title @s subtitle ["",{"text":"萨","italic":false,"color":"#C4433A","bold":true},{"text":"麦尔 · 暴怒","italic":false,"color":"#C4433A","bold":true},{"text":" 𝔚𝔯𝔞𝔱𝔥","italic":false,"color":"#8F7430"},{"text":"  附身 20 秒","italic":false,"color":"#9C9A94"}]
