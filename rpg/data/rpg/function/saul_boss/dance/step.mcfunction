# 穿刺一步（as/at 他）：每刻 2 格；沿途留下一节剑痕（到最后一起斩开）
execute if block ^ ^0.5 ^2 #minecraft:replaceable if block ^ ^1.5 ^2 #minecraft:replaceable unless block ^ ^-0.5 ^2 #minecraft:replaceable run tp @s ^ ^ ^2
execute at @s run tag @e[tag=rpg.unit.f,distance=..1.4] add rpg.slb.hit
execute at @s run function rpg:saul_boss/dance/seg
execute at @s run particle minecraft:dust_color_transition{from_color:[0.85,0.25,0.3],to_color:[0.25,0.02,0.05],scale:1.2} ~ ~1 ~ 0.3 0.5 0.3 0 6 force
