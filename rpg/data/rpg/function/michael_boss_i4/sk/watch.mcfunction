execute if score @s rpg_mk_t matches 10 run execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] run function rpg:michael_boss_i4/watch/spawn
execute if score @s rpg_mk_t matches 10 run execute store result score #w rpg_mk_i4 if entity @e[type=minecraft:vindicator,tag=rpg.mkb.w,distance=0..]
execute if score @s rpg_mk_t matches 11 run execute if score @s rpg_mk_i4 matches 1 if score #w rpg_mk_i4 matches ..1 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] run function rpg:michael_boss_i4/watch/spawn
execute if score @s rpg_mk_t matches 11 run execute if score @s rpg_mk_i4 matches 2 if score #w rpg_mk_i4 matches ..2 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] run function rpg:michael_boss_i4/watch/spawn
execute if score @s rpg_mk_t matches 33.. run function rpg:michael_boss_i4/sk/end
