# 部件不再骑着载体：载体死亡动画播完被移除了（其他移除路径都先杀乘客）。
execute as @e[type=minecraft:item_display,tag=rpg.ei.p.leftleg,predicate=!rpg:end_illager/riding] at @s run function rpg:end_illager/death
kill @e[type=minecraft:item_display,tag=rpg.ei.part,predicate=!rpg:end_illager/riding]
