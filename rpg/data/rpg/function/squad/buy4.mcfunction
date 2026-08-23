# FABLE：80 枚。
execute if entity @s[scores={rpg_sq_have=..79}] run return run function rpg:squad/poor
clear @s minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}] 80
function rpg:squad/sign_on
