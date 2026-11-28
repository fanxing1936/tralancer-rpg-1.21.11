execute if score @s rpg_mk_t matches 20 run function rpg:michael_boss_i3/who/warn0
execute if score @s rpg_mk_t matches 40 run function rpg:michael_boss_i3/who/strike0
execute if score @s rpg_mk_t matches 40 run function rpg:michael/anim/enter/slash1
execute if score @s rpg_mk_t matches 60 run function rpg:michael_boss_i3/who/warn1
execute if score @s rpg_mk_t matches 80 run function rpg:michael_boss_i3/who/strike1
execute if score @s rpg_mk_t matches 80 run function rpg:michael/anim/enter/slash1
execute if score @s rpg_mk_t matches 100 run function rpg:michael_boss_i3/who/warn2
execute if score @s rpg_mk_t matches 120 run function rpg:michael_boss_i3/who/strike2
execute if score @s rpg_mk_t matches 120 run function rpg:michael/anim/enter/slash1
execute if score @s rpg_mk_t matches 130 run function rpg:michael/anim/enter/horn
execute if score @s rpg_mk_t matches 136 run function rpg:michael_boss_i3/solid/on
execute if score @s rpg_mk_t matches 136 run scoreboard players set @s rpg_mk_so 40
execute if score @s rpg_mk_t matches 136 run function rpg:michael/anim/enter/idle
execute if score @s rpg_mk_t matches 176.. run function rpg:michael_boss_i3/sk/end
