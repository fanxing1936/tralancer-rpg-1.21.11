# 切到 rib_slash4 并立即播放第一帧。
execute unless entity @s[tag=rpg.michael_spirit.dual_rib] run return 0
scoreboard players set @s rpg_mis_anim 12
scoreboard players set @s rpg_mis_t 0
return run function rpg:michael_spirit/anim/rib_slash4/tick
