# 切到 sweep 并立即播放第一帧。
execute unless entity @s[tag=!rpg.michael_spirit.dual_rib] run return 0
scoreboard players set @s rpg_mis_anim 5
scoreboard players set @s rpg_mis_t 0
return run function rpg:michael_spirit/anim/sweep/tick
