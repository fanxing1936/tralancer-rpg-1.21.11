# 切到 stun 并立即播放第一帧。
scoreboard players set @s rpg_tg_anim 7
scoreboard players set @s rpg_tg_t 0
execute at @s run playsound rpg:tower_guard.stun hostile @a[distance=..24] ~ ~ ~ 1 1
return run function rpg:tower_guard/anim/stun/tick
