# 切到 whirlwind 并立即播放第一帧。
scoreboard players set @s rpg_pp_anim 8
scoreboard players set @s rpg_pp_t 0
execute at @s run playsound rpg:pope.whirlwind hostile @a[distance=..24] ~ ~ ~ 1 1
return run function rpg:pope/anim/whirlwind/tick
