# 还没有柱位。看手里这本是哪一柱，就翻开哪一柱的条款；真正签下要点界面上的按钮。
# `if items` 读的是手上那一件，不需要翻整个背包。
execute unless entity @s[tag=rpg.pact.off] if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:1}] run function rpg:pact/ui/terms1
execute if entity @s[tag=rpg.pact.off] if items entity @s weapon.offhand *[minecraft:custom_data~{pact:1}] run function rpg:pact/ui/terms1
execute unless entity @s[tag=rpg.pact.off] if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:2}] run function rpg:pact/ui/terms2
execute if entity @s[tag=rpg.pact.off] if items entity @s weapon.offhand *[minecraft:custom_data~{pact:2}] run function rpg:pact/ui/terms2
execute unless entity @s[tag=rpg.pact.off] if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:3}] run function rpg:pact/ui/terms3
execute if entity @s[tag=rpg.pact.off] if items entity @s weapon.offhand *[minecraft:custom_data~{pact:3}] run function rpg:pact/ui/terms3
execute unless entity @s[tag=rpg.pact.off] if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:4}] run function rpg:pact/ui/terms4
execute if entity @s[tag=rpg.pact.off] if items entity @s weapon.offhand *[minecraft:custom_data~{pact:4}] run function rpg:pact/ui/terms4
execute unless entity @s[tag=rpg.pact.off] if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:5}] run function rpg:pact/ui/terms5
execute if entity @s[tag=rpg.pact.off] if items entity @s weapon.offhand *[minecraft:custom_data~{pact:5}] run function rpg:pact/ui/terms5
execute unless entity @s[tag=rpg.pact.off] if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:6}] run function rpg:pact/ui/terms6
execute if entity @s[tag=rpg.pact.off] if items entity @s weapon.offhand *[minecraft:custom_data~{pact:6}] run function rpg:pact/ui/terms6
execute unless entity @s[tag=rpg.pact.off] if items entity @s weapon.mainhand *[minecraft:custom_data~{pact:7}] run function rpg:pact/ui/terms7
execute if entity @s[tag=rpg.pact.off] if items entity @s weapon.offhand *[minecraft:custom_data~{pact:7}] run function rpg:pact/ui/terms7
