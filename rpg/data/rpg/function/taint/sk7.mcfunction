# 三招掷一招 —— 同一位打两次不会长得一样。
execute store result score #pick rpg_fall run random value 1..3
execute if score #pick rpg_fall matches 1 run return run function rpg:taint/sk7_1
execute if score #pick rpg_fall matches 2 run return run function rpg:taint/sk7_2
execute if score #pick rpg_fall matches 3 run return run function rpg:taint/sk7_3
