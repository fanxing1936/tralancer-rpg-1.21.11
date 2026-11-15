# 部件不再骑着载体：载体死亡动画播完被移除了（其他移除路径都先杀乘客）。
execute as @e[type=minecraft:item_display,tag=rpg.bll.p.cauldronupper,predicate=!rpg:belial_lord/riding] at @s run function rpg:belial_lord/death
kill @e[type=minecraft:item_display,tag=rpg.bll.part,predicate=!rpg:belial_lord/riding]
