# 切到 kneel_down 并立即播放第一帧。
scoreboard players set @s rpg_prmm_anim 11
scoreboard players set @s rpg_prmm_t 0
return run function rpg:prologue_mammon/anim/kneel_down/tick
