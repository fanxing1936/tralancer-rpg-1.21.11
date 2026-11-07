advancement revoke @s only rpg:pact/page
execute if entity @s[scores={rpg_pact_t=1..}] run return 0
scoreboard players set @s rpg_pact_t 8
execute if items entity @s weapon.* *[minecraft:custom_data~{pact_page:1}] run return run function rpg:pact/page/try1
execute if items entity @s weapon.* *[minecraft:custom_data~{pact_page:2}] run return run function rpg:pact/page/try2
execute if items entity @s weapon.* *[minecraft:custom_data~{pact_page:3}] run return run function rpg:pact/page/try3
execute if items entity @s weapon.* *[minecraft:custom_data~{pact_page:4}] run return run function rpg:pact/page/try4
execute if items entity @s weapon.* *[minecraft:custom_data~{pact_page:5}] run return run function rpg:pact/page/try5
execute if items entity @s weapon.* *[minecraft:custom_data~{pact_page:6}] run return run function rpg:pact/page/try6
execute if items entity @s weapon.* *[minecraft:custom_data~{pact_page:7}] run return run function rpg:pact/page/try7
