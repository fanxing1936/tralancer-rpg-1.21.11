# 手里这本的阶位与身上一致就不动，否则换新。
execute if entity @s[tag=rpg.pact.off] run return run function rpg:pact/book/stale_off
execute if score @s rpg_pact_lv matches 1 if score @s rpg_pact_dom matches 0 if items entity @s weapon.mainhand *[minecraft:custom_data~{pact_lv:1,pact_dom:0}] run return 0
execute if score @s rpg_pact_lv matches 1 if score @s rpg_pact_dom matches 1 if items entity @s weapon.mainhand *[minecraft:custom_data~{pact_lv:1,pact_dom:1}] run return 0
execute if score @s rpg_pact_lv matches 2 if score @s rpg_pact_dom matches 0 if items entity @s weapon.mainhand *[minecraft:custom_data~{pact_lv:2,pact_dom:0}] run return 0
execute if score @s rpg_pact_lv matches 2 if score @s rpg_pact_dom matches 1 if items entity @s weapon.mainhand *[minecraft:custom_data~{pact_lv:2,pact_dom:1}] run return 0
execute if score @s rpg_pact_lv matches 3 if score @s rpg_pact_dom matches 0 if items entity @s weapon.mainhand *[minecraft:custom_data~{pact_lv:3,pact_dom:0}] run return 0
execute if score @s rpg_pact_lv matches 3 if score @s rpg_pact_dom matches 1 if items entity @s weapon.mainhand *[minecraft:custom_data~{pact_lv:3,pact_dom:1}] run return 0
function rpg:pact/book/fresh
