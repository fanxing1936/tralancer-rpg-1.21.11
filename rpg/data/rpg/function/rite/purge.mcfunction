# 净化。圣光沿四方连线走一圈，然后收束到阵心。
particle end_rod ~ ~0.3 ~ 3 0.1 3 0.02 90
particle dust{color:[1.0,0.98,0.86],scale:2} ~ ~1 ~ 2.6 0.6 2.6 0.04 120
particle minecraft:flash{color:16777200} ~ ~1 ~ 0 0 0 0 1
playsound minecraft:block.beacon.activate player @a[distance=..24] ~ ~ ~ 1 1.2
playsound minecraft:block.conduit.deactivate player @a[distance=..24] ~ ~ ~ 1 1.4

# 一、洗去施术者自己的魔化
execute as @a[distance=..4] run scoreboard players remove @s rpg_taint 25
execute as @a[distance=..4,scores={rpg_taint=..-1}] run scoreboard players set @s rpg_taint 0
execute as @a[distance=..4] run effect give @s minecraft:regeneration 6 0 true
execute as @a[distance=..4] run title @s actionbar ["",{"text":"驱　魔","color":"gold","bold":true},{"text":"　魔化已被洗去一分","color":"gray"}]

# 二、驱出阵内的空缺者：空壳散去，人回来
execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..6] at @s run function rpg:rite/free
