# 切到 blink 并立即播放第一帧。
scoreboard players set @s rpg_prth_anim 1
scoreboard players set @s rpg_prth_t 0
return run function rpg:prologue_throne/anim/blink/tick
