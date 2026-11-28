# 一座镇建好了（#built = 镇号，执行位置任意）：在各个锚点放人
execute as @e[type=minecraft:marker,tag=rpg.tw.at.church] if score @s rpg_tw_id = #built rpg_tw at @s run function rpg:town/life/ppl/church
execute as @e[type=minecraft:marker,tag=rpg.tw.at.elder] if score @s rpg_tw_id = #built rpg_tw at @s run function rpg:town/life/ppl/elder
execute as @e[type=minecraft:marker,tag=rpg.tw.at.tavern] if score @s rpg_tw_id = #built rpg_tw at @s run function rpg:town/life/ppl/tavern
execute as @e[type=minecraft:marker,tag=rpg.tw.at.grave] if score @s rpg_tw_id = #built rpg_tw at @s run function rpg:town/life/ppl/grave
execute as @e[type=minecraft:marker,tag=rpg.tw.at.granary] if score @s rpg_tw_id = #built rpg_tw at @s run function rpg:town/life/ppl/granary
execute as @e[type=minecraft:marker,tag=rpg.tw.at.plaza] if score @s rpg_tw_id = #built rpg_tw at @s run function rpg:town/life/ppl/plaza
execute as @e[type=minecraft:marker,tag=rpg.tw.at.house] if score @s rpg_tw_id = #built rpg_tw run tag @s add rpg.tl.pick
execute as @e[type=minecraft:marker,tag=rpg.tl.pick,limit=1,sort=random] at @s run function rpg:town/life/ppl/house
tag @e[type=minecraft:marker,tag=rpg.tl.pick] remove rpg.tl.pick
execute unless entity @e[type=minecraft:villager,tag=rpg.tnpc.bard,scores={rpg_tw_id=0}] as @e[type=minecraft:marker,tag=rpg.tw.at.plaza] if score @s rpg_tw_id = #built rpg_tw unless entity @e[type=minecraft:marker,tag=rpg.tw.at.tavern,distance=..400] at @s positioned ~-5 ~ ~5 run function rpg:town/life/ppl/tavern
execute as @e[type=minecraft:marker,tag=rpg.tw.at.bench] if score @s rpg_tw_id = #built rpg_tw at @s positioned ~-2 ~ ~1 run function rpg:merchant/spawn_smith
execute as @e[type=minecraft:marker,tag=rpg.tw.at.bench] if score @s rpg_tw_id = #built rpg_tw at @s positioned ~-2 ~ ~1 as @e[type=minecraft:villager,tag=rpg.mer.smith,distance=..2] store result entity @s Rotation[0] float 1 run random value -180..179
execute as @e[type=minecraft:marker,tag=rpg.tw.at.board] if score @s rpg_tw_id = #built rpg_tw at @s run function rpg:town/life/ppl/board
execute as @e[type=minecraft:marker,tag=rpg.tw.at.spawn] if score @s rpg_tw_id = #built rpg_tw at @s positioned ~9 ~ ~-1 run function rpg:town/life/ppl/guard
execute as @e[type=minecraft:marker,tag=rpg.tw.at.church] if score @s rpg_tw_id = #built rpg_tw at @s positioned ~-3 ~ ~1 run function rpg:town/life/ppl/guard
execute as @e[type=minecraft:marker,tag=rpg.tw.at.grave] if score @s rpg_tw_id = #built rpg_tw at @s run function rpg:town/life/ppl/graves
execute as @e[type=minecraft:marker,tag=rpg.tw.at.church] if score @s rpg_tw_id = #built rpg_tw at @s positioned ~2 ~ ~ run function rpg:town/prop {n:"bell"}
