execute if score @s rpg_dt_t matches 1..17 run execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
execute if score @s rpg_dt_t matches 6 run execute if score @s rpg_dt_wc matches 8 run function rpg:daath/anim/enter/bow_draw
execute if score @s rpg_dt_t matches 10..17 positioned ^ ^1.4 ^0.6 run particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ~ ~ ~ 0.05 0.05 0.05 0 2
execute if score @s rpg_dt_t matches 18 if score @s rpg_dt_wc matches 8 run function rpg:daath_fight/shoot/bow
execute if score @s rpg_dt_t matches 16 if score @s rpg_dt_wc matches 9 run function rpg:daath_fight/shoot/bolt
execute if score @s rpg_dt_t matches 22 if score @s rpg_dt_wc matches 9 run function rpg:daath_fight/shoot/bolt
execute if score @s rpg_dt_t matches 28 if score @s rpg_dt_wc matches 9 run function rpg:daath_fight/shoot/bolt
execute if score @s rpg_dt_t matches 19..27 run execute if score @s rpg_dt_wc matches 9 run execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
execute if score @s rpg_dt_t matches 38.. run function rpg:daath_fight/sk/end
