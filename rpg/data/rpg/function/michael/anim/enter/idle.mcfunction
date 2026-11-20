# 切到 idle 并立即播放第一帧。
execute if entity @s[tag=rpg.mk.rib] run return run function rpg:michael/anim/enter/rib_idle
scoreboard players set @s rpg_mkm_anim 0
scoreboard players set @s rpg_mkm_t 0
return run function rpg:michael/anim/idle/tick
