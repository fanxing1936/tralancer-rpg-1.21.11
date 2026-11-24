# 新版本第一次见到这名玩家（as 玩家）：拆旧角色等级的血、按经验等级折阅历、驱魔等级换成裁决次数
scoreboard players set @s rpg_sef_mig 1
attribute @s minecraft:max_health modifier remove minecraft:64
attribute @s minecraft:max_health modifier remove minecraft:32
attribute @s minecraft:max_health modifier remove minecraft:16
attribute @s minecraft:max_health modifier remove minecraft:8
attribute @s minecraft:max_health modifier remove minecraft:4
attribute @s minecraft:max_health modifier remove minecraft:2
attribute @s minecraft:max_health modifier remove minecraft:1
attribute @s minecraft:max_health modifier remove minecraft:0
scoreboard players set @s rpg_hp_level 0
execute store result score #xl rpg_sef run experience query @s levels
scoreboard players operation #xl rpg_sef *= #3 rpg_sef
execute if score #xl rpg_sef matches 101.. run scoreboard players set #xl rpg_sef 100
scoreboard players operation @s rpg_ex_xp += #xl rpg_sef
execute if score #xl rpg_sef matches 1.. run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"旧的角色等级已经并入原质：按经验等级折算阅历 +","color":"#E6DFCF","bold":false,"italic":false},{"score":{"name":"#xl","objective":"rpg_sef"},"color":"#C9A646"}]
execute unless score @s rpg_ex_rites matches 1.. if score @s rpg_ex_lvl matches 2 run scoreboard players set @s rpg_ex_rites 1
execute unless score @s rpg_ex_rites matches 1.. if score @s rpg_ex_lvl matches 3..4 run scoreboard players set @s rpg_ex_rites 3
execute unless score @s rpg_ex_rites matches 1.. if score @s rpg_ex_lvl matches 5.. run scoreboard players set @s rpg_ex_rites 6
scoreboard players add @s rpg_ex_rites 0
