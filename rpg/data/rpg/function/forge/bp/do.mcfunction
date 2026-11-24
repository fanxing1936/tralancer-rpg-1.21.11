# 图纸锻造：70 打开（读副手图纸），71 开炉
execute if score #do rpg_fg matches 70 run return run function rpg:forge/bp/open
execute if score #do rpg_fg matches 71 run return run function rpg:forge/bp/start
