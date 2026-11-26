# 每 4 刻：空手看着灵魂营火的玩家（rpg:bench/tick 挂在 tick 标签）
scoreboard players add #t rpg_bn 1
execute if score #t rpg_bn matches 4.. run function rpg:bench/scan
execute as @e[type=minecraft:interaction,tag=rpg.bench] run function rpg:bench/age
