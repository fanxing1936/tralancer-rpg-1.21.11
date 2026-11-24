# 切到 examine 并立即播放第一帧。
scoreboard players set @s rpg_msm_anim 3
scoreboard players set @s rpg_msm_t 0
return run function rpg:merchant_smith/anim/examine/tick
