# 部件不再骑着载体：载体死亡动画播完被移除了（其他移除路径都先杀乘客）。
execute as @e[type=minecraft:item_display,tag=rpg.mkwm.p.j_spine,predicate=!rpg:watchling/riding] at @s run function rpg:watchling/death
kill @e[type=minecraft:item_display,tag=rpg.mkwm.part,predicate=!rpg:watchling/riding]
