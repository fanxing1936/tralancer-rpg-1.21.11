# 部件不再骑着载体：载体死亡动画播完被移除了（其他移除路径都先杀乘客）。
execute as @e[type=minecraft:item_display,tag=rpg.sml.p.l_leg,predicate=!rpg:samael_lord/riding] at @s run function rpg:samael_lord/death
kill @e[type=minecraft:item_display,tag=rpg.sml.part,predicate=!rpg:samael_lord/riding]
