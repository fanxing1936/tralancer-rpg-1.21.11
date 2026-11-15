execute store result score #n rpg_jq if entity @e[tag=rpg.jqb.guard]
execute if score #n rpg_jq matches ..3 positioned ^3 ^ ^1 run function rpg:jacques_boss/horn/one
execute if score @s rpg_jq matches 2 run return 0
execute store result score #n rpg_jq if entity @e[tag=rpg.jqb.guard]
execute if score #n rpg_jq matches ..3 positioned ^-3 ^ ^1 run function rpg:jacques_boss/horn/one
