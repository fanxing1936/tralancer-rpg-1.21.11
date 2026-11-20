# 刺出（as/at 他）：打中了就是一下 24；没打中他冲过去跪地
execute if entity @e[tag=rpg.unit,tag=rpg.slb.hit] run return run function rpg:saul_boss/last/hit
function rpg:saul_boss/last/miss
