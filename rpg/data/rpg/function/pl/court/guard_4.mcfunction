# 随机一柱的五名罪仆
execute store result score #l rpg_pl run random value 1..7
execute if score #l rpg_pl matches 1 run function rpg:minion/summon/lucifer/all
execute if score #l rpg_pl matches 2 run function rpg:minion/summon/leviathan/all
execute if score #l rpg_pl matches 3 run function rpg:minion/summon/abaddon/all
execute if score #l rpg_pl matches 4 run function rpg:minion/summon/beelzebub/all
execute if score #l rpg_pl matches 5 run function rpg:minion/summon/samael/all
execute if score #l rpg_pl matches 6 run function rpg:minion/summon/belial/all
execute if score #l rpg_pl matches 7 run function rpg:minion/summon/mammon/all
tag @e[tag=rpg.demon.minion,distance=..14] add rpg.pl.g
