# 切到 stun 并立即播放第一帧。
scoreboard players set @s rpg_prbz_anim 6
scoreboard players set @s rpg_prbz_t 0
return run function rpg:prologue_beelzebub/anim/stun/tick
