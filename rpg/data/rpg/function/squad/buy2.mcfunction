# SONNET：20 枚。
execute if entity @s[scores={rpg_sq_have=..19}] run return run function rpg:squad/poor
clear @s minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}] 20
function rpg:squad/sign_on
