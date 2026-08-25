
# 两把珊瑚斧共用潮蚀被动，目标固定为本次受击者。
effect give @e[tag=rpg.legacy.advanced_target,limit=1] wither 2 2 true
effect give @e[tag=rpg.legacy.advanced_target,limit=1] glowing 2 0 true
particle dust_color_transition{from_color:[1.0,0.38,0.92],to_color:[1.0,0.78,0.0],scale:3} ~ ~1 ~ 0.6 0.6 0.6 0.08 18
scoreboard players reset @s sea
