# 切到 throw 并立即播放第一帧。
scoreboard players set @s rpg_prmi_anim 25
scoreboard players set @s rpg_prmi_t 0
return run function rpg:prologue_michael/anim/throw/tick
