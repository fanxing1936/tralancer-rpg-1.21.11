scoreboard players remove @s rpg_pr_down 1
execute if score @s rpg_pr_down matches 0 if score #cut rpg_pr_i2 matches 0 run function rpg:prologue_i2/player/rise
