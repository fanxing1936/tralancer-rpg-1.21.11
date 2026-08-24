# 刚落地的那位开始倒数。标签在这一刻只可能挂在他一个身上。
#
# `#boss` 是一次性的开关：空缺者那条路在召唤前把它拨上，
# 于是同一套召唤能招出"来收账的"（30 秒）和"来打架的"（2 分钟）两种，
# 而不必写两份 NBT —— 两份迟早会写歪。
execute as @e[type=minecraft:vindicator,tag=rpg.advent.new] run scoreboard players set @s rpg_fall 600
execute if score #boss rpg_fall matches 1 as @e[type=minecraft:vindicator,tag=rpg.advent.new] run scoreboard players set @s rpg_fall 2400
scoreboard players set #boss rpg_fall 0
tag @e[type=minecraft:vindicator,tag=rpg.advent.new] add rpg.advent.timed
tag @e[type=minecraft:vindicator,tag=rpg.advent.new] remove rpg.advent.new
