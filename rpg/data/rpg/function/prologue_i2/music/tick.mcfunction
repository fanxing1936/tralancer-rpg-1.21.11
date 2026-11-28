execute unless score #bgm rpg_pr_i2 matches 1.. run return 0
scoreboard players remove #bgm rpg_pr_i2 1
execute if score #bgm rpg_pr_i2 matches 0 if score #bgmid rpg_pr_i2 matches 1 run function rpg:prologue_i2/music/intro
execute if score #bgm rpg_pr_i2 matches 0 if score #bgmid rpg_pr_i2 matches 2 run function rpg:prologue_i2/music/waves
execute if score #bgm rpg_pr_i2 matches 0 if score #bgmid rpg_pr_i2 matches 3 run function rpg:prologue_i2/music/michael
execute if score #bgm rpg_pr_i2 matches 0 if score #bgmid rpg_pr_i2 matches 4 run function rpg:prologue_i2/music/end
