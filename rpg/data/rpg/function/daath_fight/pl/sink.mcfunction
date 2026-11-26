particle minecraft:dust_color_transition{from_color:[0.29,0.31,0.36],to_color:[0.04,0.05,0.06],scale:1.3} ~ ~0.1 ~ 0.8 0.05 0.8 0 12
particle minecraft:squid_ink ~ ~0.2 ~ 0.5 0.1 0.5 0.02 4
execute if score @s rpg_dt_pt matches 20 run effect give @s minecraft:blindness 4 0 true
execute if score @s rpg_dt_pt matches 30 run playsound minecraft:ambient.underwater.loop.additions.rare player @s ~ ~ ~ 1 0.6
execute if score @s rpg_dt_pt matches 50.. run function rpg:daath_fight/pl/down
