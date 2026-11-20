# 一课结束：躲对了他叫好（as 他）
execute unless entity @e[tag=rpg.unit,tag=rpg.slb.failed] run function rpg:saul_boss/lesson/good
execute if entity @e[tag=rpg.unit,tag=rpg.slb.failed] run function rpg:saul_boss/lesson/again
tag @e[tag=rpg.unit] remove rpg.slb.failed
function rpg:saul/anim/enter/idle
