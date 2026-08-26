execute positioned ^ ^ ^40 run tag @e[type=minecraft:vindicator,tag=rpg.advent,scores={rpg_dm_lord=4},distance=..8] add rpg.ch1.preexisting
execute positioned ^ ^ ^40 run function rpg:taint/lord4
execute positioned ^ ^ ^40 run tag @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.ch1.preexisting,scores={rpg_dm_lord=4},distance=..8,sort=nearest,limit=1] add rpg.ch1.boss.new
scoreboard players operation @e[type=minecraft:vindicator,tag=rpg.ch1.boss.new,limit=1] rpg_ch1_id = @s rpg_ch1_id
attribute @e[type=minecraft:vindicator,tag=rpg.ch1.boss.new,limit=1] minecraft:max_health base set 700
data merge entity @e[type=minecraft:vindicator,tag=rpg.ch1.boss.new,limit=1] {Health:700f,CustomName:["",{"text":"别西卜","color":"#5A6B1E","bold":true,"italic":false}]}
tag @e[type=minecraft:vindicator,tag=rpg.ch1.boss.new,limit=1] add rpg.ch1.boss
tag @e[type=minecraft:vindicator,tag=rpg.ch1.boss.new] remove rpg.ch1.boss.new
tag @e[tag=rpg.ch1.preexisting] remove rpg.ch1.preexisting
