execute if score @s rpg_jq_t matches 4 run function rpg:jacques/weapon/harp2
execute if score @s rpg_jq_t matches 8 run function rpg:jacques/weapon/harp3
execute if score @s rpg_jq_t matches 12 run function rpg:jacques/weapon/harp4
execute if score @s rpg_jq_t matches 14 run execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_jq_t matches 16 run function rpg:jacques/anim/enter/shoot
execute if score @s rpg_jq_t matches 16 run function rpg:jacques_boss/vfx/muzzle
execute if score @s rpg_jq_t matches 16 run execute positioned ~ ~1.45 ~ facing entity @e[tag=rpg.unit.f,distance=..27,sort=nearest,limit=1] eyes positioned ^ ^ ^0.9 run function rpg:jacques_boss/arrow/a5
execute if score @s rpg_jq_t matches 18 run function rpg:jacques/weapon/harp1
execute if score @s rpg_jq_t matches 24.. run function rpg:jacques_boss/sk/end
