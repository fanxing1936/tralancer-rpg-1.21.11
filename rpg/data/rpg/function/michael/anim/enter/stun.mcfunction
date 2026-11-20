# 切到 stun 并立即播放第一帧。
scoreboard players set @s rpg_mkm_anim 29
scoreboard players set @s rpg_mkm_t 0
return run function rpg:michael/anim/stun/tick
