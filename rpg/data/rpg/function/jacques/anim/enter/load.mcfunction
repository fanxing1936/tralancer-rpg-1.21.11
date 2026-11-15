# 切到 load 并立即播放第一帧。
scoreboard players set @s rpg_jqm_anim 6
scoreboard players set @s rpg_jqm_t 0
return run function rpg:jacques/anim/load/tick
