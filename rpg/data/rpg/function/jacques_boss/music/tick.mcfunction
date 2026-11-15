scoreboard players remove #bgm rpg_jq 1
execute if score #bgm rpg_jq matches ..0 if score #stage rpg_jq matches 1 run function rpg:jacques_boss/music/1
execute if score #bgm rpg_jq matches ..0 if score #stage rpg_jq matches 2 run function rpg:jacques_boss/music/2
