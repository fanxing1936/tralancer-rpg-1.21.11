# 切到 address 并立即播放第一帧。
scoreboard players set @s rpg_prlu_anim 3
scoreboard players set @s rpg_prlu_t 0
return run function rpg:prologue_lucifer/anim/address/tick
