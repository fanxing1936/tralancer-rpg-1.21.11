execute if score #pro rpg_mk_i4 matches 1 run return 0
scoreboard players remove #bgm rpg_mk_i4 1
execute if score #bgm rpg_mk_i4 matches ..0 if score #stage rpg_mk_i4 matches 1 run function rpg:michael_boss_i4/music/1
execute if score #bgm rpg_mk_i4 matches ..0 if score #stage rpg_mk_i4 matches 2 run function rpg:michael_boss_i4/music/2
