# 石子先飞到他头顶上方（as 石子；召出后隔一刻再传送，客户端才会插值）
data merge entity @s {teleport_duration:18}
execute at @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,limit=1] run tp @s ~ ~5 ~
