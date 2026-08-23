# 眼前有一个待雇者。数一数已经有几个人，再看钱够不够。
#
# 每一条都用 `return run`：不用的话，命中 hire0 之后人数变成 1，
# 下一行 `if n=1` 也会成立 —— 一次按下会把四档全跑一遍，只扣第一档的钱。
scoreboard players set #cnt rpg_squad 0
execute as @e[type=minecraft:husk,tag=rpg.squad] if score @s rpg_squad = #sq rpg_squad run scoreboard players add #cnt rpg_squad 1
scoreboard players operation @s rpg_sq_n = #cnt rpg_squad
execute if entity @s[scores={rpg_sq_n=4..}] run return run function rpg:squad/full

# 手上有多少钱。`clear ... 0` 是**只数不拿**，原版惯用写法。
execute store result score @s rpg_sq_have run clear @s minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}] 0
execute if entity @s[scores={rpg_sq_n=0}] run return run function rpg:squad/hire0
execute if entity @s[scores={rpg_sq_n=1}] run return run function rpg:squad/hire1
execute if entity @s[scores={rpg_sq_n=2}] run return run function rpg:squad/hire2
execute if entity @s[scores={rpg_sq_n=3}] run return run function rpg:squad/hire3
