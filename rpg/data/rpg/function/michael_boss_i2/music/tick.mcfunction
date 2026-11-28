execute if score #pro rpg_mk_i2 matches 1 run return 0
scoreboard players remove #bgm rpg_mk_i2 1
execute if score #bgm rpg_mk_i2 matches ..0 if score #stage rpg_mk_i2 matches 1 run function rpg:michael_boss_i2/music/1
execute if score #bgm rpg_mk_i2 matches ..0 if score #stage rpg_mk_i2 matches 2 run function rpg:michael_boss_i2/music/2
