# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_prth_anim 0
scoreboard players set @s rpg_prth_t 0
return run function rpg:prologue_throne/anim/idle/tick
