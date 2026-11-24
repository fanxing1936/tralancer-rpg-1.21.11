# 切到 kneel_idle 并立即播放第一帧。
scoreboard players set @s rpg_prbz_anim 12
scoreboard players set @s rpg_prbz_t 0
return run function rpg:prologue_beelzebub/anim/kneel_idle/tick
