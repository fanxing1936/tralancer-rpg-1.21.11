scoreboard players operation #m rpg_ub = @s rpg_ub_t
scoreboard players set #k rpg_ub 2
scoreboard players operation #m rpg_ub %= #k rpg_ub
execute if score @s rpg_ub_t matches 26..36 at @s if block ^ ^0.5 ^1.1 #minecraft:replaceable if block ^ ^1.5 ^1.1 #minecraft:replaceable run tp @s ^ ^ ^1.1
execute if score @s rpg_ub_t matches 27..37 if score #m rpg_ub matches 1 at @s run function rpg:usurper_boss/strike/burst
execute if score @s rpg_ub_t matches 38 run tag @e[tag=rpg.unit] remove rpg.usb.dhit
execute if score @s rpg_ub_t matches 50.. run function rpg:usurper_boss/sk/end
