# 切到 rib_idle 并立即播放第一帧。
scoreboard players set @s rpg_mkm_anim 6
scoreboard players set @s rpg_mkm_t 0
return run function rpg:michael/anim/rib_idle/tick
