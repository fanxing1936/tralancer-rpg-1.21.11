tp @s ^ ^ ^1
execute positioned ~ ~-0.9 ~ if entity @e[tag=rpg.unit.f,distance=..1.2] run return run function rpg:jacques_boss/fx/arrow_hit
execute unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:jacques_boss/fx/arrow_end
particle minecraft:end_rod ^ ^ ^-0.6 0 0 0 0 1
execute if entity @s[tag=!rpg.jqb.af] run particle minecraft:electric_spark ^ ^ ^-0.3 0.03 0.03 0.03 0.02 1
execute if entity @s[tag=!rpg.jqb.af] run particle minecraft:dust_color_transition{from_color:[1.0,0.86,0.45],to_color:[1.0,0.97,0.85],scale:1.3} ^ ^ ^-0.9 0 0 0 0 1
execute if entity @s[tag=rpg.jqb.af] run particle minecraft:flame ^ ^ ^-0.6 0.02 0.02 0.02 0.01 2
execute if entity @s[tag=rpg.jqb.af] run particle minecraft:dust_color_transition{from_color:[1.0,0.62,0.2],to_color:[0.35,0.04,0.0],scale:1.4} ^ ^ ^-1 0 0 0 0 1
