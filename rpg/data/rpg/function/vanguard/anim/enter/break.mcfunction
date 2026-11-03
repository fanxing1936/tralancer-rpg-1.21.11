# 切到 break 并立即播放第一帧。
scoreboard players set @s rpg_vg_anim 3
scoreboard players set @s rpg_vg_t 0
execute at @s run playsound rpg:vanguard.shield_break hostile @a[distance=..24] ~ ~ ~ 1 1
return run function rpg:vanguard/anim/break/tick
