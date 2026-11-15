# 部件不再骑着载体：载体死亡动画播完被移除了（其他移除路径都先杀乘客）。
execute as @e[type=minecraft:item_display,tag=rpg.mms.p.l_arm,predicate=!rpg:mammon_servant/riding] at @s run function rpg:mammon_servant/death
kill @e[type=minecraft:item_display,tag=rpg.mms.part,predicate=!rpg:mammon_servant/riding]
