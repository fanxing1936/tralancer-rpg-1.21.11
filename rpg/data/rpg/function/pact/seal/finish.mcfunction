# 处刑者：生命低于两成时追一刀。
execute store result score #h rpg_pact run data get entity @s Health 5
execute store result score #m rpg_pact run attribute @s minecraft:max_health get
execute if score #h rpg_pact < #m rpg_pact run damage @s 8 minecraft:magic
