# 部件不再骑着载体：载体死亡动画播完被移除了（其他移除路径都先杀乘客）。
execute as @e[type=minecraft:item_display,tag=rpg.sk.p.body,predicate=!rpg:sunken_skeleton/riding] at @s run function rpg:sunken_skeleton/death
kill @e[type=minecraft:item_display,tag=rpg.sk.part,predicate=!rpg:sunken_skeleton/riding]
