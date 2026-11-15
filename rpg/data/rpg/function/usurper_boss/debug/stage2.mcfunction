# 召唤后直接打到一阶段底线，走正常的变身进入二阶段。
function rpg:usurper_boss/summon
tag @e[type=minecraft:vindicator,tag=rpg.usb,limit=1,sort=nearest] add rpg.usb.hp
execute as @e[type=minecraft:vindicator,tag=rpg.usb,limit=1,sort=nearest] run function rpg:usurper_boss/refill
execute as @e[type=minecraft:vindicator,tag=rpg.usb,limit=1,sort=nearest] run data merge entity @s {Health:1f}
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.usb,limit=1,sort=nearest] rpg_ub_h 1
