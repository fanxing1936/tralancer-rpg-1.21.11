# 切到 rise 并立即播放第一帧。
scoreboard players set @s rpg_lv_anim 4
scoreboard players set @s rpg_lv_t 0
execute at @s run playsound rpg:leviathan.summoned hostile @a[distance=..24] ~ ~ ~ 1.2 0.7
return run function rpg:leviathan/anim/rise/tick
