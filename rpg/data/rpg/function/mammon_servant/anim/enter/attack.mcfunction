# 切到 attack 并立即播放第一帧。
scoreboard players set @s rpg_mms_anim 2
scoreboard players set @s rpg_mms_t 0
return run function rpg:mammon_servant/anim/attack/tick
