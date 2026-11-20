# 点燃（as 玩家）：0.5 秒的引信
scoreboard players set @s rpg_mk_fl 0
scoreboard players set @s rpg_mk_fu 10
title @s actionbar [{"text":"圣焰 ","color":"#FF805F"},{"text":"● ● ●","color":"#FF3300","bold":true}]
playsound minecraft:item.firecharge.use hostile @a[distance=..24] ~ ~ ~ 1 0.8
