# 什一税：先看口袋里有没有钱。`clear ... 0` 是只数不拿，原版惯用写法。
execute store result score #have rpg_mam run clear @s minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}] 0
execute if score #have rpg_mam matches 1.. run return run function rpg:mammon/toll2_coin
# 一个子儿也没有 —— 那就折成经验。
function rpg:mammon/toll1
