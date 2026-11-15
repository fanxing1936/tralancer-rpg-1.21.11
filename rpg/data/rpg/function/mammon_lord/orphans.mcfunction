# 部件不再骑着载体：载体死亡动画播完被移除了（其他移除路径都先杀乘客）。
execute as @e[type=minecraft:item_display,tag=rpg.mml.p.l_leg,predicate=!rpg:mammon_lord/riding] at @s run function rpg:mammon_lord/death
kill @e[type=minecraft:item_display,tag=rpg.mml.part,predicate=!rpg:mammon_lord/riding]
