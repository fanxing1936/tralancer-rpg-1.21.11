tag @s remove rpg.dm.job
scoreboard players set @s rpg_dm 0
scoreboard players add @s rpg_dm_rep 10
loot give @s loot rpg:world/sin_shard_6
loot give @s loot rpg:world/currency
particle minecraft:smoke ~ ~1.5 ~ 0.4 0.3 0.4 0.01 20
tellraw @s ["",{"text":"〖林中营地〗","color":"#A276BE","bold":true,"italic":false},{"text":"  教堂门口的蜡烛灭了。没有人看见你。","color":"#A276BE","bold":false,"italic":false}]
