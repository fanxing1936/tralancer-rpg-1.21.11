# 切到 spread 并立即播放第一帧。
scoreboard players set @s rpg_ab_anim 3
scoreboard players set @s rpg_ab_t 0
execute at @s run playsound rpg:abaddon.circle_vocal hostile @a[distance=..24] ~ ~ ~ 1.2 1
return run function rpg:abaddon/anim/spread/tick
