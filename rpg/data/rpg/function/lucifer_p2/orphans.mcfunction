# 部件不再骑着载体：载体死亡动画播完被移除了（其他移除路径都先杀乘客）。
execute as @e[type=minecraft:item_display,tag=rpg.lu2.p.p2_j_l_elbow_000,predicate=!rpg:lucifer_p2/riding] at @s run function rpg:lucifer_p2/death
kill @e[type=minecraft:item_display,tag=rpg.lu2.part,predicate=!rpg:lucifer_p2/riding]
