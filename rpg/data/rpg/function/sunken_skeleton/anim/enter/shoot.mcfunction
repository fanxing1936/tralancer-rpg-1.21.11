# 切到 shoot 并立即播放第一帧。
scoreboard players set @s rpg_sk_anim 3
scoreboard players set @s rpg_sk_t 0
return run function rpg:sunken_skeleton/anim/shoot/tick
