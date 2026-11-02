# 切到 walk 并立即播放第一帧。
scoreboard players set @s rpg_bz_anim 1
scoreboard players set @s rpg_bz_t 0
return run function rpg:beelzebub/anim/walk/tick
