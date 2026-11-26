# 找对了：其余立刻散掉
tag @s remove rpg.dt.found
tag @s remove rpg.dt.seek
execute as @e[type=minecraft:item_display,tag=rpg.dt.ten,distance=..60] at @s run particle minecraft:smoke ~ ~1 ~ 0.3 0.6 0.3 0.02 10
kill @e[type=minecraft:item_display,tag=rpg.dt.ten,distance=..60]
scoreboard players set #s rpg_dt 60
function rpg:daath_fight/stun
playsound minecraft:block.glass.break hostile @a[distance=..48] ~ ~ ~ 1.4 1
