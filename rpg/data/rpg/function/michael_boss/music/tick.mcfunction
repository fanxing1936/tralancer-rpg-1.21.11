execute if score #pro rpg_mk matches 1 run return 0
scoreboard players remove #bgm rpg_mk 1
execute if score #bgm rpg_mk matches ..0 if score #stage rpg_mk matches 1 run function rpg:michael_boss/music/1
execute if score #bgm rpg_mk matches ..0 if score #stage rpg_mk matches 2 run function rpg:michael_boss/music/2
