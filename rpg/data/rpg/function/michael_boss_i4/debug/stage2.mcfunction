# 召唤后直接打到一阶段底线，走正常的骨中之骨进入二阶段。
function rpg:michael_boss_i4/summon
tag @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,sort=nearest,distance=0..] add rpg.mkb.hp
execute as @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,sort=nearest,distance=0..] run function rpg:michael_boss_i4/refill
execute as @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,sort=nearest,distance=0..] run data merge entity @s {Health:1f}
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,sort=nearest,distance=0..] rpg_mk_h 1
