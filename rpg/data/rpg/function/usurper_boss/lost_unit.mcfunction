# 载体不见了：二阶段里被一击打穿时按胜利结算；否则清场。
execute if score #stage rpg_ub matches 2.. run return run function rpg:usurper_boss/victory
function rpg:usurper_boss/clear
