# 第三次命中引爆蛇毒。
scoreboard players set @s rpg_venom 0
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:entity_effect{color:65280} ~ ~1 ~ 0.55 0.65 0.55 0.2 30 force
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:poison 5 1 true
damage @e[tag=rpg.legacy.target,limit=1] 5 minecraft:magic by @s
playsound minecraft:entity.breeze.death player @s ~ ~ ~ 0.75 1.7
function rpg:hud/m13
