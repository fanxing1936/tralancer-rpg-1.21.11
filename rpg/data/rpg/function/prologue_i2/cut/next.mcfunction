# 一段过场放完：接下一段，或回到玩家操作
execute if score #cut rpg_pr_i2 matches 1 run return run function rpg:prologue_i2/flow/after1
execute if score #cut rpg_pr_i2 matches 3 run return run function rpg:prologue_i2/flow/after3
execute if score #cut rpg_pr_i2 matches 4 run return run function rpg:prologue_i2/flow/after4
execute if score #cut rpg_pr_i2 matches 6 run return run function rpg:prologue_i2/flow/after6
execute if score #cut rpg_pr_i2 matches 7 run return run function rpg:prologue_i2/flow/after7
