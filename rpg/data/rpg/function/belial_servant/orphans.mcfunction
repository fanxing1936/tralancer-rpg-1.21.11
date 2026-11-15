# 部件不再骑着载体：载体死亡动画播完被移除了（其他移除路径都先杀乘客）。
execute as @e[type=minecraft:item_display,tag=rpg.bls.p.l_leg,predicate=!rpg:belial_servant/riding] at @s run function rpg:belial_servant/death
kill @e[type=minecraft:item_display,tag=rpg.bls.part,predicate=!rpg:belial_servant/riding]
