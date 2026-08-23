# 不受控的一次挥砍。打的是身边的非玩家生物 —— 多人服里不该由堕落
# 替你决定去打谁。归属仍然记在本人头上：命令是单线程执行的，
# 这个标签在别人眼里从来不存在。
tag @s add rpg.fall.cast
execute at @s as @e[distance=..4.5,limit=1,sort=random,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display,type=!minecraft:text_display,type=!minecraft:marker] at @s run function rpg:taint/swing
tag @s remove rpg.fall.cast
