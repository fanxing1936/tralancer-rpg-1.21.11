# 切割链锯 · 血痂：稳定的一次追加切割；六刻闸门防止追加伤害递归触发。
scoreboard players set @s rpg_leg_cd 6
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:dust{color:[0.55,0.02,0.02],scale:1.4} ~ ~1 ~ 0.45 0.55 0.45 0.08 18 force
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:damage_indicator ~ ~1 ~ 0.3 0.4 0.3 0.1 8 force
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:weakness 2 0 true
damage @e[tag=rpg.legacy.target,limit=1] 2 minecraft:player_attack by @s
playsound minecraft:block.grindstone.use player @s ~ ~ ~ 0.65 1.35
function rpg:hud/m6
