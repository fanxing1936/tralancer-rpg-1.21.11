# prologue_multi hub
# 跳过序章（as 玩家）：排队的出队、分了组还没进去的撤回、正在打的还原背包送回去；记为打过（面板不再显示「序章」，不发羽毛）。
# 新手开局里的人接着进正式游戏（onboard/pro/after → finish）
scoreboard players set @s rpg_pr_done 1
tag @s remove rpg.pr.q
tag @s remove rpg.pr.pick
scoreboard players reset @s rpg_pr_qt
execute if entity @s[tag=rpg.pri1] in rpg:armageddon run return run function rpg:prologue_i1/skip_in
tag @s remove rpg.pr.join1
execute if entity @s[tag=rpg.pri2] in rpg:armageddon_2 run return run function rpg:prologue_i2/skip_in
tag @s remove rpg.pr.join2
execute if entity @s[tag=rpg.pri3] in rpg:armageddon_3 run return run function rpg:prologue_i3/skip_in
tag @s remove rpg.pr.join3
execute if entity @s[tag=rpg.pri4] in rpg:armageddon_4 run return run function rpg:prologue_i4/skip_in
tag @s remove rpg.pr.join4
scoreboard players reset @s rpg_pr_g
execute if entity @s[tag=rpg.ob] run function rpg:onboard/pro/after
tellraw @s {"text":"[序章] 已跳过。","color":"#E8D9B0"}
