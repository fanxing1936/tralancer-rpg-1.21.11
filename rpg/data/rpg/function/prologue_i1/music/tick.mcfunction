execute unless score #bgm rpg_pr_i1 matches 1.. run return 0
scoreboard players remove #bgm rpg_pr_i1 1
execute if score #bgm rpg_pr_i1 matches 0 if score #bgmid rpg_pr_i1 matches 1 run function rpg:prologue_i1/music/intro
execute if score #bgm rpg_pr_i1 matches 0 if score #bgmid rpg_pr_i1 matches 2 run function rpg:prologue_i1/music/waves
execute if score #bgm rpg_pr_i1 matches 0 if score #bgmid rpg_pr_i1 matches 3 run function rpg:prologue_i1/music/michael
execute if score #bgm rpg_pr_i1 matches 0 if score #bgmid rpg_pr_i1 matches 4 run function rpg:prologue_i1/music/end
