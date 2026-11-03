# 切到 summon 并立即播放第一帧。
scoreboard players set @s rpg_lv_anim 3
scoreboard players set @s rpg_lv_t 0
execute at @s run playsound rpg:leviathan.prepare hostile @a[distance=..24] ~ ~ ~ 1 1
return run function rpg:leviathan/anim/summon/tick
