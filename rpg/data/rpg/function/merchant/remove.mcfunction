# 管理员：移走 4 格内最近的商人（连同模型部件）
execute as @e[tag=rpg.mer,distance=..4,limit=1,sort=nearest] run function rpg:merchant/gone
