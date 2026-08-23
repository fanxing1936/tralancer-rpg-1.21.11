# 还没有柱位。看手里这本是哪一柱，就签哪一柱。
# `if items` 读的是手上那一件，不需要翻整个背包。
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:1}] run function rpg:pact/sign1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:2}] run function rpg:pact/sign2
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:3}] run function rpg:pact/sign3
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:4}] run function rpg:pact/sign4
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:5}] run function rpg:pact/sign5
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:6}] run function rpg:pact/sign6
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:7}] run function rpg:pact/sign7
