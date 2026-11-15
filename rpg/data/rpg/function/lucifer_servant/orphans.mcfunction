# 部件不再骑着载体：载体死亡动画播完被移除了（其他移除路径都先杀乘客）。
execute as @e[type=minecraft:item_display,tag=rpg.lcs.p.r_leg,predicate=!rpg:lucifer_servant/riding] at @s run function rpg:lucifer_servant/death
kill @e[type=minecraft:item_display,tag=rpg.lcs.part,predicate=!rpg:lucifer_servant/riding]
