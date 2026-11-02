# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_bz_anim 0
scoreboard players set @s rpg_bz_t 0
return run function rpg:beelzebub/anim/idle/tick
