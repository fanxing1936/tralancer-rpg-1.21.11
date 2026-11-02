# 切到 charge 并立即播放第一帧。
scoreboard players set @s rpg_tg_anim 3
scoreboard players set @s rpg_tg_t 0
execute at @s run playsound rpg:tower_guard.charge hostile @a[distance=..24] ~ ~ ~ 1 1
return run function rpg:tower_guard/anim/charge/tick
