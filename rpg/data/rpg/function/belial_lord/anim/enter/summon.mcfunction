# 切到 summon 并立即播放第一帧。
scoreboard players set @s rpg_bll_anim 3
scoreboard players set @s rpg_bll_t 0
return run function rpg:belial_lord/anim/summon/tick
