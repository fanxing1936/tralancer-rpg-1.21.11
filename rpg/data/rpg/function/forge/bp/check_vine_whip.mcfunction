# 核对藤蔓之鞭的材料：#ok 1 = 够
scoreboard players set #ok rpg_fg 0
execute unless score @s rpg_sef matches 4.. run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　原质要到第 4 阶才能锻[史诗]","color":"#C04A3C","bold":false,"italic":false}]
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"blank"}] run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　主手要拿着器胚","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"sp_stone"}] 0
execute unless score #c rpg_fg matches 1.. run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　山岩之心不够（要 1）","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:diamond[!minecraft:custom_data] 0
execute unless score #c rpg_fg matches 6.. run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　钻石不够（要 6）","color":"#C04A3C","bold":false,"italic":false}]
execute store result score #c rpg_fg run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] 0
execute unless score #c rpg_fg matches 4.. run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　残魂不够（要 4）","color":"#C04A3C","bold":false,"italic":false}]
scoreboard players set #ok rpg_fg 1
