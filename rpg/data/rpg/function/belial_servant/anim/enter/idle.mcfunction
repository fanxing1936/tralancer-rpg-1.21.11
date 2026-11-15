# 切到 idle 并立即播放第一帧。
scoreboard players set @s rpg_bls_anim 0
scoreboard players set @s rpg_bls_t 0
return run function rpg:belial_servant/anim/idle/tick
