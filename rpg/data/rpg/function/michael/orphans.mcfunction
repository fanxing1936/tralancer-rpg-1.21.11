# 部件不再骑着载体：载体死亡动画播完被移除了（其他移除路径都先杀乘客）。
execute as @e[type=minecraft:item_display,tag=rpg.mkm.p.head,predicate=!rpg:michael/riding] at @s run function rpg:michael/death
kill @e[type=minecraft:item_display,tag=rpg.mkm.part,predicate=!rpg:michael/riding]
