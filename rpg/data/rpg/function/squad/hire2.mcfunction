# 第 3 名，价钱 24 枚。
execute if entity @s[scores={rpg_sq_have=..23}] run return run function rpg:squad/poor
clear @s minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}] 24
function rpg:squad/spawn
