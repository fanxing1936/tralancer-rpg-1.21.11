scoreboard players set #fm rpg_fo 0
scoreboard players set #fo rpg_fo 0
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_sigil:1}] run scoreboard players set #fm rpg_fo 1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_sigil:2}] run scoreboard players set #fm rpg_fo 2
execute if items entity @s weapon.offhand *[minecraft:custom_data~{rpg_sigil:1}] run scoreboard players set #fo rpg_fo 1
execute if items entity @s weapon.offhand *[minecraft:custom_data~{rpg_sigil:2}] run scoreboard players set #fo rpg_fo 2
# 契约之书算第 3 种（化身 / 打开契约，rpg:pact/fkey）
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact_tag:1b}] run scoreboard players set #fm rpg_fo 3
execute if items entity @s weapon.offhand *[minecraft:custom_data~{pact_tag:1b}] run scoreboard players set #fo rpg_fo 3
execute if score @s rpg_fo_pm matches 0.. if score @s rpg_fo_po matches 0.. unless score @s rpg_fo_pm = @s rpg_fo_po if score #fm rpg_fo = @s rpg_fo_po if score #fo rpg_fo = @s rpg_fo_pm run function rpg:force/fpress
scoreboard players operation @s rpg_fo_pm = #fm rpg_fo
scoreboard players operation @s rpg_fo_po = #fo rpg_fo
