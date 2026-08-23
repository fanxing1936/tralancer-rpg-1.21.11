# 升到 SONNET：20 枚。
execute if entity @s[scores={rpg_sq_have=..19}] run return run function rpg:squad/poor
clear @s minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}] 20
execute as @e[type=minecraft:husk,tag=rpg.squad,distance=..6,limit=1,sort=nearest] run function rpg:squad/up_do2
function rpg:hud/m31
