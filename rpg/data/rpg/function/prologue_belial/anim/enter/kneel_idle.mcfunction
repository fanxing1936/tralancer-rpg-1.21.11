# 切到 kneel_idle 并立即播放第一帧。
scoreboard players set @s rpg_prbl_anim 12
scoreboard players set @s rpg_prbl_t 0
return run function rpg:prologue_belial/anim/kneel_idle/tick
