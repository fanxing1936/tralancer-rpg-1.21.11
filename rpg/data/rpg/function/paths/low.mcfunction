execute store result score #h rpg_pa run data get entity @s Health 10
execute store result score #m rpg_pa run attribute @s minecraft:max_health get 3
execute if score #h rpg_pa < #m rpg_pa run scoreboard players add @s rpg_pa_23 1
