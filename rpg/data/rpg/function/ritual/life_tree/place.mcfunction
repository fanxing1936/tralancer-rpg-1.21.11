# 由玩家执行：阵心落在脚下，美丽/Tiphereth 位于中心，朝玩家视线前方展开。
execute unless entity @s[type=minecraft:player] run return 0
execute if entity @e[type=minecraft:marker,tag=rpg.ritual.life_tree,distance=..2,limit=1] run tellraw @s ["",{"text":"[秘仪] ","color":"#D596F2","bold":true,"italic":false},{"text":"此处已有生命之树阵心。","color":"gray","bold":false,"italic":false}]
execute if entity @e[type=minecraft:marker,tag=rpg.ritual.life_tree,distance=..2,limit=1] run return 0
summon minecraft:marker ~ ~0.02 ~ {Tags:["rpg.ritual.life_tree","rpg.ritual.life_tree.new"],CustomName:'{"text":"生命之树 · 粒子阵锚","color":"#D596F2","italic":false}'}
execute store result entity @e[type=minecraft:marker,tag=rpg.ritual.life_tree.new,distance=..2,limit=1,sort=nearest] Rotation[0] float 1 run data get entity @s Rotation[0] 1
data modify entity @e[type=minecraft:marker,tag=rpg.ritual.life_tree.new,distance=..2,limit=1,sort=nearest] Rotation[1] set value 0.0f
tag @e[type=minecraft:marker,tag=rpg.ritual.life_tree.new,distance=..2,limit=1,sort=nearest] remove rpg.ritual.life_tree.new
scoreboard players set @e[type=minecraft:marker,tag=rpg.ritual.life_tree,distance=..2,limit=1,sort=nearest] rpg_lt_fill 0
scoreboard players set #life_tree rpg_lt_tick 0
execute as @e[type=minecraft:marker,tag=rpg.ritual.life_tree,distance=..2,limit=1,sort=nearest] at @s run function rpg:ritual/life_tree/draw
playsound minecraft:block.beacon.activate ambient @s ~ ~ ~ 0.55 1.35
tellraw @s ["",{"text":"[秘仪] ","color":"#D596F2","bold":true,"italic":false},{"text":"生命之树已沿你的朝向平铺于地面。","color":"#FFF2A8","bold":false,"italic":false}]
