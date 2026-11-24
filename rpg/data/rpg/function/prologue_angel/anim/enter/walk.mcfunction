# 切到 walk 并立即播放第一帧。
scoreboard players set @s rpg_pran_anim 1
scoreboard players set @s rpg_pran_t 0
return run function rpg:prologue_angel/anim/walk/tick
