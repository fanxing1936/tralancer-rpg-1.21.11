tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:item,distance=..6] if items entity @s contents #rpg:rite_media run tag @s add rpg.counter.food
execute if entity @e[type=minecraft:item,tag=rpg.counter.food,distance=..6,limit=1] run return run function rpg:inquest/counter/beelzebub_eat
execute unless entity @e[type=minecraft:item,tag=rpg.counter.food,distance=..6,limit=1] run tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"〖反仪式・暴食〗","color":"#8CA83D","bold":true,"italic":false},{"text":" 𝔊𝔩𝔲𝔱𝔱𝔬𝔫𝔶","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"别西卜没有找到可吞食的媒介。","color":"#9C9A94","italic":false}]
tag @e[type=minecraft:item,tag=rpg.counter.food,distance=..6] remove rpg.counter.food
tag @s remove rpg.rite.anchor.active
