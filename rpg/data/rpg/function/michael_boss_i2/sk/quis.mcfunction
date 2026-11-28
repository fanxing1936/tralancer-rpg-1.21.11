execute if score @s rpg_mk_t matches 1..16 run execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_mk_t matches 1..16 run execute as @e[tag=rpg.mkb.quiswarn,distance=..2] positioned as @s rotated as @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..] run tp @s ~ ~ ~ ~ ~
execute if score @s rpg_mk_t matches 1..18 run particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ^ ^2.4 ^0.3 0.15 0.4 0.15 0 2
execute if score @s rpg_mk_t matches 20 run function rpg:michael/anim/enter/slash1
execute if score @s rpg_mk_t matches 1 run function rpg:michael_boss_i2/quis/charge
execute if score @s rpg_mk_t matches 21 run function rpg:michael_boss_i2/quis/slam
execute if score @s rpg_mk_t matches 22 run execute rotated ~ 0 run function rpg:michael_boss_i2/quis/walker
execute if score @s rpg_mk_t matches 42.. run function rpg:michael_boss_i2/sk/end
