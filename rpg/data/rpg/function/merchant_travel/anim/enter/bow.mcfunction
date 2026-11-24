# 切到 bow 并立即播放第一帧。
scoreboard players set @s rpg_mtr_anim 2
scoreboard players set @s rpg_mtr_t 0
return run function rpg:merchant_travel/anim/bow/tick
