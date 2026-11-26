execute if score @s rpg_dt_t matches 1 run execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
execute if score @s rpg_dt_t matches 1 run function rpg:daath/anim/enter/ka3
execute if score @s rpg_dt_t matches 7 run function rpg:daath_fight/guard/counter
execute if score @s rpg_dt_t matches 22.. run function rpg:daath_fight/sk/end
