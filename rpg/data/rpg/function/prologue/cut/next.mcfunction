# 一段过场放完：接下一段，或回到玩家操作
execute if score #cut rpg_pr matches 1 run return run function rpg:prologue/flow/after1
execute if score #cut rpg_pr matches 3 run return run function rpg:prologue/flow/after3
execute if score #cut rpg_pr matches 4 run return run function rpg:prologue/flow/after4
execute if score #cut rpg_pr matches 6 run return run function rpg:prologue/flow/after6
execute if score #cut rpg_pr matches 7 run return run function rpg:prologue/flow/after7
