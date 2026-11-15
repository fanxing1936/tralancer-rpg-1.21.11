# 切到 hero 并立即播放第一帧。
scoreboard players set @s rpg_jqm_anim 16
scoreboard players set @s rpg_jqm_t 0
return run function rpg:jacques/anim/hero/tick
