# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_pran_anim 0
scoreboard players set @s rpg_pran_t 0
return run function rpg:prologue_angel/anim/idle/tick
