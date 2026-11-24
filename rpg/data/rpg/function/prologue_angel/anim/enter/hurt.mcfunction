# 切到 hurt 并立即播放第一帧。
scoreboard players set @s rpg_pran_anim 4
scoreboard players set @s rpg_pran_t 0
return run function rpg:prologue_angel/anim/hurt/tick
