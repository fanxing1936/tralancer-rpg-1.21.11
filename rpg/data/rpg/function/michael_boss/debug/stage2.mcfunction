# 召唤后直接打到一阶段底线，走正常的骨中之骨进入二阶段。
function rpg:michael_boss/summon
tag @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,sort=nearest] add rpg.mkb.hp
execute as @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,sort=nearest] run function rpg:michael_boss/refill
execute as @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,sort=nearest] run data merge entity @s {Health:1f}
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,sort=nearest] rpg_mk_h 1
