execute if score @s rpg_sl_t matches 1..13 run execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_sl_t matches 1..13 run particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ^ ^1.3 ^0.6 0.6 0.6 0.6 0 3
execute if score @s rpg_sl_t matches 6 run function rpg:saul_boss/vfx/gather
execute if score @s rpg_sl_t matches 14 run function rpg:saul_boss/flash/go
execute if score @s rpg_sl_t matches 15 run function rpg:saul/anim/enter/final
execute if score @s rpg_sl_t matches 18 run execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_sl_t matches 24 run function rpg:saul_boss/flash/cut
execute if score @s rpg_sl_t matches 40.. run function rpg:saul_boss/sk/end
