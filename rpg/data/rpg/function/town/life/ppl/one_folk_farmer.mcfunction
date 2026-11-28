summon minecraft:villager ~ ~ ~ {Tags:["rpg.tnpc","rpg.tnpc.folk","rpg.tl.new","rpg.tl.notrade","rpg.tnpc.farmer"],NoAI:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b,CanPickUpLoot:0b,CustomNameVisible:0b,CustomName:{"text":"𝔉𝔞𝔯𝔪𝔢𝔯","color":"#404040","bold":false,"italic":false},VillagerData:{type:"minecraft:plains",profession:"minecraft:none",level:1},Offers:{Recipes:[]}}
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.tnpc.plate","rpg.tl.pnew"],billboard:"center",text:["",{"text":"农夫","color":"#E6DFCF","bold":true,"italic":false},{"text":"\n𝔉𝔞𝔯𝔪𝔢𝔯","color":"#8F7430","bold":false,"italic":false}],transformation:{translation:[0f,0.62f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f]}}
ride @e[type=minecraft:text_display,tag=rpg.tl.pnew,limit=1,sort=nearest] mount @e[type=minecraft:villager,tag=rpg.tl.new,limit=1,sort=nearest]
tag @e[type=minecraft:text_display,tag=rpg.tl.pnew] remove rpg.tl.pnew
scoreboard players operation @e[type=minecraft:villager,tag=rpg.tl.new] rpg_tw_id = #built rpg_tw
execute as @e[type=minecraft:villager,tag=rpg.tl.new] store result entity @s Rotation[0] float 1 run random value -180..179
execute as @e[type=minecraft:villager,tag=rpg.tl.new] at @s run function #rpg:town_dress
tag @e[type=minecraft:villager,tag=rpg.tl.new] remove rpg.tl.new
