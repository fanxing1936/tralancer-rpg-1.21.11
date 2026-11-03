scoreboard players remove @s rpg_mi_fuse 1
particle dust_color_transition{from_color:[1.0,0.2,0.0],to_color:[0.3,0.06,0.0],scale:1.4} ~ ~1 ~ 0.3 0.4 0.3 0.01 2
execute if score @s rpg_mi_fuse matches ..0 run function rpg:item/extra/michael_ignite_hit
