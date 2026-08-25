# 刚落地的那位开始倒数。标签在这一刻只可能挂在他一个身上。
#
# `#boss` 是一次性的开关：空缺者那条路在召唤前把它拨上，
# 两条来源现在都需要容纳真名调查和完整仪式，因此统一使用十分钟窗口；仍由
# 同一套发条负责，避免两份 NBT 迟早写歪。
execute as @e[type=minecraft:vindicator,tag=rpg.advent.new] run scoreboard players set @s rpg_fall 12000
execute if score #boss rpg_fall matches 1 as @e[type=minecraft:vindicator,tag=rpg.advent.new] run scoreboard players set @s rpg_fall 12000
scoreboard players set #boss rpg_fall 0
tag @e[type=minecraft:vindicator,tag=rpg.advent.new] add rpg.advent.timed
tag @e[type=minecraft:vindicator,tag=rpg.advent.new] remove rpg.advent.new
