# 切到 summon 并立即播放第一帧。
scoreboard players set @s rpg_pp_anim 3
scoreboard players set @s rpg_pp_t 0
return run function rpg:pope/anim/summon/tick
