# 载体不见了：二阶段里按胜利结算；否则清场。
execute if score #stage rpg_sl matches 2.. run return run function rpg:saul_boss/victory
function rpg:saul_boss/clear
