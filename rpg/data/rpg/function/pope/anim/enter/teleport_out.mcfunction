# 切到 teleport_out 并立即播放第一帧。
scoreboard players set @s rpg_pp_anim 7
scoreboard players set @s rpg_pp_t 0
execute at @s run playsound rpg:pope.mirror_out hostile @a[distance=..24] ~ ~ ~ 1 1
return run function rpg:pope/anim/teleport_out/tick
