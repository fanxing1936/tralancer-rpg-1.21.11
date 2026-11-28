execute if score @s rpg_mk_t matches 80 run function rpg:michael/anim/enter/twirl
execute if score @s rpg_mk_t matches 10..130 run function rpg:michael_boss_i4/seraph/tick
execute if score @s rpg_mk_t matches 132 run function rpg:michael_boss_i4/seraph/out
execute if score @s rpg_mk_t matches 134 run function rpg:michael_boss_i4/solid/on
execute if score @s rpg_mk_t matches 134 run scoreboard players set @s rpg_mk_so 40
execute if score @s rpg_mk_t matches 134 run function rpg:michael/anim/enter/idle
execute if score @s rpg_mk_t matches 174.. run function rpg:michael_boss_i4/sk/end
