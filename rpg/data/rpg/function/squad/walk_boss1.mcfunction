# 朝雇主走一步 —— 但不是照直走。
#
# 先转向雇主（人一直看着他，这样才像跟班），再把**执行朝向**偏 28 度
# 迈那一步：人就会绕到侧面去，而不是和别人挤在同一条线上。
# 偏航只影响这一步的方向，不动实体自己的朝向 —— 不需要任何三角函数。
tp @s ~ ~ ~ facing entity @a[tag=rpg.sq.boss,limit=1]
execute at @s rotated ~28 0 run function rpg:squad/step
