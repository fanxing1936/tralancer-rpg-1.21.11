# 切到 walk 并立即播放第一帧。
execute if entity @s[tag=rpg.mk.rib] run return run function rpg:michael/anim/enter/rib_walk
scoreboard players set @s rpg_mkm_anim 1
scoreboard players set @s rpg_mkm_t 0
return run function rpg:michael/anim/walk/tick
