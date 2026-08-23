# 朝目标走一步，同样按编号错开，免得四个人叠在目标同一侧。
tp @s ~ ~ ~ facing entity @e[tag=rpg.sq.mark,limit=1,sort=nearest,distance=..128]
execute at @s rotated ~28 0 run function rpg:squad/step
