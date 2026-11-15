execute if score @s rpg_jq_t matches 4 run function rpg:jacques/weapon/harp2
execute if score @s rpg_jq_t matches 8 run function rpg:jacques/weapon/harp3
execute if score @s rpg_jq_t matches 12 run function rpg:jacques/weapon/harp4
execute if score @s rpg_jq_t matches 14 run execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_jq_t matches 14 run particle minecraft:end_rod ~ ~1.4 ~ 0.3 0.3 0.3 0.02 10
execute if score @s rpg_jq_t matches 2 run function rpg:jacques_boss/vfx/volley_charge
execute if score @s rpg_jq_t matches 2..18 run particle minecraft:enchant ~ ~1.5 ~ 0.8 0.8 0.8 1 6
execute if score @s rpg_jq_t matches 20 run function rpg:jacques/anim/enter/shoot
execute if score @s rpg_jq_t matches 20 run function rpg:jacques_boss/volley/fire
execute if score @s rpg_jq_t matches 22 run function rpg:jacques/weapon/harp1
execute if score @s rpg_jq_t matches 32.. run function rpg:jacques_boss/sk/end
