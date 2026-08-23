# OPUS：40 枚。
execute if entity @s[scores={rpg_sq_have=..39}] run return run function rpg:squad/poor
clear @s minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}] 40
function rpg:squad/sign_on
