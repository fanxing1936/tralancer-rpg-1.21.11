# 召唤后直接打到一阶段底线，走正常的甲碎进入二阶段。
function rpg:saul_boss/summon
tag @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1,sort=nearest] add rpg.slb.hp
execute as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1,sort=nearest] run function rpg:saul_boss/refill
execute as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1,sort=nearest] run data merge entity @s {Health:1f}
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1,sort=nearest] rpg_sl_h 1
