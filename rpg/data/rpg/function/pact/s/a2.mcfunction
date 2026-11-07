playsound minecraft:entity.elder_guardian.curse player @a[distance=..32] ~ ~ ~ 1 0.5
particle nautilus ~ ~1 ~ 5 1.2 5 0.2 80
particle bubble_column_up ~ ~0.4 ~ 5 0.5 5 0.35 80
execute as @e[type=#rpg:seal_hostile,distance=..12] at @s run function rpg:pact/s/a2_hit
attribute @s minecraft:scale modifier remove rpg:pact/avatar
attribute @s minecraft:movement_speed modifier remove rpg:pact/avatar
attribute @s minecraft:attack_damage modifier remove rpg:pact/avatar
attribute @s minecraft:scale modifier add rpg:pact/avatar 0.15 add_value
attribute @s minecraft:movement_speed modifier add rpg:pact/avatar 0.04 add_value
attribute @s minecraft:attack_damage modifier add rpg:pact/avatar 2 add_value
particle flash{color:5218032} ~ ~1 ~ 0 0 0 0 1
title @s times 5 50 15
title @s title ["",{"text":"◆ ","italic":false,"color":"#8F7430","bold":true},{"text":"妒海沉城","italic":false,"color":"#387AB7","bold":true},{"text":" ◆","italic":false,"color":"#8F7430","bold":true}]
title @s subtitle ["",{"text":"利","italic":false,"color":"#387AB7","bold":true},{"text":"维坦 · 嫉妒","italic":false,"color":"#387AB7","bold":true},{"text":" 𝔈𝔫𝔳𝔶","italic":false,"color":"#8F7430"},{"text":"  附身 20 秒","italic":false,"color":"#9C9A94"}]
