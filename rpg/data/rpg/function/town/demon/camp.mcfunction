# 林中营地（as 营地锚点，at 它）
summon minecraft:villager ~2 ~ ~ {Tags:["rpg.tnpc","rpg.tnpc.witch","rpg.dm.camp","rpg.tl.new"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,CustomName:{"text":"女巫","color":"#B48AD8","bold":true,"italic":false},VillagerData:{type:"minecraft:swamp",profession:"minecraft:none",level:1}}
summon minecraft:villager ~-2 ~ ~1 {Tags:["rpg.tnpc","rpg.tnpc.hood","rpg.dm.camp","rpg.tl.new"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,CustomName:{"text":"兜帽人","color":"#D596F2","bold":true,"italic":false},VillagerData:{type:"minecraft:swamp",profession:"minecraft:none",level:1}}
summon minecraft:interaction ~ ~ ~-4 {Tags:["rpg.tnpc","rpg.tnpc.altar","rpg.tl.new"],width:1.6f,height:1.2f,response:1b}
summon minecraft:text_display ~ ~1.6 ~-4 {Tags:["rpg.tnpc.plate"],billboard:"center",text:["",{"text":"林中祭坛","color":"#A276BE","bold":true,"italic":false},{"text":"\n𝔄𝔩𝔱𝔞𝔯","color":"#8F7430","bold":false,"italic":false}]}
execute positioned ~-1 ~ ~-4 run function rpg:town/prop {n:"candles_a"}
execute positioned ~1 ~ ~-4 run function rpg:town/prop {n:"candles_b"}
execute positioned ~3 ~ ~2 run function rpg:town/prop {n:"cauldron"}
scoreboard players operation @e[tag=rpg.tl.new,distance=..6] rpg_tw_id = #built rpg_tw
execute as @e[type=minecraft:villager,tag=rpg.tl.new,distance=..6] store result entity @s Rotation[0] float 1 run random value -180..179
execute as @e[type=minecraft:villager,tag=rpg.tl.new,distance=..6] at @s run function #rpg:town_dress
tag @e[tag=rpg.tl.new,distance=..6] remove rpg.tl.new
