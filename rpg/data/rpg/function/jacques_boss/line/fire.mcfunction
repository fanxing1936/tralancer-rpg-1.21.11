# 火墙（沿墙走一遍）：粒子，碰到的人记下
tag @e[tag=rpg.unit.f,distance=..1.1] add rpg.jqb.hit
particle minecraft:flame ~ ~0.6 ~ 0.25 0.6 0.25 0.02 4
particle minecraft:small_flame ~ ~1.6 ~ 0.2 0.5 0.2 0.01 2
particle minecraft:dust_color_transition{from_color:[1.0,0.62,0.2],to_color:[0.35,0.04,0.0],scale:1.4} ~ ~1.2 ~ 0.2 0.6 0.2 0 1
scoreboard players remove #d rpg_jq 1
execute if score #d rpg_jq matches 1.. positioned ^ ^ ^1.3 run function rpg:jacques_boss/line/fire
