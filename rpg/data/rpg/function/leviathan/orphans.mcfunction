# 部件不再骑着载体：载体死亡动画播完被移除了（其他移除路径都先杀乘客）。
execute as @e[type=minecraft:item_display,tag=rpg.lv.p.body,predicate=!rpg:leviathan/riding] at @s run function rpg:leviathan/death
kill @e[type=minecraft:item_display,tag=rpg.lv.part,predicate=!rpg:leviathan/riding]
