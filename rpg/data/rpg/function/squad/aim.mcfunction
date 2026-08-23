# 指着谁打谁。先把上一个目标摘掉，再沿视线找第一个挡路的东西。
execute as @e[tag=rpg.sq.aim] if score @s rpg_sq_aim = #sq rpg_squad run function rpg:squad/unaim
execute at @s anchored eyes run function rpg:squad/ray
