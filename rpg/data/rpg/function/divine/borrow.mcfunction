execute if score @s rpg_lt_div_cd matches 1.. run return run function rpg:divine/cooling
scoreboard players set @s rpg_lt_div_cd 300
scoreboard players set @s rpg_lt_div_max 300
tag @s add rpg.pact.cast
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:1}] run function rpg:pact/p1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:2}] run function rpg:pact/p2
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:3}] run function rpg:pact/p3
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:4}] run function rpg:pact/p4
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:5}] run function rpg:pact/p5
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:6}] run function rpg:pact/p6
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:7}] run function rpg:pact/p7
tag @s remove rpg.pact.cast
particle minecraft:end_rod ~ ~1 ~ 0.4 0.7 0.4 0.05 25
function rpg:hud/m62
