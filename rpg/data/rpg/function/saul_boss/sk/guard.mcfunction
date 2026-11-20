scoreboard players operation #m rpg_sl = @s rpg_sl_t
scoreboard players set #k rpg_sl 4
scoreboard players operation #m rpg_sl %= #k rpg_sl
execute if score #m rpg_sl matches 0 run particle minecraft:end_rod ^0.3 ^1.5 ^0.6 0.05 0.25 0.05 0 2
execute if score #m rpg_sl matches 2 run particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ^ ^1.5 ^0.7 0.2 0.3 0.1 0 2
execute if score @s rpg_sl_t matches 2 run function rpg:saul_boss/vfx/guard
execute if score @s rpg_sl_t matches 30.. run function rpg:saul_boss/sk/end
