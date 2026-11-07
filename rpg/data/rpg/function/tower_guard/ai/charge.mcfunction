# 直线推进；胸口以上被挡住算撞墙，只有脚下一格就迈上去。
scoreboard players add @s rpg_tg_ta 1
execute if score @s rpg_tg_ta matches 40.. run return run function rpg:tower_guard/ai/charge_stop
execute positioned ^ ^ ^1 if entity @a[distance=..1.7,gamemode=!spectator,gamemode=!creative] run return run function rpg:tower_guard/ai/charge_hit
execute positioned ^ ^ ^0.9 unless block ~ ~1.2 ~ #minecraft:replaceable run return run function rpg:tower_guard/ai/charge_crash
execute positioned ^ ^ ^0.9 unless block ~ ~0.2 ~ #minecraft:replaceable run return run tp @s ^ ^1 ^0.5
tp @s ^ ^ ^0.5
execute at @s if block ~ ~-0.1 ~ #minecraft:replaceable run tp @s ~ ~-0.5 ~
