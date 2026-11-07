# 加护：11 格内的圣卫减伤加速，教皇一瞬移就断。
effect give @e[type=minecraft:vindicator,tag=rpg.pf.unit,distance=..11] minecraft:resistance 10 1 true
effect give @e[type=minecraft:vindicator,tag=rpg.pf.unit,distance=..11] minecraft:speed 10 1 true
execute as @e[type=minecraft:vindicator,tag=rpg.pf.unit,distance=..11] at @s run function rpg:pope_fight/fx/seal_small
