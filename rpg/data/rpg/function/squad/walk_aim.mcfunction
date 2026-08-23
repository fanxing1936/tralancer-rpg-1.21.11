# 朝目标走一步。
tp @s ~ ~ ~ facing entity @e[tag=rpg.sq.mark,limit=1,sort=nearest,distance=..128]
execute at @s run function rpg:squad/step
