# 部件不再骑着载体：载体死亡动画播完被移除了（其他移除路径都先杀乘客）。
execute as @e[type=minecraft:item_display,tag=rpg.ab.p.body,predicate=!rpg:abaddon/riding] at @s run function rpg:abaddon/death
kill @e[type=minecraft:item_display,tag=rpg.ab.part,predicate=!rpg:abaddon/riding]
