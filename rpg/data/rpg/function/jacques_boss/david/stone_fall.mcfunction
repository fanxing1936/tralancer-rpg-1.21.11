# 石子从高处落向他（as 石子）
data merge entity @s {teleport_duration:18}
execute at @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,limit=1] run tp @s ~ ~1.7 ~
