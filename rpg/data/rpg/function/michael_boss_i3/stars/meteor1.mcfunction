# 一颗流星（at 中心）：扇区里随机一点
execute store result storage rpg:michael_boss_i3 star.a int 1 run random value 125..235
execute store result storage rpg:michael_boss_i3 star.d int 1 run random value 3..30
function rpg:michael_boss_i3/stars/fall with storage rpg:michael_boss_i3 star
