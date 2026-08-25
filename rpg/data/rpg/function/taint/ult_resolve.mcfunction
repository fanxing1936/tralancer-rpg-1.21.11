# 结算期间临时挂归属标签，复用普通招式的精确伤害来源。
tag @s add rpg.dm.cast
function rpg:taint/ultimate
tag @s remove rpg.dm.cast
