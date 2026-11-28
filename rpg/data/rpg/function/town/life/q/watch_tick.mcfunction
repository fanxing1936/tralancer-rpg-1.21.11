# 每秒（as/at 接了守夜的玩家）：只在夜里算
execute store result score #tod rpg_tl run time query daytime
execute unless score #tod rpg_tl matches 13000..23000 run return 0
execute if entity @e[type=minecraft:marker,tag=rpg.tw.at.grave,distance=..6] run function rpg:town/life/q/watch_bit {b:1}
execute if entity @e[type=minecraft:marker,tag=rpg.tw.at.plaza,distance=..6] run function rpg:town/life/q/watch_bit {b:2}
execute if entity @e[type=minecraft:marker,tag=rpg.tw.at.church,distance=..6] run function rpg:town/life/q/watch_bit {b:4}
execute if entity @e[type=minecraft:marker,tag=rpg.tw.at.bench,distance=..6] run function rpg:town/life/q/watch_bit {b:8}
