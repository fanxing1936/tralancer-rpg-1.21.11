# 右键祭坛（as/at 玩家）
execute if entity @s[tag=rpg.dm] run return run tellraw @s ["",{"text":"〖林中营地〗","color":"#A276BE","bold":true,"italic":false},{"text":"  你已经是这边的人了。","color":"#A276BE","bold":false,"italic":false}]
execute if score @s rpg_ident matches 3.. unless score @s rpg_ident matches 4 run return run tellraw @s ["",{"text":"〖林中营地〗","color":"#A276BE","bold":true,"italic":false},{"text":"  祭坛对你毫无反应。侍奉神的人不能入伙。","color":"#797979","bold":false,"italic":false}]
execute unless entity @s[tag=rpg.tl.camp] run return run tellraw @s ["",{"text":"〖林中营地〗","color":"#A276BE","bold":true,"italic":false},{"text":"  你还不知道这座祭坛是做什么的。","color":"#797979","bold":false,"italic":false}]
execute store result score #tod rpg_dm run time query daytime
execute unless score #tod rpg_dm matches 13000..23000 run return run tellraw @s ["",{"text":"〖林中营地〗","color":"#A276BE","bold":true,"italic":false},{"text":"  仪式要在夜里做。","color":"#FF6B5E","bold":false,"italic":false}]
execute unless items entity @s weapon.mainhand minecraft:candle[minecraft:custom_data~{rpg_black_candle:1b}] run return run tellraw @s ["",{"text":"〖林中营地〗","color":"#A276BE","bold":true,"italic":false},{"text":"  拿着黑蜡烛右键祭坛。","color":"#FF6B5E","bold":false,"italic":false}]
execute store result score #s rpg_dm run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"sin_shard"}] 0
execute if score #s rpg_dm matches ..2 run return run tellraw @s ["",{"text":"〖林中营地〗","color":"#A276BE","bold":true,"italic":false},{"text":"  还差罪印碎片（要 3 片，哪一柱的都行）。","color":"#FF6B5E","bold":false,"italic":false}]
function rpg:town/demon/rite
