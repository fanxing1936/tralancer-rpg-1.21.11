# 切到 summon 并立即播放第一帧。
scoreboard players set @s rpg_pe_anim 10
scoreboard players set @s rpg_pe_t 0
return run function rpg:prime_enchanter/anim/summon/tick
