# 切到 walk 并立即播放第一帧。
scoreboard players set @s rpg_jqm_anim 1
scoreboard players set @s rpg_jqm_t 0
return run function rpg:jacques/anim/walk/tick
