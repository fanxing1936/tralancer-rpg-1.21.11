execute if score @s rpg_jq_t matches 40 if entity @e[tag=rpg.jqb.stone] run return run function rpg:jacques_boss/david/hit
execute if score @s rpg_jq_t matches 2 as @e[tag=rpg.jqb.stone] run function rpg:jacques_boss/david/stone_up
execute if score @s rpg_jq_t matches 20 as @e[tag=rpg.jqb.stone] run function rpg:jacques_boss/david/stone_fall
execute if score @s rpg_jq_t matches 4 run execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_jq_t matches 4 run particle minecraft:flame ~ ~0.2 ~ 0.5 0.05 0.5 0.05 16
execute if score @s rpg_jq_t matches 10 run function rpg:jacques_boss/vfx/dash_start
execute if score @s rpg_jq_t matches 4 run playsound minecraft:entity.horse.gallop hostile @a[distance=..24] ~ ~ ~ 1 0.7
execute if score @s rpg_jq_t matches 10 run function rpg:jacques/anim/enter/roll_f
execute if score @s rpg_jq_t matches 10 run tag @e[tag=rpg.unit] remove rpg.jqb.rolled
execute if score @s rpg_jq_t matches 10..20 run function rpg:jacques_boss/last/dash
execute if score @s rpg_jq_t matches 26 run execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_jq_t matches 26 run particle minecraft:flame ~ ~0.2 ~ 0.5 0.05 0.5 0.05 16
execute if score @s rpg_jq_t matches 32 run function rpg:jacques_boss/vfx/dash_start
execute if score @s rpg_jq_t matches 26 run playsound minecraft:entity.horse.gallop hostile @a[distance=..24] ~ ~ ~ 1 0.7
execute if score @s rpg_jq_t matches 32 run function rpg:jacques/anim/enter/roll_f
execute if score @s rpg_jq_t matches 32 run tag @e[tag=rpg.unit] remove rpg.jqb.rolled
execute if score @s rpg_jq_t matches 32..42 run function rpg:jacques_boss/last/dash
execute if score @s rpg_jq_t matches 48 run execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_jq_t matches 48 run particle minecraft:flame ~ ~0.2 ~ 0.5 0.05 0.5 0.05 16
execute if score @s rpg_jq_t matches 54 run function rpg:jacques_boss/vfx/dash_start
execute if score @s rpg_jq_t matches 48 run playsound minecraft:entity.horse.gallop hostile @a[distance=..24] ~ ~ ~ 1 0.7
execute if score @s rpg_jq_t matches 54 run function rpg:jacques/anim/enter/roll_f
execute if score @s rpg_jq_t matches 54 run tag @e[tag=rpg.unit] remove rpg.jqb.rolled
execute if score @s rpg_jq_t matches 54..64 run function rpg:jacques_boss/last/dash
execute if score @s rpg_jq_t matches 76 run execute facing entity @e[tag=rpg.unit.f,distance=..8,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_jq_t matches 76 run function rpg:jacques/anim/enter/sweep
execute if score @s rpg_jq_t matches 79 run function rpg:jacques_boss/last/sweep
execute if score @s rpg_jq_t matches 96.. run function rpg:jacques_boss/skill/stagger
