# 部件不再骑着载体：载体死亡动画播完被移除了（其他移除路径都先杀乘客）。
execute as @e[type=minecraft:item_display,tag=rpg.usm.p.r_leg,predicate=!rpg:usurper/riding] at @s run function rpg:usurper/death
kill @e[type=minecraft:item_display,tag=rpg.usm.part,predicate=!rpg:usurper/riding]
