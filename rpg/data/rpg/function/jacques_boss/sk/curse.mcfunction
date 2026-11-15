execute if score @s rpg_jq_t matches 8 run execute as @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] at @s run function rpg:jacques_boss/curse/mark
execute if score @s rpg_jq_t matches 4 run function rpg:jacques_boss/vfx/curse_cast
execute if score @s rpg_jq_t matches 22.. run function rpg:jacques_boss/sk/end
