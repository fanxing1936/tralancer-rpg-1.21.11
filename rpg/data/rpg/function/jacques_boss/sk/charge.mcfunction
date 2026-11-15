execute if score @s rpg_jq_t matches 6 run function rpg:jacques/anim/enter/roll_f
execute if score @s rpg_jq_t matches 6..16 unless entity @e[tag=rpg.unit.f,distance=..1.6] if block ^ ^0.5 ^0.9 #minecraft:replaceable if block ^ ^1.5 ^0.9 #minecraft:replaceable run tp @s ^ ^ ^0.7
execute if score @s rpg_jq_t matches 6..16 run particle minecraft:cloud ~ ~0.1 ~ 0.2 0 0.2 0.01 2
execute if score @s rpg_jq_t matches 6..16 run particle minecraft:dust_color_transition{from_color:[1.0,0.86,0.45],to_color:[1.0,0.97,0.85],scale:1.3} ~ ~0.9 ~ 0.3 0.5 0.3 0 4
execute if score @s rpg_jq_t matches 6..16 run particle minecraft:electric_spark ~ ~0.6 ~ 0.3 0.3 0.3 0.05 2
execute if score @s rpg_jq_t matches 17 run execute facing entity @e[tag=rpg.unit.f,distance=..6,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_jq_t matches 17 run function rpg:jacques/anim/enter/slash1
execute if score @s rpg_jq_t matches 24 run function rpg:jacques_boss/strike/charge
execute if score @s rpg_jq_t matches 36.. run function rpg:jacques_boss/sk/end
