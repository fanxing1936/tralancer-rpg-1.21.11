execute if score @s rpg_sl_t matches 2 run execute as @e[type=minecraft:vindicator,tag=rpg.slg,distance=..4] run function rpg:saul_ghost/anim/enter/shadow
execute if score @s rpg_sl_t matches 2..60 as @e[type=minecraft:vindicator,tag=rpg.slg,distance=..4] at @s run particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~ ~1.2 ~ 0.3 0.6 0.3 0 1
execute if score @s rpg_sl_t matches 14 run playsound minecraft:item.shield.block hostile @a[distance=..20] ~ ~ ~ 0.5 1.6
execute if score @s rpg_sl_t matches 34 run playsound minecraft:item.shield.block hostile @a[distance=..20] ~ ~ ~ 0.5 1.4
execute if score @s rpg_sl_t matches 59.. run function rpg:saul_boss/sk/end
