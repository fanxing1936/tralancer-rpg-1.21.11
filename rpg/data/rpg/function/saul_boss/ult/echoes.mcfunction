scoreboard players set @s rpg_sl_sk 22
scoreboard players set @s rpg_sl_t 0
scoreboard players set @s rpg_sl_busy 168
data merge entity @s {NoAI:1b}
tp @s @e[type=minecraft:marker,tag=rpg.slb.center,limit=1]
execute at @s run function rpg:saul_boss/echoes/begin
