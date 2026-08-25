# 升到 OPUS：40 枚。
execute if entity @s[scores={rpg_sq_have=..39}] run return run function rpg:squad/poor
clear @s minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}] 40
execute as @e[type=minecraft:husk,tag=rpg.sq.pick,distance=..6,limit=1,sort=nearest] run function rpg:squad/up_do3
function rpg:hud/m51
