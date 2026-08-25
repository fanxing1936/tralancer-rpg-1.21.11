clear @s minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}] 1
function rpg:hud/m26
playsound minecraft:entity.item.pickup player @s ~ ~ ~ 1 0.6
execute at @s run particle wax_on ~ ~1 ~ 0.3 0.4 0.3 0.05 10
