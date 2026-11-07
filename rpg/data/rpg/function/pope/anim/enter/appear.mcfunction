# 切到 appear 并立即播放第一帧。
scoreboard players set @s rpg_pp_anim 5
scoreboard players set @s rpg_pp_t 0
execute at @s run playsound rpg:pope.appear hostile @a[distance=..24] ~ ~ ~ 1 1
return run function rpg:pope/anim/appear/tick
