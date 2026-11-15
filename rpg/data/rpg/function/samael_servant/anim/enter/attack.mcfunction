# 切到 attack 并立即播放第一帧。
scoreboard players set @s rpg_sms_anim 2
scoreboard players set @s rpg_sms_t 0
return run function rpg:samael_servant/anim/attack/tick
