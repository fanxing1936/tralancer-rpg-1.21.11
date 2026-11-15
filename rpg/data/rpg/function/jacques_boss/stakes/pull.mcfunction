# 整圈向中心收拢（柱子插值滑向圆心）
execute as @e[tag=rpg.jqb.stakev] run data merge entity @s {teleport_duration:15}
execute as @e[tag=rpg.jqb.stakev] at @e[type=minecraft:marker,tag=rpg.jqb.stakec,limit=1] run tp @s ~ ~ ~
tag @e[tag=rpg.jqb.stake] remove rpg.jqb.lit
kill @e[tag=rpg.jqb.wallv]
playsound minecraft:block.fire.ambient hostile @a[distance=..40] ~ ~ ~ 2 0.5
execute at @e[type=minecraft:marker,tag=rpg.jqb.stakec,limit=1] run function rpg:jacques_boss/stakes/pull_fx
