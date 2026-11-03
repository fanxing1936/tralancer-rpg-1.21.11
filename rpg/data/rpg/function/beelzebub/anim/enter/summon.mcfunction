# 切到 summon 并立即播放第一帧。
scoreboard players set @s rpg_bz_anim 3
scoreboard players set @s rpg_bz_t 0
execute at @s run playsound rpg:beelzebub.load_long hostile @a[distance=..24] ~ ~ ~ 1 1
return run function rpg:beelzebub/anim/summon/tick
