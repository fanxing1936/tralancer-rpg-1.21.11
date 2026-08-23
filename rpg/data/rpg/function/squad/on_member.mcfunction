# @s 是被点的佣兵，rpg.sq.boss 是点他的人。
execute if predicate rpg:sneaking_boss run return run function rpg:squad/dismiss
# 先把他原本拿的东西掉出来（有的话），再换上雇主手里那件
execute unless items entity @s weapon.mainhand *[] run return run function rpg:squad/take_weapon
function rpg:squad/drop_weapon
function rpg:squad/take_weapon
