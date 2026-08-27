advancement revoke @s only rpg:inquest/seal_use
function rpg:inquest/seal/reindex
scoreboard players set @s rpg_rel_gap 3
scoreboard players add @s rpg_rel_hold 1
tag @s remove rpg.seal.held_active
execute if score @s rpg_rel_1 matches 1 if items entity @s weapon.mainhand minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:1}] run tag @s add rpg.seal.held_active
execute if score @s rpg_rel_2 matches 1 if items entity @s weapon.mainhand minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:1}] run tag @s add rpg.seal.held_active
execute if score @s rpg_rel_1 matches 2 if items entity @s weapon.mainhand minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:2}] run tag @s add rpg.seal.held_active
execute if score @s rpg_rel_2 matches 2 if items entity @s weapon.mainhand minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:2}] run tag @s add rpg.seal.held_active
execute if score @s rpg_rel_1 matches 3 if items entity @s weapon.mainhand minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:3}] run tag @s add rpg.seal.held_active
execute if score @s rpg_rel_2 matches 3 if items entity @s weapon.mainhand minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:3}] run tag @s add rpg.seal.held_active
execute if score @s rpg_rel_1 matches 4 if items entity @s weapon.mainhand minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:4}] run tag @s add rpg.seal.held_active
execute if score @s rpg_rel_2 matches 4 if items entity @s weapon.mainhand minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:4}] run tag @s add rpg.seal.held_active
execute if score @s rpg_rel_1 matches 5 if items entity @s weapon.mainhand minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:5}] run tag @s add rpg.seal.held_active
execute if score @s rpg_rel_2 matches 5 if items entity @s weapon.mainhand minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:5}] run tag @s add rpg.seal.held_active
execute if score @s rpg_rel_1 matches 6 if items entity @s weapon.mainhand minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:6}] run tag @s add rpg.seal.held_active
execute if score @s rpg_rel_2 matches 6 if items entity @s weapon.mainhand minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:6}] run tag @s add rpg.seal.held_active
execute if score @s rpg_rel_1 matches 7 if items entity @s weapon.mainhand minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:7}] run tag @s add rpg.seal.held_active
execute if score @s rpg_rel_2 matches 7 if items entity @s weapon.mainhand minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:7}] run tag @s add rpg.seal.held_active
execute if score @s rpg_rel_hold matches 30 unless entity @s[tag=rpg.seal.held_active] run tellraw @s ["",{"text":"[遗物休眠] ","color":"dark_gray","bold":true,"italic":false},{"text":"它不在背包顺序的前两个生效槽位。","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_rel_hold matches 30 if entity @s[tag=rpg.seal.held_active] if predicate rpg:sneaking run return run function rpg:inquest/seal/suppress
execute if score @s rpg_rel_hold matches 30 if entity @s[tag=rpg.seal.held_active] unless predicate rpg:sneaking if items entity @s weapon.mainhand minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:2}] run return run function rpg:inquest/seal/ability/leviathan
