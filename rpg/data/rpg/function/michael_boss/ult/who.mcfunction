scoreboard players set @s rpg_mk_sk 14
scoreboard players set @s rpg_mk_t 0
scoreboard players set @s rpg_mk_busy 178
data merge entity @s {NoAI:1b}
tp @s @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,predicate=!rpg:in_prologue]
execute at @s run function rpg:michael_boss/who/begin
