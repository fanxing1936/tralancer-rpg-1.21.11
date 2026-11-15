# 切到 walk 并立即播放第一帧。
scoreboard players set @s rpg_mms_anim 1
scoreboard players set @s rpg_mms_t 0
return run function rpg:mammon_servant/anim/walk/tick
