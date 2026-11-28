execute as @e[type=minecraft:marker,tag=rpg.tw.at.house,distance=..200] if score @s rpg_tw_id = #built rpg_tw run tag @s add rpg.tl.pick
execute as @e[type=minecraft:marker,tag=rpg.tl.pick,limit=1,sort=random] at @s run function rpg:town/life/ppl/house
tag @e[type=minecraft:marker,tag=rpg.tl.pick] remove rpg.tl.pick
