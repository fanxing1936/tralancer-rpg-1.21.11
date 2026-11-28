# prologue_multi hub
# 重新登录（as 玩家）：按组号交给自己的战场；分了组却没来得及进去的，重新排队
execute if entity @s[tag=!rpg.pr] if score @s rpg_pr_g matches 1.. run function rpg:prologue/requeue
execute unless score @s rpg_pr_g matches 1.. run return run scoreboard players reset @s rpg_pr_lv
execute if score @s rpg_pr_g matches 1 in rpg:armageddon run function rpg:prologue_i1/rejoin
execute if score @s rpg_pr_g matches 2 in rpg:armageddon_2 run function rpg:prologue_i2/rejoin
execute if score @s rpg_pr_g matches 3 in rpg:armageddon_3 run function rpg:prologue_i3/rejoin
execute if score @s rpg_pr_g matches 4 in rpg:armageddon_4 run function rpg:prologue_i4/rejoin
