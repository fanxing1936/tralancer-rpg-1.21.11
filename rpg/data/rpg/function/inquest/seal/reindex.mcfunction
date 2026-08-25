scoreboard players set @s rpg_seal_i 0
tag @s remove rpg.seal.carrier
execute if items entity @s inventory.* minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b}] run tag @s add rpg.seal.carrier
execute unless entity @s[tag=rpg.seal.carrier] run scoreboard players set @s rpg_seal_t 0
