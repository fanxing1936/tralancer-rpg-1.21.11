# 已有柱位。手里必须是**自己那一本已立约的书** —— 攥着别柱的书没有用。
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{pact_signed:1b}] run return run function rpg:pact/reissue
execute if entity @s[scores={rpg_pact_cd=1..}] run return run function rpg:pact/cooling

scoreboard players set @s rpg_pact_cd 300
scoreboard players add @s rpg_taint 3
tag @s add rpg.pact.cast
execute if entity @s[scores={rpg_pact=1}] run function rpg:pact/p1
execute if entity @s[scores={rpg_pact=2}] run function rpg:pact/p2
execute if entity @s[scores={rpg_pact=3}] run function rpg:pact/p3
execute if entity @s[scores={rpg_pact=4}] run function rpg:pact/p4
execute if entity @s[scores={rpg_pact=5}] run function rpg:pact/p5
execute if entity @s[scores={rpg_pact=6}] run function rpg:pact/p6
execute if entity @s[scores={rpg_pact=7}] run function rpg:pact/p7
tag @s remove rpg.pact.cast
