# 白式回生。
scoreboard players set @s rpg_pen_mode 0
execute at @s run particle minecraft:cloud ~ ~1 ~ 0.3 0.45 0.3 0.03 15 force
effect give @s minecraft:instant_health 1 0 true
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:glowing 2 0 true
playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 0.7 1.6
function rpg:hud/m10
