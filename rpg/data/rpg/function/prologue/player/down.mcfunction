scoreboard players remove @s rpg_pr_down 1
execute if score @s rpg_pr_down matches 0 if score #cut rpg_pr matches 0 run function rpg:prologue/player/rise
