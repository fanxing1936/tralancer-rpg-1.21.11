# 剧毒之牙 · 淬毒：毒层属于攻击者，不会被另一名玩家重置或偷走。
scoreboard players set @s rpg_leg_cd 5
scoreboard players add @s rpg_venom 1
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:dust_color_transition{from_color:[0.18,0.55,0.04],to_color:[0.72,0.95,0.16],scale:1.1} ~ ~1 ~ 0.35 0.45 0.35 0.06 12 force
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:poison 3 0 true
playsound minecraft:entity.spider.hurt player @s ~ ~ ~ 0.55 1.35
execute if entity @s[scores={rpg_venom=3..}] run function rpg:item/legacy/venom_burst
