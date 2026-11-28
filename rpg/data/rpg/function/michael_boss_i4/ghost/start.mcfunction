# 载体没走完结尾就死了（as/at 战场中心）：收掉没了坐骑的部件和守望者，在最后的位置放死亡特效
tag @e[tag=rpg.mkm.part,distance=0..] add rpg.mkb.orph
execute as @e[tag=rpg.mkm,distance=0..] on passengers run tag @s remove rpg.mkb.orph
kill @e[tag=rpg.mkb.orph,distance=0..]
execute as @e[type=minecraft:vindicator,tag=rpg.mkb.w,distance=0..] run function rpg:michael_boss_i4/watch/die
kill @e[tag=rpg.mkb.fx,tag=!rpg.mkb.pillar,distance=0..]
bossbar set rpg:michael_boss_i4 value 0
scoreboard players set #ghost rpg_mk_i4 1
