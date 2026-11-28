summon minecraft:zombie ~ ~ ~ {Tags:["rpg.tw.ev","rpg.te.hol"],PersistenceRequired:1b,CanPickUpLoot:0b,CustomName:{"text":"空心人","color":"#A8B4C0","bold":false,"italic":false},attributes:[{id:"minecraft:max_health",base:26},{id:"minecraft:movement_speed",base:0.26},{id:"minecraft:follow_range",base:48}],Health:26f}
particle minecraft:block{block_state:"minecraft:dirt"} ~ ~0.3 ~ 0.4 0.2 0.4 0.1 24
playsound minecraft:block.rooted_dirt.break hostile @a[distance=..24] ~ ~ ~ 1 0.6
execute as @e[type=minecraft:zombie,tag=rpg.te.hol,distance=..1] at @s run function #rpg:town_dress
