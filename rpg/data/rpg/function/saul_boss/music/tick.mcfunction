scoreboard players remove #bgm rpg_sl 1
execute if score #bgm rpg_sl matches ..0 if score #stage rpg_sl matches 1 run function rpg:saul_boss/music/1
execute if score #bgm rpg_sl matches ..0 if score #stage rpg_sl matches 2 run function rpg:saul_boss/music/2
