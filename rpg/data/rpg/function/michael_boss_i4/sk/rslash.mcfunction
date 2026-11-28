execute if score @s rpg_mk_t matches 3 run function rpg:michael_boss_i4/strike/rib
execute if score @s rpg_mk_t matches 6 run execute store result score #r rpg_mk_i4 run random value 1..6
execute if score @s rpg_mk_t matches 6 run execute if score #r rpg_mk_i4 matches 1 run function rpg:michael/anim/enter/rib_slash1
execute if score @s rpg_mk_t matches 6 run execute if score #r rpg_mk_i4 matches 2 run function rpg:michael/anim/enter/rib_slash2
execute if score @s rpg_mk_t matches 6 run execute if score #r rpg_mk_i4 matches 3 run function rpg:michael/anim/enter/rib_slash3
execute if score @s rpg_mk_t matches 6 run execute if score #r rpg_mk_i4 matches 4 run function rpg:michael/anim/enter/rib_slash4
execute if score @s rpg_mk_t matches 6 run execute if score #r rpg_mk_i4 matches 5 run function rpg:michael/anim/enter/rib_slash5
execute if score @s rpg_mk_t matches 6 run execute if score #r rpg_mk_i4 matches 6 run function rpg:michael/anim/enter/rib_slash6
execute if score @s rpg_mk_t matches 8 run function rpg:michael_boss_i4/strike/rib
execute if score @s rpg_mk_t matches 11.. run function rpg:michael_boss_i4/sk/end
