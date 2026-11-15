# 切到 attack 并立即播放第一帧。
scoreboard players set @s rpg_bls_anim 2
scoreboard players set @s rpg_bls_t 0
return run function rpg:belial_servant/anim/attack/tick
