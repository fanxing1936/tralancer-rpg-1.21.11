# 部件不再骑着载体：载体死亡动画播完被移除了（其他移除路径都先杀乘客）。
execute as @e[type=minecraft:item_display,tag=rpg.tw.p.body,predicate=!rpg:tower_wraith/riding] at @s run function rpg:tower_wraith/death
kill @e[type=minecraft:item_display,tag=rpg.tw.part,predicate=!rpg:tower_wraith/riding]
