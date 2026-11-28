execute if score @s rpg_mk_t matches 10 run execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,predicate=!rpg:in_prologue] run function rpg:michael_boss/watch/spawn
execute if score @s rpg_mk_t matches 10 run execute store result score #w rpg_mk if entity @e[type=minecraft:vindicator,tag=rpg.mkb.w,predicate=!rpg:in_prologue]
execute if score @s rpg_mk_t matches 11 run execute if score @s rpg_mk matches 1 if score #w rpg_mk matches ..1 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,predicate=!rpg:in_prologue] run function rpg:michael_boss/watch/spawn
execute if score @s rpg_mk_t matches 11 run execute if score @s rpg_mk matches 2 if score #w rpg_mk matches ..2 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,predicate=!rpg:in_prologue] run function rpg:michael_boss/watch/spawn
execute if score @s rpg_mk_t matches 33.. run function rpg:michael_boss/sk/end
