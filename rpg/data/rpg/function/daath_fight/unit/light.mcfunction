# 灯下显形（as/at 影子）
execute if entity @s[tag=!rpg.dt.lit] if entity @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..6.2] run function rpg:daath_fight/unit/lit_on
execute if entity @s[tag=rpg.dt.lit] unless entity @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..6.6] run function rpg:daath_fight/unit/lit_off
execute if entity @s[tag=rpg.dt.lit] run particle minecraft:end_rod ~ ~1 ~ 0.35 0.7 0.35 0.01 1
execute if score @s rpg_dt_st matches 1 if entity @s[tag=!rpg.dt.lit] run particle minecraft:smoke ~ ~0.9 ~ 0.35 0.6 0.35 0.01 1
execute if score @s rpg_dt_sw matches 1.. run particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ^-0.4 ^1.2 ^0.5 0.15 0.2 0.15 0 1
execute if score @s rpg_dt_sa matches 1.. run particle minecraft:wax_off ~ ~1 ~ 0.4 0.6 0.4 0 1
