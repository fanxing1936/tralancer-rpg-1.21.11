# 书不一定在手上：在手就原地换，在背包就收走重发，一本都没有就不发。
tag @s remove rpg.pact.off
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact_signed:1b}] run return run function rpg:pact/book/fresh
tag @s add rpg.pact.off
execute if items entity @s weapon.offhand *[minecraft:custom_data~{pact_signed:1b}] run return run function rpg:pact/book/fresh
tag @s remove rpg.pact.off
execute store result score #c rpg_pact run clear @s minecraft:enchanted_book[minecraft:custom_data~{pact_signed:1b}] 0
execute if score #c rpg_pact matches ..0 run return 0
clear @s minecraft:enchanted_book[minecraft:custom_data~{pact_signed:1b}]
tag @s add rpg.pact.give
function rpg:pact/book/fresh
tag @s remove rpg.pact.give
