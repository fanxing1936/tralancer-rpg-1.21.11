execute if score @s rpg_pact_lv matches 1 if score @s rpg_pact_dom matches 0 if items entity @s weapon.offhand *[minecraft:custom_data~{pact_lv:1,pact_dom:0}] run return 0
execute if score @s rpg_pact_lv matches 1 if score @s rpg_pact_dom matches 1 if items entity @s weapon.offhand *[minecraft:custom_data~{pact_lv:1,pact_dom:1}] run return 0
execute if score @s rpg_pact_lv matches 2 if score @s rpg_pact_dom matches 0 if items entity @s weapon.offhand *[minecraft:custom_data~{pact_lv:2,pact_dom:0}] run return 0
execute if score @s rpg_pact_lv matches 2 if score @s rpg_pact_dom matches 1 if items entity @s weapon.offhand *[minecraft:custom_data~{pact_lv:2,pact_dom:1}] run return 0
execute if score @s rpg_pact_lv matches 3 if score @s rpg_pact_dom matches 0 if items entity @s weapon.offhand *[minecraft:custom_data~{pact_lv:3,pact_dom:0}] run return 0
execute if score @s rpg_pact_lv matches 3 if score @s rpg_pact_dom matches 1 if items entity @s weapon.offhand *[minecraft:custom_data~{pact_lv:3,pact_dom:1}] run return 0
function rpg:pact/book/fresh
