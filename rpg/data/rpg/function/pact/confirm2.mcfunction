# 点下「签下」。界面开着的时候书可能已经换手，所以重新认一次。
execute if entity @s[tag=rpg.pact] run return 0
tag @s remove rpg.pact.off
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{pact:2}] run tag @s add rpg.pact.off
execute if entity @s[tag=rpg.pact.off] unless items entity @s weapon.offhand *[minecraft:custom_data~{pact:2}] run return run function rpg:pact/say/no_book
execute if entity @s[gamemode=creative] run return run function rpg:pact/grant2
execute store result score #c rpg_pact run clear @s minecraft:prismarine_crystals[!minecraft:custom_data] 0
execute if score #c rpg_pact matches ..7 run return run function rpg:pact/say/tribute2
clear @s minecraft:prismarine_crystals[!minecraft:custom_data] 8
function rpg:pact/grant2
