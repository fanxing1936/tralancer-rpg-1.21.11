# 慈悲柱第 7 阶：受致命伤时 3 秒抗性 II，冷却 3 分钟（as 挨打的玩家）
execute if score @s rpg_sef_lcd matches 1.. run return 0
execute store result score #hp rpg_sef run data get entity @s Health
execute unless score #hp rpg_sef matches ..6 run return 0
effect give @s minecraft:resistance 3 1 true
scoreboard players set @s rpg_sef_lcd 180
playsound minecraft:item.shield.block player @s ~ ~ ~ 1 0.6
