# 切到 fold 并立即播放第一帧。
scoreboard players set @s rpg_prbl_anim 5
scoreboard players set @s rpg_prbl_t 0
return run function rpg:prologue_belial/anim/fold/tick
