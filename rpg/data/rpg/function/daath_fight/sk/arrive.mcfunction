execute if score @s rpg_dt_t matches 1..40 run particle minecraft:dust_color_transition{from_color:[0.29,0.31,0.36],to_color:[0.04,0.05,0.06],scale:1.3} ~ ~0.1 ~ 0.7 0.05 0.7 0 8
execute if score @s rpg_dt_t matches 6 run playsound minecraft:entity.generic.splash hostile @a[distance=..48] ~ ~ ~ 1 0.5
execute if score @s rpg_dt_t matches 50 run function rpg:daath/anim/enter/hero
execute if score @s rpg_dt_t matches 60.. run data merge entity @s {Invulnerable:0b}
execute if score @s rpg_dt_t matches 64.. run function rpg:daath_fight/sk/end
