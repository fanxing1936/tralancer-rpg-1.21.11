
# 严寒风暴／极寒之镰：寒意只落到本次受击者。
effect give @e[tag=rpg.legacy.advanced_target,limit=1] slowness 2 4 true
damage @e[tag=rpg.legacy.advanced_target,limit=1] 2 minecraft:freeze by @s
particle dust_color_transition{from_color:[0.58,0.92,1.0],to_color:[1.0,1.0,1.0],scale:3} ~ ~1 ~ 0.6 0.6 0.6 0.08 18
scoreboard players reset @s ice
