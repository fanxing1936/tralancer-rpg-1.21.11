execute unless score #bgm rpg_pr_i4 matches 1.. run return 0
scoreboard players remove #bgm rpg_pr_i4 1
execute if score #bgm rpg_pr_i4 matches 0 if score #bgmid rpg_pr_i4 matches 1 run function rpg:prologue_i4/music/intro
execute if score #bgm rpg_pr_i4 matches 0 if score #bgmid rpg_pr_i4 matches 2 run function rpg:prologue_i4/music/waves
execute if score #bgm rpg_pr_i4 matches 0 if score #bgmid rpg_pr_i4 matches 3 run function rpg:prologue_i4/music/michael
execute if score #bgm rpg_pr_i4 matches 0 if score #bgmid rpg_pr_i4 matches 4 run function rpg:prologue_i4/music/end
