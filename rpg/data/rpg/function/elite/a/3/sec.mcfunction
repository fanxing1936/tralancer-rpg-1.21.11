execute store result score #h rpg_el run data get entity @s Health 10
execute store result score #mh rpg_el run attribute @s minecraft:max_health get 4
execute if score #h rpg_el <= #mh rpg_el run effect give @s minecraft:strength 2 1 true
