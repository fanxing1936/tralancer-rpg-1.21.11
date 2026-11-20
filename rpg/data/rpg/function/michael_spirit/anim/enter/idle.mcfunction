# 切到 idle 并立即播放第一帧。
execute if entity @s[tag=rpg.michael_spirit.dual_rib] run return run function rpg:michael_spirit/anim/enter/rib_idle
scoreboard players set @s rpg_mis_anim 0
scoreboard players set @s rpg_mis_t 0
return run function rpg:michael_spirit/anim/idle/tick
