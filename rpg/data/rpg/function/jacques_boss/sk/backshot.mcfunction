execute if score @s rpg_jq_t matches 1..9 if block ^ ^0.5 ^-0.9 #minecraft:replaceable if block ^ ^1.5 ^-0.9 #minecraft:replaceable run tp @s ^ ^ ^-0.55
execute if score @s rpg_jq_t matches 1..9 run particle minecraft:cloud ~ ~0.1 ~ 0.2 0 0.2 0.01 2
execute if score @s rpg_jq_t matches 10 run function rpg:jacques/weapon/harp4
execute if score @s rpg_jq_t matches 10 run execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_jq_t matches 14 run function rpg:jacques/anim/enter/shoot
execute if score @s rpg_jq_t matches 14 run execute positioned ~ ~1.45 ~ facing entity @e[tag=rpg.unit.f,distance=..27,sort=nearest,limit=1] eyes positioned ^ ^ ^0.9 run function rpg:jacques_boss/arrow/a6
execute if score @s rpg_jq_t matches 16 run function rpg:jacques/weapon/harp1
execute if score @s rpg_jq_t matches 28.. run function rpg:jacques_boss/sk/end
