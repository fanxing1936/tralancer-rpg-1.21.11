execute if score @s rpg_dt_t matches 1..8 run execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
execute if score @s rpg_dt_t matches 9 run function rpg:daath_fight/lance/warn
execute if score @s rpg_dt_t matches 25 run function rpg:daath/anim/enter/sp3
execute if score @s rpg_dt_t matches 26 run function rpg:daath_fight/lance/go
execute if score @s rpg_dt_t matches 44.. run function rpg:daath_fight/sk/end
