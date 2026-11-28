execute if score @s rpg_mk_t matches 4 run execute if score #w rpg_mk matches 1.. at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] run function rpg:michael_boss/rain/spots
execute if score @s rpg_mk_t matches 4 run execute if score #w rpg_mk matches ..0 at @e[type=minecraft:marker,tag=rpg.mkb.lag,limit=1,predicate=!rpg:in_prologue] run function rpg:michael_boss/rain/spots
execute if score @s rpg_mk_t matches 43.. run function rpg:michael_boss/sk/end
