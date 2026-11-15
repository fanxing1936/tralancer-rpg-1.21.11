execute if score @s rpg_jq_t matches 8 at @e[tag=rpg.unit.f,distance=..25,sort=random,limit=1] run function rpg:jacques_boss/leap/mark
execute if score @s rpg_jq_t matches 8 unless entity @e[type=minecraft:marker,tag=rpg.jqb.land] run function rpg:jacques_boss/leap/mark
execute if score @s rpg_jq_t matches 12 run data merge entity @s {Invulnerable:1b,NoGravity:1b}
execute if score @s rpg_jq_t matches 12 run particle minecraft:flame ~ ~0.5 ~ 0.4 0.2 0.4 0.1 30
execute if score @s rpg_jq_t matches 12 run function rpg:jacques_boss/vfx/takeoff
execute if score @s rpg_jq_t matches 23 at @e[type=minecraft:marker,tag=rpg.jqb.land,limit=1] run function rpg:jacques_boss/vfx/meteor
execute if score @s rpg_jq_t matches 12 run tp @s ~ ~14 ~
execute if score @s rpg_jq_t matches 28 at @e[type=minecraft:marker,tag=rpg.jqb.land,limit=1] run tp @s ~ ~ ~
execute if score @s rpg_jq_t matches 28 run function rpg:jacques/anim/enter/land
execute if score @s rpg_jq_t matches 29 at @s run function rpg:jacques_boss/leap/land
execute if score @s rpg_jq_t matches 52.. run function rpg:jacques_boss/sk/end
