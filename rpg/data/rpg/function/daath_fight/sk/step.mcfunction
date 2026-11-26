execute if score @s rpg_dt_t matches 1..12 run particle minecraft:squid_ink ~ ~0.6 ~ 0.4 0.6 0.4 0.02 5
execute if score @s rpg_dt_t matches 8..20 run execute at @a[tag=rpg.dt.me,limit=1] run particle minecraft:dust_color_transition{from_color:[0.29,0.31,0.36],to_color:[0.04,0.05,0.06],scale:1.3} ~ ~0.05 ~ 0.6 0.02 0.6 0 8
execute if score @s rpg_dt_t matches 14 run function rpg:daath_fight/step/out
execute if score @s rpg_dt_t matches 15 run function rpg:daath/anim/enter/sw3
execute if score @s rpg_dt_t matches 19 run function rpg:daath_fight/step/stab
execute if score @s rpg_dt_t matches 34.. run function rpg:daath_fight/sk/end
