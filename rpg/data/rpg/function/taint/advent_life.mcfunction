# 刚落地的那位开始倒数。标签在这一刻只可能挂在他一个身上。
execute as @e[type=minecraft:vindicator,tag=rpg.advent.new] run scoreboard players set @s rpg_fall 600
tag @e[type=minecraft:vindicator,tag=rpg.advent.new] remove rpg.advent.new
