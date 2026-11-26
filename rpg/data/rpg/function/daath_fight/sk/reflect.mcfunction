execute if score @s rpg_dt_t matches 1..20 run particle minecraft:squid_ink ~ ~0.3 ~ 0.6 0.2 0.6 0.04 8
execute if score @s rpg_dt_t matches 20 run function rpg:daath_fight/reflect/hide
execute if score @s rpg_dt_t matches 24..200 at @a[tag=rpg.dt.me,limit=1] run particle minecraft:dust_color_transition{from_color:[0.29,0.31,0.36],to_color:[0.04,0.05,0.06],scale:1.3} ~ ~0.03 ~ 0.5 0.01 0.5 0 5
execute if score @s rpg_dt_t matches 36 run execute at @a[tag=rpg.dt.me,limit=1] run function rpg:daath_fight/reflect/mark
execute if score @s rpg_dt_t matches 50 run function rpg:daath_fight/reflect/spike
execute if score @s rpg_dt_t matches 70 run execute at @a[tag=rpg.dt.me,limit=1] run function rpg:daath_fight/reflect/mark
execute if score @s rpg_dt_t matches 84 run function rpg:daath_fight/reflect/spike
execute if score @s rpg_dt_t matches 100 run execute at @a[tag=rpg.dt.me,limit=1] run function rpg:daath_fight/reflect/mark
execute if score @s rpg_dt_t matches 114 run function rpg:daath_fight/reflect/spike
execute if score @s rpg_dt_t matches 126 run execute at @a[tag=rpg.dt.me,limit=1] run function rpg:daath_fight/reflect/mark
execute if score @s rpg_dt_t matches 140 run function rpg:daath_fight/reflect/spike
execute if score @s rpg_dt_t matches 164 run function rpg:daath_fight/reflect/out
