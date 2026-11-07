data modify storage rpg:pact uuid set from entity @s UUID
function rpg:pact/s/a1_rings with storage rpg:pact
playsound minecraft:entity.evoker.cast_spell player @a[distance=..32] ~ ~ ~ 1 0.6
particle dragon_breath ~ ~1 ~ 4 1 4 0.1 64
execute as @e[type=#rpg:seal_hostile,distance=..8] at @s run function rpg:pact/s/a1_hit
attribute @s minecraft:scale modifier remove rpg:pact/avatar
attribute @s minecraft:attack_damage modifier remove rpg:pact/avatar
attribute @s minecraft:scale modifier add rpg:pact/avatar 0.15 add_value
attribute @s minecraft:attack_damage modifier add rpg:pact/avatar 6 add_value
particle flash{color:6280844} ~ ~1 ~ 0 0 0 0 1
title @s times 5 50 15
title @s title ["",{"text":"◆ ","italic":false,"color":"#8F7430","bold":true},{"text":"万蛇加冕","italic":false,"color":"#34975A","bold":true},{"text":" ◆","italic":false,"color":"#8F7430","bold":true}]
title @s subtitle ["",{"text":"路","italic":false,"color":"#34975A","bold":true},{"text":"西法 · 傲慢","italic":false,"color":"#34975A","bold":true},{"text":" 𝔓𝔯𝔦𝔡𝔢","italic":false,"color":"#8F7430"},{"text":"  附身 20 秒","italic":false,"color":"#9C9A94"}]
