# 载体不见了：二阶段里（比如被一下打穿了死亡保护）在他最后的位置补放死亡特效再结算；否则清场。
execute if score #stage rpg_mk_i3 matches 2.. run return run function rpg:michael_boss_i3/ghost/start
function rpg:michael_boss_i3/clear
