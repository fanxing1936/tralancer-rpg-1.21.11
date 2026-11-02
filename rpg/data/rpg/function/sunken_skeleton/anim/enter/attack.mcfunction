# 切到 attack 并立即播放第一帧。
scoreboard players set @s rpg_sk_anim 2
scoreboard players set @s rpg_sk_t 0
return run function rpg:sunken_skeleton/anim/attack/tick
