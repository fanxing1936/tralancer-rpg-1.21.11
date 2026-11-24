# 切到 hero 并立即播放第一帧。
scoreboard players set @s rpg_prbl_anim 18
scoreboard players set @s rpg_prbl_t 0
return run function rpg:prologue_belial/anim/hero/tick
