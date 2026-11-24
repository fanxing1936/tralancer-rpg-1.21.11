# 切到 fold 并立即播放第一帧。
scoreboard players set @s rpg_prmi_anim 10
scoreboard players set @s rpg_prmi_t 0
return run function rpg:prologue_michael/anim/fold/tick
