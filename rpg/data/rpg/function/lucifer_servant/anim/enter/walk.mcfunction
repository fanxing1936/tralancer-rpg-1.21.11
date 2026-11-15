# 切到 walk 并立即播放第一帧。
scoreboard players set @s rpg_lcs_anim 1
scoreboard players set @s rpg_lcs_t 0
return run function rpg:lucifer_servant/anim/walk/tick
