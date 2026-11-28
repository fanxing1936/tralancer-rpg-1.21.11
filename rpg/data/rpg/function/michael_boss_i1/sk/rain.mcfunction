execute if score @s rpg_mk_t matches 4 run execute if score #w rpg_mk_i1 matches 1.. at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] run function rpg:michael_boss_i1/rain/spots
execute if score @s rpg_mk_t matches 4 run execute if score #w rpg_mk_i1 matches ..0 at @e[type=minecraft:marker,tag=rpg.mkb.lag,limit=1,distance=0..] run function rpg:michael_boss_i1/rain/spots
execute if score @s rpg_mk_t matches 43.. run function rpg:michael_boss_i1/sk/end
