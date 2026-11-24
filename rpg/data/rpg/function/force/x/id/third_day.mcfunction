# 受致命伤（打完剩 5 点以内）时原地半血复生，每 20 分钟一次
execute if score @s rpg_fo_3d > #now rpg_fo run return 0
execute store result score #h rpg_fo run data get entity @s Health
execute unless score #h rpg_fo matches ..5 run return 0
scoreboard players operation @s rpg_fo_3d = #now rpg_fo
scoreboard players add @s rpg_fo_3d 24000
effect give @s minecraft:instant_health 1 2 true
effect give @s minecraft:resistance 3 4 true
effect give @s minecraft:regeneration 6 1 true
playsound minecraft:block.beacon.activate player @a[distance=..24] ~ ~ ~ 1 1.8
particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.8 0.4 0.4 50
title @s times 5 40 15
title @s title {"text":"第三日","color":"#C9A646","bold":true,"italic":false}
title @s subtitle {"text":"你从死亡里站了起来（20 分钟一次）","color":"#9C9A94","bold":false,"italic":false}
