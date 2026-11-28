# 收场：怪、道具、标记都清掉；安全区恢复
execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c] if score @s rpg_tw_id = #run rpg_te run scoreboard players set @s rpg_tw_ev 0
execute in minecraft:overworld as @e[tag=rpg.tw.ev] run function rpg:town/ev/remove
bossbar set rpg:town_ev visible false
tag @a remove rpg.tw.in
tag @a remove rpg.te.cut
scoreboard players set #run rpg_te 0
