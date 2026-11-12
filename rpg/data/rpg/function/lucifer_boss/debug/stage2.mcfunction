# 召唤后直接打到一阶段底线，走正常的变身演出进入二阶段。
function rpg:lucifer_boss/summon
# 先补满（含死亡保护），再把血量压到底线，下一次读血就走正常的变身。
tag @e[type=minecraft:vindicator,tag=rpg.lub,limit=1,sort=nearest] add rpg.lub.hp
execute as @e[type=minecraft:vindicator,tag=rpg.lub,limit=1,sort=nearest] run function rpg:lucifer_boss/refill
execute as @e[type=minecraft:vindicator,tag=rpg.lub,limit=1,sort=nearest] run data merge entity @s {Health:1f}
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.lub,limit=1,sort=nearest] rpg_lub_h 1
