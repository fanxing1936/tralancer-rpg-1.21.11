# 无处可去的东西不再散成碎片 —— 它自己找了一副躯体。
#
# @s 是那个动手的人。签了哪一柱，来的就是哪一位；没签过的是无名者 ——
# 与降临同一套分流，只是这一只是来打架的，所以寿命另算。
scoreboard players set #boss rpg_fall 1
scoreboard players set #lord rpg_fall 0
execute if entity @s[tag=rpg.pact] run scoreboard players operation #lord rpg_fall = @s rpg_pact
execute at @s run function rpg:taint/lord
