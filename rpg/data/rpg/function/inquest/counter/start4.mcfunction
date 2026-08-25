tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:item,distance=..6] if items entity @s contents #rpg:rite_media run tag @s add rpg.counter.food
execute if entity @e[type=minecraft:item,tag=rpg.counter.food,distance=..6,limit=1] run return run function rpg:inquest/counter/beelzebub_eat
execute unless entity @e[type=minecraft:item,tag=rpg.counter.food,distance=..6,limit=1] run tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"[反仪式·暴食] ","color":"#DCEB72","bold":true,"italic":false},{"text":"别西卜没有找到可吞食的媒介。","color":"gray","italic":false}]
tag @e[type=minecraft:item,tag=rpg.counter.food,distance=..6] remove rpg.counter.food
tag @s remove rpg.rite.anchor.active
