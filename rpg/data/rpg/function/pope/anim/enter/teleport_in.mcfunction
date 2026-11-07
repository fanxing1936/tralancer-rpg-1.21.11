# 切到 teleport_in 并立即播放第一帧。
scoreboard players set @s rpg_pp_anim 6
scoreboard players set @s rpg_pp_t 0
execute at @s run playsound rpg:pope.mirror_in hostile @a[distance=..24] ~ ~ ~ 1 1
return run function rpg:pope/anim/teleport_in/tick
