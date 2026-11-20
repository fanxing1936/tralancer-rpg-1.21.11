execute if score @s rpg_mk_t matches 3 run function rpg:michael_boss/strike/rib
execute if score @s rpg_mk_t matches 6 run execute store result score #r rpg_mk run random value 1..6
execute if score @s rpg_mk_t matches 6 run execute if score #r rpg_mk matches 1 run function rpg:michael/anim/enter/rib_slash1
execute if score @s rpg_mk_t matches 6 run execute if score #r rpg_mk matches 2 run function rpg:michael/anim/enter/rib_slash2
execute if score @s rpg_mk_t matches 6 run execute if score #r rpg_mk matches 3 run function rpg:michael/anim/enter/rib_slash3
execute if score @s rpg_mk_t matches 6 run execute if score #r rpg_mk matches 4 run function rpg:michael/anim/enter/rib_slash4
execute if score @s rpg_mk_t matches 6 run execute if score #r rpg_mk matches 5 run function rpg:michael/anim/enter/rib_slash5
execute if score @s rpg_mk_t matches 6 run execute if score #r rpg_mk matches 6 run function rpg:michael/anim/enter/rib_slash6
execute if score @s rpg_mk_t matches 8 run function rpg:michael_boss/strike/rib
execute if score @s rpg_mk_t matches 11.. run function rpg:michael_boss/sk/end
