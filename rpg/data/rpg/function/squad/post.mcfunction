# 招一个待雇者到场，等级当场掷点 —— 甲、纹饰、基础数值与价钱全由这一掷定下。
# 掷完你看着名牌决定雇不雇，这才叫募兵。
execute store result score @s rpg_sq_roll run random value 1..100
execute if score @s rpg_sq_roll matches 1..40 run return run function rpg:squad/post1
execute if score @s rpg_sq_roll matches 41..68 run return run function rpg:squad/post2
execute if score @s rpg_sq_roll matches 69..86 run return run function rpg:squad/post3
execute if score @s rpg_sq_roll matches 87..96 run return run function rpg:squad/post4
execute if score @s rpg_sq_roll matches 97..100 run return run function rpg:squad/post5
playsound minecraft:entity.villager.trade player @s ~ ~ ~ 1 0.9
