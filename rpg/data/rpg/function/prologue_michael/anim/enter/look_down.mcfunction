# 切到 look_down 并立即播放第一帧。
scoreboard players set @s rpg_prmi_anim 27
scoreboard players set @s rpg_prmi_t 0
return run function rpg:prologue_michael/anim/look_down/tick
