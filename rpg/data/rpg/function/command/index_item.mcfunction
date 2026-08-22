# @e[type=minecraft:item] 的全部 custom_data 标记，逐个实体一次算完。

tag @s remove rpg.i.add_weapon_tag1
tag @s remove rpg.i.chestplate_tag1
tag @s remove rpg.i.diamond_tag1
tag @s remove rpg.i.echo_tag1
tag @s remove rpg.i.echo_tag2
tag @s remove rpg.i.embryo_tag1
tag @s remove rpg.i.enchant_tag1
tag @s remove rpg.i.fec_tag1
tag @s remove rpg.i.flame_tag1
tag @s remove rpg.i.gold_tag1
tag @s remove rpg.i.level_item1
tag @s remove rpg.i.loot1
tag @s remove rpg.i.loot2
tag @s remove rpg.i.loot3
tag @s remove rpg.i.loot4
tag @s remove rpg.i.loot5
tag @s remove rpg.i.loot6
tag @s remove rpg.i.loot7
tag @s remove rpg.i.loot8
tag @s remove rpg.i.loot_trigger1
tag @s remove rpg.i.loot_trigger2
tag @s remove rpg.i.sweep_tag1
tag @s remove rpg.i.sword_tag1
tag @s remove rpg.i.trial_summon1
tag @s remove rpg.i.trial_summon2
tag @s remove rpg.i.trial_tag1
tag @s remove rpg.i.trial_tag2
tag @s remove rpg.i.weapon_tag1
tag @s remove rpg.i.weapon_tree1
tag @s remove rpg.i.weapon_tree2
tag @s remove rpg.i.weapon_tree3
tag @s remove rpg.i.weapon_tree4
tag @s remove rpg.i.weapon_tree5
tag @s remove rpg.i.weapon_tree6
tag @s remove rpg.i.wind_tag1

execute if items entity @s contents *[minecraft:custom_data~{add_weapon_tag:1b}] run tag @s add rpg.i.add_weapon_tag1
execute if items entity @s contents *[minecraft:custom_data~{chestplate_tag:1b}] run tag @s add rpg.i.chestplate_tag1
execute if items entity @s contents *[minecraft:custom_data~{diamond_tag:1b}] run tag @s add rpg.i.diamond_tag1
execute if items entity @s contents *[minecraft:custom_data~{echo_tag:1b}] run tag @s add rpg.i.echo_tag1
execute if items entity @s contents *[minecraft:custom_data~{echo_tag:2b}] run tag @s add rpg.i.echo_tag2
execute if items entity @s contents *[minecraft:custom_data~{embryo_tag:1b}] run tag @s add rpg.i.embryo_tag1
execute if items entity @s contents *[minecraft:custom_data~{enchant_tag:1b}] run tag @s add rpg.i.enchant_tag1
execute if items entity @s contents *[minecraft:custom_data~{fec_tag:1b}] run tag @s add rpg.i.fec_tag1
execute if items entity @s contents *[minecraft:custom_data~{flame_tag:1b}] run tag @s add rpg.i.flame_tag1
execute if items entity @s contents *[minecraft:custom_data~{gold_tag:1b}] run tag @s add rpg.i.gold_tag1
execute if items entity @s contents *[minecraft:custom_data~{level_item:1b}] run tag @s add rpg.i.level_item1
execute if items entity @s contents *[minecraft:custom_data~{loot:1b}] run tag @s add rpg.i.loot1
execute if items entity @s contents *[minecraft:custom_data~{loot:2b}] run tag @s add rpg.i.loot2
execute if items entity @s contents *[minecraft:custom_data~{loot:3b}] run tag @s add rpg.i.loot3
execute if items entity @s contents *[minecraft:custom_data~{loot:4b}] run tag @s add rpg.i.loot4
execute if items entity @s contents *[minecraft:custom_data~{loot:5b}] run tag @s add rpg.i.loot5
execute if items entity @s contents *[minecraft:custom_data~{loot:6b}] run tag @s add rpg.i.loot6
execute if items entity @s contents *[minecraft:custom_data~{loot:7b}] run tag @s add rpg.i.loot7
execute if items entity @s contents *[minecraft:custom_data~{loot:8b}] run tag @s add rpg.i.loot8
execute if items entity @s contents *[minecraft:custom_data~{loot_trigger:1b}] run tag @s add rpg.i.loot_trigger1
execute if items entity @s contents *[minecraft:custom_data~{loot_trigger:2b}] run tag @s add rpg.i.loot_trigger2
execute if items entity @s contents *[minecraft:custom_data~{sweep_tag:1b}] run tag @s add rpg.i.sweep_tag1
execute if items entity @s contents *[minecraft:custom_data~{sword_tag:1b}] run tag @s add rpg.i.sword_tag1
execute if items entity @s contents *[minecraft:custom_data~{trial_summon:1b}] run tag @s add rpg.i.trial_summon1
execute if items entity @s contents *[minecraft:custom_data~{trial_summon:2b}] run tag @s add rpg.i.trial_summon2
execute if items entity @s contents *[minecraft:custom_data~{trial_tag:1b}] run tag @s add rpg.i.trial_tag1
execute if items entity @s contents *[minecraft:custom_data~{trial_tag:2b}] run tag @s add rpg.i.trial_tag2
execute if items entity @s contents *[minecraft:custom_data~{weapon_tag:1b}] run tag @s add rpg.i.weapon_tag1
execute if items entity @s contents *[minecraft:custom_data~{weapon_tree:1b}] run tag @s add rpg.i.weapon_tree1
execute if items entity @s contents *[minecraft:custom_data~{weapon_tree:2b}] run tag @s add rpg.i.weapon_tree2
execute if items entity @s contents *[minecraft:custom_data~{weapon_tree:3b}] run tag @s add rpg.i.weapon_tree3
execute if items entity @s contents *[minecraft:custom_data~{weapon_tree:4b}] run tag @s add rpg.i.weapon_tree4
execute if items entity @s contents *[minecraft:custom_data~{weapon_tree:5b}] run tag @s add rpg.i.weapon_tree5
execute if items entity @s contents *[minecraft:custom_data~{weapon_tree:6b}] run tag @s add rpg.i.weapon_tree6
execute if items entity @s contents *[minecraft:custom_data~{wind_tag:1b}] run tag @s add rpg.i.wind_tag1
