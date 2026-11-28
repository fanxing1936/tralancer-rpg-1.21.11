# prologue_multi hub
# 排进序章的队（as 玩家）：凑满四人或等不到别人就开一组
execute if entity @s[tag=rpg.pr] run return 0
tag @s add rpg.pr.q
scoreboard players set @s rpg_pr_qt 0
