# 部件不再骑着载体：载体死亡动画播完被移除了（其他移除路径都先杀乘客）。
execute as @e[type=minecraft:item_display,tag=rpg.tg.p.body,predicate=!rpg:tower_guard/riding] at @s run function rpg:tower_guard/death
kill @e[type=minecraft:item_display,tag=rpg.tg.part,predicate=!rpg:tower_guard/riding]
