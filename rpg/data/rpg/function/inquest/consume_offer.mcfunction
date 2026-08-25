execute store result score #offer_count rpg_ex_tmp run data get entity @e[type=minecraft:item,tag=rpg.rite.offer,limit=1] Item.count 1
scoreboard players remove #offer_count rpg_ex_tmp 1
execute if score #offer_count rpg_ex_tmp matches 1.. store result entity @e[type=minecraft:item,tag=rpg.rite.offer,limit=1] Item.count int 1 run scoreboard players get #offer_count rpg_ex_tmp
execute if score #offer_count rpg_ex_tmp matches ..0 run kill @e[type=minecraft:item,tag=rpg.rite.offer,limit=1]
tag @e[type=minecraft:item,tag=rpg.rite.offer] remove rpg.rite.offer
