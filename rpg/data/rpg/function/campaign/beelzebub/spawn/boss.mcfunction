execute positioned ^ ^ ^40 run tag @e[type=minecraft:vindicator,tag=rpg.advent,scores={rpg_dm_lord=4},distance=..8] add rpg.ch1.preexisting
execute positioned ^ ^ ^40 run function rpg:taint/lord4
execute positioned ^ ^ ^40 run tag @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.ch1.preexisting,scores={rpg_dm_lord=4},distance=..8,sort=nearest,limit=1] add rpg.ch1.boss.new
scoreboard players operation @e[type=minecraft:vindicator,tag=rpg.ch1.boss.new,limit=1] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:vindicator,tag=rpg.ch1.boss.new,limit=1] add rpg.ch1.boss
tag @e[type=minecraft:vindicator,tag=rpg.ch1.boss.new] remove rpg.ch1.boss.new
tag @e[tag=rpg.ch1.preexisting] remove rpg.ch1.preexisting
