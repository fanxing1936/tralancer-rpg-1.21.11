# 切到 walk 并立即播放第一帧。
scoreboard players set @s rpg_bls_anim 1
scoreboard players set @s rpg_bls_t 0
return run function rpg:belial_servant/anim/walk/tick
