# 残影冲一步（as/at 它）：每刻 2 格，碰到的人记下
tp @s ^ ^ ^2
execute at @s run tag @e[tag=rpg.unit.f,distance=..1.4] add rpg.slb.hit
execute at @s run particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~ ~1 ~ 0.3 0.5 0.3 0 6 force
execute at @s run particle minecraft:sweep_attack ~ ~1 ~ 0.3 0.3 0.3 0 1
