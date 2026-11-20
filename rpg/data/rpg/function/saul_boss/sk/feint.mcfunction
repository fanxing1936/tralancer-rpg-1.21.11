execute if score @s rpg_sl_t matches 2..10 run function rpg:saul_boss/lunge/step
tag @e[tag=rpg.unit] remove rpg.slb.hit
execute if score @s rpg_sl_t matches 11 run function rpg:saul_boss/strike/feint
execute if score @s rpg_sl_t matches 14 run attribute @s minecraft:armor base set 0
execute if score @s rpg_sl_t matches 14 run function rpg:saul/anim/enter/stun
execute if score @s rpg_sl_t matches 14..44 run particle minecraft:end_rod ~ ~2.15 ~ 0.2 0.05 0.2 0.01 1
execute if score @s rpg_sl_t matches 44.. run function rpg:saul_boss/stagger/end
