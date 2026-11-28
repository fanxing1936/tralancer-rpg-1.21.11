# 载体没走完结尾就死了（as/at 战场中心）：收掉没了坐骑的部件和守望者，在最后的位置放死亡特效
tag @e[tag=rpg.mkm.part,predicate=!rpg:in_prologue] add rpg.mkb.orph
execute as @e[tag=rpg.mkm,predicate=!rpg:in_prologue] on passengers run tag @s remove rpg.mkb.orph
kill @e[tag=rpg.mkb.orph,predicate=!rpg:in_prologue]
execute as @e[type=minecraft:vindicator,tag=rpg.mkb.w,predicate=!rpg:in_prologue] run function rpg:michael_boss/watch/die
kill @e[tag=rpg.mkb.fx,tag=!rpg.mkb.pillar,predicate=!rpg:in_prologue]
bossbar set rpg:michael_boss value 0
scoreboard players set #ghost rpg_mk 1
