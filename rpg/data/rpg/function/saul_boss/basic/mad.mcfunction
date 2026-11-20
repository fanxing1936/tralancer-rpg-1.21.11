# 二阶段：顺序随机
execute store result score #r rpg_sl run random value 0..2
execute if score #r rpg_sl matches 0 run function rpg:saul_boss/skill/left
execute if score #r rpg_sl matches 1 run function rpg:saul_boss/skill/right
execute if score #r rpg_sl matches 2 run function rpg:saul_boss/skill/double
