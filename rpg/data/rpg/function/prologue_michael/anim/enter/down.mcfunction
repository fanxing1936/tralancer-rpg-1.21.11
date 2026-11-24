# 切到 down 并立即播放第一帧。
scoreboard players set @s rpg_prmi_anim 23
scoreboard players set @s rpg_prmi_t 0
return run function rpg:prologue_michael/anim/down/tick
