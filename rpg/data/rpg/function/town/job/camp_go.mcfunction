$execute in minecraft:overworld positioned $(x) 0 $(z) run function rpg:town/camp/find
scoreboard players operation @e[type=minecraft:marker,tag=rpg.tw.new] rpg_tw_id = #cur rpg_tw
tag @e[type=minecraft:marker,tag=rpg.tw.new] remove rpg.tw.new
