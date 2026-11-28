scoreboard players set @s rpg_mk_sk 12
scoreboard players set @s rpg_mk_t 0
scoreboard players set @s rpg_mk_busy 36
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:michael/anim/enter/rib_slash5
execute if score #w rpg_mk_i3 matches 1.. at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] run execute rotated as @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..] rotated ~45 0 run function rpg:michael_boss_i3/cross/mark
execute if score #w rpg_mk_i3 matches ..0 at @e[type=minecraft:marker,tag=rpg.mkb.lag,limit=1,distance=0..] run execute rotated as @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..] rotated ~45 0 run function rpg:michael_boss_i3/cross/mark
