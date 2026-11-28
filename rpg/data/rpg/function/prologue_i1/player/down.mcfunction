scoreboard players remove @s rpg_pr_down 1
execute if score @s rpg_pr_down matches 0 if score #cut rpg_pr_i1 matches 0 run function rpg:prologue_i1/player/rise
