# 第 4 名，价钱 32 枚。
execute if entity @s[scores={rpg_sq_have=..31}] run return run function rpg:squad/poor
clear @s minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}] 32
function rpg:squad/sign_on
