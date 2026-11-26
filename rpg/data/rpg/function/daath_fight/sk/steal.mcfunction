execute if score @s rpg_dt_t matches 1..14 run execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
execute if score @s rpg_dt_t matches 14 run function rpg:daath_fight/steal/lane
execute if score @s rpg_dt_t matches 1..20 run particle minecraft:dust_color_transition{from_color:[0.29,0.31,0.36],to_color:[0.04,0.05,0.06],scale:1.3} ^-0.4 ^1.3 ^0.8 0.1 0.1 0.1 0 3
execute if score @s rpg_dt_t matches 24 run function rpg:daath/anim/enter/throw
execute if score @s rpg_dt_t matches 26 run function rpg:daath_fight/steal/reach
execute if score @s rpg_dt_t matches 46.. run function rpg:daath_fight/sk/end
