# 切到 seized 并立即播放第一帧。
scoreboard players set @s rpg_prlu_anim 5
scoreboard players set @s rpg_prlu_t 0
return run function rpg:prologue_lucifer/anim/seized/tick
