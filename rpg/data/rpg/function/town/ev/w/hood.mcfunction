summon minecraft:villager ~ ~ ~ {Tags:["rpg.tw.ev","rpg.tnpc","rpg.tnpc.hood","rpg.te.hood"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,CustomName:{"text":"兜帽人","color":"#D596F2","bold":true,"italic":false},VillagerData:{type:"minecraft:swamp",profession:"minecraft:none",level:1}}
execute as @e[type=minecraft:villager,tag=rpg.te.hood,distance=..1] at @s run function #rpg:town_dress
