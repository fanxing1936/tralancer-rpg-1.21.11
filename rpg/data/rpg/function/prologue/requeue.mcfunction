# prologue_multi hub
scoreboard players reset @s rpg_pr_g
scoreboard players reset @s rpg_pr_lv
tag @s remove rpg.pr.join1
tag @s remove rpg.pr.join2
tag @s remove rpg.pr.join3
tag @s remove rpg.pr.join4
execute if entity @s[tag=rpg.ob] run function rpg:prologue/enqueue
