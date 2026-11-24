execute unless score #bgm rpg_pr matches 1.. run return 0
scoreboard players remove #bgm rpg_pr 1
execute if score #bgm rpg_pr matches 0 if score #bgmid rpg_pr matches 1 run function rpg:prologue/music/intro
execute if score #bgm rpg_pr matches 0 if score #bgmid rpg_pr matches 2 run function rpg:prologue/music/waves
execute if score #bgm rpg_pr matches 0 if score #bgmid rpg_pr matches 3 run function rpg:prologue/music/michael
execute if score #bgm rpg_pr matches 0 if score #bgmid rpg_pr matches 4 run function rpg:prologue/music/end
