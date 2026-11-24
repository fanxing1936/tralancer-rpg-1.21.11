# 切到 look 并立即播放第一帧。
scoreboard players set @s rpg_mtr_anim 1
scoreboard players set @s rpg_mtr_t 0
return run function rpg:merchant_travel/anim/look/tick
