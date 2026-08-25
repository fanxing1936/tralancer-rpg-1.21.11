# 黑式破敌。
scoreboard players set @s rpg_pen_mode 1
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:squid_ink ~ ~1 ~ 0.35 0.45 0.35 0.08 18 force
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:weakness 3 1 true
damage @e[tag=rpg.legacy.target,limit=1] 3 minecraft:magic by @s
playsound minecraft:entity.squid.squirt player @s ~ ~ ~ 0.7 0.65
function rpg:hud/m9
