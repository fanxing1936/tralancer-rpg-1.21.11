scoreboard players remove @s rpg_dt_blade 1
execute on passengers if entity @s[tag=rpg.dtm.p.weapon_r] run particle minecraft:smoke ~ ~ ~ 0.2 0.3 0.2 0.01 1
particle minecraft:dust_color_transition{from_color:[0.29,0.31,0.36],to_color:[0.04,0.05,0.06],scale:1.3} ^-0.4 ^1.1 ^0.6 0.2 0.3 0.2 0 1
