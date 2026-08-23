# 手里这本没盖过印。死一次把书掉了是常事 —— 柱位还在身上，
# 只要新捡的这本正是同一柱，就地重新盖印，而不是把人卡死。
# 柱位对不上才是真的攥错了书。
execute if entity @s[scores={rpg_pact=1}] if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:1}] run return run function rpg:pact/sign1
execute if entity @s[scores={rpg_pact=2}] if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:2}] run return run function rpg:pact/sign2
execute if entity @s[scores={rpg_pact=3}] if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:3}] run return run function rpg:pact/sign3
execute if entity @s[scores={rpg_pact=4}] if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:4}] run return run function rpg:pact/sign4
execute if entity @s[scores={rpg_pact=5}] if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:5}] run return run function rpg:pact/sign5
execute if entity @s[scores={rpg_pact=6}] if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:6}] run return run function rpg:pact/sign6
execute if entity @s[scores={rpg_pact=7}] if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:7}] run return run function rpg:pact/sign7
function rpg:pact/wrong_book
