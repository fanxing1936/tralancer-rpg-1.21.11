# 部件不再骑着载体：载体死亡动画播完被移除了（其他移除路径都先杀乘客）。
execute as @e[type=minecraft:item_display,tag=rpg.slm.p.head,predicate=!rpg:saul/riding] at @s run function rpg:saul/death
kill @e[type=minecraft:item_display,tag=rpg.slm.part,predicate=!rpg:saul/riding]
