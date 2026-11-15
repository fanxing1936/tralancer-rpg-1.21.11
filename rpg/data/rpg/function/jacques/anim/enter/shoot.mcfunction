# 切到 shoot 并立即播放第一帧。
scoreboard players set @s rpg_jqm_anim 8
scoreboard players set @s rpg_jqm_t 0
return run function rpg:jacques/anim/shoot/tick
